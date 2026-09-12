"""Tests for completeflow.py.

Run it with:

    python test_completeflow.py

These use real files and a real Git child, because the point of this module is
to join the real pieces together. Every row was specified before it was written.
"""

import importlib
import tempfile
from pathlib import Path


def temporary_directory():
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def payload(tool_name, tool_input):
    return {
        "hook_event_name": "PostToolUse",
        "session_id": "session-1",
        "tool_name": tool_name,
        "tool_input": tool_input,
    }


def write_payload(file_path, content):
    return payload("Write", {"file_path": str(file_path), "content": content})


def edit_payload(file_path, old_string, new_string):
    return payload(
        "Edit",
        {
            "file_path": str(file_path),
            "old_string": old_string,
            "new_string": new_string,
        },
    )


def test_a_write_claim_that_matches_the_file_holds():
    completeflow = importlib.import_module("completeflow")
    compare = importlib.import_module("compare")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"hello\n")

        result = completeflow.start_flow(write_payload(path, "hello\n"))

    assert result.verdict is compare.ComparisonVerdict.CLAIM_HOLDS
    assert result.claim.tool_name == "Write"
    assert result.observed.file_bytes == b"hello\n"


def test_an_edit_claim_that_landed_holds():
    completeflow = importlib.import_module("completeflow")
    compare = importlib.import_module("compare")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"goodbye world\n")

        result = completeflow.start_flow(edit_payload(path, "hello", "goodbye"))

    assert result.verdict is compare.ComparisonVerdict.CLAIM_HOLDS


def test_a_bash_payload_has_nothing_to_check():
    completeflow = importlib.import_module("completeflow")

    result = completeflow.start_flow(payload("Bash", {"command": "ls -la"}))

    assert result is None


def test_a_file_inside_a_repository_is_labelled_with_its_relative_path():
    completeflow = importlib.import_module("completeflow")

    # compare.py lives in this repository, so the root must reach observe_file
    # for this label to appear at all.
    this_file = Path("compare.py").resolve()
    result = completeflow.start_flow(write_payload(this_file, "not the real content\n"))

    assert result.observed.repository_relative_path == "compare.py"


def test_a_claim_about_a_deleted_folder_still_gets_a_verdict():
    completeflow = importlib.import_module("completeflow")
    compare = importlib.import_module("compare")

    with temporary_directory() as directory:
        missing_folder = Path(directory) / "gone"
        path = missing_folder / "app.py"

        result = completeflow.start_flow(write_payload(path, "hello\n"))

    assert result.verdict is compare.ComparisonVerdict.FILE_ABSENT
    assert result.observed.repository_relative_path is None


def test_a_file_outside_any_repository_still_gets_a_verdict():
    completeflow = importlib.import_module("completeflow")
    compare = importlib.import_module("compare")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"hello\n")

        result = completeflow.start_flow(write_payload(path, "hello\n"))

    assert result.verdict is compare.ComparisonVerdict.CLAIM_HOLDS
    assert result.observed.repository_relative_path is None


def test_a_tool_with_no_comparison_is_rejected():
    completeflow = importlib.import_module("completeflow")

    try:
        completeflow.start_flow(payload("Notebook", {"file_path": "notes.md", "content": "x"}))
    except ValueError:
        pass
    else:
        raise AssertionError("a tool BuildLens cannot check was accepted")


test_a_write_claim_that_matches_the_file_holds()
test_an_edit_claim_that_landed_holds()
test_a_bash_payload_has_nothing_to_check()
test_a_file_inside_a_repository_is_labelled_with_its_relative_path()
test_a_claim_about_a_deleted_folder_still_gets_a_verdict()
test_a_file_outside_any_repository_still_gets_a_verdict()
test_a_tool_with_no_comparison_is_rejected()

def test_a_claim_from_a_claude_hook_is_recorded_as_claude_provenance():
    completeflow = importlib.import_module("completeflow")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"hello\n")

        result = completeflow.start_flow(write_payload(path, "hello\n"))

    assert result.provenance is completeflow.Provenance.CLAUDE


def test_provenance_names_both_streams_that_will_exist():
    completeflow = importlib.import_module("completeflow")

    names = {member.name for member in completeflow.Provenance}

    assert names == {"CLAUDE", "HUMAN"}


test_a_claim_from_a_claude_hook_is_recorded_as_claude_provenance()
test_provenance_names_both_streams_that_will_exist()

def test_a_file_in_no_repository_gets_an_unavailable_base_version():
    completeflow = importlib.import_module("completeflow")
    git_adapter = importlib.import_module("git_adapter")

    calls = []

    def refuse(*args, **kwargs):
        calls.append(args)
        raise AssertionError("Git was asked for a base version with no repository root")

    original = git_adapter.capture_base_version
    git_adapter.capture_base_version = refuse
    try:
        with temporary_directory() as directory:
            path = Path(directory) / "notes.md"
            path.write_bytes(b"hello\n")

            result = completeflow.start_flow(write_payload(path, "hello\n"))
    finally:
        git_adapter.capture_base_version = original

    assert result.base_version.status is git_adapter.BaseVersionStatus.UNAVAILABLE
    assert result.base_version.detail is not None
    assert calls == []


def test_a_file_in_this_repository_records_its_committed_base_version():
    completeflow = importlib.import_module("completeflow")
    git_adapter = importlib.import_module("git_adapter")

    this_file = Path("compare.py").resolve()
    result = completeflow.start_flow(write_payload(this_file, "not the real content\n"))

    assert result.base_version.status is git_adapter.BaseVersionStatus.COMMITTED
    assert len(result.base_version.commit) == 40


test_a_file_in_no_repository_gets_an_unavailable_base_version()
test_a_file_in_this_repository_records_its_committed_base_version()
print("test passed")
