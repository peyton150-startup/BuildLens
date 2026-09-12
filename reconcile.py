"""Report changes to a working tree that no claim accounted for.

PostToolUse reports a tool call and names the file it touched, so every Edit or
Write arrives with a claim BuildLens can compare an observation against. A shell
command does not: `sed -i` fires a PostToolUse whose payload names no file, so
the change it made is invisible to the comparison path entirely.

This module closes that gap by difference rather than by report. Two pictures of
the same tree, taken at two moments, are compared; every path whose content
differs and which no claim covers is an UNCLAIMED CHANGE.

What it deliberately does NOT establish:

    WHO      a hash difference says the content changed between two instants, not
             who changed it. Attribution rests on one stream editing the tree, an
             assumption Phase 13's separate worktrees make structural instead.
    WHICH    file granularity only. Isolating the session's own lines inside a
    LINES    file that was already modified beforehand needs the session-start
             BYTES, not a hash; that is the condition that would reverse this
             design.
    BEFORE   only the span between the two pictures is visible. Changes made
             before BuildLens observed the tree are absorbed into the earlier
             picture as though they had always been there.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ChangeKind(Enum):
    """How a path's presence differs between the two pictures."""

    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"


@dataclass(frozen=True)
class Picture:
    """Hold what one look at a tree found, and when that look happened.

    The moment belongs to the picture rather than to whoever reads it later.
    A caller that inferred the moment from something else — "the session started
    at 9, so the baseline is from 9" — would be silently wrong the first time a
    baseline is re-taken mid-session.
    """

    taken_at: datetime
    hashes: dict[str, str]


@dataclass(frozen=True)
class UnclaimedChange:
    """Hold one change the tree shows and no claim accounts for.

    The hash on the side where the file did not exist stays None rather than
    being filled with an empty string or a hash of nothing: absence has to stay
    distinguishable from a real fingerprint.

    There is no provenance field. Provenance would be an inference this record
    has no evidence for, and a record that states what it cannot know is worse
    than one that stays silent.
    """

    repository_relative_path: str
    kind: ChangeKind
    hash_at_baseline: str | None
    hash_at_witness: str | None
    baseline_time: datetime
    witness_time: datetime


def reconcile(
    baseline: Picture,
    witness: Picture,
    claimed_paths: set[str],
) -> list[UnclaimedChange]:
    """Return every change between two pictures that no claim covers.

    The BASELINE is what the tree held when it was last established as known;
    the WITNESS is what it holds now. Both are observations; the word
    "observed" is left to file_observer, where it means reading one file.

    Each picture maps a repository-relative path to the content hash found at
    the moment it was taken. A path missing from a picture did not exist then.

    Both moments travel onto every record, so a later reader can see the span a
    finding covers instead of having to assume one.

    Paths are walked in sorted order so one scan reads the same way twice; the
    dicts' own order reflects when files were encountered, which is not a fact
    about the repository.
    """
    changes = []

    for path in sorted(baseline.hashes.keys() | witness.hashes.keys()):
        if path in claimed_paths:
            # A claim already accounts for this path, and PostToolUse has
            # already produced a verdict for it. Reporting it again would state
            # the same change twice under two different names.
            continue

        hash_at_baseline = baseline.hashes.get(path)
        hash_at_witness = witness.hashes.get(path)

        if hash_at_baseline == hash_at_witness:
            # Identical content. Note what this cannot see: a file changed and
            # then restored between the two pictures is indistinguishable from
            # one never touched, in either direction.
            continue

        if hash_at_baseline is None:
            kind = ChangeKind.CREATED
        elif hash_at_witness is None:
            kind = ChangeKind.DELETED
        else:
            kind = ChangeKind.MODIFIED

        changes.append(
            UnclaimedChange(
                repository_relative_path=path,
                kind=kind,
                hash_at_baseline=hash_at_baseline,
                hash_at_witness=hash_at_witness,
                baseline_time=baseline.taken_at,
                witness_time=witness.taken_at,
            )
        )

    return changes
