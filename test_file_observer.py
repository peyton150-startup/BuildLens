"""Tests for file_observer.py.

Run it with:

    python test_file_observer.py

These write real files to a throwaway directory and read them back. The point
of this module is to observe the file system, so a stand-in would prove nothing
about what the file system actually does.
"""

import hashlib
import importlib
import tempfile
from datetime import datetime, timedelta, timezone
from dataclasses import FrozenInstanceError
from pathlib import Path


def temporary_directory():
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def test_existing_file_is_observed_as_read_with_its_bytes():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"hello\n")

        observed = file_observer.observe_file(str(path))

    assert observed.status is file_observer.ObservationStatus.READ
    assert observed.file_bytes == b"hello\n"
    assert observed.file_path == str(path)


def test_empty_file_is_read_not_absent():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "empty.md"
        path.write_bytes(b"")

        observed = file_observer.observe_file(str(path))

    assert observed.status is file_observer.ObservationStatus.READ
    assert observed.file_bytes == b""


def test_missing_file_is_observed_as_absent_and_does_not_raise():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "never_written.md"

        observed = file_observer.observe_file(str(path))

    assert observed.status is file_observer.ObservationStatus.ABSENT
    assert observed.file_bytes is None


def test_unreadable_path_is_observed_as_unreadable_not_absent():
    file_observer = importlib.import_module("file_observer")

    # A directory exists but cannot be read as a file. The distinction under
    # test is that "could not look" must not be reported as "not there".
    with temporary_directory() as directory:
        observed = file_observer.observe_file(directory)

    assert observed.status is file_observer.ObservationStatus.UNREADABLE
    assert observed.file_bytes is None


def test_binary_content_is_observed_without_decoding():
    file_observer = importlib.import_module("file_observer")

    png_header = b"\x89PNG\r\n\x1a\n\xff\xfe"

    with temporary_directory() as directory:
        path = Path(directory) / "image.png"
        path.write_bytes(png_header)

        observed = file_observer.observe_file(str(path))

    assert observed.status is file_observer.ObservationStatus.READ
    assert observed.file_bytes == png_header


def test_read_file_carries_the_sha256_of_its_bytes():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"hello\n")

        observed = file_observer.observe_file(str(path))

    assert observed.content_hash == hashlib.sha256(b"hello\n").hexdigest()


def test_empty_file_carries_the_real_digest_of_zero_bytes():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "empty.md"
        path.write_bytes(b"")

        observed = file_observer.observe_file(str(path))

    assert observed.content_hash is not None
    assert observed.content_hash == hashlib.sha256(b"").hexdigest()


def test_no_bytes_observed_means_no_hash():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        missing = file_observer.observe_file(str(Path(directory) / "gone.md"))
        unreadable = file_observer.observe_file(directory)

    assert missing.content_hash is None
    assert unreadable.content_hash is None


def test_observed_at_is_an_aware_utc_moment_taken_during_the_read():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"hello\n")

        before = datetime.now(timezone.utc)
        observed = file_observer.observe_file(str(path))
        after = datetime.now(timezone.utc)

    assert observed.observed_at.tzinfo is not None
    assert observed.observed_at.utcoffset() == timedelta(0)
    assert before <= observed.observed_at <= after


def test_every_outcome_carries_a_time_even_when_no_bytes_were_seen():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.md"
        path.write_bytes(b"hi")
        read = file_observer.observe_file(str(path))
        absent = file_observer.observe_file(str(Path(directory) / "gone.md"))
        unreadable = file_observer.observe_file(directory)

    for observed in (read, absent, unreadable):
        assert observed.observed_at is not None
        assert observed.observed_at.utcoffset() == timedelta(0)


def test_path_inside_the_root_is_recorded_relative_with_forward_slashes():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "src" / "app.py"
        path.parent.mkdir()
        path.write_bytes(b"x = 1\n")

        # The real mismatch: a backslash file path against a forward-slash root.
        observed = file_observer.observe_file(
            str(path), repository_root=Path(directory).as_posix()
        )

    assert observed.repository_relative_path == "src/app.py"


def test_path_outside_the_root_has_no_repository_relative_path():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as repository, temporary_directory() as elsewhere:
        path = Path(elsewhere) / "notes.txt"
        path.write_bytes(b"hi")

        observed = file_observer.observe_file(str(path), repository_root=repository)

    assert observed.status is file_observer.ObservationStatus.READ
    assert observed.repository_relative_path is None


def test_no_root_given_means_no_repository_relative_path():
    file_observer = importlib.import_module("file_observer")

    with temporary_directory() as directory:
        path = Path(directory) / "notes.txt"
        path.write_bytes(b"hi")

        observed = file_observer.observe_file(str(path))

    assert observed.status is file_observer.ObservationStatus.READ
    assert observed.repository_relative_path is None


def test_an_absent_file_inside_the_root_still_has_its_relative_path():
    file_observer = importlib.import_module("file_observer")

    # Status and path are independent facts: the path is known even when the
    # file is not there.
    with temporary_directory() as directory:
        observed = file_observer.observe_file(
            str(Path(directory) / "gone.md"), repository_root=directory
        )

    assert observed.status is file_observer.ObservationStatus.ABSENT
    assert observed.repository_relative_path == "gone.md"


def test_observed_file_fields_cannot_be_reassigned():
    file_observer = importlib.import_module("file_observer")

    observed = file_observer.ObservedFile(
        file_path="notes.md",
        status=file_observer.ObservationStatus.ABSENT,
        file_bytes=None,
        content_hash=None,
        observed_at=datetime(2026, 9, 11, 17, 16, tzinfo=timezone.utc),
        repository_relative_path=None,
    )

    try:
        observed.file_bytes = b"invented"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("ObservedFile allowed an observation to be rewritten")


test_existing_file_is_observed_as_read_with_its_bytes()
test_empty_file_is_read_not_absent()
test_missing_file_is_observed_as_absent_and_does_not_raise()
test_unreadable_path_is_observed_as_unreadable_not_absent()
test_binary_content_is_observed_without_decoding()
test_observed_file_fields_cannot_be_reassigned()
test_read_file_carries_the_sha256_of_its_bytes()
test_empty_file_carries_the_real_digest_of_zero_bytes()
test_no_bytes_observed_means_no_hash()
test_observed_at_is_an_aware_utc_moment_taken_during_the_read()
test_every_outcome_carries_a_time_even_when_no_bytes_were_seen()
test_path_inside_the_root_is_recorded_relative_with_forward_slashes()
test_path_outside_the_root_has_no_repository_relative_path()
test_no_root_given_means_no_repository_relative_path()
test_an_absent_file_inside_the_root_still_has_its_relative_path()
print("test passed")
