"""Decide which captured claims count for this repository, and which one per path.

The capture file is shared by every Claude session on the machine, so it holds
claims about other repositories too, and one path may be claimed several times.
"""

from dataclasses import dataclass

from capture_reader import CapturedClaim
from file_observer import relative_to_root


@dataclass(frozen=True)
class ClaimSelection:
    """Hold the deciding claim per path, the claims it replaced, and the rest."""

    # Keyed by Git-style repository-relative path, the same keys pictures use.
    latest: dict[str, CapturedClaim]
    # Earlier claims on a path, oldest first. Kept so the report can say they
    # exist, unchecked, rather than silently dropping what Claude reported.
    superseded: dict[str, list[CapturedClaim]]
    # Claims about files outside this repository, set aside but still counted.
    outside: list[CapturedClaim]


def select_claims(captured_claims: list[CapturedClaim], repository_root: str) -> ClaimSelection:
    """Group claims by repository path; the latest capture line on a path decides.

    Payloads carry no timestamp, so capture-file line order is the only order
    available. Sorting by line number keeps that true whatever order the claims
    arrive in.
    """
    by_path: dict[str, list[CapturedClaim]] = {}
    outside = []

    for captured in sorted(captured_claims, key=lambda item: item.line_number):
        path = relative_to_root(captured.claim.file_path, repository_root)
        if path is None:
            outside.append(captured)
            continue
        by_path.setdefault(path, []).append(captured)

    latest = {path: claims[-1] for path, claims in by_path.items()}
    superseded = {path: claims[:-1] for path, claims in by_path.items() if len(claims) > 1}

    return ClaimSelection(latest=latest, superseded=superseded, outside=outside)
