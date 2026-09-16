"""Focused CLI routing test for the interactive find command.

Run it with:

    python tests/test_find_cli.py

This is separate from test_cli.py so the find route can be developed without
coupling its RED/GREEN cycle to that script's external time-zone-data fixture.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unittest.mock import patch

from cli import main
from find_workflow import FindOutcome


def test_find_routes_to_the_interactive_workflow():
    with patch("find_workflow.run_find", return_value=FindOutcome(status=1, result=None)):
        status = main(["cli.py", "find"])

    assert status == 1


test_find_routes_to_the_interactive_workflow()
print("test passed")
