"""Tests for session.py.

Run it with:

    python test_session.py
"""

from session import Session


def test_new_session_has_no_changes():
    session = Session()
    assert len(session.changes) == 0


def test_recording_one_change_stores_it():
    session = Session()
    session.record("diff A")
    assert len(session.changes) == 1


def test_recording_two_changes_keeps_them_in_order():
    session = Session()
    session.record("diff A")
    session.record("diff B")
    assert session.changes == ["diff A", "diff B"]


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


test_new_session_has_no_changes()
test_recording_one_change_stores_it()
test_recording_two_changes_keeps_them_in_order()
test_history_returns_what_was_recorded()
test_mutating_the_history_does_not_touch_the_session()
print("test passed")
