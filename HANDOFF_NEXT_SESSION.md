# BuildLens Handoff — Continue the Post-Phase-5 Cumulative Review

Use this handoff to continue with Claude Opus. `CURRENT_STATE.md` is authoritative if anything here
conflicts with it.

## Required reading and behavior

Follow `AGENTS.md`. Before implementation, read its required project documents in the stated order.
For the immediate teaching interaction, read the latest Phase 5 and cumulative-review evidence at
the end of `learning/LEARNING_LEDGER.md`.

Do not reveal an exercise answer before the learner commits. Record every formal prompt and the
learner's exact first answer. After an incorrect answer, descend to the smallest blocker, recover it,
use near-transfer, and return to a fresh target-level problem.

## Authoritative lifecycle state

Phase 5 — Explicit Interfaces / Contracts is complete:

```text
implementation         EV-P5-SESSION-IMPLEMENTATION-248
automated verification EV-P5-COMPLETE-259
learner trace          EV-P5-SESSION-POSTPATCH-TRACE-249
learner explanation    EV-P5-ANNOTATION-VALIDATION-250
transfer variant       EV-P5-RETRY-TRANSFER-COMPLETE-258
```

The foundation counter reached 3/3 from Phases 3, 4, and 5. The mandatory cumulative foundation
review is in progress. Do not begin substantial Phase 6 work until the review passes and that
counter is explicitly reset.

## Product code that now exists

`session.py` enforces the approved supported-path invariant:

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

Contract boundary:

- annotations communicate but do not automatically validate in ordinary Python;
- `record` performs runtime validation before mutation;
- rejected writes leave `_changes` unchanged;
- supported mutable access is internal;
- `history()` returns a new copied list;
- the guarantee is scoped to supported API paths, not arbitrary Python introspection.

`test_session.py` has seven tests, including non-string rejection/unchanged history, internal storage,
and snapshot mutation isolation. The last fresh verification passed:

```text
python test_session.py   → test passed
python test_classify.py  → test passed
python test_summarize.py → test passed
```

Published commit, verified on `origin/main`:

```text
fc9eb20 — feat: enforce Session string contract
```

The ordinary local checkout may still be behind and dirty because publishing used a verified
temporary clone. Preserve local/user changes; do not reset or overwrite them merely to match the
remote.

## Cumulative review progress

Question 1 — state identity and snapshots:

```text
EV-CUM-FND-260 — passed at confidence 90
```

Question 2 — cross-module dependency/value flow:

```text
EV-CUM-FND-261  — original inbox/priority target was partial
EV-CUM-FND-261A — exact returned labels repaired: urgent, normal, urgent
EV-CUM-FND-261C — learner clarified that impossible direct access was only hypothetical
EV-CUM-FND-261D — reduced returned-data/caller-mutation chain passed at confidence 100
```

The learner understands the reduced principle: a callee returns data; the caller reads it and owns
its later local mutation. The adaptive protocol still requires a fresh target-level R6 return before
question 2 can close.

Do not repeat the `choose` / `count_one` micro-example. Do not infer a same-name-local misconception;
the learner explicitly clarified that they know such direct access is impossible.

## Exact unanswered resume prompt

Present this prompt without revealing its answer:

```python
# grading.py
def grade_score(score):
    if score >= 80:
        return "pass"

    return "review"
```

```python
# dashboard.py
from grading import grade_score


def count_reviews(scores):
    review_count = 0

    for score in scores:
        outcome = grade_score(score)

        if outcome == "review":
            review_count += 1

    return review_count
```

Call:

```python
result = count_reviews([92, 73, 80, 61])
```

Ask:

```text
Which module depends on which? =
Arguments passed into grade_score, in order =
Values returned by grade_score, in order =
Final review_count =
Final result =
Which function directly mutates review_count? =
How does grade_score influence the result without mutating review_count? =
Confidence =
```

If this fresh target passes, record it as `CUMULATIVE_RETRIEVAL`, close question 2, and continue the
review one question at a time. If it fails, remediate only the newly observed blocker.

## Remaining review coverage

Aim for approximately five cumulative questions. After question 2, cover the remaining Phase 3–5
priorities with fresh surfaces:

1. annotation versus runtime validation plus rejection-before-mutation;
2. tests as executable contracts—name which realistic mutation a test catches;
3. evidence-based architecture timing/dependency direction, including a downside and reversal
   condition.

Avoid repeating completed Session and RetryPolicy traces unless remediation genuinely requires a
smaller neighboring example. Syntax-only help remains mandatory: if the learner cannot read a form,
stop the surrounding problem, isolate one syntax form, and rebuild gradually.

## Completion boundary

When all cumulative questions pass:

1. record every Evidence Record;
2. update `CURRENT_STATE.md` replace-in-place;
3. reset only the foundation counter that reached 3/3;
4. do not mark concepts permanently mastered from this review alone;
5. begin Phase 6 specification/intent work—not automatic CLI implementation;
6. obey the Phase 6 adjacent-learning and pre-patch gates before code changes.

## Working-tree safety

There are pre-existing local modifications and untracked project/tool files. Preserve them. Do not
stage broad paths or use destructive Git commands. If the learner asks to publish, use the existing
verified temporary-clone workflow and copy only intended files.
