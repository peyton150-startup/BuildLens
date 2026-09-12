"""Capture validated Git snapshot components without leaking Git into the core."""

import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class GitCaptureError(RuntimeError):
    """Report that one required Git snapshot component could not be captured.

    repository_root is the root Git resolved before the failure, when one was
    resolved at all. It stays None when root resolution is itself what failed,
    so a caller can tell "inspecting the wrong repository" from "no repository".
    """

    repository_root: str | None = None


def _capture(
    repository: Path,
    args: list[str],
    label: str,
    accepted_statuses: tuple[int, ...] = (0,),
) -> str:
    """Run one read-only Git command and return its validated stdout.

    accepted_statuses varies how one run is judged, not what this function does.
    Most Git commands treat any nonzero status as failure, but `diff --no-index`
    documents status 1 as "the files differ", which is a valid result.
    """
    process_result = subprocess.run(
        ["git"] + args,
        cwd=repository,
        capture_output=True,
        timeout=10,
        shell=False,
    )

    if process_result.returncode not in accepted_statuses:
        # stderr is a human diagnostic, never counted data, so a lossy decode
        # is acceptable here where it would not be for stdout.
        detail = process_result.stderr.decode("utf-8", errors="replace").strip()
        message = (
            label
            + ": Git failed with status "
            + str(process_result.returncode)
        )
        if detail:
            message = message + ": " + detail
        raise GitCaptureError(message)

    try:
        return process_result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise GitCaptureError(
            label + ": Git output was not valid UTF-8 text"
        ) from None


class BaseVersionStatus(Enum):
    """What Git could say about the committed version a change was based on."""

    COMMITTED = "committed"
    ABSENT_FROM_HEAD = "absent from head"
    NO_COMMITS = "no commits"
    # Produced by the caller, not here: this function raises and lets the caller
    # decide, because only the caller knows there was no repository to ask about.
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class BaseVersion:
    """Hold the commit and blob a change was based on, and which case applied.

    detail carries Git's own message when the base version could not be read, so
    a later reader is told WHY it is missing and not only that it is.
    """

    status: BaseVersionStatus
    commit: str | None
    blob: str | None
    detail: str | None = None


def _capture_optional(repository: Path, args: list[str], label: str) -> str | None:
    """Return one revision id, or None when Git says there is no such revision.

    Both "this repository has no commits" and "this path is not in HEAD" are
    ordinary situations rather than faults, so a nonzero status is accepted here
    and turned into None — the same shape as `diff --no-index`, where status 1
    means "the files differ".

    --verify --quiet is what makes the answer readable: plain `rev-parse` exits
    128 for a missing revision but still ECHOES the argument on stdout, so
    "HEAD:new.py" would be mistaken for an id. With these flags Git prints the id
    and exits 0, or prints nothing and exits 1.
    """
    output = _capture(
        repository,
        ["rev-parse", "--verify", "--quiet"] + args,
        label,
        accepted_statuses=(0, 1),
    ).strip()

    return output or None


def capture_base_version(repository: Path, relative_path: str) -> BaseVersion:
    """Return the committed version one file's change was based on.

    Asks about HEAD first: without a commit, no question about the file can be
    answered, and a 128 from the file alone cannot tell the two cases apart.
    """
    commit = _capture_optional(repository, ["HEAD"], "BASE commit")
    if commit is None:
        return BaseVersion(BaseVersionStatus.NO_COMMITS, None, None)

    blob = _capture_optional(repository, ["HEAD:" + relative_path], "BASE blob")
    if blob is None:
        return BaseVersion(BaseVersionStatus.ABSENT_FROM_HEAD, commit, None)

    return BaseVersion(BaseVersionStatus.COMMITTED, commit, blob)


def _diff_args(extra: list[str]) -> list[str]:
    """Build the shared tracked-diff argument list."""
    return ["diff", "--no-ext-diff", "--no-color"] + extra + ["--"]


def capture_unstaged_diff(repository: Path) -> str:
    """Return tracked working-tree diff text for repository."""
    return _capture(repository, _diff_args([]), "UNSTAGED tracked")


def capture_staged_diff(repository: Path) -> str:
    """Return tracked staged diff text for repository."""
    return _capture(repository, _diff_args(["--cached"]), "STAGED tracked")


def capture_new_file_diff(repository: Path, path: str) -> str:
    """Return diff text presenting one untracked file as entirely added content.

    Git compares the file against /dev/null, the absent-before side, so the
    result carries a file header and every line as an addition. An empty file
    yields a header with no hunk, which reports as one changed file and zero
    changed lines.
    """
    return _capture(
        repository,
        _diff_args(["--no-index"]) + ["/dev/null", path],
        "UNTRACKED " + path,
        accepted_statuses=(0, 1),
    )


def capture_repository_root(repository: Path) -> str:
    """Return the root of the repository Git resolves from repository.

    Git searches parent directories, so this may be an ancestor of the given
    path. Reporting it lets the learner see which repository was inspected.
    """
    output = _capture(
        repository,
        ["rev-parse", "--show-toplevel"],
        "ROOT resolution",
    )
    return output.strip()


def capture_untracked_paths(repository: Path) -> list[str]:
    """Return repository-relative paths of untracked, non-ignored files."""
    output = _capture(
        repository,
        ["ls-files", "--others", "--exclude-standard"],
        "UNTRACKED discovery",
    )
    return output.splitlines()
