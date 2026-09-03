"""Tests for git_adapter.py.

Run it with:

    python test_git_adapter.py

The subprocess stand-in returns BYTES, because git_adapter asks subprocess.run
for raw output and performs the decode itself.
"""

import subprocess
from pathlib import Path
from unittest.mock import patch

from git_adapter import (
    GitCaptureError,
    capture_new_file_diff,
    capture_repository_root,
    capture_staged_diff,
    capture_unstaged_diff,
    capture_untracked_paths,
)


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
STAGED_DIFF = (
    "diff --git a/notes.md b/notes.md\n"
    "index 3333333..4444444 100644\n"
    "--- a/notes.md\n"
    "+++ b/notes.md\n"
    "@@ -1 +1,2 @@\n"
    " intro\n"
    "+staged line\n"
)


def completed(returncode=0, stdout=b"", stderr=b""):
    return subprocess.CompletedProcess(
        args=["git", "diff"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_capture_unstaged_diff_runs_expected_command_and_returns_stdout():
    prepared = completed(stdout=UNSTAGED_DIFF.encode("utf-8"))

    with patch("git_adapter.subprocess.run", return_value=prepared) as fake_run:
        result = capture_unstaged_diff(REPOSITORY)

    assert result == UNSTAGED_DIFF
    fake_run.assert_called_once_with(
        ["git", "diff", "--no-ext-diff", "--no-color", "--"],
        cwd=REPOSITORY,
        capture_output=True,
        timeout=10,
        shell=False,
    )


def test_capture_unstaged_diff_rejects_unexpected_status():
    prepared = completed(returncode=2, stderr=b"fatal: failed")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_unstaged_diff(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "UNSTAGED tracked: Git failed with status 2: fatal: failed"
            )
        else:
            raise AssertionError("capture_unstaged_diff did not reject status 2")


def test_capture_rejects_undecodable_output_with_its_component_label():
    prepared = completed(stdout=b"diff --git a/caf\xe9.py b/caf\xe9.py\n")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_staged_diff(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "STAGED tracked: Git output was not valid UTF-8 text"
            )
        else:
            raise AssertionError(
                "capture_staged_diff did not reject undecodable output"
            )


def test_capture_staged_diff_runs_expected_command_and_returns_stdout():
    prepared = completed(stdout=STAGED_DIFF.encode("utf-8"))

    with patch("git_adapter.subprocess.run", return_value=prepared) as fake_run:
        result = capture_staged_diff(REPOSITORY)

    assert result == STAGED_DIFF
    fake_run.assert_called_once_with(
        ["git", "diff", "--no-ext-diff", "--no-color", "--cached", "--"],
        cwd=REPOSITORY,
        capture_output=True,
        timeout=10,
        shell=False,
    )


def test_capture_staged_diff_rejects_unexpected_status_with_its_own_label():
    prepared = completed(returncode=128, stderr=b"fatal: not a repository")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_staged_diff(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "STAGED tracked: Git failed with status 128: "
                "fatal: not a repository"
            )
        else:
            raise AssertionError("capture_staged_diff did not reject status 128")


def test_capture_untracked_paths_runs_expected_command_and_splits_lines():
    prepared = completed(stdout=b"notes/new.py\nreadme.md\n")

    with patch("git_adapter.subprocess.run", return_value=prepared) as fake_run:
        result = capture_untracked_paths(REPOSITORY)

    assert result == ["notes/new.py", "readme.md"]
    fake_run.assert_called_once_with(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=REPOSITORY,
        capture_output=True,
        timeout=10,
        shell=False,
    )


def test_capture_untracked_paths_returns_empty_list_when_none_exist():
    prepared = completed(stdout=b"")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        result = capture_untracked_paths(REPOSITORY)

    assert result == []


def test_capture_untracked_paths_rejects_unexpected_status():
    prepared = completed(returncode=129, stderr=b"usage: git ls-files")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_untracked_paths(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "UNTRACKED discovery: Git failed with status 129: "
                "usage: git ls-files"
            )
        else:
            raise AssertionError("capture_untracked_paths did not reject status 129")


def test_capture_repository_root_runs_expected_command_and_strips_newline():
    prepared = completed(stdout=b"C:/projects/example\n")

    with patch("git_adapter.subprocess.run", return_value=prepared) as fake_run:
        result = capture_repository_root(REPOSITORY)

    assert result == "C:/projects/example"
    fake_run.assert_called_once_with(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=REPOSITORY,
        capture_output=True,
        timeout=10,
        shell=False,
    )


def test_capture_repository_root_rejects_unexpected_status():
    prepared = completed(returncode=128, stderr=b"fatal: not a git repository")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_repository_root(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "ROOT resolution: Git failed with status 128: "
                "fatal: not a git repository"
            )
        else:
            raise AssertionError("capture_repository_root did not reject status 128")


NEW_FILE_DIFF = (
    "diff --git a/brand_new.py b/brand_new.py\n"
    "new file mode 100644\n"
    "index 0000000..687c3e2\n"
    "--- /dev/null\n"
    "+++ b/brand_new.py\n"
    "@@ -0,0 +1 @@\n"
    "+print('ready')\n"
)


def test_capture_new_file_diff_runs_expected_command_and_accepts_status_1():
    prepared = completed(returncode=1, stdout=NEW_FILE_DIFF.encode("utf-8"))

    with patch("git_adapter.subprocess.run", return_value=prepared) as fake_run:
        result = capture_new_file_diff(REPOSITORY, "brand_new.py")

    assert result == NEW_FILE_DIFF
    fake_run.assert_called_once_with(
        [
            "git",
            "diff",
            "--no-ext-diff",
            "--no-color",
            "--no-index",
            "--",
            "/dev/null",
            "brand_new.py",
        ],
        cwd=REPOSITORY,
        capture_output=True,
        timeout=10,
        shell=False,
    )


def test_capture_new_file_diff_also_accepts_status_0():
    prepared = completed(returncode=0, stdout=b"")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        assert capture_new_file_diff(REPOSITORY, "same.py") == ""


def test_capture_new_file_diff_rejects_a_genuine_error_status():
    prepared = completed(returncode=128, stderr=b"fatal: cannot read file")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_new_file_diff(REPOSITORY, "brand_new.py")
        except GitCaptureError as error:
            assert str(error) == (
                "UNTRACKED brand_new.py: Git failed with status 128: "
                "fatal: cannot read file"
            )
        else:
            raise AssertionError("capture_new_file_diff did not reject status 128")


def test_status_1_still_fails_for_the_tracked_diff_captures():
    prepared = completed(returncode=1, stderr=b"fatal: bad revision")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_unstaged_diff(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "UNSTAGED tracked: Git failed with status 1: fatal: bad revision"
            )
        else:
            raise AssertionError("capture_unstaged_diff accepted status 1")


test_capture_unstaged_diff_runs_expected_command_and_returns_stdout()
test_capture_unstaged_diff_rejects_unexpected_status()
test_capture_new_file_diff_runs_expected_command_and_accepts_status_1()
test_capture_new_file_diff_also_accepts_status_0()
test_capture_new_file_diff_rejects_a_genuine_error_status()
test_status_1_still_fails_for_the_tracked_diff_captures()
test_capture_repository_root_runs_expected_command_and_strips_newline()
test_capture_repository_root_rejects_unexpected_status()
test_capture_rejects_undecodable_output_with_its_component_label()
test_capture_staged_diff_runs_expected_command_and_returns_stdout()
test_capture_staged_diff_rejects_unexpected_status_with_its_own_label()
test_capture_untracked_paths_runs_expected_command_and_splits_lines()
test_capture_untracked_paths_returns_empty_list_when_none_exist()
test_capture_untracked_paths_rejects_unexpected_status()
print("test passed")
