# BuildLens

BuildLens is a learning-first control tower for AI-assisted software development.

Its purpose is to stop AI coding speed from outrunning the developer's understanding.

The eventual product will observe Claude Code development, show meaningful changes and execution/state flows, generate source-grounded knowledge gates, track mastery and misconceptions, preserve design decisions, and run architecture/code-defense interviews.

The project itself is intentionally built in the same order those ideas should be learned.

## Start here

1. `IMPLEMENTATION_PLAN.md`
2. `CURRENT_STATE.md`
3. `docs/CURRICULUM.md`
4. `learning/LEARNING_RULES.md`
5. `docs/CODE_READING_DEBUGGING_PLAYBOOK.md`
6. `docs/DESIGN_REVIEW_RUBRIC.md`
7. `learning/LEARNING_LEDGER.md`
8. `docs/LEARNING_SOURCES.md`
9. `docs/REFERENCE_PROJECTS.md`
10. `CLAUDE.md`

## Current status

**Phase 8 — Claude boundary (specification in progress; no Phase 8 product code yet).**

Phase 7's Git-backed CLI vertical slice is complete. Phase 8 is defining how Claude Code hook events enter BuildLens, what information can be trusted, and what must be verified against authoritative repository state. `CURRENT_STATE.md` is authoritative for the exact completed code, retrieval commitments, and next step.

The curriculum uses selected CMU and MIT material as an academic backbone while BuildLens implementation continues to determine when each concept is introduced.

## Core rule

```text
predict
→ sketch
→ implement a small patch
→ trace
→ test
→ teach
→ transfer exercise
→ commit
```

Tests passing are necessary, but not sufficient.

## What you learn while building BuildLens

The implementation and curriculum advance together. Each phase adds only the software needed to make the next ideas concrete.

| Phase | What you implement | Main ideas you learn |
|---|---|---|
| 0 — Specification | Define behavior before writing product code | Read syntax, trace execution, turn requirements into precise examples, and record evidence of understanding |
| 1 — Pure functions | Diff-line classification and small transformations | Assignment, expressions, strings, branches, function calls, local scope, return values, and control-flow order |
| 2 — Representation and tests | Explicit result records and systematic tests | Dataclasses, collection choice, contracts, invariants, boundary/invalid cases, and shallow versus deep immutability |
| 3 — State | In-memory sessions and change history | State versus value, object identity, mutation, aliasing, ownership, snapshots, and legal state transitions |
| 4 — Decomposition | Refactor behavior into focused modules | Cohesion, coupling, imports, dependency direction, code reading, and evidence-driven debugging |
| 5 — Contracts | Explicit interfaces between components | Preconditions, postconditions, abstraction boundaries, type hints versus runtime validation, and representation independence |
| 6 — CLI vertical slice | A complete command-line workflow | Argument parsing, entry points, stdout versus stderr, exit status, user-facing errors, and end-to-end testing |
| 7 — Git boundary | Capture and summarize staged, unstaged, and untracked changes | Parent/child processes, Git's working tree/index/history model, bytes versus text, return codes, timeouts, paths, and all-or-nothing snapshots |
| 8 — Claude boundary | Observe Claude Code through hooks | JSON representation, untrusted input, hashes, provenance, signal versus authority, and why model or hook output is not authoritative application state |
| 9 — Event reliability | Project events into dependable state | Ordering, duplicate delivery, idempotence, optimistic concurrency, retries, partial failure, reconciliation, and the basic agent loop |
| 10 — Learning engine | Generate and evaluate knowledge gates | Authoritative evidence versus generated content, task-level success criteria, representative evaluation sets, and human versus automated evaluation |
| 11 — Persistence | Store sessions, events, evidence, and decisions | Schemas, SQL parameters, indexes, constraints, transactions, commit/rollback, recovery, and embeddings as a representation |
| 12 — Local API | Expose BuildLens through a process/network boundary | HTTP and JSON, client/server contracts, serialization, transport validation versus domain validation, and the retrieval/RAG mental model |
| 13 — Collaborative editing | Reconcile isolated learner and Claude worktrees | Multiple writers, version hashes, stale writes, three-way merge, explicit conflicts, atomic publication, crash recovery, and no-silent-overwrite guarantees |
| 14 — Architecture views | Visualize runtime, data, failure, and decision flows | Quality scenarios, architectural drivers, measurable evidence, tradeoffs, risks, ADRs, and reversal conditions |
| 15 — Oral defense | Explain and defend the completed system | Cumulative line-to-system reasoning, unfamiliar-code review, agentic-AI architecture, guardrails, observability, and conditional design judgment |

Several skills recur at increasing depth throughout the phases: choosing algorithms and data structures for real operations, writing tests as executable contracts, debugging from evidence, reasoning about performance, identifying trust and security boundaries, using logs and runtime state as evidence, and explaining design decisions with honest tradeoffs.

The full curriculum, including promotion tests, academic source mappings, transfer exercises, and the mastery model, lives in `docs/CURRICULUM.md`.

## Practice domains

As BuildLens grows, learning exercises evolve from small CMU/Berkeley-inspired problems into new problems derived from:

- BuildLens itself;
- Argos Control Tower;
- Datum;
- Trellis AI Agent;
- later unfamiliar related systems.

The problems must preserve the underlying idea while changing the surface form.

See `docs/REFERENCE_PROJECTS.md`.


## Live editing

The final BuildLens workspace is intentionally editable.

You will be able to watch Claude's diff, open the same logical source file, and make your own changes.

BuildLens will not implement this as two writers racing on one physical file. Human and Claude edits live in separate managed Git worktrees and are reconciled from a common base. Non-overlapping changes can merge; overlapping changes pause with an explicit conflict instead of silently overwriting either side.

See `docs/COLLABORATIVE_EDITING.md`.


The live editor's core promise is intentionally simple:

> Claude's diff stays visible. Your edits stay separately visible. If both of you change the same line or overlapping merge hunk, BuildLens stops automatic synchronization and makes you reconcile the two versions before anything can be silently replaced.


## Learning depth

BuildLens eventually moves below framework-level explanations.

As the project grows, exercises connect application code to:
- data representation;
- data structures/algorithms;
- processes, memory, files, and networks;
- performance/profiling;
- persistence, concurrency, and distributed failure;
- security/trust;
- runtime evidence/operations;
- architecture and tradeoffs.

These topics are introduced only when the current BuildLens phase gives them a concrete use.


BuildLens uses a just-in-time learning rule: **the implementation itself triggers the curriculum**. New syntax, processes, serialization, persistence, concurrency, filesystem behavior, and architecture concepts are introduced when a real BuildLens feature first needs them, then revisited at deeper levels later.


## Wrong answers trigger adaptive remediation

BuildLens treats incorrect answers as diagnostic evidence, not as a reason to keep increasing pressure.

If a learner misses a problem, the system:

```text
preserves the exact attempt
→ identifies the smallest missing prerequisite
→ gives a simpler one-concept problem
→ rebuilds complexity one step at a time
→ returns to a fresh target-level variant
```

Support is gradually removed after the concept becomes stable.
