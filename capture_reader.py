"""Read the claims appended to the hook capture file since a remembered position.

The capture hook runs in its own short-lived process and appends each payload to
payload_samples.jsonl, followed by the blank line its `echo` adds. find cannot
receive payloads in memory, so it remembers how many lines the file held at the
baseline and reads only the lines appended after that.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from claude_adapter import ClaimedEdit, parse_post_tool_use


@dataclass(frozen=True)
class CapturedClaim:
    """Hold one claim together with the capture line it came from."""

    line_number: int
    claim: ClaimedEdit


@dataclass(frozen=True)
class SkippedLine:
    """Name a capture line that could not become a claim, and why."""

    line_number: int
    reason: str


@dataclass(frozen=True)
class CaptureRead:
    """Hold what one read of the capture file established."""

    claims: list[CapturedClaim]
    skipped: list[SkippedLine]


def count_complete_lines(capture_path: Path) -> int:
    """Return how many newline-terminated lines the capture file holds.

    A last line without a newline may still be mid-append, so it is not counted:
    once the hook finishes it, it falls inside the next read. A file that does
    not exist yet holds no lines.
    """
    try:
        with open(capture_path, "rb") as handle:
            return sum(1 for line in handle if line.endswith(b"\n"))
    except FileNotFoundError:
        return 0


def read_capture(capture_path: Path, position: int) -> CaptureRead:
    """Return the claims and skipped lines after the first `position` lines.

    OSError propagates: whether a capture file missing at the witness stops find
    or offers a retry is the caller's decision, not the reader's.
    """
    claims = []
    skipped = []

    with open(capture_path, "rb") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line_number <= position:
                continue

            if not line.endswith(b"\n"):
                # Only the last line can lack a newline, and the hook may still
                # be writing it; calling it invalid would state an unobserved fact.
                skipped.append(SkippedLine(line_number, "still being written"))
                continue

            if line.strip() == b"":
                # The separator the hook's `echo` writes. Judged by content, not
                # by position, so a change in the hook's layout drops no claim.
                continue

            try:
                payload = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                skipped.append(SkippedLine(line_number, "not valid JSON"))
                continue

            if isinstance(payload, dict) and payload.get("hook_event_name") != "PostToolUse":
                # A proposal or another event: never a claim about the disk.
                continue

            try:
                claim = parse_post_tool_use(payload)
            except ValueError as error:
                skipped.append(SkippedLine(line_number, "not a usable claim (" + str(error) + ")"))
                continue

            if claim is not None:
                claims.append(CapturedClaim(line_number, claim))

    return CaptureRead(claims=claims, skipped=skipped)
