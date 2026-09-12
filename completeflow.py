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


def start_flow(payload: object) -> CompleteCompare | None:
    """Return the complete comparison for one payload, or None when there is none.

    None means the payload named no file to observe — a Bash command — which the
    adapter already reports by returning None rather than raising.
    """
    claim = claude_adapter.parse_post_tool_use(payload)
    if claim is None:
        return None

    observed = file_observer.observe_file(
        claim.file_path,
        repository_root=_repository_root_for(claim.file_path),
    )

    return CompleteCompare(
        claim=claim,
        observed=observed,
        verdict=compare.compare_tool_name(claim, observed),
        # A PostToolUse payload is a report of a tool call Claude made, so every
        # record this function builds belongs to the Claude stream.
        provenance=Provenance.CLAUDE,
    )
