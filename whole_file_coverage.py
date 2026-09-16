"""Decide which paths a whole-file claim fully accounts for (D6).

reconcile compares pictures and knows nothing about claims (D22). This step runs
before it and hands it only the paths whose latest claim is a Write that holds:
a Write states every byte of the file, so a holding one leaves nothing
unaccounted for. An Edit states only fragments, so it never qualifies.

The verdict comes from reading the file again now (D23). That read happens after
the witness picture, so on its own it could judge a later moment than the one
reconcile reports. A path therefore counts as held only when the re-read bytes
are also the bytes the witness recorded (D23a); otherwise the file changed after
the witness, and the path stays reported and is flagged instead of skipped.
"""

from dataclasses import dataclass

from compare import ComparisonVerdict, compare_write
from claim_selection import ClaimSelection
from file_observer import observe_file
from reconcile import Picture


@dataclass(frozen=True)
class WholeFileCoverage:
    """Hold the paths a whole-file claim accounts for, and those that moved on."""

    # Handed to reconcile as whole_file_held_paths: skipped as changes.
    held: set[str]
    # A holding Write whose file no longer matches the witness picture. Kept
    # for the report to label; never skipped.
    changed_after_witness: set[str]


def whole_file_coverage(
    selection: ClaimSelection,
    witness: Picture,
    repository_root: str,
) -> WholeFileCoverage:
    """Return which latest Write claims hold at the witness, judged by re-reading.

    Only CLAIM_HOLDS counts. A match after normalizing line endings still means
    the bytes differ, so that path stays reported (D6a).
    """
    held = set()
    changed_after_witness = set()

    for path, captured in selection.latest.items():
        if captured.claim.tool_name != "Write":
            continue

        observed = observe_file(captured.claim.file_path, repository_root)
        if compare_write(captured.claim, observed) is not ComparisonVerdict.CLAIM_HOLDS:
            continue

        witness_hash = witness.hashes.get(path)
        if witness_hash is None:
            # The witness could not read the path or did not see it: no recorded
            # bytes to agree with, and no evidence of a later change either.
            continue

        if witness_hash == observed.content_hash:
            held.add(path)
        else:
            changed_after_witness.add(path)

    return WholeFileCoverage(held=held, changed_after_witness=changed_after_witness)
