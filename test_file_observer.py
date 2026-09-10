"""Tests for file_observer.py.

Run it with:

    python test_file_observer.py

These write real files to a throwaway directory and read them back. The point
of this module is to observe the file system, so a stand-in would prove nothing
about what the file system actually does.
"""

import importlib
import tempfile
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


def test_observed_file_fields_cannot_be_reassigned():
    file_observer = importlib.import_module("file_observer")

    observed = file_observer.ObservedFile(
        file_path="notes.md",
        status=file_observer.ObservationStatus.ABSENT,
        file_bytes=None,
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
print("test passed")
