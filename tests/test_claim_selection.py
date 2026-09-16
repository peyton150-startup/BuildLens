"""Tests for claim_selection.py.

Run it with:

    python tests/test_claim_selection.py

Claims are built directly: which lines of the capture file become claims is
capture_reader's job, and these tests only decide what happens to claims once
they exist.
"""

import sys
from pathlib import Path

# Put the repository root first on the import search path, so the product
# modules it holds import by bare name when this file runs as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from types import MappingProxyType

import claim_selection
from capture_reader import CapturedClaim
from claude_adapter import ClaimedEdit

ROOT = "C:/Users/nicol/BuildLens_Project"


def captured(line_number: int, file_path: str) -> CapturedClaim:
    claim = ClaimedEdit(
        file_path=file_path,
        session_id="session-1",
        tool_name="Write",
        details=MappingProxyType({"content": "line " + str(line_number)}),
    )
    return CapturedClaim(line_number, claim)


def test_a_claim_inside_the_repository_is_keyed_by_its_git_style_path():
    claim = captured(3, "C:\\Users\\nicol\\BuildLens_Project\\tests\\test_cli.py")

    selection = claim_selection.select_claims([claim], ROOT)

    assert selection.latest == {"tests/test_cli.py": claim}
    assert selection.superseded == {}
    assert selection.outside == []


def test_a_claim_outside_the_repository_is_set_aside_not_selected():
    claim = captured(4, "C:/Users/nicol/Datum/x.py")

    selection = claim_selection.select_claims([claim], ROOT)

    assert selection.latest == {}
    assert selection.outside == [claim]


def test_the_latest_capture_line_decides_and_earlier_claims_are_superseded():
    first = captured(41, "C:/Users/nicol/BuildLens_Project/e.py")
    second = captured(45, "C:/Users/nicol/BuildLens_Project/e.py")
    third = captured(49, "C:/Users/nicol/BuildLens_Project/e.py")

    selection = claim_selection.select_claims([second, third, first], ROOT)

    assert selection.latest == {"e.py": third}
    assert selection.superseded == {"e.py": [first, second]}


def test_claims_on_different_paths_do_not_supersede_each_other():
    e_claim = captured(41, "C:/Users/nicol/BuildLens_Project/e.py")
    f_claim = captured(45, "C:/Users/nicol/BuildLens_Project/f.py")

    selection = claim_selection.select_claims([e_claim, f_claim], ROOT)

    assert selection.latest == {"e.py": e_claim, "f.py": f_claim}
    assert selection.superseded == {}


test_a_claim_inside_the_repository_is_keyed_by_its_git_style_path()
test_a_claim_outside_the_repository_is_set_aside_not_selected()
test_the_latest_capture_line_decides_and_earlier_claims_are_superseded()
test_claims_on_different_paths_do_not_supersede_each_other()
print("test passed")
