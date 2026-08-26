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

