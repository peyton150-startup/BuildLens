"""Tests for summarize.py.

Run it with:

    python test_summarize.py
"""

from summarize import (
    count_added_lines,
    count_changed_files,
    count_removed_lines,
    summarize_diff,
)


TWO_FILE_DIFF = [
    "diff --git a/app.py b/app.py",
    "index 078ac13..3e779b8 100644",
    "--- a/app.py",
    "+++ b/app.py",
    "@@ -1,2 +1,3 @@",
    "-DEBUG = False",
    "+import os",
    "+DEBUG = True",
    " PORT = 8000",
    "diff --git a/config.py b/config.py",
    "index 7f9f1df..a5501d6 100644",
    "--- a/config.py",
    "+++ b/config.py",
    "@@ -1,2 +1,2 @@",
    ' NAME = "buildlens"',
    "-RETRIES = 3",
    "+RETRIES = 5",
]


def test_two_file_diff_has_three_added_lines():
    result = count_added_lines(TWO_FILE_DIFF)
    assert result == 3


def test_two_file_diff_has_two_removed_lines():
    result = count_removed_lines(TWO_FILE_DIFF)
    assert result == 2


def test_two_file_diff_has_two_changed_files():
    result = count_changed_files(TWO_FILE_DIFF)
    assert result == 2


def test_summarize_diff_reports_all_three_counts():
    result = summarize_diff(TWO_FILE_DIFF)
    assert result.files_changed == 2
    assert result.lines_added == 3
    assert result.lines_removed == 2


test_two_file_diff_has_three_added_lines()
test_two_file_diff_has_two_removed_lines()
test_two_file_diff_has_two_changed_files()
test_summarize_diff_reports_all_three_counts()
print("test passed")
