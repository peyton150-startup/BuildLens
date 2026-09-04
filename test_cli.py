"""Tests for cli.py.

Run it with:

    python test_cli.py

cli.py owns the process boundary only, so these patch snapshot.capture_snapshot
and check what reaches stdout, stderr, and the returned status.
"""

import io
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from cli import format_summary, main
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


test_analyze_prints_the_root_and_both_labelled_views()
test_a_capture_failure_reports_the_root_it_was_inspecting()
test_a_failure_before_the_root_was_resolved_prints_no_repository_line()
test_no_partial_summary_is_printed_on_failure()
test_analyze_takes_no_path_argument()
test_a_missing_command_is_rejected()
test_an_unsupported_command_is_rejected()
test_format_summary_still_renders_three_labelled_counts()
print("test passed")
