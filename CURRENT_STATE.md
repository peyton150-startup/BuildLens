# BuildLens — Current State

> **Maintenance rule:** this file is a replace-in-place snapshot, not a session log. Update or remove
> obsolete statements whenever state changes. Preserve historical prompts, answers, remediation, and
> rationale in `learning/LEARNING_LEDGER.md`, `QUIZZES.md`, and Git history.

Last updated: 2026-08-29

## Lifecycle

**Current phase:** Phase 3 complete. Phase 4 has not started.

Phase 3 is complete in every required dimension:

```text
implementation       complete
automated tests      complete
learner trace        complete
knowledge gate       complete
learner explanation  complete — EV-P3-TEACH-185
transfer variant     complete — EV-P3-TRANSFER-186
```

Phase 4 implementation is paused for the overdue formal Phase 0–2 cumulative checkpoint.

## Exact code that exists

### `classify.py`

`classify_diff_line(line)` accepts one unified-diff line and returns exactly one label.

Branch order is intentionally most-specific first:

```text
"diff --git"                              → file_header
"index ", "--- ", "+++ ", or "@@"       → metadata
leading "+"                               → added
leading "-"                               → removed
otherwise                                 → context
```

The input and outside state remain unchanged.

### `summarize.py`

`DiffSummary` is a dataclass with:

```text
files_changed
lines_added
lines_removed
```

`summarize_diff(diff_text)`:

```text
one complete diff string
→ splitlines()
→ classify each line
→ increment three fresh local counters
→ return one DiffSummary
```

Only `file_header`, `added`, and `removed` affect counters. Metadata and context do not.

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

Known limitation: `changes` is public. A caller can still mutate real state directly with
`session.changes.append(...)`. Copying in `history()` protects only against mutation through the
returned snapshot.

## Automated verification

The repository has three directly executable suites:

```text
python test_classify.py   — 8 test functions
python test_summarize.py  — 1 end-to-end summary test function
python test_session.py    — 5 test functions
```

All three passed locally and in the publishing clone before commit `2545047`. No product code has
changed since that verification.

The load-bearing Session test is
`test_mutating_the_history_does_not_touch_the_session`. Replacing the copy with an alias makes the
test compare actual `["diff A", "diff B"]` with expected `["diff A"]` and fail.

## Current execution paths

```text
diff line
→ classify_diff_line
→ one label
```

```text
complete diff string
→ split into lines
→ classify each line
→ update local summary counters
→ DiffSummary
```

```text
Session()
→ fresh instance-owned changes list
→ record(diff_text) mutates that list in order
→ history() returns a separate snapshot
```

## Current learning evidence

Demonstrated through delayed or transferred retrieval, but not permanently mastered:

- longest-prefix-first branch precedence;
- output versus return values, including implicit `None`;
- `.sort()` mutation/`None` versus `sorted()` allocation;
- aliases versus copies and object identity;
- list-literal allocation, including outer mixed-value lists;
- shared dictionary mutation and fresh local counters;
- transitive observable effects through called functions;
- per-instance state, copied snapshots, and the public-attribute limitation;
- whole-program object counting after adaptive remediation.

Known cold from delayed evidence:

- branch precedence for unified-diff headers versus source additions/removals;
- shell exit status `0` means success;
- `Session.history()` must copy to prevent snapshot mutation from reaching session state.

Still uncertain or due for later retrieval:

- retaining every object/allocation under heavy composition without a state freeze;
- confidence calibration: several correct answers were underconfident and some misses were reported
  at confidence 100;
- precise runtime-contract language: current code does not coerce or validate `diff_text` as a
  string;
- shallow-copy depth when mutable elements are eventually introduced.

## Last completed gates

- Requested three-question Phase 0–2 super-hard review: complete after remediation.
- Phase 3 state movie and alias/copy knowledge gate: complete.
- `session.py` learner teach-back: complete (`EV-P3-TEACH-185`).
- Unrelated `InspectionLog` snapshot transfer: complete (`EV-P3-TRANSFER-186`).

Do not mark these concepts permanently mastered after one review sequence.

## Cumulative-review and architecture counters

The first foundation counter was triggered by Phase 2 completion. It has no valid reset record:
earlier fundamentals questions were not recorded with exercise type `CUMULATIVE_RETRIEVAL`.
Historical attempts must not be retroactively relabeled.

Before Phase 4 code, complete four formal questions:

```text
Q1 DEBUG / TEST      classification precedence and summary consequence
Q2 TRACE / EXPLAIN   return value, output, and per-call local state
Q3 CONTRACT / APPLY  DiffSummary contract and boundary case
Q4 ARCHITECTURE      current shape, split trigger, alternative, downside, reversal condition
```

Question 4 doubles as the architecture reset before the Phase 4 decomposition transition. Reset
only the foundation counter after all four pass. Phase 3 then counts as 1/3 toward the next
foundation checkpoint covering Phases 3–5.

## Open interaction

**Cumulative checkpoint questions 1–3 passed. Question 4 is next.**

Evidence `EV-CUM-FND-187`: at confidence 100, branch shadowing, longest-prefix-first repair, and test
purpose were correct. The learner recovered the missed space-leading context line and supplied the
faulty-code counts: added 2, removed 2, metadata 0, context 1.

Evidence `EV-CUM-FND-188`: cumulative question 2 passed at confidence 90. The learner correctly
traced fresh local lists across two calls, distinguished internal output from returned values, and
gave the exact final output order.

Immediate next prompt: cumulative question 3, applying the `DiffSummary` contract and empty-input
boundary.

Evidence `EV-CUM-FND-189`: question 3 initially paused because physical newlines in a triple-quoted
string were thought absent without visible `\n`. The R0/R1 remediation passed at confidence 90:
`"""red\nblue""".splitlines()` was correctly modeled as `["red", "blue"]`. Resume the unchanged
two-file summary target; do not repeat the syntax explanation.

Evidence `EV-CUM-FND-189`: question 3 passed after remediation. The learner recovered triple-quoted
newline representation, computed `DiffSummary(2, 2, 1)`, identified exact contributing lines,
explained metadata precedence and context exclusion, predicted the all-zero empty result, and stated
no input/outside mutation. After briefly proposing `None` for the assertion, the learner recovered
the explicit return as `DiffSummary(0, 0, 0)` at confidence 80.

Immediate next prompt: cumulative question 4 of 4, an architecture defense that also serves as the
pre-Phase-4 architecture reset. Do not repeat question 3.

## Exact next step

```text
ask cumulative question 4 of 4
→ remediate only if needed
→ reset foundation counter after it passes
→ record/reset the foundation counter
→ begin Phase 4 intent and architecture discussion
```

There is no authorized product-code patch yet. Phase 4 is decomposition by refactoring: the learner
must first identify the concrete responsibility split and defend why the current single-module shape
has become uncomfortable. Do not scaffold future frameworks or layers.

## Session-close fields

```text
phase                       Phase 3 complete; Phase 4 not started
last knowledge gate         EV-P3-TRANSFER-186, passed at confidence 100
next retrieval due          cumulative checkpoint 4 of 4
next architecture reset     question 4 itself
next implementation step    none until the formal checkpoint passes
last published commit       2545047
```

Files the learner should currently be able to teach:

- `classify.py`
- `summarize.py`
- `session.py`
- `test_classify.py`
- `test_summarize.py`
- `test_session.py`

Historical evidence lives in:

- `learning/LEARNING_LEDGER.md` — exact formal prompts, committed answers, evaluation, remediation;
- `QUIZZES.md` — readable quiz transcript;
- Git history — prior full versions of this snapshot and all published state.
