"""Tests for find_report.py, the find report wording.

Run it with:

    python tests/test_find_report.py

These build a FindResult by hand rather than running a session: the wording is
what is under test, so the pictures, keypresses and capture read that a real
session needs would only be setup standing between the test and the sentences.
"""

import sys
from pathlib import Path

# Put the repository root first on the import search path, so the product
# modules it holds import by bare name when this file runs as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone

from capture_reader import CaptureRead
from claim_selection import ClaimSelection
from find_report import format_find_report
from find_workflow import FindResult
from reconcile import ChangeKind, Picture, ScanResult, UnclaimedChange
from whole_file_coverage import WholeFileCoverage

BASELINE_TIME = datetime(2026, 9, 17, 9, 0, tzinfo=timezone.utc)
WITNESS_TIME = datetime(2026, 9, 17, 9, 30, tzinfo=timezone.utc)


def test_missing_capture_file_reports_the_change_and_checks_no_claims():
    """D16: report every observed change, say the capture file was missing.

    Never say Claude made no changes: with no capture file there is no record
    to read, and missing evidence is not observed absence.
    """
    result = FindResult(
        repository_root="C:/repo",
        baseline=Picture(taken_at=BASELINE_TIME, hashes={"a.py": "hash-1"}),
        witness=Picture(taken_at=WITNESS_TIME, hashes={"a.py": "hash-2"}),
        capture_position=0,
        capture=CaptureRead(claims=[], skipped=[]),
        selection=ClaimSelection(latest={}, superseded={}, outside=[]),
        coverage=WholeFileCoverage(held=set(), changed_after_witness=set()),
        scan=ScanResult(
            changes=[
                UnclaimedChange(
                    repository_relative_path="a.py",
                    kind=ChangeKind.MODIFIED,
                    hash_at_baseline="hash-1",
                    hash_at_witness="hash-2",
                    baseline_time=BASELINE_TIME,
                    witness_time=WITNESS_TIME,
                )
            ],
            undetermined=[],
        ),
        capture_missing=True,
    )

    lines = format_find_report(result)

    assert any("a.py" in line for line in lines)
    assert any("capture file was missing" in line for line in lines)
    assert not any("made no" in line for line in lines)


test_missing_capture_file_reports_the_change_and_checks_no_claims()
print("test passed")
