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
import json
import sys
from datetime import datetime, tzinfo
from pathlib import Path

import completeflow
import snapshot
from git_adapter import GitCaptureError


def format_local_time(moment: datetime, zone: tzinfo | None = None) -> str:
    """Return a stored moment as 12-hour time in zone, or the machine's zone.

    Records hold aware UTC moments. This is the only place one is converted,
    so travelling changes what a person sees and never what was recorded.
    """
    return moment.astimezone(zone).strftime("%I:%M %p %Z")


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


def format_complete_compare(result) -> str:
    """Return one comparison as the lines a user reads.

    The verdict comes first because it is the answer; the path says which file
    it is about, and the status and time say what was seen and when.
    """
    lines = [
        result.verdict.value,
        result.claim.file_path,
        result.observed.status.value
        + ", observed at "
        + format_local_time(result.observed.observed_at),
    ]

    return "\n".join(lines)


def read_payload_text(payload_path: str | None) -> str:
    """Return the payload text from a file, or from standard input."""
    if payload_path is None:
        # What a PostToolUse hook does: pipe its JSON to the command.
        return sys.stdin.read()

    with open(payload_path, encoding="utf-8") as handle:
        return handle.read()


def ingest(payload_path: str | None) -> int:
    """Run one payload through the observation boundary and report the verdict.

    A verdict is the successful outcome even when it is "claim does not hold":
    the check ran and reported a finding. Status 1 is reserved for BuildLens
    being unable to produce a verdict at all.
    """
    try:
        payload_text = read_payload_text(payload_path)
    except OSError as error:
        print(str(error), file=sys.stderr)
        return 1

    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as error:
        print("The payload is not valid JSON: " + str(error), file=sys.stderr)
        return 1

    try:
        result = completeflow.start_flow(payload)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    if result is None:
        print("nothing to check: this tool call named no file")
        return 0

    print(format_complete_compare(result))

    return 0


def report_failure(error: GitCaptureError) -> None:
    """Explain which component failed, and where, without any counts."""
    if error.repository_root is not None:
        print("Repository: " + error.repository_root, file=sys.stderr)

    print(str(error), file=sys.stderr)
    print("Run buildlens analyze again.", file=sys.stderr)


def main(argv: list[str]) -> int:
    """Run one command, allowing argparse to exit for malformed syntax."""
    parser = argparse.ArgumentParser(prog=argv[0])
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("analyze")
    ingest_parser = actions.add_parser("ingest")
    ingest_parser.add_argument("payload", nargs="?")

    args = parser.parse_args(argv[1:])

    if args.action == "ingest":
        return ingest(args.payload)

    try:
        result = snapshot.capture_snapshot(Path.cwd())
    except GitCaptureError as error:
        report_failure(error)
        return 1

    print(format_snapshot(result))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
