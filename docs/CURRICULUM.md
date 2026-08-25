# BuildLens — Curriculum Map

## Purpose

This document answers:

> What should I learn, in what order, while BuildLens evolves?

BuildLens is the project. This curriculum is the **knowledge spine** underneath it.

The goal is not to finish a pile of courses. The goal is to repeatedly connect:

```text
concept
→ tiny exercise
→ BuildLens implementation
→ reference-project transfer
→ explanation
→ delayed retrieval
```

The curriculum deliberately moves through different zoom levels:

```text
LINE
↓
FUNCTION
↓
FILE
↓
MODULE
↓
PROCESS
↓
SYSTEM
↓
DEPLOYMENT
↓
TRADEOFF
```

You should eventually be able to move both directions.

## The broader coding-world map

The curriculum must eventually connect application code to the layers underneath and around it.

```text
SOURCE CODE / TYPES
        ↓
DATA REPRESENTATION
bytes, numbers, strings, serialization
        ↓
ALGORITHMS + DATA STRUCTURES
lists, maps, sets, trees, heaps, graphs
        ↓
RUNTIME EXECUTION
calls, stack, heap, interpreter/compiler boundaries
        ↓
OPERATING SYSTEM
processes, threads, files, virtual memory, scheduling
        ↓
NETWORK
sockets, HTTP, latency, partial failure
        ↓
PERSISTENCE
files, databases, indexes, transactions, migrations
        ↓
CONCURRENCY / DISTRIBUTED STATE
locks, optimistic concurrency, retries, idempotency, ordering
        ↓
APPLICATION ARCHITECTURE
modules, APIs, adapters, trust boundaries
        ↓
OPERATIONS
logs, metrics, traces, deployment, recovery
        ↓
QUALITY + TRADEOFFS
performance, reliability, security, modifiability, cost
```

BuildLens does **not** attempt to recreate full CMU 15-213, Berkeley 61B, or Berkeley 162 courses.

Instead it introduces the relevant underlying idea exactly when the project first creates a reason to care about it.

This prevents two failure modes:

```text
framework-only knowledge
"I know FastAPI calls this function but not what a process/socket/file is"

and

detached theory
"I memorized virtual memory but cannot connect it to software I build"
```

---

# Strand 1 — Execute Code in Your Head

## Core ideas

- assignment
- expressions
- conditionals
- loops
- function calls
- parameters / arguments
- local frames
- return values
- recursion
- mutation / aliasing

## Primary sources

- CMU 15-112
- Berkeley CS61A environment diagrams

## BuildLens phases

0–3

## Promotion test

Given unfamiliar small Python:

```text
predict output
→ draw state/call frames
→ run
→ explain mismatch
→ solve changed variant
```

## Transfer

BuildLens helpers → Argos helpers/projections.

---

# Strand 1.5 — Data Representation: Values Become Bytes

## Why this exists

CMU 15-213 starts below ordinary application abstractions: bits, bytes, integers, floating point, machine representation, and the consequences of those representations.

BuildLens does not need a full C/assembly curriculum, but the learner should stop treating Python values and JSON as magical.

## Core ideas

- bit / byte distinction
- integer representation at a conceptual level
- floating-point is finite/inexact
- text encodings such as UTF-8
- Python object vs serialized bytes
- JSON numbers/strings vs domain types
- money/precision: float vs decimal reasoning
- hash input is bytes
- file/network/database boundaries eventually carry encoded representations

## BuildLens phases

2–15, introduced gradually.

## Example exercises

```text
Python str
→ UTF-8 bytes
→ hash

Pydantic/Python object
→ JSON
→ HTTP bytes
→ JSON
→ Python/domain object
```

Ask:

```text
Where did the representation change?
What information/type guarantees were lost?
Where could precision/encoding bugs appear?
```

Use Argos money/yield examples later to connect representation choices to real code.

## Promotion test

The learner can distinguish:

```text
domain value
in-memory Python representation
serialized representation
persistent/network representation
```

and can explain why the distinction matters.

---

# Strand 2 — Data Structures and Algorithmic Shape

## Core ideas

- arrays/lists and linked structures conceptually
- dictionaries / hash tables
- sets
- stacks / queues / deques
- trees / search trees
- heaps / priority queues
- graphs
- lookup vs scan
- ordering
- accumulation
- recursion
- asymptotic complexity
- choosing a representation based on the operations the program needs

## Primary sources

- CMU 15-112
- Berkeley CS61B

## BuildLens phases

2–6

## Promotion test

You must answer:

```text
What operations dominate this code?
What data representation supports them?
What is the rough time/space growth?
What alternative representation would change that?
```

## Transfer

Argos aggregation → Datum reconciliation → unfamiliar domain.

---

# Strand 3 — State, Identity, and Invariants

## Core ideas

- value vs state
- object identity
- mutable ownership
- snapshots
- state machines
- invariants
- authoritative state

## BuildLens phases

3–9

## Promotion test

For any stateful feature:

```text
previous state
+ event
→ transition
→ new state
```

You must identify:
- owner;
- legal transitions;
- impossible states;
- invariant.

## Transfer

BuildLens sessions → Argos job lifecycle → Trellis lease states.

---

# Strand 4 — Testing as Problem Understanding

## Core ideas

- example before implementation
- normal case
- boundary case
- invalid case
- failure case
- regression test
- test smallest abstraction first
- tests as executable contracts

## Primary sources

- CMU 15-112
- Berkeley CS61B testing
- Berkeley CS162 student testing/design review

## BuildLens phases

all phases

## Promotion test

Before seeing Claude's tests:

```text
state the requirement
→ propose tests
→ state which assumption each test attacks
```

A test without a reason does not count.

---

# Strand 5 — Debugging as Evidence

## Core ideas

- observed behavior vs hypothesis
- call stack
- breakpoints
- step into / over / out
- watch variables
- smallest reproducer
- falsifying experiment
- root cause vs symptom

## Primary sources

- Berkeley CS61B debugger material
- Berkeley CS61B debugging guidance

## BuildLens phases

4 onward

## Promotion test

Before changing code:

```text
OBSERVATION
HYPOTHESIS
EVIDENCE NEEDED
SMALLEST EXPERIMENT
RESULT
UPDATED MODEL
```

No random editing.

See `docs/CODE_READING_DEBUGGING_PLAYBOOK.md`.

---

# Strand 6 — Git and Change History

## Core ideas

- working tree
- diff
- commit
- branch
- merge
- merge base
- worktree
- revert vs new correction
- behavioral meaning of a commit

## Primary sources

- Berkeley CS61B Git guide
- Git documentation

## BuildLens phases

4–13

## Promotion test

Given a diff:

```text
what changed?
what behavior should change?
what should remain invariant?
what test proves it?
why was this change needed?
```

Later:
- explain BuildLens worktree isolation;
- explain three-way reconciliation.

---

# Strand 7 — Modules, Interfaces, and Boundaries

## Core ideas

- responsibility
- cohesion
- coupling
- interface / contract
- adapter
- validation boundary
- dependency direction
- domain vs transport

## Primary sources

- Berkeley CS169
- Berkeley CS162 design documents
- CMU software architecture material

## BuildLens phases

4–12

## Promotion test

For every boundary:

```text
what crosses it?
in what representation?
who owns validation?
what must not cross it?
why is this boundary here?
```

## Transfer

BuildLens adapter → Datum barricade → Trellis trust boundary.

---

# Strand 8 — Systems: What Happens Under the Framework

## Why this exists

CMU 15-213 explicitly teaches a programmer's view of how systems execute programs, store information, communicate, perform, and support concurrent computation.

Its published learning objectives also include process/thread control, virtual memory, networking, crashes/security vulnerabilities, compilers, analyzers, debuggers, consistency checkers, profilers, and reliable/efficient programming.

BuildLens should therefore deepen the learner from:

```text
"Python called Git"
```

toward:

```text
"my Python process started a child Git process,
received bytes/status from it,
decoded/interpreted the result,
and handled a non-zero exit"
```

without pretending the learner has completed a systems course.

## Core ideas

### Program representation/execution

- source code vs runtime execution
- interpreter/compiler at an appropriate conceptual level
- call stack vs heap-owned objects conceptually
- exceptions/control transfer

### Operating-system boundary

- process vs thread
- child process
- exit status
- file descriptor / file handle conceptually
- system I/O
- virtual memory/address-space purpose
- resource lifetime

### Memory/performance

- memory hierarchy
- locality
- cache effects conceptually
- allocation
- CPU vs I/O work
- asymptotic complexity is not the whole performance story

### Network

- socket conceptually
- client/server process
- request/response bytes
- latency
- timeout
- connection failure
- partial failure

### Tools

- debugger
- profiler
- linter/static analyzer
- type checker
- consistency checker
- logs/traces as runtime evidence

## Primary sources

- CMU 15-213 / Introduction to Computer Systems
- Berkeley CS162 when operating-system/distributed concepts become relevant

## BuildLens phases

7–15

## Example exercises

### `subprocess`

```text
BuildLens process
   ↓ creates child
git process
   ↓ stdout/stderr + exit status
BuildLens process
```

Questions:

```text
Which process executes Git?
What crosses back into Python?
What does exit code mean?
What if the child hangs?
What resource needs cleanup?
```

### HTTP

```text
browser
→ encoded HTTP request
→ network
→ server process
→ validation
→ domain
→ encoded response
```

Questions:

```text
Where are bytes converted into application objects?
Which failures can occur before domain code executes?
What does timeout mean from each side?
```

### Persistence

```text
Python domain value
→ SQL parameter/serialization
→ database transaction
→ durable state
```

### Collaborative editing

Ask which protection is:
- application logic;
- Git behavior;
- filesystem publication behavior;
- persistent recovery metadata.

## Promotion test

You can explain a feature at both:

```text
APPLICATION LEVEL
and
SYSTEMS LEVEL
```

and clearly label what is verified versus what is only a conceptual model.

---

# Strand 8.5 — Performance, Measurement, and Profiling

## Why this exists

CMU 15-213 explicitly emphasizes that performance is more than asymptotic complexity: constant factors, locality, memory behavior, I/O, and measurement matter.

## Core ideas

- latency vs throughput
- CPU-bound vs I/O-bound
- algorithmic complexity vs constant/system effects
- locality/cache behavior conceptually
- benchmark before optimizing
- representative workload
- profiler
- bottleneck
- p50/p95-style thinking conceptually
- measurement noise / warm-up / environment

## BuildLens phases

6–15

## Promotion test

Before optimizing:

```text
What is slow?
How do we know?
What layer is likely responsible?
What measurement would distinguish hypotheses?
What did the change improve?
What did it make worse?
```

Never accept:

> "This should be faster."

without a mechanism and measurement plan.

---

# Strand 9 — Persistence, Transactions, Concurrency, and Distributed Failure

## Core ideas

### Persistence

- persistent vs in-memory state
- file vs database
- schema
- index purpose
- migration
- authoritative record

### Transactions

- transaction
- atomicity
- isolation conceptually
- commit / rollback
- crash windows

### Concurrency

- shared mutable resource
- race condition
- synchronization
- optimistic concurrency
- lock scope
- lost update
- deadlock conceptually
- independent work should remain concurrent where practical

### Distributed / retry behavior

- timeout does not prove whether remote work happened
- retry
- idempotency
- duplicate delivery
- ordering
- partial failure
- stale state
- replay
- reconciliation
- exactly-once claims require skepticism and precise boundaries

## Primary sources

- CMU 15-213 concurrency/system interactions
- Berkeley CS162 synchronization, transactions, reliability, and distributed systems
- Trellis as a later applied transfer domain

## BuildLens phases

9–15

## Transfer

BuildLens collaborative editing → Datum reconciliation → Trellis idempotency → unfamiliar webhook/payment/job-worker domain.

## Promotion test

For a mutation:

```text
What state can change?
Who owns the authoritative state?
What must commit together?
What if the process dies here?
What if the request times out?
What if the request repeats?
What if another writer acts concurrently?
What evidence distinguishes "failed response" from "failed operation"?
```

---

# Strand 9.5 — Security and Trust Boundaries

## Core ideas

- trusted vs untrusted input
- validation at boundaries
- authentication vs authorization
- least authority
- client claim vs server-owned truth
- secrets/configuration
- injection as untrusted data crossing into an interpreter/query
- information disclosure before authorization
- dependency/supply-chain awareness at a conceptual level

## BuildLens phases

7–15

## Transfer

BuildLens Claude-hook input → Datum barricade → Trellis server authority.

## Promotion test

For every external input:

```text
Who produced this?
Why should I trust it?
What is validated?
Where does it become a domain type?
What decision may it influence?
Could validation happen too late?
```

---

# Strand 9.75 — Operations and Observability

## Why this exists

Production understanding requires more than source code. A system must provide enough evidence to understand what happened after deployment.

## Core ideas

- logs
- metrics
- traces
- correlation/request/run identifiers
- health/readiness conceptually
- deployment/runtime configuration
- failure evidence
- alert signal vs root cause
- recovery/runbook thinking
- "2 AM" operability test

## BuildLens phases

8–15

## Promotion test

For an important failure:

```text
What would the user observe?
What would the logs/metrics/state show?
How would I correlate the failure to one request/session?
What would I inspect first?
Can a developer unfamiliar with the code diagnose it?
```

---

# Strand 10 — Architecture and Quality Attributes

## Core ideas

- requirements
- constraints
- architectural drivers
- quality attributes
- quality scenarios: stimulus → mechanism → measurable response
- module/runtime/data/deployment/failure views
- assumptions
- sensitivity points
- tradeoff points
- risks / non-risks
- ADRs
- evidence
- reversal conditions

## Primary sources

- CMU SEI
- Berkeley CS162 design review

## BuildLens phases

10–15

## Promotion test

Every major decision:

```text
problem
constraints
quality requirement
alternatives
decision
mechanism
cost
failure mode
evidence
reversal condition
```

---

# Strand 11 — Code Reading and Review

## Core ideas

- start from behavior, not folder tree
- follow one call chain
- follow one value
- identify invariants
- distinguish correctness / security / performance / maintainability
- review unfamiliar code

## BuildLens phases

6–15

## Promotion test

Given 50–100 unfamiliar lines:

```text
purpose
inputs
outputs
state
dependencies
behavior
bug/risk
test
design concern
```

Practitioner discussions increasingly describe code-reading/review and debugging interviews because generated code is easy to produce but harder to understand and defend. Treat that as anecdotal industry evidence, not academic authority.

See `docs/CODE_READING_DEBUGGING_PLAYBOOK.md`.

---

# Strand 12 — Explanation and Design Defense

## Core ideas

- one-sentence behavior
- line-level explanation
- mechanism-level explanation
- architecture narrative
- counterargument
- failure explanation
- design review

## BuildLens phases

all phases, increasing difficulty

## Promotion test

Explain the same feature at four depths:

```text
30 seconds — product
2 minutes  — architecture
5 minutes  — runtime/data flow
10 minutes — files/functions/state/failure/tradeoff
```

See `docs/DESIGN_REVIEW_RUBRIC.md`.

---

# Weekly Learning Rhythm

Do not create a second full-time course beside the project.

Use small pauses.

## Every implementation session

```text
5–10 min  cold retrieval
build small patch
10–20 min trace/test/teach
record one learning note
```

## Once per week

```text
architecture reset
one unfamiliar-code review
one design defense
one delayed concept test
```

## Every major phase transition

```text
closed-repo architecture reconstruction
cumulative knowledge gate
one reference-project transfer
one "what changed in my mental model?" reflection
```

---

# Promotion Philosophy

Time does not advance the curriculum.

Competence does.

A concept moves from:

```text
NEW
→ RECOGNIZE
→ TRACE
→ EXPLAIN
→ TRANSFER
→ DEFEND
→ MASTERED
```

"Mastered" means:
- multiple unseen variants;
- multiple contexts;
- delayed retrieval;
- correct explanation;
- ability to recognize when the concept does *not* apply.

---

# Final Curriculum Outcome

You should eventually be able to receive an unfamiliar software feature and ask, in order:

```text
What behavior is required?
What data enters, and in what representation?
What algorithm/data structure fits the operations?
What code executes?
What process/thread owns that execution?
What state changes?
What is authoritative?
What crosses trust/process/network boundaries?
What can fail or race?
How is it tested?
What runtime evidence would prove what happened?
What is the performance mechanism and measurement?
What happens underneath the framework?
What security assumptions exist?
What design alternatives exist?
Why was this choice reasonable under these constraints?
What downside did I knowingly accept?
What evidence supports the decision?
What would have to become true for me to redesign it?
```

That is the mental framework BuildLens is intended to make automatic.
