# BuildLens — Current State

> **Maintenance rule:** this file is a replace-in-place snapshot, not a session log. Update or remove
> obsolete statements whenever state changes. Preserve historical prompts, answers, remediation, and
> rationale in `learning/LEARNING_LEDGER.md`, `QUIZZES.md`, and Git history.

Last updated: 2026-08-29

## Lifecycle

**Current phase:** Phase 5 contract audit in progress. No product-code change is currently justified
or authorized.

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
        self.changes = []

    def record(self, diff_text):
        self.changes.append(diff_text)

    def history(self):
        history_list = list(self.changes)
        return history_list
```

Each construction runs `__init__`; `[]` creates a fresh list; `self.changes` attaches it to that
instance. `record` appends the exact passed object in order. `history` returns a shallow snapshot,
not an alias.

Known limitation: `changes` is public. A caller can mutate real state directly with
`session.changes.append(...)`. Copying in `history()` protects only against mutation through the
returned snapshot.

## Automated verification

```text
python test_classify.py   — 8 test functions
python test_summarize.py  — 1 end-to-end summary test function
python test_session.py    — 5 test functions
```

All three passed locally and in the publishing clone before commit `e3a5838`. No product code has
changed since.

The load-bearing Session test is `test_mutating_the_history_does_not_touch_the_session`. Returning
an alias changes the actual value to `["diff A", "diff B"]` and makes its expected `["diff A"]`
assertion fail.

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

Do not mark these concepts permanently mastered after one review sequence.

## Cumulative-review counters

The Phase 0–2 foundation counter was reset on 2026-08-29 after four formal cumulative questions
passed with remediation where needed.

Phases 3 and 4 now count as 2/3 toward the next foundation checkpoint. The next foundation review
triggers after Phase 5 before substantial Phase 6 work.

The major/deep Phase 7–15 counter has not started.

## Open interaction and exact next step

There is no unanswered quiz question. Phase 5 remains open at the next contract-audit step.

Continue Phase 5 as an intent/contract audit, not an automatic code patch:

```text
inspect the contracts already expressed by classify.py, summarize.py, and session.py
→ identify what values/types cross each module boundary
→ distinguish documentation/type hints from runtime validation
→ identify one concrete contract ambiguity or explicitly conclude no patch is earned yet
```

Completed Phase 5 evidence now establishes:

```text
documented contract excludes the integer
→ docstring does not enforce
→ no explicit validation exists
→ integer lacks startswith
→ AttributeError stops execution before fallback else

summarize_diff local line: str
→ classify_diff_line
→ label: str
→ local integer accumulator
→ final DiffSummary record
```

Resume by auditing the existing `Session.record(diff_text)` and `Session.history()` interfaces:

```text
exact input value/type
→ state mutation or non-mutation
→ exact output value/type
→ documented assumption
→ explicit runtime validation, if any
```

Then use one different-surface transfer and ask the learner to identify a concrete contract
ambiguity or explicitly conclude no Phase 5 patch is earned. Do not add type hints or validation
before the learner proposes the intended contract behavior.

Phase 4 confirmed that no restructure is earned. Do not revisit that decision or manufacture a
package/file move during Phase 5 without new evidence.

If a Phase 5 contract patch becomes justified, first state the required pre-patch block from
`AGENTS.md` and run the implementation-adjacent prediction/transfer loop.

## Session-close fields

```text
phase                       Phase 5 contract audit in progress
last knowledge gate         EV-P5-INTERFACE-197, correct after remediation at confidence 90
next retrieval due          Session.record/history interface contract audit
next architecture reset     complete; next by time or major transition
next implementation step    none until the Phase 5 audit finds an earned contract change
last published commit       d2d2652
```

Files the learner should currently be able to teach:

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
