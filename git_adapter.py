"""Capture validated Git snapshot components without leaking Git into the core."""

import subprocess
from pathlib import Path


class GitCaptureError(RuntimeError):
    """Report that one required Git snapshot component could not be captured."""


def _capture(repository: Path, args: list[str], label: str) -> str:
    """Run one read-only Git command and return its validated stdout."""
    process_result = subprocess.run(
        ["git"] + args,
        cwd=repository,
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
    )

    if process_result.returncode != 0:
        detail = process_result.stderr.strip()
        message = (
            label
            + ": Git failed with status "
            + str(process_result.returncode)
        )
        if detail:
            message = message + ": " + detail
        raise GitCaptureError(message)

    return process_result.stdout


def _diff_args(extra: list[str]) -> list[str]:
    """Build the shared tracked-diff argument list."""
    return ["diff", "--no-ext-diff", "--no-color"] + extra + ["--"]


def capture_unstaged_diff(repository: Path) -> str:
    """Return tracked working-tree diff text for repository."""
    return _capture(repository, _diff_args([]), "UNSTAGED tracked")


def capture_staged_diff(repository: Path) -> str:
    """Return tracked staged diff text for repository."""
    return _capture(repository, _diff_args(["--cached"]), "STAGED tracked")


def capture_untracked_paths(repository: Path) -> list[str]:
    """Return repository-relative paths of untracked, non-ignored files."""
    output = _capture(
        repository,
        ["ls-files", "--others", "--exclude-standard"],
        "UNTRACKED discovery",
    )
    return output.splitlines()
