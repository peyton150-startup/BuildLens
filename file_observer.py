"""Read files from disk into observations of what is actually there."""

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
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
    content_hash: str | None
    observed_at: datetime


def observe_file(file_path: str) -> ObservedFile:
    """Return what the file system shows for file_path. Never raises."""
    # Taken once, before the attempt, so every outcome carries the same moment.
    # Aware UTC: one exact instant everywhere; conversion to a local zone is a
    # display concern and happens where a person reads it.
    observed_at = datetime.now(timezone.utc)
    try:
        with open(file_path, "rb") as handle:
            file_bytes = handle.read()
    except FileNotFoundError:
        # A fact about the file: it is not there.
        return ObservedFile(
            file_path=file_path,
            status=ObservationStatus.ABSENT,
            file_bytes=None,
            content_hash=None,
            observed_at=observed_at,
        )
    except OSError:
        # A fact about this process or the device, not about the file.
        # Reporting it as ABSENT would blame the write for our own blindness.
        return ObservedFile(
            file_path=file_path,
            status=ObservationStatus.UNREADABLE,
            file_bytes=None,
            content_hash=None,
            observed_at=observed_at,
        )

    return ObservedFile(
        file_path=file_path,
        status=ObservationStatus.READ,
        file_bytes=file_bytes,
        # A fingerprint of these exact bytes. Equal digests mean equal bytes —
        # not the same author, not permission, not the same meaning.
        content_hash=hashlib.sha256(file_bytes).hexdigest(),
        observed_at=observed_at,
    )
