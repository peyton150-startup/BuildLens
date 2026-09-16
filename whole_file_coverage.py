"""Decide which paths a whole-file claim fully accounts for (D6).

reconcile compares pictures and knows nothing about claims (D22). This step runs
before it and hands it only the paths whose latest claim is a Write that holds:
a Write states every byte of the file, so a holding one leaves nothing
unaccounted for. An Edit states only fragments, so it never qualifies.

Known limit (D23): the verdict comes from reading the file again now, not from
the witness picture. A change the witness recorded but that is undone before
this read is judged against the later content, and can go unreported.
"""

from compare import ComparisonVerdict, compare_write
from claim_selection import ClaimSelection
from file_observer import observe_file


def whole_file_held_paths(selection: ClaimSelection, repository_root: str) -> set[str]:
    """Return the repository paths whose latest claim is a Write that holds.

    Only CLAIM_HOLDS counts. A match after normalizing line endings still means
    the bytes differ, so that path stays reported (D6a).
    """
    held = set()

    for path, captured in selection.latest.items():
        if captured.claim.tool_name != "Write":
            continue

        observed = observe_file(captured.claim.file_path, repository_root)
        if compare_write(captured.claim, observed) is ComparisonVerdict.CLAIM_HOLDS:
            held.add(path)

    return held
