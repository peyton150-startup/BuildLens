"""Tests for cli.py.

Run it with:

    python test_cli.py
"""

import os

from cli import format_summary, main, read_diff
from summarize import summarize_diff

SAMPLE_DIFF = """diff --git a/one.py b/one.py
index 111..222 100644
--- a/one.py
+++ b/one.py
@@ -1,2 +1,3 @@
 kept
+added one
-removed one
"""

TEMP_PATH = "_test_cli_sample.diff"


def write_sample():
    with open(TEMP_PATH, "w", encoding="utf-8") as handle:
        handle.write(SAMPLE_DIFF)


def remove_sample():
    os.remove(TEMP_PATH)


def test_read_diff_returns_the_file_contents():
    write_sample()
    try:
        assert read_diff(TEMP_PATH) == SAMPLE_DIFF
    finally:
        remove_sample()


def test_format_summary_labels_all_three_counts():
    summary = summarize_diff(SAMPLE_DIFF)
    text = format_summary(summary)

    assert text.splitlines() == [
        "Files changed: 1",
        "Lines added: 1",
        "Lines removed: 1",
    ]


def test_analyze_on_a_real_file_succeeds():
    write_sample()
    try:
        assert main(["cli.py", "analyze", TEMP_PATH]) == 0
    finally:
        remove_sample()


def test_missing_file_fails_without_raising():
    assert main(["cli.py", "analyze", "_no_such_file.diff"]) == 1


def test_unknown_action_fails():
    write_sample()
    try:
        assert main(["cli.py", "banana", TEMP_PATH]) == 1
    finally:
        remove_sample()


def test_missing_arguments_fail():
    assert main(["cli.py"]) == 1


def test_too_many_arguments_fail():
    assert main(["cli.py", "analyze", "a.diff", "b.diff"]) == 1


test_read_diff_returns_the_file_contents()
test_format_summary_labels_all_three_counts()
test_analyze_on_a_real_file_succeeds()
test_missing_file_fails_without_raising()
test_unknown_action_fails()
test_missing_arguments_fail()
test_too_many_arguments_fail()
print("test passed")
