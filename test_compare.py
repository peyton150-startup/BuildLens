"""Tests for compare.py.

Run it with:

    python test_compare.py

Every case here was specified before any of it was written: see EV-P8-TEST-ROWS-420
in learning/LEARNING_LEDGER.md, where the expected result of each row was decided.
"""

import hashlib
import importlib
from datetime import datetime, timezone

from claude_adapter import ClaimedEdit
from file_observer import ObservationStatus, ObservedFile


MOMENT = datetime(2026, 9, 11, 20, 0, tzinfo=timezone.utc)


def write_claim(content):
    return ClaimedEdit(
        file_path="notes.md",
        session_id="session-1",
        tool_name="Write",
        details={"content": content},
    )


def edit_claim():
    return ClaimedEdit(
        file_path="notes.md",
        session_id="session-1",
        tool_name="Edit",
        details={"old_string": "hello", "new_string": "goodbye"},
    )


def read_observation(file_bytes):
    return ObservedFile(
        file_path="notes.md",
        status=ObservationStatus.READ,
        file_bytes=file_bytes,
        content_hash=hashlib.sha256(file_bytes).hexdigest(),
        observed_at=MOMENT,
        repository_relative_path="notes.md",
    )


def observation_without_bytes(status):
    return ObservedFile(
        file_path="notes.md",
        status=status,
        file_bytes=None,
        content_hash=None,
        observed_at=MOMENT,
        repository_relative_path="notes.md",
    )


def test_exact_match_holds():
    compare = importlib.import_module("compare")

    verdict = compare.compare_write(write_claim("hello\n"), read_observation(b"hello\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_same_text_with_windows_line_endings_holds_after_normalize():
    compare = importlib.import_module("compare")

    verdict = compare.compare_write(write_claim("hello\n"), read_observation(b"hello\r\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS_AFTER_NORMALIZE


def test_different_content_does_not_hold():
    compare = importlib.import_module("compare")

    verdict = compare.compare_write(write_claim("hello\n"), read_observation(b"goodbye\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_DOES_NOT_HOLD


def test_normalizing_does_not_rescue_different_content():
    compare = importlib.import_module("compare")

    verdict = compare.compare_write(write_claim("hello\n"), read_observation(b"goodbye\r\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_DOES_NOT_HOLD


def test_missing_file_contradicts_the_claim():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.ABSENT)
    verdict = compare.compare_write(write_claim("hello\n"), observed)

    assert verdict is compare.ComparisonVerdict.FILE_ABSENT


def test_unreadable_file_decides_nothing():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.UNREADABLE)
    verdict = compare.compare_write(write_claim("hello\n"), observed)

    assert verdict is compare.ComparisonVerdict.INCOMPARABLE


def test_empty_claim_against_a_missing_file_is_still_absent():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.ABSENT)
    verdict = compare.compare_write(write_claim(""), observed)

    assert verdict is compare.ComparisonVerdict.FILE_ABSENT


def test_empty_claim_against_an_empty_file_holds():
    compare = importlib.import_module("compare")

    verdict = compare.compare_write(write_claim(""), read_observation(b""))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_non_ascii_claim_is_encoded_as_utf8():
    compare = importlib.import_module("compare")

    verdict = compare.compare_write(write_claim("caf\u00e9\n"), read_observation(b"caf\xc3\xa9\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_a_status_compare_write_does_not_know_is_not_judged():
    compare = importlib.import_module("compare")

    # A dataclass annotation describes but does not enforce, so a test can stand in
    # a status that does not exist yet.
    observed = observation_without_bytes("too_large")
    verdict = compare.compare_write(write_claim("hello\n"), observed)

    assert verdict is compare.ComparisonVerdict.STATUS_NOT_ACCEPTED


def test_an_edit_claim_is_rejected_before_the_content_lookup():
    compare = importlib.import_module("compare")

    try:
        compare.compare_write(edit_claim(), read_observation(b"goodbye\n"))
    except ValueError as error:
        assert "Edit" in str(error)
    else:
        raise AssertionError("compare_write judged an Edit claim")


def test_an_edit_claim_is_rejected_even_when_the_file_is_absent():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.ABSENT)
    try:
        compare.compare_write(edit_claim(), observed)
    except ValueError as error:
        assert "Edit" in str(error)
    else:
        raise AssertionError("an absent file answered for a claim compare_write cannot judge")


def test_every_real_status_has_a_branch():
    compare = importlib.import_module("compare")

    for status in ObservationStatus:
        if status is ObservationStatus.READ:
            observed = read_observation(b"hello\n")
        else:
            observed = observation_without_bytes(status)

        verdict = compare.compare_write(write_claim("hello\n"), observed)

        assert verdict is not compare.ComparisonVerdict.STATUS_NOT_ACCEPTED, status


test_exact_match_holds()
test_same_text_with_windows_line_endings_holds_after_normalize()
test_different_content_does_not_hold()
test_normalizing_does_not_rescue_different_content()
test_missing_file_contradicts_the_claim()
test_unreadable_file_decides_nothing()
test_empty_claim_against_a_missing_file_is_still_absent()
test_empty_claim_against_an_empty_file_holds()
test_non_ascii_claim_is_encoded_as_utf8()
test_a_status_compare_write_does_not_know_is_not_judged()
test_an_edit_claim_is_rejected_before_the_content_lookup()
test_an_edit_claim_is_rejected_even_when_the_file_is_absent()
test_every_real_status_has_a_branch()

def edit_claim_with(old_string, new_string, replace_all=None):
    details = {"old_string": old_string, "new_string": new_string}
    if replace_all is not None:
        details["replace_all"] = replace_all

    return ClaimedEdit(
        file_path="notes.md",
        session_id="session-1",
        tool_name="Edit",
        details=details,
    )


def test_edit_holds_when_the_new_text_is_there_and_the_old_is_gone():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("hello", "goodbye")
    verdict = compare.compare_edit(claim, read_observation(b"goodbye world\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_edit_does_not_hold_when_the_replaced_text_is_still_there():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("hello", "goodbye")
    verdict = compare.compare_edit(claim, read_observation(b"goodbye world\nhello again\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_DOES_NOT_HOLD


def test_edit_does_not_hold_when_the_new_text_is_missing():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("hello", "goodbye")
    verdict = compare.compare_edit(claim, read_observation(b"hello world\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_DOES_NOT_HOLD


def test_edit_holds_after_normalize_when_only_line_endings_differ():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("hello", "goodbye\nworld")
    verdict = compare.compare_edit(claim, read_observation(b"goodbye\r\nworld\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS_AFTER_NORMALIZE


def test_old_text_may_survive_when_the_new_text_contains_it():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("hello", "hello there")
    verdict = compare.compare_edit(claim, read_observation(b"hello there world\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_replace_all_does_not_change_the_verdict():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("hello", "goodbye", replace_all=True)
    verdict = compare.compare_edit(claim, read_observation(b"goodbye\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_edit_against_a_missing_file_is_absent():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.ABSENT)
    verdict = compare.compare_edit(edit_claim_with("hello", "goodbye"), observed)

    assert verdict is compare.ComparisonVerdict.FILE_ABSENT


def test_edit_against_an_unreadable_file_decides_nothing():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.UNREADABLE)
    verdict = compare.compare_edit(edit_claim_with("hello", "goodbye"), observed)

    assert verdict is compare.ComparisonVerdict.INCOMPARABLE


def test_edit_against_a_status_it_does_not_know_is_not_judged():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes("too_large")
    verdict = compare.compare_edit(edit_claim_with("hello", "goodbye"), observed)

    assert verdict is compare.ComparisonVerdict.STATUS_NOT_ACCEPTED


def test_a_write_claim_is_rejected_by_compare_edit():
    compare = importlib.import_module("compare")

    try:
        compare.compare_edit(write_claim("hello\n"), read_observation(b"hello\n"))
    except ValueError as error:
        assert "Write" in str(error)
    else:
        raise AssertionError("compare_edit judged a Write claim")


def test_every_real_status_has_a_branch_in_compare_edit():
    compare = importlib.import_module("compare")

    for status in ObservationStatus:
        if status is ObservationStatus.READ:
            observed = read_observation(b"goodbye world\n")
        else:
            observed = observation_without_bytes(status)

        verdict = compare.compare_edit(edit_claim_with("hello", "goodbye"), observed)

        assert verdict is not compare.ComparisonVerdict.STATUS_NOT_ACCEPTED, status


def test_edit_strings_are_encoded_as_utf8():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("caf\u00e9", "th\u00e9")
    verdict = compare.compare_edit(claim, read_observation(b"th\xc3\xa9 world\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


test_edit_holds_when_the_new_text_is_there_and_the_old_is_gone()
test_edit_does_not_hold_when_the_replaced_text_is_still_there()
test_edit_does_not_hold_when_the_new_text_is_missing()
test_edit_holds_after_normalize_when_only_line_endings_differ()
test_old_text_may_survive_when_the_new_text_contains_it()
test_replace_all_does_not_change_the_verdict()
test_edit_against_a_missing_file_is_absent()
test_edit_against_an_unreadable_file_decides_nothing()
test_edit_against_a_status_it_does_not_know_is_not_judged()
test_a_write_claim_is_rejected_by_compare_edit()
test_every_real_status_has_a_branch_in_compare_edit()
test_edit_strings_are_encoded_as_utf8()

def notebook_claim():
    return ClaimedEdit(
        file_path="notes.md",
        session_id="session-1",
        tool_name="Notebook",
        details={"content": "hello\n"},
    )


def test_dispatcher_routes_a_write_claim():
    compare = importlib.import_module("compare")

    verdict = compare.compare_tool_name(write_claim("hello\n"), read_observation(b"hello\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_dispatcher_routes_an_edit_claim():
    compare = importlib.import_module("compare")

    claim = edit_claim_with("hello", "goodbye")
    verdict = compare.compare_tool_name(claim, read_observation(b"goodbye world\n"))

    assert verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_dispatcher_passes_through_absent_for_a_write_claim():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.ABSENT)
    verdict = compare.compare_tool_name(write_claim("hello\n"), observed)

    assert verdict is compare.ComparisonVerdict.FILE_ABSENT


def test_dispatcher_passes_through_absent_for_an_edit_claim():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.ABSENT)
    verdict = compare.compare_tool_name(edit_claim_with("hello", "goodbye"), observed)

    assert verdict is compare.ComparisonVerdict.FILE_ABSENT


def test_dispatcher_passes_through_unreadable_for_a_write_claim():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.UNREADABLE)
    verdict = compare.compare_tool_name(write_claim("hello\n"), observed)

    assert verdict is compare.ComparisonVerdict.INCOMPARABLE


def test_dispatcher_passes_through_unreadable_for_an_edit_claim():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes(ObservationStatus.UNREADABLE)
    verdict = compare.compare_tool_name(edit_claim_with("hello", "goodbye"), observed)

    assert verdict is compare.ComparisonVerdict.INCOMPARABLE


def test_dispatcher_passes_through_an_unknown_status_for_a_write_claim():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes("too_large")
    verdict = compare.compare_tool_name(write_claim("hello\n"), observed)

    assert verdict is compare.ComparisonVerdict.STATUS_NOT_ACCEPTED


def test_dispatcher_passes_through_an_unknown_status_for_an_edit_claim():
    compare = importlib.import_module("compare")

    observed = observation_without_bytes("too_large")
    verdict = compare.compare_tool_name(edit_claim_with("hello", "goodbye"), observed)

    assert verdict is compare.ComparisonVerdict.STATUS_NOT_ACCEPTED


def test_dispatcher_rejects_a_tool_it_cannot_route():
    compare = importlib.import_module("compare")

    try:
        compare.compare_tool_name(notebook_claim(), read_observation(b"hello\n"))
    except ValueError as error:
        assert "Notebook" in str(error)
    else:
        raise AssertionError("the dispatcher routed a claim it has no comparison for")


test_dispatcher_routes_a_write_claim()
test_dispatcher_routes_an_edit_claim()
test_dispatcher_passes_through_absent_for_a_write_claim()
test_dispatcher_passes_through_absent_for_an_edit_claim()
test_dispatcher_passes_through_unreadable_for_a_write_claim()
test_dispatcher_passes_through_unreadable_for_an_edit_claim()
test_dispatcher_passes_through_an_unknown_status_for_a_write_claim()
test_dispatcher_passes_through_an_unknown_status_for_an_edit_claim()
test_dispatcher_rejects_a_tool_it_cannot_route()
print("test passed")
