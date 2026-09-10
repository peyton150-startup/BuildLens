"""Translate Claude PostToolUse payloads into BuildLens representations."""

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


def _required_object(
    values: dict[str, object], field: str
) -> dict[str, object]:
    value = _required_value(values, field)
    if not isinstance(value, dict):
        raise ValueError("field must be an object: " + field)

    return value


def parse_post_tool_use(payload: object) -> ClaimedEdit | None:
    """Return a claimed edit, or None when no file is directly observed."""
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    hook_event_name = _required_string(payload, "hook_event_name")
    if hook_event_name != "PostToolUse":
        raise ValueError("unexpected hook event: " + hook_event_name)

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

    return ClaimedEdit(
        file_path=file_path,
        session_id=session_id,
        tool_name=tool_name,
        details=MappingProxyType(details),
    )
