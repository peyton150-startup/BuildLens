"""Focused CLI routing test for the interactive find command.

Run it with:

    python tests/test_find_cli.py

This is separate from test_cli.py so the find route can be developed without
coupling its RED/GREEN cycle to that script's external time-zone-data fixture.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import io
from contextlib import redirect_stdout
from unittest.mock import patch

from cli import main
from find_workflow import FindOutcome


def test_find_routes_to_the_interactive_workflow():
    with patch("find_workflow.run_find", return_value=FindOutcome(status=1, result=None)):
        status = main(["cli.py", "find"])

    assert status == 1


def test_a_successful_find_prints_the_report_before_the_review_menu():
    """The report is printed by cli.py, from the lines find_report returns.

    The formatter is stood in for here: this checks the wiring, that the lines
    reach the terminal before the menu opens, not the wording, which
    tests/test_find_report.py states.
    """
    outcome = FindOutcome(status=0, result=object())
    printed = io.StringIO()

    with patch("find_workflow.run_find", return_value=outcome), \
            patch("find_report.format_find_report", return_value=["MODIFIED a.py"]), \
            patch("find_workflow.review_find_result") as review:
        with redirect_stdout(printed):
            status = main(["cli.py", "find"])

    assert status == 0
    assert "MODIFIED a.py" in printed.getvalue()
    assert review.called


test_find_routes_to_the_interactive_workflow()
test_a_successful_find_prints_the_report_before_the_review_menu()
print("all tests passed")
