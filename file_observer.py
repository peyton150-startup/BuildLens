"""Read files from disk into observations of what is actually there."""

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path


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
    repository_relative_path: str | None


def _relative_to_root(file_path: str, repository_root: str | None) -> str | None:
    """Return file_path relative to repository_root, in Git's forward-slash style.

    None when no root was given or the file lies outside it. pathlib compares
    path parts, not characters, so a backslash hook path matches a forward-slash
    Git root — the case a plain startswith check gets wrong.
    """
    if repository_root is None:
        return None
    try:
        return Path(file_path).relative_to(Path(repository_root)).as_posix()
    except ValueError:
        return None


def observe_file(file_path: str, repository_root: str | None = None) -> ObservedFile:
    """Return what the file system shows for file_path. Never raises.

    The caller supplies repository_root; this module does not ask Git. Reading
    the file never uses the root — it only labels the path.
    """
    # Taken once, before the attempt, so every outcome carries the same moment.
    # Aware UTC: one exact instant everywhere; conversion to a local zone is a
    # display concern and happens where a person reads it.
    observed_at = datetime.now(timezone.utc)
    # Status and path are independent facts: an ABSENT file still has a known path.
    repository_relative_path = _relative_to_root(file_path, repository_root)
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
            repository_relative_path=repository_relative_path,
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
            repository_relative_path=repository_relative_path,
        )

    return ObservedFile(
        file_path=file_path,
        status=ObservationStatus.READ,
        file_bytes=file_bytes,
        # A fingerprint of these exact bytes. Equal digests mean equal bytes —
        # not the same author, not permission, not the same meaning.
        content_hash=hashlib.sha256(file_bytes).hexdigest(),
        observed_at=observed_at,
        repository_relative_path=repository_relative_path,
    )
