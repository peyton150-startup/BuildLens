"""Capture validated Git diff text without leaking Git into the core."""

import subprocess
from pathlib import Path


class GitCaptureError(RuntimeError):
    """Report that one required Git snapshot component could not be captured."""


def capture_unstaged_diff(repository: Path) -> str:
    """Return tracked working-tree diff text for repository."""
    process_result = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--no-color", "--"],
        cwd=repository,
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
    )

    if process_result.returncode != 0:
        detail = process_result.stderr.strip()
        message = (
            "UNSTAGED tracked: Git failed with status "
            + str(process_result.returncode)
        )
        if detail:
            message = message + ": " + detail
        raise GitCaptureError(message)

    return process_result.stdout
