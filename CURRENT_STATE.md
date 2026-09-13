# BuildLens — Current State

Last updated: 2026-09-13 — Core v0.1 scope revision authorized by the user.

This file is the current snapshot. The [prior accumulated state notes](docs/history/CURRENT_STATE-before-core-v0.1-2026-09-13.md) are preserved byte-for-byte for historical context, not current instructions. Exact historical prompts and learner answers remain in `learning/LEARNING_LEDGER.md`; none were changed by this scope revision.

## Phase and active release

**Phase 8 remains OPEN.** Phase 7 is complete. The latest recorded product commits are `c78b1b6` (PreToolUse parser) and `bb92ba5` (optional PostToolUse tool-call ID); `c8bb04e` records the gate in progress.

The active scope at the top of `IMPLEMENTATION_PLAN.md` is authoritative: finish the observation core and a single-process reconciliation workflow, then attempt one tracing archetype only if time permits. Facilitator-run gates are the release fallback. Persistence, API/UI, collaborative editing (including Phase 9 merge primitives), automated mastery, and automated interviews are deferred. Phase numbers are preserved. No phase was closed or counter reset in this documentation session.

## Exact code that exists

| Module | Implemented behavior |
|---|---|
| `classify.py`, `summarize.py` | Classify unified-diff lines and calculate counts |
| `session.py` | Validated in-memory diff-string history; not an integrated hook/session lifecycle |
| `git_adapter.py` | Repository resolution, staged/unstaged/new-file diffs, NUL-separated tracked/untracked paths, HEAD commit/blob context |
| `snapshot.py` | Assemble separate staged/unstaged summaries; no partial summary on capture failure |
| `claude_adapter.py` | Separate `ClaimedEdit`/`ProposedEdit`, PostToolUse/PreToolUse parsing, shared field validation, optional report ID and required proposal ID |
| `file_observer.py` | Read bytes, SHA-256, UTC observation time, repository-relative path; READ/ABSENT/UNREADABLE |
| `compare.py` | Write equality and Edit fragment checks, separate normalized-line-ending verdict, explicit absent/unknown outcomes |
| `completeflow.py` | PostToolUse -> claim -> Git context -> file observation -> comparison and metadata record |
| `reconcile.py` | Compare two pictures for created/modified/deleted and undetermined paths, currently excluding claimed paths |
| `working_tree_picture.py` | Build a picture from real Git path listings and disk reads |
| `cli.py` | `analyze` and `ingest [payload]`; stdin when payload omitted |

PreToolUse capture is configured in machine-local, Git-excluded `.claude/settings.local.json`; this is not a portable product installation. There is no PreToolUse CLI route, reconciliation CLI flow, gate engine, database, API, or editor.

## Execution paths

```text
python cli.py analyze
  -> snapshot -> git_adapter -> summarize -> classify -> separately labeled counts

python cli.py ingest [payload.json] (or stdin)
  -> JSON decoding -> completeflow -> parse_post_tool_use
  -> Git repository context -> observe_file -> compare -> verdict/observation output

parse_pre_tool_use(payload) -> ProposedEdit (or None for supported no-file tool)
  [callable parser; not connected to a decision or persistence system]

take_picture(repository) -> git_adapter + file_observer -> Picture
reconcile(baseline, witness, claimed_paths) -> ScanResult
  [callable machinery; no user-facing lifecycle yet]
```

Separate `ingest` invocations do not share state. Automatic SessionStart/Stop wiring requires persistence, still assigned to future Phase 11. Core v0.1 will hold baseline and witness in one running process; its exact interaction remains to be designed with the learner.

## Known release issues and limits

- `reconcile()` skips a claimed path before checking its witness hash or unreadability. A later shell mutation to that path can disappear from the report. Reproduced in the scope review. Plan version-aware accounting and a regression scenario; if deferred, explicitly narrow and surface the coverage limitation. Do not report complete coverage without resolving it.
- Pictures are sequential, not atomic. Changes restored between pictures are invisible. Untracked ignored paths are excluded; tracked files remain in scope even if an ignore pattern matches them.
- Write comparison concerns observed content; Edit comparison checks fragments, not exact patch execution. Neither proves authorship. CLAUDE provenance labels the report stream.
- `analyze` produces counts, not a diff browser. Base-version metadata is available in records but is not all printed by `ingest`.
- Reproducible Python/Git setup and applicable failure handling are release work; no new runtime infrastructure is needed to document or test the supported boundary.

## Verification evidence

The prior learning sessions recorded thirteen test scripts green. The separate 2026-09-13 scope-review run passed 12 scripts; `test_cli.py` stopped because its Python environment lacked `tzdata` for `America/New_York`. Treat that as an unresolved setup prerequisite, not a verified product regression or a current all-green run. No product code changed in this documentation session, and tests were not rerun for Markdown edits.

## Learning evidence and exact restart point

**Last completed gate:** EV-P8-WORKING-TREE-PICTURE-458. **Current gate:** EV-P8-PRETOOLUSE-459, trace part in progress, mid-remediation. See the exact attempt and pending question at the end of the learning ledger; do not reveal its answer in a restart message.

Next teaching interaction, in order:

1. Resume the pending condition-evaluation remediation for the two Bash payload traces. Ask for the check-by-check prediction and reasoning before revealing outcomes.
2. Check whether the learner can read `**fields`; use syntax-only help if needed.
3. Require a fresh target-level trace after recovery.
4. Finish the explanation, concrete downside/reversal condition, and transfer.
5. Review remaining Phase 8 closure obligations, then formally close only when evidence supports it. Run the major cumulative review before significant Phase 9 implementation.

Known cold from prior evidence, not newly assessed here:

- An answer-shaped value must not stand in for absence of knowledge.
- Records should assert only what was established.
- Missing evidence and observed absence are different.

Uncertain / due for retrieval:

- CONDITION_EVALUATION: predicting a raise without identifying a failed check; the active blocker in gate 459.
- `**fields`, and the parser design's downside/reversal condition: still owed.
- Proposal versus report, missing hooks versus disk authority, hook failure/exit behavior: recovered with assistance; fade scaffolding and retrieve later.
- Set union/intersection, trailing NUL split behavior, HEAD versus working-tree bytes, Git root discovery, picture placement versus reconciliation conclusions, and the time-span reason for two timestamps.

## Counters and next work

- Major counter: **1/2**; closing Phase 8 makes **2/2**, due before significant Phase 9 work.
- Foundation counter: **1/3**; unchanged.
- Next retrieval: active gate remediation first, then the overdue/weak concepts above through fresh surfaces and the due cumulative review.
- Next architecture reset: required at the Phase 8 -> 9 major transition; the seven-active-day clock was not newly verified. No reset is claimed here.
- Next implementation step after the gates: learner specification for the single-process baseline/edit/witness/report workflow and claimed-path coverage policy. No exact command name, event hierarchy, or implementation design has been approved by this scope decision.
- Final release reserve: setup, tests/defects, documentation, demo, static architecture view, manual defense. Phase 10's narrow extension begins only after the observation workflow is ready.

Files the learner should be able to teach: `compare.py`, `completeflow.py`, `reconcile.py`, and `working_tree_picture.py`. `claude_adapter.py`'s new PreToolUse/shared-parser path still has an open gate; do not call it mastered.
