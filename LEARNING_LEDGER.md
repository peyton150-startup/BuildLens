# BuildLens — Learning Ledger

## Purpose

CMU's learning principles emphasize that prior knowledge and how knowledge is organized affect later learning. Retrieval practice is most useful when it exposes what can actually be recalled and transferred.

This file tracks **mental-model quality**, not project completion.

Do not log every fact.

Log concepts that matter.

---

# Concept Entry Template

## Concept

`<name>`

### My explanation

Write from memory before checking documentation.

### Mental picture

```text
draw / ASCII map
```

### Example I can solve

`<example>`

### Transfer example

`<different context>`

### Common mistake / misconception

`<what I previously misunderstood>`

### Evidence I understand it

- [ ] unseen variant
- [ ] second context
- [ ] delayed retrieval
- [ ] teach aloud
- [ ] used in real BuildLens code
- [ ] defended under questioning

### Confidence before check

`0–100%`

### Actual result

`correct / partial / wrong`

### Calibration note

Was confidence too high, too low, or appropriate?

### Next retrieval due

`<phase/date>`

---

# Formal Exercise Evidence Record

Every formal tracing, transfer, debugging, test-design, teach-back, and oral-defense exercise creates an Evidence Record.

The learner's original answer is historical evidence and is never cleaned up or replaced by the correction.

## Required record

```text
EVIDENCE ID:
<stable id>

DATE / PHASE / GATE:
...

IMPLEMENTATION TRIGGER:
<real BuildLens task that made this concept relevant>

ADJACENT CONCEPT:
...

EXERCISE TYPE:
<tracing | transfer | debugging | test design | teach-back | oral defense>

SOURCE / CONTEXT:
<academic | BuildLens | Argos | Datum | Trellis | blind transfer>

PROBLEM — VERBATIM:
<exact prompt>

MY ANSWER — VERBATIM:
<exact first committed answer>

MY REASONING — VERBATIM:
<exact reasoning or "not provided">

CONFIDENCE BEFORE CHECK:
<0–100% or not provided>

TOOLS / HELP USED BEFORE COMMITMENT:
<none | interpreter | debugger | docs | Claude | Codex | other>

RESULT:
<correct | partial | wrong>

MISCONCEPTION / GAP:
...

CORRECT MODEL — ADDED AFTER ATTEMPT:
...

WHY THIS MATTERS TO THE REAL IMPLEMENTATION:
...

TRANSFER / NEXT RETRIEVAL:
...
```

Rules:

1. Preserve the exact problem and first committed answer.
2. Preserve every later attempt separately.
3. Never reconstruct a missing verbatim answer from memory; write `VERBATIM ANSWER UNAVAILABLE`.
4. Gate completion references Evidence IDs.
5. A bare checklist checkmark is not evidence; point it to a record.

Example:

```text
- [x] unseen variant — EV-P1-STR-003
- [x] second context — EV-P3-ALIAS-002
- [ ] delayed retrieval
```

---

# Remediation Chain

When an Evidence Record is `wrong` or `partial`, link the follow-up attempts instead of treating them as unrelated questions.

Add these fields to every remediation Evidence Record:

```text
PARENT EVIDENCE ID:
<failed attempt that triggered this remediation>

PRIMARY BLOCKER:
<SYNTAX_READING | EXECUTION_ORDER | ...>

SCAFFOLD RUNG:
<R0 | R1 | R2 | R3 | R4 | R5 | R6>

WHY THIS RUNG:
<what complexity was removed and why>

SUPPORT PROVIDED BEFORE THIS ATTEMPT:
<none | syntax explanation | state table | guiding question | worked example | partial example>

RECOVERY STATUS:
<descending | stable-at-rung | climbing | target-restored>
```

## Example chain

```text
EV-P1-014
target-level function trace
RESULT: wrong
PRIMARY BLOCKER: STRING_INDEXING
SCAFFOLD RUNG: R5

        ↓

EV-P1-015
`word = "Hi"` → `word[-1]`
SCAFFOLD RUNG: R0
RESULT: correct
RECOVERY STATUS: stable-at-rung

        ↓

EV-P1-016
fresh string-indexing micro-variant
R0
RESULT: correct

        ↓

EV-P1-017
one simple branch using a string prefix
R3
RESULT: correct

        ↓

...

        ↓

EV-P1-021
fresh target-level classifier trace
R5
RESULT: correct
RECOVERY STATUS: target-restored
```

The chain makes progress visible without deleting the original mistake.

## Attempt-count interpretation

A long remediation chain is not a negative score.

It is useful evidence showing:

```text
initial mental model
→ exact blocker
→ scaffolding needed
→ recovery path
→ later independence
```

Do not summarize multiple wrong answers into one cleaned-up record.

Each committed attempt keeps its own verbatim problem and answer.

---

# Status Vocabulary

Use:

```text
NEW
RECOGNIZE
TRACE
EXPLAIN
TRANSFER
DEFEND
MASTERED
```

Do not mark `MASTERED` because a concept feels familiar.

---

# Weekly Reflection

## 1. What can I now explain that I could not last week?

## 2. What did I think I understood but fail to retrieve?

## 3. Which architecture box/arrow did I forget during reconstruction?

## 4. Which debugging hypothesis was wrong, and why?

## 5. What design decision can I now defend with alternatives and tradeoffs?

## 6. Which concept needs a different-looking transfer problem?

## 7. What should Claude give me *less* help with next week?

---

# Calibration Rule

Before running code or revealing an answer, record confidence:

```text
Prediction: X
Confidence: 80%
```

Then compare.

The purpose is to learn the difference between:

```text
"I recognize this"
and
"I can actually predict/explain this"
```

A confidently wrong answer is especially useful study material.

---

# Architecture Reconstruction Log

Once per week:

```text
VIEW:
module / runtime / data / deployment / failure

REMEMBERED:
...

MISSING:
...

WRONG CONNECTION:
...

WHY I MISSED IT:
...

NEXT EXERCISE:
...
```

Do not merely redraw the missing arrow afterward.

Create a retrieval/transfer exercise around it.


# Decision Defense Entry

For every major architectural choice, occasionally retrieve this **without opening the ADR**:

```text
DECISION:
...

CONSTRAINT THAT MATTERED:
...

QUALITY I OPTIMIZED FOR:
...

CREDIBLE ALTERNATIVE:
...

WHY MY CHOICE WORKS — MECHANISM:
...

DOWNSIDE I ACCEPTED:
...

EVIDENCE I HAVE:
...

EVIDENCE I DO NOT HAVE YET:
...

WHAT WOULD HAVE TO BE TRUE TO REVERSE IT:
...

45-SECOND SPOKEN ANSWER:
...
```

Then have Claude challenge the answer using the five-round defense in `docs/DESIGN_REVIEW_RUBRIC.md`.

# Systems Connection Entry

When a new boundary appears, record one connection:

```text
APPLICATION CONCEPT:
e.g. subprocess.run

UNDERLYING SYSTEM CONCEPT:
child process + stdout/stderr + exit status

FAILURE I CAN NOW EXPLAIN:
non-zero exit / timeout / unavailable executable

WHAT I STILL DO NOT UNDERSTAND:
...
```

The goal is gradual depth, not pretending every abstraction has been mastered.
