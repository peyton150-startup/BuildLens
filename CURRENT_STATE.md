# BuildLens — Current State

> **Maintenance rule:** this file is a replace-in-place snapshot, not a session log. Update or remove
> obsolete statements whenever state changes. Preserve historical prompts, answers, remediation, and
> rationale in `learning/LEARNING_LEDGER.md`, `QUIZZES.md`, and Git history.

Last updated: 2026-09-05

## Lifecycle

**Current phase:** Phase 6 complete. Do not begin Phase 7 automatically; start its specification and
adjacent-learning sequence in the next implementation session.

Phase 7 specification has begun (`EV-P7-GIT-SPEC-281`); no Phase 7 code exists. The learner
tentatively prefers `buildlens analyze` inspecting the repository containing the current working
directory but has not approved the choice. Clarify whether Phase 7 optimizes for invocation inside
the target repository or central inspection from elsewhere.

The learner committed to the inside-repository workflow. Phase 7 CLI behavior is
`buildlens analyze` with no repository argument; the CLI resolves current-directory context and the
future adapter receives the repository path explicitly. Next decide which Git comparison is
authoritative: unstaged, staged, or both.

The learner tentatively chose combined `git diff HEAD` to see the current tracked worktree state but
identified the choice as gut instinct. Explain that the combined diff preserves the net content
difference while collapsing staged-versus-unstaged provenance. Ask whether that distinction is
required in Phase 7 before treating the choice as approved.

The learner refined the need: inspect active edits and separately double-check staged changes before
push, suggesting both unstaged and staged views rather than one combined diff. Correct that these
states do not encode edit recency and that Phase 7 is snapshot inspection, not continuous real-time
streaming. Discuss two labeled snapshots first; defer filters/UI/live monitoring.

The learner approved two separately labeled unstaged and staged summaries, with no filter syntax in
Phase 7 and no summing of the two views. They asked whether later continuous observation watches
files rather than summaries. Clarify: events/watchers signal possible change; Git inspection remains
authoritative; diffs and summaries are recomputed derived views. Live observation remains deferred.
Next decide untracked-file scope.

The learner did not yet know whether Phase 7 must include untracked files. Descend to a concrete
scenario with one edited tracked file and one newly created source file. Ask whether omitting the
new file would violate the intended snapshot; defer implementation tradeoffs until that requirement
is clear.

The concrete scenario established that omitting a newly created dependency would make the snapshot
incomplete. Phase 7 must discover untracked files. Next clarify whether it only lists their paths or
also treats their text contents as additions in the summary pipeline.

The learner chose full new-file content for untracked text files, correctly noting that filename-only
or omission would hide half of a cross-file change. Treat these files as entirely added content in
the unstaged view. Refine “timeline” to point-in-time snapshot; chronology is not inferred. Next
decide whether any failed snapshot component invalidates the whole result or permits partial output.

The learner clarified the Phase 7 operating workflow: Claude Code and BuildLens are side by side;
after Claude changes files and settles for a few seconds, the learner manually runs
`buildlens analyze` for a fresh snapshot. This is not automatic monitoring. Given the completeness
requirement and cheap retry, recommend rejecting an incomplete snapshot with a readable error and
letting the learner rerun. Await explicit approval.

The learner approved whole-snapshot failure with one added contract: the readable stderr diagnostic
must tell the learner to try `buildlens analyze` again. Failure returns 1 and emits no partial
summary. Next decide successful no-change output.

The learner approved clean-repository behavior: status 0 with explicit UNSTAGED and STAGED sections,
each showing zero counts. Requirements are now sufficient to compare non-mutating Git capture
approaches; implementation remains unauthorized.

The learner approved Git-native, read-only capture. Planned commands separately obtain tracked
unstaged and staged diffs, discover untracked paths, and ask Git to create no-index new-file diffs.
The adapter must understand that no-index status 1 means “different,” not failure. Index-mutating
approaches are rejected. Present module/data-flow design next.

During the module/data-flow design, the learner asked what `cwd()` means. Activate syntax-only help:
`Path.cwd()` returns the process's current working directory as a Path object and does not change
directories. Require one micro-prediction before resuming design approval.

The `Path.cwd()` micro-check passed at confidence 90: it represents the current directory and does
not change it. Resume approval of the module/data-flow design.

The learner approved the module/data-flow boundary at confidence 90 and defended it through
responsibility separation. CLI orchestrates, the Git adapter owns Git/process details, and the
existing core consumes only diff text. Present subprocess/error handling design next.

During subprocess/error design, the learner asked for every line of `subprocess.run(...)` to be
explained. Activate syntax-only help and pause design approval. Explain the call/keywords and require
one small non-Git call-reading prediction before resuming.

The subprocess call-reading micro-check passed at confidence 90: executable, arguments, child cwd,
string stdout, and timeout were all correct. Resume approval of the subprocess/error contract.

The learner correctly objected that subprocess syntax was taught but the process/error semantics
were presented for approval before teaching. Treat the apparent approval as provisional. Restore
the required adjacent-learning sequence using `CMU-15213-SYSTEMS` and `PY-SUBPROCESS`: begin with a
parent-Python/child-Git prediction, then channels, status, timeout, and application/transfer before
final design approval.

The first parent/child prediction was `i have no idea` at confidence 5. Descend to one concept:
BuildLens Python is the parent process; the operating system starts Git as a separate child;
`subprocess.run` waits for it to finish. Defer every other subprocess concept and require one
generic-tool labeling check.

The parent/child model passed on the BuildLens surface at confidence 90: Git is a separate child and
the BuildLens Python parent waits for it to finish. Require one unrelated same-rung transfer before
adding stdout/stderr.

The non-Git compressor transfer passed at confidence 90: Python parent, compressor child, parent
wait, and resume-after-child-exit were all correct. Parent/child remediation is closed. Add captured
stdout/stderr through a prediction next.

The captured-channel prediction passed at confidence 90: normal and error strings are available as
`result.stdout` and `result.stderr`. Add child return code behavior next; defer timeout and Git
status interpretation.

The first default return-code prediction was `i have no idea`. Explain only that without
`check=True`, a started/completed child returning nonzero still yields a CompletedProcess and stores
the integer in `result.returncode`. Require one fresh numeric example; defer all other failures.

The learner correctly explained normal return and parent interpretation at confidence 90 but copied
status 3 into a case where the child exited 4. Ask only for the exact stored integer before adding
Git-specific status meaning.

The exact status correction passed: a child exiting 4 produces `result.returncode == 4`. Default
nonzero transport is recovered. Apply it to `git diff --no-index`, where status 1 has a documented
command-specific meaning.

On the no-index scenario, the learner asked whether it meant `helper.py` was empty. Clarify that the
first path is a separate empty baseline and the second is the new file. A nonempty helper differs
and yields added content with status 1. This also exposes an empty-untracked-file edge case that must
be handled explicitly later. First require one nonempty comparison trace.

The learner asked whether the empty file is what Git compares against `helper.py`. Confirm yes and
acknowledge that the placeholder notation was undefined. Re-present explicit contents before asking
for status interpretation.

The learner still did not understand the explicit no-index comparison. Descend below Git/files/status
to one empty-before versus one-line-after text comparison. Ask only whether the line is added or
removed.

The learner requested a picture-based explanation. A two-panel visual showed an empty BEFORE
baseline and `helper.py` containing `print("ready")` AFTER. The learner correctly identified the
line as added, passed a fresh transfer, and then correctly interpreted `git diff --no-index` status
1 as valid difference data rather than adapter failure. Their reasoning also correctly predicted
status 0 when both compared files are empty. Introduce timeout behavior next. No Phase 7 product
code exists.

The learner correctly predicted that `subprocess.run(..., timeout=10)` raises
`subprocess.TimeoutExpired` when the Git child does not finish in time, rather than returning a
normal `CompletedProcess`, then transferred that behavior to a compressor child with a five-second
timeout.

The learner revised and approved the Phase 7 subprocess/error contract. Launch failure is explicit,
and process-level success is distinct from data validity: malformed or unusable required Git output
invalidates the whole snapshot even when the child process completed acceptably. The complete
contract is now recorded in `IMPLEMENTATION_PLAN.md`. The required test matrix covers expected
status 0, no-index status 1 as valid difference data, genuine Git error status, launch failure,
timeout, and valid-process/malformed-output rejection. Higher-level Agentic-AI concepts and later
reliability machinery remain deferred.

Next require one non-Git transfer that distinguishes a successfully completed process from unusable
application data, then return to the remaining Phase 7 specification edge cases. No Phase 7 product
code exists.

On the first non-Git transfer, the learner correctly rejected nonnumeric weather data and said the
parent should surface an error, but incorrectly concluded that the process contract also failed and
that success would have used status 1. Primary blocker: keeping a documented process status separate
from later validation of returned data. Descend to an R1 process-only check before a fresh
process-success/data-failure near-transfer. No Phase 7 product code exists.

The R1 process-only check passed: for a generic tool whose contract defines status 0 as successful
completion, returned status 0 satisfies the process contract. The learner correctly recalled that
`git diff --no-index` differs: statuses 0 and 1 are both valid command outcomes, with 1 meaning
differences found. Require a fresh near-transfer separating valid process completion from invalid
application data.

The fresh inventory-tool near-transfer passed at confidence 90: status 0 satisfied that child's
process contract while malformed required JSON failed the data contract. The learner independently
separated the two layers, so this remediation chain is closed. Return to the empty-untracked-file
Phase 7 specification edge case.

When asked whether an empty untracked `placeholder.py` should be omitted or shown, the learner first
asked what “omit” means. Syntax-only vocabulary help defined it as “leave out / not include.” The
learner then chose to show the file in UNSTAGED with zero added and removed lines. The choice is
correct, but require their completeness reasoning before approving the requirement.

The session paused for dinner before that reasoning was supplied. Resume by asking only why an empty
untracked file should remain visible when both line counts are zero. Do not implement Phase 7 yet.

When resumed, the learner answered `i do not know`. Primary blocker: distinguishing file presence
from file contents. Descend below Git and line-count policy to an R1 before/after check asking only
whether creating an empty file changed the folder state.

The R1 check passed: the learner correctly identified that creating an empty `placeholder.py`
changes the folder state even though the file contains no lines. Require one near-transfer linking
that changed existence to the completeness of a repository snapshot.

The near-transfer passed. The learner explained that the empty file must be shown because its
creation is a state change and that change belongs in the snapshot. Approve the requirement:
UNSTAGED reports the empty untracked file as one changed file with zero added and zero removed
lines. Next compare implementation mechanisms without writing Phase 7 code yet.

When asked which evidence should determine file presence, the learner chose the content-line counter
and was unsure. This is incorrect because both “no file created” and “empty file created” produce
zero added/removed content lines. Primary blocker: recognizing when one representation cannot
distinguish two relevant states. Descend to an R1 two-case distinguishability check.

The R1 distinguishability check passed: the learner correctly said identical zero line counts cannot
tell “no file created” from “empty file created” apart. Now ask which available evidence does
distinguish those states.

The learner correctly questioned that path discovery cannot itself tell whether a file is empty.
Clarify the split: path discovery proves that the untracked file exists and therefore establishes
the file-level change; content inspection establishes its line counts. The learner then explained
the two-source sequence correctly. Preserve the precision that content counts measure content and
do not decide whether the new path exists. This remediation chain is closed.

The learner then suggested the counts are needed to see whether there is a change. Correct the
precision: a file header/path establishes a file-level change; content counts only measure changed
lines. A local read-only Git probe compared `/dev/null` (nonexistence before) with an existing empty
file and returned status 1 plus `diff --git`, `new file mode`, and `index` metadata, with no content
hunk. This is sufficient for the existing summarizer to report one changed file and zero added or
removed lines. The earlier “empty baseline” teaching simplification is not the final mechanism:
an existing empty file compared with another empty file would erase the creation distinction.

During the exact trace, the learner asked whether `index 0000000..e69de29` counted lines. Syntax-only
help explained that these are abbreviated Git object identifiers: left is the absent-before side and
right identifies empty content. The learner then correctly traced BEFORE/AFTER, `new file mode`, one
file changed, and zero added/removed lines. Ask for explicit approval of the `/dev/null` mechanism.

When comparing representations, clarify that validation and representation are separate decisions:
both a plain string and a structured result must reject malformed required output. The learner judged
the structured per-command result to be overkill because the current downstream core needs only
validated diff text. Approve validated plain diff text at this boundary; keep path, return code, and
stderr inside the adapter's validation work. This does not collapse the separately labeled UNSTAGED
and STAGED captures. Require a reversal condition before closing the design decision.

The learner explicitly approved the validated plain-diff mechanism. The only remaining design-defense
item for this representation is a concrete future consumer requirement that would justify reversing
the decision and introducing a structured result.

The learner proposed “the return code” as a tentative reversal condition. Accept with precision:
the structured result becomes justified if a downstream consumer gains a concrete requirement to
receive the exact return code (for example, display or audit), rather than the adapter merely using
it internally for validation. Require one unrelated representation transfer before closing the
decision.

The image-converter transfer passed: the learner correctly justified a structured result when the
UI needs image bytes plus width and height. They remain unsure what data type crosses to the caller.
Activate syntax-level help for one small record/dataclass example and field access; do not add such
a type to Phase 7.

The learner asked whether `b"image bytes"` was a typo. Syntax-only help distinguished a bytes literal
from a text string and mapped the positional `ImageResult` arguments. The learner correctly read
`800` as the width. The representation decision, reversal condition, unrelated transfer, and syntax
check are complete. Present the first Phase 7 implementation patch scope for approval; do not code
before approval.

The learner asked whether staged capture would still be built later, then explicitly approved the
first patch after confirming that the split changes sequencing rather than final scope. Patch 1 is
limited to one tracked-UNSTAGED capture function and focused tests. STAGED capture, untracked
discovery, `/dev/null` new-file diffs, multi-command composition, and CLI integration remain required
later patches. Complete the test-strategy design section before writing the architectural design
record or product code.

The learner approved controlled subprocess tests for the first patch, with a real-Git integration
test deferred until the capture paths are assembled. The full approved design is recorded in
`docs/superpowers/specs/2026-09-02-phase-7-git-boundary-design.md`. Self-review found no placeholders,
scope contradictions, or unresolved first-slice behavior. The learner must review and approve that
written design before implementation planning. No Phase 7 product code exists.

The learner reviewed the written design and said everything looks good. The design is approved.
Before the implementation plan reveals concrete controlled-subprocess test syntax, run one smallest
prerequisite check: whether substituting a test stand-in for `subprocess.run` launches real Git.

The learner correctly answered that the controlled stand-in does not launch a real Git child. Their
reasoning correctly favors learning the parent-side boundary mechanism first. Preserve the precision
that this proves BuildLens's construction/interpretation behavior, not operating-system process
launch or real Git behavior. Require one proves/does-not-prove check before showing mock syntax.

The learner's proves/does-not-prove answer passed with precision. A controlled test can prove that
BuildLens attempted the expected call and interpreted the prepared result; it cannot prove operating-
system launch or real Git output. Show only the smallest `unittest.mock.patch` form and require a
one-value trace before writing the implementation plan.

The session paused because the learner needed to move locations. Resume by showing the minimal
`mock.patch` example described above and ask only what value `subprocess.run` returns inside the
indented block. No Phase 7 product code or implementation plan exists yet.

On resume, the learner correctly explained that the patched call reaches the Git-adapter stand-in
rather than launching real Git, at confidence 90, but did not name the exact returned value. Ask only
for the value assigned to `received`. The learner also requested moving to a new session after Phase
7 implementation is complete; preserve that transition point rather than ending this session early.

The exact return-value remediation passed: `received` gets the string `"controlled result"`. The
learner then asked whether `received` is a record type when real Git runs. Clarify an ambiguity in the
toy example: real `subprocess.run` returns a `CompletedProcess` record-like object inside the adapter;
the approved adapter boundary extracts and returns only its `.stdout` string. Require a two-variable
type mapping before showing the real controlled-test form.

The two-variable mapping passed: `process_result` holds the `CompletedProcess`, while `diff_text`
holds the stdout string. Show the realistic controlled test with a prepared `CompletedProcess` and
ask separately what the subprocess stand-in returns and what `capture_unstaged_diff` returns.

On the realistic controlled test, the learner said the patched subprocess returns diff text and the
adapter gets unstaged-file diff, at confidence 90. The adapter-output intent is correct, but the
first step regressed: patched `subprocess.run` returns the prepared `CompletedProcess`; the adapter
then extracts `.stdout`. Ask only for the patched subprocess return before rebuilding the two-step
trace.

The isolated return check passed: the patched function returns the prepared `CompletedProcess`
object. Rebuild the full two-step trace once without hints before writing the implementation plan.

The rebuilt trace passed: the learner identified `process_result` as the `CompletedProcess` containing
the prepared Git fields and the adapter return as the exact stdout string `"DIFF TEXT"`. When the
learner asked what type `CompletedProcess` is, clarify that it is a class in `subprocess`; the returned
value is an instance whose attributes reference other Python objects. The learner correctly identified
`returncode` as an integer attribute at confidence 90 and then correctly stated that `diff_text`
references only the `.stdout` string, not the entire `CompletedProcess`.

While reviewing execution options, the learner asked whether objects inside functions/modules are
only referable there. Clarify that scope controls names, not object lifetime: a local name disappears
after return, while a returned object may remain reachable through the caller's new name. The learner
correctly traced the returned list reference, with the precision that the object is not renamed; one
binding ends and another exists. Require one module-name access transfer before execution selection.

The learner restated the object-binding precision correctly, then supplied the correct module-dot-
function access pattern but omitted underscores from both identifiers. Show the exact expression
`git_adapter.capture_unstaged_diff()` and require one exact reproduction before execution selection.

The learner placed every underscore correctly but escaped them as `\_`. Clarify that backslash
escaping belongs to Markdown prose and is invalid in this Python expression. Require the literal
expression in a fenced code block without backslashes.

The learner's second response again displayed `\_` and was not fenced. Do not continue a formatting-
sensitive copying loop. Descend to the underlying R0 rule: ask whether Python source includes a
backslash before an underscore. If the learner answers no, accept the identifier syntax and return
to execution selection.

The learner requested skipping this as a nitpick. Honor that request: underscore placement and the
module-qualified access model were already correct, and no useful Phase 7 understanding depends on
continuing a Markdown-formatting drill. Return to implementation-plan execution selection.

The learner chose inline execution because they want to learn how the patch is implemented. The
checkout is the normal `main` workspace, so the learner requested committing/pushing the planning
records and then implementing in an isolated worktree. Create branch
`codex/phase-7-unstaged-capture`, verify all four existing suites in the isolated baseline, and only
then resume the plan's pre-patch prediction. No Phase 7 product code exists.

The first-slice implementation plan is recorded in
`docs/superpowers/plans/2026-09-03-phase-7-git-boundary.md`. Self-review narrowed the plan to the one
approved tracked-UNSTAGED patch; staged, untracked, CLI, and integration work remain separately
planned later slices. No Phase 7 product code exists.

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

Phase 6 is complete in every required dimension:

```text
implementation       complete — argparse CLI vertical slice
automated tests      complete — all four suites passed 2026-09-02
learner trace        complete — valid Namespace path and malformed SystemExit path
learner explanation  complete — EV-P6-CLI-EXPLANATION-275
transfer variant     complete — EV-P6-CLI-TRANSFER-277
policy decision      complete — EV-P6-ARGPARSE-POLICY-280
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

### `cli.py`

`main(argv)` owns the command-line/process boundary. It gives `argv[0]` to argparse as the displayed
program name, parses `argv[1:]` into `Namespace(action=..., path=...)`, restricts action to
`"analyze"`, reads `args.path`, delegates counting to `summarize_diff`, and prints the formatted
summary. Malformed syntax uses argparse's generated stderr diagnostic and raises `SystemExit(2)`.
A missing file prints a readable stderr message and returns 1; success returns 0.

## Automated verification

```text
python test_classify.py   — 8 test functions
python test_summarize.py  — 1 end-to-end summary test function
python test_session.py    — 7 test functions
python test_cli.py        — 7 test functions
```

All four passed together after the Phase 6 argparse patch on 2026-09-02.

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

```text
shell argv
→ main separates argv[0] from argv[1:]
→ argparse validates action/path and returns Namespace
→ read_diff(args.path)
→ summarize_diff(diff_text)
→ format_summary(summary)
→ stdout + status 0

malformed syntax → argparse stderr + SystemExit(2)
missing file     → BuildLens stderr + return 1
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
passed, and the counter reset. Phase 6 is now complete, so the foundation counter stands at 1/3.

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

The Phase 6 transfer began on an unrelated alert-log CLI (`EV-P6-CLI-TRANSFER-277`). The learner's
end-to-end trace passed at confidence 90: guards, file read, split line strings, branch decisions,
two increments, and returned success status were correct. Refine exact stdout from `Alters: 2` to
`Alerts: 2`; stderr is empty. Boundary rationale, explicit remaining representations, and rough
growth were omitted. Ask only those fields; do not restart the trace.

The learner clarified `Alters` was fast typing; treat stdout as conceptually passed. On narrowed
completion, responsibility boundary and linear growth passed at confidence 90. Representation
fields remain open: types were not named, two answers carried Git-diff/files-changed language into
the alert-log surface, and formatted output was not represented as a string. Ask exact type plus
value/shape for argv, full log text, split lines, integer count, and output string only.

The exact representation completion passed at confidence 90 with spelling refinements. `argv` is
`list[str]`; full file text is one newline-containing `str`; `splitlines()` yields `list[str]`;
count is integer `2`. Correct the facilitator prompt: `print("Alerts:", alert_count)` receives a
string and integer as two arguments, which the learner recognized, rather than one formatted
string. The first Phase 6 transfer is closed. Run one shorter second transfer and ask what deep
principle both variants share before argparse.

The second `checks_cli.py` transfer trace passed at confidence 90: guard behavior, `argv[1:]`
excluding the script name, four result strings, two increments, stdout `Failures: 2`, empty stderr,
and returned success `0` were correct. Representations, 10x growth, responsibility boundary, and
the principle shared with `alert_cli.py` were omitted. Ask only those analytical fields.

The narrowed second-transfer analysis passed representation values, sliced result list, integer
count, boundary ownership, and shared principle at confidence 90. Two exact fields remain: name
argv as `list[str]`, and state roughly 10x work/linear growth for 10x arguments. Ask only those.

The final two transfer fields passed: argv is `list[str]`, and 10x arguments produce roughly 10x
counting work (`O(n)`). `EV-P6-CLI-TRANSFER-277` is CLOSED. The two transfer surfaces shared the
principle that main owns the external CLI/process boundary while a separate deterministic function
owns domain counting; representations and status remain explicit. The deferred argparse patch is
now eligible, but its success representation and bad-input behavior must be predicted first.

The first argparse success-path prediction was not attempted (`EV-P6-ARGPARSE-SYNTAX-278`): the
learner said they did not know what was happening. Activate syntax-only help. Reduce from action +
path to one positional name/token/attribute: parser creation, `add_argument("color")`,
`parse_args(["blue"])`, and `args.color`. Do not return to BuildLens or bad-input behavior until a
fresh one-argument parse is independently readable.

On the fresh one-argument prompt, the learner asked what “parse” means. Descend to R0 vocabulary:
parsing interprets raw input according to rules and produces a structured representation. In the
micro-example, raw `"fast"` plus registered name `mode` becomes `mode = "fast"`; nothing is run or
mutated. Require a one-sentence restatement before returning to `parse_args` syntax.

The parse-vocabulary micro-check was partial at confidence 60. The learner compared the registered
name to a key/label but omitted the raw token from the named result and generalized to arbitrary
Python objects. Keep default tokens as strings; narrow to one fill-in `speed = "slow"` before
returning to the one-argument parser.

The fill-in passed: parsed result `speed = "slow"`. Parse vocabulary and one name=value binding
are recovered. Return to the one-argument `add_argument("mode")` / `parse_args(["fast"])` syntax.

The learner spontaneously transferred `action = "analyze"` correctly. On the two-argument
completion, `path` was called `diff_text`. Correct the boundary: argparse binds the second raw token
to filename string `"changes.diff"`; file contents do not exist until later `read_diff`. Isolate
that binding once, then complete the script-filename and Namespace fields.

The learner clarified they meant actual BuildLens, then correctly mapped action to `"analyze"` but
reversed the remaining roles at confidence 90: called the filename `diff_text` and file contents
`args.path`. Exact flow is filename token → `args.path` → `read_diff(args.path)` → `diff_text`.
Require one matching check before continuing argparse.

The filename/content matching check passed at confidence 90: filename maps to `args.path`, loaded
content maps to `diff_text`. The boundary is recovered. Return to the original successful argparse
fields: `args.action`, `args.path`, omission of script filename from the explicit parse list, and
the parsed object-with-named-attributes representation.

The original successful parse passed action/path values and omitted script filename at confidence
90. The learner called `args` a “list object with named attributes.” Correct representation:
`parse_args` consumes `list[str]` and returns a new `argparse.Namespace` object; use `.action` and
`.path`, not list indexing. Isolate that input/output distinction before bad-input behavior.

On the next representation attempt, the learner supplied `(action = analyze, path = xhengesdiff)`.
The two named fields are understood, but the `Namespace(...)` container, string quotes, and
`.action`/`.path` retrieval syntax were omitted. Reduce to one field before returning to both.

The one-field reduction correctly mapped `mode` to `"slow"` at confidence 60, but attribute
retrieval was unknown. Isolate `object.attribute` syntax next; do not introduce parser failures yet.

The fresh `settings = Namespace(speed="fast")` check passed at confidence 90 with
`settings.speed`. Attribute access is recovered; climb to a fresh two-field representation next.

On the fresh two-field surface, `parsed.command` and `parsed.filename` both passed at confidence 90,
as did the intended field/value mapping. The exact parsed-object representation still omitted the
`Namespace(...)` wrapper and string quotes. Require only that line before parser failure behavior.

The learner then changed the retrieval to `parser.command`, revealing a variable-role confusion:
`parser` stores parsing rules, while `parsed` is the returned `Namespace` that stores parsed values.
Reduce to choosing which object contains one result value.

The next answer, `parser.filename`, repeated the same confusion, which the learner explicitly
recognized. Temporarily rename the objects to `rules` and `result`; check retrieval from `result`
before restoring `parser`/`args` naming.

With `rules` and `result`, the learner correctly retrieved `result.color` at confidence 90. Restore
the conventional `parser` and `args` names in a one-field near-transfer next.

The conventional-name near-transfer passed at confidence 100: `args.format` retrieves `"json"`.
Return to a fresh two-field target-level representation; parser failure behavior remains deferred.

The fresh two-field target passed the object roles and both retrievals at confidence 100. The learner
wrote `args = (task=scan, source = buildlog)`, so only exact notation remains: include
`Namespace(...)`, quote strings, and preserve the filename dot. Use one supplied syntax frame.

The next answer correctly added `Namespace(...)` at confidence 100 but still wrote the text values
without quotes and removed the filename dot. Isolate a single Python string literal before rebuilding
the full representation.

The learner clarified that quotes/spelling were fast-typing shorthand and that the values are known
to be strings. Stop grading transcription noise. The success representation passes: input is
`list[str]`, output is a `Namespace`, and values are read with `args.<field>`.

The first missing-positional argparse prediction was `no idea`. Default parser failure behavior is
new: use one minimal worked example before a near-transfer. Do not patch product code yet.

The first near-transfer recovered exit code 2 at confidence 20 but described the output as “prints
parser.” Clarify that the parser generates usage/error text; isolate stderr and the raised
`SystemExit` control effect next.

The narrowed retrieval passed: argparse generates usage/error text on stderr and raises
`SystemExit(2)` for the missing positional argument. `EV-P6-ARGPARSE-SYNTAX-278` is CLOSED after
adaptive remediation. Before the product patch, resolve whether BuildLens adopts argparse's status 2
or preserves the current status-1 user-error contract.

A requested four-topic pre-policy review began (`EV-P6-ARGPARSE-REVIEW-279`). The filename/content
distinction and the CLI/domain responsibility boundary passed at confidence 90. The original prompt
did not name the variable receiving `parse_args(...)`; the learner correctly objected that using
`parser` as that missing name did not establish parser/result confusion. On an explicit
`rules`/`result` surface, the learner correctly identified `result` as the object containing the
parsed value at confidence 100, but omitted the requested field-access expression passed to
`read_log`. The completion `resukt.source` passes as `result.source`, treating the typo as
transcription noise; the representation item is closed. Default argparse failure was recalled as
returning 1 instead of raising `SystemExit(2)`. On a reduced fresh surface, the learner then
correctly predicted generated usage/error text on stderr and raised `SystemExit(2)` at confidence
90. `EV-P6-ARGPARSE-REVIEW-279` is CLOSED. Do not treat this one short review as durable mastery.
The BuildLens status-policy choice remains the next gate before the product patch.

The learner began the status-policy reasoning (`EV-P6-ARGPARSE-POLICY-280`). Their core process-level
intuition is directionally correct: when the file runs as a script, both returning 1 through
`sys.exit(main(sys.argv))` and argparse raising `SystemExit(2)` terminate the process nonzero. Before
a final choice, distinguish the exact shell status, where control stops, and what a direct Python
call to `main(...)` observes. No argparse product patch is authorized yet.

The learner then tentatively chose standard `SystemExit(2)` but asked whether return 1 could still
print a bad-argv message and interpreted the existing assertion as obscuring failure. Separate
diagnostic output from failure signaling: both policies can print to stderr and both can be tested;
the assertion only encodes which outcome is expected. Require a confirmed choice, downside, and
reversal condition before patching.

After separating output from signaling, the learner leaned toward preserving return 1 because both
policies can print diagnostics and the remaining concern appeared to be `main`'s structure. Refine
that the shell normally sees the numeric status, not the meaning of stderr, so the decision also
controls whether malformed syntax (2) is distinguishable from file/other user errors (1). Continue
the tradeoff discussion before requiring a final defense.

The learner made the final policy choice at confidence 90: adopt argparse's standard
`SystemExit(2)` for malformed command syntax so the shell receives a distinct syntax-error status,
accepting that this breaks `main`'s former return-only user-error contract and requires
exception-aware tests. Reconsider only if a future uniform library-style `main(argv) -> int`
interface becomes more important than shell-visible error categorization. The policy gate is
passed; implement via a failing test first. File-read failure remains return status 1.

The learner requested collaborative test construction, so an unrun Codex-authored `test_cli.py`
edit was fully reversed. On the first missing-arguments test-design prompt, the learner named
`SystemExit(2)` and usage/error content but asked how to call SystemExit without bad argv and omitted
stderr at confidence 20. Clarify that the test intentionally supplies malformed real input rather
than calling the expected exception itself. On the reduced comparison, the learner correctly
identified command/action and path as the two missing tokens at confidence 100. Next reconnect this
malformed input to exception/status and stderr before writing test syntax.

SESSION STOP — 2026-09-02: the learner is moving locations and requested commit/push. The pending
prompt is `main(["cli.py"])` with no command/path; ask for the exact raised exception, status, and
usage/error stream. After that passes, construct the smallest `try`/`except` RED test together. No
`cli.py` or `test_cli.py` argparse implementation has been made.

On resumption, the learner correctly supplied status 2 and stderr at confidence 30 but named
`usage error` as the control effect. The diagnostic text and exception type are being merged.
On the reduced constructor form, the learner supplied `systemexit` at confidence 100; refine
capitalization to `SystemExit`. Together the attempts recover raised `SystemExit(2)` plus
usage/error text on stderr. Present the smallest exception-aware test skeleton and require only its
`error.code` assertion before editing `test_cli.py`. The first assertion attempt was
`SystemExit == 2` at confidence 90: status 2 is correct, but the exception class was compared instead
of the caught `error` instance's `.code`. Two further attempts were `error == 2` and
`main.error == 2` at confidence 90: the first compares the whole exception object, while the second
puts the field on the `main` function. Descend to retrieving `code` from a familiar one-field
`Namespace` object before restoring the exception surface. The learner correctly retrieved
`result.code` at confidence 90. Near-transfer the same object/attribute pattern to the caught
`error` object next, without adding comparison syntax yet. The learner then correctly supplied
`error.code` at confidence 90 and asked how `code` could be known when the except statement never
names it. This is a valid API-contract distinction: the syntax names `error`; the `SystemExit` type
defines `.code`. A live object check confirmed `SystemExit(2).code == 2`. Explain that library
attributes come from documentation/type information/inspection, then rebuild the assertion.

The learner completed `assert error.code == 2`. The first collaborative test is now authorized:
replace only the missing-arguments return-1 assertion with a `try`/`except SystemExit as error`
test and verify that it fails because current `main` returns rather than raises. Production code
must remain unchanged during RED.

RED was verified: `python test_cli.py` exited 1 because the new test reached its `else` and raised
`AssertionError: main did not raise SystemExit`. In tracing this, the learner correctly noted that
current `main` returns 1 and execution reaches `else`, but also said it raised and that `except`
ran. Clarify that normal return skips `except` and activates `else`; the test's own explicit raise
creates the observed AssertionError. Descend to a no-function try/except/else trace next.

The learner correctly restated the RED-to-GREEN intention but said the test changes `main`.
Refine that the test specifies/detects behavior; the later production patch changes `main`. The
reduced try/except/else trace then passed at confidence 90: normal assignment skips except and runs
else. Refine that absence of any exception, not the particular integer 7, controls the branch.
Return to a fresh trace of the real RED test before production editing.

On the real test, the learner correctly traced current `main` returning 1, control reaching else,
and the test raising AssertionError. Two explicit fields were omitted: the `except SystemExit`
handler is skipped, and production must raise `SystemExit(2)` for malformed arguments. Ask only
those fields before GREEN.

The learner correctly named the missing `SystemExit(2)` behavior at confidence 90 but described
except as running to check and else as running when the error is not SystemExit. Correct rule: else
runs only after zero exceptions; an unmatched exception propagates and skips else. Isolate this with
a tiny `ValueError`/`except SystemExit` example before GREEN.

On the unmatched-exception example, the learner correctly said ValueError continues outward because
the SystemExit handler does not match, but also said the else branch prints `finished`. Correct that
any exception leaving try skips else. On the binary follow-up, the learner correctly answered that
`finished` does not print at confidence 80 and distinguished it from the earlier normal-completion
example. The prerequisite is recovered. Transfer the chosen contract to unknown-action and
too-many-argument tests before production editing.

The first transfer reverted both cases to return 1 at confidence 70. The learner correctly named
`banana` as an invalid command but used `usage stderr` as the reason for the too-many-arguments case.
Under the chosen policy both raise `SystemExit(2)` and write diagnostics to stderr; the second is
malformed because it has an unexpected extra positional token. Reduce to one invalid choice, then
retry the excess-token case. The invalid-choice reduction passed at confidence 90 with raised
`SystemExit(2)`. Ask the excess-token near-transfer next.

The excess-token near-transfer passed at confidence 90: the second path is unexpected and produces
`SystemExit(2)`. The policy now transfers across all three malformed cases. Collaboratively specify
one test helper taking argv and asserting raised code 2, then update the tests before production.

The learner approved and correctly traced the proposed helper at confidence 90: each malformed argv
causes the except handler to verify code 2 and the helper then finishes normally. Update all three
malformed-input tests to use it and rerun RED with `cli.py` unchanged.

All three tests now use the agreed helper. RED was verified: `python test_cli.py` exited 1 at the
first malformed case because current `main` returned 1 and the helper raised its deliberate
`AssertionError`. `cli.py` remains unchanged. Before GREEN, trace the proposed parser's valid
`argv[1:]` input and returned action/path fields.

The valid parser trace passed action/path conceptually at confidence 90, but gave only the path for
`argv[1:]` and tied script-name exclusion to `main`. Descend to one unrelated `[1:]` slice. Then
rebuild that `argv[0]` is the program name used for diagnostics while argparse consumes user tokens
after it. Production remains unchanged.

The unrelated slice passed conceptually at confidence 90 as `["scan", "events.log"]`. The learner
asked its purpose. Explain that argv element 0 identifies the program, while elements from 1 onward
are user tokens; BuildLens keeps the former as argparse `prog` and parses the latter. Require one
fresh prog/tokens mapping before production editing.

The learner asked what `prog` means. Activate syntax-only help: `prog` is argparse's display name
for generated help/usage/error text; it neither runs the program nor becomes a parsed positional
value. Use one fixed `prog="audit-tool"` example before returning to argv mapping.

The learner spontaneously transferred the concept to BuildLens: `prog` is `"cli.py"` when
`prog=argv[0]` and argv begins with that string. This passes the syntax check. Return to one fresh
prog/tokens mapping before production editing.

The fresh mapping passed at confidence 90: `prog` receives `"audit.py"` and `parse_args` receives
`["check", "build.log"]`. The parser boundary is recovered. Apply the agreed minimal argparse
implementation and run the targeted CLI suite for GREEN evidence; do not mark the milestone complete
without the learner trace/explanation/transfer requirements.

The minimal argparse implementation is present in `cli.py`. Targeted GREEN was verified with
`python test_cli.py` exiting 0: valid analysis, file-read return 1, and all three malformed
`SystemExit(2)` cases passed. Stop before full verification/completion and require a learner trace
of one valid parse path and one malformed parser-exit path.

The post-GREEN malformed trace passed fully at confidence 90. The valid trace had the right token
list shape and continuation but renamed `action` to `command`, misspelled `path` as `poath`, and
passed standalone `path` rather than `args.path` to `read_diff`. Require only the exact Namespace
fields and file-read expression before full-suite verification.

The exact valid-path completion passed at confidence 90:
`Namespace(action="analyze", path="changes.diff")` and `read_diff(args.path)`. The learner explained
that `path` is an attribute on the Namespace referenced by `args`. The post-GREEN trace is closed.
Rename the two remaining vague malformed-input tests, rerun targeted tests, then run all four suites
for fresh verification evidence.

SESSION 2026-09-03 — FIRST PHASE 7 PRODUCT CODE EXISTS.

Isolated worktree `C:/Users/nicol/BuildLens_wt/phase-7-unstaged-capture` on branch
`codex/phase-7-unstaged-capture`. Baseline verified there before any new code: all four existing
suites passed.

The pre-patch prediction (`EV-P7-PREPATCH-CALL-282`) closed only after a long remediation chain.
The learner's first response treated `cwd`, `capture_output`, and `text` as fields on the returned
object. Recovery ran through call-inputs-versus-returned-object-fields on a non-subprocess surface,
default parameter values (`EV-P7-DEFAULT-PARAMETERS-283`), argument-list role reading with a
worked-example rescue (`EV-P7-ARGV-LIST-284`), and the `CompletedProcess` class name
(`EV-P7-COMPLETEDPROCESS-285`). A live probe in the worktree confirmed the returned fields are
`args`, `returncode`, `stderr`, `stdout` — proving inputs do not reappear on the result.

RED was observed as `ModuleNotFoundError: No module named 'git_adapter'` before implementation.
GREEN followed, and all five suites now pass (`EV-P7-ADAPTER-RED-GREEN-286`).

The post-GREEN trace closed (`EV-P7-ADAPTER-TRACE-288`) with `CompletedProcess` retrieved unaided on
first delayed retrieval. The boundary explanation closed (`EV-P7-ADAPTER-BOUNDARY-289`): the learner
established that zero lines of `summarize.py` change to accept Git output, and independently named
the newline-separated unified-diff content contract as the adapter's obligation.

FACILITATOR ERROR RECORDED (`EV-P7-PATH-BINDING-287`): a `str(42)` descent immediately preceded a
question about `Path(...)`, signalling the wrong result type. The learner correctly objected. Do not
descend through a constructor whose result type differs from the target. The learner is invited to
halt any descent when they already hold the concept.

CARRIED FORWARD: the reversal condition for the adapter needed explicit World A / World B
scaffolding and was not independently generated. Re-target it later without scaffolding.

Two recurring procedural patterns, both still live:

```text
carrying a previous scenario's names into the current program
answering what code CAN accept instead of what THIS call does
```

SESSION 2026-09-03 (continued) — TASK 1 OF THE FIRST SLICE IS COMPLETE.

The non-Git formatter-child transfer (`EV-P7-ADAPTER-TRANSFER-290`) passed six of seven fields
unaided on an unseen surface, and was clean on both procedural patterns flagged earlier: no
carry-over of prior-program names, and the branch field answered the specific run rather than
restating the rule. The learner then named the return code as the field the caller cannot read —
the exact field their own reversal condition depends on.

The shared principle and reversal condition closed in `EV-P7-ADAPTER-PRINCIPLE-291`. The principle
was restated without naming Git, `cli`, or `summarize`. The reversal condition was produced WITHOUT
the World A / World B scaffolding, closing the item carried forward from the previous session. It
needed one correction: the learner first proposed a second call to obtain the return code, then
self-corrected to one call returning a structured object whose fields the caller reads — the
`ImageResult` shape from the original design decision. Not a clean first-attempt pass.

Phase 7 Task 1 is complete in every required dimension:

```text
implementation       complete — git_adapter.py
automated tests      complete — five suites pass
learner trace        complete — EV-P7-ADAPTER-TRACE-288
learner explanation  complete — EV-P7-ADAPTER-BOUNDARY-289
transfer variant     complete — EV-P7-ADAPTER-TRANSFER-290, EV-P7-ADAPTER-PRINCIPLE-291
```

### `git_adapter.py`

`GitCaptureError(RuntimeError)` reports that one required snapshot component could not be captured.

`capture_unstaged_diff(repository: Path) -> str` runs Git as a child process with an argument list
and no shell, captures stdout and stderr as text with a 10-second timeout, rejects any nonzero
status with a `GitCaptureError` naming the component and preserving Git's stderr detail, and returns
`process_result.stdout`.

Only validated plain diff text crosses the boundary. Path, return code, and stderr stay inside the
adapter's validation work.

```text
Path → capture_unstaged_diff → git child in that directory
→ CompletedProcess → status check → stdout string → caller
```

`test_git_adapter.py` patches `git_adapter.subprocess.run` with a prepared `CompletedProcess`. It
asserts the exact argument list and keywords, and asserts the exact rejection message for status 2.
No real Git child is launched, so the tests prove call construction and result interpretation, not
operating-system launch or real Git behavior.

SESSION 2026-09-03 (continued) — STAGED CAPTURE SLICE COMPLETE.

The design decision was the learner's (`EV-P7-STAGED-DESIGN-292`). They chose the shared-helper
option, but their first reason — that it would run Git once — was wrong and was repaired: sharing a
body reduces how many times code is WRITTEN, never how many times it RUNS. Both options launch two
Git children. The corrected benefit is a single edit site, so the two views cannot drift apart and
report different contracts as one snapshot. The learner independently read the leading underscore as
an internal-helper convention and predicted that the coming untracked slice will force `_capture` to
stop raising on every nonzero status. The indirection cost was supplied, not generated.

### `git_adapter.py` (updated)

`_capture(repository, extra_args, label)` owns the Git call: it builds the argument list by joining
three lists, runs Git with no shell and a 10-second timeout, raises `GitCaptureError` on any nonzero
status with the component label and Git's stderr detail, and returns stdout.

```text
capture_unstaged_diff → _capture(repository, [],            "UNSTAGED tracked")
capture_staged_diff   → _capture(repository, ["--cached"],  "STAGED tracked")
```

```text
git diff --no-ext-diff --no-color --            5 arguments
git diff --no-ext-diff --no-color --cached --   6 arguments
```

`test_git_adapter.py` has four tests. The two pre-existing unstaged tests passed unchanged after the
body moved into `_capture` — that is the evidence the refactor preserved behavior.

Syntax closed this slice: list concatenation with `+`, `.strip()` as whitespace-ends-only, and
non-empty-string truthiness in `if detail:`.

WATCH ITEM — new recurring pattern:

```text
restating an expression with variables substituted, instead of evaluating it to a value
```

It appeared on both list and string concatenation. Every reduced form was evaluated correctly and
immediately, and the learner attributes it to speed rather than a gap. Treat an unevaluated
expression as unanswered.

The describing-a-role-instead-of-this-call pattern occurred three times and has now been named
explicitly to the learner.

SESSION 2026-09-03 (continued) — UNTRACKED PATH DISCOVERY COMPLETE.

The branch was merged into `main` with a merge commit rather than a rebase, because its three
commits were already published and rebasing would have required a force-push. The two lines had
touched no common file — docs on `main`, product code on the branch — so the three-way merge was
clean with no conflict.

Design decision `EV-P7-UNTRACKED-DESIGN-296`: `_capture` now takes the complete argument list and
prepends `"git"` itself, and `_diff_args` builds the shared tracked-diff flags for the two diff
callers. The learner drew the responsibility line well — `_capture` owns process mechanics, not which
Git command — and supplied the reversal condition unscaffolded: collapse `_diff_args` when only one
diff caller remains.

Recorded honestly: the drift failure was SUPPLIED as a worked scenario, not generated. The learner's
first choice rested on a misreading of the second option, and their initial acceptance was challenged
as capitulation before they restated it as their own decision.

### `git_adapter.py` (current)

```text
_capture(repository, args, label)   runs ["git"] + args, no shell, 10s timeout,
                                    raises GitCaptureError on any nonzero status,
                                    returns stdout as text
_diff_args(extra)                   ["diff", "--no-ext-diff", "--no-color"] + extra + ["--"]

capture_unstaged_diff    -> str        _diff_args([])
capture_staged_diff      -> str        _diff_args(["--cached"])
capture_untracked_paths  -> list[str]  ["ls-files", "--others", "--exclude-standard"], splitlines()
```

`test_git_adapter.py` has seven tests. The four pre-existing tests passed unchanged through the
`_capture` restructure — the second refactor-safety demonstration this phase.

Boundary principle established: Git emits only text, so the LIST is BuildLens's choice. The adapter
converts Git's output into the representation the domain needs, once, rather than making every
caller remember to split it.

Syntax closed this slice: iterating a string yields characters while iterating a list yields entries;
`"".splitlines()` is `[]`; a trailing newline produces no extra empty entry.

SESSION 2026-09-03 (continued) — ENCODING PATCH, AND A FACILITATOR BUG CAUGHT BY REAL GIT.

The learner asked unprompted how untracked paths relate to `summarize`, which produced the snapshot
cost analysis (`EV-P7-SNAPSHOT-COST-300`). Process count is `3 + n`. Measured: ~59 ms per Git child
versus ~1 ms for `summarize_diff` on a 1734-line input, a 58x ratio. The learner declined to change
the design, citing linear growth and a realistic n of 3-4 — the strongest architecture judgement
recorded so far.

`EV-P7-ENCODING-301`: `text=True` was decoding Git output with the locale encoding (`cp1252` here),
which either raised or silently produced wrong text. The learner chose strict UTF-8 over
`errors="replace"`, accepting that one latin-1 file fails every snapshot, because lossy decoding
trades a crash for uncountable wrong numbers. They also revised an initial choice to leak
`UnicodeDecodeError` to callers, settling on one normalized `GitCaptureError`.

`EV-P7-MOCK-LIMIT-302` — IMPORTANT. The first encoding patch was WRONG and all eight tests passed
anyway. `subprocess.run` decodes in a background reader thread; a `UnicodeDecodeError` there is
printed and discarded, and `run` returns normally with `stdout` as `None` and status 0. The
`except UnicodeDecodeError` never fired and the adapter returned `None` as text. The test passed
because its stand-in raised an exception real `subprocess.run` never raises — a green test asserting
fiction. A real repository with a latin-1 file exposed it.

This is the concrete realization of the limitation the learner articulated at
`EV-P7-PREPATCH-CALL-282`.

Resolution: capture raw bytes and decode in BuildLens's own code, so the failure is raised by a
documented method at a line we wrote. The learner rejected the alternative of checking for `None`
after being shown that documenting an assumption about someone else's library does not bind that
library.

STANDING RULE ADOPTED: any adapter behavior that depends on how a real external tool or the operating
system actually behaves must be verified against the real tool at least once. A passing controlled
test can encode a false belief.

OPEN RECOMMENDATION: add a real-Git integration test. The plan deferred it until the capture paths
were assembled; three now exist, and this bug is exactly what it would have caught.

### `git_adapter.py` (current)

```text
_capture(repository, args, label)
    runs ["git"] + args, no shell, 10s timeout, capture_output, NO text mode
    nonzero status      -> GitCaptureError, label + status + stderr detail
    stdout decode fails -> GitCaptureError, label + not valid UTF-8
    otherwise           -> stdout decoded strictly as UTF-8

_diff_args(extra)  ["diff", "--no-ext-diff", "--no-color"] + extra + ["--"]

capture_unstaged_diff    -> str        _diff_args([])
capture_staged_diff      -> str        _diff_args(["--cached"])
capture_untracked_paths  -> list[str]  ls-files --others --exclude-standard, splitlines()
```

Deliberate asymmetry, disclosed: `stderr` decodes with `errors="replace"` because it is only a human
diagnostic; `stdout` is strict because it is counted data.

`test_git_adapter.py` has eight tests, and its stand-ins now return BYTES because the adapter performs
the decode itself.

SESSION 2026-09-03 (continued) — REAL-GIT INTEGRATION TESTS, AND A RESOLUTION FINDING.

`EV-P7-INTEGRATION-TEST-303`: the learner sorted candidate assertions between the two test files,
four of five correct at confidence 20 (underconfident). Division settled: controlled tests own exact
call construction and interpretation of prepared results; real-Git tests own whether Git accepts the
arguments and what it actually outputs.

FINDING: `C:/Users/nicol` is itself a Git repository. Every temp directory under
`AppData/Local/Temp` therefore resolves to it, and `git ls-files --others --exclude-standard` there
had to be killed after two minutes while walking the whole home directory. `buildlens analyze` run
anywhere under the home directory would inspect the home repository. The 10-second timeout means it
fails rather than printing wrong numbers, but nothing tells the user which repository was chosen; in
a smaller ancestor repository it would silently print plausible counts for the wrong project.

The learner chose to REPORT the resolved root rather than REQUIRE the directory to be the root, after
the two options were separated: requiring the root would reject running from a subdirectory, which is
normal and legitimate. `capture_repository_root` now exists in the adapter; the CLI display does not.

### Test inventory

```text
test_git_adapter.py              10 controlled tests, bytes stand-ins, no Git required
test_git_adapter_integration.py   8 real-Git tests, throwaway repositories, ~6 s
```

`test_classify.py`, `test_summarize.py`, `test_session.py`, `test_cli.py` unchanged. Six suites total.

Windows detail: Git marks `.git/objects` files read-only, so `tempfile.TemporaryDirectory` needs
`ignore_cleanup_errors=True`.

SESSION 2026-09-03 (continued) — ALL FOUR CAPTURE PATHS EXIST.

`EV-P7-NOINDEX-DESIGN-304`: the predicted reversal test arrived. `--no-index` documents status 1 as
"the files differ", a valid result, while every other caller treats 1 as failure. The learner chose
to add `accepted_statuses` to `_capture` rather than split off a separate function, and answered the
coherence question with a criterion they produced themselves:

```text
a parameter that varies HOW ONE RUN IS JUDGED keeps the job single
a parameter that varies WHAT COMES BACK would split it
```

`_capture` therefore remains one coherent job at four parameters, three required. The default is the
tuple `(0,)` rather than the set `{0}`, because a default is evaluated once at definition time and an
immutable default closes the mutable-default trap by construction.

`EV-P7-NOINDEX-REAL-GIT-305`: real Git was probed BEFORE the test was written, per the standing rule.
Git 2.55 returns status 1 for both a nonempty and an empty new file, and `/dev/null` works on Windows.
The 2026-09-02 requirement was verified end to end against the real summarizer:

```text
helper.py   files_changed=1, lines_added=1, lines_removed=0
empty.py    files_changed=1, lines_added=0, lines_removed=0
```

A guard test asserts the default was not widened for everyone: status 1 still fails the tracked
captures.

### `git_adapter.py` (current)

```text
_capture(repository, args, label, accepted_statuses=(0,))
    runs ["git"] + args, no shell, 10s timeout, capture_output, no text mode
    status not accepted -> GitCaptureError with label, status, stderr detail
    stdout decode fails -> GitCaptureError with label
    otherwise           -> stdout decoded strictly as UTF-8

_diff_args(extra)  ["diff", "--no-ext-diff", "--no-color"] + extra + ["--"]

capture_unstaged_diff(repository)         -> str        _diff_args([])
capture_staged_diff(repository)           -> str        _diff_args(["--cached"])
capture_untracked_paths(repository)       -> list[str]  ls-files, splitlines()
capture_new_file_diff(repository, path)   -> str        _diff_args(["--no-index"])
                                                        + ["/dev/null", path],
                                                        accepted_statuses=(0, 1)
capture_repository_root(repository)       -> str        rev-parse --show-toplevel, stripped
```

### Test inventory

```text
test_git_adapter.py              14 controlled tests, bytes stand-ins, no Git required
test_git_adapter_integration.py  10 real-Git tests, throwaway repositories
test_classify.py / test_summarize.py / test_session.py / test_cli.py   unchanged
```

SESSION 2026-09-03 (continued) — COMPOSITION EXISTS; ITS TRACE GATE IS OPEN.

`EV-P7-COMPOSITION-DESIGN-307`: the learner placed composition in a new `snapshot.py` rather than in
`git_adapter` or `cli`, after the cohesion test showed that adding it to `git_adapter` forces an
"and also" into that module's one-sentence job. Recorded as consistent with the Phase 4 refusal to
split without evidence — there is evidence here, and there was none then.

The Snapshot carries SUMMARIES rather than diff text, so the never-sum rule is stated and tested once
instead of once per front end. Two of the learner's premises were corrected along the way: compute is
identical between the options, and "more could go wrong" was replaced with the concrete Phase 12 API
duplication argument.

FACILITATOR ERROR: the real-repository snapshot result was printed BEFORE the learner was asked to
predict it. That scenario is spent; a fresh one replaces it.

### `snapshot.py`

```text
Snapshot(repository_root, unstaged, staged)   frozen dataclass, two DiffSummary fields

capture_snapshot(repository) -> Snapshot
    runs NO Git command itself
    root      = capture_repository_root
    unstaged  = capture_unstaged_diff + one capture_new_file_diff per untracked path,
                joined, then summarized once
    staged    = capture_staged_diff, summarized separately
    any GitCaptureError propagates; no partial snapshot is returned
```

`test_snapshot.py` has six tests and patches the five capture functions rather than subprocess:
mechanism is tested in the adapter suites, policy here.

### Test inventory

```text
test_git_adapter.py              14 controlled
test_git_adapter_integration.py  10 real-Git
test_snapshot.py                  6 policy, capture functions patched
test_classify.py / test_summarize.py / test_session.py / test_cli.py   unchanged
```

Seven suites, all passing.

SESSION 2026-09-04 — SNAPSHOT TRACE CLOSED.

`EV-P7-SNAPSHOT-TRACE-309` passed, verified against a real repository built to the exact scenario:
6 child processes, UNSTAGED 3/4/1, STAGED 1/2/0, every field matching.

Getting there required supplying the Git model as a prerequisite, and it should be treated as newly
taught rather than known:

```text
tracked vs untracked     does Git know the file at all; git add makes a new file TRACKED
staged vs unstaged       for tracked files, is the change in the index or only the working tree
three places             working tree -> git add -> index -> git commit -> history
two diffs                git diff = working tree vs index; git diff --cached = index vs HEAD
```

The learner independently derived that three versions of a file coexist and that this is why the two
views cannot be summed — they measure adjacent gaps.

TWO FACILITATOR ERRORS, both caught by the learner and both upheld (`EV-P7-NAMING-DETOUR-310`):

1. Their confusion about `unstaged_parts` was escalated into a rename of the whole view to WORKING,
   agreed and applied, then reverted at the learner's instruction. The question was comprehension —
   which Git command emits which file — and was resolved by showing the three commands' real output.
   The worktree was returned to ab2206d; no rename survives.
2. "Working and unstaged are not synonyms" was stated without naming whose vocabulary was meant.
   Inside BuildLens they name the same view; the contrast is only against GIT's term.

STANDING INSTRUCTIONS ADOPTED:

```text
qualify every ambiguous term as Git's or BuildLens's
answer a comprehension question by showing what the code or command actually produces,
    before considering whether a name should change
do not escalate confusion into a design change without first checking the confusion
    is not simply unanswered
```

OPEN ITEM, deliberately not acted on: `unstaged_parts` in `snapshot.py` holds untracked files, which
are not unstaged in Git's vocabulary. The learner rejected renaming it for now. Revisit only if it
causes a real misreading in code, not in conversation.

SESSION 2026-09-04 (continued) — THE VERTICAL SLICE IS COMPLETE AND RUNS.

`buildlens analyze` now inspects the repository resolved from the current directory and prints the
root followed by separately labelled UNSTAGED and STAGED sections. Verified end to end against real
repositories on both paths; the success numbers matched the learner's own prediction from
`EV-P7-SNAPSHOT-TRACE-309`.

```text
SUCCESS   Repository: <root>
          UNSTAGED  Files changed: 3 / Lines added: 4 / Lines removed: 1
          STAGED    Files changed: 1 / Lines added: 2 / Lines removed: 0
          exit 0

FAILURE   Repository: <root>
          UNSTAGED tracked: Git output was not valid UTF-8 text
          Run buildlens analyze again.
          exit 1, stdout empty
```

Learner decisions this slice: `read_diff` deleted after its disuse was verified rather than assumed;
the repository line added to the FAILURE output too, because the wrong-repository hazard bites
hardest when the run fails; and `GitCaptureError` carries the resolved root so no extra Git call is
needed.

`EV-P7-GIT-IS-A-REQUIREMENT-314` — the learner overturned a facilitator premise. A Git-named
exception in `cli.py` was offered as a boundary leak; they pointed out there will never be another
tool. Correct: Phase 13 depends on Git worktrees and Claude Code uses them.

ARCHITECTURAL ASSUMPTION, now explicit:

```text
Git is a requirement of BuildLens, not a swappable choice.
Naming Git in module and type names is accurate, not a leak.
```

A second facilitator claim was WITHDRAWN: two misplaced responsibilities were described as a
reasoning pattern, when the simpler cause was that the learner had not read `snapshot.py` or the new
`cli.py`, both written minutes earlier by Claude.

### Module map, as it now stands

```text
git_adapter   MECHANISM   which Git command, which statuses are valid, decoding
snapshot      POLICY      which view a change lands in, never summing, all-or-nothing
summarize     COUNTING    diff text -> three numbers
classify      COUNTING    one diff line -> one label
session       STATE       in-memory change history, not yet wired to the snapshot path
cli           BOUNDARY    arguments, formatting, streams, exit status
```

SESSION 2026-09-04 (continued) — PHASE 7 MILESTONE TRANSFER PASSED.

`EV-P7-MILESTONE-TRANSFER-315` on a linter surface, with no code on screen and no file lookups.
Module placement, the per-caller status mechanism, representation, reversal condition, and the limits
of a stand-in test all transferred. The surface was built to tempt the wrong representation answer —
pylint's exit code looks meaningful — and the learner still reasoned that stdout alone suffices. Their
reversal condition was sharper than the one they set for BuildLens.

Two facilitator errors recorded: the transfer was first set in an unfamiliar lab-assay domain, which
the learner correctly rejected as vocabulary noise; and the prompt under-specified how the TRACKED
section was produced, leaving the process count ambiguous.

RULE ADOPTED: choose transfer surfaces from domains the learner already knows.

Phase 7 is complete in every required dimension:

```text
implementation       complete — git_adapter, snapshot, cli vertical slice
automated tests      complete — seven suites, controlled and real-Git
learner trace        complete — EV-P7-SNAPSHOT-TRACE-309, EV-P7-CLI-BOUNDARY-313
learner explanation  complete — EV-P7-CLI-BOUNDARY-313, EV-P7-GIT-IS-A-REQUIREMENT-314
transfer variant     complete — EV-P7-MILESTONE-TRANSFER-315
```

ONE ITEM BLOCKS THE PHASE CLOSE: the delayed argparse parser-versus-Namespace retrieval, owed since
Phase 6. Separately, the Git model taught this session was SUPPLIED rather than retrieved and needs
one delayed retrieval before being called held.

SESSION 2026-09-04 (continued) — PHASE 7 IS CLOSED.

The owed argparse retrieval ran on a fresh archive-tool surface (`EV-P7-ARGPARSE-DELAYED-316`). The
item actually owed — parser holds the rules, args holds the parsed values, `args.target` retrieves,
`Namespace(...)` is the representation — PASSED cleanly with no scaffolding.

`SystemExit(2)` lapsed for the third time and was recovered by reading the learner's own
`expect_system_exit_2` helper. Recorded with the distinction that matters:

```text
HELD      the concept — malformed syntax deserves a status distinct from other user
          errors. The learner chose and defended this policy themselves.
NOT HELD  the values SystemExit and 2 as a recalled fact.
```

That is a lookup-able fact living in one line of their own tests, not a mental-model gap. Do not
re-teach the policy. One more delayed retrieval; if it lapses again, stop testing it.

SESSION 2026-09-04 (continued) — PHASE 8 SPECIFICATION OPENED.

`EV-P8-HOOKS-SPEC-317`. Hooks were introduced from real evidence: three of the four hooks the plan
names are already configured on this machine and firing in this session, and the UserPromptSubmit
hook's stdout is visible in the transcript on every learner message.

Hooks were taught as a transfer from Phase 7 rather than as new machinery:

```text
PHASE 7   BuildLens (parent)   -> git (child)          args in, stdout/exit out
PHASE 8   Claude Code (parent) -> hook script (child)  JSON on stdin, stdout/exit out
```

The learner unaided identified both things hooks add over polling — timing, and provenance — and
anticipated Stop's role as the turn boundary. `provenance` was supplied as the name for what they had
already described.

They were partially right that another tool could corrupt provenance; the mechanism is inverted
(Codex fires nothing, rather than firing Claude's hook), but the gap is real and applies to this
project, which is developed with both tools.

ESTABLISHED THIS SESSION, to carry into every Phase 8 patch:

```text
events are a fast signal that something MAY have changed; Git inspection stays authoritative
PostToolUse fires only for Claude's file tools — Bash edits, learner edits, and other tools
    produce changes with no event at all
therefore Stop must re-inspect actual Git state, not trust the event stream
```

ACTOR SCOPE (`EV-P8-ACTOR-SCOPE-318`): the learner scoped the product to TWO actors — the learner
editing through BuildLens, and Claude. Codex is a fact about how BuildLens is built today, not about
what it ships. Accepted; it matches the plan's collaborative-editing section.

That scoping closes two no-event paths but NOT this one, which alone justifies the Stop sweep:

```text
Claude runs sed -i or git checkout through Bash -> no PostToolUse fires
```

OPEN, flagged for the spec: is "the learner edits only through BuildLens" a stated product
assumption, or something BuildLens must tolerate being violated? The plan forbids claiming that
arbitrary external processes cannot bypass the workflow.

No Phase 8 code exists and none is authorized.
SESSION 2026-09-05 — PHASE 8 TRUST BOUNDARY SPECIFIED.

`EV-P8-TRUST-BOUNDARY-319` through `EV-P8-TRANSFER-326`. Payload fields were deliberately withheld
for the whole session; the boundary was derived, not read off a schema.

THE RULE, now established and derived by the learner:

```text
CONTENT       what the files say        Git can settle it       VERIFY
PROVENANCE    who / when / which turn   Git has no record       BELIEVE or reject
```

The learner's own formulation, which is the one to keep:

```text
git cannot see who did what, it just states what was done
```

DECIDED, and binding on every Phase 8 patch:

```text
CONTENT claims     the adapter verifies them against Git; on disagreement GIT WINS
PROVENANCE claims  the adapter records them AS CLAIMS, attributed to the hook, never as facts
never             strip or lose the claim label, so that a later reader can mistake it for fact
```

The learner eliminated the two wrong policies themselves. `verify provenance first` fails because
nothing exists to verify it against — re-asking Claude is asking the same source twice, which the
learner identified unprompted. `discard unverifiable data` fails because it deletes the only question
BuildLens exists to answer.

CONSEQUENCE THE LEARNER SHOULD BE ABLE TO STATE:

```text
the claims BuildLens CAN check are the ones it needs the hook for least
the claim BuildLens CANNOT check is the only reason the hook exists at all
```

TRANSFER PASSED on a CI-webhook surface (`EV-P8-TRANSFER-326`): the commit and branch state are
content-like; the pushing user and timestamp are provenance. The learner also confirmed that a Git
author name does not verify the author, since it is self-declared config — another claim.

FOUND EARLY BY THE LEARNER, deferred to Phase 9: hook and file write are separate operations, so
BuildLens can be asked to look before a change lands or after it is overwritten. This is the ordering
and duplication concern Phase 9 exists for. Do not solve it in Phase 8.

GIT MODEL — FAILED THEN REBUILT THIS SESSION. The owed delayed retrieval lapsed: `git diff HEAD` was
answered as HEAD versus the index. The root cause was NOT operand recall but a misconception about
what the operation returns.

```text
BELIEVED   a diff prints the contents of one side
ACTUAL     a diff prints the difference between two sides
```

Rebuilt via an R0 non-Git list surface, one worked example, then a clean climb. The model now stands:

```text
git diff          index <-> working tree
git diff --cached HEAD  <-> index
git diff HEAD     HEAD  <-> working tree
```

The Phase 7 design rationale is restored with it: `git diff HEAD` skips the index, so staged and
unstaged work both appear in one call.

No Phase 8 code exists and none is authorized.

SESSION 2026-09-05 (second sitting) — OBSERVED-VERSION RECORD DERIVED.

TWO OWED RETRIEVALS CLEARED.

The three-place diff model is now HELD (`EV-P8-DIFF-INVERSE-327`). It was retrieved unaided on a new
surface and in the reverse direction — given diff output, reconstruct the cause. One wrong field was
notation only (`-` read as an addition), corrected in a single exchange.

The deferred adversarial state was constructed by the learner (`EV-P8-STAGED-ONLY-STATE-328`):

```text
1  edit api.py
2  git add api.py
3  edit api.py back to its original content
   -> git diff HEAD prints nothing while git diff --cached prints something
```

Consequence flagged for the adapter, NOT yet decided: the choice of comparison bounds what BuildLens
can observe at all.

THE PRODUCT JUSTIFICATION IS NOW DERIVED, NOT ASSERTED (`EV-P8-WHY-BUILDLENS-329`). The learner
objected that Git can answer content questions too. That objection was tested rather than waved away,
and the learner traced their way to:

```text
Git answers questions about states it was handed — commits and the index
BuildLens answers questions about states nobody ever handed Git, which exist
    for minutes and are then overwritten forever
```

Two corrections were needed on the way, both recorded in the ledger: tracked-versus-untracked is not
the reason a lost version is unrecoverable, and a hook preserves nothing — it is a signal that
arrives and is gone.

TRUST BOUNDARY SHARPENED by the learner's own question ("I thought we were storing them as a claim
not a fact?"). Both halves now stated:

```text
what the hook told BuildLens     claim, labelled, unverifiable
what BuildLens saw for itself    observation, first-hand
```

Storing provenance as a claim does not mean declining to store observed content.

RECORD FIELDS DERIVED BACKWARDS FROM QUERIES (`EV-P8-RECORD-FIELDS-330`), with the plan's list
withheld until after commitment. Four of six derived:

```text
repository-relative path   derived, and reused the Phase 7 boundary unprompted
base commit                derived by asking where a diff chain starts
observed-at time           derived
provenance                 derived, correctly hedged as a claim
content hash               derived in the third sitting, after the hashlib loop
session/worktree id        NOT derived — needs the isolated-worktree fact
```

The learner chose to store FULL CONTENT rather than diffs, and after one wrong defense produced the
correct one: replaying a chain of diffs costs more than a single read. Noted that Git does both.

No Phase 8 code exists and none is authorized.

```text
phase                       Phase 8 — five of six record fields derived, no code
last knowledge gate         hashing: both directions of the guarantee, and that a digest
                            proves neither authorship nor authority
                            (EV-P8-HASH-DETERMINISM-333, transfer EV-P8-HASH-TRANSFER-334)
next retrieval due          THREE items, fresh surfaces, later sessions:
                            1. SystemExit(2) — third lapse already spent; if it lapses again,
                               stop testing it
                            2. the believe/verify rule, unaided, on a surface that is neither
                               hooks nor CI webhooks
                            3. the hash asymmetry — held only after repeated flipping between the
                               forward and backward directions; retrieve it cold on a new surface
                            CLEARED: the three-place diff model, now HELD
next architecture reset     complete; next by time or major transition
next implementation step    THE SIXTH RECORD FIELD: session/worktree id. This requires showing
                            that Claude Code Desktop uses an ISOLATED WORKTREE for Git-backed
                            sessions — a fact the learner has not been given. Do not present the
                            record model as finished until they can say why a worktree id is not
                            redundant with a repository path.
                            Then: is session.py the right home for these records?
                            Still open from 2026-09-04: is "the learner edits only through
                            BuildLens" a stated product assumption, or something BuildLens must
                            tolerate being violated?
deferred to a later slice   launch failure (FileNotFoundError) and timeout (TimeoutExpired)
                            normalization; neither is handled by _capture today.
                            Storage mechanism for records (SQLite vs file) — Phase 10.
                            Hook-versus-write ordering and duplication — Phase 9; found early by
                            the learner and deliberately not solved here.
milestone owed              none; Phase 7 milestone is complete
major/deep counter          1/2. Cumulative review due after the SECOND completed major phase,
                            so NOT due before Phase 8.
last published commit       see git log
```

Files the learner should currently be able to teach:

- `cli.py`
- `git_adapter.py`
- `snapshot.py`
- `test_git_adapter.py`
- `test_git_adapter_integration.py`
- `test_snapshot.py`
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
