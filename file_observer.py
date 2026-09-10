"""Read files from disk into observations of what is actually there."""

from dataclasses import dataclass
from enum import Enum


class ObservationStatus(Enum):
    """What the attempt to observe a file established."""

    READ = "read"
    ABSENT = "absent"
    UNREADABLE = "unreadable"


@dataclass(frozen=True)
class ObservedFile:
    """Hold what reading one path established, including finding nothing."""

    file_path: str
    status: ObservationStatus
    file_bytes: bytes | None


def observe_file(file_path: str) -> ObservedFile:
    """Return what the file system shows for file_path. Never raises."""
    try:
        with open(file_path, "rb") as handle:
            file_bytes = handle.read()
    except FileNotFoundError:
        # A fact about the file: it is not there.
        return ObservedFile(
            file_path=file_path,
            status=ObservationStatus.ABSENT,
            file_bytes=None,
        )
    except OSError:
        # A fact about this process or the device, not about the file.
        # Reporting it as ABSENT would blame the write for our own blindness.
        return ObservedFile(
            file_path=file_path,
            status=ObservationStatus.UNREADABLE,
            file_bytes=None,
        )

    return ObservedFile(
        file_path=file_path,
        status=ObservationStatus.READ,
        file_bytes=file_bytes,
    )
