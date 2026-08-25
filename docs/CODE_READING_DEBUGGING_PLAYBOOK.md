# BuildLens — Code Reading & Debugging Playbook

## Purpose

Use this whenever you open:
- a file Claude just changed;
- a failing test;
- an unfamiliar repository;
- interview code.

The goal is to avoid passive rereading.

---

# Part A — Reading One File

## 1. Start with the contract

Before line-by-line reading, answer:

```text
Why does this file exist?
What enters it?
What leaves it?
Who calls it?
What does it call?
What state can it change?
```

## 2. Write a one-sentence behavior description

Berkeley CS61A explicitly asks students to describe a process in plain English rather than merely read the code.

Bad:

> "This loops over events."

Better:

> "This converts an ordered event sequence into the latest job lifecycle state."

## 3. Mark dependencies

For every import/dependency:

```text
WHAT do we use from it?
WHY is it needed?
IS it domain logic, infrastructure, framework, or standard library?
```

## 4. Follow one representative path

Pick one normal input.

Trace:

```text
input
→ branch
→ function call
→ state mutation
→ return
```

## 5. Follow one edge path

Pick:
- empty;
- invalid;
- missing;
- boundary;
- failure.

Predict before running.

---

# Part B — Reading Across Files

Do not browse folders randomly.

Start from one behavior.

```text
ENTRYPOINT
↓
CALLER
↓
DOMAIN OPERATION
↓
PERSISTENCE / EXTERNAL BOUNDARY
↓
RETURN / RENDER
```

For every arrow record:

```text
file
function
input type
output type
state affected
```

Then close the code and redraw the chain.

---

# Part C — Follow One Value

Choose one important value.

Examples:

```text
BuildLens: lines_added
Argos: good_quantity
Datum: natural_key
Trellis: tool_call_id
```

Follow it from origin to final use.

Ask:

```text
Where is it created?
Where is it transformed?
Where is it validated?
Where is it persisted?
Where could it become stale/wrong?
What representation crosses each boundary?
```

---

# Part D — Debugging Protocol

Berkeley CS61B's debugging material emphasizes the debugger's call stack, variable inspection, breakpoints, step-in/over/out, and small inputs. Its help guidance asks students to state what is failing and what they already learned rather than asking someone else to debug blindly.

Use:

```text
1. OBSERVATION
2. EXPECTED BEHAVIOR
3. SMALLEST REPRODUCTION
4. LIKELY LAYER
5. HYPOTHESIS
6. FALSIFYING EXPERIMENT
7. RESULT
8. UPDATED HYPOTHESIS
9. ROOT CAUSE
10. REGRESSION TEST
```

Never begin with:

> "I'll change this and see."

---

# Part E — Debugger Questions

When paused at a breakpoint:

```text
Which function/frame am I in?
Who called it?
What are the important local values?
Which value first differs from my prediction?
What line produced that value?
Should I step into, over, or out?
```

Use:
- Step Into when the called function may contain the cause.
- Step Over when its contract is already trusted.
- Step Out when the current function is not the useful level.
- Watch expressions for important state/invariants.

---

# Part F — Rubber-Duck / Teach-Aloud Mode

Practitioner discussions repeatedly report discovering bugs while explaining code aloud. This is anecdotal, but it complements CMU retrieval/peer-teaching ideas.

Teach without saying vague phrases like:

> "Basically it handles stuff."

Explain:

```text
dependency
→ input
→ call
→ branch
→ state
→ returned value
→ assumption
```

If you cannot explain a line's *role* in the behavior, mark it as a knowledge gap.

---

# Part F.5 — Under-the-Framework Lens

When the code crosses an abstraction boundary, add one systems question.

Examples:

```text
subprocess
→ what process starts and what bytes/status return?

HTTP
→ what representation crosses the network?

database
→ what transaction/persistent state exists?

thread/task
→ what mutable resource can be shared?

file
→ what does write/replace mean if the process crashes?
```

Do not derail every code review into operating-systems theory.

Ask only the systems question that helps explain the code's behavior or failure mode.

---

# Part F.75 — Trust / Security Lens

For external data or consequential actions ask:

```text
Who supplied this?
What is trusted?
What is merely claimed?
Where is validation?
Where is authorization?
Could data be exposed before authorization?
Does untrusted input reach SQL/shell/template/interpreter boundaries?
```

---

# Part G — Code Review Lens

For unfamiliar code, review in this order:

```text
1. correctness
2. data/state authority
3. failure / concurrency behavior
4. security / trust boundary
5. tests
6. performance / measurement
7. operability / runtime evidence
8. maintainability / complexity
```

Do not begin with naming/style while a correctness bug is still unexplained.

---

# Part H — End-of-Review Output

After reading/debugging, produce:

```text
BEHAVIOR:
one sentence

EXECUTION PATH:
A → B → C

ROOT STATE:
what owns truth

IMPORTANT INVARIANT:
one sentence

FAILURE:
most important unhappy path

TEST:
one regression/edge test

DESIGN QUESTION:
one thing you would challenge

CONFIDENCE:
0–100%

UNKNOWN:
what you still cannot explain
```

Your confidence should be compared with actual results later. BuildLens can use this to train calibration rather than only correctness.
