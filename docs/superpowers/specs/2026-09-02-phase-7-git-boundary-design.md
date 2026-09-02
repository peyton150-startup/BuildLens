# Phase 7 Git Boundary Design

Date: 2026-09-02

## Purpose

Phase 7 replaces manual diff-file input with a read-only Git boundary while leaving the existing
diff classifier and summarizer unchanged. It is a manually triggered repository snapshot, not live
monitoring.

The command is:

```text
buildlens analyze
```

It inspects the repository containing the process's current working directory.

## User-visible behavior

A successful snapshot prints two separately labeled summaries:

```text
UNSTAGED
Files changed: ...
Lines added: ...
Lines removed: ...

STAGED
Files changed: ...
Lines added: ...
Lines removed: ...
```

The sections are not summed. They describe repository states, not edit chronology. A clean
repository prints both sections with zero counts and returns status 0.

The UNSTAGED section includes tracked working-tree changes and untracked text files. A newly created
empty file appears as one changed file with zero added and zero removed lines.

## Architecture and boundaries

```text
CLI
→ resolve Path.cwd()
→ ask Git adapter for validated capture text
→ pass text to existing summarize_diff()
→ format separately labeled UNSTAGED and STAGED summaries
```

Responsibilities remain separate:

- `cli.py` owns command parsing, orchestration, user-facing output, and process exit status.
- `git_adapter.py` owns Git arguments, child-process execution, command-specific return-code
  interpretation, path handling, and capture validation.
- `summarize.py` and `classify.py` continue to understand unified-diff text, not Git processes.

Each adapter capture returns validated unified-diff text as a plain string. Return codes, stderr,
and path evidence remain internal to validation. A structured result is deferred until a concrete
downstream consumer needs that metadata.

## Git capture behavior

Git commands use argument lists without a shell, run with the target repository as their child
working directory, capture stdout and stderr as text, and have a ten-second timeout.

Capture proceeds in later small slices:

1. tracked UNSTAGED diff;
2. tracked STAGED diff;
3. untracked-path discovery and per-file new-file diffs;
4. CLI composition of the two labeled summaries.

Untracked files are discovered without changing the index. Each discovered path is compared from
`/dev/null`, meaning “did not exist before,” to the current file. Git therefore emits real new-file
diff metadata even for an empty file. `git diff --no-index` status 1 is accepted as valid difference
data for this operation.

Index-mutating alternatives, synthetic Git-shaped diff text, and an existing-empty-file baseline
are rejected. The first would alter observed state; the second would manufacture evidence; the
third cannot distinguish no file from a newly created empty file.

## Error and data-validity contract

Process success and data validity are separate:

```text
PROCESS CONTRACT
Did the child start, finish within the timeout, and return a status accepted for this Git command?

        ↓

DATA CONTRACT
Did the command produce the required usable capture output?
```

Failure to launch Git, timeout, a genuine Git error status, or malformed required output invalidates
the whole snapshot. BuildLens prints no partial summary. The stderr diagnostic identifies the failed
snapshot component, retains useful Git diagnostic information, and tells the learner to rerun
`buildlens analyze`. The CLI returns status 1.

## First implementation slice

The first product patch adds only `git_adapter.py` with one tracked-UNSTAGED capture operation and
focused tests. It does not change `cli.py` and is not yet user reachable.

```text
repository path
→ tracked-UNSTAGED capture
→ child git diff
→ accept the command's normal status 0
→ return stdout text
```

The first slice must reject an unexpected nonzero result rather than returning its stdout as valid
capture data. Normalizing executable-launch failure, timeout, and malformed output is the next
single-purpose patch before CLI integration.

## Testing strategy

The first slice uses controlled subprocess tests. The test temporarily substitutes a stand-in for
`subprocess.run`, records the invocation, and returns prepared process results. Tests verify:

- the exact argument-list invocation;
- the repository used as the child working directory;
- captured text mode;
- the ten-second timeout;
- returned stdout for accepted status 0;
- rejection of an unexpected nonzero status.

This is deterministic and does not mutate a real repository. Its accepted downside is that it does
not prove actual Git integration. A small real-Git integration test is deferred until the staged,
unstaged, and untracked capture paths have been assembled.

Later tests cover executable-not-found, timeout, accepted no-index status 1, genuine command error,
malformed output, empty untracked files, clean repositories, whole-snapshot rejection, and labeled
CLI output.

## Explicitly deferred

- live file watching or automatic monitoring;
- filter syntax;
- retries and configurable timeout policy;
- logging infrastructure and recovery state;
- concurrency or reconciliation;
- Claude hooks or Agentic-AI architecture;
- a structured capture result without a downstream consumer requirement.

