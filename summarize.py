"""Count what a whole diff changed.

Contract:
    in        a list of unified-diff lines, each a string
    out       one count
    unchanged the list passed in, and everything outside this call
"""

from classify import classify_diff_line


def count_added_lines(all_lines):
    count = 0
    for line in all_lines:
        if classify_diff_line(line) == "added":
            count = count + 1
    return count


def count_removed_lines(all_lines):
    count = 0
    for line in all_lines:
        if classify_diff_line(line) == "removed":
            count = count + 1
    return count


def count_changed_files(all_lines):
    count = 0
    for line in all_lines:
        if classify_diff_line(line) == "file_header":
            count = count + 1
    return count
