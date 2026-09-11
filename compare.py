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


def _edit_landed(file_bytes: bytes, old_bytes: bytes, new_bytes: bytes) -> bool:
    """Return whether the file shows what a successful edit would leave behind.

    Containment, not equality: an Edit claim names two fragments, never the whole
    file, so this is all the claim can establish.
    """
    if new_bytes not in file_bytes:
        return False

    # The Edit tool refuses a non-unique old_string unless replace_all is set
    # (observed, EV-P8-EDIT-UNIQUENESS-OBSERVATION-428), and a refused edit writes
    # no record. So every claim we hold replaced either its one occurrence or all
    # of them, and old_string should be gone either way — which is why replace_all
    # is never read here. The exception: an old_string the new text contains is
    # expected to survive.
    if old_bytes in new_bytes:
        return True

    return old_bytes not in file_bytes


def compare_edit(claim, observed) -> ComparisonVerdict:
    """Return what the observation establishes about one Edit claim.

    CLAIM_HOLDS here means the expected text is present and the replaced text is
    gone. It is not proof that Claude made the change, any more than a matching
    hash proved authorship for a Write.
    """
    if claim.tool_name != "Edit":
        raise ValueError("compare_edit needs an Edit claim, got: " + claim.tool_name)

    if observed.status is ObservationStatus.UNREADABLE:
        return ComparisonVerdict.INCOMPARABLE

    if observed.status is ObservationStatus.ABSENT:
        return ComparisonVerdict.FILE_ABSENT

    if observed.status is ObservationStatus.READ:
        # Same UTF-8 assumption, and the same evidence for it, as compare_write.
        old_bytes = claim.details["old_string"].encode("utf-8")
        new_bytes = claim.details["new_string"].encode("utf-8")

        if _edit_landed(observed.file_bytes, old_bytes, new_bytes):
            return ComparisonVerdict.CLAIM_HOLDS

        if _edit_landed(
            _normalise_line_endings(observed.file_bytes),
            _normalise_line_endings(old_bytes),
            _normalise_line_endings(new_bytes),
        ):
            return ComparisonVerdict.CLAIM_HOLDS_AFTER_NORMALIZE

        return ComparisonVerdict.CLAIM_DOES_NOT_HOLD

    return ComparisonVerdict.STATUS_NOT_ACCEPTED


def compare_tool_name(claim, observed) -> ComparisonVerdict:
    """Send one claim to the comparison that knows its tool, and return the verdict.

    Each tool's claim asks a different question of the file — Write asks equality,
    Edit asks containment — so there is one function per tool and this chooses
    between them by name.
    """
    if claim.tool_name == "Write":
        return compare_write(claim, observed)

    if claim.tool_name == "Edit":
        return compare_edit(claim, observed)

    # parse_post_tool_use never builds a claim for any other tool, so reaching here
    # means BuildLens's own code did. That is a fault in whatever drives the batch,
    # not in this claim, so it stops rather than being recorded per claim.
    raise ValueError("no comparison for tool: " + claim.tool_name)
