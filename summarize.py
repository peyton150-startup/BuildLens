"""Count what a whole diff changed.

Contract:
    in        one string of unified-diff text, as git prints it
    out       one DiffSummary with files_changed, lines_added, lines_removed
    unchanged the string passed in, and everything outside this call
"""

from dataclasses import dataclass

from classify import classify_diff_line


@dataclass
class DiffSummary:
    files_changed: int
    lines_added: int
    lines_removed: int


def summarize_diff(diff_text):
    files_changed = 0
    lines_added = 0
    lines_removed = 0

    for line in diff_text.splitlines():
        label = classify_diff_line(line)
        if label == "file_header":
            files_changed = files_changed + 1
        elif label == "added":
            lines_added = lines_added + 1
        elif label == "removed":
            lines_removed = lines_removed + 1

    return DiffSummary(files_changed, lines_added, lines_removed)
