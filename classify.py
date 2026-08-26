"""Classify a single line of unified-diff text.

Contract:
    in        exactly one line of unified-diff text, as a string
    out       exactly one label string
    unchanged the line passed in, and everything outside this call
"""


def classify_diff_line(line):
    if (
        line.startswith("diff --git")
        or line.startswith("index ")
        or line.startswith("--- ")
        or line.startswith("+++ ")
        or line.startswith("@@")
    ):
        return "metadata"
    elif line.startswith("+"):
        return "added"
    elif line.startswith("-"):
        return "removed"
    else:
        return "context"
