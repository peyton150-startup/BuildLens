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
   - Test list in progress (plan acceptance: net changes, claimed-path coverage policy, unreadable paths, invalid inputs, applicable capture failures). Test 1 (D16) written with the learner: reports the change plus the missing-capture-file message; must not state that Claude made no claims. Derived via broken-find probes; the learner relapsed once to "Claude has no claims" (missing evidence vs observed absence) and recovered at R0.
   - Test 2 (D15b/D15c) written with the learner: action includes the Git failure at the witness plus y; must contain the cli.py change, the first-failure message, and a window ending at the successful retry; must not end the window at the failed attempt. Learner first omitted the failure from the action (action vs check confusion, recovered at R0) and carried Test 1's "claims" must-NOT over.
   - Test 2 patch (learner-derived 2026-09-15): `patch("git_adapter.capture_tracked_paths", side_effect=[paths, GitCaptureError(...), paths])`. Evidence: predicted a single-exception side_effect as failing only at the witness (misconception), corrected by a run (every call raises); invented the per-call list idea unprompted; predicted the list form correctly; confused "tracked paths" with changed content (recovered: names only, observe_file reads content); predicted the exhausted list as "never ends and crashes" (it raises StopIteration at once).
   - side_effect transfer (weather app) succeeded unaided on the mechanics; the learner wrongly generalized that too few calls also raise StopIteration, then correctly predicted that unused entries pass silently (verified by a run).
   - side_effect principle: the unscaffolded restatement swapped the cases; recovered at R0 with counts named (2 entries/3 calls -> StopIteration; 3 entries/2 calls -> unused silently). Retrieval due on a fresh surface without counts named.
   - Test 3 (net changes) written with the learner: notes.md CREATED, cli.py MODIFIED, old.py DELETED; must not contain README.md (edited then restored, invisible to two pictures). Needed R0 per-file scaffolding. The learner repeated Test 1's "claims" as must-NOT four times across Tests 2-3; retrieve writing scenario-specific must-NOT lines.
   - Test 4 (coverage policy D6/D6a/D7) written with the learner: b.py (Edit holds + extra change), c.py (Write does not hold), d.py (line-endings only) reported; a.py (Write holds) must not appear. The learner asked why a holding claim is sometimes reported; explained once (Write = whole file accounted for; Edit = one fragment), then applied it to new files correctly. Expected lines still needed per-file R0 and a Write/Edit contrast for the must-NOT line.
   - D8a (revised): a path skipped under D6 (latest claim is a holding Write) still shows its superseded earlier claims, summarized as "<path> has N unchecked superseded claims. Press i to see them." (no new store: the claims are already in the capture file; payload content is only a claim). The learner first proposed a claim/file-version store (deferred durable history), then found the capture file already holds them.
   - D17 after the report find stays open: i shows the unchecked superseded claims (no confirmation); Enter asks "Press Enter again to exit, or i to see the unchecked superseded claims." Learner's confirmation rule, stated in own words: confirm when an accidental keypress would end the session or start/end a long process forcing a restart.
   - Test 5 (D8/D8a/D17) written with the learner: e.py (latest Write holds) shows only its superseded-claim summary and must not appear as a changed path; f.py (latest Write fails after a shell append) is reported with its summary. Must-NOT retrieval failed unaided twice late in the session and recovered only at R0; the action again omitted the key event (shell append) and the setup again named an event instead of starting files.
   - Must-NOT retrieval after a break (library overdue emails, 2026-09-15): not independent. The learner classified the items correctly but needed the fields split, and missed C (not yet due) until a broken-app probe. Pattern: correct per-item reasoning; does not spontaneously ask "what would a broken version wrongly print?" Next retrieval: fresh surface with only a reminder to run that check.
   - Test 6 (unreadable paths) written with the learner: h.py DELETED; g.py undetermined (unreadable at witness); must not call g.py DELETED nor h.py undetermined. The learner traced reconcile.py:148-164 and the g.py flags correctly; the must-contain line was vague until paths were requested; the must-NOT was first written inverted (self-corrected after a broken-find probe).
   - Test 7 (invalid inputs D12/D14) written with the learner: k.py changed with no claim plus "capture line 60 skipped: not valid JSON"; must not draw a claim from line 60, show a verdict for the out-of-repository x.py, or stay silent about line 60. Must-contain needed an R0 choice among three reports (input-vs-output blocker recurring); the x.py must-NOT line was produced from the broken-find framing alone (improvement).
   - Tests 1-7 cover every plan acceptance category (capture failures 1-2, net changes 3, coverage policy 4-5, unreadable 6, invalid inputs 7). Decisions without tests: D15a, D13b, D9-D11, D15c, D17; D14's open detail (count excluded claims?) undecided.
   - D14a (settles D14's open detail): excluded out-of-repository claims get one count line plus a key to view their paths. D17b: after the report, options one per line: (i) see unchecked superseded claims, (o) see claims for files outside this repository, (Enter) exit with confirmation. Learner's downside: more options to read; reversal: one key if the two lists were nearly always needed together.
   - Test coverage decisions: the learner chose Test 8 (D15a, Git fails at baseline) and an own test for D13b, and raised D13c (retry when the capture file is missing at the witness, with the learner's downside that most causes are permanent). The learner then DELEGATED the remaining coverage decisions to Claude (2026-09-15); these are CLAUDE-PROPOSED, not learner evidence, and must be defended or revised by the learner at the Phase 9 gate: D13c keeps "print the path looked at" and the D15c n-confirmation (Test 9); D11 own test (Test 10); D9/D10/D15c-n/D17b folded into one scripted-input interaction test (Test 11); D14a count line folded into Test 7; real-console Enter/Ctrl+C is a manual demo check.
   - Test list complete: Tests 1-11. Implementation has NOT started: no `find` code exists.
   - Patch 1 (capture-file reader) contract drafted. D18: capture position = line count at baseline (the learner chose it over a byte offset because line numbers are needed for D12 messages); measured 0.42-0.66 s to count 237 MB / 1,350 lines on this machine; learner's reversal: switch to a byte offset if counting reaches ~10 s (~5.6 GB at the measured rate). D18a (learner leaning, under review): the baseline count includes only newline-terminated lines, so a line half-written at baseline is read at the witness once complete (learner first predicted Python would not count an unterminated last line; a run showed it does). D18b: at the witness, an unterminated final line is named "capture line N still being written" (not "not valid JSON"), because it may still become valid; its file's change is reported without a claim. D18a reversal (recovered at R0): count unterminated lines only if appends were guaranteed to land whole. Evidence from the real capture file (2026-09-15): 399 PostToolUse claims, 302 PreToolUse, 701 BLANK lines, 0 invalid JSON: the capture hook `{ cat; echo; } >>` writes an extra empty line per payload, so a naive D12 would name every blank line "not valid JSON".
   - D19 (accepted 2026-09-16): keep the capture hook unchanged (`echo` guarantees a trailing newline, per the Phase 8 ledger); find silently skips whitespace-only lines (content, not position). Downside: a capture with no input is byte-identical to a separator, so a lost claim cannot be warned about (its change still appears unclaimed); removing echo would not fix that (verified: writes nothing) and would risk joined payloads. The learner confused the two hook variants' empty-input output twice; recovered with runs.
   - D20 (2026-09-16): a valid-JSON PostToolUse line that `parse_post_tool_use` rejects is skipped and named with the parser's reason; never reinterpret an unrecognized field (the learner first chose stopping find, citing "no partial pictures", then recognized one bad line would stop every session; also briefly treated a renamed `path` field as the file, recovered at R0).
   - Patch 1 design complete: D3, D4, D12, D13a, D18/D18a, D18b, D19, D20.
   - Patch 1 IMPLEMENTED 2026-09-16 (test-first): `capture_reader.py` (`count_complete_lines`, `read_capture`) + `tests/test_capture_reader.py` (8 tests); all 14 test scripts pass. Claude choices awaiting learner review: Bash PostToolUse dropped silently; non-object JSON named as not a usable claim; OSError propagates; invalid UTF-8 = not valid JSON.
   - Patch 1 gate, trace: completed WITH scaffolding (missed the position check on line 1 and listed silent skips as named skips; recovered at R0). Result: claims [6]; skipped [5 "not valid JSON", 7 "still being written"].
   - Patch 1 milestone gate PASSED WITH ASSISTANCE (2026-09-16): explanation needed a syntax detour on `json.loads`/`JSONDecodeError` (learner believed bare words and empty text were JSON values; corrected by a run); transfer (greenhouse sensor log) needed R0 on `number <= position` (the learner inverted which line the position skips) and a worked example; the key transfer idea was stated: the wrong check order stores a wrong number (21.0 for 21.7) silently. Retrieval due on a fresh surface: `<=` position check and first-match order; silent vs named skips; what json.loads accepts.
   - Patch 1's four Claude choices approved by the learner (2026-09-16). Choice 1 (Bash PostToolUse dropped silently) was discussed: hooks match `Edit|Write`, so the real file has 0 Bash payloads; reason given: nothing checkable. Downside, partly reached: the report would not reveal a command ran.
   - D21 (learner's): `file_observer._relative_to_root` renamed public `relative_to_root` (the learner first chose importing the private helper for "least work"; the "(outside)" scenario showed a silent keep; then weighed copying against drift). Downside: coupling; the learner's claim that "Phase 10 is last, so it won't change" was corrected.
   - Patch 2 IMPLEMENTED 2026-09-16 (test-first): `claim_selection.py` (`select_claims` -> `ClaimSelection` latest/superseded/outside) + `tests/test_claim_selection.py` (4 tests); all 15 test scripts pass. Real-file smoke: 457 claims, 21 inside paths, 12 with superseded (max 192 on the Phase 9 ledger), 11 outside (Claude memory files). Claude choice awaiting review: sort by line_number.
   - Patch 2 gate: trace completed WITH HEAVY SCAFFOLDING (syntax detours: `[-1]`/`[:-1]` indexing and slicing; dict-comprehension `if` filter; the learner repeatedly treated `latest` as one value and put a single-claim path into `superseded` until an explicit analogy mapping). Explanation: reached that without the sort, arrival order would pick the older claim; the sort choice was approved. Retrieval due: negative indexing/slicing; comprehension filters; one dict entry per key.
   - Patch 2 milestone gate PASSED WITH ASSISTANCE (2026-09-16). Transfer (warehouse scans) mostly unaided: sort order, per-package latest, history, and the arrival-order failure correct; one inconsistency (gave a set-aside W2 package a current location).
   - D22 (learner's, after an R0 dependency check): D6 lives in a step before `reconcile`; `reconcile` stays unaware of claims. D22a: its parameter `claimed_paths` is renamed `whole_file_held_paths` (the learner tested "latest claimed" and "latest held" against an Edit-holds path and found the missing idea: the whole file is accounted for).
   - D23 (LEARNER'S DECISION over Claude's challenge): the D6 step re-reads each latest Write claim's file (`observe_file` + `compare_write`) rather than comparing with the witness picture's hash. Known downside, recorded: a change the witness recorded but that is undone right after it can be skipped and never reported; this revises the D5 "one witness-time observation" settlement and is an exception to D12's never-hide rule for that window. Learner's reason: a user who opens the file later should not see the report contradict it. Reversal condition not yet given; must be defended at the Phase 9 gate.
   - Patch 3 IMPLEMENTED 2026-09-16 (test-first): `reconcile`'s parameter renamed `whole_file_held_paths`; new `whole_file_coverage.py` (`whole_file_held_paths(selection, root)`, re-reads per D23) + `tests/test_whole_file_coverage.py` (5 tests); all 16 test scripts pass.
   - Patch 3 gate, trace: CORRECT and UNAIDED (2026-09-16), the first unscaffolded trace of the implementation run. The learner then proposed holding normalize-only matches too; reminded of their own D6a, they kept D6a.
   - D23a (learner's proposal during the D23 defense, 2026-09-16): a latest Write counts as held only if it holds on re-read AND the re-read hash equals the witness hash; otherwise it is reported and flagged "changed after the witness". This closes D23's hiding case. Implemented test-first: `whole_file_coverage(selection, witness, root) -> WholeFileCoverage(held, changed_after_witness)`; a path the witness could not read is neither held nor flagged. All 16 test scripts pass.
   - Patch 3 gate: trace done unaided. Explanation partly given (hash vs bytes for normalize; the learner did not describe D23's hiding case) and produced D23a.
   - Patch 3 / D23a milestone gate PASSED WITH ASSISTANCE (2026-09-16). After remediation, the learner independently traced the mismatched-hash case: not held, changed-after-witness flagged, and the baseline-to-witness change remains reportable. The warehouse transfer decisions were correct; the learner recovered that a validation of one version does not prove facts about a different version. Not mastered; delayed retrieval is due on version-linked suppression and the change-and-restore limit.
   - **Resume at:** patch 4, the `find` interaction loop. D23a is committed and pushed as `6b220fa`; all 16 test scripts passed at handoff, and only `.codex/` was untracked.
   - Implementation plan: the input-source question (how `find` receives keypresses so Tests 10-11 can script them) belongs to patch 4. Proposed patch order (Claude-proposed, learner to confirm): (1) capture-file reader: position, read range, JSON parse/skip, PostToolUse only (D3, D4, D12, D13a); (2) claim filter and latest-claim selection (D14, D8); (3) D6 coverage policy in reconcile; (4) `find` interaction loop with injected input (D9-D11, D15, D13c, D17b); (5) report wording (D7, D8a, D14a, D16). Then the Phase 9 knowledge gate (event/state trace through a failure + fresh debugging scenario + transfer). Major counter is 0/2 and becomes 1/2 when Phase 9 closes, so no cumulative review blocks Phase 10's narrow extension.

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
