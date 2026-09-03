"""Assemble one point-in-time snapshot of a repository's changes.

This module runs no Git command itself. It sequences git_adapter's capture
functions and applies BuildLens's policy about the result:

    UNSTAGED  tracked working-tree changes, plus every untracked file's
              content treated as entirely added
    STAGED    tracked staged changes

The two views are counted separately and are never summed. If any component
fails, the whole snapshot fails; no partial result is returned.
"""

from dataclasses import dataclass
from pathlib import Path

import git_adapter
from summarize import DiffSummary, summarize_diff


@dataclass(frozen=True)
class Snapshot:
    repository_root: str
    unstaged: DiffSummary
    staged: DiffSummary


def capture_snapshot(repository: Path) -> Snapshot:
    """Return one snapshot, or raise GitCaptureError without a partial result."""
    repository_root = git_adapter.capture_repository_root(repository)

    unstaged_parts = [git_adapter.capture_unstaged_diff(repository)]
    for path in git_adapter.capture_untracked_paths(repository):
        unstaged_parts.append(git_adapter.capture_new_file_diff(repository, path))

    staged_text = git_adapter.capture_staged_diff(repository)

    return Snapshot(
        repository_root=repository_root,
        unstaged=summarize_diff("".join(unstaged_parts)),
        staged=summarize_diff(staged_text),
    )
