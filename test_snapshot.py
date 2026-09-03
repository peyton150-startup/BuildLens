"""Tests for snapshot.py.

Run it with:

    python test_snapshot.py

snapshot.py runs no Git command itself, so these patch the five capture
functions rather than subprocess. Mechanism belongs to git_adapter and is
tested there; policy belongs here.
"""

from pathlib import Path
from unittest.mock import patch

from git_adapter import GitCaptureError
from snapshot import Snapshot, capture_snapshot
from summarize import DiffSummary


REPOSITORY = Path("C:/projects/example")

TRACKED_UNSTAGED = (
    "diff --git a/app.py b/app.py\n"
    "--- a/app.py\n"
    "+++ b/app.py\n"
    "@@ -1 +1 @@\n"
    "-old\n"
    "+new\n"
)
STAGED = (
    "diff --git a/notes.md b/notes.md\n"
    "--- a/notes.md\n"
    "+++ b/notes.md\n"
    "@@ -1 +1,2 @@\n"
    " intro\n"
    "+staged line\n"
)
NEW_FILE = (
    "diff --git a/brand_new.py b/brand_new.py\n"
    "new file mode 100644\n"
    "--- /dev/null\n"
    "+++ b/brand_new.py\n"
    "@@ -0,0 +1 @@\n"
    "+print('ready')\n"
)
EMPTY_NEW_FILE = (
    "diff --git a/placeholder.py b/placeholder.py\n"
    "new file mode 100644\n"
    "index 0000000..e69de29\n"
)


def patched(unstaged="", staged="", untracked=(), new_file_diffs=None):
    """Patch every capture function snapshot.py calls."""
    new_file_diffs = new_file_diffs or {}
    return (
        patch("git_adapter.capture_repository_root", return_value="C:/projects/example"),
        patch("git_adapter.capture_unstaged_diff", return_value=unstaged),
        patch("git_adapter.capture_staged_diff", return_value=staged),
        patch("git_adapter.capture_untracked_paths", return_value=list(untracked)),
        patch(
            "git_adapter.capture_new_file_diff",
            side_effect=lambda repository, path: new_file_diffs[path],
        ),
    )


def run_with(**kwargs):
    root, unstaged, staged, untracked, new_file = patched(**kwargs)
    with root, unstaged, staged, untracked, new_file:
        return capture_snapshot(REPOSITORY)


def test_clean_repository_reports_two_empty_views_and_the_root():
    result = run_with()

    assert result == Snapshot(
        repository_root="C:/projects/example",
        unstaged=DiffSummary(0, 0, 0),
        staged=DiffSummary(0, 0, 0),
    )


def test_the_two_views_are_counted_separately_and_never_summed():
    result = run_with(unstaged=TRACKED_UNSTAGED, staged=STAGED)

    assert result.unstaged == DiffSummary(1, 1, 1)
    assert result.staged == DiffSummary(1, 1, 0)


def test_untracked_content_is_counted_inside_the_unstaged_view():
    result = run_with(
        unstaged=TRACKED_UNSTAGED,
        untracked=["brand_new.py"],
        new_file_diffs={"brand_new.py": NEW_FILE},
    )

    assert result.unstaged == DiffSummary(2, 2, 1)
    assert result.staged == DiffSummary(0, 0, 0)


def test_an_empty_untracked_file_counts_as_one_changed_file_and_no_lines():
    result = run_with(
        untracked=["placeholder.py"],
        new_file_diffs={"placeholder.py": EMPTY_NEW_FILE},
    )

    assert result.unstaged == DiffSummary(1, 0, 0)


def test_every_untracked_path_is_captured():
    result = run_with(
        untracked=["brand_new.py", "placeholder.py"],
        new_file_diffs={
            "brand_new.py": NEW_FILE,
            "placeholder.py": EMPTY_NEW_FILE,
        },
    )

    assert result.unstaged == DiffSummary(2, 1, 0)


def test_one_failing_component_rejects_the_whole_snapshot():
    root, unstaged, staged, untracked, new_file = patched(
        unstaged=TRACKED_UNSTAGED,
        untracked=["brand_new.py"],
    )
    failing = patch(
        "git_adapter.capture_new_file_diff",
        side_effect=GitCaptureError("UNTRACKED brand_new.py: Git failed with status 128"),
    )

    with root, unstaged, staged, untracked, failing:
        try:
            capture_snapshot(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "UNTRACKED brand_new.py: Git failed with status 128"
            )
        else:
            raise AssertionError("capture_snapshot returned a partial snapshot")


test_clean_repository_reports_two_empty_views_and_the_root()
test_the_two_views_are_counted_separately_and_never_summed()
test_untracked_content_is_counted_inside_the_unstaged_view()
test_an_empty_untracked_file_counts_as_one_changed_file_and_no_lines()
test_every_untracked_path_is_captured()
test_one_failing_component_rejects_the_whole_snapshot()
print("test passed")
