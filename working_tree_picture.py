"""Take one picture of a repository's working tree.

This module runs no Git command and reads no file itself. It sequences
git_adapter (which paths to look at) and file_observer (what the disk holds at
each one) into a reconcile.Picture:

    tracked, or untracked and not ignored   READ         -> hashes[path]
                                            UNREADABLE   -> unreadable
                                            ABSENT       -> in neither
    ignored                                 never listed, so never looked at

The picture is of the WORKING TREE: what is on disk, not what Git has committed.
Git still lists a tracked file after it is deleted from disk, so leaving an
ABSENT path out is what lets reconcile report DELETED against a baseline.

A picture is NOT atomic. taken_at is captured once, before anything is asked or
read, and the reads that follow take real time; a file changed while they run
may be seen before or after its change.

If any Git call fails, the whole picture fails. A picture silently missing paths
would read, to reconcile, as every one of those paths having been deleted.
"""

from datetime import datetime, timezone
from pathlib import Path

import file_observer
import git_adapter
from file_observer import ObservationStatus
from reconcile import Picture


def take_picture(repository: Path) -> Picture:
    """Return one picture of the working tree that holds repository.

    repository may be any folder inside the working tree. Git lists paths
    relative to the folder it runs in, so a listing from notes/ would say
    "plan.md" where a listing from the root says "notes/plan.md", and the two
    pictures would never match. The root is resolved first and every listing runs
    there.
    """
    taken_at = datetime.now(timezone.utc)

    root = Path(git_adapter.capture_repository_root(repository))
    paths = git_adapter.capture_tracked_paths(root) + git_adapter.capture_untracked_paths(root)

    hashes = {}
    unreadable = set()

    for relative_path in paths:
        observed = file_observer.observe_file(
            str(root / relative_path),
            repository_root=str(root),
        )

        if observed.status is ObservationStatus.READ:
            hashes[relative_path] = observed.content_hash
        elif observed.status is ObservationStatus.UNREADABLE:
            unreadable.add(relative_path)
        elif observed.status is ObservationStatus.ABSENT:
            # Listed by Git, gone from disk: the working tree does not hold it.
            continue
        else:
            # Silently dropping a status this code has never heard of would make
            # reconcile report the path DELETED. Refuse instead.
            raise ValueError(
                "unexpected observation status for "
                + relative_path
                + ": "
                + str(observed.status)
            )

    return Picture(taken_at=taken_at, hashes=hashes, unreadable=frozenset(unreadable))
