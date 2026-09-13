"""Translate Claude PreToolUse and PostToolUse payloads into BuildLens representations.

The two events carry identical tool_input, but they do not mean the same thing:

    PostToolUse   a REPORT: the tool ran and succeeded   -> ClaimedEdit
    PreToolUse    a PROPOSAL: the tool has not run yet   -> ProposedEdit

A proposal may still be denied, rejected, or fail after its hook fires, and a
tool call can fail before any hook fires at all. So neither type is evidence of
what the disk holds; only observing the file is. They are separate types so that
nothing which judges claims against the disk can be handed a proposal.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class ClaimedEdit:
    """Hold the edit details claimed by one Claude hook payload."""

    file_path: str
    session_id: str
    tool_name: str
    details: Mapping[str, object]
    # The directory the Claude session was working in. Optional: a payload from
    # another Claude version, or relayed by another agent, may not send one, and
    # refusing such a payload would cost a claim BuildLens could otherwise judge.
    # Only the Stop reconciliation scan needs it, and only as a place to run Git.
    session_cwd: str | None = None


@dataclass(frozen=True)
class ProposedEdit:
    """Hold the edit details of one tool call Claude has PROPOSED but not run.

    Same fields as ClaimedEdit, deliberately a different type: a ClaimedEdit is a
    report to check against the disk, a ProposedEdit is a request that a later
    phase may approve or deny. In Phase 8 BuildLens only records proposals.
    """

    file_path: str
    session_id: str
    tool_name: str
    details: Mapping[str, object]
    # Required, unlike session_cwd: it is the only field that can ever pair this
    # proposal with the report of the same tool call.
    tool_use_id: str
    session_cwd: str | None = None


def _required_value(values: dict[str, object], field: str) -> object:
    if field not in values:
        raise ValueError("missing required field: " + field)

    return values[field]


def _required_string(values: dict[str, object], field: str) -> str:
    value = _required_value(values, field)
    if not isinstance(value, str):
        raise ValueError("field must be a string: " + field)

    if value == "":
        raise ValueError("empty required field: " + field)

    return value


def _required_text(values: dict[str, object], field: str) -> str:
    """Return a claimed string, allowing "" as a value the tool may really send."""
    value = _required_value(values, field)
    if not isinstance(value, str):
        raise ValueError("field must be a string: " + field)

    return value


def _optional_string(values: dict[str, object], field: str) -> str | None:
    """Return a string the sender may omit, but must type correctly if sent."""
    if field not in values:
        return None

    value = values[field]
    if not isinstance(value, str):
        raise ValueError("field must be a string: " + field)

    return value


def _required_boolean(values: dict[str, object], field: str) -> bool:
    value = _required_value(values, field)
    if not isinstance(value, bool):
        raise ValueError("field must be a boolean: " + field)

    return value


def _required_object(
    values: dict[str, object], field: str
) -> dict[str, object]:
    value = _required_value(values, field)
    if not isinstance(value, dict):
        raise ValueError("field must be an object: " + field)

    return value


def _checked_event(payload: object, expected_event: str) -> dict[str, object]:
    """Return payload as a dict after confirming it is the expected hook event."""
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    hook_event_name = _required_string(payload, "hook_event_name")
    if hook_event_name != expected_event:
        raise ValueError("unexpected hook event: " + hook_event_name)

    return payload


def _tool_call_fields(payload: dict[str, object]) -> dict[str, object] | None:
    """Return the fields both events share, or None when the tool names no file.

    PreToolUse and PostToolUse send identical tool_input, so this is written once:
    the two parsers differ only in which event they accept and what they build.
    """
    session_id = _required_string(payload, "session_id")
    tool_name = _required_string(payload, "tool_name")
    tool_input = _required_object(payload, "tool_input")

    if tool_name == "Bash":
        _required_string(tool_input, "command")
        return None

    if tool_name not in ("Edit", "Write"):
        raise ValueError("unsupported tool_name: " + tool_name)

    file_path = _required_string(tool_input, "file_path")

    details: dict[str, object] = {}
    if tool_name == "Write":
        details["content"] = _required_text(tool_input, "content")
    else:
        details["old_string"] = _required_string(tool_input, "old_string")
        details["new_string"] = _required_text(tool_input, "new_string")
        if "replace_all" in tool_input:
            details["replace_all"] = _required_boolean(tool_input, "replace_all")

    return {
        "file_path": file_path,
        "session_id": session_id,
        "tool_name": tool_name,
        "details": MappingProxyType(details),
        # Read from the payload's top level, never from tool_input, so details
        # keeps one source: the keys the tool itself sent.
        "session_cwd": _optional_string(payload, "cwd"),
    }


def parse_post_tool_use(payload: object) -> ClaimedEdit | None:
    """Return a claimed edit, or None when no file is directly observed."""
    fields = _tool_call_fields(_checked_event(payload, "PostToolUse"))
    if fields is None:
        return None

    return ClaimedEdit(**fields)


def parse_pre_tool_use(payload: object) -> ProposedEdit | None:
    """Return a proposed edit, or None when the proposed tool names no file."""
    checked = _checked_event(payload, "PreToolUse")
    tool_use_id = _required_string(checked, "tool_use_id")

    fields = _tool_call_fields(checked)
    if fields is None:
        return None

    return ProposedEdit(tool_use_id=tool_use_id, **fields)
