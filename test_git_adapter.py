"""Tests for git_adapter.py.

Run it with:

    python test_git_adapter.py
"""

import subprocess
from pathlib import Path
from unittest.mock import patch

from git_adapter import GitCaptureError, capture_unstaged_diff


REPOSITORY = Path("C:/projects/example")
UNSTAGED_DIFF = (
    "diff --git a/app.py b/app.py\n"
    "index 1111111..2222222 100644\n"
    "--- a/app.py\n"
    "+++ b/app.py\n"
    "@@ -1 +1 @@\n"
    "-old\n"
    "+new\n"
)


def completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=["git", "diff"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_capture_unstaged_diff_runs_expected_command_and_returns_stdout():
    prepared = completed(stdout=UNSTAGED_DIFF)

    with patch("git_adapter.subprocess.run", return_value=prepared) as fake_run:
        result = capture_unstaged_diff(REPOSITORY)

    assert result == UNSTAGED_DIFF
    fake_run.assert_called_once_with(
        ["git", "diff", "--no-ext-diff", "--no-color", "--"],
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
    )


def test_capture_unstaged_diff_rejects_unexpected_status():
    prepared = completed(returncode=2, stderr="fatal: failed")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_unstaged_diff(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "UNSTAGED tracked: Git failed with status 2: fatal: failed"
            )
        else:
            raise AssertionError("capture_unstaged_diff did not reject status 2")


test_capture_unstaged_diff_runs_expected_command_and_returns_stdout()
test_capture_unstaged_diff_rejects_unexpected_status()
print("test passed")
