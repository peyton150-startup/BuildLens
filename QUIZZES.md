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

## Q6 — exit status vs output (shell, not Python)

**Asked:**

Nothing to do with Python here — this is a shell transcript. `echo $?` prints the exit status of
the command that just finished.

There's a file `fruits.txt` containing exactly two lines:

```text
apple
banana
```

Here is the session. Two commands run, and I've blanked what `echo $?` printed each time:

```bash
$ grep "apple" fruits.txt
apple
$ echo $?
A

$ grep "cherry" fruits.txt
$ echo $?
B
```

Tell me what number `A` is and what number `B` is.

Then one more thing: a teammate wires up CI so that a build step counts as **passing** if the
command printed any output at all. Give me one concrete case where that rule reports the wrong
result. Confidence tag.

**Answered:**

```text
apple
cherry, 20
```

---

### Q6 remediation 1 — syntax-only help on `$?`

**Asked:** after explaining that `$?` holds one number, the exit status, 0 for success and
non-zero for failure — what number is `A`, what number is `B`?

**Answered:**

```text
1 and 1, my thinking is that there is something there so it is 1 and nothing would be 0, 30
```

---

### Q6 remediation 2 — the truthiness collision named, `A` alone

**Asked:** after naming the collision (1 is truthy in Python; 0 is success in exit statuses,
because the status answers "how many problems", not "did you find something") — just `A`.

**Answered:**

```text
1, 40
```

---

### Q6 remediation 3 — real transcript shown

Ran it. `A` is 0, `B` is 1.

**Learner then asked:**

```text
so does that mean apple was inside of fruits.txt and cherry was not?
```

Correct model of grep. Confirmed.

---

### Q6 — CI half

**Asked:** in your own words, name one concrete way the "passing if it printed any output" rule
reports the wrong answer. Confidence tag.

**Answered:**

```text
. isn't pruning 1 still an output, there has to be another usecase i am missing, 30
```

**Outcome:** conflated the status with the command's output — the `1` was printed by `echo`, not
by grep. Worked-example rescue used: a build log printing four lines including `ERROR` and exiting
2. `EV-P1-EXIT-101`, result `wrong, remediated to partial`. **This retrieval does not count** —
the learner saw the answer rather than producing it. Re-run from the worked example.

---

# Session 3 — 2026-08-28

Fundamentals review continuation. Scope limited to completed Phases 0–2.

---

## Q1 — `= +1` versus `+= 1`

**Asked:**

Start with:

```python
count = 5
count = +1
```

versus:

```python
count = 5
count += 1
```

For each version:

1. What is the final value of `count`?
2. What does the second line do?
3. Are `= +` and `+=` the same operator or different forms?
4. Confidence: 0–100.

**Answered:**

```text
in the first one it is 1 and the second one it is 6, 100
```

**Outcome:** both values correct; operator-mechanism explanation still due.
`EV-P1-ACCUMULATOR-155`.

---

### Q1 follow-up — mechanism teach-back

**Answered:**

```text
\= +1 is poitive one and += is add ont to the number
90, skip this one i am looking for harder questions
```

**Outcome:** correct at confidence 90. Micro-scaffolding ended at learner request; next question
returns to target-level composition. `EV-P1-ACCUMULATOR-156`.

---

## Q2 — two-call loop accumulator

**Asked:**

```python
def change_score(labels):
    score = 0

    for label in labels:
        if label == "added":
            score += 2
        elif label == "removed":
            score += 1

    return score


first = change_score(["added", "context", "removed"])
second = change_score(["removed", "added", "added"])

print(first + second)
```

Track both calls, give `first`, `second`, and the printed result, explain why the second call starts
with a new local `score = 0`, and give confidence.

**Answered:**

```text
first is called then we start the loop, it goes added so plus 2 then context so nothing happens and then removed so 2 + 1 first = 3, then second removed so +1 then added 1+2 then added 3+2 so second = 5  and finally it rints first +second which is 3+5 which is 8 
90
```

**Outcome:** computation fully correct; local-state explanation omitted. `EV-P1-ACCUMULATOR-157`.

---

### Q2 follow-up — why the accumulator resets

**Answered:**

```text
the score =0 happens everytime you call  change score before the loop
90
```

**Outcome:** correct. Each call executes the local initialization before its loop.
`EV-P1-LOCAL-158`.

---

## Q3 — external dictionary state across calls

**Asked:** a two-call `count_added` trace using external dictionary
`totals = {"added": 0}`, including final values, purity, and how to make calls independent.

**Learner asked before attempting:**

```text
what does that mean "added" : 0 is that an annotation like with :int for the dataclass
```

The target problem was paused for syntax-only dictionary help.

### Q3 syntax remediation 1 — dictionary lookup

**Asked:**

```python
fruit_counts = {"apples": 2}
print(fruit_counts["apples"])
```

What does `fruit_counts["apples"]` retrieve, and what is printed? Confidence: 0–100.

**Answered:**

```text
it should print 2 because that is the value, it retireves "apples" but the vlaue of apples was set to 2, 90
```

**Outcome:** output/value association correct; key versus retrieved value wording remains.
`EV-P1-DICT-159`.

---

### Q3 syntax remediation 2 — fresh lookup

**Asked:**

```python
settings = {"retries": 3}
value = settings["retries"]
```

What value is assigned to `value`? Identify the key and retrieved value separately. Confidence:
0–100.

**Answered:**

```text
value is assinged 3, it looks up "retries" and the value stored under that key is 3, 100
```

**Outcome:** correct. `EV-P1-DICT-160`.

---

### Q3 syntax remediation 3 — dictionary entry update

**Asked:**

```python
totals = {"added": 0}
totals["added"] += 1
```

What value is stored under `"added"`, and is the dictionary mutated or replaced? Confidence:
0–100.

**Answered:**

```text
time to guess, so the value looked up by "added" is 0 so then we take 0 and += 1 so the value under added becomes 1, 2. i have no idea, 40
```

**Outcome:** value update correct; mutation identity unknown. `EV-P1-DICT-161`.

---

### Q3 syntax remediation 4 — dictionary alias mutation

**Asked:**

```python
totals = {"added": 0}
alias = totals
totals["added"] += 1
```

What does `alias["added"]` retrieve, and why can the alias observe the update? Confidence: 0–100.

**Answered:**

```text
alias is still 0, so it createss a new object, 2. i have no idea 40
```

**Outcome:** wrong; dictionary entry update was modeled as creating a new object.
`EV-P1-DICT-162`.

---

### Q3 syntax remediation 5 — familiar list alias

**Asked:**

```python
numbers = [0]
alias = numbers
numbers[0] = 1
```

What does `alias[0]` retrieve, and was the list replaced or mutated? Confidence: 0–100.

**Answered:**

```text
i just do not understand the rules of apples : 3 and how it applies to the other conecpts we have gone over, alias[0] =1, it mutated the shared list, 90
```

**Outcome:** list alias mutation correct; learner explicitly requested the conceptual bridge to
dictionary mapping. `EV-P1-ALIAS-163`.

---

### Q3 syntax remediation 6 — indexed list mutation through alias

**Asked:**

```python
numbers = [3]
alias = numbers
numbers[0] = 4
```

What does `alias[0]` retrieve, and why? Confidence: 0–100.

**Answered:**

```text
alias would still have 3 becasue it only threw away the 3 in the list for numbers, 30
```

**Outcome:** wrong; alias was modeled as a separate copied list. `EV-P1-ALIAS-164`.

---

### Q3 syntax remediation 7 — alias object count

**Asked:**

```python
numbers = [3]
alias = numbers
```

Does this create one shared list or two separate lists? Explain and give confidence.

**Answered:**

```text
one list, both pointing at the same list
100
```

**Outcome:** correct. `EV-P1-ALIAS-165`.

---

### Q3 syntax remediation 8 — dictionary state movie

**Learner observation before the question:**

```text
for some reason adding the one extra step throws me off
```

**Asked:** track object count and names after each line:

```python
counts = {"apples": 3}
alias = counts
```

**Answered:**

```text
line 1 counts is a list with apples as a key and 3 as the lookup value, then alias is created pointing at the same list
90
```

**Outcome:** one-object/two-name state model correct; container should be called a dictionary, not
a list. `EV-P1-DICT-166`.

---

### Q3 syntax remediation 9 — dictionary mutation state

**Asked:**

```python
counts = {"apples": 3}
alias = counts
counts["apples"] = 4
```

Track object count, both lookups, and whether names moved or the shared object changed.

**Answered:**

```text
1 list exssts, count apples and count alias both point at the same lsit, so now apples is 4 for the lookup value for both objects
90
```

**Outcome:** shared dictionary state correct; terminology not drilled. `EV-P1-DICT-167`.

---

### Q3 syntax remediation 10 — composed shared counter

**Asked:**

```python
shared = {"hits": 0}
first = shared
second = shared
first["hits"] += 2
second["hits"] += 3
```

Track object count, all three lookups, and why the second update sees the first update.

**Answered:**

```text
so all of them point at the same list, hits starts at zero and then first adds 2 and then second adds 3 so they all retireve 5, 90
```

**Outcome:** correct shared-state composition; container terminology not drilled.
`EV-P1-DICT-168`.

---

## Q4 — external-state leakage across function calls

**Asked:**

```python
stats = {"errors": 0}

def count_errors(events):
    for event in events:
        if event == "error":
            stats["errors"] += 1
    return stats["errors"]

first = count_errors(["error", "ok"])
second = count_errors(["error", "error"])
print(first, second)
```

Track both calls, output, state leakage, purity, and a design repair.

**Answered:**

```text
first is 1 and second is 3, this is a cool conecpt you can make the key you are counting very obious so then the key and the lookup value are simple and convientent, it prints 4, the stats error : 0 is at the top of the file instead of before the loop in the function so it only is set to 0 at the start of the file call, that is a good question and i have no idea for number 4, i think it would mutate every object in the list but i am not sure. put the errors : 0  under def count errors and befroe the loop
90
```

**Outcome:** cross-call state and repair direction correct; output and purity partial.
`EV-P1-EXTERNAL-169`.

**Learner grading instruction:** disregard the `print(first, second)` slip as "just blind." No
output remediation; purity remains.

---

### Q4 purity judgment

**Answered:**

```text
ok then it is pure, it returns a number and does not mutate any of the lsits, the result is a count of a certian criteria of the inputs so the input is directly responsible for the result output, 90
```

**Outcome:** wrong; input mutation was checked, but external counter mutation was missed.
`EV-P1-PURITY-170`.

### Q4 purity contrast follow-up

**Asked:** why is the external-counter version impure, and why is a version with a fresh local
counter pure?

**Answered:**

```text
becasue it changes the counter outside the function, the count is created inside the function adn so it does not affecct anything outside the function, 90, can you push i need to move locations
```

**Outcome:** correct at confidence 90. `EV-P1-PURITY-171`.

---
