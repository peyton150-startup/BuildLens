"""Real-Git tests for git_adapter.py.

Run it with:

    python test_git_adapter_integration.py

These launch actual Git child processes against throwaway repositories, so they
are slower than test_git_adapter.py and require Git on PATH. They exist to prove
claims a controlled stand-in cannot establish: that Git accepts the arguments
BuildLens sends, and what Git actually writes to stdout.

Keep exact-argument and prepared-result assertions in test_git_adapter.py.
"""

import subprocess
import tempfile
from pathlib import Path

from git_adapter import (
    GitCaptureError,
    capture_new_file_diff,
    capture_repository_root,
    capture_staged_diff,
    capture_unstaged_diff,
    capture_untracked_paths,
)


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
    """Create a repository holding one committed file."""
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


def test_git_accepts_the_arguments_and_a_clean_repository_reports_nothing():
    with temporary_directory() as directory:
        repository = new_repository(directory)

        assert capture_unstaged_diff(repository) == ""
        assert capture_staged_diff(repository) == ""
        assert capture_untracked_paths(repository) == []


def test_a_modified_tracked_file_appears_in_unstaged_and_not_in_staged():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "tracked.txt").write_bytes(b"changed\n")

        unstaged = capture_unstaged_diff(repository)

        assert "diff --git a/tracked.txt b/tracked.txt" in unstaged
        assert "+changed" in unstaged
        assert capture_staged_diff(repository) == ""


def test_staging_moves_the_change_from_unstaged_to_staged():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "tracked.txt").write_bytes(b"changed\n")
        run_git(repository, ["add", "tracked.txt"])

        staged = capture_staged_diff(repository)

        assert "diff --git a/tracked.txt b/tracked.txt" in staged
        assert "+changed" in staged
        assert capture_unstaged_diff(repository) == ""


def test_untracked_discovery_finds_a_file_that_was_never_added():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "brand_new.py").write_bytes(b"print('hi')\n")

        paths = capture_untracked_paths(repository)

        assert paths == ["brand_new.py"]
        assert "brand_new.py" not in capture_unstaged_diff(repository)


def test_untracked_discovery_reports_an_empty_new_file():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "placeholder.py").write_bytes(b"")

        assert capture_untracked_paths(repository) == ["placeholder.py"]


def test_a_latin_1_working_tree_file_is_rejected_not_silently_mangled():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "tracked.txt").write_bytes(b"caf\xe9 latin1\n")

        try:
            capture_unstaged_diff(repository)
        except GitCaptureError as error:
            assert str(error) == (
                "UNSTAGED tracked: Git output was not valid UTF-8 text"
            )
        else:
            raise AssertionError(
                "capture_unstaged_diff accepted undecodable Git output"
            )


def test_new_file_diff_presents_an_untracked_file_as_added_content():
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "brand_new.py").write_bytes(b"print('ready')\n")

        diff = capture_new_file_diff(repository, "brand_new.py")

        assert "new file mode" in diff
        assert "--- /dev/null" in diff
        assert "+print('ready')" in diff


def test_new_file_diff_of_an_empty_file_has_a_header_and_no_hunk():
    """The approved requirement: an empty untracked file is a visible change.

    Its creation changes repository state even though it contains no lines, so
    it must report as one changed file with zero added and zero removed lines.
    """
    with temporary_directory() as directory:
        repository = new_repository(directory)
        (repository / "placeholder.py").write_bytes(b"")

        diff = capture_new_file_diff(repository, "placeholder.py")

        assert "diff --git" in diff
        assert "new file mode" in diff
        assert "@@" not in diff


def test_repository_root_is_the_repository_directory_itself():
    with temporary_directory() as directory:
        repository = new_repository(directory)

        root = capture_repository_root(repository)

        assert Path(root).resolve() == repository.resolve()


def test_repository_root_reveals_an_ancestor_when_git_searches_upward():
    """Git resolves upward, so a bare directory can belong to a parent repo.

    This is the hazard that reporting the root exists to expose: analyze run
    in a subdirectory may inspect an ancestor repository the user did not mean.
    """
    with temporary_directory() as directory:
        repository = new_repository(directory)
        nested = repository / "deep" / "nested"
        nested.mkdir(parents=True)

        root = capture_repository_root(nested)

        assert Path(root).resolve() == repository.resolve()
        assert Path(root).resolve() != nested.resolve()


test_git_accepts_the_arguments_and_a_clean_repository_reports_nothing()
test_a_modified_tracked_file_appears_in_unstaged_and_not_in_staged()
test_staging_moves_the_change_from_unstaged_to_staged()
test_untracked_discovery_finds_a_file_that_was_never_added()
test_untracked_discovery_reports_an_empty_new_file()
test_a_latin_1_working_tree_file_is_rejected_not_silently_mangled()
test_new_file_diff_presents_an_untracked_file_as_added_content()
test_new_file_diff_of_an_empty_file_has_a_header_and_no_hunk()
test_repository_root_is_the_repository_directory_itself()
test_repository_root_reveals_an_ancestor_when_git_searches_upward()
print("test passed")
