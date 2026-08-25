# BuildLens — Current State

## Lifecycle

**Current phase:** Phase 1 — Pure Functions and Execution (contract prediction; no code yet)

## What exists

Planning and learning documents only.

There is intentionally no application implementation yet.

The Phase 0 tracing history is recorded verbatim in
`learning/LEARNING_LEDGER.md`.

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

Proposed first path:

```text
one diff-line string
→ classify_diff_line
→ one classification string
```

## What I should know cold before Phase 1

- variable assignment vs mutation at a basic level;
- function argument → parameter → local state → return;
- sequential / conditional execution;
- how to predict output without running Python;
- how to describe an input/output contract in plain English.

## What I demonstrated

- correctly traced an unseen two-call Python program before running it;
- bound arguments to per-call parameters and tracked local reassignment;
- selected branches from exact indexed string values;
- carried return values into later calls;
- preserved string case and produced the exact final output;
- explained the shared principle as following values through the code.

This passes the Phase 0 gate. It does not mark the concept mastered; delayed
retrieval and additional contexts are still required.

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

**Result:** Passed on unseen exercise `BL-P0-TRANSFER-20260825-012` after
correctly predicting both output and execution path without reported tool use.

## Reference-project use

Not yet.

Argos, Datum, and Trellis are deliberately deferred until the matching Python/design concepts have been introduced.

## Weak concepts / retrieval targets

- `exact_case_tracking`: initially changed capitalization mentally; corrected in
  later attempts and applied correctly in the final unseen trace. Delayed
  retrieval remains due.
- `local_reassignment_and_return_expression`: initially evaluated a return with
  an old local value; corrected and applied correctly in the final unseen trace.
- `trace_transcription_precision`: an earlier submitted explanation did not match
  the reported paper trace; the final unseen written trace was internally exact.
- Confidence calibration is not yet available because confidence has not been
  provided with the Phase 0 predictions.
- `branch_precedence`: the first Phase 1 prediction classified `+++` and `---`
  lines as ordinary additions/removals instead of checking the more specific
  metadata prefixes first.
- `empty_input_classification`: the empty string was classified as metadata
  instead of the default/context category.
- `unified_diff_metadata_meaning`: `+++` and `---` file headers were described
  as removed source-code lines and written with four prefix characters.
- `function_contract`: the learner does not yet know how to state the function's
  accepted input and promised output.
- `pure_function_side_effects`: the learner does not yet know whether the proposed
  pure function changes state outside its call.
- `classification_vs_extraction`: the classifier was described as returning a
  file path instead of a category label.
- `pure_function_vs_mutation`: the classifier was described as removing a header
  even though its contract only returns a value and leaves the input/external
  state unchanged.
- `data_vs_external_resource`: path-like characters inside a string were treated
  as an opened file rather than ordinary input data.
- `function_call_implies_mutation`: calling a classifier was assumed to remove
  part of its input despite a return-only contract with no file operation.
- `return_literal_as_call_value`: the learner is unsure that an executed
  `return` expression becomes the value of the function-call expression and is
  then assigned to the caller's variable.
- `dynamic_return_paths_vs_contract`: Python's runtime return behavior was
  treated as if one return expression guaranteed the function would always
  return that type; the distinction between possible branches and an intended
  stable contract needs reinforcement.

### Active remediation status

- `RETURN_VALUE` is stable at R4 on evidence `EV-P1-RETURN-007`: the learner
  correctly traced a no-argument function returning a string into a caller
  assignment and exact printed output.
- Next: one fresh R4 near-transfer without guiding state prompts. If correct,
  climb to R5 by adding exactly one branch.
- Evidence `EV-P1-RETURN-008` correctly completed that fresh R4 near-transfer
  without guiding state prompts. `RETURN_VALUE` is ready to climb to R5.
- Next: one function, one branch, one call, and no nested calls or domain
  vocabulary. If correct, give a fresh R5 near-transfer before returning to the
  BuildLens classifier contract.
- Evidence `EV-P1-BRANCH-009` predicted the exact R5 output correctly but did
  not include reasoning. The learner reported that the scaffold was too similar.
- Next: fade detailed prompts and test the real prefix-classification structure
  with two calls. Require branch-order reasoning before implementation.
- Evidence `EV-P1-CLASSIFY-010` correctly predicted `added metadata context`
  and connected `startswith` to return behavior. Detailed branch-order and
  outside-state explanations remain retrieval targets.
- New question: `diff_marker_vs_source_code` — the learner asked what the leading
  `+` in `+value = 1` is adding. Clarify that it is unified-diff notation marking
  the source content `value = 1` as newly present, not Python arithmetic.
- Evidence `EV-P1-DIFF-011` correctly explained that `+` marks `value = 1` as
  added and `-` marks it as removed. The diff-marker-versus-source distinction is
  stable at R1; `+++`/`---` metadata-header precedence remains a later retrieval.
- The learner requested a subject change after several similar traces. Next topic:
  design the first failing behavior test rather than issuing another trace.
- Evidence `EV-P1-TEST-012` proposed a valid input but described the expected
  behavior as applying a file change rather than returning `"added"`.
- Active test-design blocker: `classification_return_vs_downstream_effect`.
  Descend to R1 with a generic classifier and one input/expected-return pair;
  return to the BuildLens test only after that distinction is stable.
- Evidence `EV-P1-TEST-013` correctly identified input `20` and expected return
  `"adult"`, but confused an alternate input (`18`) with an incorrect returned
  value and misread the exact boundary. Continue at R1 with one changed-boundary
  variant before returning to BuildLens. Public evidence sync count: 1 of 5.
- Evidence `EV-P1-TEST-014` correctly reasoned that `18 <= 18` is true, expected
  `"child"`, and identified `"adult"` as the competing wrong return. Next: one
  differently surfaced blind transfer and the shared principle. Public evidence
  sync count: 2 of 5.
- Evidence `EV-P1-TEST-015` expressed the blind-transfer contract as an attempted
  function instead of a test specification and omitted the shared principle.
  Remain at R1: answer the package test fields without code, then explain the
  shared boundary-test principle. Public evidence sync count: 3 of 5.
- Evidence `EV-P1-TEST-016` correctly specified input `10`, expected `"heavy"`,
  and competing wrong return `"standard"`. Clarified that `10 >= 10` evaluates
  to Boolean `True`. Require the learner's shared-principle explanation before
  advancing. Public evidence sync count: 4 of 5.
- Evidence `EV-P1-TEST-017` did not yet identify the shared exact-boundary
  principle and conflated comparison direction, `else`/`else if`, and input versus
  return types. Provide one fresh plain-language boundary variant. The scheduled
  five-attempt public evidence sync is now due; do not advance the gate.
- Evidence `EV-P1-TEST-018` correctly solved and explained an unseen inclusive
  boundary test. The boundary-test transfer gate is passed. Python branch syntax
  remains an R0 remediation target; do not treat syntax transcription as a failed
  boundary concept.
- Evidence is recorded locally after every attempt. Public pushes are batched
  after five new attempts or immediately before implementation, whichever comes
  first; individual answers do not require individual pushes. Current batch: 1/5.
- Evidence `EV-P1-SYNTAX-019` correctly added colons and predicted the boundary
  behavior, but the submitted Python still lacked visible block indentation.
  Isolate indentation at R0 before introducing the BuildLens contract. Current
  public-sync batch: 2/5.
- Evidence `EV-P1-SYNTAX-020` used comments to describe indentation and placed the
  fallback return three levels deep. Remediate with explicit leading-space counts:
  function body = 4 spaces; branch body = 8 spaces; fallback return = 4 spaces.
  Current public-sync batch: 3/5.
- Evidence `EV-P1-SYNTAX-021` corrected the fallback indentation and predicted
  `"no"`, but could not explain that a false condition skips the `if` body and
  continues at the next function-level statement. Test that execution rule in one
  unseen local-value variant. Current public-sync batch: 4/5.
- Evidence `EV-P1-SYNTAX-022` correctly predicted returned `"standard"` and exact
  output `standard`, and recognized call-time local initialization. The learner
  remains unsure whether indentation/statement position or the Boolean condition
  controls execution. Require a two-rule teach-aloud before the next unseen trace.
  The scheduled five-attempt public evidence sync is due.
- Evidence `EV-P1-SYNTAX-023` correctly connected the Boolean condition to
  executing/skipping the `if` body, but described indentation as controlling calls
  and execution order. Require one corrected restatement: indentation owns blocks;
  calls invoke functions; execution normally proceeds top to bottom. Current
  public-sync batch: 1/5.
- Evidence `EV-P1-SYNTAX-024` correctly identified indentation as block ownership,
  but invocation, condition evaluation, and normal order remain conflated. Descend
  to a four-item concept match before another trace. Current public-sync batch:
  2/5.
- Evidence `EV-P1-SYNTAX-025` matched all four mechanisms correctly, but the prose
  still attributed branch execution to indentation and described an `if` as a
  returned value. Require four one-sentence definitions before another trace.
  Current public-sync batch: 3/5.
- Evidence `EV-P1-SYNTAX-026` correctly separated indentation, conditions,
  execution order, and return, with minor terminology refinements still useful.
  Climb to one unseen overlapping-prefix `if`/`elif` trace before introducing the
  BuildLens contract. Current public-sync batch: 4/5.
- Evidence `EV-P1-BRANCH-027` correctly identified the first overlapping-prefix
  condition as true and the returned string as `"pair"`, but the learner explicitly
  does not yet know `elif` and wrote the printed output with quotation marks.
  Descend to an R0 `if`/`elif` micro-problem, then require one unseen branch-order
  trace. The scheduled five-attempt public sync is due.
- Handoff checkpoint: remain in Phase 1 contract prediction with no application
  code. The immediate blocker is `ELIF_AND_FIRST_MATCH`; do not introduce the
  BuildLens function contract until that blocker passes an unseen variant.
- Evidence `EV-P1-ELIF-028` was answered correctly at R0. The learner identified the
  false first condition, stated the correct reason the `elif` is evaluated (the
  preceding condition was false), named the winning branch, and wrote the exact
  output `medium` without quotation marks. That last point resolves
  `printed_output_includes_quotes` for one attempt; it is not yet mastered.
- Evidence `EV-P1-ELIF-029` passed the unseen branch-order transfer. The learner
  asked to skip ahead first; the gate was compressed to its single transfer question
  rather than waived, and the learner then correctly stated that the swapped chain
  matches `score >= 90` and never evaluates the condition below it. The
  `ELIF_AND_FIRST_MATCH` blocker is cleared for Phase 1 purposes. It is not mastered:
  mastery still needs a third unseen variant in a second context plus one delayed
  retrieval.
- Open terminology refinements from that attempt: `return` was used for what is an
  assignment plus `print`, and the second branch of a swapped chain was called the
  `if` rather than the `elif`. Correct these in passing; do not descend a rung for
  them.
- Gate cleared, so the `classify_diff_line` contract has been stated in plain English.
  Evidence `EV-P1-CONTRACT-030` restated the input and the four labels correctly but
  answered the unchanged-state question with the project's name, which is not program
  state. The contract is therefore NOT yet approved, and no failing test or
  implementation may be written.
- Active blocker: `PURE_FUNCTION_NO_SIDE_EFFECTS`. Evidence `EV-P1-PURE-031` passed at
  R1: the learner predicted `hello` then `HELLO` exactly, showing that producing a new
  value leaves the original variable unchanged. Evidence `EV-P1-PURE-032` climbs one
  feature to R4 by replacing the string method with a `classify_diff_line` call and
  asking for the same two predicted outputs. A correct answer closes contract part 3.
- Evidence `EV-P1-PURE-032` answered correctly: `added`, and `line` unchanged. The
  transcribed line contained one extra space, which is `trace_transcription_precision`
  rather than a purity error; no rung was descended for it. Contract part 3 is closed
  and `PURE_FUNCTION_NO_SIDE_EFFECTS` is cleared for Phase 1 purposes, not mastered.
- All three contract parts are now restated correctly across `EV-P1-CONTRACT-030` and
  `EV-P1-PURE-032`. The contract awaits only the learner's explicit word of approval
  and explicit authorization to continue. No test and no implementation may be written
  before both are given.
- Two triggers for the public evidence sync are now active at once: five new attempts
  (`EV-P1-ELIF-028` through `EV-P1-PURE-032`) and the pre-implementation checkpoint.
  The repository-path blocker is resolved: use a temporary clone of
  `peyton150-startup/BuildLens` inside the workspace, copy the changed authoritative
  documents into it, commit and push there, verify public `main`, then remove the
  temporary clone. Do not commit through the enclosing home-directory repository.
- Confidence was reported for the first time in Phase 1 on `EV-P1-PURE-031`, as the
  words `faily confident` rather than a number. Keep requesting a number so
  calibration can eventually be measured.
- Format note from the learner: they report difficulty answering list-style recall
  prompts. Prefer concrete output prediction over enumeration, and infer the concept
  from the prediction rather than asking for properties to be listed.
- Confidence remains unreported on every Phase 1 attempt, so calibration still
  cannot be computed. Continue requiring a confidence number in each response.
- Public-sync resolution: `C:\Users\nicol\BuildLens_Project` intentionally remains
  a documentation workspace without its own `.git`. Codex performs verified public
  syncs through a disposable child clone. Evidence `028`–`032` is included in the
  pre-implementation sync checkpoint; implementation remains blocked only on the
  learner's explicit contract approval and authorization to continue.

## Files I should be able to teach

Planning only. No code file yet.

## Weekly architecture reset

Not started because there is no architecture yet.

The first reset becomes due after the first week of active implementation.

## Next implementation milestone

After the learner correctly restates and approves the first function contract,
write one focused failing test, verify that it fails for the expected missing-
behavior reason, and only then add the smallest implementation needed to pass it.

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
