"""Tests for the interactive single-process find workflow.

Run it with:

    python tests/test_find_workflow.py

The workflow's input and output functions are injected so confirmation,
interrupt, and retry paths are deterministic without a real terminal.
"""

import sys
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unittest.mock import patch
from datetime import datetime, timezone

from git_adapter import GitCaptureError
from reconcile import Picture


BASELINE = Picture(
    datetime(2026, 9, 16, 10, 0, tzinfo=timezone.utc),
    {"a.py": "h1"},
)
WITNESS = Picture(
    datetime(2026, 9, 16, 10, 30, tzinfo=timezone.utc),
    {"a.py": "h2"},
)


def test_a_baseline_git_failure_stops_before_waiting_for_input():
    import find_workflow

    messages = []
    input_calls = []

    def read_input(prompt):
        input_calls.append(prompt)
        return ""

    error = GitCaptureError("TRACKED discovery: Git failed with status 128")

    with patch("find_workflow.git_adapter.capture_repository_root", return_value="C:/repo"), \
            patch("find_workflow.take_picture", side_effect=error):
        outcome = find_workflow.run_find(
            Path("C:/repo"),
            read_input=read_input,
            write_output=messages.append,
        )

    assert outcome.status == 1
    assert outcome.result is None
    assert input_calls == []
    assert any("baseline picture failed" in message.lower() for message in messages)
    assert any("TRACKED discovery" in message for message in messages)


def test_no_at_end_confirmation_returns_to_waiting_then_yes_takes_one_witness():
    import find_workflow

    answers = iter(["", "n", "", "y"])
    prompts = []

    def read_input(prompt):
        prompts.append(prompt)
        return next(answers)

    with patch("find_workflow.git_adapter.capture_repository_root", return_value="C:/repo"), \
            patch("find_workflow.take_picture", side_effect=[BASELINE, WITNESS]) as pictures, \
            patch("find_workflow.count_complete_lines", return_value=0):
        outcome = find_workflow.run_find(
            Path("C:/repo"),
            read_input=read_input,
            write_output=lambda message: None,
        )

    assert outcome.status == 0
    assert outcome.result.baseline is BASELINE
    assert outcome.result.witness is WITNESS
    assert pictures.call_count == 2
    assert sum("Press Enter to end" in prompt for prompt in prompts) == 2
    assert sum("Are you sure" in prompt for prompt in prompts) == 2


def test_ctrl_c_while_waiting_can_confirm_the_witness():
    import find_workflow

    calls = 0

    def read_input(prompt):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise KeyboardInterrupt
        assert "Are you sure" in prompt
        return "y"

    with patch("find_workflow.git_adapter.capture_repository_root", return_value="C:/repo"), \
            patch("find_workflow.take_picture", side_effect=[BASELINE, WITNESS]), \
            patch("find_workflow.count_complete_lines", return_value=0):
        outcome = find_workflow.run_find(
            Path("C:/repo"),
            read_input=read_input,
            write_output=lambda message: None,
        )

    assert outcome.status == 0
    assert outcome.result.witness is WITNESS


def test_ctrl_c_during_the_witness_returns_no_partial_result():
    import find_workflow

    answers = iter(["", "y"])
    messages = []

    with patch("find_workflow.git_adapter.capture_repository_root", return_value="C:/repo"), \
            patch("find_workflow.take_picture", side_effect=[BASELINE, KeyboardInterrupt]), \
            patch("find_workflow.count_complete_lines", return_value=0):
        outcome = find_workflow.run_find(
            Path("C:/repo"),
            read_input=lambda prompt: next(answers),
            write_output=messages.append,
        )

    assert outcome.status == 1
    assert outcome.result is None
    assert any("witness picture was interrupted" in message.lower() for message in messages)


def test_a_witness_git_failure_can_retry_without_replacing_the_baseline():
    import find_workflow

    answers = iter(["", "y", "y"])
    messages = []
    error = GitCaptureError("TRACKED discovery: Git failed with status 128")

    with patch("find_workflow.git_adapter.capture_repository_root", return_value="C:/repo"), \
            patch("find_workflow.take_picture", side_effect=[BASELINE, error, WITNESS]) as pictures, \
            patch("find_workflow.count_complete_lines", return_value=7):
        outcome = find_workflow.run_find(
            Path("C:/repo"),
            read_input=lambda prompt: next(answers),
            write_output=messages.append,
        )

    assert outcome.status == 0
    assert outcome.result.baseline is BASELINE
    assert outcome.result.witness is WITNESS
    assert outcome.result.capture_position == 7
    assert pictures.call_count == 3
    assert any("witness picture failed" in message.lower() for message in messages)


def test_no_after_a_witness_failure_warns_and_confirms_before_exit():
    import find_workflow

    answers = iter(["", "y", "n", "y"])
    messages = []
    error = GitCaptureError("TRACKED discovery: Git failed with status 128")

    with patch("find_workflow.git_adapter.capture_repository_root", return_value="C:/repo"), \
            patch("find_workflow.take_picture", side_effect=[BASELINE, error]), \
            patch("find_workflow.count_complete_lines", return_value=7):
        outcome = find_workflow.run_find(
            Path("C:/repo"),
            read_input=lambda prompt: next(answers),
            write_output=messages.append,
        )

    assert outcome.status == 1
    assert outcome.result is None
    assert any("can no longer report what changed" in message for message in messages)
    assert any("files" in message.lower() and "stay exactly as they are" in message for message in messages)


def test_missing_capture_at_both_ends_still_reconciles_observed_changes():
    import find_workflow

    answers = iter(["", "y"])

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
        root = Path(directory)
        with patch("find_workflow.git_adapter.capture_repository_root", return_value=str(root)), \
                patch("find_workflow.take_picture", side_effect=[BASELINE, WITNESS]):
            outcome = find_workflow.run_find(
                root,
                read_input=lambda prompt: next(answers),
                write_output=lambda message: None,
            )

    assert outcome.status == 0
    assert outcome.result.capture_missing is True
    assert outcome.result.capture.claims == []
    assert outcome.result.coverage.held == set()
    assert [change.repository_relative_path for change in outcome.result.scan.changes] == ["a.py"]


def test_capture_present_at_baseline_but_missing_at_witness_produces_no_result():
    import find_workflow

    answers = iter(["", "y", "n", "y"])
    messages = []

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
        root = Path(directory)
        capture_path = root / "payload_samples.jsonl"
        capture_path.write_text("{}\n", encoding="utf-8")
        picture_calls = 0

        def take_picture_then_remove_capture(repository):
            nonlocal picture_calls
            picture_calls += 1
            if picture_calls == 1:
                return BASELINE
            capture_path.unlink(missing_ok=True)
            return WITNESS

        with patch("find_workflow.git_adapter.capture_repository_root", return_value=str(root)), \
                patch("find_workflow.take_picture", side_effect=take_picture_then_remove_capture):
            outcome = find_workflow.run_find(
                root,
                read_input=lambda prompt: next(answers),
                write_output=messages.append,
            )

    assert outcome.status == 1
    assert outcome.result is None
    assert any(str(capture_path) in message for message in messages)
    assert any("capture file" in message.lower() and "missing" in message.lower() for message in messages)


def test_missing_capture_can_reappear_on_a_witness_retry():
    import find_workflow

    answers = iter(["", "y", "y"])

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
        root = Path(directory)
        capture_path = root / "payload_samples.jsonl"
        capture_path.write_text("\n", encoding="utf-8")
        picture_calls = 0

        def pictures_with_capture_recovery(repository):
            nonlocal picture_calls
            picture_calls += 1
            if picture_calls == 1:
                return BASELINE
            if picture_calls == 2:
                capture_path.unlink()
                return WITNESS
            capture_path.write_text("\n", encoding="utf-8")
            return WITNESS

        with patch("find_workflow.git_adapter.capture_repository_root", return_value=str(root)), \
                patch("find_workflow.take_picture", side_effect=pictures_with_capture_recovery):
            outcome = find_workflow.run_find(
                root,
                read_input=lambda prompt: next(answers),
                write_output=lambda message: None,
            )

    assert outcome.status == 0
    assert outcome.result.baseline is BASELINE
    assert outcome.result.witness is WITNESS
    assert outcome.result.capture_missing is False
    assert picture_calls == 3


def test_post_report_navigation_inspects_both_lists_then_confirms_exit():
    import find_workflow

    run_answers = iter(["", "y"])
    review_answers = iter(["i", "o", "", ""])
    prompts = []
    messages = []

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
        root = Path(directory)
        with patch("find_workflow.git_adapter.capture_repository_root", return_value=str(root)), \
                patch("find_workflow.take_picture", side_effect=[BASELINE, WITNESS]):
            outcome = find_workflow.run_find(
                root,
                read_input=lambda prompt: next(run_answers),
                write_output=messages.append,
            )

    def review_input(prompt):
        prompts.append(prompt)
        return next(review_answers)

    find_workflow.review_find_result(
        outcome.result,
        read_input=review_input,
        write_output=messages.append,
    )

    assert any("No unchecked superseded claims" in message for message in messages)
    assert any("No claims for files outside" in message for message in messages)
    assert any("Press Enter again to exit" in prompt for prompt in prompts)


test_a_baseline_git_failure_stops_before_waiting_for_input()
test_no_at_end_confirmation_returns_to_waiting_then_yes_takes_one_witness()
test_ctrl_c_while_waiting_can_confirm_the_witness()
test_ctrl_c_during_the_witness_returns_no_partial_result()
test_a_witness_git_failure_can_retry_without_replacing_the_baseline()
test_no_after_a_witness_failure_warns_and_confirms_before_exit()
test_missing_capture_at_both_ends_still_reconciles_observed_changes()
test_capture_present_at_baseline_but_missing_at_witness_produces_no_result()
test_missing_capture_can_reappear_on_a_witness_retry()
test_post_report_navigation_inspects_both_lists_then_confirms_exit()
print("test passed")
