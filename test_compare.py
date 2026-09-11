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
print("test passed")
