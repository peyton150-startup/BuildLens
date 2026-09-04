"""Run BuildLens from a shell.

Contract:
    in        a command line: analyze
              the repository is resolved from the current working directory
    out       the resolved repository root, then separately labelled UNSTAGED
              and STAGED sections, three counts each
    status    0 when the whole snapshot was produced
              1 when any snapshot component failed
              2 when argparse rejects the command line
    errors    reported on stderr as readable lines; never a raw traceback
              no partial summary is ever printed

This module owns the process boundary only. Counting stays in summarize.py and
the snapshot policy stays in snapshot.py; neither knows about arguments,
streams, or exit status.
"""

import argparse
import sys
from pathlib import Path

import snapshot
from git_adapter import GitCaptureError


def format_summary(summary) -> str:
    """Return the three counts as the lines a user reads."""
    lines = [
        "Files changed: " + str(summary.files_changed),
        "Lines added: " + str(summary.lines_added),
        "Lines removed: " + str(summary.lines_removed),
    ]

    return "\n".join(lines)


def format_snapshot(result) -> str:
    """Return the whole snapshot as the block a user reads."""
    sections = [
        "Repository: " + result.repository_root,
        "",
        "UNSTAGED",
        format_summary(result.unstaged),
        "",
        "STAGED",
        format_summary(result.staged),
    ]

    return "\n".join(sections)


def report_failure(error: GitCaptureError) -> None:
    """Explain which component failed, and where, without any counts."""
    if error.repository_root is not None:
        print("Repository: " + error.repository_root, file=sys.stderr)

    print(str(error), file=sys.stderr)
    print("Run buildlens analyze again.", file=sys.stderr)


def main(argv: list[str]) -> int:
    """Run one command, allowing argparse to exit for malformed syntax."""
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument("action", choices=["analyze"])
    parser.parse_args(argv[1:])

    try:
        result = snapshot.capture_snapshot(Path.cwd())
    except GitCaptureError as error:
        report_failure(error)
        return 1

    print(format_snapshot(result))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
