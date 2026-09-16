"""Run the single-process baseline -> wait -> witness find lifecycle.

This module owns interaction and sequencing. Picture capture, claim parsing,
coverage, reconciliation, and final report wording remain in their focused
modules.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import git_adapter
from capture_reader import CaptureRead, count_complete_lines, read_capture
from claim_selection import ClaimSelection, select_claims
from git_adapter import GitCaptureError
from reconcile import Picture, ScanResult, reconcile
from whole_file_coverage import WholeFileCoverage, whole_file_coverage
from working_tree_picture import take_picture


@dataclass(frozen=True)
class FindResult:
    """Hold the two observations and the capture-file window they bound."""

    repository_root: str
    baseline: Picture
    witness: Picture
    capture_position: int
    capture: CaptureRead
    selection: ClaimSelection
    coverage: WholeFileCoverage
    scan: ScanResult
    capture_missing: bool


@dataclass(frozen=True)
class FindOutcome:
    """Hold the process status and a successful result when one exists."""

    status: int
    result: object | None


def _ask_to_retry(
    read_input: Callable[[str], str],
    write_output: Callable[[str], None],
) -> bool:
    """Return True to retry, or False after a confirmed session exit."""
    while True:
        retry = read_input("Try again? (y/n): ").strip().lower()
        if retry == "y":
            return True

        write_output(
            "If you exit, find can no longer report what changed "
            "since you started it."
        )
        write_output(
            "Your files, including Claude's edits, stay exactly as they are."
        )
        confirm_exit = read_input("Exit find? (y/n): ").strip().lower()
        if confirm_exit == "y":
            return False


def run_find(
    repository: Path,
    *,
    read_input: Callable[[str], str] = input,
    write_output: Callable[[str], None] = print,
) -> FindOutcome:
    """Run one in-memory find session."""
    try:
        root = Path(git_adapter.capture_repository_root(repository))
        baseline = take_picture(root)
        capture_path = root / "payload_samples.jsonl"
        capture_existed_at_baseline = capture_path.exists()
        capture_position = count_complete_lines(capture_path)
    except (GitCaptureError, OSError) as error:
        write_output("The baseline picture failed: " + str(error))
        return FindOutcome(status=1, result=None)

    while True:
        try:
            read_input("Press Enter to end the session and get a detailed report: ")
        except KeyboardInterrupt:
            # While idle, Ctrl+C means "I may want to end this session." It is
            # still confirmed because ending loses the in-memory baseline.
            pass
        confirmation = read_input("Are you sure? (y/n): ").strip().lower()
        if confirmation == "y":
            break

    while True:
        try:
            witness = take_picture(root)
        except KeyboardInterrupt:
            write_output("The witness picture was interrupted. No report was produced.")
            return FindOutcome(status=1, result=None)
        except (GitCaptureError, OSError) as error:
            write_output("The witness picture failed: " + str(error))
            if _ask_to_retry(read_input, write_output):
                continue
            return FindOutcome(status=1, result=None)

        capture_missing = not capture_path.exists()
        if capture_missing:
            if capture_existed_at_baseline:
                write_output("The capture file is missing at the witness: " + str(capture_path))
                if _ask_to_retry(read_input, write_output):
                    continue
                return FindOutcome(status=1, result=None)
            capture = CaptureRead(claims=[], skipped=[])
        else:
            try:
                capture = read_capture(capture_path, capture_position)
            except OSError as error:
                write_output("The capture file could not be read: " + str(capture_path))
                write_output(str(error))
                if _ask_to_retry(read_input, write_output):
                    continue
                return FindOutcome(status=1, result=None)
        break

    selection = select_claims(capture.claims, str(root))
    coverage = whole_file_coverage(selection, witness, str(root))
    scan = reconcile(baseline, witness, coverage.held)

    return FindOutcome(
        status=0,
        result=FindResult(
            repository_root=str(root),
            baseline=baseline,
            witness=witness,
            capture_position=capture_position,
            capture=capture,
            selection=selection,
            coverage=coverage,
            scan=scan,
            capture_missing=capture_missing,
        ),
    )


def review_find_result(
    result: FindResult,
    *,
    read_input: Callable[[str], str] = input,
    write_output: Callable[[str], None] = print,
) -> None:
    """Let the user inspect claim lists after the main report, then exit."""
    menu = (
        "(i) see unchecked superseded claims\n"
        "(o) see claims for files outside this repository\n"
        "(Enter) exit: "
    )

    while True:
        choice = read_input(menu).strip().lower()
        if choice == "":
            choice = read_input(
                "Press Enter again to exit, or i/o to inspect claims: "
            ).strip().lower()
            if choice == "":
                return

        if choice == "i":
            if not result.selection.superseded:
                write_output("No unchecked superseded claims.")
                continue
            for path in sorted(result.selection.superseded):
                claims = result.selection.superseded[path]
                write_output(
                    path
                    + " has "
                    + str(len(claims))
                    + " unchecked superseded claims."
                )
                for captured in claims:
                    write_output(
                        "capture line "
                        + str(captured.line_number)
                        + ": "
                        + captured.claim.tool_name
                        + " "
                        + captured.claim.file_path
                    )
            continue

        if choice == "o":
            if not result.selection.outside:
                write_output("No claims for files outside this repository.")
                continue
            for captured in result.selection.outside:
                write_output(
                    "capture line "
                    + str(captured.line_number)
                    + ": "
                    + captured.claim.file_path
                )
