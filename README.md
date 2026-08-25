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

**Phase 0 — Specification Before Code.**

No application code should exist yet.

The first task is to pass the Phase 0 tracing gate and then implement one tiny pure Python transformation.

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
