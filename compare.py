"""Judge one claim from Claude against one observation of the file on disk."""

import hashlib
from enum import Enum

from file_observer import ObservationStatus


class ComparisonVerdict(Enum):
    """What comparing a claim with an observation established about the claim."""

    CLAIM_HOLDS = "claim holds"
    CLAIM_HOLDS_AFTER_NORMALIZE = "claim holds after normalize"
    CLAIM_DOES_NOT_HOLD = "claim does not hold"
    FILE_ABSENT = "file absent"
    INCOMPARABLE = "incomparable"
    STATUS_NOT_ACCEPTED = "status not accepted"


def _normalise_line_endings(data: bytes) -> bytes:
    """Return data with Windows line endings rewritten as Unix ones."""
    return data.replace(b"\r\n", b"\n")


def compare_write(claim, observed) -> ComparisonVerdict:
    """Return what the observation establishes about one Write claim.

    The verdict is about the claim, not a restatement of the observation, and it
    describes the file only at observed.observed_at.
    """
    # First: a claim this function cannot judge is a mistake in the caller, not a
    # fact about the file. Raising stops a batch whose driver is misrouting; a
    # verdict here would let an absent or unreadable file answer confidently for
    # a claim that was never read.
    if claim.tool_name != "Write":
        raise ValueError("compare_write needs a Write claim, got: " + claim.tool_name)

    # Each known status is named explicitly, so the hash comparison below is only
    # ever reached for READ — never by elimination.
    if observed.status is ObservationStatus.UNREADABLE:
        # BuildLens could not look. That is no evidence either way.
        return ComparisonVerdict.INCOMPARABLE

    if observed.status is ObservationStatus.ABSENT:
        # A file that is not there cannot hold the claimed content.
        return ComparisonVerdict.FILE_ABSENT

    if observed.status is ObservationStatus.READ:
        # The claim is text and the file is bytes: encode the claim so the two can
        # be compared. Assumes Claude's Write tool saves UTF-8 — observed for a new
        # file and for overwriting a Latin-1 file, Windows, 2026-09-11
        # (EV-P8-WRITE-ENCODING-OBSERVATION-405). If Write is ever seen saving
        # another encoding, non-ASCII claims here will read "claim does not hold".
        claim_bytes = claim.details["content"].encode("utf-8")

        if observed.content_hash == hashlib.sha256(claim_bytes).hexdigest():
            return ComparisonVerdict.CLAIM_HOLDS

        # Only on a mismatch, and only for a file that was read: Git rewrites line
        # endings on checkout here (core.autocrlf=true), so the same text can reach
        # disk as \r\n. Reported separately rather than as a plain match, so the
        # reader learns the bytes were not identical.
        if _normalise_line_endings(observed.file_bytes) == _normalise_line_endings(claim_bytes):
            return ComparisonVerdict.CLAIM_HOLDS_AFTER_NORMALIZE

        return ComparisonVerdict.CLAIM_DOES_NOT_HOLD

    # A status this function was never taught: a fact about BuildLens's own code.
    # Returned rather than raised, so one unknown status cannot cost a whole batch
    # its verdicts.
    return ComparisonVerdict.STATUS_NOT_ACCEPTED
