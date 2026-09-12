"""Tests for reconcile.py.

Run it with:

    python test_reconcile.py

Rows 1-6 were approved before any of this was written; row 7 (a claimed path in
neither picture) was ruled out of scope, since PostToolUse already gives a
verdict for a claim whose file is absent.
"""

from datetime import datetime, timezone

from reconcile import ChangeKind, UnclaimedChange, reconcile

MOMENT = datetime(2026, 9, 12, 15, 0, tzinfo=timezone.utc)


def test_unchanged_path_is_not_reported():
    """A path whose hash is identical in both pictures changed nothing."""
    result = reconcile({"a.py": "h1"}, {"a.py": "h1"}, claimed_paths=set(), observed_at=MOMENT)

    assert result == []


def test_changed_and_unclaimed_path_is_reported_as_modified():
    """The motivating case: a shell edit no claim accounts for."""
    result = reconcile(
        {"notes/plan.md": "h1"},
        {"notes/plan.md": "h2"},
        claimed_paths=set(),
        observed_at=MOMENT,
    )

    assert result == [
        UnclaimedChange(
            repository_relative_path="notes/plan.md",
            kind=ChangeKind.MODIFIED,
            hash_at_start="h1",
            hash_at_stop="h2",
            observed_at=MOMENT,
        )
    ]


def test_changed_but_claimed_path_is_not_reported():
    """A claim already accounts for the change, so the scan stays silent."""
    result = reconcile(
        {"a.py": "h1"},
        {"a.py": "h2"},
        claimed_paths={"a.py"},
        observed_at=MOMENT,
    )

    assert result == []


def test_path_only_in_the_later_picture_is_created():
    """No entry at session start means the file did not exist then."""
    result = reconcile({}, {"new.py": "h2"}, claimed_paths=set(), observed_at=MOMENT)

    assert result == [
        UnclaimedChange(
            repository_relative_path="new.py",
            kind=ChangeKind.CREATED,
            hash_at_start=None,
            hash_at_stop="h2",
            observed_at=MOMENT,
        )
    ]


def test_path_only_in_the_earlier_picture_is_deleted():
    """The absent side stays absent rather than being filled with a stand-in."""
    result = reconcile({"gone.py": "h1"}, {}, claimed_paths=set(), observed_at=MOMENT)

    assert result == [
        UnclaimedChange(
            repository_relative_path="gone.py",
            kind=ChangeKind.DELETED,
            hash_at_start="h1",
            hash_at_stop=None,
            observed_at=MOMENT,
        )
    ]


def test_two_empty_pictures_report_nothing():
    """Nothing observed twice establishes nothing to reconcile."""
    assert reconcile({}, {}, claimed_paths=set(), observed_at=MOMENT) == []


def test_every_kind_is_reported_in_one_scan_in_path_order():
    """One scan reports each independent finding; order is stable for a reader."""
    result = reconcile(
        {"gone.py": "h1", "same.py": "h1", "touched.py": "h1"},
        {"same.py": "h1", "touched.py": "h2", "new.py": "h9"},
        claimed_paths=set(),
        observed_at=MOMENT,
    )

    assert [(change.repository_relative_path, change.kind) for change in result] == [
        ("gone.py", ChangeKind.DELETED),
        ("new.py", ChangeKind.CREATED),
        ("touched.py", ChangeKind.MODIFIED),
    ]


def test_a_claim_does_not_silence_a_different_path():
    """Claims are matched per path, not taken as blanket coverage."""
    result = reconcile(
        {"a.py": "h1", "b.py": "h1"},
        {"a.py": "h2", "b.py": "h2"},
        claimed_paths={"a.py"},
        observed_at=MOMENT,
    )

    assert [change.repository_relative_path for change in result] == ["b.py"]


test_unchanged_path_is_not_reported()
test_changed_and_unclaimed_path_is_reported_as_modified()
test_changed_but_claimed_path_is_not_reported()
test_path_only_in_the_later_picture_is_created()
test_path_only_in_the_earlier_picture_is_deleted()
test_two_empty_pictures_report_nothing()
test_every_kind_is_reported_in_one_scan_in_path_order()
test_a_claim_does_not_silence_a_different_path()
print("test passed")
