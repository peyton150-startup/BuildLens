# HANDOFF — Quiz Session 2 (for Sol / Codex)

You are picking up a learning-first project mid-stream. Read `CLAUDE.md` first; it governs
everything below and it overrides your defaults. `HANDOFF_QUIZ.md` is the previous handoff and is
now partly stale — this file supersedes it.

This session continues a **quiz**. Do not implement Phase 4. Do not write new product code.

---

## What exists right now

```text
classify.py     Phase 1   classify_diff_line(line) -> file_header | metadata | added | removed | context
summarize.py    Phase 2   summarize_diff(diff_text) -> dict of three counts
session.py      Phase 3   class Session: __init__, record, history

test_classify.py     green
test_summarize.py    green
test_session.py      green, five tests
```

Confirm this yourself before quizzing. Never assert it from this document.

```bash
cd C:/Users/nicol/BuildLens_Project && python test_classify.py && python test_summarize.py && python test_session.py
```

101 evidence records in `learning/LEARNING_LEDGER.md`. `CURRENT_STATE.md` is authoritative.

---

## The rules that get broken most often

```text
never reveal the answer before the learner commits to one
require a confidence tag (0 to 100) on every answer
a wrong answer makes the NEXT problem SIMPLER, not merely different
do not lecture after a wrong answer
preserve the learner's verbatim first answer in the ledger, never rewritten
wrong attempts are not phase failures; no attempt-count penalty
do not run code before the learner predicts its output
```

---

## What session 1 closed — do NOT re-teach these

Four exercises, records `EV-P1-HEADER-097` through `EV-P1-RETURN-100`.

```text
file_header             CLOSED. Cold, unseen diff, unseen domain, eight lines
                        labelled, all eight correct including the @@ hunk header.
                        This was the project's most persistent gap at 13 prior
                        appearances. It is no longer the top target.

nested_call_evaluation  CLOSED. Traced bump(bump(3)) unaided, named the inner call
                        as first, carried the intermediate value, handled 3 > 3
                        correctly. This was the Phase 1 gate as written in the plan.

branch_precedence       MECHANISM CLOSED. Stated first-match-wins unaided and
                        transferred it to a non-diff domain immediately.
                        See the caveat below — it is not fully MASTERED.
```

Also still solid from earlier sessions, per the previous handoff: the three diff labels, TDD
red-then-green, contract thinking, purity, list accumulation, instance vs class attributes,
aliasing vs copying.

---

## The one real finding from session 1

**The learner's misses are procedural, not conceptual.**

Twice in one session they answered a per-item question at the group level:

```text
asked   which line numbers change, and to what
gave    "the metadata becomes added"        (line 1 becomes REMOVED; line 3 does not change)

asked   which of these four inputs change
gave    "the top 3"                         ("/about" returned page before AND after)
```

Both times, the moment a single item was isolated, they answered correctly and diagnosed it
themselves — "ok i misread again". The branch-selection model is sound. The habit of scanning a
group and answering for the group is what fails.

**How to handle this:** do not re-teach branch logic. Force per-item enumeration in the question
itself — "answer for each one separately, one line per item". If they still group, isolate one
item, do not descend into a concept lesson.

The second miss came at **confidence 90**, the highest of the session and the only overconfident
one. Everything else was underrated as usual.

---

## WEAK AREAS — targets for this session

Ranked. The first two are the real ones.

### 1. `print_vs_return` — partial, self-corrected, NOT cold

At `EV-P1-RETURN-100` the learner first said `describe(4)` produces `answer: positive`, then
reversed themselves inside the same answer: "also label returns nothing it prints it". Correct
concept, retrieved unaided — but the *first* instinct was still the printed value, and this is the
second consecutive session where this idea was self-corrected rather than answered right initially
(see `EV-P3-LEAK-095-CLOSE`).

Retrieve it in a form where the `None` goes somewhere non-obvious: stored in a list, compared with
`==`, or used as an `if` condition. Not another string concatenation — they have now seen that one.

### 2. `branch_precedence` — enumeration half still owed

Mechanism is proven twice. The "which items actually change" half failed twice. Give it once more
after a gap, phrased as a per-item question, and require item-by-item answers.

### 3. `output_and_exit_status_are_independent` — ATTEMPTED AND FAILED, must be re-run

Given at the end of session 1 as a shell/grep transcript, per the constraint. It **failed**, and
the constraint means it does not count: the learner ended up seeing the answer rather than
producing it. See `EV-P1-EXIT-101`.

Two blockers surfaced, in this order:

```text
1  `$?` was unreadable        the learner read grep's output instead of echo's
2  0-is-success did not stick  stated twice, inverted both times, because it
                              collides with 1-is-truthy from Python
```

Do NOT re-ask the CI question first. The convention itself needs a cold retrieval before the
independence idea is worth testing again. Then resume the worked-example sequence at step B: the
learner explains the build-log case back in their own words, then solves a fresh one in the
**reverse** direction — a step that succeeds silently, prints nothing, and gets marked failing.
That direction was never touched.

### 4. The `splitlines` family and string-method immutability

Tags: `splitlines_splits_on_spaces`, `splitlines_is_a_printing_operation`,
`splitlines_input_is_a_list`, `string_methods_mutate`. Marked "re-learned, retrieval still due".
Test whether they see `word.upper()` and `sorted()` vs `.sort()` as ONE principle or two facts.

### Records still marked `open`

```text
EV-P2-MODEL-060   named the right three fields, computed them from the wrong diff,
                  did not name the individual values
EV-P3-RECORD-094  self binding, = vs ==, == comparing list contents in order
```

Close both or confirm they are still open. `EV-P3-RECORD-094` pairs naturally with the
`print_vs_return` retrieval, since `==` on a `None` result is one question.

---

## Owed from Phase 3, still outstanding

```text
learner explanation   teach session.py aloud, in their own words
transfer variant      the aliasing/copying idea in a domain with no sessions in it
```

Neither was reached in session 1. Both are short. They are the Phase 3 milestone and they gate the
move to Phase 4.

---

## Suggested shape

Do not run all of it. Pick by what the early probes reveal.

```text
1  print_vs_return retrieval, None in a non-obvious place    the live gap
2  exit status retrieval, NOT a Python test run              owed, constrained
3  teach-aloud on session.py                                 Phase 3 milestone
4  transfer variant for aliasing, non-session domain         Phase 3 milestone
5  branch_precedence enumeration, per-item phrasing          if time
6  splitlines / immutability as one principle                lower priority
```

---

## Calibration — mention only if the learner raises it

They systematically **under**rate correct answers. Session 1: an 80 on a flawless eight-line
answer, a 90 on a fully correct unaided trace, a 40 on an answer they then self-corrected to
correct. The single overconfident answer was the 90 on the grouping miss.

Keep requiring the tag. Do not lecture about it.

---

## Session close

Follow `CLAUDE.md`. Append an Evidence Record per exercise with the verbatim prompt and the
learner's verbatim first committed answer, update `CURRENT_STATE.md`, then push.

Repo `https://github.com/peyton150-startup/BuildLens`, branch `main`.

**Important:** the working directory `C:/Users/nicol/BuildLens_Project` is NOT a clone of origin —
it has no commits and no remote. Publishing means: clone origin to a temp `_sync` directory, copy
changed files in, verify the suites are green there, commit, push, confirm hashes match, remove the
directory.

**Known trap:** heredocs containing apostrophes have broken this workflow twice. Write long content
to a scratch file first, then `cat` it into place.
