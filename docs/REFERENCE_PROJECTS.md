# BuildLens — Reference Projects for Evolving Exercises

## Purpose

BuildLens should evolve from small synthetic Python exercises into transfer exercises based on real systems.

This file tells Claude where to look and which concepts each repository is suited to teach.

The repositories are **practice domains**, not answer banks.

Before producing an exercise, Claude must:
1. identify the current BuildLens lifecycle phase;
2. identify one learning objective;
3. inspect a current relevant source file when GitHub access is available;
4. simplify away unrelated complexity;
5. generate a related but non-identical exercise;
6. test the same idea in a second context.

---

# Curriculum order

```text
CMU / Berkeley micro-exercise
        ↓
current BuildLens implementation
        ↓
Argos
        ↓
Datum
        ↓
Trellis
        ↓
unfamiliar transfer project
```

This is a **difficulty order**, not a ranking of project quality.

---

# 1. Argos Control Tower

Repository:
`peyton150-startup/Argos_Control_Tower`

Verified during plan refinement at:
`65b560b0fad3a434520ba431ccb04bbcd1feba06`

## Why Argos comes first

Argos's central behavior is deterministic event projection.

Its main path is easy to draw:

```text
events
  ↓
sort
  ↓
per-job accumulator
  ↓
JobState
  ↓
overview / quality / attention
```

This makes it suitable for moving from small Python tracing into real application code.

## Primary source

`backend/app/projection.py`

Verified concepts in the current code include:

- trusted events are sorted by `(timestamp, ingestion_index)`;
- creation events establish job accumulators;
- lifecycle events update started/completed/blocked state;
- pre-creation events remain timeline evidence but do not mutate lifecycle state;
- completion clears active block state;
- quality counts pass/fail inspection events and defect codes;
- overview aggregates quantities, yield, overdue state, blocking, and priced work at risk.

## Exercise families

### Basic Python transfer

Source idea:
`_optional_string`, `_parse_quantity`, `_parse_price`

Generate a new helper using a different domain.

Test:
- type checking;
- `None`;
- invalid value;
- return type;
- side-effect/error list.

### Loop + accumulator

Source idea:
`_build_quality`

Do not use the literal defect dataset.

Generate:
- test-result categories;
- package scan results;
- sensor status;
- support-ticket categories.

Learner must trace the dictionary accumulator.

### State transition

Source idea:
`project_factory_state`

Generate a new sequence:

```text
created
started
blocked
unblocked
completed
```

Change timestamps/order/metadata.

Ask for final state and evidence.

### Aggregation

Source idea:
`_build_overview`

Generate different totals and missing values.

Ask:
- what is included;
- what is excluded;
- when `None` should survive instead of becoming zero;
- which denominator is authoritative.

### Architecture

Ask why projection owns manufacturing rules rather than API/UI.

Then use a non-manufacturing transfer domain and ask the same question.

---

# 2. Datum

Repository:
`peyton150-startup/Datum-Project`

Verified during plan refinement at:
`3d1d73736bbe149c22b3e88f6a8e3315db1d71e3`

## Why Datum comes after Argos

Datum adds multiple representations of truth and explicit reconciliation.

The README describes declared state from Git and discovered state from provider APIs as intentionally separate planes, with their differences promoted into first-class discrepancies.

## Primary source

`datum/reconcile/diff.py`

Current code provides a clean progression:

```text
matched pair
   ↓
union(attribute keys)
   ↓
PlaneValue on each side
   ↓
compare
   ↓
FieldDiscrepancy
```

and:

```text
declared orphan → DECLARED_MISSING
discovered orphan → DISCOVERED_UNDECLARED
```

Output is deterministic through sorting.

## Exercise families

### Sets/dictionaries

Generate two mappings with partially overlapping keys.

Ask the learner to:
- compute the union;
- predict ordered iteration;
- distinguish absent from explicit null;
- produce discrepancies.

### Domain representation

Give a loose dictionary representation and ask when/why to introduce a typed object.

Compare:
```text
dict
vs
domain value object
```

### Trust boundary

Use a different external system.

Ask:
- where raw input ends;
- where typed/validated data begins;
- what code may assume after crossing the boundary.

### Reconciliation architecture

Transfer domain examples:
- desired vs installed packages;
- expected vs observed feature flags;
- declared vs deployed cloud settings;
- scheduled vs actual machine configuration.

Ask why the two sides should not silently overwrite one another.

### ADR defense

Select one real Datum-style decision pattern and generate an analogous decision.

Require:
```text
context
options
decision
consequence
reversal cost
```

---

# 3. Trellis AI Chatbot Task Manager

Repository:
`peyton150-startup/Trellis_AI_Chatbot_Task_Manager`

Verified during plan refinement at:
`11cf50bc5882b71062b65e83f436b2e9317354b1`

## Why Trellis comes late

Trellis's important concepts require prior understanding of:

- state;
- persistence;
- trust boundaries;
- transactions;
- failure paths;
- concurrency.

Its README defines the core thesis:

```text
model proposes
deterministic code decides
PostgreSQL records truth
```

## Primary source

`backend/app/idempotency.py`

Representative lease state reasoning:

```text
new key
→ EXECUTE

same key + same arguments + completed
→ REPLAY

same key + different arguments
→ CONFLICT

failed
→ guarded reacquire

pending
→ bounded resolution/wait
```

The module also intentionally requires lease completion to participate in the same transaction as the domain mutation and audit evidence.

## Exercise families

### Finite-state reasoning

Use a simplified state machine first.

Then increase difficulty until the learner can predict:
- execute;
- replay;
- conflict;
- wait/fail.

### Idempotency

Transfer domains:
- payment request;
- webhook;
- background job;
- inventory reservation;
- manufacturing command.

Never let "AI agent" become the memorized cue for idempotency.

### Transaction boundary

Present:
```text
business mutation
audit event
idempotency completion
```

Ask what happens when each commits separately.

Then ask the learner to design the transaction boundary.

### Authorization vs UI state

Generate a different client/server system.

Ask:
- what the client may claim;
- what the server must verify;
- what is authoritative;
- which check must happen before data is revealed.

### Concurrency

Only after the relevant curriculum phase.

Ask the learner to identify the race in:
```text
SELECT
decide
unguarded UPDATE
```

Then compare with guarded/atomic mutation.

---

# 4. Unfamiliar / adjacent repositories

After Phase 10, Claude may choose another repository only when it adds a concept not already overrepresented.

Selection criteria:

- Python or an adjacent stack the learner can reasonably read;
- relevant to backend/data/agent/reliability work;
- source code small enough to isolate one behavior;
- license/public access compatible with inspection;
- no need to understand an enormous framework before the target concept.

Good exercise targets:
- deterministic transformation;
- parser;
- state machine;
- queue worker;
- API boundary;
- retry behavior;
- cache invalidation;
- transaction;
- reconciliation.

Do not choose a repository merely because it is popular.

---

# Freshness

Before using a reference project, prefer current default-branch code.

Record:

```text
repo
commit
file
concept
academic source
generated exercise ID
```

The exercise itself must remain understandable even if the source project evolves later.
