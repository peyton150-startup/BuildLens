"""Tests for the Claude hook adapter.

Run it with:

    python test_claude_adapter.py
"""

import importlib
from dataclasses import FrozenInstanceError


def test_valid_edit_returns_claimed_edit_from_nested_tool_input():
    try:
        claude_adapter = importlib.import_module("claude_adapter")
    except ModuleNotFoundError as error:
        raise AssertionError("claude_adapter is not implemented") from error

    payload = {
        "session_id": "session-7",
        "hook_event_name": "PostToolUse",
        "tool_name": "Edit",
        "tool_input": {
            "file_path": "C:/repo/app.py",
        },
    }

    result = claude_adapter.parse_post_tool_use(payload)

    assert result == claude_adapter.ClaimedEdit(
        file_path="C:/repo/app.py",
        session_id="session-7",
        tool_name="Edit",
    )


def test_claimed_edit_fields_cannot_be_reassigned():
    claude_adapter = importlib.import_module("claude_adapter")
    edit = claude_adapter.ClaimedEdit(
        file_path="C:/repo/app.py",
        session_id="session-7",
        tool_name="Edit",
    )

    try:
        edit.session_id = "invented-session"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("ClaimedEdit allowed provenance reassignment")


def test_valid_bash_returns_none():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-7",
        "hook_event_name": "PostToolUse",
        "tool_name": "Bash",
        "tool_input": {
            "command": "echo hello",
        },
    }

    try:
        result = claude_adapter.parse_post_tool_use(payload)
    except KeyError as error:
        raise AssertionError("valid Bash must return None") from error

    assert result is None


def test_missing_session_id_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Edit",
        "tool_input": {
            "file_path": "C:/repo/app.py",
        },
    }

    try:
        claude_adapter.parse_post_tool_use(payload)
    except ValueError as error:
        assert str(error) == "missing required field: session_id"
    except KeyError as error:
        raise AssertionError("adapter leaked a raw missing-key error") from error
    else:
        raise AssertionError("missing session_id was accepted")


def test_missing_hook_event_name_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-7",
        "tool_name": "Edit",
        "tool_input": {
            "file_path": "C:/repo/app.py",
        },
    }

    try:
        claude_adapter.parse_post_tool_use(payload)
    except ValueError as error:
        assert str(error) == "missing required field: hook_event_name"
    else:
        raise AssertionError("missing hook_event_name was accepted")


def assert_payload_error(claude_adapter, payload, expected_message):
    try:
        claude_adapter.parse_post_tool_use(payload)
    except ValueError as error:
        assert str(error) == expected_message
    except (KeyError, TypeError) as error:
        raise AssertionError("adapter leaked a raw lookup error") from error
    else:
        raise AssertionError("malformed payload was accepted")


def test_missing_edit_fields_raise_readable_errors():
    claude_adapter = importlib.import_module("claude_adapter")
    cases = [
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_input": {"file_path": "C:/repo/app.py"},
            },
            "missing required field: tool_name",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
            },
            "missing required field: tool_input",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
                "tool_input": {},
            },
            "missing required field: file_path",
        ),
    ]

    for payload, expected_message in cases:
        assert_payload_error(claude_adapter, payload, expected_message)


def test_empty_required_strings_raise_readable_errors():
    claude_adapter = importlib.import_module("claude_adapter")
    cases = [
        (
            {
                "session_id": "session-7",
                "hook_event_name": "",
                "tool_name": "Edit",
                "tool_input": {"file_path": "C:/repo/app.py"},
            },
            "empty required field: hook_event_name",
        ),
        (
            {
                "session_id": "",
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
                "tool_input": {"file_path": "C:/repo/app.py"},
            },
            "empty required field: session_id",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "",
                "tool_input": {"file_path": "C:/repo/app.py"},
            },
            "empty required field: tool_name",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
                "tool_input": {"file_path": ""},
            },
            "empty required field: file_path",
        ),
    ]

    for payload, expected_message in cases:
        assert_payload_error(claude_adapter, payload, expected_message)


def test_wrong_payload_types_raise_readable_errors():
    claude_adapter = importlib.import_module("claude_adapter")
    cases = [
        ([], "payload must be an object"),
        (
            {
                "session_id": 7,
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
                "tool_input": {"file_path": "C:/repo/app.py"},
            },
            "field must be a string: session_id",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
                "tool_input": None,
            },
            "field must be an object: tool_input",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Edit",
                "tool_input": {"file_path": 7},
            },
            "field must be a string: file_path",
        ),
    ]

    for payload, expected_message in cases:
        assert_payload_error(claude_adapter, payload, expected_message)


def test_wrong_event_name_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-7",
        "hook_event_name": "Stop",
        "tool_name": "Edit",
        "tool_input": {"file_path": "C:/repo/app.py"},
    }

    assert_payload_error(
        claude_adapter,
        payload,
        "unexpected hook event: Stop",
    )


def test_unsupported_tool_name_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-7",
        "hook_event_name": "PostToolUse",
        "tool_name": "Read",
        "tool_input": {"file_path": "C:/repo/app.py"},
    }

    assert_payload_error(
        claude_adapter,
        payload,
        "unsupported tool_name: Read",
    )


def test_malformed_bash_command_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")
    cases = [
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Bash",
                "tool_input": {},
            },
            "missing required field: command",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": ""},
            },
            "empty required field: command",
        ),
        (
            {
                "session_id": "session-7",
                "hook_event_name": "PostToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": 7},
            },
            "field must be a string: command",
        ),
    ]

    for payload, expected_message in cases:
        assert_payload_error(claude_adapter, payload, expected_message)


test_valid_edit_returns_claimed_edit_from_nested_tool_input()
test_claimed_edit_fields_cannot_be_reassigned()
test_valid_bash_returns_none()
test_missing_session_id_raises_readable_error()
test_missing_hook_event_name_raises_readable_error()
test_missing_edit_fields_raise_readable_errors()
test_empty_required_strings_raise_readable_errors()
test_wrong_payload_types_raise_readable_errors()
test_wrong_event_name_raises_readable_error()
test_unsupported_tool_name_raises_readable_error()
test_malformed_bash_command_raises_readable_error()
print("test passed")
