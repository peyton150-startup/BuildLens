"""Build the find report's lines, without printing them.

Wording lives here rather than inside run_find so a test can state what a
report must say by handing this function a FindResult it built itself, instead
of driving a whole session to reach the sentences.

Every line here reports what the two pictures and the capture file
established, and nothing else: no line attributes a change to anyone, and no
line says a file was left alone. A reader is told what was seen, over which
window, and what the report does not rule out (D7).
"""

from datetime import datetime
from typing import Callable

from find_workflow import FindResult


def _local_time(moment: datetime) -> str:
    """Return a stored aware moment as 12-hour local time."""
    return moment.astimezone().strftime("%I:%M %p %Z")


def format_find_report(
    result: FindResult,
    *,
    format_time: Callable[[datetime], str] = _local_time,
) -> list[str]:
    """Return the report's lines, in the order a reader should see them."""
    lines = [
        "Changes between "
        + format_time(result.baseline.taken_at)
        + " and "
        + format_time(result.witness.taken_at)
        + ":"
    ]

    if not result.scan.changes:
        lines.append("No changes were observed between the two pictures.")

    for change in result.scan.changes:
        line = change.kind.name + " " + change.repository_relative_path
        if change.repository_relative_path in result.coverage.changed_after_witness:
            # D23a: a Write claim that held on re-read but no longer matches
            # the witness. The witness saw one version, the re-read another.
            line += " (changed after the witness)"
        lines.append(line)

    for undetermined in result.scan.undetermined:
        # A finding about the scan's reach, never about the tree: calling an
        # unreadable path DELETED would assert the file is gone.
        if undetermined.unreadable_at_witness:
            when = "unreadable at the witness"
        else:
            when = "unreadable at the baseline"
        lines.append(
            "UNDETERMINED "
            + undetermined.repository_relative_path
            + " ("
            + when
            + ")"
        )

    for skipped in result.capture.skipped:
        # D12/D18b/D20: name the line and the reason. The file it named still
        # gets reported as a change, just without a claim.
        lines.append(
            "capture line " + str(skipped.line_number) + " skipped: " + skipped.reason
        )

    for path in sorted(result.selection.superseded):
        # D8a: claims already in the capture file, never checked, never
        # dropped in silence.
        count = len(result.selection.superseded[path])
        lines.append(
            path
            + " has "
            + str(count)
            + " unchecked superseded claims. Press i to see them."
        )

    if result.selection.outside:
        # D14a: one count line plus the key that shows the paths.
        lines.append(
            str(len(result.selection.outside))
            + " claims name files outside this repository. Press o to see them."
        )

    if result.capture_missing:
        # D16: with no capture file there is no record to read. Never say
        # Claude made no changes; missing evidence is not observed absence.
        lines.append(
            "The capture file was missing, so no Claude reports were checked."
        )

    lines.append(
        "This report covers what the two pictures and the capture file showed. "
        "Other changes are not ruled out."
    )

    return lines
