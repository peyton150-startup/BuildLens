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

**Phase 3 — State and the State Movie (implementation and knowledge gate complete; transition milestones pending).**

Phase 2 is closed and Phase 4 has not started. The remaining Phase 3 transition work is the `session.py` teach-aloud plus a different-domain aliasing/copying transfer; `CURRENT_STATE.md` is authoritative for the exact completed code, retrieval commitments, and next step.

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
