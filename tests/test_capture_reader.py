"""Tests for capture_reader.py.

Run it with:

    python tests/test_capture_reader.py

These write real capture files to a throwaway directory. The reader's job is to
decide what each appended line means, so the lines are written as the capture
hook writes them: one JSON payload, then the blank line its `echo` adds.
"""

import sys
from pathlib import Path

# Put the repository root first on the import search path, so the product
# modules it holds import by bare name when this file runs as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import tempfile

import capture_reader

FIXTURES = Path(__file__).resolve().parent


def temporary_directory():
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def post_tool_use_line(file_path: str) -> bytes:
    payload = json.loads((FIXTURES / "fixtures_post_tool_use_edit.json").read_text(encoding="utf-8"))
    payload["tool_input"]["file_path"] = file_path
    return json.dumps(payload).encode("utf-8") + b"\n"


def pre_tool_use_line() -> bytes:
    payload = json.loads((FIXTURES / "fixtures_pre_tool_use_edit.json").read_text(encoding="utf-8"))
    return json.dumps(payload).encode("utf-8") + b"\n"


def write_capture(directory: str, content: bytes) -> Path:
    path = Path(directory) / "payload_samples.jsonl"
    path.write_bytes(content)
    return path


def test_a_missing_capture_file_counts_as_position_zero():
    with temporary_directory() as directory:
        path = Path(directory) / "payload_samples.jsonl"

        assert capture_reader.count_complete_lines(path) == 0


def test_a_half_written_last_line_is_not_counted():
    with temporary_directory() as directory:
        path = write_capture(directory, b'{"a": 1}\n{"b":')

        assert capture_reader.count_complete_lines(path) == 1


def test_only_lines_after_the_position_become_claims_with_their_line_numbers():
    with temporary_directory() as directory:
        path = write_capture(
            directory,
            post_tool_use_line("C:/repo/old.py")
            + b"\n"
            + post_tool_use_line("C:/repo/new.py"),
        )

        result = capture_reader.read_capture(path, 2)

    assert [(c.line_number, c.claim.file_path) for c in result.claims] == [(3, "C:/repo/new.py")]
    assert result.skipped == []


def test_pre_tool_use_lines_are_ignored_silently():
    with temporary_directory() as directory:
        path = write_capture(directory, pre_tool_use_line())

        result = capture_reader.read_capture(path, 0)

    assert result.claims == []
    assert result.skipped == []


def test_whitespace_only_lines_are_skipped_silently():
    with temporary_directory() as directory:
        path = write_capture(directory, b"\n" + b"\r\n" + b"   \n")

        result = capture_reader.read_capture(path, 0)

    assert result.claims == []
    assert result.skipped == []


def test_a_complete_line_that_is_not_json_is_named():
    with temporary_directory() as directory:
        path = write_capture(directory, b"\n" + b"{\n")

        result = capture_reader.read_capture(path, 0)

    assert result.claims == []
    assert result.skipped == [capture_reader.SkippedLine(2, "not valid JSON")]


def test_an_unterminated_last_line_is_named_as_still_being_written():
    with temporary_directory() as directory:
        path = write_capture(directory, b'{"hook_event_name": "PostTo')

        result = capture_reader.read_capture(path, 0)

    assert result.claims == []
    assert result.skipped == [capture_reader.SkippedLine(1, "still being written")]


def test_a_post_tool_use_the_parser_rejects_is_named_with_its_reason():
    payload = json.loads((FIXTURES / "fixtures_post_tool_use_edit.json").read_text(encoding="utf-8"))
    payload["tool_input"]["path"] = payload["tool_input"].pop("file_path")

    with temporary_directory() as directory:
        path = write_capture(directory, json.dumps(payload).encode("utf-8") + b"\n")

        result = capture_reader.read_capture(path, 0)

    assert result.claims == []
    assert result.skipped == [
        capture_reader.SkippedLine(1, "not a usable claim (missing required field: file_path)")
    ]


test_a_missing_capture_file_counts_as_position_zero()
test_a_half_written_last_line_is_not_counted()
test_only_lines_after_the_position_become_claims_with_their_line_numbers()
test_pre_tool_use_lines_are_ignored_silently()
test_whitespace_only_lines_are_skipped_silently()
test_a_complete_line_that_is_not_json_is_named()
test_an_unterminated_last_line_is_named_as_still_being_written()
test_a_post_tool_use_the_parser_rejects_is_named_with_its_reason()
print("test passed")
