"""Tests for cli.py.

Run it with:

    python test_cli.py

cli.py owns the process boundary only, so these patch snapshot.capture_snapshot
and check what reaches stdout, stderr, and the returned status.
"""

import io
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from pathlib import Path

from claude_adapter import ClaimedEdit
from cli import format_local_time, format_summary, main
from compare import ComparisonVerdict
from completeflow import CompleteCompare, Provenance
from file_observer import ObservationStatus, ObservedFile
from git_adapter import GitCaptureError
from snapshot import Snapshot
from summarize import DiffSummary


SNAPSHOT = Snapshot(
    repository_root="C:/projects/example",
    unstaged=DiffSummary(3, 4, 1),
    staged=DiffSummary(1, 2, 0),
)


def run_main(argv, snapshot_result=None, snapshot_error=None):
    """Run main with capture_snapshot patched; return status, stdout, stderr."""
    out = io.StringIO()
    err = io.StringIO()

    if snapshot_error is not None:
        replacement = patch("snapshot.capture_snapshot", side_effect=snapshot_error)
    else:
        replacement = patch("snapshot.capture_snapshot", return_value=snapshot_result)

    with replacement, redirect_stdout(out), redirect_stderr(err):
        status = main(argv)

    return status, out.getvalue(), err.getvalue()


def expect_system_exit_2(argv):
    """Malformed command lines stay argparse's to reject."""
    err = io.StringIO()
    try:
        with redirect_stderr(err):
            main(argv)
    except SystemExit as error:
        assert error.code == 2
    else:
        raise AssertionError("main did not raise SystemExit for " + str(argv))


def test_analyze_prints_the_root_and_both_labelled_views():
    status, out, err = run_main(["cli.py", "analyze"], snapshot_result=SNAPSHOT)

    assert status == 0
    assert err == ""
    assert out == (
        "Repository: C:/projects/example\n"
        "\n"
        "UNSTAGED\n"
        "Files changed: 3\n"
        "Lines added: 4\n"
        "Lines removed: 1\n"
        "\n"
        "STAGED\n"
        "Files changed: 1\n"
        "Lines added: 2\n"
        "Lines removed: 0\n"
    )


def test_a_capture_failure_reports_the_root_it_was_inspecting():
    error = GitCaptureError("UNSTAGED tracked: Git failed with status 128")
    error.repository_root = "C:/Users/nicol"

    status, out, err = run_main(["cli.py", "analyze"], snapshot_error=error)

    assert status == 1
    assert out == ""
    assert err == (
        "Repository: C:/Users/nicol\n"
        "UNSTAGED tracked: Git failed with status 128\n"
        "Run buildlens analyze again.\n"
    )


def test_a_failure_before_the_root_was_resolved_prints_no_repository_line():
    error = GitCaptureError("ROOT resolution: Git failed with status 128")

    status, out, err = run_main(["cli.py", "analyze"], snapshot_error=error)

    assert status == 1
    assert out == ""
    assert err == (
        "ROOT resolution: Git failed with status 128\n"
        "Run buildlens analyze again.\n"
    )


def test_no_partial_summary_is_printed_on_failure():
    error = GitCaptureError("UNTRACKED new.py: Git failed with status 128")

    status, out, err = run_main(["cli.py", "analyze"], snapshot_error=error)

    assert status == 1
    assert "Files changed" not in out
    assert "Files changed" not in err


def test_analyze_takes_no_path_argument():
    expect_system_exit_2(["cli.py", "analyze", "changes.diff"])


def test_a_missing_command_is_rejected():
    expect_system_exit_2(["cli.py"])


def test_an_unsupported_command_is_rejected():
    expect_system_exit_2(["cli.py", "banana"])


def test_format_summary_still_renders_three_labelled_counts():
    assert format_summary(DiffSummary(2, 17, 4)) == (
        "Files changed: 2\nLines added: 17\nLines removed: 4"
    )


MOMENT = datetime(2026, 9, 11, 17, 16, tzinfo=timezone.utc)


def test_a_stored_moment_is_shown_as_12_hour_time_in_the_given_zone():
    assert format_local_time(MOMENT, ZoneInfo("America/New_York")) == "01:16 PM EDT"


def test_the_same_moment_is_shown_in_whatever_zone_is_asked_for():
    assert format_local_time(MOMENT, ZoneInfo("Europe/London")) == "06:16 PM BST"


def test_winter_moments_are_shown_in_standard_time_not_daylight_time():
    winter = datetime(2026, 1, 15, 17, 16, tzinfo=timezone.utc)
    assert format_local_time(winter, ZoneInfo("America/New_York")) == "12:16 PM EST"


def test_with_no_zone_the_machines_current_zone_is_used():
    shown = format_local_time(MOMENT)
    assert shown.endswith(("AM", "PM")) or " AM " in shown or " PM " in shown


test_analyze_prints_the_root_and_both_labelled_views()
test_a_capture_failure_reports_the_root_it_was_inspecting()
test_a_failure_before_the_root_was_resolved_prints_no_repository_line()
test_no_partial_summary_is_printed_on_failure()
test_analyze_takes_no_path_argument()
test_a_missing_command_is_rejected()
test_an_unsupported_command_is_rejected()
test_format_summary_still_renders_three_labelled_counts()
test_a_stored_moment_is_shown_as_12_hour_time_in_the_given_zone()
test_the_same_moment_is_shown_in_whatever_zone_is_asked_for()
test_winter_moments_are_shown_in_standard_time_not_daylight_time()
test_with_no_zone_the_machines_current_zone_is_used()

# --- ingest -----------------------------------------------------------------

INGEST_CLAIM = ClaimedEdit(
    file_path="C:/proj/src/app.py",
    session_id="session-1",
    tool_name="Write",
    details={"content": "hello\n"},
)

INGEST_OBSERVED = ObservedFile(
    file_path="C:/proj/src/app.py",
    status=ObservationStatus.READ,
    file_bytes=b"hello\n",
    content_hash="9b71d224bd62",
    observed_at=datetime(2026, 9, 12, 1, 14, tzinfo=timezone.utc),
    repository_relative_path="src/app.py",
)


def ingest_record(verdict):
    return CompleteCompare(
        claim=INGEST_CLAIM,
        observed=INGEST_OBSERVED,
        verdict=verdict,
        provenance=Provenance.CLAUDE,
    )


PAYLOAD_TEXT = json.dumps(
    {
        "hook_event_name": "PostToolUse",
        "session_id": "session-1",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "C:/proj/src/app.py",
            "content": "hello" + chr(10),
        },
    }
)


def run_ingest(argv, record=None, error=None, stdin_text=""):
    """Run main with start_flow patched and stdin prepared."""
    out = io.StringIO()
    err = io.StringIO()

    if error is not None:
        replacement = patch("completeflow.start_flow", side_effect=error)
    else:
        replacement = patch("completeflow.start_flow", return_value=record)

    with replacement, patch("sys.stdin", io.StringIO(stdin_text)), \
            redirect_stdout(out), redirect_stderr(err):
        status = main(argv)

    return status, out.getvalue(), err.getvalue()


def test_ingest_reads_a_payload_file_and_prints_the_verdict(tmp_payload="payload_for_test.json"):
    Path(tmp_payload).write_text(PAYLOAD_TEXT, encoding="utf-8")
    try:
        status, out, err = run_ingest(
            ["cli.py", "ingest", tmp_payload],
            record=ingest_record(ComparisonVerdict.CLAIM_HOLDS),
        )
    finally:
        Path(tmp_payload).unlink()

    assert status == 0
    assert "claim holds" in out
    assert "C:/proj/src/app.py" in out
    assert "read" in out
    assert err == ""


def test_ingest_with_no_path_reads_standard_input():
    status, out, err = run_ingest(
        ["cli.py", "ingest"],
        record=ingest_record(ComparisonVerdict.CLAIM_HOLDS),
        stdin_text=PAYLOAD_TEXT,
    )

    assert status == 0
    assert "claim holds" in out
    assert err == ""


def test_a_bash_payload_reports_that_there_is_nothing_to_check():
    status, out, err = run_ingest(
        ["cli.py", "ingest"], record=None, stdin_text=PAYLOAD_TEXT
    )

    assert status == 0
    assert "nothing to check" in out
    assert err == ""


def test_a_claim_that_does_not_hold_is_still_a_successful_run():
    status, out, err = run_ingest(
        ["cli.py", "ingest"],
        record=ingest_record(ComparisonVerdict.CLAIM_DOES_NOT_HOLD),
        stdin_text=PAYLOAD_TEXT,
    )

    assert status == 0
    assert "claim does not hold" in out


def test_malformed_json_is_reported_without_any_verdict():
    status, out, err = run_ingest(
        ["cli.py", "ingest"],
        record=ingest_record(ComparisonVerdict.CLAIM_HOLDS),
        stdin_text="{not json at all",
    )

    assert status == 1
    assert out == ""
    assert err != ""


def test_a_missing_payload_file_is_reported():
    status, out, err = run_ingest(
        ["cli.py", "ingest", "no_such_payload.json"],
        record=ingest_record(ComparisonVerdict.CLAIM_HOLDS),
    )

    assert status == 1
    assert err != ""


def test_a_tool_buildlens_cannot_check_is_reported():
    status, out, err = run_ingest(
        ["cli.py", "ingest"],
        error=ValueError("unsupported tool_name: Notebook"),
        stdin_text=PAYLOAD_TEXT,
    )

    assert status == 1
    assert out == ""
    assert "Notebook" in err


test_ingest_reads_a_payload_file_and_prints_the_verdict()
test_ingest_with_no_path_reads_standard_input()
test_a_bash_payload_reports_that_there_is_nothing_to_check()
test_a_claim_that_does_not_hold_is_still_a_successful_run()
test_malformed_json_is_reported_without_any_verdict()
test_a_missing_payload_file_is_reported()
test_a_tool_buildlens_cannot_check_is_reported()


def test_ingest_prints_which_stream_the_change_came_from():
    status, out, err = run_ingest(
        ["cli.py", "ingest"],
        record=ingest_record(ComparisonVerdict.CLAIM_HOLDS),
        stdin_text=PAYLOAD_TEXT,
    )

    assert status == 0
    assert "claude" in out


test_ingest_prints_which_stream_the_change_came_from()
print("test passed")
