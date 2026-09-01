# BuildLens — Current State

> **Maintenance rule:** this file is a replace-in-place snapshot, not a session log. Update or remove
> obsolete statements whenever state changes. Preserve historical prompts, answers, remediation, and
> rationale in `learning/LEARNING_LEDGER.md`, `QUIZZES.md`, and Git history.

Last updated: 2026-08-29

## Lifecycle

**Current phase:** Phase 5 complete. The mandatory cumulative foundation review is now due before
substantial Phase 6 work; no Phase 6 product implementation is authorized yet.

Phase 3 is complete in every required dimension:

```text
implementation       complete
automated tests      complete
learner trace        complete
knowledge gate       complete
learner explanation  complete — EV-P3-TEACH-185
transfer variant     complete — EV-P3-TRANSFER-186
```

The formal Phase 0–2 cumulative checkpoint and pre-Phase-4 architecture reset are also complete.

Phase 4 completed without a product patch:

```text
cross-module value trace                complete — EV-P4-READ-191
module responsibility/dependency audit complete — EV-P4-ARCH-192
unrelated decomposition transfer       complete — EV-P4-TRANSFER-193
refactor decision                       keep existing flat modules
```

Phase 5 is complete in every required dimension:

```text
implementation       complete — EV-P5-SESSION-IMPLEMENTATION-248
automated tests      complete — EV-P5-COMPLETE-259
learner trace        complete — EV-P5-SESSION-POSTPATCH-TRACE-249
learner explanation  complete — EV-P5-ANNOTATION-VALIDATION-250
transfer variant     complete — EV-P5-RETRY-TRANSFER-COMPLETE-258
```

## Exact code that exists

### `classify.py`

`classify_diff_line(line)` accepts one unified-diff line and returns exactly one label.

```text
"diff --git"                              → file_header
"index ", "--- ", "+++ ", or "@@"       → metadata
leading "+"                               → added
leading "-"                               → removed
otherwise                                 → context
```

The most-specific prefixes come first. The input and outside state remain unchanged.

### `summarize.py`

`DiffSummary` is a dataclass with `files_changed`, `lines_added`, and `lines_removed`.

`summarize_diff(diff_text)` follows:

```text
one complete diff string
→ splitlines()
→ classify each line through classify_diff_line
→ increment three fresh local counters
→ return one DiffSummary
```

Only `file_header`, `added`, and `removed` affect counters. Metadata and context do not.

Dependency direction:

```text
summarize imports/calls classify
summarize depends on classify
classify is a dependency of summarize
```

### `session.py`

```python
class Session:
    def __init__(self):
        self._changes: list[str] = []

    def record(self, diff_text: str) -> None:
        if not isinstance(diff_text, str):
            raise TypeError("must be a string")

        self._changes.append(diff_text)

    def history(self) -> list[str]:
        history_list = list(self._changes)
        return history_list
```

Each construction creates a fresh internal `_changes` list. Supported writes go through `record`,
which declares `str`, explicitly validates at runtime, and raises `TypeError("must be a string")`
before mutation for a non-string. Valid strings append in order and the method returns `None`.
`history` declares and returns a fresh `list[str]` snapshot without rescanning elements. The
string-only guarantee is deliberately scoped to supported API paths, not arbitrary Python
introspection of `_changes`.

## Automated verification

```text
python test_classify.py   — 8 test functions
python test_summarize.py  — 1 end-to-end summary test function
python test_session.py    — 7 test functions
```

All three passed locally after the Phase 5 Session contract patch on 2026-08-31.

Load-bearing Session tests include:

- `test_mutating_the_history_does_not_touch_the_session` for snapshot identity;
- `test_mutable_storage_is_not_public` for removal of the supported public mutation bypass;
- `test_rejecting_non_string_input_preserves_history` for exact error behavior and
  rejection-before-mutation.

## Current execution paths

```text
diff line → classify_diff_line → one label
```

```text
complete diff string
→ split into lines
→ classify each line
→ update local counters
→ DiffSummary
```

```text
Session()
→ fresh instance-owned changes list
→ record(diff_text) mutates that list in order
→ history() returns a separate snapshot
```

## Current architecture decision

Keep the repository's current flat module structure.

Evidence:

- each responsibility currently fits in one module;
- no observed navigation, naming, boundary, or import problem exists;
- all three suites pass;
- creating `backend/`, `tests/`, or a package now would cause guaranteed path/import churn for a
  speculative benefit.

Accepted downside: waiting may require file moves and import changes later.

Reversal condition: restructure when one responsibility genuinely needs several related modules and
flat placement obscures ownership/naming, or when another concrete package/import requirement appears.

Vocabulary:

```text
module          one Python file
responsibility  the job/reason that module exists
dependency      another module it uses
boundary        what belongs inside/outside that responsibility
package         a directory/namespace grouping related modules
cohesion        how strongly code serves one responsibility
```

## Learning evidence snapshot

Demonstrated through delayed or transferred retrieval, but not permanently mastered:

- branch precedence and exact context-line classification;
- output versus return values and per-call local state;
- `.sort()` mutation/`None` versus `sorted()` allocation;
- aliases, copies, object identity, and outer-list allocation;
- shared dictionary state versus local counters;
- transitive observable effects through called functions;
- triple-quoted physical newlines and `splitlines()`;
- explicit dataclass return versus implicit `None`;
- per-instance Session state, snapshots, tests, and public-attribute limitation;
- evidence-first architecture timing, dependency direction, downside, and reversal conditions.
- cross-module tracing from caller to classifier and back to caller-local aggregation;
- decomposition transfer outside the diff domain.

Still uncertain or due for later retrieval:

- retaining every object/allocation under heavy composition without a state freeze;
- confidence calibration: several correct answers were underconfident and some misses were reported
  at confidence 100;
- current code does not coerce or validate `diff_text` as a string;
- shallow-copy depth when mutable elements are introduced later.
- keeping documented contracts, type annotations, explicit validation, and incidental runtime
  failures distinct under composed function/branch traces;
- confidence calibration after incompatible-input predictions changed at confidence 90–100.
- recently introduced tuple syntax/immutability; representation and unsupported `.append()` were
  recovered but need later retrieval outside the remediation chain;
- wording deliberate validation as code that runs after function entry but before protected main
  work, rather than “before the function executes.”

## Last completed gates

- Phase 3 state movie and alias/copy knowledge gate: complete.
- `session.py` learner teach-back: complete (`EV-P3-TEACH-185`).
- Unrelated `InspectionLog` snapshot transfer: complete (`EV-P3-TRANSFER-186`).
- Formal foundation cumulative review: complete (`EV-CUM-FND-187` through `190`).
- Pre-Phase-4 architecture reset: complete (`EV-CUM-FND-190`).
- Phase 4 cross-module reading audit: complete (`EV-P4-READ-191`).
- Phase 4 responsibility/dependency explanation: complete (`EV-P4-ARCH-192`).
- Phase 4 unrelated decomposition transfer: complete (`EV-P4-TRANSFER-193`).
- Phase 5 documented-contract versus runtime-enforcement recovery: fresh target passed after
  adaptive descent and rebuild (`EV-P5-CONTRACT-194`); broader boundary audit remains open.
- Phase 5 `summarize_diff(42)` cross-module boundary and transfer: complete after syntax and
  terminology remediation (`EV-P5-BOUNDARY-195`, `EV-P5-BOUNDARY-TRANSFER-196`).
- Phase 5 exact `summarize.py` ↔ `classify.py` interface trace: complete after local/instance-state
  remediation (`EV-P5-INTERFACE-197`).
- Phase 5 `Session.record` / `Session.history` contract audit: first target attempt recorded
  (`EV-P5-SESSION-CONTRACT-198`); the R2 snapshot-source micro-example passed at confidence 100
  (`EV-P5-SESSION-SNAPSHOT-199`), and the intervening-state-mutation near-transfer passed at
  confidence 100 (`EV-P5-SESSION-NEAR-TRANSFER-200`). Return-value/type recovery remains open.
- The fresh full Session audit remained partial (`EV-P5-SESSION-CONTRACT-201`): instance mutation
  and snapshot identity were correct, while implicit return, exact types, assumptions, and validation
  remain open.
- The first exact implicit-return choice was `""` and was incorrect (`EV-P5-RETURN-202`). Remediation
  descended to R0; after a second incorrect guess of `[]`, explicit `return []` syntax was traced
  correctly at confidence 90 (`EV-P5-RETURN-SYNTAX-203`). A fresh no-return function is next.
- The fresh no-return function was described as a blank at confidence 20
  (`EV-P5-IMPLICIT-RETURN-204`). After repeated difficulty, worked-example rescue is active:
  `None` / `NoneType` has been modeled and must now be explained, partially completed, and retrieved
  in a fresh example.
- The learner explained the worked example correctly at confidence 90
  (`EV-P5-IMPLICIT-EXPLAIN-205`), distinguishing `None` from string/list values. One missing-step
  completion is next before fresh unaided retrieval.
- The missing-step mutation example was completed correctly at confidence 90
  (`EV-P5-IMPLICIT-PARTIAL-206`): the learner supplied `None` and `NoneType`. Fresh unaided
  retrieval is next.
- Fresh unaided retrieval with list mutation passed at confidence 100
  (`EV-P5-IMPLICIT-FRESH-207`): mutation and implicit `None` / `NoneType` were separated correctly.
  Near-transfer to `Session.record` is next.
- The `Session.record("diff Z")` near-transfer produced the correct state, `None`, and `NoneType` at
  confidence 90 (`EV-P5-RECORD-RETURN-208`); the requested causal explanation was omitted and needs
  one concise completion.
- The causal explanation was completed correctly at confidence 90 (`EV-P5-RECORD-EXPLAIN-209`),
  closing implicit-return remediation. The learner additionally called `record` more secure because
  it uses `self`; method encapsulation versus actual validation/access control is now isolated.
- The method-versus-direct-append comparison passed at confidence 100
  (`EV-P5-ENFORCEMENT-210`): both paths accept `7` and reach `[7]`; neither validates today, while
  `record` remains a possible future validation boundary.
- The restored full Session audit was partial at confidence 80 (`EV-P5-SESSION-CONTRACT-211`):
  implicit returns and snapshot identity were correct, but exact types, runtime acceptance,
  mutation/validation details, and whether a documented contract exists without enforcement were
  omitted or ambiguous.
- The contract-versus-validation clarification remained contradictory at confidence 100
  (`EV-P5-CONTRACT-EXISTENCE-212`): no runtime validation and possible contract-without-validation
  were recognized, but the quoted documented string contract was denied. Remediation descends to
  one generic contract sentence.
- The generic documented-contract sentence was recognized correctly at confidence 80
  (`EV-P5-CONTRACT-GENERIC-213`): intended integer input and lack of implied validation were
  separated. Near-transfer back to Session is next.
- Session near-transfer passed at confidence 100 (`EV-P5-CONTRACT-SESSION-214`): documented string
  elements, absent runtime validation, accepted integer storage, and the resulting concrete contract
  mismatch were all identified.
- The full contract synthesis was partial at confidence 90 (`EV-P5-SESSION-SYNTHESIS-215`): mutation,
  returns, list contents, identity, and absent validation were mostly correct. Exact `NoneType`,
  arbitrary-object acceptance, no caller-supplied `history` input, non-mutation by `history`, and
  “stored-element assumption” remain incomplete. The learner also exposed that `record` lacks a
  method-specific docstring/type annotation while the module contract implies string elements.
- The generic stored-element-assumption micro-check passed at confidence 90
  (`EV-P5-ASSUMPTION-216`): expected temperature-number elements were separated from absent history
  validation. Apply the term back to Session next.
- The concise Session field repair remained partial at confidence 90
  (`EV-P5-SESSION-FIELDS-217`). Correct: `history` non-mutation, list return, and no validation.
  Still conflated: method-specific versus module-level documentation, examples versus arbitrary
  runtime acceptance, return value versus type, implicit `self` versus caller-supplied input, and
  copy behavior versus stored-element assumption. Remediation splits these field families.
- Documentation scope was recovered at confidence 70 (`EV-P5-DOC-SCOPE-218`): `record` has no
  method-specific declared input type, while the module contract intends a list whose elements are
  diff-text strings.
- Return value versus type was recovered at confidence 100 (`EV-P5-RETURN-TYPE-219`): `None` is the
  value and `NoneType` is its type.
- Caller-input versus implicit-`self` audit was partial at confidence 90 (`EV-P5-CALL-INPUT-220`):
  automatic `self` binding was recognized, but “arguments explicitly written inside parentheses”
  was unreadable. Syntax-only R0 remediation is active.
- The first syntax micro-check correctly counted explicit argument `5` as one, but denied that the
  receiver `box` is automatically bound to `self` (`EV-P5-CALL-SYNTAX-221`, confidence 60). Continue
  with one receiver/parameter binding map.
- The receiver/parameter binding map passed at confidence 90 (`EV-P5-CALL-BINDING-222`): `self` was
  bound to `box`, `amount` to `5`, with one explicit caller argument. One fresh zero-argument method
  call remains before returning to `history()`.
- The fresh zero-explicit-argument method call passed at confidence 90 (`EV-P5-CALL-FRESH-223`):
  `self` bound to `log` and the caller supplied zero arguments. Apply this result to
  `session.history()` without further syntax remediation.
- Runtime acceptance was generalized correctly in `EV-P5-RUNTIME-ACCEPTANCE-224`: `record` accepts
  any Python object because it only forwards the value to `list.append` and performs no validation.
  Confidence was supplied afterward as 90.
- The faded integrated teach-back was strong but incomplete at confidence 90
  (`EV-P5-SESSION-TEACHBACK-225`): intended strings, arbitrary-object acceptance, snapshot protection,
  and public-state risk were correct. Exact `record` return and `history` input/output were omitted,
  while “all functions need validation” remains an untested design conclusion.
- The two-sentence completion was behaviorally correct at confidence 90
  (`EV-P5-SESSION-COMPLETION-226`): `record` mutation/`None`/`NoneType`, zero explicit history
  arguments, and copied-list identity were recovered. Only the exact built-in type name needs
  correction from `listtype` to `list`.
- The exact history sentence was corrected (`EV-P5-SESSION-EXACT-227`): zero explicit arguments,
  return type `list`, and a copied/different list object. The Session target audit is complete after
  remediation; the required different-surface transfer remains.
- The TemperatureLog different-surface transfer was strong partial at confidence 90
  (`EV-P5-TEMPERATURE-TRANSFER-228`): final state/snapshot values, arbitrary-object acceptance,
  absent validation, float-contract mismatch, and shared Session principle were correct. Add return
  values/types, declaration scope, snapshot validation/protection, and validation placement remain.
- Transfer completion remained partial at confidence 90 (`EV-P5-TEMPERATURE-COMPLETION-229`):
  `None` values, float intent, absent snapshot validation, and an add-only validation proposal were
  supplied. `NoneType`, absent method-specific declaration, exact copy protection, and the public
  direct-mutation bypass remain. Challenge the add-only proposal adversarially.
- The adversarial public-mutation challenge passed at confidence 90
  (`EV-P5-TEMPERATURE-BYPASS-230`): invalid state bypasses add validation, snapshot returns it, and
  add-only validation cannot guarantee a class-wide float invariant. The learner independently
  proposed per-element snapshot checking, exposing prevention-at-write versus detection-at-read.
- The learner selected a class-wide supported-path string invariant at confidence 90
  (`EV-P5-SESSION-DECISION-231`): prevent non-string Session state so `history` need not rescan.
  The answer mistakenly said `record` would not validate; correction is required because `record`
  must enforce the chosen write boundary.
- The corrected contract was approved at confidence 90 (`EV-P5-SESSION-CONTRACT-232`): supported
  writes go through `record`, which validates strings; mutable storage becomes internal; `history()`
  returns a copy without rescanning. The guarantee is limited to supported API paths. A product patch
  is now justified but has not been authorized or written.
- The required pre-patch rejection prediction was partial at confidence 40
  (`EV-P5-REJECTION-233`): `TypeError`, the pre-rejection `["diff A"]` snapshot, and uncaught
  exception control-flow interruption were recognized, but exception message, process exit status,
  post-rejection object state, return behavior, and snapshot contract were conflated or omitted.
  Adaptive remediation descends to one caught-exception validation branch before implementation.
- The caught-exception micro-trace was unreadable (`EV-P5-EXCEPTION-MICRO-234`) because it introduced
  `try`, `raise`, `except`, exception binding, and inspection syntax together. Syntax-only help is
  active at R0: read one `raise TypeError("...")` form before rebuilding control flow.
- The first R0 raise-syntax read was partial at confidence 90 (`EV-P5-RAISE-SYNTAX-235`): the
  learner identified `TypeError` but copied the modeled message instead of the fresh message and
  asked whether `raise` checks or signals. Clarify that a condition checks while `raise` actively
  signals the explicitly named exception, then use one fresh R0 line.
- The raise/check concept was recovered at confidence 90 (`EV-P5-RAISE-CONCEPT-236`): the learner
  independently proposed checking for a non-string and then raising `TypeError` with a requirement
  message. Exact `isinstance`/`not` syntax and one branch trace are next.
- The first exact condition-plus-raise trace passed at confidence 100 (`EV-P5-RAISE-BRANCH-237`):
  integer `7` made the negated string check true and produced the exact `TypeError` and message.
  One fresh opposite-branch trace with hints removed is next before adding state.
- The fresh valid-input opposite branch passed at confidence 100 (`EV-P5-RAISE-OPPOSITE-238`): the
  raise was skipped and the later assignment executed. Advance one rung to rejection before a list
  mutation.
- The next rejection-before-list-mutation trace was presented but not answered because the learner
  needed to relocate. Resume with the exact preserved `items = ["A"]`, `value = 7` prompt; do not
  reveal its answer or implement the Session patch first.
- The resumed rejection-before-mutation trace passed at confidence 100
  (`EV-P5-REJECTION-STATE-239`): the learner explained that `TypeError` is raised before `append`,
  so the existing list remains unchanged. One different-surface near-transfer is next before
  rebuilding to the Session `record(7)` prediction.
- The learner immediately recognized the job-queue near-transfer as the same control-flow structure
  under different names (`EV-P5-REJECTION-TRANSFER-240`). Do not require a redundant field table;
  ask for the shared deep principle, then return to the Session prediction.
- The shared rejection-before-mutation principle passed at confidence 100
  (`EV-P5-REJECTION-PRINCIPLE-241`): validation stops execution before append, preserving prior
  state. Return now to the exact Session `record(7)` pre-implementation prediction.
- The restored Session rejection prediction was strong partial at confidence 100
  (`EV-P5-SESSION-REJECTION-242`): `TypeError`, no normal return, unchanged `["diff A"]` state, and
  rejection-before-append causality were correct. Correct “record never executes” to “record enters
  and raises before mutation,” supply the snapshot returned by a later handled-error history call,
  and choose an exact stable message before implementation.
- The concise completion was partial at confidence 80 (`EV-P5-SESSION-REJECTION-COMPLETION-243`):
  method entry/raise and fixed message `"must be a string"` were correct, but `None` was incorrectly
  transferred from `record` to a later `history()` call. Descend to one direct `list(...)` result,
  then a tiny snapshot method, before returning to Session.
- The direct-copy micro-check produced the correct conceptual question
  (`EV-P5-HISTORY-COPY-MICRO-244`): a later list operation returns a copy of the state that existed
  before rejection. Clarify that rejection preserves state while the later call creates the copy;
  exact value/type/identity terminology is next.
- The copied snapshot type and distinct identity passed at confidence 100
  (`EV-P5-HISTORY-COPY-IDENTITY-245`); only the exact contents `["diff A"]` were omitted. Request
  that one value, then return directly to Session history after rejection.
- The exact copied-list value was recovered at confidence 100 (`EV-P5-HISTORY-COPY-EXACT-246`):
  `["diff A"]`, with distinct identity from stored. Return now to the single Session history field.
- The returned Session history field passed at confidence 100 (`EV-P5-SESSION-HISTORY-247`): after
  invalid input is rejected before mutation, `history()` returns a distinct `list` with exact value
  `["diff A"]`. The pre-implementation rejection/state gate is complete; the approved focused
  Session patch may begin.
- The implemented Session valid-write/rejected-write/snapshot path passed at confidence 100
  (`EV-P5-SESSION-POSTPATCH-TRACE-249`): exact return/error behavior, unchanged internal state,
  mutated snapshot, fresh history, and distinct identity were traced correctly. Require the concise
  annotation-versus-runtime-validation explanation next, followed by a fresh transfer.
- The annotation-versus-runtime-validation explanation passed at confidence 100
  (`EV-P5-ANNOTATION-VALIDATION-250`): annotations communicate but do not enforce here; the
  `isinstance` branch raises, and without it an integer would append. One fresh different-surface
  transfer remains before Phase 5 completion can be evaluated.
- The RetryPolicy transfer was unreadable (`EV-P5-RETRY-TRANSFER-251`) because the complete class
  introduced unfamiliar syntax at once. Syntax-only help is active at R0 for the annotated instance
  collection line `self._limits: list[int] = []`; do not solve the transfer yet.
- The annotated instance-list concept was read correctly at confidence 80
  (`EV-P5-INSTANCE-LIST-SYNTAX-252`): instance ownership, intended element type, and empty-list
  allocation were identified. Refine `_limits` as the attribute name, then use one fresh same-form
  line before rebuilding the transfer.
- The fresh `_labels: list[str] = []` read passed at confidence 90
  (`EV-P5-INSTANCE-LIST-FRESH-253`): attribute, element intent, actual list allocation, and absent
  runtime enforcement were all correct. Isolate the `-> list[int]` return annotation next.
- The return-arrow read was partial (`EV-P5-RETURN-ANNOTATION-254`): lack of automatic runtime
  enforcement was recognized, but the annotation was called functionally meaningless. Require the
  narrower distinction: it communicates/supports tooling but does not automatically enforce.
- The communication role was supplied (`EV-P5-RETURN-ANNOTATION-COMMUNICATION-255`), but the
  automatic-enforcement field was omitted. Ask one yes/no wrong-return counterexample.
- The wrong-return counterexample passed at confidence 90 (`EV-P5-RETURN-ANNOTATION-FRESH-256`):
  ordinary Python returns `"oops"` despite `-> list[int]`. Return-annotation syntax is recovered;
  rebuild RetryPolicy one method contract at a time before the full transfer trace.
- The RetryPolicy method-contract rebuild passed at confidence 90 (`EV-P5-RETRY-METHODS-257`):
  initialization, integer intent, runtime validation, and copied return were correct. Use `_limits`
  for the internal attribute and `limits()` for the public method. Resume the original composed trace.
- The resumed RetryPolicy transfer passed at confidence 100
  (`EV-P5-RETRY-TRANSFER-COMPLETE-258`): exact valid/rejected behavior, unchanged internal state,
  snapshot mutation isolation, absent annotation enforcement, and the shared Session principles were
  all correct. The learner identified the obstacle as syntax rather than the underlying model.

Do not mark these concepts permanently mastered after one review sequence.

## Cumulative-review counters

The Phase 0–2 foundation counter was reset on 2026-08-29 after four formal cumulative questions
passed with remediation where needed.

The Phase 3-5 foundation counter reached 3/3, the review ran on 2026-08-31, all five questions
passed, and the counter is now RESET as of 2026-08-31. It stands at 0/3; Phase 6 will count as 1/3.

The major/deep Phase 7–15 counter has not started.

## Open interaction and exact next step

Phase 5 is complete and the cumulative foundation review is complete with the counter reset. There
is no blocking gate outstanding.

Phase 6 has BEGUN. The specification was written by the learner (`EV-P6-CLI-SPEC-267`) and the
first patch is implemented and verified (`EV-P6-CLI-IMPLEMENTATION-270`), with the milestone trace
passed (`EV-P6-CLI-TRACE-271`).

Agreed CLI contract, assembled from the learner's own answers:

```text
input            the text inside the named file, read with open
success output   three labelled counts, one per line
success status   0
missing file     a readable error on stderr
failure status   1
counting         summarize.py, unchanged
```

`cli.py` now exists with `read_diff`, `format_summary`, `main(argv) -> int`, and an `if __name__`
entry point handing `main`'s return value to `sys.exit`. `test_cli.py` has seven tests.
`classify.py`, `summarize.py`, and `session.py` were not modified.

Syntax closed this phase: `with open(...) as handle` / `.read()` and `FileNotFoundError`
(`EV-P6-FILEREAD-SYNTAX-268`); `sys.argv` indexing and `IndexError` (`EV-P6-ARGV-SYNTAX-269`).
Both were genuinely new — the learner had never read a file in Python nor built a CLI before.

STILL OWED BEFORE PHASE 6 CAN CLOSE:

```text
transfer variant      same end-to-end and cost analysis on a different small CLI
argparse patch        deliberately deferred as a SECOND patch; not yet started
delayed retrieval     __name__ on a fresh surface, see below
```

NEXT SESSION STARTS HERE: the learner asked to repeat the `cli.py` teach-aloud cold, as the first
activity of the next session, before the transfer variant or any code. Do not show `cli.py` first;
ask for the explanation from memory and supply the code only if the learner asks. Assistance must
fade — the third failure path and the return-versus-exit rationale needed remediation today and
should come unaided this time. Record it as a fresh Evidence Record.

The learner explanation is DONE (`EV-P6-CLI-EXPLANATION-274`). Purpose, boundary rationale, the
return-value design, all three failure paths, and the decisive boundary evidence — `summarize.py`
did not change when the CLI was added — were all given, with remediation only on the third failure
path and the return-versus-exit rationale.

Watch item: `__name__` needed its rule restated within minutes of passing at
`EV-P6-ENTRYPOINT-272`, self-reported by the learner as still shaky. The rule now held is: the file
typed after `python` is `"__main__"`; imported files carry their own module names; only one file per
run is ever `"__main__"`. Schedule one delayed retrieval on a fresh surface before Phase 6 closes.

Both remaining syntax pieces are now closed. `if __name__ == "__main__"` passed
(`EV-P6-ENTRYPOINT-272`): the learner can state that `__name__` is `"cli"` during tests, that the
guard is therefore false, and that deleting it would kill the suite at its own import line.
Import-executes-the-whole-file and loose-`sys.exit`-kills-the-process were both new and are now
held. `file=sys.stderr` passed (`EV-P6-STDERR-273`), and this satisfies the delayed retrieval owed
against `EV-P1-EXIT-108` on a new surface: the learner traced that a redirected run captures only
stdout, that the missing-file path writes nothing there, and that the exit status carries the
verdict independently.

Standing instructions carried out of the review:

```text
state code in full when asking for a verdict on it; never describe an edit only in prose
narrow the prompt rather than lowering the rung when reflective fields get dropped
do not re-target callee-return-versus-caller-mutation; the learner asked, and it passed at target
watch the source-file versus in-memory-data terminology collision when specifying persistence
```

The completed review covered:

```text
state identity and snapshots
cross-module dependency/value flow
contracts: annotation versus runtime validation
rejection-before-mutation
evidence-based architecture timing
```

All five answers were recorded with exercise type `CUMULATIVE_RETRIEVAL`. See the review summary
block at the end of `learning/LEARNING_LEDGER.md` for the cross-cutting findings.

Cumulative progress: question 1 passed (`EV-CUM-FND-260`) at confidence 90. Next: cross-module
caller/callee value flow.

Cumulative question 2 was partial at confidence 90 (`EV-CUM-FND-261`): dependency direction and
final count were correct, but the middle call/returned labels were omitted and the classifier was
incorrectly said to mutate the caller-local accumulator. Descend to one call plus one caller branch;
do not advance the cumulative review until direct mutation versus returned-data influence recovers.

The omitted original return sequence was repaired in `EV-CUM-FND-261A` as urgent/normal/urgent.
The direct-mutation blocker remains open; continue the reduced one-call trace.

The reduced trace wording was initially interpreted as a same-named-local misconception
(`EV-CUM-FND-261B`), but the learner clarified that they knew such direct access was impossible
(`EV-CUM-FND-261C`). Do not run the basic scope descent. Require one precise sentence describing the
actual return → caller branch → caller-local mutation chain, then restore/close question 2.

The reduced causal distinction was recovered at confidence 100 (`EV-CUM-FND-261D`): the callee
returns data, the caller reads it, and the callee does not directly mutate caller-local state. The
required fresh target-level R6 return remains open. The learner paused to relocate; resume there.

The fresh target-level R6 return passed at confidence 90 (`EV-CUM-FND-262`, grading/dashboard
surface): dependency direction, per-item arguments, per-item returned labels including the `80`
boundary, final accumulator, final result, and caller-owned mutation were all correct. Cumulative
question 2 is CLOSED. Do not re-target the callee-return-versus-caller-mutation distinction as a
primary objective; the learner has asked that it not be re-asked and it has now passed at target
level. Next: cumulative question 3 — annotation versus runtime validation plus
rejection-before-mutation, on a fresh non-Session, non-RetryPolicy surface.

Cumulative question 3 was strong partial then closed (`EV-CUM-FND-263`, `EV-CUM-FND-263A`,
TagBoard surface). Rejection-before-mutation, snapshot identity, and annotation-communicates-only
were correct unprompted; three fields were omitted, including the value `add` evaluates to. On the
narrowed completion prompt all three passed at confidence 90, with `None` produced as a FIRST
answer rather than self-corrected — an improvement over `EV-P1-RETURN-100`. The live fragility is
now field omission under wide multi-field prompts, not the return-versus-side-effect concept.
Cumulative question 4 (tests as executable contracts) required an extended remediation chain
(`EV-CUM-FND-264` through `EV-CUM-FND-265`) and then CLOSED on the fresh `Roster` surface. Recovered
in the process:

```text
a green suite does not establish contract satisfaction
an uncaught regression can be generated unaided (case-sensitive duplicate check)
except ValueError does not catch TypeError
an assertion that ignores the message does not protect the message
```

Two blockers were procedural, not conceptual, and recur across records: carrying a PREVIOUS
scenario's outcome into a new one, and inserting a hypothetical call into the code under discussion.
Both cleared whenever the full code was restated with no omissions. Prompt-design rule adopted: show
code in full when asking for a verdict on it; do not describe candidate edits in prose.

`try` / `except` / `pass` required syntax-only help at R0 (`EV-CUM-FND-265-SYNTAX`) and is now read
correctly on both the raising and non-raising paths. The blocker there was reading past a `raise`
line inside a `try`, not exception semantics.

Cumulative question 5 (architecture timing and dependency direction) is OPEN and paused
mid-remediation (`EV-CUM-FND-266`). Two fields passed: the import direction
(`summarize.py` imports `classify`; `session.py` imports nothing of ours, verified against the
files) and a concrete deferral downside (nothing recorded in a `Session` survives the process).
Three fields are blocked and have no prior evidence record — reuse cost, the evidence that would
justify persistence, and the reversal condition. Treat these as not-yet-taught, not forgotten.

Cumulative question 5 CLOSED (`EV-CUM-FND-266A`). All five fields satisfied, ending with an unaided
reversal condition stated as retrofit cost: had `Session` already had many callers, deferring
persistence would have been the wrong call. Two conceptual repairs held afterward - being imported
by a module is not a dependency on it, and a reversal condition is about the cost of changing later
rather than a restatement of the need. One terminology collision surfaced and was resolved: "file"
as source code versus a `Session`'s in-memory data; watch for it when persistence is specified.

THE CUMULATIVE FOUNDATION REVIEW IS COMPLETE. All five questions passed.

The learner-requested cold `cli.py` teach-aloud was attempted on 2026-09-01
(`EV-P6-CLI-EXPLANATION-275`). Purpose, module responsibility, the `0`/`1` return shape, and the
fact that `summarize.py` did not change were retrieved unaided. The gate remains open: the answer
conflated a missing input file with `ImportError`, collapsed the argument-count cases into one
duplicated path, omitted the command-selection path, and described return as selectively stopping
`cli.py` rather than ending one call and returning a value to its caller. Per adaptive remediation,
descend to one isolated file-open failure, complete a near-transfer, then rebuild the failure paths
and return-versus-exit rationale before repeating the full teach-aloud. Do not start the separate
`__name__` retrieval, Phase 6 transfer, or argparse patch yet.

First R1 remediation attempt: the learner correctly identified `open("missing.diff")` as filesystem
access rather than importing, but did not know the exception name at confidence 60. The single rule
`open(...)` on a missing path raises `FileNotFoundError` was supplied. Next: a fresh R1 file-open
near-transfer with no hint.

The fresh R1 near-transfer then passed at confidence 90: `FileNotFoundError` was named and the
learner correctly said the read does not execute. Refine the wording to say that `open(...)` fails
before the variable is bound. Next, climb to a caught-failure trace with stderr, a returned status,
and skipped downstream work.

The caught-failure trace was partial at confidence 90. Return value `1` and skipped downstream
analysis were correct, but stdout/stderr were reversed, the caught exception was treated as if it
were automatically printed, and `return` was again described as stopping a module. Descend to one
R2 return-scope trace before rebuilding stream routing and the CLI failure path.

The reduced R2 return trace passed at confidence 80. The learner correctly predicted `inside` then
`outside 1`, stated that return stops only `choose`, and used the later module-level print as
evidence that the caller continues. At the learner's request, explain that the call transfers
control into the callee and return transfers a value and control back to the waiting caller. Next:
one less-prompted near-transfer before returning to process exit and the CLI failure path.

The less-prompted return-scope near-transfer passed independently at confidence 90: exact output,
returned value, stopped callee, and continuing caller were all correct. The return-scope blocker is
recovered. Next: compare a returned status with process exit inside a callable, then restore the
CLI failure-path trace.

The return-versus-process-exit trace passed at confidence 100: Run A returns `1` and its caller
continues; Run B exits before the caller receives a normal value or reaches its final print. The
testability/outer-entry-point rationale was omitted. Ask only that missing field at the same rung,
then restore the CLI failure-path trace.

On the narrowed rationale prompt, the learner said the caller receives exit code `1`; confidence
and the testability rationale were omitted. Correct the recipient distinction: `sys.exit(1)` raises
`SystemExit`, the caller's assignment does not complete, and the uncaught status is reported to the
shell/operating environment. Descend to one R1 assignment-completion check, then re-ask the
testability rationale.

The R1 assignment-completion check passed at confidence 100: the learner correctly stated that
the assignment and following print do not complete and that the shell/operating environment
receives the uncaught exit status. Next: one near-transfer connecting a normal return to a test
assertion, then rebuild the CLI failure path and full teach-aloud.

The testability near-transfer passed at confidence 100. The learner connected returned data to the
test assertion and explained why `sys.exit` belongs outside callable `main`. Refine the sequence:
`SystemExit` is raised first, then an uncaught process termination is observed by the shell; import
alone does not invoke `main`. Return-versus-exit is recovered. Next: rebuild caught file failure,
stderr routing, and the three CLI failure paths before the fresh full teach-aloud.

The fresh caught-failure composition was incorrect at confidence 90. stdout/stderr were reversed,
the caught exception was treated as automatically printed, and downstream `deploy`/`return 0`
were predicted to run after `return 2`. The primary blocker is composing an exception-handler
return with later function statements. Remove streams and descend to one caught-exception/return
control-flow trace before rebuilding output routing.

The reduced trace was not answered; the learner clarified that `deploy` had been read as outside
the function. This exposes an indentation/block-membership syntax prerequisite. Activate syntax-
only help: explain that dedenting from `except` can still leave a line indented inside `def`, then
use an R0 membership micro-example before returning to the exception trace.

The R0 membership example passed at confidence 90. The learner distinguished leaving the nested
`if` block from leaving the enclosing function: `print("B")` remains inside the function, while
`print("C")` is outside. Per the learning rules, require one fresh same-rung variant on a try/except
surface before adding execution behavior.

The learner asked to skip the fresh same-rung try/except membership check and move on. The check
was paused without an answer, so it is neither passed nor failed. Under the mandatory learning and
implementation gates, later Phase 6 work cannot begin yet. On resumption, use a new R0 surface to
verify nested-block versus enclosing-function membership, then rebuild the exception-handler return,
stderr routing, three CLI failure paths, and full cold teach-aloud.

The learner explicitly asked that inside/outside function membership be assumed understood. Treat
it as a working assumption, not verified mastery, and do not repeat that syntax check now. Resume
at a fresh exception-handler return trace without streams. Revisit indentation only if it causes
another error.

The fresh exception-handler return trace passed at confidence 90. The learner correctly predicted
status `3`, skipped `send` and `return 0`, and continuing module-level `record(3)`. Exception-handler
return flow is recovered under the learner-requested indentation assumption. Next: add only stderr
routing, then rebuild the three CLI failure paths and full cold teach-aloud.

The caught-failure stream trace was partial at confidence 100. Status `3`, skipped `send`, and no
automatic exception printing were correct. stdout was incorrectly called `None`, while stderr was
given both the explicit message and the exception name. Correct result: caller prints `status 3`
to stdout; handler prints only `Input missing` to stderr. Isolate two explicit print destinations
without exceptions or calls, then rebuild the composition.

The stream-only two-print check failed at confidence 90: the answer carried `Input missing` and
`FileNotFoundError` from the previous surface even though neither appears in the new program.
Activate syntax-only help: `print` emits its explicit value arguments; `file=sys.stderr` selects
the destination and adds no content. Reduce to one literal print call before a fresh two-call check.

The R0 single-print stream check passed at confidence 90. Destination and literal content were
correct; refine `None` to “empty stdout,” because no `None` value is printed. Require one fresh
same-rung multi-value stderr print before adding a second output stream.

On the fresh one-call multi-value check, the learner correctly said stdout is empty but omitted the
stderr content and confidence. Narrow to the two missing fields without lowering the rung.

On the narrowed stderr field, the learner correctly stated the routing principle at confidence 100
but again omitted the exact emitted text. Ask one fill-in blank for the current call; add no new
concept.

The exact stderr fill-in passed: `Warning 5`. The single-call content/destination step is closed.
Next: a fresh two-call example with one stdout and one stderr print, then return to the caught-
failure composition.

The fresh two-stream check passed at confidence 90: `Ready` to stdout and `Problem 7` to stderr.
Stream routing is independently recovered in isolation. Next: recombine caught file failure,
stderr, returned status, skipped downstream work, and continuing caller on a fresh surface.

The combined fresh caught-failure trace passed at confidence 100. stdout/stderr, returned status,
skipped downstream work, absence of automatic exception printing, and caller continuation were
all correct. Combined failure mechanics are recovered. Next: retrieve the trigger, stream behavior,
and returned status for all three actual `cli.py` failure paths from memory.

The three-path CLI retrieval was partial. Invalid argument count and missing-file triggers were
recalled, but user-visible details were imprecise, `main` return was described as an exit code, and
the caught exception was named as visible output. The unsupported-command path was not recalled;
confidence was omitted. Descend to two equal-length invocations to separate the length guard from
command-token validation, then rebuild all three contracts.

The equal-length comparison exposed ambiguous prompt wording; the learner had considered the
unsupported-command path but thought it violated the instruction not to double-count missing-
argument variants. After clarification, `argv[1]`, return-before-open, and returned `1` passed at
confidence 90. “Passes the length guard” was reversed: with length 3, `len(argv) != 3` is false, so
the failure body is skipped. Isolate that Boolean once, then rebuild the three paths.

The isolated length-guard trace passed at confidence 90. `len(argv)` is 3, the failure body is
skipped, `return 1` does not run, and command validation follows. Refine the Boolean field to the
literal value `False`. Next: rebuild all three actual CLI failure contracts with unambiguous labels.

The rebuilt three-path CLI contract was a strong partial at confidence 60. Wrong-count and
unsupported-command paths passed fully. For missing-file, trigger, readable message, returned `1`,
and skipped summarization passed; only the stream field used the exception type instead of the
destination. Ask only which stream receives the readable missing-file message, then treat the
three-path rebuild as closed if correct.

The narrowed missing-file stream field passed: the readable message goes to stderr, while
`FileNotFoundError` is the caught exception type. All three CLI failure contracts are rebuilt.
Next: a fresh full `cli.py` teach-aloud from memory. If it passes, continue in the recorded order
to the separate `__name__` retrieval and Phase 6 transfer variant before argparse.

SESSION PAUSE — 2026-09-01: a fresh target-level full `cli.py` teach-aloud was presented, but the
learner asked to pause and move locations before answering. It is unattempted and must not be
graded. Resume with a newly presented full teach-aloud from memory. The remediation beneath
`EV-P6-CLI-EXPLANATION-275` has recovered return scope, return-versus-exit/testability, caught
`FileNotFoundError`, stdout/stderr routing, and all three CLI failure contracts. Indentation is a
learner-requested working assumption, not newly verified mastery.

After returning, the learner attempted the fresh full teach-aloud at confidence 90. Purpose,
counting responsibility, unsupported-command path, missing-file path, and unchanged-`summarize.py`
evidence passed. The attempt incorrectly said success returns the three summary values, described
return as stopping a block, and said the wrong-count path gives a copy of argv. All failures were
also described as not necessarily showing a message. Descend first to printed values versus
returned status, then rebuild return-versus-exit and the usage path before another target attempt.

The reduced printed-output versus return trace passed three of four fields at confidence 90: exact
printed counts, stored result `0`, and counts-not-returned were correct. The learner described only
the control-flow effect of `return 0`; add the semantic meaning that status `0` communicates success
to the caller. Ask only that meaning on a fresh surface.

On the fresh status-meaning check, returned-versus-printed separation and possible conversion to
process exit status were correct at confidence 90, but the meaning “0 = success” was omitted.
Supply the one convention `0` success / nonzero failure, then require a no-output classification.

The no-output classification passed `0` as success and `3` as failure at confidence 90, closing
the status convention. The learner did not know the immediate recipient: a normal return goes to
the Python caller and may be stored by its assignment; the shell is involved only if an outer
boundary later invokes `sys.exit`. Require one normal-call assignment check.

The normal-call recipient check passed at confidence 60: the module-level assignment calls
`finish()`, stores returned `0`, and does not involve the shell. Refine the wording from
“`status = finish` is the caller” to the assignment statement being the caller and `finish()` being
the call expression. Next: rebuild why callable CLI `main` returns for testability.

After requesting more code, the learner saw complete `cli.py` and `test_cli.py`. The unsupported-
action branch and returned `1` were correct at confidence 90, and internal `sys.exit` was correctly
recognized as hostile to normal assertion evaluation. The learner incorrectly predicted that the
test call later reaches the outer `sys.exit` line and that an assertion error occurs. Isolate one
normal return into a passing assertion, without entry-point code; keep the separate `__name__`
retrieval deferred until the teach-aloud closes.

In the isolated assertion trace, the learner correctly said the test passes but then predicted a
`sys.exit` call that is absent from the displayed program. The blocker is carrying prior-surface
code into the current snippet. Descend to a presence-only check for `sys.exit`, then rebuild exact
current-program execution before returning to the CLI rationale.

The learner clarified that the prior `sys.exit` statement referred to the full `cli.py` question,
not the reduced snippet. On the narrowed test context, the learner correctly stated at confidence
100 that `test_cli.py` is the executed main file, imported `cli` has `__name__ == "cli"`, and the
entry-point `sys.exit` line is therefore not called. The test-call/assertion and outer-exit
separation are recovered. Ask for one concise independent design rationale next.

The concise return-versus-exit rationale passed at confidence 90. The learner explained that tests
must receive and assert guard results without terminating, while a real shell execution still gets
the status through the guarded outer `sys.exit`. This rationale is recovered. Next: retrieve only
the wrong-argument-count message, stream, return, and prevented work; then repeat the full target.

The wrong-argument-count contract passed at confidence 90: usage to stderr, returned `1`, and
action validation/file access prevented. All isolated blockers from the resumed target attempt are
now rebuilt. Next: one fresh full `cli.py` teach-aloud with assistance removed. Only after it passes
may the session continue to the separate `__name__` retrieval and Phase 6 transfer variant.

Fresh target attempt 27 was a strong partial at confidence 100. Correct: success prints the counts;
all three failure messages go to stderr; returning keeps guard results testable. Omitted: purpose,
counting responsibility, success status/meaning, trigger-to-message/return pairings, and unchanged-
`summarize.py` boundary evidence. Do not re-ask correct fields or lower the rung; issue one compact
narrowed completion prompt for only these omissions.

The narrowed target completion passed purpose, responsibility separation, all three failure
triggers/statuses, and unchanged-`summarize.py` boundary evidence at confidence 90. The learner
again said success returns the three counts rather than printing them and returning success status
`0`. This is a repeated target-level relapse after isolated success. Use worked-example rescue:
one solved neighboring example, learner explains the steps, learner completes one missing step,
then a fresh unaided example before returning to the target.

On the first worked-example explanation attempt, the learner correctly repaired the BuildLens
contract—prints three counts, returns `0`—but did not explain the neighboring `backup()` steps.
Narrow to the exact print line, exact return line, caller-stored value, and confidence. Do not move
to the partial example until those are supplied.

The worked `backup()` example was then explained correctly at confidence 90 after the code was
re-shown: exact print line, return line, stored `0`, and printed-not-returned distinction all passed.
The learner attributes the target error to lazy/imprecise wording rather than the mental model.
Because that wording changes the contract and recurred, continue the required rescue sequence with
one missing-step example and one fresh unaided example before returning to the target.

The missing-step rescue example passed all fields at confidence 100: return `0`, stdout warning
count, stored `0`, and count printed rather than returned. One fresh unaided non-BuildLens example
remains before returning to the target teach-aloud.

The fresh unaided `ship()` transfer passed at confidence 100: domain count printed, status `0`
returned/stored, and success meaning all correct. The worked-example rescue sequence is complete.
Return to one fresh target-level BuildLens success-contract prompt; do not re-ask already-passed
failure paths, testability rationale, purpose, or boundary evidence.

The fresh BuildLens target success contract passed four fields at confidence 90: three counts
printed, `main` returns `0`, `0` means success, and counts are printed rather than returned. The
outer-shell field was generic (“success or failure status”); narrow only to the exact successful
status `0`. If supplied, close the resumed full teach-aloud using the already-passed fields.

The exact shell-status completion passed: `0` success, `1` failure. The learner-requested resumed
`cli.py` teach-aloud is CLOSED through the adaptive remediation chain under
`EV-P6-CLI-EXPLANATION-275`. This was not a cold single-attempt pass; it required return/status,
stream, failure-path, and worked-example remediation. Next in the recorded order: delayed
`__name__` retrieval on a fresh non-BuildLens surface, then Phase 6 transfer, then argparse.

SESSION STOP — 2026-09-01: the delayed fresh-surface `__name__` retrieval failed at confidence 100
(`EV-P6-ENTRYPOINT-276`). For `python forecast.py`, the learner reversed the roles, assigning
`forecast` to the executed file and `"__main__"` to imported `formatter`, predicted formatter's
guard would run, and reversed the import direction. The correct model was supplied after the
attempt. The learner had explicitly designated this as the last question before moving locations,
so do not issue the mandatory simpler follow-up now. Next session must start at R0/R1: identify the
filename typed after `python`, assign `"__main__"` only to that file, then add one imported module
and guard consequence. Do not start the Phase 6 transfer or argparse patch.

The learner chose to complete a follow-up before leaving. The reduced `python dashboard.py` surface
passed at confidence 100: dashboard received `"__main__"` and imported colors received `"colors"`.
Require one fresh same-rung executed/imported distinction before adding the guard consequence.

The fresh `python worker.py` / imported `log_tools.py` same-rung transfer also passed at confidence
100. Refine the imported name to exact string `"log_tools"`. The executed/imported distinction is
recovered on two reduced surfaces. Add one imported-module guard consequence next.

The imported-module guard consequence then passed at confidence 100. The learner correctly stated
that worker alone has `"__main__"`, imported log_tools has `"log_tools"`, and log_tools' guarded
print does not run. `EV-P6-ENTRYPOINT-276` is CLOSED after remediation, not as a first-attempt pass.

SESSION STOP — 2026-09-01: the learner is moving locations and requested commit/push after this
follow-up. Next session starts with the Phase 6 transfer variant: end-to-end path and rough cost
analysis on a different small CLI. Do not begin argparse until that transfer passes.

```text
phase                       Phase 6 in progress; first CLI patch complete
last knowledge gate         EV-P6-ENTRYPOINT-276, delayed retrieval closed after remediation
next retrieval due          Phase 6 transfer variant on a different small CLI
next architecture reset     complete; next by time or major transition
next implementation step    Phase 6 transfer variant; then argparse patch
last published commit       docs: record Phase 6 teaching and retrieval state
```

Files the learner should currently be able to teach:

- `cli.py`
- `test_cli.py`
- `classify.py`
- `summarize.py`
- `session.py`
- `test_classify.py`
- `test_summarize.py`
- `test_session.py`

Historical evidence lives in:

- `learning/LEARNING_LEDGER.md` — exact prompts, committed answers, evaluation, and remediation;
- `QUIZZES.md` — readable transcript;
- Git history — prior full versions of this snapshot and all published state.
