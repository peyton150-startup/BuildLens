"""Tests for find_report.py, the find report wording.

Run it with:

    python tests/test_find_report.py

These build a FindResult by hand rather than running a session: the wording is
what is under test, so the pictures, keypresses and capture read a real session
needs would only be setup standing between the test and the sentences.

Times are formatted through an injected format_time, so a report can be checked
without the machine's time zone deciding whether a test passes.
"""

import sys
from pathlib import Path

# Put the repository root first on the import search path, so the product
# modules it holds import by bare name when this file runs as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone

from capture_reader import CaptureRead, CapturedClaim, SkippedLine
from claim_selection import ClaimSelection
from claude_adapter import ClaimedEdit
from find_report import format_find_report
from find_workflow import FindResult
from reconcile import (
    ChangeKind,
    Picture,
    ScanResult,
    UnclaimedChange,
    UndeterminedPath,
)
from whole_file_coverage import WholeFileCoverage

BASELINE_TIME = datetime(2026, 9, 17, 9, 0, tzinfo=timezone.utc)
WITNESS_TIME = datetime(2026, 9, 17, 9, 30, tzinfo=timezone.utc)


def fixed_time(moment):
    """Return a stable label per moment, so wording alone decides a result."""
    return {BASELINE_TIME: "09:00", WITNESS_TIME: "09:30"}[moment]


def make_change(path, kind):
    """Return one established change between the two fixed moments."""
    return UnclaimedChange(
        repository_relative_path=path,
        kind=kind,
        hash_at_baseline=None if kind is ChangeKind.CREATED else "hash-1",
        hash_at_witness=None if kind is ChangeKind.DELETED else "hash-2",
        baseline_time=BASELINE_TIME,
        witness_time=WITNESS_TIME,
    )


def make_claim(line_number, path, tool_name="Write"):
    """Return one captured claim naming path, as the capture file held it."""
    return CapturedClaim(
        line_number=line_number,
        claim=ClaimedEdit(
            file_path="C:/repo/" + path,
            session_id="session-1",
            tool_name=tool_name,
            details={},
        ),
    )


def make_result(
    *,
    changes=(),
    undetermined=(),
    skipped=(),
    superseded=None,
    outside=(),
    changed_after_witness=frozenset(),
    capture_missing=False,
):
    """Return a FindResult holding only what the case under test needs."""
    return FindResult(
        repository_root="C:/repo",
        baseline=Picture(taken_at=BASELINE_TIME, hashes={"a.py": "hash-1"}),
        witness=Picture(taken_at=WITNESS_TIME, hashes={"a.py": "hash-2"}),
        capture_position=0,
        capture=CaptureRead(claims=[], skipped=list(skipped)),
        selection=ClaimSelection(
            latest={},
            superseded=dict(superseded or {}),
            outside=list(outside),
        ),
        coverage=WholeFileCoverage(
            held=set(),
            changed_after_witness=set(changed_after_witness),
        ),
        scan=ScanResult(changes=list(changes), undetermined=list(undetermined)),
        capture_missing=capture_missing,
    )


def test_missing_capture_file_reports_the_change_and_checks_no_claims():
    """D16: report every observed change, say the capture file was missing.

    Never say Claude made no changes: with no capture file there is no record
    to read, and missing evidence is not observed absence.
    """
    result = make_result(
        changes=[make_change("a.py", ChangeKind.MODIFIED)],
        capture_missing=True,
    )

    lines = format_find_report(result, format_time=fixed_time)

    assert any("a.py" in line for line in lines)
    assert any("capture file was missing" in line for line in lines)
    assert not any("made no" in line for line in lines)


def test_net_changes_name_each_kind_and_the_observation_window():
    """Test 3 and D7: the three kinds, over a window with both moments.

    A file edited and restored between the pictures is invisible to two
    pictures, so it is not in scan.changes and must not be named.
    """
    result = make_result(
        changes=[
            make_change("notes.md", ChangeKind.CREATED),
            make_change("cli.py", ChangeKind.MODIFIED),
            make_change("old.py", ChangeKind.DELETED),
        ],
    )

    lines = format_find_report(result, format_time=fixed_time)

    assert any("CREATED notes.md" in line for line in lines)
    assert any("MODIFIED cli.py" in line for line in lines)
    assert any("DELETED old.py" in line for line in lines)
    assert any("09:00" in line and "09:30" in line for line in lines)
    assert not any("README.md" in line for line in lines)


def test_the_report_never_attributes_a_change_or_rules_others_out():
    """D7: no authorship, and no claim that nothing else happened."""
    result = make_result(changes=[make_change("a.py", ChangeKind.MODIFIED)])

    lines = format_find_report(result, format_time=fixed_time)

    assert any("not ruled out" in line for line in lines)
    assert not any("Claude changed" in line for line in lines)
    assert not any("no unexpected changes" in line for line in lines)


def test_a_write_that_no_longer_matches_the_witness_is_flagged():
    """D23a: held on re-read but not equal to the witness hash.

    The path is reported like any other change, and labelled, because the
    validated version is not the version the witness saw.
    """
    result = make_result(
        changes=[make_change("c.py", ChangeKind.MODIFIED)],
        changed_after_witness={"c.py"},
    )

    lines = format_find_report(result, format_time=fixed_time)

    assert any(
        "c.py" in line and "changed after the witness" in line for line in lines
    )


def test_an_unreadable_path_is_undetermined_and_not_called_deleted():
    """Test 6: a gap in the scan's reach, reported as its own finding."""
    result = make_result(
        changes=[make_change("h.py", ChangeKind.DELETED)],
        undetermined=[
            UndeterminedPath(
                repository_relative_path="g.py",
                unreadable_at_baseline=False,
                unreadable_at_witness=True,
                baseline_time=BASELINE_TIME,
                witness_time=WITNESS_TIME,
            )
        ],
    )

    lines = format_find_report(result, format_time=fixed_time)

    assert any("UNDETERMINED g.py" in line for line in lines)
    assert any("unreadable at the witness" in line for line in lines)
    assert any("DELETED h.py" in line for line in lines)
    assert not any("DELETED g.py" in line for line in lines)
    assert not any("UNDETERMINED h.py" in line for line in lines)


def test_a_skipped_capture_line_is_named_with_its_reason():
    """D12, D18b, D20: name the line and why it was skipped.

    Over-reporting, never hiding: the file that line named still appears as a
    change, just without a claim.
    """
    result = make_result(
        changes=[make_change("k.py", ChangeKind.MODIFIED)],
        skipped=[SkippedLine(line_number=60, reason="not valid JSON")],
    )

    lines = format_find_report(result, format_time=fixed_time)

    assert any(
        "capture line 60" in line and "not valid JSON" in line for line in lines
    )
    assert any("MODIFIED k.py" in line for line in lines)


def test_superseded_claims_are_summarised_with_a_count_and_a_key():
    """D8a: claims already captured, never checked, never silently dropped."""
    result = make_result(
        superseded={"e.py": [make_claim(10, "e.py"), make_claim(12, "e.py")]},
    )

    lines = format_find_report(result, format_time=fixed_time)

    assert any(
        "e.py has 2 unchecked superseded claims" in line for line in lines
    )
    assert any("Press i" in line for line in lines)


def test_claims_outside_the_repository_get_one_count_line_and_a_key():
    """D14a: counted rather than dropped, with a key that shows the paths."""
    result = make_result(
        outside=[make_claim(20, "../elsewhere/x.py"), make_claim(21, "../y.py")],
    )

    lines = format_find_report(result, format_time=fixed_time)

    assert any(
        "2 claims name files outside this repository" in line for line in lines
    )
    assert any("Press o" in line for line in lines)
    assert not any("x.py" in line for line in lines)


def test_no_observed_changes_says_what_was_observed_not_that_nothing_happened():
    """Two pictures that agree establish no change, not an untouched tree."""
    result = make_result()

    lines = format_find_report(result, format_time=fixed_time)

    assert any("No changes were observed" in line for line in lines)
    assert not any("nothing happened" in line for line in lines)
    assert not any("made no" in line for line in lines)


test_missing_capture_file_reports_the_change_and_checks_no_claims()
test_net_changes_name_each_kind_and_the_observation_window()
test_the_report_never_attributes_a_change_or_rules_others_out()
test_a_write_that_no_longer_matches_the_witness_is_flagged()
test_an_unreadable_path_is_undetermined_and_not_called_deleted()
test_a_skipped_capture_line_is_named_with_its_reason()
test_superseded_claims_are_summarised_with_a_count_and_a_key()
test_claims_outside_the_repository_get_one_count_line_and_a_key()
test_no_observed_changes_says_what_was_observed_not_that_nothing_happened()
print("all tests passed")
