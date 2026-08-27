"""Tests for session.py.

Run it with:

    python test_session.py
"""

from session import Session


def test_new_session_has_no_changes():
    session = Session()
    assert len(session.changes) == 0


test_new_session_has_no_changes()
print("test passed")
