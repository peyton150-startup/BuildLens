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

## QUIZ CONTINUATION — 2026-08-28

The learner explicitly limited the quiz to fundamentals from completed Phases 0–2. Do not test
Phase 3 material in this quiz and do not begin Phase 4.

Evidence `EV-P1-EXIT-102`: cold retrieval of the shell convention was correct. The learner chose
`0` as success at confidence 70 without running anything. The convention is now stable for this
rung; next give one same-rung silent-success near-transfer before returning to the larger
output-versus-status problem.

Evidence `EV-P1-EXIT-103`: the silent-success values were both predicted correctly (`0`, nothing
on screen), but the learner explicitly said the scenario was not understood. Do not mark the
independence concept passed yet. Show a small two-channel diagram and require a teach-back. The
learner requested pictures for harder questions; diagrams are welcome after commitment or when
they do not expose the answer.

Evidence `EV-P1-EXIT-104`: teach-back passed. The learner explained that a command can print
nothing while its hidden status tells the shell it succeeded, confidence 70. The confidence tag
needed one reminder. Next use the partially scaffolded reverse direction: a successful silent
command that an output-only rule marks incorrectly.

Evidence `EV-P1-EXIT-105`: verdicts correct at confidence 80—the output-only rule says FAIL while
status `0` means PASS. A new heuristic surfaced: assuming silence means success. This is unsafe;
screen silence still cannot determine status. Descend to one R1 problem where screen text and
status conflict, asking which channel controls the shell's judgment.

Evidence `EV-P1-EXIT-106`: R1 recovery correct at confidence 80. With screen text `Completed` but
status `1`, the learner classified failure and said the status should be trusted over the text.
Give one same-rung near-transfer with alarming text and status `0` before climbing.

Evidence `EV-P1-EXIT-107`: opposite-direction R1 transfer passed at confidence 70. Status `0` was
correctly treated as the shell/CI success verdict even though the output contained `ERROR`; the
learner also appropriately said the text deserves investigation. Give one final fresh
target-level two-command case, item by item, then rotate to another Phase 0–2 fundamental.

Evidence `EV-P1-EXIT-108`: fresh target-level transfer passed at confidence 80. The learner
evaluated both commands separately and correctly rejected the teammate's output-only verdict in
both directions. `output_and_exit_status_are_independent` is remediated for this review. Retrieve
later on a delayed new surface; rotate now to `print_vs_return`.

Evidence `EV-P1-RETURN-109`: `print_vs_return` mechanism was correct at confidence 80. The learner
identified printed `GO`, missing return as `None`, and appended `None`, and correctly said it is
not equal to `"GO"`. The final printed Boolean was instead written as `exit code 1`, likely
interference from the preceding topic. Descend to R1: print one list-equality expression with no
function or shell context.

Evidence `EV-P1-EQUALITY-110`: R1 recovery correct at confidence 80. `[None] == ["GO"]` was
correctly predicted to print `False`, with no exit-status substitution. Give one same-rung
near-transfer testing whether list equality compares contents in order.

Evidence `EV-P1-EQUALITY-111`: wrong at confidence 80. The learner said lists with the same
members in different orders compare equal and explicitly stated that `==` checks contents but not
order. Primary blocker: list equality is being modeled as unordered membership. Simplify to one
corresponding pair in plain language; do not repeat a whole-list problem yet.

Evidence `EV-P1-EQUALITY-112`: isolated-pair recovery correct at confidence 100. The learner said
`"red" == "blue"` is false and restated that list equality requires the same contents in the same
order. Give one fresh single-pair near-transfer, then reintroduce a whole list.

Evidence `EV-P1-EQUALITY-113`: fresh single-pair near-transfer correct at confidence 100.
`"green" == "green"` was correctly identified as true because the strings are the same. Climb to
a two-position whole-list comparison and require one answer per position before the overall result.

Evidence `EV-P1-EQUALITY-114`: ordered list equality recovered at confidence 100. Both positions
and the whole-list result were conceptually correct. Exact screen output was written lowercase
`false` instead of Python's `False`; this is transcription/capitalization, not an equality-model
failure. Isolate exact Boolean spelling at R0 before returning to `print_vs_return`.

Evidence `EV-P1-BOOLEAN-115`: exact Boolean capitalization corrected at confidence 100. The
learner stated that Python uses capital initial letters in `False` and `True`. Return now to a fresh
target-level `print_vs_return` trace with the call value stored inside a list.

Evidence `EV-P1-RETURN-116`: `print_vs_return` mechanism correct at confidence 100—the learner
said `mark()` prints `saved`, has no explicit return, contributes `None`, and leaves `None` in the
list. Exact final output omitted the list brackets, and an unrequested exit code was inserted.
Descend to R1: print `[None]` directly with no function or shell context.

Evidence `EV-P1-LIST-117`: R1 exact-output check wrong at confidence 30. `box = [None]; print(box)`
was predicted as bare `None`, losing the list brackets. Primary blocker is container versus item,
not `None` or return behavior. Descend to R0 and ask what object the assignment creates before
doing any printing.

The learner then corrected the output to `[None]` at confidence 80 and explicitly noted, "you
hinted at it." Preserve this as an assisted correction, not an independent pass. Give a fresh
one-item numeric list with no output hint.

Evidence `EV-P1-LIST-118`: independent R1 recovery correct at confidence 100. `numbers = [7];
print(numbers)` was predicted exactly as `[7]`, preserving the list brackets. Give one fresh
same-rung list-output near-transfer, then rebuild toward the printing-function target.

Evidence `EV-P1-LIST-119`: two-item list container and values were correct, but the first answer
`[3,8]` omitted the default space. After a reminder that spacing would be evaluated, the learner
self-corrected at confidence 100 and said a space belongs after the comma. Treat as partial and
descend to R0 recognition between two exact spellings.

Evidence `EV-P1-LIST-120`: R0 recognition correct at confidence 100. The learner selected the
spaced list representation and explicitly requested no more nitpicking and a move to another
Phase 0–2 topic. Honor this: stop formatting drills and only flag precision when it changes program
meaning or is itself the target. Rotate to Phase 2 summary-model fundamentals, especially the
still-open individual values from `EV-P2-MODEL-060`.

Evidence `EV-P2-MODEL-121`: fresh Phase 2 summary values all correct at confidence 80:
`files_changed=1`, `lines_added=2`, `lines_removed=1`. This closes the individual-value gap from
`EV-P2-MODEL-060`. Explanation was partial: `cake` was correctly named context, but "everything
else is metadata" grouped added, removed, and file-header lines incorrectly. This matches the
known procedural grouping pattern. Isolate `-tea` and ask for its label and counter; do not
re-teach the model.

Evidence `EV-P2-MAP-122`: isolated mapping correct at confidence 100. `-tea` was labelled removed
and mapped to `lines_removed`. Give one fresh same-rung added-line mapping before climbing back to
per-item enumeration.

Evidence `EV-P2-MAP-123`: added-line near-transfer correct at confidence 100. The learner
explicitly said the questions had become too simple. Fade the scaffold now: stop one-line mapping
questions and rotate to a harder composed Phase 0–2 trace on mutation versus new values.

Evidence `EV-P2-MUTATION-124`: composed mutation trace paused for syntax-only remediation. The
learner correctly said at confidence 100 that `word.upper()` does not change `word`, but explicitly
has not learned `sorted(...)`. Do not evaluate the list portion or continue the larger trace yet.
Explain only `sorted(list)` and give one R1 example tracking the original and returned list.

Evidence `EV-P2-SORTED-125`: R1 `sorted(...)` syntax passed at confidence 100. The learner
correctly kept `numbers` as `[2, 1]` and assigned `[1, 2]` to `ordered`, then asked about `.sort()`.
Teach `.sort()` in isolation next: it mutates the list and its call value is `None`.

Evidence `EV-P2-SORT-126`: partial at confidence 100. The learner correctly intended that
`numbers.sort()` changes `numbers` into sorted order, but said `result` receives that same list.
Primary blocker: conflating the mutated object with the method's call value. Ignore the extra
comma as a harmless typo. Descend to R0 and ask only whether the assignment receives the list or
`None`.

Evidence `EV-P2-SORT-127`: R0 choice wrong at confidence 40 after `.sort()` returning `None` had
already been taught. The learner chose the sorted list and remained unsure about assignment and
later printing. Enter worked-example rescue: use neighboring `.append()` to draw mutation and
return as separate paths, then require teach-back before any missing-step or fresh problem.

Evidence `EV-P2-MUTATION-128`: worked-example teach-back failed at confidence 80. Despite the
diagram explicitly separating mutation and return, the learner said `items` and `result` point to
the same list and predicted printing `result` shows the list. Primary blocker is now assignment:
the left-hand name is not being bound to the right-hand call value. Descend below method calls to
R0 `result = None` before rebuilding.

Evidence `EV-P1-NONE-129`: partial at confidence 80. The learner correctly predicted that
`print(result)` displays `None`, but said `result` has no value. Clarify that `None` is a real
Python value representing absence; the name exists and is bound to it. Stay at R0 and retrieve
that distinction before rebuilding assignment and method return.

Evidence `EV-P1-NONE-130`: R0 recovery correct at confidence 100. The learner stated that the name
`result` exists and its value is `None`. Give one short assignment near-transfer, then rebuild
toward the mutation/return target.

Evidence `EV-P1-NONE-131`: bridge answer partial at confidence 100. `copy` correctly received
`None`, but the learner called `None` a string. This is a meaningful type distinction, not
formatting: unquoted `None` is the absence value; `"None"` is a string. Descend to R0 recognition.

Evidence `EV-P1-ASSIGN-132`: teach-back correct at confidence 100. The learner's core model is that
assignment binds the new name to the same value/object held by the right-hand name. Clarified that
the shared object here is `None`, not the string `"None"`; mutable-list consequences differ from
immutable strings/None. Resume worked-example rescue at step C: supply the changed list state and
ask for the one missing return value from `append`.

Evidence `EV-P1-MUTABILITY-133`: object/mutability transfer correct at confidence 100. The learner
kept the old lowercase string through `copy`, rebound `word` to uppercase, and recognized that both
names for the mutable list observe the appended item. Resume worked-example step C and isolate the
return value of `append`.

Evidence `EV-P2-APPEND-134`: worked-example step C passed at confidence 90. The learner correctly
said `append` mutates `items` and assigns `None` to `returned`. Give the required fresh unaided
step D using `.sort()`, tracking both the changed list and the assigned call value.

Evidence `EV-P2-SORT-135`: fresh worked-example step D passed at confidence 80. The learner
correctly said `.sort()` changes `numbers` into sorted order while assigning `None` to `returned`.
The learner asked whether `.append()` and `.sort()` share this behavior because both are in
Python's library. Explain the API-contract distinction: common mutating-list-method convention,
not a universal library behavior. The original composed trace still needs a fresh target-level
return later.

Evidence `EV-P2-POP-136`: fresh counterexample correct at confidence 100. The learner tracked
`pop()` mutating the list to `['a']` while returning `'b'`. This confirms mutation and return are
separate API-contract choices. Return now to a fresh composed target using `.upper()`, `sorted()`,
and `.sort()`.

Evidence `EV-P2-MUTATION-137`: composed target partial at confidence 100. String values, sorted
contents, separate list identities, and `.sort()` as the sole mutation were all correct. The only
miss was saying `.sort()` assigns the sorted list rather than `None`; the micro recovery did not
survive composition. Ignore missing list brackets per preference. Descend only the failed return
edge to a fresh R1 problem, then climb with one added operation.

After evaluation, the learner corrected `returned` to `None` at confidence 80. This is assisted,
not independent. Proceed with the planned fresh isolated `.sort()` return check.

Evidence `EV-P2-SORT-138`: fresh isolated `.sort()` recovery correct at confidence 100. The
learner independently kept the mutation and `None` return separate. Climb exactly one rung by
adding `sorted(...)` in the same short trace before returning to full composition.

Evidence `EV-P2-SORT-139`: two-operation composition passed at confidence 100. The learner kept
`scores` and `snapshot` as separate list objects with equal contents, identified `.sort()` as the
mutation, and assigned `None` to `outcome`. Give one fresh full target by adding an immutable string
operation.

Evidence `EV-P2-MUTATION-140`: fresh full composition passed at confidence 100. String
immutability, new-list creation, separate list identity, in-place mutation, and `.sort()` returning
`None` all survived together. This completes the target-level recovery. Rotate to the owed Phase 1
branch-precedence enumeration and require one line per input.

Evidence `EV-P1-BRANCH-141`: partial at confidence 100. All reordered outputs were correct, but the
learner grouped inputs 1–3 and omitted the original outputs, changed yes/no decisions, and
explanation. This is the known procedural enumeration gap, not a precedence-model failure. Do not
re-teach. Isolate `"PRO-ANNUAL-TEAM"` in the original function and ask for its first true branch.

Evidence `EV-P1-BRANCH-142`: wrong at confidence 100. Even with one input and "original function
only" stated twice, the learner answered about the reordered version. This is version selection /
prompt reading, not precedence logic. Descend to the single Boolean
`"PRO-ANNUAL-TEAM".startswith("PRO-ANNUAL")`.

Evidence `EV-P1-PREFIX-143`: isolated prefix condition correct at confidence 100. The learner
correctly said the string starts with `PRO-ANNUAL`. Give one fresh single-version bridge in a new
domain to check first-match selection before returning to paired versions.

Evidence `EV-P1-BRANCH-144`: fresh single-version bridge correct at confidence 100. The learner
selected the specific `VIP-GOLD` branch, returned `gold`, and said later branches are skipped.
Return to a fresh paired-version target with four inputs and enforce one complete line per input.

Evidence `EV-P1-BRANCH-145`: paired-version target partial at confidence 90. The learner's
aggregate conclusion was correct—Version B gives `t-code` for inputs 1–3, `BASIC` stays unchanged,
and only items 1 and 2 change. But Version A results and four separate rows were omitted again.
This is procedural enumeration, not branch logic. Isolate one complete A/B/change row.

Evidence `EV-P1-BRANCH-146`: one complete comparison row passed at confidence 100. For
`TEAM-ADMIN-EAST`, the learner explicitly supplied Version A `admin`, Version B `t-code`, and
changed yes. Field order is not graded. Give one fresh same-rung row for `TEAM-MEMBER`.

Evidence `EV-P1-BRANCH-147`: Version A branch selection, Version B `t-code`, and changed yes were
correct at confidence 100. The learner explicitly asked that `team-` versus `team` be disregarded
as a nitpick. Honor that preference: accept the row and do not issue a label-precision drill.
Rotate to a different Phase 2 fundamental.

Evidence `EV-P2-MODEL-148`: Phase 2 representation reasoning partial at confidence 80. Named-field
clarity, positional mix-up risk, and a limited acceptable case for a documented list were all
explained correctly. Automatic validation was explicitly unknown. Isolate the actual plain
`DiffSummary` declaration with a negative value and ask whether construction succeeds; do not run
before prediction.

Evidence `EV-P2-ANNOTATION-149`: partial at confidence 80. The learner correctly predicted that a
plain dataclass accepts `lines_added=-5`, but connected `: int` to the shell. Clarify that the shell
is uninvolved; annotations guide humans and checking tools and do not automatically enforce type
or range in ordinary Python. Give one R1 string-in-an-int-annotated-field prediction.

Evidence `EV-P2-ANNOTATION-150`: R1 recovery correct at confidence 80. The learner predicted that
plain Python creates the dataclass, stores `"five"` unchanged, and performs no conversion from the
`int` annotation. Give one fresh same-rung wrong-type value, then climb to the runtime-validation
design question.

Evidence `EV-P2-ANNOTATION-151`: fresh wrong-type near-transfer correct at confidence 60. The
learner predicted that a plain `int`-annotated dataclass accepts `[1, 2]`, stores it, and prints the
list. Climb to plain-English runtime-contract design: classify candidate count sets as acceptable
or rejectable and name the checks annotations do not perform.

Evidence `EV-P2-VALIDATION-152`: runtime-contract design passed at confidence 100. The learner
accepted the valid counts, rejected the negative count for range, and rejected the string for
type. These explanations supply both required checks, so do not demand a redundant summary. Rotate
to the `splitlines()` family and string immutability.

Evidence `EV-P2-SPLITLINES-153`: full composed transfer passed at confidence 100. The learner
correctly modeled string input, newline-only splitting, no implicit printing, a new returned list,
unchanged source string, and `append()` as the mutation. The `splitlines` misconception family is
recovered at target level for this review. Rotate to a harder loop-accumulator bug.

---

# SESSION CLOSE — 2026-08-28, fundamentals quiz before dinner

## Scope

The learner explicitly limited this quiz to completed Phases 0–2. Phase 3 was not tested, Phase 4
was not started, and no product code was changed.

## Quiz recording rule from the learner

For future review/quiz sessions, append the verbatim questions and learner answers to
`QUIZZES.md` as the session proceeds. Continue using `learning/LEARNING_LEDGER.md` for evaluation,
misconceptions, confidence, and remediation chains.

## Code verification

At session start, all three suites were independently run and passed:

```text
python test_classify.py
python test_summarize.py
python test_session.py
```

## Strong recoveries this session

```text
output_vs_exit_status       output and status are independent; status controls shell/CI verdict
print_vs_return             printing function with no return contributes None
list_equality               compares contents in order
DiffSummary values          files_changed / lines_added / lines_removed computed on fresh diff
mutation_vs_return          append/sort mutate and return None; pop mutates and returns removed item
immutable_vs_mutable        string rebinding versus shared-list mutation
sorted_vs_sort              new list versus in-place mutation; full composed transfer passed
splitlines                  string input, newline splitting, new list, no print, source unchanged
annotations_vs_validation   annotations do not enforce type/range; runtime needs both checks
```

The learner requested that harmless formatting and label transcription not be graded. Continue to
ignore punctuation/spacing unless it changes the concept or runtime value.

## Still developing

```text
per_item_enumeration        aggregate branch conclusions are usually right, but requested A/B/change
                            rows are repeatedly omitted. One complete row passed; the four-row target
                            was not independently completed.

sort_return_under_load      recovered through worked example and full composed transfer. Retrieve
                            after a delay; do not drill immediately.

confidence_tags             repeatedly omitted and supplied after reminder.
```

## New open blocker

Evidence `EV-P1-ACCUMULATOR-154`, confidence 80:

```text
count = +1    was read as incrementing the old count
count += 1    was described as a spacing correction
```

Actual loop states were `1, 1, 1, 1`, not `1, 1, 2, 3`. Remediation was deliberately deferred
because the learner said this was the last question before dinner.

Important correction: the learner independently supplied `count += 1` in the first answer. The
fix itself is correct and unassisted. What remains open is why `+=` works, why it is not a spacing
variant, and tracing the buggy `= +1` loop.

NEXT SESSION MUST BEGIN HERE:

```text
R0  distinguish `x = +1` from `x += 1` as separate operators/forms
R1  one sequential near-transfer
R3  one small conditional accumulator
R6  fresh loop accumulator target
```

Do not treat this wrong attempt as a phase failure.

## Next implementation step

None. The learner requested quiz-only work on Phases 0–2. Phase 4 remains out of scope.

## QUIZ RESUMED — 2026-08-28

Evidence `EV-P1-ACCUMULATOR-155`: at confidence 100, the learner correctly predicted
`count = +1` ends at `1` and `count += 1` ends at `6` from a starting value of `5`. Mechanism
explanation and explicit different-form statement were omitted; require that teach-back before
climbing. New quiz transcripts are now also being appended to `QUIZZES.md`.

Evidence `EV-P1-ACCUMULATOR-156`: mechanism teach-back correct at confidence 90. The learner
distinguished `= +1` from `+= 1` and requested harder questions. End micro-scaffolding and return
directly to a fresh target-level two-call accumulator trace.

Evidence `EV-P1-ACCUMULATOR-157`: harder two-call accumulator trace fully correct at confidence
90: states `2,2,3` and `1,3,5`, returned values `3` and `5`, printed sum `8`. The learner omitted
the explanation of fresh local state twice. Ask that as a conceptual lifetime/ownership question;
do not repeat accumulator arithmetic.

Evidence `EV-P1-LOCAL-158`: local-state explanation correct at confidence 90. The learner said
`score = 0` runs at the start of every call before the loop. The accumulator blocker is recovered
at target level. Rotate to a harder debugging transfer involving external state leaking across
calls.

External-state target paused when the learner could not read `{"added": 0}` and asked whether its
colon was a dataclass annotation. Evidence `EV-P1-DICT-159`: syntax-only lookup partial at
confidence 90. Printed value `2` and key/value association were understood, but the learner said
the lookup retrieves the key. Ask one fresh lookup result only; do not resume the target yet.

Evidence `EV-P1-DICT-160`: fresh lookup correct at confidence 100. The learner separately named
the key `"retries"`, retrieved value `3`, and assignment to `value`. Give one dictionary-entry
`+= 1` bridge, then resume the external-state target.

Evidence `EV-P1-DICT-161`: dictionary-entry arithmetic correct at confidence 40: the learner
looked up `0`, added one, and stored `1`. Whether this mutates or replaces the dictionary was
explicitly unknown. Explain that subscript assignment mutates the existing mapping, then test it
through an alias before resuming the target.

Evidence `EV-P1-DICT-162`: dictionary alias transfer wrong at confidence 40. Despite the
same-object diagram, the learner said `totals["added"] += 1` creates a new dictionary and leaves
the alias at zero. Descend to the already-familiar list alias case with one indexed replacement,
then transfer back to dictionaries gradually.

Evidence `EV-P1-ALIAS-163`: list alias prerequisite correct at confidence 90. The learner said
`numbers[0] = 1` mutates the shared list and `alias[0]` sees `1`, while explicitly asking how
`"apples": 3` connects to prior concepts. Give a direct index-to-value versus key-to-value
comparison, then one dictionary alias update.

Evidence `EV-P1-ALIAS-164`: indexed list alias transfer wrong at confidence 30. The learner said
`alias` keeps `3` because only "the list for numbers" changed, revealing a copied-container model.
Descend to R0: ask whether `alias = numbers` creates one or two list objects before any mutation.
Dictionary target remains paused.

Evidence `EV-P1-ALIAS-165`: R0 list object-count recovery correct at confidence 100. The learner
said one list exists with both names pointing to it. Transfer the same object-count question to a
dictionary before reintroducing entry mutation.

Evidence `EV-P1-DICT-166`: line-by-line dictionary state movie passed at confidence 90. The
learner created one object and correctly bound `alias` to the same object, though called the
dictionary a list. The learner's own diagnosis—"adding the one extra step throws me off"—matches
the evidence: individual rules are stable, composition tracking fails. Continue with explicit
state freezing and add exactly one mutation step.

Evidence `EV-P1-DICT-167`: three-line dictionary alias mutation passed at confidence 90. The
learner kept one shared object and correctly said both names see value `4`. Container terminology
was inconsistent, but the identity/state model was explicit and accepted under the no-nitpicking
preference. Fade filled state prompts and give a harder shared-counter transfer.

Evidence `EV-P1-DICT-168`: composed shared-counter transfer passed at confidence 90 without filled
state prompts. The learner tracked two updates through three names and correctly concluded all
lookups return `5`. Dictionary alias mutation is recovered sufficiently to resume a fresh
external-state function target.

Evidence `EV-P1-EXTERNAL-169`: fresh external-state target partial at confidence 90. The learner
correctly derived `first=1`, `second=3`, explained why the second call inherits external state,
and proposed moving initialization inside the function. `print(first, second)` was read as sum `4`,
and purity was explicitly unknown. Remediate output first with a bare two-argument print, then
isolate purity.

Learner correction to grading: disregard the two-argument `print` slip as "just blind." Honor it;
do not remediate output. Isolate purity only: the function mutates external `stats` while leaving
the input `events` list unchanged.

Evidence `EV-P1-PURITY-170`: purity judgment wrong at confidence 90. The learner checked that
inputs remain unchanged but missed mutation of a separate external dictionary. Evidence
`EV-P1-PURITY-171`: after contrasting external and local counters, the learner correctly explained
that the external version is impure and the fresh-local version is pure, confidence 90. Retrieve
later in a new domain; do not drill immediately.

## SESSION HANDOFF — location change, 2026-08-28

The learner requested a push before moving locations. Quiz remains limited to completed Phases
0–2; no product code changed. New questions and answers were recorded in `QUIZZES.md` as requested.

Strongest new results:

```text
accumulator target       two-call loop trace and local reset explanation passed
dictionary mapping       key/value lookup and shared mutation recovered through state movies
purity                   external versus local counter contrast passed
```

Still due after a delay:

```text
composition tracking     learner explicitly said one extra step causes loss of earlier state;
                         line-by-line state freezing worked
purity transfer          new domain with a complete scan of all external objects
per-item enumeration     aggregate branch answer remains easier than complete rows
```

Next session should not restart syntax drills cold. Begin with one moderately composed state movie,
then fade the table if correct.

## QUIZ CONTINUED — 2026-08-29

The learner requested exactly three final super-hard Phase 0–2 questions before returning to the
Phase 3 milestone. Super-hard question 1 (`EV-P1-COMPOSE-172`) was partial at confidence 90.
Longest-prefix control flow, printed `unknown`, implicit `None`, alias mutation, and per-call local
reset were traced well. Under full composition, the learner changed looked-up numeric values back
into dictionary keys, dropped `None` from the final lists, judged the caller pure despite its called
function printing, and overcounted function-local dictionaries. Per the mandatory remediation rule,
give one short value/object-count checkpoint, then resume super-hard question 2 rather than opening
a long drill.

Evidence `EV-P1-COMPOSE-173`: the required short checkpoint passed at confidence 60. The learner
correctly stated that dictionary lookups supply values, both calls return `[2, 1]`, and two calls
create two dictionaries plus two lists. Resume full complexity with super-hard question 2 of 3.

Evidence `EV-P1-COMPOSE-174`: super-hard question 2 was wrong at confidence 60. The
learner correctly identified impurity, aliases, `sorted()` producing a separate list, both popped
values, and shared report mutation. Under composition, `.sort()` was incorrectly treated as a
non-mutating operation returning a sorted list. This propagated through the final states and object
count. The learner paused for lunch and requested a push. On return, mandatory remediation is one
short `.sort()` versus `sorted()` checkpoint, then one near-transfer with an alias. Super-hard
question 3 of 3 remains unasked; do not move to Phase 3 until it and any necessary recovery finish.

Evidence `EV-P1-SORT-175`: at confidence 90, the learner correctly recovered that `.sort()` mutates
the existing list and returns `None`, while `sorted()` returns a separate sorted list without
mutating its input. The exact list contents and count of two list objects were omitted. Ask one
compact completion check for only those details, then give the required alias near-transfer before
super-hard question 3 of 3.

The `EV-P1-SORT-175` completion check passed: the learner independently stated that `values` and
`separate` both contain `[1, 2, 3]`, are different list objects, and that two list objects exist.
The isolated recovery is complete. Next: one alias near-transfer, then super-hard question 3 of 3.

Evidence `EV-P1-ALIAS-176`: the required alias near-transfer passed at confidence 100. The learner
correctly traced `.sort()` mutation through a shared alias, its `None` return, the distinct list
created by `sorted()`, and the total of two list objects. The super-hard question 2 remediation chain
is complete. Next: super-hard question 3 of 3, with no state table; retrieve per-item branches,
mutation/aliasing, return values, and purity in a fresh domain.

Evidence `EV-P1-COMPOSE-177`: the learner committed a trace for super-hard question 3 of 3 but
omitted the required confidence score. Evaluation and all correction are withheld until confidence
is committed. Do not replace or rewrite the verbatim first answer.

The confidence follow-up for `EV-P1-COMPOSE-177` was 50. Result: partial. The learner correctly
traced the first call's three route results, fallback print/implicit `None`, cumulative shared
counters, alias mutation, `.sort()` returning `None`, a separate snapshot, impurity, and two
`unknown` prints. The primary blocker was exact mixed-case string sort order: lowercase-leading
`mystery` was placed before uppercase-leading `P1...`, which corrupted the second-call order.
Complete nested return values, final output, list-object count, full purity inventory, and shared
principle were unfinished. Descend to one R1 mixed-case sort prediction, then near-transfer and a
simplified fresh target completion. Do not reveal the full answer yet or advance Phase 3.

Evidence `EV-P1-SORT-178`: the learner committed an intended ordering for the R1 mixed-case sort and
explicitly said they were unsure how case affects it, but omitted confidence. Evaluation is pending
the required 0–100 score. Do not penalize the harmless `banan` transcription.

The `EV-P1-SORT-178` confidence follow-up was 80. The intended result
`["Apple", "Banana", "mango"]` was correct; the harmless transcription typo was ignored. Mechanism
remains uncertain: Python's default ordering is case-sensitive and uppercase-leading English words
precede lowercase-leading words in this exercise. Ask one two-item case-only check before a
same-prefix near-transfer.

Evidence `EV-P1-SORT-179`: the learner committed an intended two-item ordering and identified
uppercase as the reason, then asked whether `you = sorted(oil)` uses the same idea. Confidence is
still required before evaluation and feedback. Ignore the harmless `banan` transcription.

The `EV-P1-SORT-179` confidence follow-up was 60 and the check passed. The learner correctly placed
uppercase-leading `Banana` before lowercase-leading `apple`. Clarified that `.sort()` and `sorted()`
use the same default ordering, while `.sort()` mutates/returns `None` and `sorted()` creates a new
list without changing its input. Next: one same-prefix `sorted()` near-transfer, then rebuild the
unfinished target trace.

Evidence `EV-P1-SORT-180`: the same-prefix near-transfer passed at confidence 100. The learner
correctly preserved the input list, ordered the new list as `["place", "plan", "plate"]`, and counted
two list objects. The explicit deciding letters `c`, `n`, `t` were omitted, but the learner requested
to move on and the actual ordering was correct. Sorting remediation is complete; do not add another
isolated sort drill. Return to the unfinished `EV-P1-COMPOSE-177` trace with the recovered ticket
order supplied.

`EV-P1-COMPOSE-177` completion continuation: the learner correctly gave final stats
`{"escalated": 2, "unknown": 2}`, second-call labels `["escalated", "urgent", None]`, and the intended
`second` nested value. Clarify identity: first-call `alias` refers to original `tickets`; second-call
`alias` refers to the distinct list at `first[2]`. Still require only the remaining outer output,
seven-list object count, complete impurity inventory, shared principle, and completion confidence.

The `EV-P1-COMPOSE-177` completion confidence follow-up is 80. Do not retrace counters or sorting;
ask only for final object/effect/principle accounting and concise outer-output confirmation.

`EV-P1-COMPOSE-177` completion continuation 2: the learner asked what "five outer print results"
means, counted two list objects, identified only original-list mutation as an impurity reason, and
did not retrieve the earlier alias principle. Clarify that outer output means the five bottom-level
prints, excluding `route`'s internal prints. Then ask only `print(tickets)`. Primary blocker is
whole-program list identity/counting; after output clarification, rebuild allocations at R2 one
statement/call at a time. Do not reveal all remaining answers together.

Completion-continuation confidence: 30.

Output recovery 1 passed at confidence 30: the learner correctly gave `print(tickets)` as shorthand
`[p1+, p1-, mystery]`. Next ask only `print(same)` plus the identity reason.

Output recovery 2 value passed at confidence 60: `same` displays the same sorted list. Ask only for
the shared-object reason before continuing.

Alias explanation passed at confidence 60: the learner independently stated that `same`, `tickets`,
and the first call's `alias` all point to one list object. The shared identity/mutation principle is
recovered. Next: count lists only through the end of the first call, explicitly separating aliases
from allocation expressions.

First-call object-count attempt: the learner correctly identified `alias = tickets` as non-allocating
and identified `labels` and `snapshot` as separate lists. Confidence was omitted. After confidence,
isolate whether `return [labels, status, snapshot]` creates another outer list.

First-call object-count confidence: 70. Result partial because the outer list literal in
`return [labels, status, snapshot]` was not counted. Ask only about that literal before recomputing
the first-call total.

Outer-list micro-check: the learner now recognizes that the return list literal creates a new outer
list and reports nested-list representation as somewhat new. Confidence and exact elements remain.
After this topic closes, the learner requested a verified commit/push and updated handoff before
moving locations.

Outer-list confidence: 70. The learner independently recovered that the return literal allocates a
new outer list. Clarified its mixed contents: references to `labels` and `snapshot`, with `None` in
the middle. Next ask first-call total from the four named objects, then transfer the three-new-lists
per-call pattern to call two and close/publish.

The learner correctly adopted the mixed-object outer-list terminology. First-call numeric list count
and confidence remain; ask only for those two fields.

First-call object-count follow-up at confidence 90: the learner correctly described the returned
outer list's elements as two list references plus `None`, but substituted element count for total
object count and omitted the original/outer lists. Repeated difficulty now permits one worked
neighboring example. Require explanation of that example before returning to BuildLens.

## SESSION HANDOFF — location change, 2026-08-29 (super-hard question 3 recovery)

The learner requested an immediate commit/push and paused after seeing, but before explaining, this
worked neighboring example:

```python
base = [1]
inner = []
wrapper = [inner, None]
```

The modeled count is three lists: `base`, `inner`, and `wrapper`. On return, do not lecture or reveal
the BuildLens total. Ask exactly: "In your own words, why is the count three rather than one or
four?" Then require one missing allocation step and a fresh independent micro-example before
returning to the BuildLens first-call and whole-program counts.

Current quiz status:

- super-hard question 1 was partial; its recovery passed;
- super-hard question 2 was partial/wrong; `.sort()`/`sorted()` recovery and alias transfer passed;
- super-hard question 3 (`EV-P1-COMPOSE-177`) remains partial;
- routing, counters, sorted state, second-call labels, alias principle, and core return values were
  recovered;
- exact whole-program list-object counting and the complete impurity inventory remain open;
- no product code changed and Phase 3 may not advance yet.

Concepts demonstrated this session include `.sort()` mutation/`None`, `sorted()` allocation,
case-sensitive and same-prefix ordering, mutation visibility through aliases, cumulative dictionary
counters, longest-prefix routing, and implicit `None`. Do not mark nested object counting mastered.

Next retrieval due: the worked-example explanation above.
Next architecture reset due: unchanged; this was a Phase 0–2 fundamentals quiz.
Next implementation step: unchanged and blocked behind completion of the current learning gate.
Files the learner should be able to teach remain the completed Phase 0–2 implementation files; the
new uncertainty is nested list identity/allocation counting, not product behavior.
