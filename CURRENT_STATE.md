# BuildLens — Current State

## Lifecycle

**Current phase:** Phase 0 — Specification Before Code

## What exists

Planning and learning documents only.

There is intentionally no application implementation yet.

## What does NOT exist yet

- Python BuildLens domain code
- parser
- state store
- CLI
- Git adapter
- Claude hooks
- learning engine
- SQLite
- FastAPI
- React UI

Do not create these until their phase.

## Current execution path

None yet.

The first implementation target will be a tiny deterministic transformation whose complete execution can be traced by hand.

## What I should know cold before Phase 1

- variable assignment vs mutation at a basic level;
- function argument → parameter → local state → return;
- sequential / conditional execution;
- how to predict output without running Python;
- how to describe an input/output contract in plain English.

## First gate

A fresh CMU-style small Python trace.

Required sequence:

```text
predict by hand
→ commit answer
→ run
→ explain mismatch if any
→ modify one meaningful condition
→ predict again
```

The generated problem should use the same deep skill as the academic examples but not reproduce them.

## Reference-project use

Not yet.

Argos, Datum, and Trellis are deliberately deferred until the matching Python/design concepts have been introduced.

## Weak concepts

None recorded yet.

## Files I should be able to teach

Planning only. No code file yet.

## Weekly architecture reset

Not started because there is no architecture yet.

The first reset becomes due after the first week of active implementation.

## Next implementation milestone

After the Phase 0 gate passes:

Create the smallest pure-function BuildLens behavior from Phase 1.

## End-game relationship

This phase establishes the rule that behavior is understood before architecture is generated.


## Future non-negotiable requirement

When the UI/editing phase is eventually reached, BuildLens must support live manual editing alongside Claude without silent overwrite.

This is **not Phase 0 work**.

The eventual design is documented in `docs/COLLABORATIVE_EDITING.md` and uses:
- separate human/Claude worktrees;
- content-version hashes;
- three-way reconciliation;
- explicit conflict state;
- atomic publication of manual saves.

Do not scaffold this architecture early.


The later live-editor requirement has now been tightened further:

```text
Claude diff stays visible
+ human diff stays visible separately
+ overlapping same-line/hunk edits force CONFLICT
+ no blind override
+ clean merges use a current Git merge base
+ all promotion is version-checked and recoverable
```

This remains later-phase work; do not implement it during Phase 0.


## Supporting curriculum now available

These documents now guide later learning without changing the current Phase 0 scope:

```text
docs/CURRICULUM.md
docs/CODE_READING_DEBUGGING_PLAYBOOK.md
docs/DESIGN_REVIEW_RUBRIC.md
learning/LEARNING_LEDGER.md
```

Do not attempt to study them all before beginning. Claude should introduce the relevant sections when the matching project phase arrives.


## Just-in-time learning crosswalk

The implementation plan now contains phase-specific adjacent-learning triggers. This does **not** advance the current phase.

During Phase 0/1, if a Python trace is too complex, reduce it to the smallest syntax unit the learner cannot yet read, record the exact attempt, then rebuild complexity gradually.

Formal exercises must use Evidence Records in `learning/LEARNING_LEDGER.md`.


## Adaptive remediation is active

During the current early phases, wrong answers should trigger a **simpler prerequisite problem**, not another equally complex problem.

Use the remediation ladder in `learning/LEARNING_RULES.md`:

```text
R0 syntax
→ R1 operation
→ R2 sequential state
→ R3 one branch
→ R4 one function
→ R5 function + branch
→ R6 composition
```

If the learner says a line of Python is unreadable, stop the larger trace and remediate that syntax first.

Every attempt remains verbatim in `learning/LEARNING_LEDGER.md` and is linked into a remediation chain.

This does not advance the project phase.
