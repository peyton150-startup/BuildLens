# Phase 7 Tracked UNSTAGED Capture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one tested Git-adapter operation that captures tracked UNSTAGED unified-diff text without changing the CLI.

**Architecture:** A new `git_adapter.py` owns the first Git subprocess boundary. It receives a repository `Path`, runs one fixed read-only Git command, validates the completed status, and returns stdout as a plain string for the existing summarizer.

**Tech Stack:** Python standard library (`pathlib`, `subprocess`, `unittest.mock`), Git CLI, existing assertion-based test scripts.

**Spec:** `docs/superpowers/specs/2026-09-02-phase-7-git-boundary-design.md`

## Global Constraints

- Keep the existing flat module layout.
- Invoke Git with an argument list and `shell=False`.
- Use the supplied repository as the child process's `cwd`.
- Capture stdout and stderr as text with a ten-second timeout.
- Accept only status 0 for the tracked UNSTAGED command in this slice.
- Return stdout as `str`; do not return `CompletedProcess` across the adapter boundary.
- Keep `summarize.py`, `classify.py`, and `cli.py` unchanged.
- Do not add STAGED capture, untracked discovery, `/dev/null` capture, full failure normalization, malformed-output validation, or CLI integration in this slice.
- After automated tests pass, stop for learner trace, explanation, and transfer before committing.

## File map

- Create `git_adapter.py`: own the fixed tracked-UNSTAGED Git subprocess call and status interpretation.
- Create `test_git_adapter.py`: control `subprocess.run`, verify the call contract, and test accepted/rejected completed statuses.
- Modify `CURRENT_STATE.md` after the learner gate: record exact product state and next step.
- Modify `learning/LEARNING_LEDGER.md` after each formal attempt: preserve prompts and verbatim answers.

---

### Task 1: Capture tracked UNSTAGED diff text

**Files:**
- Create: `git_adapter.py`
- Create: `test_git_adapter.py`
- Modify after learner gate: `CURRENT_STATE.md`
- Modify after learner gate: `learning/LEARNING_LEDGER.md`

**Interfaces:**
- Consumes: `repository: pathlib.Path`
- Produces: `GitCaptureError`; `capture_unstaged_diff(repository: Path) -> str`

- [ ] **Step 1: State the required pre-patch learning block**

State:

```text
Current phase             Phase 7 — Git as the first external boundary
Learning objective        trace Python parent → controlled subprocess result → stdout string
Behavior being added      capture tracked UNSTAGED Git diff text
Conceptual change         first production subprocess boundary
Explicitly out of scope   STAGED, untracked, CLI integration, launch/timeout normalization, malformed output
Expected patch size       two new small files
Knowledge gate afterward  trace, explain, and transfer the boundary before commit
```

- [ ] **Step 2: Ask the learner to predict the controlled call**

Show the expected argument list and keyword arguments without showing the function body. Require the learner to identify:

```text
executable        git
Git arguments     diff --no-ext-diff --no-color --
child cwd         repository
captured values   stdout and stderr strings
timeout           10 seconds
process value     CompletedProcess
adapter value     stdout string
```

Record the exact answer before continuing. If any syntax is unreadable, descend to that one syntax form.

- [ ] **Step 3: Write the failing controlled-subprocess tests**

Create `test_git_adapter.py`:

```python
"""Tests for git_adapter.py.

Run it with:

    python test_git_adapter.py
"""

import subprocess
from pathlib import Path
from unittest.mock import patch

from git_adapter import GitCaptureError, capture_unstaged_diff


REPOSITORY = Path("C:/projects/example")
UNSTAGED_DIFF = (
    "diff --git a/app.py b/app.py\n"
    "index 1111111..2222222 100644\n"
    "--- a/app.py\n"
    "+++ b/app.py\n"
    "@@ -1 +1 @@\n"
    "-old\n"
    "+new\n"
)


def completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=["git", "diff"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_capture_unstaged_diff_runs_expected_command_and_returns_stdout():
    prepared = completed(stdout=UNSTAGED_DIFF)

    with patch("git_adapter.subprocess.run", return_value=prepared) as fake_run:
        result = capture_unstaged_diff(REPOSITORY)

    assert result == UNSTAGED_DIFF
    fake_run.assert_called_once_with(
        ["git", "diff", "--no-ext-diff", "--no-color", "--"],
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
    )


def test_capture_unstaged_diff_rejects_unexpected_status():
    prepared = completed(returncode=2, stderr="fatal: failed")

    with patch("git_adapter.subprocess.run", return_value=prepared):
        try:
            capture_unstaged_diff(REPOSITORY)
        except GitCaptureError as error:
            assert str(error) == (
                "UNSTAGED tracked: Git failed with status 2: fatal: failed"
            )
        else:
            raise AssertionError("capture_unstaged_diff did not reject status 2")


test_capture_unstaged_diff_runs_expected_command_and_returns_stdout()
test_capture_unstaged_diff_rejects_unexpected_status()
print("test passed")
```

- [ ] **Step 4: Run the focused test and verify RED**

Run:

```text
python test_git_adapter.py
```

Expected: import failure because `git_adapter.py` does not exist.

Record the exact failure. Do not create implementation before observing RED.

- [ ] **Step 5: Implement the minimum adapter behavior**

Create `git_adapter.py`:

```python
"""Capture validated Git diff text without leaking Git into the core."""

import subprocess
from pathlib import Path


class GitCaptureError(RuntimeError):
    """Report that one required Git snapshot component could not be captured."""


def capture_unstaged_diff(repository: Path) -> str:
    """Return tracked working-tree diff text for repository."""
    process_result = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--no-color", "--"],
        cwd=repository,
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
    )

    if process_result.returncode != 0:
        detail = process_result.stderr.strip()
        message = (
            "UNSTAGED tracked: Git failed with status "
            + str(process_result.returncode)
        )
        if detail:
            message = message + ": " + detail
        raise GitCaptureError(message)

    return process_result.stdout
```

- [ ] **Step 6: Run the focused test and verify GREEN**

Run:

```text
python test_git_adapter.py
```

Expected: `test passed`.

- [ ] **Step 7: Run all regression suites**

Run:

```text
python test_classify.py
python test_summarize.py
python test_session.py
python test_cli.py
python test_git_adapter.py
```

Expected: every script prints `test passed`.

- [ ] **Step 8: Stop for the required learner trace**

Do not commit or begin another patch merely because tests are green. Ask the learner to trace:

```text
repository Path
→ subprocess argument list and child cwd
→ controlled CompletedProcess
→ returncode branch
→ stdout string
→ capture_unstaged_diff return value
```

Require an explanation of why Git knowledge stays in `git_adapter.py` and why `summarize.py` remains unchanged.

- [ ] **Step 9: Require one transfer variant**

Use a non-Git parent program that runs a formatter child, receives a completed result, rejects an unexpected status, and returns stdout text. Require the learner to distinguish the subprocess result object from the adapter string.

- [ ] **Step 10: Record evidence and update the current snapshot**

Preserve the exact prompt, verbatim first answer, reasoning, confidence, evaluation, and any remediation in `learning/LEARNING_LEDGER.md`. Update `CURRENT_STATE.md` with exact code, execution path, tests, known/uncertain concepts, and the next patch: launch/timeout/malformed-output normalization.

- [ ] **Step 11: Commit only after every Task 1 gate passes**

Run `git diff --check`, verify only the four intended files changed, then commit:

```text
git add git_adapter.py test_git_adapter.py CURRENT_STATE.md learning/LEARNING_LEDGER.md
git commit -m "feat: capture tracked unstaged git diff"
```

Do not push or begin STAGED capture automatically. Stop and report the commit plus the next learning gate.

## Later separately planned slices

After Task 1 is completed and defended, create fresh approved plans for:

1. executable-launch failure, timeout, and malformed-output normalization;
2. tracked STAGED capture;
3. untracked discovery and `/dev/null` new-file diffs;
4. separately labeled CLI composition;
5. real-Git integration verification and the Phase 7 completion gate.

These are preserved Phase 7 requirements, not part of this implementation plan.

