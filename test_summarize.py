"""Tests for summarize.py.

Run it with:

    python test_summarize.py
"""

from summarize import summarize_diff


TWO_FILE_DIFF = (
    "diff --git a/app.py b/app.py\n"
    "index 078ac13..3e779b8 100644\n"
    "--- a/app.py\n"
    "+++ b/app.py\n"
    "@@ -1,2 +1,3 @@\n"
    "-DEBUG = False\n"
    "+import os\n"
    "+DEBUG = True\n"
    " PORT = 8000\n"
    "diff --git a/config.py b/config.py\n"
    "index 7f9f1df..a5501d6 100644\n"
    "--- a/config.py\n"
    "+++ b/config.py\n"
    "@@ -1,2 +1,2 @@\n"
    ' NAME = "buildlens"\n'
    "-RETRIES = 3\n"
    "+RETRIES = 5\n"
)


def test_summarize_diff_reports_all_three_counts():
    result = summarize_diff(TWO_FILE_DIFF)
    assert result.files_changed == 2
    assert result.lines_added == 3
    assert result.lines_removed == 2


test_summarize_diff_reports_all_three_counts()
print("test passed")
