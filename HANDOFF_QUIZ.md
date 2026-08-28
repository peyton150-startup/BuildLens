# HANDOFF — Review and Quiz Session

You are picking up a learning-first project mid-stream. Read `CLAUDE.md` first; it governs
everything below and it overrides your defaults.

This session has one job: **quiz the learner on Phases 1 to 3 and strengthen the weak areas.**
Do not implement Phase 4. Do not write new product code.

---

## What exists right now

```text
classify.py     Phase 1   classify_diff_line(line) -> "added" | "removed" | "context"
summarize.py    Phase 2   summarize_diff(diff_text) -> dict of three counts
session.py      Phase 3   class Session: __init__, record, history

test_classify.py     green
test_summarize.py    green
test_session.py      green, five tests
```

All three suites exit 0. Confirm this yourself before quizzing — never assert it from this
document.

```bash
cd C:/Users/nicol/BuildLens_Project && python test_classify.py && python test_summarize.py && python test_session.py
```

96 evidence records exist in `learning/LEARNING_LEDGER.md`. `CURRENT_STATE.md` is 2138 lines.
Both are authoritative; this file is a summary and may be stale.

---

## The rules you must follow

From `CLAUDE.md` and `learning/LEARNING_RULES.md`, the ones that get broken most often:

```text
never reveal the answer before the learner commits to one
require a confidence tag (0 to 100) on every answer
a wrong answer makes the NEXT problem SIMPLER, not merely different
do not lecture after a wrong answer
preserve the learner's verbatim first answer in the ledger, never rewritten
wrong attempts are not phase failures; no attempt-count penalty
```

**Syntax-only help mode.** If the learner says they cannot read a piece of syntax, stop solving
the surrounding problem. Explain only that syntax form, give a tiny example, have them read it,
then rebuild. This has been needed repeatedly and skipping it has never worked.

**Do not run code before the learner predicts its output.** Prediction first, every time. This is
the single most productive habit in the record so far.

---

## Established performance — do not re-teach these

Across 96 records: 33 correct, 29 partial, 4 wrong. The partials are usually right-shape,
wrong-detail, not confusion.

Solid, demonstrated more than once, on unseen surface forms:

```text
the three diff line labels and why order matters once known
TDD red-then-green, including why a test that passes first is suspect
function contract thinking: in / out / unchanged
purity, and why classify is easy to test
list accumulation in a loop
instance attributes in __init__ vs class attributes in the class body
aliasing vs copying, and why history() returns list(self.changes)
tests as a world you control
```

The learner discovered the class-attribute trap themselves and proposed the mutation-leak test
before having the vocabulary for it. Treat both as owned.

---

## WEAK AREAS — this is the session's target

Ranked by evidence weight. Quiz these; the list above is background.

### 1. `file_header` — 13 separate appearances, the most persistent gap in the project

Confusion about lines like `+++ b/file.py` and `--- a/file.py` in a unified diff. They start with
`+` and `-` but are **metadata, not content changes**. Related tags: `files_changed`,
`diff_a_b_prefixes_are_two_files`, `test_file_header_is_metadata`,
`unified_diff_metadata_meaning`.

The learner has been corrected on this repeatedly and it keeps resurfacing in new surface forms.
Assume it is NOT stable. Probe it early with a diff they have not seen.

### 2. `branch_precedence` — 5 appearances, and an OWED retrieval

Which branch wins when conditions overlap, and why `if/elif` order changes behavior. Marked in
`CURRENT_STATE.md` as: **unaided, after a longer gap, then MASTERED.** It has never been given
that clean unaided retrieval. Give it in this session, cold, with no warning and no lead-in.

### 3. `output_and_exit_status_are_independent` — OWED retrieval, with a constraint

A program can print "test passed" and still exit non-zero, and vice versa. The state file is
explicit about how to test this: **unaided, unannounced, and NOT via a Python test run.** Use a
different context entirely — a shell command, a non-Python program — or the retrieval does not
count.

### 4. `return_value_is_the_call_expression` — re-slipped recently

A function that computes and does not `return` yields `None`. This was re-demonstrated at
`EV-P3-LEAK-095-CLOSE` when the learner built a copy and did not return it. They self-corrected,
but the slip means it is not cold. Due for retrieval after a gap.

### 5. The `splitlines` family and string-method immutability

Tags: `splitlines_splits_on_spaces`, `splitlines_is_a_printing_operation`,
`splitlines_input_is_a_list`, `string_methods_mutate`.

Marked "re-learned, retrieval still due". The general principle — `word.upper()` returns a new
string, it does not change `word` — was extended at the end of Phase 3 to `sorted()` vs `.sort()`.
Test whether the learner sees those as the same principle or two facts.

### 6. `nested_call_evaluation`

Which call runs first in `f(g(x))`. Two appearances, never given a clean unaided check.

### Two records still marked `open`

```text
EV-P2-MODEL-060   named the right three fields, computed them from the wrong diff,
                  did not name the individual values
EV-P3-RECORD-094  self binding, = vs ==, == comparing list contents in order
```

Close both or confirm they are still open.

---

## Calibration — mention only if the learner raises it

The learner systematically **under**rates correct answers. Recent low-confidence answers that were
right: a `30` on a correct state prediction, a `40` on a correctly-hedged design answer. The one
notable overconfident miss was an alias trace at `100`.

Do not turn this into a lecture. Keep requiring the tag; let the pattern speak.

---

## Owed from Phase 3, still outstanding

```text
learner explanation   teach session.py aloud, in their own words
transfer variant      the aliasing/copying idea in a domain with no sessions in it
```

Both are short. They belong in this session if quizzing goes well.

---

## Suggested shape for this session

Do not run all of this. Pick by what the early probes reveal.

```text
1  cold open on file_header with an unseen diff          the biggest gap
2  branch_precedence retrieval, unaided, no warning      owed
3  exit status retrieval, NOT a Python test run          owed, constrained
4  teach-aloud on session.py                             Phase 3 milestone
5  transfer variant for aliasing, non-session domain     Phase 3 milestone
6  nested_call_evaluation or splitlines, if time         lower priority
```

If the learner struggles on 1, drop the scaffold rung and stay there. The plan is not a schedule.

---

## Session close

Follow `CLAUDE.md`. Append an Evidence Record per exercise with the verbatim prompt and the
learner's verbatim first committed answer, update `CURRENT_STATE.md`, then push.

The repo is `https://github.com/peyton150-startup/BuildLens`, branch `main`. The working pattern
used so far: clone to a temp `_sync` directory, copy changed files in, verify the suites are green
there, commit, push, confirm local and origin hashes match, remove the directory.

**Known trap:** heredocs containing apostrophes have broken this workflow twice. Write long
content with the Write tool to a scratch file first, then `cat` it into place.
