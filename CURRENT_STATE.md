# BuildLens — Current State

## Lifecycle

**Current phase:** Phase 2 — Data Representation and Test Design (started; no Phase 2 code
yet, data model being specified by the learner)

## What exists

Planning and learning documents, plus the first implementation.

- `classify.py` — `classify_diff_line(line)`. Four branches in the learner's stated
  order: the five metadata prefixes first, then `+` for `"added"`, then `-` for
  `"removed"`, then an `else` returning `"context"`. The `---` and `+++` tests require a
  trailing space so headers are separated from deleted or added content. Every input
  receives a label, so the amended contract's total promise is met and `None` is no longer
  reachable.
- `test_classify.py` — seven tests, run with `python test_classify.py`: an added line, a
  removed line, a deleted line of dashes, a file header, a hunk marker, an unchanged
  context line, and the empty string. All green, exit code 0.

No test runner is installed and no package layout exists; both are deliberate and
recorded below.

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

This path now exists and runs:

```text
one diff-line string
→ classify_diff_line
→ one classification string
```

Concretely, in `classify.py`:

```text
line
→ starts with diff --git / index / "--- " / "+++ " / @@  → return "metadata"
→ startswith("+")                                  → return "added"
→ startswith("-")                                  → return "removed"
→ otherwise                                        → return "context"
```

Every input now reaches a return, so the amended contract's promise of exactly one label
per call is met.

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

- The learner explicitly approved the `classify_diff_line` contract and authorized the
  first failing test with the words `i approve and authroize it all`. The contract is
  now the accepted behavior specification for the first implementation.
- First test written: `test_classify.py` at the project root. It asserts that
  `classify_diff_line("+value = 1")` returns `"added"`. Only that one category is
  tested; the other three are deliberately deferred.
- Two tooling decisions were made deliberately and are both reversible. No test runner
  was installed, because a single `assert` and one command achieve the same result
  without introducing machinery the learner has not earned; a runner becomes justified
  when running tests by hand becomes the actual annoyance. The module and its test sit
  flat at the project root with no import-path code, so that moving them into `src/`
  and `tests/` during Phase 4 decomposition is a motivated refactor with visible
  history rather than empty folders created early.
- Evidence `EV-P1-RED-033` is SUSPENDED, not answered. The learner approved the test
  as written but could not commit to a prediction, because two prerequisites surfaced:
  `assert` is unreadable, and the line Python stops on is unknown. Do not run the test
  and do not write `classify.py` until the prediction is reissued and committed.
- Active blocker: `SYNTAX_READING` on `assert`. Evidence `EV-P1-SYNTAX-034` descends to
  R0 with one integer, two assertions, and two prints. The remediation order is fixed:
  `assert` first, then the `import` line as a separate concept, then reissue
  `EV-P1-RED-033`.
- Evidence `EV-P1-SYNTAX-034` passed. The learner predicted both outputs correctly and
  stated the mechanism correctly: execution continues line by line until an assertion
  is false, then stops. New misconception corrected in passing:
  `failed_assert_prints_a_message` — a violated assertion prints nothing; it raises
  `AssertionError` and writes a traceback. `assert` is stable at R0.
- Evidence `EV-P1-RED-035` reissues the suspended red-test prediction. The import form
  was explained, deliberately withholding what happens when the named module is absent,
  since that is exactly what the learner must predict. Do not run the test and do not
  write `classify.py` until this prediction is committed.
- Evidence `EV-P1-RED-035` passed. The learner predicted the stop line and the reason
  before the run, and the observed `ModuleNotFoundError: No module named 'classify'` at
  line 8 matched. The traceback was then read field by field with the learner. The
  first red is confirmed to fail for the missing-behavior reason.
- Evidence `EV-P1-GREEN-036` is issued: choose which of three candidate
  implementations make the single existing assertion pass. The intended insight is that
  the unconditional `return "added"` also passes, which is what motivates a second
  test. Do not write `classify.py` until the selection is committed.
- Evidence `EV-P1-GREEN-036` is partial. Candidate B was chosen correctly and candidate
  C was rejected for the correct reason, but the unconditional candidate A was also
  rejected even though it passes the single existing assertion. New misconception
  `test_passes_implies_implementation_correct`: one passing test is assumed to select
  exactly one implementation.
- Active blocker: `TEST_STRENGTH`. Evidence `EV-P1-GREEN-037` descends one rung and
  asks the learner to trace candidate A directly, reusing the already stable
  return-value and `assert` skills. After that, ask which second test would fail for A
  but pass for B, and write `classify.py` only then.
- Evidence `EV-P1-GREEN-037` passed and reached the target insight: the learner
  recognized that the unconditional candidate A also satisfies the single test.
  `TEST_STRENGTH` is cleared for Phase 1 purposes. Two refinements: candidate A does
  not inspect its input at all, and the printed value was again written with quotation
  marks, the second Phase 1 occurrence of `printed_output_includes_quotes`.
- First implementation written and green. `classify.py` contains exactly the selected
  candidate B, and `test_classify.py` now prints `test passed` with exit code 0. The
  red was predicted, observed, and explained before any implementation existed.
- Evidence `EV-P1-GAP-038` is issued: the learner supplies one input the current
  function answers wrongly or not at all, plus the label it should return. That example
  becomes the second test. Do not choose the next behavior for the learner.
- Evidence `EV-P1-GAP-038` is partial. The learner correctly restated, unprompted, that
  candidate A inspects nothing, but the supplied example `+green_giant` expecting
  `added` is a case the current implementation already handles correctly, not a gap.
  New misconception `handled_case_vs_failing_case`: examples are being chosen by
  category fit rather than by whether the code currently fails them.
- Active blocker: `FUNCTION_WITH_NO_RETURN_PATH`. Evidence `EV-P1-GAP-039` descends to
  a two-call trace of the real four-line function, contrasting `+green_giant` with
  `-green_giant`, so the learner discovers the silent `None` rather than being told.
  Do not write the second test until that trace is committed.
- Evidence `EV-P1-GAP-039` passed. The learner predicted `added` exactly and answered
  `nothing` for the minus line, which is the right model with one refinement: the call
  produces the value `None`, which was then observed together. This located the failing
  input the learner could not choose earlier, resolving `handled_case_vs_failing_case`
  by observation rather than by being told.
- Second test written from the learner's own example: `classify_diff_line("-green_giant")`
  must return `"removed"`. `classify.py` is deliberately unchanged so the red can be
  predicted first. Evidence `EV-P1-RED2-040` asks which test fails, which error type
  occurs and why, and whether `test passed` prints.
- Evidence `EV-P1-RED2-040` is SUSPENDED, not failed. The learner correctly hunched
  that `test passed` will not print, but reasoned that no `AssertionError` is possible
  because no `assert` was visible. The prompt had quoted only the final three lines of
  the file, which caused this; the full file was shown immediately afterward. The real
  blocker is `assert_inside_called_function`: an assertion inside a called test function
  is not yet recognized as code that runs.
- Active blocker: `FUNCTION_CALL_FLOW`. Evidence `EV-P1-CALL-041` descends to R1 with
  one no-argument function whose entire body is one false assertion, plus two prints.
  Reissue `EV-P1-RED2-040` only after that is stable, and do not add a branch to
  `classify.py` before then.
- Presentation rule learned this session: when asking about a file's behavior, show the
  whole file. Quoting a fragment produced a reasonable but wrong inference from an
  incomplete picture, and that is a prompt defect rather than a learner error.
- Presentation rule extended, again at the learner's correction: whenever an output is
  shown, show the exact source that produced it in the same message. In one comparison
  the one-branch source was displayed with its traceback but the two-branch run showed
  only its output, leaving the learner unable to tell which code produced `test passed`.
  Never print a result without the code beside it.
- Evidence `EV-P1-FILES-045` is RETIRED as superseded rather than answered. Its purpose
  was to establish which file owns behavior and which owns expectations; the learner
  reached that understanding instead through a side-by-side run in which one identical
  test file was executed against the one-branch and two-branch modules, producing
  opposite verdicts. `MODULE_VS_TEST_FILE_OWNERSHIP` is resolved by demonstration. The
  capitalization variant remains available later as a fresh surface form for the older
  `exact_case_tracking` weakness.
- Evidence `EV-P1-CALL-041` is wrong and preserved as such. The learner named the exact
  open question unprompted — whether a false assertion ends only the function or the
  whole program — then committed to the wrong side of that binary. New misconception
  `exception_stops_only_the_function`: a raised error is treated as a local exit rather
  than as something that propagates to the caller and terminates an uncaught program.
  The failing run and its two-frame traceback were read together afterward.
- Evidence `EV-P1-CALL-042` stays at the same rung rather than descending, because the
  structure is identical and only the assertion's truth value changed. It tests whether
  the learner overcorrects into believing any assertion inside a function halts the
  program. Reissue `EV-P1-RED2-040` only after this is correct.
- Evidence `EV-P1-CALL-042` passed with no overcorrection, which was the specific risk
  it was built to detect. `exception_stops_only_the_function` is corrected and
  `FUNCTION_CALL_FLOW` is stable at R1. Confidence was reported qualitatively for only
  the second time in Phase 1.
- Evidence `EV-P1-RED2-043` reissues the second-red prediction with both files shown in
  full, per the new presentation rule. Do not add a branch to `classify.py` until the
  prediction is committed and the run has been compared against it.
- Evidence `EV-P1-RED2-043` passed on all three answers. The red was observed, the
  `elif` branch for removed lines was added, and both tests are green at exit code 0.
  The implementation now contains the exact `if`/`elif` structure the learner traced in
  the locker and grading exercises.
- The learner reported the problem was too easy and asked for more difficulty at the
  same conceptual level. This is the assistance-fading signal from LEARNING_RULES 14.8.
  Scaffolding is now removed: no options, no sub-questions, no indication of which part
  is the trap. Maintain this reduced support unless an answer shows it was withdrawn too
  early.
- New question raised by the learner: `which_file_holds_which_code` — on being shown
  `test_classify.py` they asked why there is no `elif` in it. The two-file split and the
  import bridge were not yet clear. Both files were then displayed complete and labelled
  by filename, and the division was stated explicitly: the test file states expectations
  and contains no branching, the module holds the behavior, and the import connects them.
  Evidence `EV-P1-FILES-045` checks this with a hypothetical capitalization change,
  which also revisits the older `exact_case_tracking` weakness in a new surface form.
- `EV-P1-META-044` is SUSPENDED, not failed. The learner classified none of the eight
  lines and disputed the diff format itself, proposing two-character header prefixes.
  This is `unified_diff_metadata_meaning` resurfacing in a third form: previously written
  with four characters, now with two. Rather than assert the format, a real repository was
  created and real `git diff` output was displayed, confirming three dashes and three
  plusses. Settle format questions by generating real tool output, never by assertion.
- Active blocker: `OVERLAPPING_PREFIX_MATCHING`. Evidence `EV-P1-PREFIX-046` descends to
  R1 with a single Boolean: is `"+++ b/app.py".startswith("+")` True or False. If True,
  the first branch of the current function claims every file header as an added source
  line and the `metadata` category is unreachable regardless of how many branches follow.
  That one fact is the whole reason arrangement matters. Reissue `EV-P1-META-044` only
  after this is stable.
- Evidence `EV-P1-PREFIX-046` was not answered directly. The learner instead diagnosed,
  correctly and unprompted, that the function only handles added and removed and that two
  of the four contract labels have no branch at all. The ordering consequence was not
  reached: adding a metadata branch below the single-plus branch leaves it unreachable.
- Evidence `EV-P1-ORDER-047` reframes the same idea using the learner's own implied fix
  as the subject — a four-branch function with `metadata` appended at the bottom — and
  asks what it returns for a real header line. This is a more honest test than the
  abstract Boolean and shares its deep structure with the already-passed grading
  exercise. Do not restructure `classify.py` until this is answered.
- Evidence `EV-P1-ORDER-047` is wrong and preserved as such. The learner predicted
  `metadata`; the running code printed `added`. `"+++ b/app.py".startswith("+")` is True,
  so the broader branch matched first and the metadata branch below it was unreachable
  for every possible input. This is the `branch_precedence` weakness recorded from the
  first Phase 1 prediction, now reproduced against executing code rather than on paper.
  The learner had previously stated this rule correctly in the abstract on
  `EV-P1-ELIF-029` but did not transfer it to string prefixes in the project's own code,
  which is exactly the surface-versus-deep-structure failure the curriculum predicts.
- Evidence `EV-P1-ORDER-048` asks the learner to state the required branch order and
  justify it. This is the Phase 1 target and must come from the learner, not from a
  generated implementation. `classify.py` remains at two branches until then.
- Evidence `EV-P1-ORDER-048` produced the correct order — metadata first, then added and
  removed, with context last as the fallback — and a correct description of the fallback's
  role. The justification was not stated, so the arrangement is produced but not yet
  defended. `branch_precedence` therefore stays open.
- New misconception `removed_line_vs_context_line`: the learner identified
  `-DEBUG = False` as a context line. It begins with a single dash and is a deleted source
  line; context lines are the unchanged ones, which Git prefixes with a single space. Real
  `git diff` output was displayed with each line's first character extracted so the space
  prefix could be observed rather than asserted.
- Resolved without a special case: the learner worried about detecting the empty line. An
  empty string satisfies none of the earlier conditions and reaches the fallback, which the
  approved contract already assigns to `context`. No emptiness check is needed. This also
  addresses the older `empty_input_classification` weakness.
- Evidence `EV-P1-META-049` closes out the metadata exercise: label all nine real diff
  lines, notice that two of them fit no category in the approved contract, and justify the
  ordering in one sentence. The `diff --git`, `index`, and `@@` lines are the first genuine
  gap in the contract and are the learner's to notice unprompted.
- Evidence `EV-P1-META-049` passed. Six of nine lines were labelled correctly, and the
  three the learner declined to label were exactly the three the contract does not cover,
  so the uncertainty was well calibrated: it found an underspecified contract rather than
  revealing a knowledge gap. Claude's prompt had said two such lines; the correct count is
  three, and that error was corrected in the same message.
- CONTRACT AMENDED by the learner. `metadata` now covers five prefixes: `diff --git`,
  `index`, `---`, `+++`, and `@@`. The learner's stated reason was to keep the counts as
  factually correct as possible rather than quietly convenient. This is the first design
  decision the learner has made and defended unprompted, and it supersedes the
  four-category contract approved earlier in the session.
- Stated assumption attached to that amendment, to be defended later: the classifier is
  correct only because every content line in a unified diff carries a prefix character, so
  a bare `index ...` can only be a Git header. If raw source text were ever fed to this
  function it would misclassify. Revisit when Git becomes a real external boundary in
  Phase 7.
- `branch_precedence` is now STATED AND DEFENDED, not merely produced. The open-form
  justification was requested three times without an answer, so the format was changed to
  selection among three candidate sentences; the learner chose correctly and reported a
  numeric confidence of 100. This is the first numeric confidence in Phase 1, so
  calibration tracking can finally begin.
- Format finding worth keeping: when an open-ended justification repeatedly fails to
  produce an answer, converting it to a selection among plausible candidates recovered the
  concept immediately. Prefer that over repeating the same open question.
- Four new tests written from the amended contract, covering a file header, a hunk marker,
  an unchanged context line, and the empty line. `classify.py` is deliberately unchanged so
  the red can be predicted first. Evidence `EV-P1-RED3-050` asks which call fails and how
  many failures are actually visible.
- Evidence `EV-P1-RED3-050` passed with correct reasoning: the file-header test fails
  first, and only that one failure is visible because the raised error ends the program
  while three further broken tests never run. `classify.py` was then restructured to the
  learner's stated order and all six tests are green.
- Deferred tooling decision now has a concrete justification forming: the hand-rolled test
  file reports one failure at a time. A runner would report all four at once. Add one when
  running tests by hand becomes the actual friction, not before.
- PROCESS DEVIATION to correct: the `or` operator was introduced by Claude inside the
  restructuring patch without first being predicted or explained, which skips the
  implementation-adjacent teaching loop required by CLAUDE.md. The learner subsequently
  called the compound condition a `switch`. Explain and test `or` before it appears in any
  further code.
- Evidence `EV-P1-TEACH-051` is the milestone teach-aloud and is partial. The control flow
  and the ordering rationale were explained correctly in the learner's own words. Three
  requested points were not answered: the input/output/unchanged contract, what `or` does,
  and one input the function still gets wrong. Those three were reissued.
- Active blocker: `KNOWN_LIMITATIONS_OF_OWN_CODE`. The learner defended the file by what it
  now handles rather than by what it still misses. A real defect exists for input Git
  genuinely produces, and the learner must locate it before the milestone closes.
- Support is now fully faded at the learner's explicit request: questions only, no hints,
  no leading commentary. Maintain this unless an answer shows it was withdrawn too early.
- Evidence `EV-P1-BUG-052` completed the outstanding teach-aloud points. `or` was described
  correctly in effect; input and output were stated correctly; the unchanged half of the
  contract was omitted a third time and remains a retrieval target rather than a lost
  concept. The learner could not name a remaining defect unaided, said so plainly, and then
  correctly identified both the wrong answer and the right one once given a concrete
  scenario.
- New weak concept `diff_prefix_character_count`: the learner wrote two dashes where Git
  emits four. This is the same run-length counting error behind the earlier two-character
  and four-character header guesses, and it is now tracked separately from
  `unified_diff_metadata_meaning` because it is a counting problem, not a meaning problem.
- The `----` defect is FIXED. The learner chose to tighten the rule rather than accept the
  limitation, and derived the rule unaided from four contrasting strings with support fully
  faded: a Git file header carries a space after its three markers, so `"--- "` and
  `"+++ "` separate headers from deleted or added content. Evidence `EV-P1-RULE-053`. This
  is the first classification rule the learner has derived rather than predicted. Seven
  tests green.
- ACCEPTED LIMITATION, evidence `EV-P1-LIMIT-054`. Deleting a line whose content is
  `-- notes` produces `--- notes`, which is character-for-character identical to a real
  file header, and the classifier labels it `metadata`. No rule examining only that line
  can resolve it. Disambiguation needs positional context: headers precede the first hunk
  marker and appear as a `---`/`+++` pair. The approved contract supplies one line and no
  context, so this is a limit of the contract, not of the implementation. It is the first
  requirement a pure single-value transformation cannot satisfy, and it is the concrete
  motivation for Phase 2 representation and Phase 3 state. When it is revisited, ask the
  learner what additional information would resolve it before writing anything.
- MILESTONE PAUSE per CLAUDE.md. Automated tests, learner trace, and learner explanation
  are satisfied for the first behavior. The sync-blocking inconsistency is now resolved:
  the evidence above records the defect as fixed, matching the local source and test files.
  Evidence through `EV-P1-BUG-052` was included in the last public checkpoint sync;
  `EV-P1-RULE-053` through `EV-P1-TRANSFER-055` are not yet synced.
  Outstanding before Phase 1 closes: evidence `EV-P1-TRANSFER-055`, a chat client labelling
  messages by `//` and `/` prefixes, including one part asking for an input that no ordering
  can rescue. That part tests whether the accepted limitation has been generalized rather
  than memorized as a dash case. Do not begin Phase 2 automatically.
- Evidence `EV-P1-TRANSFER-055` is partial. Parts 1 and 2 were answered correctly without
  hints in an unfamiliar domain, which demonstrates that `branch_precedence` has
  transferred away from diffs: testing the single slash first mislabels a double-slash
  message as a command, and the required order is double slash, single slash, fallback.
  Part 3 is not established. The learner nominated `///`, which this scheme actually
  handles correctly, and did not say why ordering cannot help. Part 3 was reframed rather
  than answered and remains open.
- CALIBRATION is now informative and should be tracked from here. Two honest data points
  exist: `100` on the branch-order selection, which was correct, and `low confidence` on
  the transfer variant, which was weak on exactly the part the learner was unsure about.
  The long-standing note that calibration cannot be computed is now obsolete.
- Phase 1 does not close until part 3 is answered. The target is that the learner can state
  a case no ordering can rescue and say why: the required label depends on information that
  is not present in the input the contract supplies.
- Evidence `EV-P1-TRANSFER-056` is recorded as ASSISTED and does not count toward the gate.
  The learner named the correct case, a plain-text message beginning with a slash, and then
  disclosed unprompted that the answer had been surfaced to them by a client-side preview
  or suggestion feature before they committed. The disclosure is recorded as a credit: the
  ledger is only worth keeping if attempts are reported honestly, and the learner protected
  its integrity at their own cost.
- Prompt defect to avoid repeating: Claude's reframing of part 3 narrowed toward a single
  phrase, which made the answer easy for a predictive feature to complete. Do not funnel
  questions toward one specific wording; ask openly enough that only understanding
  produces the answer.
- Claude cannot disable client-side preview or suggestion features from within the session
  and said so plainly. If the learner can describe what appeared and where, it may be
  identifiable; Claude Code's own settings require an interactive session.
- Evidence `EV-P1-TRANSFER-057` reissues the limitation transfer in a third domain: a
  spreadsheet that treats a leading `=` as a formula. It uses only two rules, so ordering is
  visibly not the issue, and it is phrased without funnelling.
- Evidence `EV-P1-TRANSFER-057` was answered incorrectly: both proposals named inputs the
  rule already handles correctly. Low confidence was reported and the answer was wrong,
  which is the third consecutive accurate calibration point.
- Evidence `EV-P1-TRANSFER-058` descended to one concrete cell and, after a worked-example
  rescue, reached the target. The learner did not know the leading-apostrophe convention and
  said so; it was supplied as a tool fact, and the learner then produced the reasoning:
  an escape marker is needed when a value begins with the marker character but the user
  does not want it interpreted. The phrase `you dont want it to run` is the concept, since
  intent is exactly what the characters cannot carry.
- Recorded as CORRECT WITH SCAFFOLDING, not as an independent transfer. Under
  LEARNING_RULES 14.6 a worked example must be followed by a fresh example solved unaided
  before the concept counts as transferred. A delayed unaided variant of
  `INFORMATION_NOT_PRESENT_IN_THE_INPUT` is DUE, in a fourth domain, after a gap.
- The learner also observed unprompted that spreadsheets show the formula when a cell is
  selected. That is a genuine and relevant observation: the interpretation lives outside the
  displayed value, which is the same shape as Git keeping header identity in position rather
  than in the line.
- Two prompt-wording defects were corrected this session at the learner's insistence, both
  recorded because they caused reasonable wrong inferences: quoting a fragment instead of
  a whole file, and writing `more than one line comes back wrong` when the intended
  meaning was that the function returns the wrong label for more than one line. Phrase
  questions so the code, not the input data, is the thing under suspicion.
- Evidence `EV-P1-META-044` is issued at R6 against real `git diff` output. It revisits
  `branch_precedence`, `unified_diff_metadata_meaning`, and `empty_input_classification`
  simultaneously and requires a design justification for branch arrangement rather than a
  code change. Do not reorder `classify.py` until the learner has committed an answer.
- Confidence has now been omitted on five consecutive attempts, so calibration still
  cannot be computed. Keep requesting a number.
- Milestone reached: first behavior implemented. Automated test and learner trace are
  satisfied. Still outstanding for this milestone are a learner explanation of
  `classify.py` taught aloud and one transfer variant. The earlier sync note through
  `EV-P1-GAP-038` is superseded by the current checkpoint through `EV-P1-BUG-052`.
- Environment limitation found: `python-test-runner` is bind-mounted to
  `Trellis_AI_Agent_HistoryTool/backend` and cannot see BuildLens files. The first test
  was therefore run locally on Python 3.14.6. Wiring a BuildLens-mounted container is
  available on request and is not required by Phase 1.
- A second environment note: at the learner's request a dedicated
  `postgres-test-runner` container (`postgres:16`, port 5433, db `testdb`) was created
  fresh rather than renaming Trellis's Compose-managed database. Trellis remains on
  port 55432 and was not modified. BuildLens still requires no database until Phase 11.
- Environment note. At the learner's request the container `trellis-t19-test`
  (`python:3.12`) was renamed to `python-test-runner`. The postgres container was NOT
  renamed: `trellis-ai-agent-postgres-1` is Docker Compose managed and healthy, so a
  direct rename would detach it from Compose and risk a duplicate database for Trellis.
  Renaming the service inside Trellis's compose file is the correct route and is a
  Trellis change, not a BuildLens one. Phase 1 requires neither container; BuildLens
  does not reach persistence until Phase 11.

## Files I should be able to teach

- `classify.py` — the four-branch classifier: its contract, why the metadata prefixes are
  tested first, what `or` contributes to the first condition, and what it still gets wrong.
- `test_classify.py` — the import bridge, six assertions, and why only one failure is
  visible per run.

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

## Phase 2 — opening state

Phase 1 closed with `classify.py` and `test_classify.py` synced to public `main` at commit
`e419b0c`, seven tests green.

Phase 2 begins at MEDIUM assistance per the implementation plan: Claude asks what the data
model should contain rather than defining it. No Phase 2 code exists.

Carried into Phase 2:

- DELAYED RETRIEVAL DUE: one unaided variant of `INFORMATION_NOT_PRESENT_IN_THE_INPUT` in a
  fourth domain, after a gap. `EV-P1-TRANSFER-058` reached the concept only with a
  worked-example rescue, so it does not yet count as transferred.
- The accepted limitation `EV-P1-LIMIT-054` is the concrete motivation for this phase: a
  single line cannot carry positional meaning, so a representation richer than one string
  is now justified rather than assumed.
- Prerequisites the learner has NOT yet met: lists, iteration, and any form of loop. These
  are required to summarize a whole diff and must be introduced through the
  implementation-adjacent loop, not assumed.
- Process rules now standing: show whole files, never a fragment; never print output without
  the code that produced it; settle tool-behavior questions by generating real output rather
  than asserting; do not funnel questions toward a single wording; support stays faded to
  questions only unless an answer shows it was withdrawn too early.

Evidence `EV-P2-MODEL-059` is issued: the learner specifies what BuildLens should report
about a real nine-line diff, names each value, and identifies anything the per-line
classifier cannot supply. Do not define the data model for the learner and do not write
code until the specification is committed.

Evidence `EV-P2-MODEL-059` is partial, and the important half is correct. The learner named
the model's shape unprompted — files changed, lines added, lines removed — which matches the
fields sketched in the implementation plan without having seen them. Two corrections: the
figures were computed from the sync commit rather than from the `app.py` diff in the prompt,
a reading-target error that does not affect the shape; and `a git diff summary` names the
record rather than its three values, which remain unnamed.

Part 3 named continuous integration, which is not derivable from diff text. Evidence
`EV-P2-MODEL-060` reframes it concretely: given a diff touching two files, can a per-line
label say which file an added line belongs to. This is a second, independent instance of
`INFORMATION_NOT_PRESENT_IN_THE_INPUT` arising from the project itself rather than from a
constructed analogy. If the learner reaches it unaided, it counts toward the delayed
retrieval carried over from Phase 1.

Evidence `EV-P2-MODEL-060` is partial. New misconception `diff_a_b_prefixes_are_two_files`:
the learner read `a/app.py` and `b/app.py` as two separate files. They are one file shown
before and after, and this is the most common misreading of unified diff output. It was
corrected by labelling the diff line by line with the learner's own classifier, which also
showed that five of the nine lines are Git describing one file rather than changing it. The
learner then produced the correct counts unaided: one file changed, two lines added, one
removed.

Also corrected: Git records `DEBUG = False` becoming `DEBUG = True` as one removal plus one
addition, because it has no concept of a changed line.

Candidate field noted, not accepted: the learner proposed reporting the changed line numbers,
having spotted that the information lives in the `@@` hunk marker. That is a real observation
about the data rather than an invention. It carries a cost, since extracting it means reading
numbers from the middle of a string rather than testing how a line starts, so it stays a
deliberate decision rather than a free addition.

Prompt defect, the third this project: the request for field NAMES was not distinguished from
the request for VALUES, and the learner reported the question unintelligible. It was reissued
with a non-diff contrast between the values `4` and `2500` and the names `doors` and
`weight_lbs`. When asking for a name, show an example of a name in a domain that cannot leak
the answer.

Evidence `EV-P2-COUNT-061` descends to R1: given a four-row label tally and the three known
numbers, match each number to its label. `lines_added` and `lines_removed` are direct label
counts; `files_changed` is not, because one file produces five metadata lines. That asymmetry
is what will force a richer representation, and it is the same shape as the positional gap in
part 3 of `EV-P2-MODEL-060`, which remains unanswered.

DESIGN DECISION by the learner, evidence `EV-P2-COUNT-061`: Option A. `classify_diff_line`
gains a fifth label, `file_header`, returned for lines beginning `diff --git`. The remaining
four metadata prefixes keep the `metadata` label. All three summary values then derive from
one tally of labels — `file_header`, `added`, `removed` — so the knowledge that `diff --git`
marks a file lives only in the classifier and is not duplicated in the counting code. The
rejected Option B left the classifier untouched and gave the counting code its own prefix
test.

Fields deliberately EXCLUDED, and the reasoning is the learner's: counts of metadata and
context lines do not earn a place, because metadata only identifies the file before and after,
which the file count already conveys, and context lines are unchanged code. Cutting a field
for want of a named reader is the design-review standard and the learner applied it unprompted.

New concept `hunk_vs_file`, corrected by observation: the learner believed `@@` appears once
per file. A one-file two-hunk diff was generated showing one `diff --git` line and two `@@`
lines. `@@` marks a hunk, a contiguous neighbourhood of change, and one file may contain many.
`diff --git` is the only line guaranteed to appear exactly once per file. This also prices the
learner's earlier changed-line-number proposal: those numbers live in `@@`, so they form a
list per file rather than a single value.

The learner found the label asymmetry unaided — `added` and `removed` match tally entries
while `files_changed` has none — and proposed the label that became the adopted design.

Outstanding: the learner has not yet given `files_changed`, `lines_added`, and `lines_removed`
for the two-file diff. Those counts are the specification the first Phase 2 tests will be
written from and must come from the learner. No Phase 2 code exists.

PHASE 2 KNOWLEDGE GATE PASSED, evidence `EV-P2-CASES-063`. The learner specified all four
cases before any test was shown, which is what the gate requires:

```text
two-file diff   files_changed 2, lines_added 3, lines_removed 2
empty input     0, 0, 0
new file        files_changed 1, lines_added 2, lines_removed 0
shopping list   0, 0, 0, no error raised
```

NAME SETTLED by the learner after considering three candidates: `DiffSummary`, holding
`files_changed`, `lines_added`, `lines_removed`. `QuickGitDiff` was rejected because the record
contains no diff text, and `Git` was dropped as redundant in a project where everything is a
git diff. Python casing was introduced here: CapWords for a type, lower_snake_case for values
and functions.

ACCEPTED TRADE, and the learner should be able to defend it: non-diff input produces zeros
rather than an error, so nothing and nonsense are indistinguishable in the output. The learner
proposed an error, then withdrew it once the cost was visible — detecting a non-diff means
first writing down what a valid diff is, while the existing classifier already labels every
shopping-list line as context. Validation is the natural subject of Phase 5.

New concept `hunk_numbers_are_changes_not_coordinates`, corrected: the learner first read the
`@@` numbers as identifying added and removed lines. They are `start,count` per side, minus for
the old file and plus for the new. The learner then read an unseen header correctly and
inferred the net length change unprompted. Precision point supplied: a length change gives the
NET difference, not the added count, which is why the summary counts content lines rather than
doing hunk arithmetic.

NEXT, and not yet started: `classify_diff_line` gains the `file_header` label, then lists and
iteration are introduced through the implementation-adjacent loop, since the learner has met
neither. Only then is the summary function built, test-first, from the four cases above.

RISK RAISED BY THE LEARNER, and it changed the analysis. The learner challenged the invalid
input case, arguing that Claude Code would never hand BuildLens nonsense. That is correct: a
shopping list never arrives. Real git output of an unexpected SHAPE does. Three cases were
generated and run through the current classifier:

```text
binary file changed   files=1 added=0 removed=0   honest
file renamed          files=1 added=0 removed=0   defensible, rename is invisible
git command failed    files=0 added=0 removed=0   DANGEROUS
```

The third is the hazard. When BuildLens runs git as a subprocess in Phase 7 and the command
fails, stderr text such as `fatal: not a git repository` is classified entirely as context and
summarizes to zeros. BuildLens would then report `Claude changed nothing` when the truth is
`we failed to look`. Those are opposite statements and the reader cannot distinguish them.

This does not require solving in Phase 2. It MUST be resolved before or during Phase 7, when
the Git boundary is built, and the likely mechanism is the subprocess exit status rather than
anything in the text. Record the resolution as an explicit decision rather than letting the
zeros stand by default.

Also noted: renames and binary changes are currently invisible in the summary. Neither is a
defect against the agreed specification; both are consequences of a model built from line
counts, and the learner should be able to say so when defending it.


## Phase 2 — session of 2026-08-26, second sitting

DELAYED RETRIEVAL SATISFIED, evidence `EV-P2-POSITION-064-CLOSE`. The unaided variant of
`INFORMATION_NOT_PRESENT_IN_THE_INPUT` owed since `EV-P1-TRANSFER-058` is now banked in a
fourth domain. Asked whether the label `"added"` returned for `+RETRIES = 5` can say the line
came from `config.py`, the learner answered no and named the mechanism unaided: you would have
to look at the `diff --git` above it. That is positional context the single-line contract does
not supply. The concept now has its third variant across two contexts plus one delayed
retrieval; it moves toward MASTERED once the learner defends it in the oral-defence format.

CALIBRATION IS NOW LIVE. The first two confidence numbers in the project were recorded this
sitting, after roughly eight consecutive omissions. The scale was confirmed as out of 100.

```text
EV-P2-SYNTAX-066        8/100   correct    large underconfidence
EV-P2-POSITION-064-CLOSE 80/100  correct    well calibrated
```

Watch whether low numbers cluster on syntax questions specifically. Keep asking every time;
the learner still does not volunteer them.

New remediation chain closed, `EV-P2-SYNTAX-065` and `EV-P2-SYNTAX-066`. Blocker
`SYNTAX_READING` on string-literal quotes, surfaced when the learner wrote `would it not be
able to return anything because of the ""`. The diff problem was stopped and the syntax
isolated at R0 per LEARNING_RULES 14.3. The learner predicted `added` and `5` correctly and
explained that the quotes are not part of the value. A near-transfer with single quotes was
also correct, and the learner reached the nesting rule unaided after `marker == "diff --git"`
was run and printed `True`. `'` and `"` are now known to be a style choice, not a semantic one.

Process note that worked and should continue: part 2 of the near-transfer was answered `idk`
and was settled by generating real output rather than by asserting the answer.

NEXT, unchanged and not yet started: `classify_diff_line` gains the `file_header` label,
test-first. Then lists and iteration through the implementation-adjacent loop. Then the
summary function from the four cases in `EV-P2-CASES-063`.

LEARNER HYPOTHESIS, offered unprompted on 2026-08-26 and to be tested rather than assumed:

> "syntax is more of a struggle for me than logic"

The first two calibration points are consistent with it — 8/100 on a quote-syntax question,
80/100 on a design question, both answers correct. Two points establish nothing. Tag each
future confidence number as SYNTAX or DESIGN so the claim can be checked against evidence
rather than impression. If it holds, the consequence is concrete: syntax gets isolated at R0
on sight, while design questions should be issued at full difficulty without scaffolding.

## Phase 2 — step 1 complete

`classify_diff_line` now has five labels. `diff --git` returns `file_header` from its own
leading branch; the other four metadata prefixes moved into an `elif` and keep `metadata`.
Eight tests green, `python test_classify.py` prints `test passed`, exit code 0.

The branch was placed first for READABILITY, not correctness. The learner verified that none
of the six remaining conditions match a `diff --git` line, so its position is free. The rule,
in the learner's words: order matters when "there is a part of it that is included in the
other". This retires `branch_precedence`, open since Phase 1, as a stated rule rather than a
memorised instance.

New misconceptions this sitting:

- `branch_order_mirrors_input_order` — branch order justified by where the line appears in the
  diff file. Dislodged by quoting the learner's own EV-P2-POSITION-064-CLOSE conclusion back.
- `output_and_exit_status_are_independent` — a printed success paired with exit code 1, twice.
  The learner stated the correct rule when asked directly, then reverted on the next
  prediction, so the rule is available but not yet driving the trace. Expect this one again.

CALIBRATION, five points, all on CORRECT answers:

```text
8/100   SYNTAX    correct
80/100  DESIGN    correct
70/100  DESIGN    correct
50/100  mixed     correct
20/100  TRACING   correct
```

The learner's syntax-versus-logic hypothesis does NOT fit this data. Revised working
hypothesis, to be tested rather than assumed: the learner rates how supported the path felt
rather than whether the reasoning held. Both 20 and 30 followed an admission of being unsure
and preceded error-free sequences.

TWO PROMPT DEFECTS, mine, fourth and fifth in the project:

- a prediction was requested against a previous run the learner had to recall rather than see,
  violating the standing show-whole-files rule. The learner asked for the code, correctly.
- a four-blank two-row table was issued immediately after a 30 confidence and produced
  `im not sure`. After a low confidence, reduce the number of blanks rather than increasing
  structure. One branch test per question recovered it in four exchanges.

UNPROMPTED LEARNER CONTRIBUTION, not built and out of scope: once a line is classified
`file_header`, every later line belongs to that file until the next `file_header`. That is the
caller-held-state answer to the positional gap and is the design for a per-file breakdown when
one is wanted.

MILESTONE PAUSE IS ACTIVE per CLAUDE.md. Automated tests and learner trace are satisfied.
Still owed before Phase 2 continues: the learner teaching `classify.py` aloud, and one transfer
variant. Do not begin lists and iteration until both are done.

### Standing retrieval commitment — do not drop

`output_and_exit_status_are_independent` is NOT settled and is scheduled for re-testing.

Evidence: in `EV-P2-GREEN-069` the learner twice predicted that `test passed` would print AND
the exit code would be 1. Asked directly whether both could happen, they answered correctly —
"no assertion error will not run" — and then produced the same inconsistent pairing on the very
next prediction. A rule that can be stated on demand but does not govern the next trace is not
yet knowledge.

Re-test in a DIFFERENT surface form, not another run of `test_classify.py`. Candidates:

- a script that prints, then raises, with the print BEFORE the failure rather than after;
- a script that prints and exits 0 while reporting a logical failure in its text;
- a command that writes to stderr and still exits 0.

The third is the one that matters most, because it is the Phase 7 git hazard in miniature: text
and exit status are separate channels, and the whole `fatal: not a git repository` problem
exists because BuildLens would read the text and ignore the status. Settling this concept is a
prerequisite for the learner making that Phase 7 decision on their own evidence.

Do not announce the re-test in advance.

## Phase 2 — step 1 MILESTONE CLOSED

All four requirements met, evidence `EV-P2-GREEN-069`, `EV-P2-TEACH-070`, `EV-P2-TRANSFER-071`.

```text
automated tests      eight green, exit 0
learner trace        predicted the run before it ran
learner explanation  taught classify.py, defended three limitations
transfer variant     unseen domain, found the dead branch, stated the rule generally
```

`branch_precedence` now has three unseen correct variants across two contexts plus a correct
general explanation. One DELAYED RETRIEVAL remains before it can be marked MASTERED — schedule
it after a gap, in a domain that is neither diffs nor letter codes.

Corrected during the explanation: the learner opened by saying the function "looks at each line
in the git diff". One question fixed it at 90 confidence, and they volunteered the caller-side
iteration unprompted. Left uncorrected on purpose: `startswith` was called a function rather
than a method. Not worth interrupting the explanation for; raise it when methods matter.

Confirmed limitations the learner can now name and defend: `--- notes` as prose is
indistinguishable from a header; no line can say which file it belongs to; a rename with no
content edit is invisible. Correctly rejected as NOT a limitation: counting files, which is
exactly what this patch bought.

CALIBRATION, nine points, every underlying answer correct:

```text
8/100   SYNTAX    correct
80/100  DESIGN    correct
70/100  DESIGN    correct
50/100  mixed     correct
20/100  TRACING   correct
90/100  DESIGN    correct
60/100  DESIGN    correct
90/100  DESIGN    correct
90/100  TRANSFER  correct
```

Nine for nine. The syntax-versus-logic hypothesis does not fit. The revised hypothesis does:
the low numbers cluster where the learner had been walked through the path, the high numbers
where they moved unaided. The learner is measuring how much help arrived, not whether the
reasoning was sound.

New tracked pattern `credits_examiner_for_own_conclusion`, three occurrences this sitting. The
learner wrote "your are right" in response to a question that asserted nothing. Combined with
the underconfidence, the practical cost is that a wrong correction from Claude would likely be
accepted. Worth testing directly at some point with a confidently stated wrong claim.

NEXT: lists and iteration, which the learner has never used. The learner has already described
what iteration must do — call the classifier once per line until the diff ends, and hold the
last `file_header` seen — so the concept is motivated and does not need justifying. Do not
write a loop in front of them before they have predicted what one does.

## Phase 2 — rename done

`test_file_header_is_metadata` is now `test_plus_file_marker_is_metadata`, renamed at both its
definition and its call. Suite output unchanged: `test passed`, exit code 0. `file_header` now
means exactly one thing across the codebase. Name chosen by the learner after rejecting `line`
as insufficiently distinguishing.

New misconception `missing_name_vs_failed_assertion`, evidence `EV-P2-RENAME-072`: a
half-finished rename was predicted to raise an AssertionError. It raises `NameError` at the
call site and the assert never runs — nothing is tested at all. Demonstrated by executing a
half-renamed copy rather than describing it.

This is adjacent to the standing `output_and_exit_status_are_independent` commitment and was
raised without announcing it as the re-test. Both failures exit 1, so the exit code alone
cannot separate "checked and disagreed" from "never checked". The scheduled re-test is still
owed, still unannounced.

Deferred with reasons, not forgotten:

- Phase 7 git-failure decision — Phase 2 does not run git; deciding it now means deciding it
  without the subprocess present.
- `.gitignore` — near-worthless while syncing copies three named files into a fresh clone;
  `__pycache__` has no path into the repo. Becomes real only if the workspace gains its own
  `.git`.
- `branch_precedence` delayed retrieval — requires a gap to mean anything.

NEXT: lists and iteration. Still never used by the learner.

## Phase 2 — learner-initiated: execution order

Evidence `EV-P2-EXEC-073`. The learner asked unprompted how `test_classify.py` runs, reporting
that `classify.py` reads easily but the test file does not. They predicted `A C B D` correctly
first time on a six-line example and applied it to the real file unaided: a `def` binds a name
without running the body, and nothing is tested until the calls at the bottom execute.

The reported difficulty was VOLUME, not concept. Eight definitions of near-identical shape read
as a wall. The learner found the structure when asked: three lines each, identical shape, two
varying parts. Record this as a reading strategy, not a Python gap.

Second learner-initiated question and the better one: where the tested line comes from. Answer
given correctly — typed by hand. This retires the neighbourhood of the Phase 1 misconception
`data_vs_external_resource`.

Stated unaided, and it is the honest reading of a green suite: eight passing tests prove only
the cases someone chose to write. This is exactly why `--- notes` and the failed-git case go
undetected — no test exists that would turn red.

Note for the next sitting: the learner is now asking their own questions about the code rather
than only answering. Two of the three best moments this session came from their questions, not
from issued exercises. Leave room for that.

## Phase 2 — lists and iteration, GATE PASSED

Evidence `EV-P2-LIST-074`. The learner predicted an unseen `for` loop's output — three lines,
`added removed context` — before it was run. That is the Phase 2 requirement and the standing
rule that no loop is written in front of them unpredicted was honoured.

Now known, none of it previously met:

```text
a list holds many values in order under one name
len counts items in a list, characters in a string
labels[1] selects one item by position
for NAME in LIST: creates NAME and binds each item in turn
the loop variable's name is chosen by the author
indexing selects one; iteration visits all
```

UNPROMPTED: asked to print three labels using only what they already knew, the learner invented
indexing without having seen it. They also worked out the arbitrary loop-variable name from a
single `for banana in labels` example and raised it as a question before being told.

Three misconceptions surfaced and resolved, all by generated output rather than assertion:

- `nested_call_evaluation` — `print(len(labels[0]))` was expected to print words. Resolved by
  evaluating inside-out; confirmed as 5, 7, 7.
- `print_list_vs_iterate` — `print(labels)` was expected to show the first slot. It shows the
  container, brackets and all, on one line.
- `loop_vs_index` — a loop was defined as the tool for reaching a numbered slot. Resolved by
  asking the learner to make the loop print only `"removed"`; they correctly answered that it
  cannot.

Calibration continues to be sound. 90 on a correct list-length answer, 40 on the one wrong
answer of the sequence. The earlier underconfidence pattern did not repeat here.

NEXT, and deliberately not started: accumulation. Counting labels across a loop requires a
running total that survives between passes, which is a genuinely new idea and must not be
folded into the same sitting as the loop itself. After that, the summary function can be built
test-first from the four cases in `EV-P2-CASES-063`.

## Phase 2 — accumulation and the string-to-lines boundary

Evidence `EV-P2-ACC-075`. Four accumulator predictions correct at 100 confidence, including the
reset-inside-the-loop variant that yields 1 instead of 3. The learner identified unaided that a
counter initialised inside the loop is wiped every pass.

Also established: looping a string yields characters, not lines — the learner inferred this
unaided and was off only by not counting the space. `\n` is one character; `len("alpha\nbeta")`
predicted correctly as 10. `splitlines()` converts one string into a list of lines.

The complete pipeline, stated by the learner in their own words before it was written down:

```text
one diff string
  -> splitlines()
  -> for line in lines
  -> classify_diff_line
  -> compare the label
  -> bump one of three counters
  -> three numbers
```

STOP POINT, and this is a deliberate judgement rather than fatigue. Seven new syntax forms
landed in one sitting: list literal, indexing, `for`, the loop variable, the accumulator update,
`\n`, and `splitlines`. Building the summary function immediately would rest the first real
Phase 2 code on concepts hours old with no retrieval behind them.

REQUIRED BEFORE THE SUMMARY FUNCTION IS WRITTEN:

- one delayed retrieval on the accumulator, especially the reset-placement distinction;
- one delayed retrieval on `splitlines` versus looping a raw string;
- both in surface forms that are not label counting.

Prompt-reading note, and it was Claude's risk rather than the learner's error: the phrase
`afterwards it goes back to zero for the next interation` had two opposite readings. It was
disambiguated by asking rather than assumed. Keep doing that; three of this project's recorded
defects came from not doing it.

## Phase 2 — delayed retrievals, split result

Evidence `EV-P2-RETR-076`, taken after a genuine session gap.

```text
accumulator reset placement   RETRIEVED, unaided, 90 confidence, correct
splitlines                    NOT RETRIEVED, learner asked what it does
```

The accumulator retrieval counts. It used a summing form, `total + p` rather than `total + 1`,
which is a real variation rather than the same problem renumbered, and the reset-inside case was
answered correctly again.

`splitlines` failed and is recorded as re-learned, not banked. One more unaided attempt after a
gap is owed. The scheduling decision was vindicated: building on it yesterday would have
surfaced this gap inside the summary function rather than in a two-line example.

`nested_call_evaluation` recurred, second occurrence. Asked for the output of two lines that
both wrap a result in `len`, the learner reported the innermost value instead of evaluating
outward. It did not recur once the lines were described in terms of what each counts. Watch it.

REVISED PLAN, and it keeps the patch to one new idea: the summary function can be built against
a LIST OF LINES first, with the string boundary and `splitlines` added afterwards as a separate
step. That way the unretained concept is not load-bearing while the first Phase 2 code is
written, and `splitlines` gets its unaided retrieval when it is actually needed.

## Phase 2 — first working summary code

`summarize.py` exists. One function, every line of it specified by the learner:

```python
def count_added_lines(all_lines):
    count = 0
    for line in all_lines:
        if classify_diff_line(line) == "added":
            count = count + 1
    return count
```

`test_summarize.py` holds the seventeen-line two-file diff as a constant and asserts 3.
Both suites green, exit 0. Evidence `EV-P2-COUNT-077`.

The learner proposed the whole design unprompted — classify the line, compare the label, bump a
counter — and needed three corrections, all reached by question rather than statement:

- `loop_outside_vs_inside` — the loop was drafted OUTSIDE, calling the function once per line.
  Fixed by pointing at the test, which calls it once with all seventeen.
- `code_after_return` — `count = 0` placed after `return count`. Dislodged by quoting the
  learner's own sentence from `EV-P2-TDD-067`.
- `locals_persist_between_calls` — the reset was wanted because `count` was thought to survive.
  Settled by calling a function twice: 2 and 2, not 2 and 4.

FIRST MODULE-BOUNDARY DECISION, and it is the learner's. Asked whether the function belonged in
`classify.py`, they said `how do i even think about that?`. Given one heuristic — write a single
sentence covering both functions and watch for an "and" — they wrote `classify a single line of
diff text while counting the added lines`, saw the bolt-on, and chose a new file. `summarize.py`,
job: count what a whole diff changed. That sentence still holds for the two counters to come.

Error taxonomy now has three members, all exiting non-zero:

```text
ModuleNotFoundError   the file is not there
NameError             the file is there, the name inside it is not
AssertionError        both are there, the value is wrong
```

## Phase 2 — exit status, root cause found

Evidence `EV-P2-EXIT-078`. The scheduled unannounced re-test arrived naturally and the learner
predicted `it passes and exit 1` for a third time.

Descending twice found the actual cause, and it was not carelessness. Asked what an exit code
IS, the learner answered `i have no idea`. The number had never had a referent, so pairing it
with a pass was never a contradiction. Every prior correct statement of the rule was recall
without meaning.

METHOD NOTE FOR CLAUDE, and it is the most useful thing in this sitting: when a learner can
state a rule and then immediately contradict it, suspect a missing referent before suspecting
carelessness. Two earlier re-tests of this rule failed to ask whether the term was understood.
Ask what a term means before re-testing a rule built on it.

Resolved by running two scripts that both print `hello`, one exiting 0 and one raising after the
print and exiting 1. Text cannot distinguish them; the number can. The learner then predicted a
fresh case correctly at 80 and stated the rule in their own words.

DIRECT CONSEQUENCE for Phase 7, and the learner now has the concept to decide it themselves:
when git fails it prints `fatal: not a git repository` and exits non-zero. The classifier labels
that text as context and summarises to zeros; the exit status reports the failure independently.
That is precisely the information the learner said the text does not carry.

One delayed unaided retrieval on exit status is now DUE, in a form that is not a Python test
run — ideally a real command writing to stderr. Do not announce it.

## Phase 2 — what remains

```text
count_removed_lines    same shape as count_added_lines, should be quick
count_changed_files    same shape, counts "file_header"
three values at once   GENUINELY NEW, must be its own patch
splitlines boundary    unaided retrieval still owed, then wire string -> list
```

Still open from earlier: `.gitignore` (low value), the `branch_precedence` delayed retrieval
(needs a longer gap), and the Phase 7 decision itself, which is now much closer to decidable.

PROMPT DEFECTS, seventh and eighth, both the same shape and both recorded because the learner
had to ask: predictions were requested against code the learner could not see — once an input
they were asked to invent from nothing, once a file created through a tool call and never shown.
The standing rule is whole files, every time, including files Claude has just written.

## Phase 2 — all three counts exist

`summarize.py` now has `count_added_lines`, `count_removed_lines`, and `count_changed_files`.
Every value from the Phase 2 gate specification `EV-P2-CASES-063` now computes from the real
seventeen-line diff: 3 added, 2 removed, 2 files. Ten tests green across both files, exit 0.

Evidence `EV-P2-REPEAT-079`. Support was faded deliberately — the learner supplied both expected
values and both function bodies in one pass, no step-by-step. Parts 3 and 4 were correct first
time: only the function name and the compared label change.

Two things worth keeping:

- The learner again filled a test slot with a description rather than a value, second occurrence
  after `EV-P2-TDD-067`. Asked directly for numbers, they gave 2 and 2 correctly. When asking for
  an expected value, ask for the NUMBER, not what the function returns.
- Caught before it bit: the label was written `"file header"` with a space. The real label is
  `"file_header"`. Comparison is exact, so that would have produced a silent zero with every
  other test still green. The learner was shown the branch and typed the string themselves.

Error taxonomy now has four members, all exiting non-zero:

```text
ModuleNotFoundError   the file is not there
ImportError           the file is there, the name is not, caught at the import line
NameError             the name is not there, caught where it is used
AssertionError        everything exists, the value is wrong
```

`ImportError` was met for the first time here. The learner predicted `NameError`, which is the
correct inference from the three-member taxonomy they had; the distinction is where the failure
is caught, not what is missing.

## Phase 2 — the learner proposed the consolidation

Evidence `EV-P2-DRY-080`. Shown the three stacked functions and asked how many of the eighteen
lines actually differ, the learner proposed the target design unprompted:

> one function, called once, that loops the diff, looks for all three findings with three
> separate counters, and returns the three counts

This is the second time they have identified repetition without being led to it — the first was
their own complaint about the eight near-identical tests in `test_classify.py`.

They named the requirement, returning three counts, without knowing the mechanism. Returning
more than one value is the ONLY genuinely new idea left in Phase 2 and gets its own patch.

Ninth prompt defect, same family as the seventh and eighth: `what do you notice` produced `what
am i looking for?`. Open noticing questions do not work here; a concrete count of what differs
worked immediately. Ask for something countable.

## Phase 2 — what remains

```text
one function returning three values   NEW IDEA, next patch, design already the learner's
splitlines boundary                   unaided retrieval owed, then string -> list
exit status retrieval                 owed, unannounced, not a Python test run
branch_precedence retrieval           owed, needs a longer gap
```

## Phase 2 — DiffSummary chosen and defended

Evidence `EV-P2-RECORD-081`. The learner chose Option B, a `DiffSummary` record, over a plain
tuple, and defended it under challenge.

```text
positional access   you get the value by knowing WHERE it is    tuple
named access        you get the value by knowing WHAT it is     attribute on an instance
```

The decision arrived before the reasoning — `I like B but i ma not totaly sure why`. Both
failure cases were then generated rather than argued:

```text
Option A, wrong order        printed 2 under the name "added", exit 0, nobody finds out
Option B, misspelled field   AttributeError, named the mistake, suggested the fix, exit 1
```

A is dangerous BECAUSE it succeeded. Same shape as the learner's own git-failure hazard.

One claim in the learner's explanation was false and they caught it themselves before it ran:
they said a dataclass can be unpacked by position as well as by name. It cannot —
`files, added, removed = summary` raises TypeError. Recorded as `dataclass_is_unpackable`,
resolved immediately. The falsification strengthened the argument: Option B does not add named
access alongside positional, it REMOVES position as a way in, which is exactly why the
misspelling failed loudly.

Vocabulary was requested by the learner AFTER describing the mechanism correctly in their own
words: class, dataclass, instance, attribute, tuple, unpacking. Supplying it then rather than
earlier was the right order and should be repeated.

Error taxonomy now has five members, all exiting non-zero:

```text
ModuleNotFoundError   the file is not there
ImportError           the file is there, the name is not, caught at the import line
NameError             the name is not there, caught where it is used
AttributeError        the object exists, the field on it does not
AssertionError        everything exists, the value is wrong
```

ORAL DEFENCE PASSED against `docs/DESIGN_REVIEW_RUBRIC.md`, with no labels prompted:

```text
requirement    three counts must reach a caller without being confused for one another
alternative    a plain tuple
mechanism      the value is reached by name, so position cannot be gotten wrong
downside       an extra class definition, judged negligible at three integers
reversal       a tuple is better when order is obvious and the count is small — the learner
               offered the threshold unprompted, four or five values needs names
```

The reversal condition is the element the rubric flags as most often missing, and it was
answered without hesitation.

## Phase 2 — PAUSED RED, deliberately

`test_summarize.py` now contains a failing test and this is the intended state:

```python
def test_summarize_diff_reports_all_three_counts():
    result = summarize_diff(TWO_FILE_DIFF)
    assert result.files_changed == 2
    assert result.lines_added == 3
    assert result.lines_removed == 2
```

`summarize.py` has no `summarize_diff` and no `DiffSummary`. The import at the top of the test
file asks for `summarize_diff`, so the suite fails at the import line.

RESUME HERE. The learner was asked which of the five errors this produces and at which line,
and had not answered when the session paused. That question is the first thing to ask tomorrow.
Do not answer it for them and do not run the suite before they commit.

Agreed sequencing for the next patch, one idea at a time:

```text
1. predict the failure, then build DiffSummary and summarize_diff, test-first
2. delete count_added_lines, count_removed_lines, count_changed_files once nothing calls them
3. splitlines boundary, string -> list, after its unaided retrieval
```

Still owed and unannounced: the exit-status retrieval, in a form that is not a Python test run.
Still owed after a longer gap: the `branch_precedence` retrieval.

### Resume question SPOILED — Claude's error, tenth prompt defect

The paused-red state above was intended as tomorrow's opening question: which of the five errors
does the failing import produce, and at which line. Claude then ran the suite in the same
message in order to verify the red state, printing `ImportError` before the learner had
committed to a prediction.

This is the tenth recorded prompt defect and the first that destroyed a planned assessment
rather than merely confusing one. The instruction not to run the suite before the learner
commits had been written into HANDOFF.md by Claude in the same turn.

RULE: verify a red state BEFORE writing the test into the conversation, or not at all. Never run
a suite in the same message that asks the learner to predict its output.

Salvage, and it is arguably the better question: ask the learner to EXPLAIN why the failure is
`ImportError` at the import line rather than `NameError` at the call site, given that in both
cases a name is missing from a file that exists. Then issue one fresh unspoiled prediction
before any code is written.

## Phase 2 — splitlines, second failed retrieval, re-learned

Evidence `EV-P2-SPLIT-082`. Learner-initiated: they opened the session asking to go over
`splitlines`. A recall attempt was taken before any teaching, since it was an owed retrieval.

The recall failed for the second time, at 10 confidence, correctly low. The wrong answer was
diagnostic rather than blank:

```text
said input is a LIST        it is a STRING
said output is PRINTING     it is a LIST, and nothing prints
```

The printing error is CLAUDE'S FAULT. Every prior demonstration followed `splitlines` with a
loop that printed each line, so the two fused. The fix showed `splitlines` with no printing of
parts, `type()` on both sides, and pointed out that the original string already prints on three
lines because of the `\n` — so line-by-line appearance was never `splitlines`' doing.

LEARNER QUESTION, and it was the right one: *isn't that a little redundeant why not just make a
list*. Answered by asking who authors the text. `TWO_FILE_DIFF` is hand-written, so a list was
possible there; real diff text is written by git.

The learner then said they did not know whether git returns one string or separate lines. Settled
by generating real output per the standing rule — `git diff` through `subprocess.run` with
`capture_output=True, text=True`:

```text
type      : <class 'str'>
len       : 143
exit code : 0
repr      : 'diff --git a/app.py b/app.py\nindex 078ac13..d8cb1a4 100644\n--- a/app.py\n...'
```

One string, `\n` between lines. `repr` was used deliberately because `print` would have acted on
the `\n` and hidden the answer. The learner also saw the Phase 7 subprocess call and its exit
code sitting beside the text, with no Phase 7 code written.

SCORING: taught and tested in the same sitting, so this does NOT count as the delayed retrieval.
Re-learned for the second time. One unaided attempt after a gap is still owed, and the surface
must not be a string of short words.

METHOD NOTE, second of its kind after the exit-code one: when a learner's wrong answer names a
neighbouring operation, check whether Claude's own examples always paired the two. Twice now the
misconception has been induced by demonstration habits rather than by the learner.

## Phase 2 — DATA MODEL COMPLETE

`summarize.py` is now 34 lines: a `DiffSummary` dataclass and one `summarize_diff` that walks the
lines once, keeps three counters, and returns one record. The three single-count functions and
their three tests are deleted. Both suites green, exit 0, at every step.

Evidence `EV-P2-IMPORT-083` and `EV-P2-SUMMARY-084`.

Delivered in two patches on purpose, and the learner agreed the sequencing after fairly
challenging it:

```text
patch 1   add DiffSummary and summarize_diff      suite green throughout
patch 2   delete the three counters               green means the deletion was safe
patch 3   fix the stale docstring                 comment only, behaviour unchanged
```

Both predictions unaided and correct — 90 on the build, 100 on the deletion. The coverage
question was answered correctly: the deleted tests asserted the same three numbers against the
same input that the surviving test asserts by name.

Claude did NOT run either suite in the same message as a prediction request. That corrects the
tenth prompt defect recorded yesterday.

`ImportError` versus `NameError` settled, evidence `EV-P2-IMPORT-083`:

```text
looking during an import statement    ImportError
looking at a name being used          NameError
```

Demonstrated by moving the import block to the bottom of a scratch copy: the suite then fails
with `NameError` on a function that DOES exist in `summarize.py`. Only position changed. The
learner applied this unaided minutes later, predicting that deleting the three counters would
fail at the import and never reach the calls.

Learner-supplied wording for the corrected contract line: `out one DiffSummary holding three
counts`.

New notation named rather than left to guess: the `dataclasses` import, the `@dataclass`
decorator, and `int` type annotations that Python does not enforce.

## Phase 2 — what remains

```text
splitlines boundary   summarize_diff takes a list; git returns one string
                      this is the last piece of Phase 2
```

Retrievals still owed:

```text
splitlines            THIRD unaided attempt after a gap, no demonstration first,
                      and not a string of short words
exit status           unaided, unannounced, not a Python test run
branch_precedence     unaided, after a longer gap, then MASTERED
```

`HANDOFF.md` is now partly stale: its START HERE section points at the ImportError question,
which is answered. Refresh it before moving sessions.

## Phase 2 — splitlines RETRIEVAL SATISFIED

Evidence `EV-P2-SPLIT-085`. Third attempt, issued immediately on return from a real gap, with no
demonstration in front of it — the two previous failures had both followed one. All three parts
correct at 90 confidence: the list of whole lines, `len` of 3, and the direction stated
unprompted as string in, list out.

The learner volunteered that they had previously held a space-splitting misconception, now
closed. Recorded as `splitlines_splits_on_spaces`, resolved. That disclosure is worth more than
the correct answer, and it came from asking which of two readings they meant rather than taking
the generous one.

`splitlines` is now banked, not borrowed. Three surfaces, one genuine delayed retrieval, and the
direction explained rather than recited.

Retrievals still owed:

```text
exit status         unaided, unannounced, not a Python test run
branch_precedence   unaided, after a longer gap, then MASTERED
```

### Recurring correction: git is not GitHub

The learner has now said twice that the diff text arrives "from github". It arrives from `git`,
the local command-line program, run as a subprocess. BuildLens never contacts GitHub. The only
GitHub involvement in this project is the sync push, which is unrelated to the diff pipeline.

Worth re-pinning whenever the Phase 7 boundary comes up, because the distinction matters for the
failure mode: a local program failing produces stderr and a non-zero exit code, which is a
different situation from a network call failing.

## Phase 2 — PIPELINE COMPLETE AND VALIDATED

`summarize_diff` now takes ONE STRING of diff text, exactly the shape git produces, and returns a
`DiffSummary`. Evidence `EV-P2-BOUNDARY-086` and `EV-P2-REAL-087`.

```text
one diff string
  -> splitlines()
  -> classify_diff_line, once per line
  -> three counters
  -> one DiffSummary
```

That is the design the learner described in their own words at `EV-P2-ACC-075`, before they had
met a loop.

The boundary decision was the learner's. Offered three placements, they first chose C — accept
either shape — reasoning that a caller might save work by passing a list. One question dislodged
it: that caller has a string from git, so who called `splitlines` and when. They saw that C saves
nothing and only relocates the work, and switched to A unaided. No argument against C was stated
by Claude.

The loud failure is a feature and the learner should be able to say so: passing a list now raises
`AttributeError: 'list' object has no attribute 'splitlines'` rather than silently producing
zeros.

New misconception `method_distributes_over_elements`, resolved: the learner reasoned that calling
`.splitlines()` on a list would work because the strings inside have that method. Resolved by
asking what `all_lines` IS at the moment of the call.

VALIDATED AGAINST REAL GIT OUTPUT, and the learner approved the check after being given the case
for declining it as out of phase. A three-file diff including a brand-new file, 452 characters,
a shape the tests do not cover:

```text
exit code : 0
type      : <class 'str'>
length    : 452

DiffSummary(files_changed=3, lines_added=5, lines_removed=1)
```

The learner hand-counted 3, 5, 1 before anything ran, including two line forms they had never
seen — `new file mode 100644`, which matches no prefix and falls through to context, and
`--- /dev/null`, caught by the `"--- "` branch they defended back in Phase 1 without needing to
know what /dev/null means.

No subprocess code entered the repository. The harness lived in the scratchpad.

## Phase 2 — what is left

Functionally, nothing. What remains is closing discipline:

```text
milestone requirements   learner explanation of summarize.py, plus one transfer variant
exit status retrieval    owed, unannounced, NOT a Python test run
branch_precedence        owed, after a longer gap, then MASTERED
```

The exit code printed beside the text in the validation run is the whole of the Phase 7 decision.
It was pointed out once and deliberately not pressed, since the retrieval must not be announced.

Phase 3 should not begin until the milestone is closed.

## Phase 2 — MILESTONE CLOSED

Evidence `EV-P2-TEACH-088` and `EV-P2-TRANSFER-089`. All four requirements met:

```text
automated tests      both suites green, validated against real git output
learner trace        every run predicted before it ran
learner explanation  contract, mechanism, three limitations, ranked by danger
transfer variant     unseen domain, found a silent bug, stated the rule generally
```

CONTRACT IMPROVED BY THE LEARNER, and the reasoning matters more than the wording. They asked to
name `DiffSummary` as a dataclass instance in the contract. Challenged, they did not understand
the objection, so it was made concrete: if `@dataclass` were replaced by a hand-written class
with identical fields, how many of the four calling lines change? They answered none, unaided,
then produced the better line themselves:

```text
out       one DiffSummary with files_changed, lines_added, lines_removed
```

Rule extracted: a contract states what the caller can rely on, not how you built it.

Limitations: the open question produced `i do not know, 0` and was converted to a four-way
selection. All four correct, including the odd one out — passing a list is NOT a limitation
because it raises `AttributeError`, so the caller finds out. On the per-file question the learner
named the fix and then argued it should not be built yet, which is the correct instinct.

Danger ranking correct and unaided: git failing beats binary files and missing per-file
attribution, because its output is indistinguishable from success.

REGRESSION, and it needs scheduling: `return_value_is_the_call_expression` resurfaced. The learner
said `print(summarize_log(log))` would print nothing because the function returns rather than
prints. This was stable in Phase 1 at `EV-P1-RETURN-007` and `EV-P1-RETURN-008`. Remediated by
descending to R1 — a function returning 2, printed both ways — then climbing to a function
returning a dataclass instance. A DELAYED RETRIEVAL IS NOW DUE on this concept.

The transfer itself: a log summarizer missing `splitlines`, so it loops characters. It returns
`LogSummary(errors=0, warnings=0)` for a log containing two errors, and exits 0. The learner
worked the whole chain unaided once asked what `line` holds on the first pass, then gave the fix
and the general rule with no domain terms:

> a silent error that never crashes means you can never fix it unless you notice the output

That is the third distinct place today the learner has made the loud-versus-silent argument — for
`DiffSummary` over a tuple, for the git-failure hazard, and here in a domain with no git in it.

## Retrievals owed entering Phase 3

```text
exit status                        unaided, unannounced, NOT a Python test run
branch_precedence                  unaided, after a longer gap, then MASTERED
return_value_is_the_call_expression NEW, after a gap, following today's regression
```

Phase 2 is complete. Phase 3 may begin.

### STANDING RULE — learner is a visual learner

Requested directly on 2026-08-27, at the start of Phase 3:

> can it be noted that i am a visual learner so code snippits or pictures would make this a lot
> smoother

Apply this from now on. Concretely, for this project:

- prefer a drawn diagram or a concrete code snippet over an abstract question;
- when asking the learner to choose, SHOW the options as code or as a picture rather than
  describing them in prose;
- when asking what something should contain, draw an example of the container first;
- reserve pure prose questions for defence and explanation, where the point is their words.

This is consistent with what has already been observed independently. Every recorded prompt
defect in this project has the same shape — an abstract or open question producing "what am I
looking at?" — and every recovery has come from making the question concrete or countable.
There are now ten such defects on record. Treat this rule as the fix for that whole class.

## Phase 3 — STARTED. Model specified, alias/copy gate PASSED. No code yet.

Evidence `EV-P3-STATE-090` and `EV-P3-ALIAS-091`. No Phase 3 code exists; this was specification
and the knowledge gate.

DESIGN DECISION, the learner's:

```text
Session
└── changes[]
     └── one diff_text string per change
```

The summary is NOT stored. It is recomputed by calling `summarize_diff` when needed, because
derived data goes stale. The learner reached this by asking which of the two would be wrong if
they disagreed, answering correctly that the summary is derived, then concluding on their own to
store only the text.

Both costs were MEASURED rather than asserted, and the learner forced that:

```text
one small edit in a 1,500-line file     272 chars
rewriting all 500 functions in it    41,667 chars
100 typical changes, recompute        0.328 ms   ~2% of one screen frame
```

CLAUDE ERROR, caught by the learner. A 50,000-character figure was invented and placed beside two
measured numbers, making it look measured. The learner pushed back and asked what it represented.
Real diffs were then generated. The invented figure turned out near a genuine worst case, but
that case is a whole-file rewrite, not a typical change. Do not put invented numbers beside
measured ones.

Reversal condition the learner can state: if summarizing became expensive, or the list very
large, storing the summary would start to win.

Also clarified: the editable code lives on disk and is Phase 13. The session remembers events;
the editor reads files.

ALIAS/COPY GATE PASSED, `EV-P3-ALIAS-091`, after three wrong predictions that were all
productive:

```text
p.append(9)     changes the object      every name pointing at it sees it
p = [9]         moves the name          other names stay where they were

immutable   str, int    methods return a new value, original untouched
mutable     list        methods change in place, return None
```

The learner traced aliasing, rebinding, both in one sequence, mutation through a function
parameter, and rebinding of a parameter — the last correctly and with the mechanism in their own
words: *other did not change what it was pointing at the entire time*.

THE IMPORTANT MOMENT: the three-name trace was answered WRONG at 100 CONFIDENCE, immediately
after the learner said they understood and asked to move on. The plan's instruction — *if you
cannot explain which object owns the list and who can mutate it, stop here* — was quoted and the
phase held. Overconfidence, not underconfidence, was the risk this time; it is the first such
instance recorded.

Sixth taxonomy member met: `TypeError` on `word[0] = "z"`, since strings are immutable.

## Phase 3 — NEXT, unanswered

The question on the table when the session paused:

> `session.changes` hands out the actual list, not a copy. What could go wrong with that?

The learner now has every tool needed to answer it and has not yet been asked to. Do not answer
it for them.

Then: build `Session` test-first, and trace the real session state through several operations,
which is the second half of the Phase 3 gate.

Retrievals owed:

```text
exit status                          unaided, unannounced, NOT a Python test run
branch_precedence                    unaided, after a longer gap, then MASTERED
return_value_is_the_call_expression  after a gap, following the Phase 2 regression
```

## Phase 3 — session.py exists, rung 1 green

```python
class Session:
    def __init__(self):
        self.changes = []
```

`test_session.py` asserts `len(session.changes) == 0` on a new Session. Green, exit 0. All three
suites green. Evidence `EV-P3-COPY-092` and `EV-P3-SESSION-093`.

TEST LADDER agreed with the learner, who first proposed the leak test and then reasoned correctly
that a copy must exist before it can leak:

```text
1  a new Session has no changes                     len == 0   DONE
2  record one change, it is there                   len == 1
3  record two, both there in order                  len == 2
4  the history you get back holds what was put in
5  mutating that history does not touch the session  <- the leak test
```

DESIGN DECISION, the learner's: `history()` returns `list(self.changes)`, a copy, rather than
marking the attribute private by convention. Reason given — most reliable, and the copy is freed
once nothing points at it. The garbage-collection claim was checked and is correct.

Shallow copy established, including its limit. `original is copy` False, `original[0] is copy[0]`
True. New misconception `shallow_copy_protects_nested_items` surfaced and was resolved: the
learner attributed a nested leak to "position", which was falsified by showing `copy[1]` leaks
identically while `copy[0] = ...` does not. Reduced to the pair they already knew:

```text
.append()   changes the object       shared -> leaks
=           moves a name or slot     the copy's own -> contained
```

Their items are strings, which cannot be mutated, so `list(...)` is sufficient. Had they been
mutable, a deep copy would be required. The learner should be able to state that condition.

CLAUDE ERROR, raised by the learner: the nested list-of-lists example was a hypothetical about
the limit of shallow copying, not their design, and was introduced mid-build without being
labelled. Label hypotheticals as hypotheticals.

LEARNER QUESTION that found a real trap, unprompted: *if we had no init session would still have
the persisitent memory of the last session?* They predicted 1 and 0 for a class-body
`changes = []`. The real answer is 1 and 1, with `a.changes is b.changes` True:

```text
self.changes = [] in __init__     runs per instance    a new list each time
changes = [] in the class body    runs once at import  ONE list, shared forever
```

Recorded as `class_attribute_is_shared`. Their instinct was right and the sharing is worse than
they guessed — not the previous session, but every session simultaneously.

NEXT: rung 2, `record`, test-first.

## Phase 3 — rungs 2 and 3 green, rungs 4 and 5 written, PAUSED WITH A PREDICTION OPEN

```python
class Session:
    def __init__(self):
        self.changes = []

    def record(self, diff_text):
        self.changes.append(diff_text)
```

Three tests green, exit 0. Evidence `EV-P3-RECORD-094`.

```text
1  a new Session has no changes                     DONE, green
2  record one change, it is there                   DONE, red first, then green
3  record two, both there in order                  DONE, green on first run
4  history returns what was recorded                WRITTEN, not yet run
5  mutating history does not touch the session      WRITTEN, not yet run
```

RUNG 3 PASSED IMMEDIATELY and this was flagged rather than glossed. A test that DRIVES new
behaviour must be red first; a test that LOCKS IN existing behaviour is a regression guard and may
legitimately be green first. The one to distrust passes immediately and defends nothing.

Three misconceptions this stretch, all resolved:

- `derived_state_duplicated` — the learner proposed a counter attribute tracking how many times
  `record` ran. Dislodged by placing it beside their own rejected stored-summary decision. Both
  are derived data that must be kept in step by hand.
- `test_must_discover_the_number` — a genuine and useful confusion: how can a test assert a count
  once 652 changes exist? Resolved by drawing the difference between a test, which builds a world
  it controls, and the real run, where nobody asserts anything. The learner restated it: *652 is
  not for a test it is the real run*.
- `assignment_in_place_of_comparison` — the ordering assert was first written with a single `=`,
  which would have replaced the list and made the test pass regardless. Self-corrected when shown
  their own earlier asserts.

The learner then observed unprompted that `len == 2` was redundant once the whole list is
compared, and it was removed.

Supplied because not derivable: `record` is not a Python name and there is no reserved list to
collide with; `self` is how a method knows which instance it was called on.

## RESUME HERE — an open prediction, deliberately not run

`test_session.py` now contains rungs 4 and 5, and `session.py` has NO `history()` method. The
suite has NOT been run. Evidence `EV-P3-LEAK-095`.

The learner's committed prediction, verbatim:

> assertion error the append will add the second diff and then it will be diff a and b

Do NOT reveal the result. Ask them to walk it: which test runs first, and whether `history()`
exists at the moment it is called. Their reasoning is about rung 5's logic and assumes the method
is already there.

The suite was left unrun on purpose so this is worked through live rather than read while leaving.
That follows the rule added after the tenth prompt defect.

After that: implement `history()` returning `list(self.changes)`, get both rungs green, then the
Phase 3 milestone — explanation plus transfer — and the second half of the Phase 3 gate, tracing
real session state through several operations.

## Phase 3 — Session COMPLETE, ladder green

```python
class Session:
    def __init__(self):
        self.changes = []

    def record(self, diff_text):
        self.changes.append(diff_text)

    def history(self):
        history_list = list(self.changes)
        return history_list
```

All five rungs green, all three suites green, exit 0. Evidence `EV-P3-LEAK-095-CLOSE`.

THE COPY WAS PROVEN LOAD-BEARING, not asserted. A scratch copy with `history_list = self.changes`
was run against the same tests: rungs 1 to 4 still pass, rung 5 fails with `AssertionError`. One
word decides it, and only the leak test defends it. That is the difference between a test that
means something and one that happens to pass.

The banked prediction resolved. The learner had predicted `AssertionError`, reasoning correctly
about rung 5 logic while assuming `history()` existed. On resume they spotted the gap themselves,
saying *great call i missed it*, and named call 4 and `AttributeError`.

METHOD MADE EXPLICIT after the learner asked *can you tell me why i am gussing here*. They were
not guessing, they were reasoning without trusting it. The procedure, now written down for reuse:

```text
walk each call in order
  -> list what each line touches
  -> check each against the file
  -> the first missing thing is where it stops
  -> then locate WHAT is missing to pick the error name
```

Two implementation misconceptions, both self-caught:

- `aliasing_instead_of_copying` — the first draft was `history = self.changes`. The learner spotted
  it in the same breath and asked for the copying mechanism.
- `missing_return` — the second draft built the copy and discarded it. Shown the inside/outside
  picture and reminded that `append` returns `None`, they supplied the return unprompted.

Missing colon after `def`, second occurrence. Corrected in passing.

## Phase 3 — what remains

```text
automated tests      DONE, five green
learner trace        DONE, every run predicted first
learner explanation  OWED — teach session.py
transfer variant     OWED
second half of gate  OWED — trace real session state through several operations
```

Retrievals still owed:

```text
exit status                          unaided, unannounced, NOT a Python test run
branch_precedence                    unaided, after a longer gap, then MASTERED
return_value_is_the_call_expression  after a gap; note the missing_return slip above
```

## Phase 3 — KNOWLEDGE GATE PASSED, both halves

Evidence `EV-P3-ALIAS-091` (alias/copy trace) and `EV-P3-MOVIE-096` (session state movie). The
plan's stopping condition is cleared.

The movie, all six states predicted correctly before it was run:

```text
                        session.changes                 h
STATE 0                 []                              does not exist yet
STATE 1                 ['diff A']                      does not exist yet
STATE 2                 ['diff A', 'diff B']            does not exist yet
STATE 3                 ['diff A', 'diff B']            ['diff A', 'diff B']
STATE 4                 ['diff A', 'diff B']            ['diff A', 'diff B', 'diff C']
STATE 5                 ['diff A', 'diff B', 'diff D']  ['diff A', 'diff B', 'diff C']
```

The two lists diverge at STATE 3 and never speak again. `h` is a SNAPSHOT — true when taken, never
updating. That cuts both ways: the session is protected from `h`, and `h` is stale the instant
anything is recorded. The learner asked about the diff D behaviour unprompted, having already
answered it correctly in the table.

GATE ANSWERS, reached in two passes:

```text
who owns it     each Session instance owns its own list

who can mutate  record()                            the intended path
                anything holding session.changes    UNPROTECTED
                the copy returned by history()      cannot reach back
```

The first ownership answer said the CLASS owns the list, contradicting the learner's own
class-attribute discovery. Asked to reconcile it, they corrected to the instance unaided.

The mutation answer was initially the INTENT rather than the fact. `session.changes` is a plain
public attribute, so `session.changes.append("sneaky")` works and `history()` then reports it as
real history. Demonstrated rather than asserted.

KNOWN LIMITATION the learner can now state: the design stops the ACCIDENTAL case — someone takes
the history and edits it — and does not stop the deliberate one. The learner asked the sharper
question, *who is writing that*, and the honest answer is themselves: in six months, or from the
CLI in Phase 6, or the API in Phase 12. Not a saboteur, someone who forgot `record` existed and
saw a list sitting there. That is exactly what the rejected underscore convention was for, and
adding it later is a live option rather than a defect.

Calibration note: 30 confidence on a correct STATE 5, 40 on a correctly-hedged ownership answer.
Underconfidence continues on correct answers; the single overconfident miss remains the alias
trace at 100.

## Phase 3 — what remains

```text
automated tests      DONE, five green
learner trace        DONE, every run predicted first
knowledge gate       DONE, both halves
learner explanation  OWED — teach session.py
transfer variant     OWED
```

Retrievals still owed:

```text
exit status                          unaided, unannounced, NOT a Python test run
branch_precedence                    unaided, after a longer gap, then MASTERED
return_value_is_the_call_expression  after a gap
```

### Carried forward — the mutable-state question returns three times

The learner asked a fair design question at the close of Phase 3:

> but if i know i can call history why append and if i know everything is recorded why append

Answered honestly: at one caller who wrote the class yesterday, the copy is cheap insurance
rather than a necessity. The case it actually defends is not a deliberate `append("sneaky")`,
which nobody writes, but the operation that does not look like a mutation:

```text
.sort()      wanted a sorted view, mutated the real one
.reverse()   wanted newest-first, reversed history permanently
.clear()     wanted to clear the display, cleared the record
.pop()       wanted to peek at the last one, removed it
```

Demonstrated: three changes recorded in order C, A, B. `sorted(session.changes)` left the real
order alone; `session.changes.sort()` silently rewrote it to A, B, C. The control tower would then
report an order Claude never worked in, with no traceback and nothing to notice.

Filed alongside `word.upper()` versus `word = word.upper()` — same shape, one returns a new thing,
one changes yours.

WHERE THIS RETURNS, confirmed by reading IMPLEMENTATION_PLAN.md rather than asserted:

```text
Phase 5   Explicit Interfaces / Contracts
          "what crosses the boundary matters more than the filenames"
          The underscore decision and what a caller may touch belong here,
          revisited with the vocabulary for it.

Phase 9   Event-Driven State and Reliability
          A formal event model - ChangeObserved, TurnCompleted, GatePassed.
          Once history is an event stream rather than a list of strings,
          protecting it stops being style and becomes the point.

Phase 13  Safe Collaborative Editing
          The no-silent-overwrite invariant, two writers, real consequences.
          CLAUDE.md forbids weakening it without an ADR.
```

A list quietly reordered by `.sort()` is the toy version of what Phase 13 spends its entire length
preventing. Raise this thread again at Phase 5 and confirm the learner still holds it.

---

# SESSION CLOSE — 2026-08-28, quiz session 2

## Phase

Still Phase 3 complete, Phase 4 not started. No product code was written this session. No
implementation was attempted and none should have been.

## Exact code that exists

Unchanged from the previous close:

```text
classify.py     classify_diff_line(line) -> file_header | metadata | added | removed | context
summarize.py    summarize_diff(diff_text) -> dict of three counts
session.py      class Session: __init__, record, history

test_classify.py     green
test_summarize.py    green
test_session.py      green, five tests
```

All three verified exit 0 at the start of this session before any quizzing, per the handoff's
instruction not to assert it from the document.

## New files

```text
HANDOFF_QUIZ_2.md   handoff for the next quiz session, supersedes HANDOFF_QUIZ.md
QUIZZES.md          verbatim questions and verbatim answers, session by session
```

## Evidence added

Records 97 to 100. Ledger is now 100 records.

```text
EV-P1-HEADER-097            correct
EV-P1-BRANCH-098            partial, remediated
EV-P1-BRANCH-098-TRANSFER   partial, remediated
EV-P1-NEST-099              correct
EV-P1-RETURN-100            partial, self-corrected before reveal
```

## Concepts known cold — changed this session

```text
file_header             was the project's most persistent gap at 13 appearances.
                        Given cold on an unseen diff in an unseen domain, eight
                        lines, all eight correct including the @@ hunk header.
                        Moved to known. Do not re-teach. Retrieve after a long gap
                        with a diff containing `diff --git` and `index ` lines,
                        which this probe deliberately omitted.

nested_call_evaluation  bump(bump(3)) traced unaided. Named the inner call as
                        first, carried the intermediate value forward, handled the
                        3 > 3 boundary correctly. This is the Phase 1 knowledge
                        gate as written in IMPLEMENTATION_PLAN.md. Closed.
```

## Uncertain concepts

```text
branch_precedence       mechanism proven twice, including transfer to a non-diff
                        routing domain. The "which items actually change" half
                        failed twice. Not MASTERED. Retrieve once more, phrased
                        per-item.

print_vs_return         first instinct was still the printed value; the learner
                        reversed themselves unaided inside the same answer. This
                        is the second consecutive session where this idea was
                        self-corrected rather than answered right initially
                        (see EV-P3-LEAK-095-CLOSE). Not cold.

str(None) is "None"     supplied as a fact this session, not tested.
```

## The finding worth carrying forward

The learner's misses this session were **procedural, not conceptual**.

Twice they answered a per-item question at the group level — "the metadata becomes added", "the
top 3 lines" — and both times, the moment a single item was isolated, they answered correctly and
diagnosed it themselves. The branch-selection model is sound. The habit of scanning a group and
answering for the group is what fails.

The remedy is procedural. Force per-item enumeration in the question itself. Do not descend into a
concept lesson, which is what the remediation ladder would otherwise suggest — the prerequisite is
already stable.

## Calibration

The underrating pattern held, and sharpened. An 80 on a flawless eight-line answer. A 90 on a
fully correct unaided trace. A 40 on the answer where they self-corrected to the right concept.

The one overconfident answer of the session — 90 — was the grouping miss. Not raised with the
learner beyond a single factual line, per the handoff.

## Last knowledge gate

Phase 1 gate, passed: "trace a new function problem with 2-3 calls and one branch"
(`EV-P1-NEST-099`).

## Next retrieval due

```text
print_vs_return                        with the None somewhere non-obvious:
                                       in a list, compared with ==, or as an
                                       if condition. NOT another concatenation.

output_and_exit_status_are_independent OWED, untouched, still constrained:
                                       unaided, unannounced, and NOT via a
                                       Python test run.

branch_precedence enumeration          per-item phrasing, after a gap

splitlines / string immutability       test whether word.upper() and
                                       sorted() vs .sort() read as ONE
                                       principle or two facts
```

## Still open

```text
EV-P2-MODEL-060   right three fields, wrong diff, individual values never named
EV-P3-RECORD-094  self binding, = vs ==, == comparing list contents in order
```

Neither was reached. `EV-P3-RECORD-094` pairs naturally with the `print_vs_return` retrieval, since
`==` against a `None` result is one question rather than two.

## Next implementation step

None. Phase 4 remains blocked on the two outstanding Phase 3 milestones:

```text
learner explanation   teach session.py aloud, in their own words
transfer variant      the aliasing/copying idea in a domain with no sessions in it
```

Both were listed as owed in the previous handoff and neither was reached this session. They gate
the move to Phase 4.

## Files the learner should be able to teach

Unchanged: `classify.py`, `summarize.py`, `session.py`. The teach-aloud on `session.py` is still
owed and is now the oldest outstanding item in the project.

---

## ADDENDUM — exit status retrieval attempted and failed

Added after the session-close section above. One further exercise was run before the learner
switched tools.

`EV-P1-EXIT-101`, tag `output_and_exit_status_are_independent`. Ledger is now 101 records.

The retrieval owed since Phase 1 was finally given, in the constrained form the state file
required: a shell transcript with grep, not a Python test run, unannounced.

It failed, and it does not count as delivered. The learner saw the answer rather than producing
it. Two blockers, in order:

```text
1  `$?` unreadable            read grep's output instead of echo's
                              first answer was "apple / cherry" - fruit, not numbers

2  0-is-success not retained  stated twice in different framings, inverted both
                              times. Answered "1 and 1" with reasoning that implied
                              1 and 0, then "1" again after the collision was named
```

The second blocker is the interesting one. It is not carelessness — it is direct interference from
Python, where 1 is truthy and 0 is falsy. The shell reverses that, because an exit status answers
"how many problems occurred", not "did you find something". The learner has a correct model that
is actively fighting the new one.

A third confusion appeared at the end: "isn't printing 1 still an output". The status was being
treated as part of the command's output. It is not — grep printed nothing when it failed, and the
`1` on screen came from `echo`. Clarified but not retested.

Worked-example rescue was entered (rule 14.6 step A) and the session ended there. Steps B, C and D
were not performed.

NEXT RETRIEVAL, revised:

```text
0-is-success convention      cold, on its own, before anything else. It has now
                             failed twice after being stated twice.

worked-example step B        learner explains the build-log case back

fresh case, reverse direction a step that SUCCEEDS silently, prints nothing, and
                             the teammate's rule marks it failing. Never touched.
```

Do not re-ask the CI question before the convention is stable. The independence idea cannot be
tested through a convention the learner is still inverting.
