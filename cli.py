"""Run BuildLens from a shell.

Contract:
    in        a command line: analyze <path-to-diff-file>
    out       three labelled counts on stdout, one per line
    status    0 when the summary was produced
              1 when the file cannot be read
              2 when argparse rejects the command line
    errors    reported on stderr as a readable line; never a raw traceback

This module owns the process boundary only. Counting stays in summarize.py,
which knows nothing about files, arguments, or exit status.
"""

import argparse
import sys

from summarize import summarize_diff

def read_diff(path: str) -> str:
    """Return the whole text stored in the file named by path."""
    with open(path, encoding="utf-8") as handle:
        diff_text = handle.read()

    return diff_text


def format_summary(summary) -> str:
    """Return the three counts as the lines a user reads."""
    lines = [
        "Files changed: " + str(summary.files_changed),
        "Lines added: " + str(summary.lines_added),
        "Lines removed: " + str(summary.lines_removed),
    ]

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    """Run one command, allowing argparse to exit for malformed syntax."""
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument("action", choices=["analyze"])
    parser.add_argument("path")
    args = parser.parse_args(argv[1:])

    try:
        diff_text = read_diff(args.path)
    except FileNotFoundError:
        print("no such file: " + args.path, file=sys.stderr)
        return 1

    summary = summarize_diff(diff_text)
    print(format_summary(summary))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
