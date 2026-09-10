"""Tests for the Claude hook adapter.

Run it with:

    python test_claude_adapter.py
"""

import importlib
from dataclasses import FrozenInstanceError


def test_empty_write_content_is_recorded_as_claimed():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "notes.txt",
            "content": "",
        },
    }

    result = claude_adapter.parse_post_tool_use(payload)

    assert result.details == {"content": ""}


def test_empty_file_path_still_raises():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "",
            "content": "hello",
        },
    }

    assert_payload_error(
        claude_adapter, payload, "empty required field: file_path"
    )


def _edit_payload(tool_input):
    return {
        "session_id": "session-7",
        "hook_event_name": "PostToolUse",
        "tool_name": "Edit",
        "tool_input": tool_input,
    }


def test_edit_details_hold_the_claimed_strings_and_flag():
    claude_adapter = importlib.import_module("claude_adapter")

    result = claude_adapter.parse_post_tool_use(
        _edit_payload(
            {
                "file_path": "notes.md",
                "old_string": "cat",
                "new_string": "dog",
                "replace_all": True,
            }
        )
    )

    assert result.details == {
        "old_string": "cat",
        "new_string": "dog",
        "replace_all": True,
    }


def test_absent_replace_all_is_recorded_as_absent():
    claude_adapter = importlib.import_module("claude_adapter")

    result = claude_adapter.parse_post_tool_use(
        _edit_payload(
            {
                "file_path": "notes.md",
                "old_string": "cat",
                "new_string": "dog",
            }
        )
    )

    assert "replace_all" not in result.details
    assert result.details == {"old_string": "cat", "new_string": "dog"}


def test_edit_that_deletes_text_records_empty_new_string():
    claude_adapter = importlib.import_module("claude_adapter")

    result = claude_adapter.parse_post_tool_use(
        _edit_payload(
            {
                "file_path": "notes.md",
                "old_string": "dead code",
                "new_string": "",
            }
        )
    )

    assert result.details["new_string"] == ""


def test_empty_old_string_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")

    assert_payload_error(
        claude_adapter,
        _edit_payload(
            {"file_path": "notes.md", "old_string": "", "new_string": "dog"}
        ),
        "empty required field: old_string",
    )


def test_non_boolean_replace_all_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")

    assert_payload_error(
        claude_adapter,
        _edit_payload(
            {
                "file_path": "notes.md",
                "old_string": "cat",
                "new_string": "dog",
                "replace_all": "yes",
            }
        ),
        "field must be a boolean: replace_all",
    )


def test_details_cannot_be_mutated_after_construction():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "notes.txt",
            "content": "hello",
        },
    }

    result = claude_adapter.parse_post_tool_use(payload)

    try:
        result.details["content"] = "something Claude never claimed"
    except TypeError:
        pass
    else:
        raise AssertionError("ClaimedEdit allowed a claim to be rewritten")

    assert result.details == {"content": "hello"}


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
            "old_string": "cat",
            "new_string": "dog",
        },
    }

    result = claude_adapter.parse_post_tool_use(payload)

    assert result == claude_adapter.ClaimedEdit(
        file_path="C:/repo/app.py",
        session_id="session-7",
        tool_name="Edit",
        details={"old_string": "cat", "new_string": "dog"},
    )


def test_valid_write_returns_claimed_edit_from_nested_tool_input():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "notes.txt",
            "content": "hello",
        },
    }

    result = claude_adapter.parse_post_tool_use(payload)

    assert result == claude_adapter.ClaimedEdit(
        file_path="notes.txt",
        session_id="session-9",
        tool_name="Write",
        details={"content": "hello"},
    )


def test_claimed_edit_fields_cannot_be_reassigned():
    claude_adapter = importlib.import_module("claude_adapter")
    edit = claude_adapter.ClaimedEdit(
        file_path="C:/repo/app.py",
        session_id="session-7",
        tool_name="Edit",
        details={},
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


def test_missing_write_file_path_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "content": "hello",
        },
    }

    assert_payload_error(
        claude_adapter,
        payload,
        "missing required field: file_path",
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


def test_write_details_hold_the_claimed_content():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "notes.txt",
            "content": "hello",
        },
    }

    result = claude_adapter.parse_post_tool_use(payload)

    assert result.details == {"content": "hello"}


def test_missing_write_content_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "notes.txt",
        },
    }

    assert_payload_error(claude_adapter, payload, "missing required field: content")


test_valid_edit_returns_claimed_edit_from_nested_tool_input()
test_valid_write_returns_claimed_edit_from_nested_tool_input()
test_claimed_edit_fields_cannot_be_reassigned()
test_valid_bash_returns_none()
test_missing_session_id_raises_readable_error()
test_missing_hook_event_name_raises_readable_error()
test_missing_edit_fields_raise_readable_errors()
test_empty_required_strings_raise_readable_errors()
test_wrong_payload_types_raise_readable_errors()
test_wrong_event_name_raises_readable_error()
test_unsupported_tool_name_raises_readable_error()
test_missing_write_file_path_raises_readable_error()
test_malformed_bash_command_raises_readable_error()
test_write_details_hold_the_claimed_content()
test_missing_write_content_raises_readable_error()
test_details_cannot_be_mutated_after_construction()
test_empty_write_content_is_recorded_as_claimed()
test_empty_file_path_still_raises()
test_edit_details_hold_the_claimed_strings_and_flag()
test_absent_replace_all_is_recorded_as_absent()
test_edit_that_deletes_text_records_empty_new_string()
test_empty_old_string_raises_readable_error()
test_non_boolean_replace_all_raises_readable_error()
print("test passed")
