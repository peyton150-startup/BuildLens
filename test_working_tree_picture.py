"""Real-Git tests for working_tree_picture.py.

Run it with:

    python test_working_tree_picture.py

Rows 1-8 were approved before any of this was written. Every test uses a real
repository and a real disk, because the claims under test — what Git lists and
what the file system holds — are exactly what a stand-in cannot establish.
"""

import hashlib
import subprocess
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

from git_adapter import GitCaptureError
from working_tree_picture import take_picture


def run_git(repository, args):
    """Set up repository state for a test. Not the code under test."""
    subprocess.run(
        ["git"] + args,
        cwd=repository,
        capture_output=True,
        timeout=10,
        shell=False,
        check=True,
    )


def new_repository(directory):
    """Create a repository holding one committed file, tracked.txt."""
    repository = Path(directory)
    run_git(repository, ["init", "--quiet", "."])
    run_git(repository, ["config", "user.email", "test@example.invalid"])
    run_git(repository, ["config", "user.name", "BuildLens Test"])
    (repository / "tracked.txt").write_bytes(b"original\n")
    run_git(repository, ["add", "tracked.txt"])
    run_git(repository, ["commit", "--quiet", "-m", "base"])
    return repository


def temporary_directory():
    # Git marks files under .git/objects read-only, which makes ordinary
    # cleanup fail on Windows. Tolerate that rather than leave the test brittle.
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def test_row_1_a_tracked_readable_file_is_fingerprinted():
    with temporary_directory() as directory:
        repository = new_repository(directory)

        picture = take_picture(repository)

        assert picture.hashes["tracked.txt"] == sha256(b"original\n")
        assert "tracked.txt" not in picture.unreadable


def test_row_2_an_untracked_file_that_is_not_ignored_is_fingerprinted():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "fresh.py").write_bytes(b"print('hi')\n")

        picture = take_picture(repository)

        assert picture.hashes["fresh.py"] == sha256(b"print('hi')\n")


def test_row_3_an_ignored_file_is_not_in_the_picture_at_all():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / ".gitignore").write_bytes(b"*.log\n")
        (repository / "debug.log").write_bytes(b"noise\n")

        picture = take_picture(repository)

        assert "debug.log" not in picture.hashes
        assert "debug.log" not in picture.unreadable


def test_row_4_a_tracked_file_deleted_from_disk_is_in_neither_place():
    # Git still lists it, but the picture is of the WORKING TREE, where it is gone.
    # Leaving it out is what lets reconcile report DELETED against a baseline.
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "tracked.txt").unlink()

        picture = take_picture(repository)

        assert "tracked.txt" not in picture.hashes
        assert "tracked.txt" not in picture.unreadable


def test_row_5_a_tracked_path_that_cannot_be_read_is_unreadable():
    # A folder now sits where the committed file was. Git still lists the path,
    # and opening a folder as a file fails — portably, on every platform.
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "tracked.txt").unlink()
        (repository / "tracked.txt").mkdir()

        picture = take_picture(repository)

        assert "tracked.txt" in picture.unreadable
        assert "tracked.txt" not in picture.hashes


def test_row_6_taken_at_is_one_aware_utc_moment_within_the_call():
    with temporary_directory() as directory:
        repository = new_repository(directory)

        before = datetime.now(timezone.utc)
        picture = take_picture(repository)
        after = datetime.now(timezone.utc)

        assert picture.taken_at.utcoffset() == timedelta(0)
        assert before <= picture.taken_at <= after


def test_row_7_a_subfolder_still_yields_keys_relative_to_the_repository_root():
    # ls-files prints paths relative to the folder it runs in. Run from notes/ it
    # would say "plan.md", which would never match a picture taken from the root.
    with temporary_directory() as directory:
        repository = new_repository(directory)
        notes = repository / "notes"
        notes.mkdir()
        (notes / "plan.md").write_bytes(b"alpha\n")
        run_git(repository, ["add", "notes/plan.md"])
        run_git(repository, ["commit", "--quiet", "-m", "notes"])

        picture = take_picture(notes)

        assert "notes/plan.md" in picture.hashes
        assert "plan.md" not in picture.hashes
        assert "tracked.txt" in picture.hashes


def test_row_8_a_failure_in_git_raises_and_returns_no_partial_picture():
    with temporary_directory() as directory:
        not_a_repository = Path(directory)

        try:
            take_picture(not_a_repository)
        except GitCaptureError:
            pass
        else:
            raise AssertionError("take_picture returned a picture from no repository")


test_row_1_a_tracked_readable_file_is_fingerprinted()
test_row_2_an_untracked_file_that_is_not_ignored_is_fingerprinted()
test_row_3_an_ignored_file_is_not_in_the_picture_at_all()
test_row_4_a_tracked_file_deleted_from_disk_is_in_neither_place()
test_row_5_a_tracked_path_that_cannot_be_read_is_unreadable()
test_row_6_taken_at_is_one_aware_utc_moment_within_the_call()
test_row_7_a_subfolder_still_yields_keys_relative_to_the_repository_root()
test_row_8_a_failure_in_git_raises_and_returns_no_partial_picture()
print("test passed")
