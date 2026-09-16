"""Tests for whole_file_coverage.py.

Run it with:

    python tests/test_whole_file_coverage.py

These write real files: the step re-reads each file a Write claim names (D23),
so a stand-in for the disk would prove nothing about that read.
"""

import sys
from pathlib import Path

# Put the repository root first on the import search path, so the product
# modules it holds import by bare name when this file runs as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import hashlib
import tempfile
from datetime import datetime, timezone
from types import MappingProxyType

import whole_file_coverage
from capture_reader import CapturedClaim
from claim_selection import select_claims
from claude_adapter import ClaimedEdit
from reconcile import Picture

WITNESS_TIME = datetime(2026, 9, 16, 10, 30, tzinfo=timezone.utc)


def temporary_directory():
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def write_claim(line_number: int, file_path: Path, content: str) -> CapturedClaim:
    claim = ClaimedEdit(
        file_path=str(file_path),
        session_id="session-1",
        tool_name="Write",
        details=MappingProxyType({"content": content}),
    )
    return CapturedClaim(line_number, claim)


def edit_claim(line_number: int, file_path: Path, old: str, new: str) -> CapturedClaim:
    claim = ClaimedEdit(
        file_path=str(file_path),
        session_id="session-1",
        tool_name="Edit",
        details=MappingProxyType({"old_string": old, "new_string": new}),
    )
    return CapturedClaim(line_number, claim)


def witness_of(root: str, *relative_paths: str) -> Picture:
    """Picture the named files exactly as they are on disk right now."""
    hashes = {
        relative: hashlib.sha256((Path(root) / relative).read_bytes()).hexdigest()
        for relative in relative_paths
    }
    return Picture(taken_at=WITNESS_TIME, hashes=hashes)


def coverage(root: str, claims: list[CapturedClaim], witness: Picture):
    return whole_file_coverage.whole_file_coverage(select_claims(claims, root), witness, root)


def held_paths(root: str, claims: list[CapturedClaim], *pictured: str) -> set[str]:
    """Judge claims against a witness taken of the files as they are now."""
    return coverage(root, claims, witness_of(root, *pictured)).held


def test_a_latest_write_that_holds_covers_its_path():
    with temporary_directory() as root:
        path = Path(root) / "a.py"
        path.write_bytes(b"x = 1\n")

        assert held_paths(root, [write_claim(3, path, "x = 1\n")], "a.py") == {"a.py"}


def test_a_latest_write_that_does_not_hold_covers_nothing():
    with temporary_directory() as root:
        path = Path(root) / "c.py"
        path.write_bytes(b"x = 1\nappended()\n")

        assert held_paths(root, [write_claim(3, path, "x = 1\n")], "c.py") == set()


def test_an_edit_never_covers_its_path_even_when_it_holds():
    with temporary_directory() as root:
        path = Path(root) / "b.py"
        path.write_bytes(b"x = 2\n")

        assert held_paths(root, [edit_claim(3, path, "x = 1", "x = 2")], "b.py") == set()


def test_a_write_that_holds_only_after_normalizing_line_endings_covers_nothing():
    with temporary_directory() as root:
        path = Path(root) / "d.py"
        path.write_bytes(b"x = 1\r\n")

        assert held_paths(root, [write_claim(3, path, "x = 1\n")], "d.py") == set()


def test_only_the_latest_claim_decides_even_if_an_earlier_write_held():
    with temporary_directory() as root:
        path = Path(root) / "e.py"
        path.write_bytes(b"version one\n")

        claims = [
            write_claim(41, path, "version one\n"),
            write_claim(45, path, "version two\n"),
        ]

        assert held_paths(root, claims, "e.py") == set()


def test_a_write_that_holds_now_but_differs_from_the_witness_is_not_held():
    """The file changed after the witness picture: judge it, but do not skip it (D23a)."""
    with temporary_directory() as root:
        path = Path(root) / "cli.py"
        path.write_bytes(b"x = 1\nappended()\n")
        witness = witness_of(root, "cli.py")
        path.write_bytes(b"x = 1\n")

        result = coverage(root, [write_claim(55, path, "x = 1\n")], witness)

    assert result.held == set()
    assert result.changed_after_witness == {"cli.py"}


def test_a_write_the_witness_could_not_read_is_not_held():
    with temporary_directory() as root:
        path = Path(root) / "g.py"
        path.write_bytes(b"x = 1\n")
        witness = Picture(taken_at=WITNESS_TIME, hashes={}, unreadable=frozenset({"g.py"}))

        result = coverage(root, [write_claim(7, path, "x = 1\n")], witness)

    assert result.held == set()
    # Not "changed after the witness": the witness saw no bytes, so there is no
    # evidence it changed. reconcile reports the path as undetermined instead.
    assert result.changed_after_witness == set()


test_a_latest_write_that_holds_covers_its_path()
test_a_latest_write_that_does_not_hold_covers_nothing()
test_an_edit_never_covers_its_path_even_when_it_holds()
test_a_write_that_holds_only_after_normalizing_line_endings_covers_nothing()
test_only_the_latest_claim_decides_even_if_an_earlier_write_held()
test_a_write_that_holds_now_but_differs_from_the_witness_is_not_held()
test_a_write_the_witness_could_not_read_is_not_held()
print("test passed")
