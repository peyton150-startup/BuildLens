"""Run one Claude hook payload through the whole observation boundary.

This module does no work of its own. It sequences the four steps and holds the
policy about what happens between them:

    payload -> claude_adapter   what Claude claimed
            -> git_adapter      which repository the file belongs to (a label only)
            -> file_observer    what the file actually holds
            -> compare          what the observation establishes about the claim
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import claude_adapter
import compare
import file_observer
import git_adapter
from claude_adapter import ClaimedEdit
from git_adapter import BaseVersion, BaseVersionStatus
from compare import ComparisonVerdict
from file_observer import ObservedFile


class Provenance(Enum):
    """Which change stream one version came from."""

    CLAUDE = "claude"
    # Not produced yet: the learner's own edits get their own worktree in a later
    # phase, and every version will then say which stream it belongs to.
    HUMAN = "human"


@dataclass(frozen=True)
class CompleteCompare:
    """Hold one claim, what was observed of its file, and the resulting verdict.

    All three exist together only here. Anything left out is gone when the call
    returns, since nothing in BuildLens persists yet.
    """

    claim: ClaimedEdit
    observed: ObservedFile
    verdict: ComparisonVerdict
    provenance: Provenance
    base_version: BaseVersion


def _repository_root_for(file_path: str) -> str | None:
    """Return the root of the repository holding file_path, or None.

    Git is asked from the file's PARENT DIRECTORY, because a child process
    starts inside a directory and a file path is not one.

    The root only labels the observation, so failing to get one must not cost
    the claim its verdict: a folder that no longer exists is a fact about that
    one file, not about BuildLens's own code.
    """
    try:
        return git_adapter.capture_repository_root(Path(file_path).parent)
    except git_adapter.GitCaptureError:
        # Git ran and said no: the file is in no repository.
        return None
    except OSError:
        # Git never started, e.g. the directory is gone.
        return None


def _base_version_for(
    repository_root: str | None, relative_path: str | None
) -> BaseVersion:
    """Return the base version for one file, or why it could not be read.

    A missing base version never costs the claim its verdict: like the
    repository-relative path, it describes context rather than the comparison.
    """
    if repository_root is None or relative_path is None:
        # Nothing to ask: Git is not consulted at all for a file that belongs to
        # no repository.
        return BaseVersion(
            BaseVersionStatus.UNAVAILABLE,
            None,
            None,
            detail="the file is in no repository",
        )

    try:
        return git_adapter.capture_base_version(Path(repository_root), relative_path)
    except git_adapter.GitCaptureError as error:
        return BaseVersion(BaseVersionStatus.UNAVAILABLE, None, None, detail=str(error))
    except OSError as error:
        return BaseVersion(BaseVersionStatus.UNAVAILABLE, None, None, detail=str(error))


def start_flow(payload: object) -> CompleteCompare | None:
    """Return the complete comparison for one payload, or None when there is none.

    None means the payload named no file to observe — a Bash command — which the
    adapter already reports by returning None rather than raising.
    """
    claim = claude_adapter.parse_post_tool_use(payload)
    if claim is None:
        return None

    repository_root = _repository_root_for(claim.file_path)
    observed = file_observer.observe_file(
        claim.file_path,
        repository_root=repository_root,
    )

    return CompleteCompare(
        claim=claim,
        observed=observed,
        verdict=compare.compare_tool_name(claim, observed),
        base_version=_base_version_for(
            repository_root, observed.repository_relative_path
        ),
        # A PostToolUse payload is a report of a tool call Claude made, so every
        # record this function builds belongs to the Claude stream.
        provenance=Provenance.CLAUDE,
    )
