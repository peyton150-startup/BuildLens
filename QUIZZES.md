# QUIZZES — verbatim questions and answers

Every quiz question as it was asked, and every answer as it was given. Nothing rewritten,
nothing cleaned up. Spelling and punctuation are the learner's own.

The Learning Ledger holds the evaluation and the remediation chain. This file is just the record
of what was asked and what came back.

---

# Session 2 — 2026-08-28

Review and quiz session. No implementation. Covered Phases 1 to 3.

---

## Q1 — file_header, cold open

**Asked:**

Here is a unified diff you have not seen. It is from a garden-planner project, not BuildLens.

```text
1   --- a/planting/schedule.py
2   +++ b/planting/schedule.py
3   @@ -8,6 +8,7 @@
4        rows = load_rows(bed)
5   -    total = 0
6   +    total = len(rows)
7   +    logged = True
8        return total
```

For **each numbered line**, tell me what it is.

Give me eight answers, one per line number, then your confidence tag.

**Answered:**

```text
1.metadata
2.metadata
3.metadata
4.context
5.removed
6.added
7.added
8.context
80
```

**Outcome:** all eight correct. `EV-P1-HEADER-097`, result `correct`.

---

## Q2 — branch_precedence, reordering the real classifier

**Asked:**

This is `classify.py` as it exists in your repo right now.

```python
def classify_diff_line(line):
    if line.startswith("diff --git"):
        return "file_header"
    elif (
        line.startswith("index ")
        or line.startswith("--- ")
        or line.startswith("+++ ")
        or line.startswith("@@")
    ):
        return "metadata"
    elif line.startswith("+"):
        return "added"
    elif line.startswith("-"):
        return "removed"
    else:
        return "context"
```

Suppose someone moves the `startswith("+")` branch and the `startswith("-")` branch **above** the
metadata branch, changing nothing else — same conditions, same return values, just reordered:

```python
def classify_diff_line(line):
    if line.startswith("diff --git"):
        return "file_header"
    elif line.startswith("+"):
        return "added"
    elif line.startswith("-"):
        return "removed"
    elif (
        line.startswith("index ")
        or line.startswith("--- ")
        or line.startswith("+++ ")
        or line.startswith("@@")
    ):
        return "metadata"
    else:
        return "context"
```

Feed the eight lines from Question 1 into this reordered version.

Which line numbers get a **different** label than before, and what does each of those become?
Confidence tag.

**Answered:**

```text
the meta data becomes added which is incorrect, 80, you switched the metadata and the added in the
elif, which makes it call metadata added because they both start with a +
```

**Outcome:** mechanism correct, enumeration missing. `EV-P1-BRANCH-098`, result `partial`.

---

### Q2 follow-up — per-line

**Asked:**

Three lines from the diff, against the **reordered** function:

```text
line 1    --- a/planting/schedule.py
line 2    +++ b/planting/schedule.py
line 3    @@ -8,6 +8,7 @@
```

For each of these three, walk the reordered branch chain from the top and tell me the label it
returns. Three answers. Confidence tag.

**Answered:**

```text
1 and 2 and i said they become added
```

---

### Q2 remediation — R1, one expression

**Asked:**

Two expressions. No function, no branch chain. Just tell me what each one evaluates to — `True` or
`False`.

```python
"--- a/planting/schedule.py".startswith("+")
"--- a/planting/schedule.py".startswith("-")
```

Two answers. Confidence tag.

**Answered:**

```text
ok i misread the line, line 1 is removed and line 2 is added
```

Self-corrected before answering the micro-example.

---

### Q2 close — line 3

**Asked:**

Line 3 is still unanswered, and it's the one that decides whether "the metadata becomes added" is
true as a blanket statement.

```text
line 3    @@ -8,6 +8,7 @@
```

Against the reordered function: what label does it return, and why that one? Confidence tag.

**Answered:**

```text
metadata, the prefix is not caught in the added or removed umbrella
```

**Outcome:** correct, with correct reasoning. Remediated.

---

## Q3 — branch_precedence transfer, non-diff domain

**Asked:**

Different domain, no diffs anywhere in it.

```python
def route(path):
    if path.startswith("/admin/health"):
        return "healthcheck"
    elif path.startswith("/admin"):
        return "admin"
    elif path.startswith("/"):
        return "page"
    else:
        return "invalid"
```

Someone moves the `startswith("/")` branch to the **top**, changing nothing else:

```python
def route(path):
    if path.startswith("/"):
        return "page"
    elif path.startswith("/admin/health"):
        return "healthcheck"
    elif path.startswith("/admin"):
        return "admin"
    else:
        return "invalid"
```

Four inputs:

```text
"/admin/health"
"/admin/users"
"/about"
"reports"
```

For each one: what did the original return, what does the reordered version return, and does it
change? Confidence tag.

**Answered:**

```text
. all lines exept for reports become page and reports stays invalid, 80
```

**Outcome:** all four resulting labels correct.

---

### Q3 precision check

**Asked:**

Of these four:

```text
"/admin/health"
"/admin/users"
"/about"
"reports"
```

which ones get a **different** label from the reordered version than the original gave?
Confidence tag.

**Answered:**

```text
i told you the top 3 lines, so admin health admin users and about
90
```

**Outcome:** incorrect. `"/about"` returned `page` in the original too. `EV-P1-BRANCH-098-TRANSFER`,
result `partial`.

---

### Q3 remediation — R3, original function only

**Asked:**

This is the **original** `route`, before any reordering.

What does `route("/about")` return? Confidence tag.

**Answered:**

```text
page, ok i misread again
```

**Outcome:** correct, self-diagnosed. Remediated.

---

## Q4 — Phase 1 gate, nested calls with one branch

**Asked:**

2 calls, one branch. Predict by hand; nothing gets run until you commit.

```python
def bump(n):
    if n > 3:
        return n + 10
    return n + 1


def apply_twice(n):
    return bump(bump(n))


print(apply_twice(3))
```

Two things:

```text
a   what does this print
b   which bump call finishes first, the inner one or the outer one
```

Confidence tag.

**Answered:**

```text
. apply twice runs first it calls bump first inside the brackets and then the outside, inside
returns 4 because it is equal to 3 then it calls bump again with that value so then it is greater
than 3 so it returns 14 and then it prints 14
90
```

**Outcome:** correct in full, unaided. Confirmed by running: `14`. `EV-P1-NEST-099`, result
`correct`. This is the Phase 1 knowledge gate as written in the plan.

---

## Q5 — print vs return

**Asked:**

Predict before anything runs.

```python
def label(n):
    if n > 0:
        print("positive")
    else:
        print("negative")


def describe(n):
    return "answer: " + str(label(n))


print(describe(4))
```

`str(x)` just turns whatever `x` is into text.

What appears on screen, in order, exactly? Confidence tag.

**Answered:**

```text
starts at decsribe runs label it returns positive and then anser: + "positive",40, what does str do
for this problem, also label returns nothing it prints it so it would be positive anser: + idk
```

**Outcome:** first instinct wrong, self-corrected inside the same answer. Actual output:

```text
positive
answer: None
```

`EV-P1-RETURN-100`, result `partial, self-corrected before reveal`.

---
