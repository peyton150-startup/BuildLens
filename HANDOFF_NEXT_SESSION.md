# BuildLens — Next Session Handoff

Updated 2026-09-13 for the approved Core v0.1 scope. Follow `AGENTS.md` / `CLAUDE.md` and their required reading order. `IMPLEMENTATION_PLAN.md` controls scope; `CURRENT_STATE.md` controls current facts; `learning/LEARNING_LEDGER.md` preserves exact learner evidence.

## Resume here

**Phase 8 is CLOSED** (2026-09-13): composite gate EV-P8-PHASE-GATE-460 passed; see "GATE PASSED; PHASE 8 CLOSED" at the end of the ledger. Both parsers and tool-call IDs already exist; do not rebuild them.

**Next: the major cumulative review is DUE** (counter 2/2) before any significant Phase 9 work, together with the Phase 8 -> 9 architecture reset. Build it from the ledger's RETRIEVAL DUE list and `CURRENT_STATE.md`'s uncertain items; reset only the major counter after it passes. Foundation remains 1/3.

## Remaining release work

1. Run the due major cumulative review (Phase 8 gates are done).
2. Specify and build a single-process baseline -> edits -> witness -> report workflow, using existing picture/reconciliation machinery. Address the claimed-path suppression limitation or explicitly expose a narrower coverage contract. Let the learner propose the detailed design.
3. Only if the observation workflow is complete and time remains, add one source-grounded tracing archetype, fresh transfer, and human-reviewed reasoning. Manual facilitator-run gates are the fallback; preserve exact evidence in the ledger.
4. Reserve the final day for setup, tests/defects, accurate docs, a demo, static architecture view, and manual defense.

Do not build storage, automatic SessionStart/Stop continuity, API/UI, an editor, merge/stale-save machinery, additional provider adapters, automated mastery, or an interview engine. Preserve future phase numbers and safety contracts.

Verification limitation: the scope-review run passed 12 scripts; the CLI script stopped on missing `tzdata`. A fresh-environment setup/test procedure remains release work. No product changes or learning-gate completion occurred during the scope documentation update.

The [previous handoff](docs/history/HANDOFF_NEXT_SESSION-before-core-v0.1-2026-09-13.md) is archived historical context, not a restart instruction.
