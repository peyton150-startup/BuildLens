"""Capture validated Git diff text without leaking Git into the core."""

import subprocess
from pathlib import Path


class GitCaptureError(RuntimeError):
    """Report that one required Git snapshot component could not be captured."""


def _capture(repository: Path, extra_args: list[str], label: str) -> str:
    """Run one read-only Git diff command and return its validated stdout."""
    process_result = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--no-color"] + extra_args + ["--"],
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


def capture_unstaged_diff(repository: Path) -> str:
    """Return tracked working-tree diff text for repository."""
    return _capture(repository, [], "UNSTAGED tracked")


def capture_staged_diff(repository: Path) -> str:
    """Return tracked staged diff text for repository."""
    return _capture(repository, ["--cached"], "STAGED tracked")
