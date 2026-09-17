"""Build the find report's lines, without printing them.

Wording lives here rather than inside run_find so a test can state what a
report must say by handing this function a FindResult it built itself, instead
of driving a whole session to reach the sentences.
"""

from find_workflow import FindResult


def format_find_report(result: FindResult) -> list[str]:
    """Return the report's lines, in the order a reader should see them."""
    lines = [
        change.kind.name + " " + change.repository_relative_path
        for change in result.scan.changes
    ]

    if result.capture_missing:
        # Never "Claude made no changes": with no capture file there is no
        # record to read, so nothing about Claude's edits was established.
        lines.append(
            "The capture file was missing, so no Claude reports were checked."
        )

    return lines
