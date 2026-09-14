"""Tests for session.py.

Run it with:

    python tests/test_session.py
"""

import sys
from pathlib import Path

# Put the repository root first on the import search path, so the product
# modules it holds import by bare name when this file runs as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from session import Session


def test_new_session_has_no_changes():
    session = Session()
    assert session.history() == []


def test_recording_one_change_stores_it():
    session = Session()
    session.record("diff A")
    assert session.history() == ["diff A"]


def test_recording_two_changes_keeps_them_in_order():
    session = Session()
    session.record("diff A")
    session.record("diff B")
    assert session.history() == ["diff A", "diff B"]


def test_history_returns_what_was_recorded():
    session = Session()
    session.record("diff A")
    session.record("diff B")
    assert session.history() == ["diff A", "diff B"]


def test_mutating_the_history_does_not_touch_the_session():
    session = Session()
    session.record("diff A")

    history = session.history()
    history.append("diff B")

    assert session.history() == ["diff A"]


def test_mutable_storage_is_not_public():
    session = Session()
    assert not hasattr(session, "changes")


def test_rejecting_non_string_input_preserves_history():
    session = Session()
    session.record("diff A")

    try:
        session.record(7)
    except TypeError as error:
        assert str(error) == "must be a string"
    else:
        assert False, "record should reject non-string input"

    assert session.history() == ["diff A"]


test_new_session_has_no_changes()
test_recording_one_change_stores_it()
test_recording_two_changes_keeps_them_in_order()
test_history_returns_what_was_recorded()
test_mutating_the_history_does_not_touch_the_session()
test_mutable_storage_is_not_public()
test_rejecting_non_string_input_preserves_history()
print("test passed")
