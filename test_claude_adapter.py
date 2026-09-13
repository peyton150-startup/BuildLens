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

def write_payload_with(**extra):
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "notes.txt", "content": "hello"},
    }
    payload.update(extra)
    return payload


def test_the_session_working_directory_is_recorded():
    claude_adapter = importlib.import_module("claude_adapter")

    result = claude_adapter.parse_post_tool_use(write_payload_with(cwd="C:/proj"))

    assert result.session_cwd == "C:/proj"


def test_a_payload_without_a_working_directory_still_gets_a_claim():
    claude_adapter = importlib.import_module("claude_adapter")

    result = claude_adapter.parse_post_tool_use(write_payload_with())

    assert result.session_cwd is None
    assert result.details == {"content": "hello"}


def test_a_non_string_working_directory_raises_readable_error():
    claude_adapter = importlib.import_module("claude_adapter")

    try:
        claude_adapter.parse_post_tool_use(write_payload_with(cwd=5))
    except ValueError as error:
        assert "cwd" in str(error)
    else:
        raise AssertionError("a non-string cwd was accepted")


def test_the_working_directory_is_not_mixed_into_details():
    claude_adapter = importlib.import_module("claude_adapter")

    result = claude_adapter.parse_post_tool_use(write_payload_with(cwd="C:/proj"))

    assert "cwd" not in result.details


test_the_session_working_directory_is_recorded()
test_a_payload_without_a_working_directory_still_gets_a_claim()
test_a_non_string_working_directory_raises_readable_error()
test_the_working_directory_is_not_mixed_into_details()


# --- PreToolUse: a PROPOSAL, not a report (EV-P8-PRETOOLUSE-459) -------------
#
# Rows 1-7 were approved before any of this was written. A proposal arrives
# before the tool runs, so it says nothing about the disk: it gets its own type,
# and nothing that judges claims against the disk can be handed one.


def pre_payload(tool_name, tool_input, **top_level):
    payload = {
        "session_id": "session-9",
        "cwd": "C:\\repo",
        "hook_event_name": "PreToolUse",
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_use_id": "toolu_test",
    }
    payload.update(top_level)
    return payload


def expect_value_error(parse, payload, fragment):
    try:
        parse(payload)
    except ValueError as error:
        assert fragment in str(error), str(error)
    else:
        raise AssertionError("expected ValueError mentioning " + fragment)


def test_row_1_a_write_proposal_becomes_a_proposed_edit():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = pre_payload("Write", {"file_path": "C:\\repo\\notes.txt", "content": "hi\n"})

    result = claude_adapter.parse_pre_tool_use(payload)

    assert isinstance(result, claude_adapter.ProposedEdit)
    assert not isinstance(result, claude_adapter.ClaimedEdit)
    assert result.file_path == "C:\\repo\\notes.txt"
    assert result.session_id == "session-9"
    assert result.tool_name == "Write"
    assert result.details == {"content": "hi\n"}
    assert result.tool_use_id == "toolu_test"
    assert result.session_cwd == "C:\\repo"


def test_row_2_an_edit_proposal_holds_the_proposed_strings_and_flag():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = pre_payload(
        "Edit",
        {
            "file_path": "C:\\repo\\plan.md",
            "old_string": "alpha",
            "new_string": "beta",
            "replace_all": False,
        },
    )

    result = claude_adapter.parse_pre_tool_use(payload)

    assert result.details == {"old_string": "alpha", "new_string": "beta", "replace_all": False}


def test_row_3_a_bash_proposal_names_no_file_and_returns_none():
    claude_adapter = importlib.import_module("claude_adapter")
    payload = pre_payload("Bash", {"command": "sed -i 's/alpha/beta/' plan.md"})

    assert claude_adapter.parse_pre_tool_use(payload) is None


def test_row_4_each_parser_rejects_the_other_event():
    claude_adapter = importlib.import_module("claude_adapter")
    tool_input = {"file_path": "C:\\repo\\notes.txt", "content": "hi\n"}

    expect_value_error(
        claude_adapter.parse_pre_tool_use,
        pre_payload("Write", tool_input, hook_event_name="PostToolUse"),
        "PostToolUse",
    )
    expect_value_error(
        claude_adapter.parse_post_tool_use,
        pre_payload("Write", tool_input),
        "PreToolUse",
    )


def test_row_5_a_proposal_without_a_tool_use_id_raises():
    # tool_use_id is the only field that can ever pair a proposal with its report.
    claude_adapter = importlib.import_module("claude_adapter")
    payload = pre_payload("Write", {"file_path": "C:\\repo\\notes.txt", "content": "hi\n"})
    del payload["tool_use_id"]

    expect_value_error(claude_adapter.parse_pre_tool_use, payload, "tool_use_id")


def test_row_6_a_real_captured_edit_proposal_parses():
    # Captured from a live PreToolUse on 2026-09-13; paths and session trimmed the
    # same way as fixtures_post_tool_use_edit.json.
    import json
    from pathlib import Path

    claude_adapter = importlib.import_module("claude_adapter")
    fixture = Path(__file__).with_name("fixtures_pre_tool_use_edit.json")
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    result = claude_adapter.parse_pre_tool_use(payload)

    assert result.file_path == "C:\\repo\\hook_probe.txt"
    assert result.details == {"old_string": "alpha", "new_string": "beta", "replace_all": False}
    assert result.tool_use_id == "toolu_019jdKPf6Rm1QeKHXXQvo67D"


test_row_1_a_write_proposal_becomes_a_proposed_edit()
test_row_2_an_edit_proposal_holds_the_proposed_strings_and_flag()
test_row_3_a_bash_proposal_names_no_file_and_returns_none()
test_row_4_each_parser_rejects_the_other_event()
test_row_5_a_proposal_without_a_tool_use_id_raises()
test_row_6_a_real_captured_edit_proposal_parses()


# --- tool_use_id on ClaimedEdit: OPTIONAL, the learner's ruling -----------------
#
# A report's verdict never reads tool_use_id, so refusing a report without one
# would cost a verdict to protect only a pairing. Absent is recorded as None, a
# visible gap, never a stand-in id. ProposedEdit keeps it required: a proposal has
# no verdict to lose.


def post_write_payload(**top_level):
    payload = {
        "session_id": "session-9",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "C:\\repo\\notes.txt", "content": "hi\n"},
    }
    payload.update(top_level)
    return payload


def test_a_report_records_its_tool_use_id():
    claude_adapter = importlib.import_module("claude_adapter")

    claim = claude_adapter.parse_post_tool_use(post_write_payload(tool_use_id="toolu_abc"))

    assert claim.tool_use_id == "toolu_abc"


def test_a_report_without_a_tool_use_id_still_gets_a_claim():
    claude_adapter = importlib.import_module("claude_adapter")

    claim = claude_adapter.parse_post_tool_use(post_write_payload())

    assert claim is not None
    assert claim.tool_use_id is None


def test_a_non_string_tool_use_id_on_a_report_raises():
    claude_adapter = importlib.import_module("claude_adapter")

    expect_value_error(
        claude_adapter.parse_post_tool_use,
        post_write_payload(tool_use_id=42),
        "tool_use_id",
    )


def test_a_proposal_and_its_report_share_one_tool_use_id():
    claude_adapter = importlib.import_module("claude_adapter")
    tool_input = {"file_path": "C:\\repo\\notes.txt", "content": "hi\n"}

    proposal = claude_adapter.parse_pre_tool_use(
        pre_payload("Write", tool_input, tool_use_id="toolu_pair")
    )
    claim = claude_adapter.parse_post_tool_use(
        pre_payload("Write", tool_input, hook_event_name="PostToolUse", tool_use_id="toolu_pair")
    )

    assert proposal.tool_use_id == claim.tool_use_id == "toolu_pair"


test_a_report_records_its_tool_use_id()
test_a_report_without_a_tool_use_id_still_gets_a_claim()
test_a_non_string_tool_use_id_on_a_report_raises()
test_a_proposal_and_its_report_share_one_tool_use_id()
print("test passed")
