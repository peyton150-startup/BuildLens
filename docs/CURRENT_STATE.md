# BuildLens — Current State

Last updated: 2026-09-14 — major cumulative review 2 passed; tests and docs layout patches done; Phase 9 started (idempotence lesson done, learner-led workflow design in progress).

This file is the current snapshot. The [prior accumulated state notes](history/CURRENT_STATE-before-core-v0.1-2026-09-13.md) are preserved byte-for-byte for historical context, not current instructions. Exact historical prompts and learner answers remain in `learning/LEARNING_LEDGER.md`; none were changed by this scope revision.

## Phase and active release

**Phase 8 is CLOSED** (2026-09-13, composite gate EV-P8-PHASE-GATE-460). Phases 7 and 8 are complete. **Phase 9 STARTED 2026-09-14** (reduced Core v0.1 scope); no Phase 9 product code yet. The latest recorded product commits are `c78b1b6` (PreToolUse parser) and `bb92ba5` (optional PostToolUse tool-call ID); no product code changed while the gate ran.

The active scope at the top of `IMPLEMENTATION_PLAN.md` is authoritative: finish the observation core and a single-process reconciliation workflow, then attempt one tracing archetype only if time permits. Facilitator-run gates are the release fallback. Persistence, API/UI, collaborative editing (including Phase 9 merge primitives), automated mastery, and automated interviews are deferred. Phase numbers are preserved. No counter was reset.

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

Tests live in `tests/` (moved 2026-09-14, EV-LAYOUT-PREDICT-468). Each test script puts the repository root first on `sys.path`, so any one runs by path from any folder, for example `python tests/test_reconcile.py`. On 2026-09-14 all 13 scripts passed on this machine, run from the repository root, from `tests/`, and from an unrelated folder, including `test_cli.py`. The 2026-09-13 scope-review environment lacked `tzdata` for `test_cli.py`; a fresh-environment setup procedure is still release work, so do not claim a fresh environment passes.

## Learning evidence and exact restart point

**Last completed gate:** EV-P8-PHASE-GATE-460, the Phase 8 composite phase gate — PASSED 2026-09-13 across non-Claude surfaces Tern (remediated), Kestrel, Wren, Osprey, Heron and a closing check; exact prompts, verbatim answers, grading corrections and facilitator errors are at the end of the learning ledger. **No gate is open.**

Next, in order:

1. **Major cumulative review 2 — PASSED 2026-09-14** after adaptive remediation (EV-CR2-Q1-461 .. EV-CR2-ARCH-467; see "MAJOR CUMULATIVE COUNTER RESET — 2026-09-14" in the ledger). Phase 8 -> 9 architecture reset completed with scaffolding.
2. **Layout patch — tests moved to `tests/`** (2026-09-14, option B chosen by the learner: a `sys.path` insert at the top of each test). The learner predicted the bare-name import failure and the `-m` success; both were verified. The move exposed a hidden dependency on the current folder in `test_completeflow.py` (`Path("compare.py")`), now anchored to the repository root. **Knowledge gate passed with assistance** (2026-09-14): import mechanism, ordering, downside and the cwd fix correct; the run command `python tests/test_cli.py` needed a worked example. Retrieval due: file path form versus `-m` module name form. **Docs grouping done** (2026-09-14, EV-DOCS-LAYOUT-469): plan, current state and handoff moved to `docs/`; old handoffs and `QUIZZES.md` moved to `learning/`; `CLAUDE.md`, `AGENTS.md`, `README.md` stay at the root. Archived handoffs and plans keep their original, now-stale paths as verbatim records.
3. **Phase 9 in progress.** Idempotence lesson done (EV-P9-IDEMPOTENCE-470 .. EV-P9-DEDUP-TRANSFER-472): an ID names a thing, not an event; ID-only dedup is safe only when the id is unique per real event and reused by its retries. **Learner-led design, under review, not approved** (EV-P9-DESIGN-473):
   - D1 `python cli.py find`, a new subcommand.
   - D2 claims come from the hook capture file `payload_samples.jsonl` read at witness time (hooks write to disk in separate processes; `find` cannot receive payloads in memory).
   - D3 scope = the file position remembered at baseline; only lines appended before the witness are read (payloads carry no timestamp; session_id rejected by the learner because a new Claude session would be excluded).
   - D4 PreToolUse lines are ignored; only PostToolUse lines become claims.
   - D5 a repeated PostToolUse in range needs no dedup: all claims are judged against one witness-time observation and `claimed_paths` is a set.
   - Settled with the learner: judging claims at witness time makes a later rewrite visible as a failed claim (without attribution); change-and-restore stays invisible; no report-time hash exists (payloads carry none, the capture hook observes nothing, and storing per-report observations is deferred persistence), so the Q6 hash idea does not apply.
   - D6 claimed-path coverage policy: skip a claimed path only when a Write claim holds at witness time (whole-file equality); report every other changed path, including Edit-claimed ones (containment checks only two fragments — traced with an unreported appended line that an Edit CLAIM_HOLDS would otherwise hide).
   - D6 downside, named by the learner: expected Claude Edit changes still appear as reported changes (noise); change-and-restore stays invisible.
   - D7 report wording for a changed path with a claim: state the change window, the claim and its witness-time verdict with what it covers, and that other changes are not ruled out; never attribute the change or say "no unexpected changes" (the learner first chose an authorship-claiming wording at confidence 90, then recovered).
   - D6a `CLAIM_HOLDS_AFTER_NORMALIZE` paths are reported, marked line-endings-only (learner's reason: the bytes still differ; downside: noise where many files are converted).
   - Learning ledger split per phase on 2026-09-14: `learning/LEARNING_LEDGER.md` is now an index; Phase 9 evidence goes in `learning/LEARNING_LEDGER_PHASE_9.md`.
   - D8 several claims on one path: the latest claim by capture-file line order decides D6 (an older superseded claim is reported only as "does not hold as of witness").
   - D9 the user triggers the witness picture from find's own terminal (Claude's Stop hook is a separate per-turn process and is not used): "Press Enter to end the session and get a detailed report", then "Are you sure? (y/n)"; n returns to waiting.
   - D10 Ctrl+C while waiting asks y (take the witness and report) / n (return to waiting).
   - D11 Ctrl+C during the witness picture: no report; say the picture was interrupted (a partial witness would make unread files look DELETED).
   - D12 an unparseable capture line in the read range is skipped and named in the output as not valid JSON, for a reason find cannot verify; its file's change is then reported without a claim (over-reporting, never hiding).
   - D13a capture file missing at baseline counts as position 0; at witness every line is read. D13b capture file present at baseline but missing at witness: stop with a message, no report (claims may exist but cannot be read).
   - D14 claim filter: convert each claim's absolute `file_path` with `_relative_to_root` against the repository root; `None` (outside the repository) is excluded; kept claims enter `claimed_paths` as Git-style relative paths (e.g. `tests/test_cli.py`). `cwd` is not a filter — real payloads show Claude working in `tests\` (4 of 222), which a cwd-equals-root rule would wrongly drop.
   - D15a Git fails at baseline: find catches `GitCaptureError`/`OSError`, prints its own message (the baseline picture failed, and why), and stops; nothing is lost.
   - D15b Git fails at the witness: no report (one picture cannot show a change; a baseline-only report would present a missing measurement as "no changes"). Print that the witness picture failed and why; keep the baseline picture (paths, hashes, root) and the capture-file position in memory; ask "Try again? (y/n)". y retakes only the witness (the window ends at the successful witness); n exits and loses the baseline. No silent automatic retry (permanent failures never clear, and the user cannot fix an unseen failure). Learner's reversal condition: silent retry only if every failure were temporary and self-clearing.
   - D15c wording accepted by the learner: "Try again? (y/n)" / "If you press n, find exits and can no longer report what changed since you started it." / "Your files, including Claude's edits, stay exactly as they are." Final (learner's, under review): n leads to a second confirmation showing this warning (an accidental n would lose the session); y retries immediately with no confirmation (an accidental y costs only a short wait). D9 and D15c both confirm only steps that cannot be undone.
   - D2 checked against the plan (Challenge 16, 2026-09-15): find writes nothing to disk, so no stopgap store; the capture file is a cross-process relay (hook process -> file -> find), but line 12 says a relay is "not required", not forbidden. Consequence: find must work without the capture hook. The learner first misread "not required" as "forbidden" and recovered at R0.
   - D16 capture file missing at both baseline and witness: still report every observed change, with no claims, and state explicitly that the capture file was missing so no Claude reports were checked (learner first chose no report, then revised after the D13b comparison).
   - D16 clarified: with no hook, Claude's tool calls still happen, but no readable record exists; the message must say reports were not captured, never that Claude made none.
   - **Resume at:** the test list for the find workflow (plan acceptance: net changes, claimed-path coverage policy, unreadable paths, invalid inputs, applicable capture failures), learner-proposed.

Known cold from prior evidence, not newly assessed here:

- An answer-shaped value must not stand in for absence of knowledge.
- Records should assert only what was established.
- Missing evidence and observed absence are different.

Uncertain / due for retrieval:

- From gate 460: validate (shape, adapter) versus verify (truth, observe + compare) inside a composite question; an event/lifecycle field is read by the adapter then stops (relapsed 4x); argument versus return value; `ObservedFile` class versus `observe_file`; why compare is testable without a disk; stating rules without sentence frames.

- CONDITION_EVALUATION: predicting a raise without identifying a failed check; recovered in gate 459, retrieval due.
- Step order in find (2026-09-15, Challenge 15b): the learner believed claims and verdicts exist before the witness picture; corrected at an R0 step-order question; retrieve on a new surface. Also retrieve "a missing measurement is reported as missing, never as a result" as a general principle (stated only as an action rule). User-facing warning wording (2026-09-15): the learner's reasoning about the loss was correct, but the wording kept naming internal data ("baseline/observational data") and once read the kept part of a worked example as lost; produced both parts (lost ability + what stays safe) only after a worked example and an R0 split. Retrieve on a new surface.
- `**` with an explicit duplicate argument; declaration versus runtime check (`file_path: str`); stating a reversal condition from scratch rather than choosing one.
- Proposal versus report, missing hooks versus disk authority, hook failure/exit behavior: recovered with assistance; fade scaffolding and retrieve later.
- Set union/intersection, trailing NUL split behavior, HEAD versus working-tree bytes, Git root discovery, picture placement versus reconciliation conclusions, and the time-span reason for two timestamps.

## Counters and next work

- Major counter: **0/2** (reset 2026-09-14 after major cumulative review 2 passed).
- Foundation counter: **1/3**; unchanged.
- Next retrieval: unaided two-path architecture redraw (ingest path and picture/reconcile path, with data on arrows); ObservedFile vs observe_file unprompted on a fresh surface; argument vs return value unprompted; CONDITION_EVALUATION on another surface; naming concrete validation checks. Ask for confidence inside every answer block — still often omitted.
- Architecture reset study targets (EV-CR2-ARCH-467): `take_picture` calls `git_adapter` (root, tracked + untracked listings) then `file_observer.observe_file` per path; `git_adapter` and `file_observer` are shared by both paths; `claimed_paths` is reconcile's third input; `reconcile` calls no other BuildLens module; no session-end trigger exists.
- Next architecture reset: by the seven-active-day clock or the next major transition.
- Next implementation step: finish the learner's design review (see item 3 above), then tests first. No design is approved yet. Retrieval due from Phase 9 so far: event identity vs thing identity; relative links from the linking file's folder; file path form vs `-m`.
- Final release reserve: setup, tests/defects, documentation, demo, static architecture view, manual defense. Phase 10's narrow extension begins only after the observation workflow is ready.

Files the learner should be able to teach: `compare.py`, `completeflow.py`, `reconcile.py`, and `working_tree_picture.py`. `claude_adapter.py`'s adapter boundary is gated (459, 460) but not mastered; retrieval is due.
