"""First failing test for classify_diff_line.

Run it with:

    python test_classify.py
"""

from classify import classify_diff_line


def test_single_plus_line_is_added():
    result = classify_diff_line("+value = 1")
    assert result == "added"


def test_single_minus_line_is_removed():
    result = classify_diff_line("-green_giant")
    assert result == "removed"


def test_file_header_is_metadata():
    result = classify_diff_line("+++ b/app.py")
    assert result == "metadata"


def test_hunk_marker_is_metadata():
    result = classify_diff_line("@@ -1,2 +1,3 @@")
    assert result == "metadata"


def test_unchanged_line_is_context():
    result = classify_diff_line(" import os")
    assert result == "context"


def test_empty_line_is_context():
    result = classify_diff_line("")
    assert result == "context"


def test_deleted_dashes_line_is_removed():
    result = classify_diff_line("----")
    assert result == "removed"


def test_diff_git_line_is_file_header():
    result = classify_diff_line("diff --git a/config.py b/config.py")
    assert result == "file_header"


test_single_plus_line_is_added()
test_single_minus_line_is_removed()
test_deleted_dashes_line_is_removed()
test_file_header_is_metadata()
test_hunk_marker_is_metadata()
test_unchanged_line_is_context()
test_empty_line_is_context()
test_diff_git_line_is_file_header()
print("test passed")
