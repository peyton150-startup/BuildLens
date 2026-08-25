# BuildLens — Learning-Driven Implementation Plan

## 1. End Game

BuildLens is a local learning/control-tower for AI-assisted software development.

Its purpose is not merely to show what Claude Code changed. It is designed to prevent the developer from progressing faster than their understanding.

At the end of the project, BuildLens should let a developer:

1. observe meaningful Claude Code changes in near real time;
2. inspect the relevant diff without immediately receiving an explanation;
3. predict what the code will do;
4. trace important values and state transitions;
5. draw or reconstruct the execution/data flow;
6. complete a source-grounded knowledge gate generated from an exercise archetype;
7. explain the changed code aloud or in writing;
8. connect the patch to the system architecture;
9. record and defend important design decisions;
10. review the same ideas later through different-looking transfer exercises;
11. enter an interview mode where Claude attacks the implementation, failure modes, and design decisions.

The final skill is:

> Move fluently from product behavior → architecture → module → function → state/data → failure → tradeoff, and defend why the system is designed that way.

BuildLens must therefore optimize for **comprehension before throughput**.

---


# Supporting Learning Documents

The implementation plan controls **what gets built and when**. These supporting documents control how the learner develops deeper software-engineering understanding while building it:

```text
docs/CURRICULUM.md
→ the full knowledge sequence from Python execution to systems/architecture

docs/CODE_READING_DEBUGGING_PLAYBOOK.md
→ the procedure for reading unfamiliar code and debugging from evidence

docs/DESIGN_REVIEW_RUBRIC.md
→ oral-defense standards and review scoring

learning/LEARNING_LEDGER.md
→ misconceptions, confidence calibration, transfer, and delayed retrieval
```

Claude must use these documents rather than inventing a new teaching process each session.

The curriculum includes a later **systems-depth strand** based on CMU 15-213 so the learner does not stop at framework-level knowledge. When the project reaches subprocesses, HTTP, persistence, and concurrency, Claude should add small questions about what the operating system/process/network/database is doing underneath the Python abstraction.

The broader curriculum must eventually touch, in project-relevant increments:

```text
representation / bytes
data structures / algorithms
runtime execution
processes / threads / virtual memory
files / I/O
networking
performance / caches / profiling
databases / transactions / migrations
concurrency / distributed failure
security / trust boundaries
operations / observability
architecture / quality attributes
technical communication / defense
```

This is a map, not permission to front-load all of these topics into early phases.


# 2. Final Technical Shape

The final architecture is a target, not the starting architecture.

```text
                    CLAUDE CODE DESKTOP / CLI
                              |
                              | lifecycle/tool events
                              v
                   .claude/settings.json hooks
                              |
                              v
                     Hook Relay / Adapter
                     (small Python process)
                              |
                              | normalized HTTP event
                              v
+----------------------------------------------------------------+
|                      BUILDLENS PYTHON CORE                       |
|                                                                 |
|  Event Normalizer                                               |
|         |                                                       |
|         v                                                       |
|  Change Capture / Git Inspector                                 |
|         |                                                       |
|         +--------------------+                                  |
|         |                    |                                  |
|         v                    v                                  |
|  Session Service       Learning Gate Service                    |
|         |                    |                                  |
|         |                    +--> Exercise Archetypes            |
|         |                    +--> Attempt Evaluation              |
|         |                    +--> Mastery Model                   |
|         |                                                       |
|         +--------------------+----------------------------------+
|                              |                                  |
|                              v                                  |
|                     SQLite Persistence                           |
|                sessions / changes / attempts /                  |
|                mastery / decisions / diagrams                   |
+------------------------------+----------------------------------+
                               |
                               | API + one-way live stream
                               v
+----------------------------------------------------------------+
|                         BUILDLENS UI                             |
|                                                                 |
|  Change Timeline     Diff Viewer       Knowledge Gate            |
|  Execution Map       State Movie       Mastery                   |
|  Architecture Map    Decision Ledger   Interview Mode            |
+----------------------------------------------------------------+
```

### Intended final technologies

| Concern | Intended final choice | Why it fits BuildLens |
|---|---|---|
| Core/domain | Python | The curriculum centers on Python execution and makes the important logic directly learnable. |
| API/local service | FastAPI | Creates a clear HTTP/application boundary after the Python core is understood. |
| Models/contracts | Pydantic/dataclasses | Makes input/output contracts explicit. |
| Local persistence | SQLite | BuildLens owns local transactional learning/session state and does not need a database server. |
| Git inspection / isolation | `git` subprocess + Git worktrees | Makes change provenance visible and physically separates learner and Claude writes before reconciliation. |
| Claude integration | Claude Code hooks | Provides lifecycle/tool events without modifying Claude Code itself. |
| Live UI updates | SSE (or equivalent) for events + explicit HTTP save/reconcile commands | Live observation is mostly server → UI, while manual edits use explicit version-checked write commands rather than hidden shared-file mutation. |
| UI | small React/TypeScript frontend with code editor/diff/merge panes | Added late; lets the learner inspect and edit code while keeping reconciliation logic in the backend. |

Do not add a technology simply because it belongs in the final architecture. Each technology must be earned by a problem encountered in an earlier phase.

## Non-negotiable collaborative-editing invariant

The final BuildLens product is not read-only.

### The behavior must be obvious to the learner

At all times during a Claude coding session, BuildLens must make these three lanes visually distinct:

```text
CLAUDE LANE
exact diff Claude has produced
+ additions
- removals

HUMAN LANE
the learner's own unsaved/saved edits
shown separately from Claude's diff

INTEGRATION LANE
the candidate combined result
or an explicit conflict
```

The learner must never have to guess which actor produced a change.

If the learner and Claude modify the same line or an overlapping merge hunk:

```text
Claude edits
     +
Human edits
     ↓
BuildLens detects overlap
     ↓
SYNC STATE = CONFLICT
     ↓
PAUSE automatic promotion for that file
     ↓
show BASE | HUMAN | CLAUDE
     ↓
learner explicitly resolves
     ↓
tests / validation
     ↓
record resolved version
```

There is **no supported "Claude wins", "human wins", "newest wins", or blind overwrite path**.


The learner must be able to open the code Claude is changing, edit that code manually, and continue watching Claude work.

However:

> **Claude and the learner must never silently overwrite one another.**

BuildLens must treat Claude edits and learner edits as distinct change streams.

### Required synchronization state machine

Each tracked logical file is always in one explicit synchronization state:

```text
SYNCED
HUMAN_CHANGED
CLAUDE_CHANGED
BOTH_CHANGED_CLEAN
MERGE_PENDING
CONFLICT
STALE_BUFFER
APPLYING
RECOVERY_REQUIRED
```

Only these transitions may write a merged result into the learner's managed worktree:

```text
CLAUDE_CHANGED → MERGE_PENDING → APPLYING → SYNCED
BOTH_CHANGED_CLEAN → MERGE_PENDING → APPLYING → SYNCED
CONFLICT → explicit resolution → MERGE_PENDING → APPLYING → SYNCED
```

`CONFLICT`, `STALE_BUFFER`, and `RECOVERY_REQUIRED` are stop states for automatic promotion.

This state machine is part of the correctness contract, not merely UI terminology.

The supported safe architecture is:

```text
                         COMMON BASE COMMIT
                         /                \
                        /                  \
                       v                    v
             HUMAN / BUILDLENS          CLAUDE SESSION
                WORKTREE                  WORKTREE
                    |                        |
                    | manual edits           | Claude edits
                    v                        v
              HumanVersion              ClaudeVersion
                    \                        /
                     \                      /
                      v                    v
                       RECONCILIATION
                  base + human + Claude
                           |
             +-------------+-------------+
             |                           |
             v                           v
        clean 3-way merge          overlapping hunk
             |                           |
             v                           v
          apply                    PAUSE PROMOTION
                                   require explicit
                                   human resolution
```

**Never use last-write-wins for source code.**

A manual save must carry the content/version hash that the editor started from. If the backing version changed, BuildLens rejects the stale save and asks the learner to reconcile instead of overwriting newer bytes.

A clean merged result may be written only after:
1. the expected base/version still matches;
2. three-way reconciliation reports no conflict;
3. the resulting content is written to a temporary file; and
4. the temporary file is atomically replaced into the destination where the platform/filesystem supports it.

Claude hooks are a second guard, not the primary isolation mechanism:
- `PreToolUse` may block `Edit|Write` while a file is in unresolved conflict;
- `PostToolUse` records successful Claude file-tool edits;
- shell commands can also change files, so `Stop` reconciliation must inspect actual Git working-tree state;
- `FileChanged` is useful for observation but is not a blocking mechanism.

The safety claim is intentionally narrow:

> **Within BuildLens's managed-worktree workflow, no supported code path may silently discard either the learner's or Claude's edit.**

BuildLens must not claim that arbitrary external processes on the machine can never bypass the workflow.

See `docs/COLLABORATIVE_EDITING.md`.

---

# 3. The Mandatory Build Loop

Every meaningful patch follows the same loop.

```text
INTENT
  |
  v
PREDICT
  |
  v
SKETCH
  |
  v
IMPLEMENT A SMALL PATCH
  |
  v
TRACE
  |
  v
DESIGN TESTS
  |
  v
RUN / COMPARE
  |
  v
TEACH BACK
  |
  v
CONNECT TO ARCHITECTURE
  |
  v
KNOWLEDGE GATE
  |
  v
COMMIT
```

A passing automated test suite does **not** complete a milestone.

A milestone is complete only when:

```text
code works
AND
you can trace it
AND
you can explain it
AND
you can place it in the system
AND
you pass an unseen transfer variant
```

---

# 4. Exercise Generation Rules

University examples are references for the **deep skill**, not a fixed question bank.

For each exercise archetype Claude must:

```text
SOURCE EXAMPLE
    |
    v
IDENTIFY DEEP SKILL
    |
    v
PRESERVE COGNITIVE STRUCTURE
    |
    v
CHANGE SURFACE FEATURES
    |
    v
GENERATE UNSEEN TEST
    |
    v
LEARNER COMMITS TO ANSWER
    |
    v
FEEDBACK
    |
    v
SECOND TRANSFER VARIANT
    |
    v
"WHAT PRINCIPLE DID BOTH SHARE?"
```

Claude must substantially change names, constants, ordering, context, and presentation.

It must not merely randomize numbers.

Examples should gradually move through three contexts:

```text
generic Python
      ↓
BuildLens code
      ↓
unfamiliar/transfer domain
```

Example:

```text
CMU-style list aliasing
      ↓
BuildLens session.events aliasing
      ↓
manufacturing inspection_events aliasing
```

The learner passes the **concept**, not the literal question.

---

# 5. Lifecycle

## Phase 0 — Specification Before Code

### High-level idea

Software begins with behavior and examples, not classes and frameworks.

### Build

Repository skeleton only:

```text
BuildLens/
├── docs/
├── learning/
├── src/
├── tests/
└── README.md
```

Create examples of expected behavior, but no real application implementation.

Example:

```text
INPUT:
a Git diff containing one changed file and two source additions

EXPECTED:
files_changed = 1
lines_added = 2
lines_removed = 0
```

### You learn

Define a problem precisely, restate it, produce test cases, and carry out a human version of the algorithm before writing code.

### Knowledge gate

Tiny sequential Python traces.

You must predict output and variable state by hand, then run the code, then solve a changed variant.

### WHERE YOU SHOULD BE

You should **not have an app yet**.

You should be able to say:

> "I know what the first BuildLens behavior is supposed to do, what goes in, what should come out, and the steps I would perform manually."

If Claude has already created a frontend, API, database, hook framework, or service layer, the project has moved too fast.

### Claude assistance level

HIGH.

Claude models how to decompose the problem, but does not solve the knowledge gate before you answer.

### Source anchors

CMU-112-ALGO, CMU-112, CMU-EBERLY-RETRIEVAL.

---

## Phase 1 — Pure Functions and Execution

### High-level idea

A program is a sequence of deterministic transformations before it becomes an architecture.

### Build

Create only small pure functions, for example:

```python
classify_diff_line(...)
count_changes(...)
parse_diff(...)
```

Prefer functions that can be viewed in their entirety on one screen.

### You learn

Parameters, arguments, local variables, branches, loops, function calls, return values, and deterministic transformation.

### Knowledge gate

Trace a new function problem with 2–3 calls and one branch.

Then trace one real BuildLens function line-by-line.

### WHERE YOU SHOULD BE

BuildLens should look like a **tiny Python library**, not an application.

You should be able to execute every important function mentally.

Target conceptual shape:

```text
raw text
   ↓
pure function
   ↓
simple Python value
```

### Claude assistance level

HIGH → MEDIUM.

Claude can implement small functions after you predict their contracts.

### Do not introduce yet

Classes for architecture, database, API, React, Claude hooks, async code.

---

## Phase 2 — Data Representation and Test Design

### High-level idea

Code becomes easier to reason about when important data has an explicit representation and contract.

### Build

Start with simple dictionaries/lists where appropriate, then introduce a small named structure such as:

```python
@dataclass(frozen=True)
class ChangeSummary:
    files_changed: int
    lines_added: int
    lines_removed: int
```

Add focused unit tests.

### You learn

Collections, structured data, representation choice, immutability, edge cases, and test-first thinking.

### Knowledge gate

Before Claude shows tests, design normal, boundary, empty, and invalid cases.

Complete an unseen CMU-style list/string trace.

Explain why a dictionary may have been sufficient earlier and why a named domain structure is now useful.

### WHERE YOU SHOULD BE

BuildLens is still primarily **input → transformation → result**.

There is little or no long-lived state.

You should know every field in `ChangeSummary`, where it originates, and why it exists.

### Claude assistance level

MEDIUM.

Claude increasingly asks you what the data model should contain instead of defining it for you.

---

## Phase 3 — State and the State Movie

### High-level idea

State means the output of one operation can affect future operations.

### Build

Introduce the smallest meaningful session state:

```text
Session
└── changes[]
```

Add a state-transition representation suitable for later visualization.

### You learn

Mutation, aliases, copies, object identity, ownership of mutable state, previous-state → event → new-state reasoning.

### Knowledge gate

CMU-style alias/copy trace with a fresh variant.

Then trace the real BuildLens session state through several operations.

### WHERE YOU SHOULD BE

You should now be able to draw:

```text
STATE 0
[]
   |
record change
   v
STATE 1
[change_a]
   |
record change
   v
STATE 2
[change_a, change_b]
```

The project still has no need for a polished UI.

If you cannot explain which object owns the list and who can mutate it, stop here.

### Claude assistance level

MEDIUM.

---

## Phase 4 — Decomposition by Refactoring

### High-level idea

Modules should emerge because responsibilities have actually diverged.

### Build

Allow the simple implementation to become mildly uncomfortable, then separate responsibilities.

Possible result:

```text
src/buildlens/
├── diff_parser.py
├── models.py
└── change_store.py
```

### You learn

Top-down design, cohesion, coupling, responsibility boundaries, refactoring versus behavior change.

### Knowledge gate

Teach one full source file aloud.

Then trace one value across two modules.

Explain:

> Why are these responsibilities separate?

and:

> Why do they not need five more layers?

### WHERE YOU SHOULD BE

BuildLens should be a small **multi-module Python program**.

You should know the dependency direction from memory.

You should remember why the split happened because you experienced the pre-refactor state.

### Claude assistance level

MEDIUM → LOW.

You propose the split first. Claude critiques it.

---

## Phase 5 — Explicit Interfaces / Contracts

### High-level idea

Once modules depend on one another, what crosses the boundary matters more than the filenames.

### Build

Make contracts explicit.

Example:

```text
DiffParser

INPUT:
str

OUTPUT:
ChangeSummary


ChangeStore

INPUT:
ChangeSummary

OUTPUT:
Change identifier / result
```

Use type hints and explicit domain models.

### You learn

Interface, contract, dependency direction, representation boundaries.

### Knowledge gate

Given a new multi-function example, draw caller/callee frames.

Then label every BuildLens module boundary with the type/value crossing it.

### WHERE YOU SHOULD BE

You should be able to draw BuildLens without implementation detail:

```text
diff source
   ↓ str
parser
   ↓ ChangeSummary
store
```

If your explanation depends on filenames instead of responsibilities/contracts, repeat the gate.

### Claude assistance level

LOW.

Claude asks questions; you propose the interface.

---

## Phase 6 — First Complete Vertical Slice: CLI

### High-level idea

Understand a complete runtime path before adding visual/frontend complexity.

### Build

Add a tiny CLI:

```bash
buildlens analyze
```

Example output:

```text
Files changed: 2
Lines added: 17
Lines removed: 4
```

### You learn

Entry point, call chain, orchestration, end-to-end data flow.

### Knowledge gate

Close the repository.

Recreate the vertical slice from memory.

Then follow a single value such as `lines_added = 17` from input to terminal output, naming each function and representation.

### WHERE YOU SHOULD BE

You now have the **first real application**.

It is intentionally plain.

You should understand essentially the entire runtime flow:

```text
CLI
 ↓
application function
 ↓
parser
 ↓
store
 ↓
formatted output
```

This is the first major checkpoint.

### Claude assistance level

LOW.

---

## Phase 7 — Git as the First External Boundary

### High-level idea

External integrations should enter through a narrow boundary instead of leaking through the domain.

### Build

Replace hard-coded/manual diff input with Git inspection.

```text
Git
 ↓
Git adapter
 ↓
raw diff
 ↓
existing BuildLens core
```

### You learn

I/O, subprocesses, external-system boundaries, adapters, error handling.

### Knowledge gate

Explain what code knows about Git and what code does not.

Trace a Git failure.

Compare:

```text
manual input path
vs
Git input path
```

and identify what remained unchanged.

### WHERE YOU SHOULD BE

BuildLens can inspect **real repository changes**, but is not yet Claude-aware.

The important mental model is:

```text
OUTSIDE
Git
 |
------- boundary -------
 |
BUILDLENS
parser → store → output
```

### Claude assistance level

LOW.

---

## Phase 8 — Claude Code Adapter

### High-level idea

A second external system should plug into the existing architecture without forcing the core to become Claude-specific.

### Build

Integrate Claude Code hooks **and capture Claude's isolated worktree identity**.

Claude Code Desktop uses isolated Git worktrees for Git-backed sessions. BuildLens should treat the Claude session worktree as the Claude-owned change stream rather than encouraging Claude and the learner to edit the same physical file.

Start with:
- session/worktree identity;
- successful `Edit|Write` `PostToolUse`;
- `PreToolUse` for later conflict blocking;
- a `Stop` reconciliation scan of the actual Git working tree.

Do not rely only on `FileChanged`: it is useful for observation but cannot block a file change. Claude can also alter files through Bash/PowerShell, so `Stop` must compare Git state against BuildLens's last observed snapshot.

For every observed file version record at least:

```text
session/worktree id
repository-relative path
base commit/blob
content hash
observed-at time
provenance = CLAUDE
```

Conceptual flow:

```text
Claude Code Desktop
   ↓ isolated Claude worktree
PreToolUse / PostToolUse / Stop
   ↓
hook relay
   ↓
Claude adapter
   ↓
versioned ClaudeChange
   ↓
existing BuildLens core
```

At this phase BuildLens only observes the Claude worktree. The learner-edit worktree is introduced later, after the observation/version model is understood.

### You learn

Event source, integration adapter, event normalization, lifecycle events, reconciliation.

### Knowledge gate

Given an unfamiliar hook payload, decide:

> What belongs to the Claude adapter?

> What internal representation should leave the adapter?

Then draw the "new" and "unchanged" parts of the system.

### WHERE YOU SHOULD BE

BuildLens can now **observe Claude-assisted development**, but the interface may still be CLI/log based.

You should be able to explain exactly why Claude-specific JSON does not flow through every module.

### Claude assistance level

VERY LOW for design.

Claude can help with exact hook schema implementation after you propose the boundary.

---

## Phase 9 — Event-Driven State and Reliability

### High-level idea

A stream of external events creates ordering, duplication, failure, and reconciliation concerns.

### Build

Formalize an internal event model and session lifecycle.

Examples:

```text
ChangeObserved
TurnCompleted
ReconciliationCompleted
GateStarted
GatePassed
```

Add invalid-input behavior, deduplication/reconciliation where justified, and failure-path tests.

Also introduce the **version/reconciliation primitives** that later protect manual editing:

```text
FileVersion
- repo path
- worktree id
- base Git blob/commit
- content hash
- provenance
- observed sequence

ReconcileInput
- common base
- human version
- Claude version

ReconcileResult
- CLEAN
- CONFLICT
- STALE
- ERROR
```

Do not add the visual editor yet. First prove headlessly that:
- two non-overlapping edits from a common base can merge;
- overlapping edits return `CONFLICT`;
- stale expected hashes are rejected;
- neither original version is destroyed during reconciliation.

### You learn

Events vs direct calls, state machines, happy path vs failure path, idempotence where needed, failure ownership.

### Knowledge gate

Trace:

```text
initial state
→ event A
→ state
→ event B
→ state
→ failure
→ resulting state
```

Then solve a fresh debugging scenario using hypothesis → evidence → falsifying test.

### WHERE YOU SHOULD BE

BuildLens should be a reliable **headless event-capture application**.

At this point the backend behavior is more important than visual polish.

You should be able to tell an interviewer what happens if an event is malformed or a turn ends after edits made through Bash.

### Claude assistance level

REVIEWER.

Claude should challenge your state design rather than choosing it.

---

## Phase 10 — Learning Engine and Knowledge Gates

### High-level idea

BuildLens now begins enforcing understanding rather than merely collecting changes.

### Build

Create:

```text
learning/
├── archetypes/
├── attempts/
└── mastery/
```

Core concepts:

```text
ExerciseArchetype
KnowledgeGate
Attempt
Misconception
MasteryRecord
```

The generator uses source-grounded archetypes and creates new surface forms.

### You learn

Abstraction at the learning-system level, deterministic records vs generated content, evaluation criteria, transfer.

### Knowledge gate

The learning engine tests *you* on previous phases.

A gate passes only after:

```text
primary unseen variant
+
transfer variant
+
principle explanation
```

### WHERE YOU SHOULD BE

BuildLens is now recognizably a **learning product**, but still does not need a polished dashboard.

It can say:

```text
Claude changed X.
Before continuing, explain Y.
Here is an unseen tracing problem testing the same idea.
```

### Claude assistance level

EXAMINER.

---

## Phase 11 — Persistence

### High-level idea

Persistence exists because sessions, attempts, mastery, and decisions now need to survive restarts.

### Build

Introduce SQLite only now.

Persist:

```text
sessions
changes
events
attempts
mastery
architecture decisions
```

Keep persistence behind narrow repositories/interfaces.

### You learn

In-memory vs persistent state, database responsibility, schema, transactions, repository boundaries.

### Knowledge gate

Take one object from Python memory and trace how it becomes a database row and comes back.

Then defend:

> Why SQLite for BuildLens?

and:

> Under what requirement would SQLite stop being the right choice?

### WHERE YOU SHOULD BE

Closing and reopening BuildLens should preserve your development-learning history.

You should understand why a database has appeared now when it was unnecessary in Phase 1.

### Claude assistance level

REVIEWER.

---

## Phase 12 — Local API

### High-level idea

The domain becomes usable by another process through explicit network contracts.

### Build

Add a small FastAPI layer over already-understood services.

Keep route handlers thin.

Conceptual shape:

```text
HTTP
 ↓
validation / request model
 ↓
application service
 ↓
domain
 ↓
repository
```

### You learn

Process boundaries, serialization, request/response, API/domain separation.

### Knowledge gate

Follow one value:

```text
HTTP JSON
→ request model
→ domain type
→ service
→ response model
→ JSON
```

Identify where validation belongs and where business rules belong.

### WHERE YOU SHOULD BE

BuildLens is now a **local service**.

The API exposes an existing application; it should not become the place where the domain logic suddenly moves.

### Claude assistance level

REVIEWER / INTERVIEWER.

---

## Phase 13 — Real-Time Code Workspace and Safe Collaborative Editing

### High-level idea

The frontend becomes a **live editable coding workspace**, not merely a dashboard.

The learner must be able to:

```text
watch Claude edit
→ inspect Claude's live diff
→ open the changed file
→ type a manual edit
→ save that edit as a separate human change
→ reconcile human + Claude changes
→ continue without silent overwrite
```

### Build

Add the smallest useful React UI with a code-editor component.

Initial panes:

```text
File Tree
Live Claude Diff
Editable Human File
Current Knowledge Gate
```

Then:

```text
Execution Map
State Movie
Mastery
```

For reconciliation add a three-pane conflict view:

```text
BASE
| 
|--- HUMAN
|
|--- CLAUDE
```

or an equivalent clear merge UI.

### Write model

A BuildLens editor buffer opens against a specific `FileVersion`.

On save it sends:

```text
path
human content
expected/base content hash
human worktree id
```

The backend must re-read/hash the destination before writing.

If:

```text
current_hash != expected_hash
```

the save is `STALE_BUFFER`.

BuildLens does **not** overwrite.

Claude Desktop's own file pane warns when a file changed on disk after it was opened. BuildLens adopts that stale-buffer idea but intentionally removes blind overwrite from the normal workflow: a stale buffer must reload or enter reconciliation.

For a valid save:

```text
write new bytes to temporary file
→ flush/close
→ atomically replace destination where supported
→ calculate new hash
→ record provenance = HUMAN
```

Python's `hashlib` provides the version fingerprint; temporary-file APIs plus `os.replace()`/`Path.replace()` provide the safe write primitive. Atomic replacement prevents readers from seeing a half-written manual save on supported same-filesystem paths; it does not solve logical merge conflicts, which is why version checking happens first.


Do not overclaim atomic replacement. Python documents `os.replace()` as atomic when successful as a POSIX requirement, and it can fail across filesystems. Therefore the temporary file must be created in the destination directory/same filesystem.

For crash consistency, file bytes are authoritative and metadata is recoverable. Before applying a merged/manual version:

```text
1. persist WriteIntent(status=PENDING, expected_hash, result_hash)
2. write temp file in destination directory
3. close + flush file
4. os.replace(temp, destination)
5. re-hash destination
6. mark WriteIntent COMMITTED
```

On startup, any `PENDING` write intent is reconciled against the actual destination hash before BuildLens resumes automatic editing.

This closes the important crash window:

```text
file replaced
BUT
metadata not yet marked committed
```

without pretending Python alone provides database/filesystem distributed transactions.

### Isolation model

Claude and learner changes must normally live in separate Git worktrees.

Do not assume their current tips still share the exact commit they originally started from. At reconciliation time, BuildLens resolves the actual Git merge base and obtains the file's base blob from that commit.

```text
merge_base = git merge-base(H_tip, C_tip)
BASE       = file blob at merge_base
HUMAN      = current human-worktree bytes
CLAUDE     = current Claude-worktree bytes
```

Then reconcile:

```text
merge(current=HUMAN, base=BASE, other=CLAUDE)
```

This matters when either side has committed or advanced independently after the session began.

A Git-style three-way merge is appropriate because it can distinguish:
- only-human changes;
- only-Claude changes;
- compatible non-overlapping changes;
- overlapping changes requiring resolution.

### Conflict rule

If both sides modify an overlapping segment:

```text
DO NOT:
pick newest
pick Claude
pick human
concatenate blindly
hide one side
```

Instead:

```text
ConflictDetected
→ mark path unresolved
→ stop promotion/apply for that path
→ show base + human + Claude
→ require explicit resolution
→ verify resolution
→ record resolved version
```

Claude may continue reasoning, but BuildLens should prevent an unresolved path from being silently synchronized over the human version.

Where useful, a `PreToolUse` hook can deny Claude `Edit|Write` calls for a path currently marked `CONFLICT`, with the reason returned to Claude. This is defense in depth only: shell-based file mutation means the worktree separation and `Stop` reconciliation remain the authoritative safeguards.


### Reconciliation cadence

BuildLens should not wait until the end of a long Claude turn to discover a collision.

Use layered detection:

```text
HUMAN SAVE
→ immediate version check + reconcile affected file

CLAUDE Edit|Write PostToolUse
→ immediate reconcile affected file

FileChanged
→ mark observed path dirty and reconcile when it belongs to a managed worktree

Stop
→ full `git status --porcelain` / repository reconciliation sweep

SESSION/APP START
→ recovery sweep before allowing automatic promotion
```

`PostToolUse` gives fast feedback for successful Claude file tools; `FileChanged` catches watched on-disk changes regardless of writer but cannot block them; the `Stop` sweep is the completeness backstop for shell commands, untracked files, renames, and anything an earlier event missed.


### Manual edits are first-class history

Every manual edit should appear in the timeline separately from Claude edits.

Example:

```text
09:31:02 CLAUDE  parser.py  +12 -3
09:32:18 HUMAN   parser.py   +2  -1
09:32:22 SYSTEM  parser.py   CONFLICT
09:34:01 HUMAN   parser.py   RESOLVED
```

The learner should always be able to answer:

> Which bytes came from Claude?

> Which bytes came from me?

> What base did we both start from?

> Was this result auto-merged or manually resolved?

### You learn

- optimistic concurrency/version checking;
- immutable provenance;
- Git worktrees;
- three-way merge;
- logical conflict vs physical file-write safety;
- why observation hooks are different from authority;
- why atomic write is different from conflict resolution.

### Knowledge gate — collaborative editing architecture

Claude gives a **new** base/human/Claude example.

You must classify it:

```text
CLEAN
STALE
CONFLICT
```

Then explain the next legal state transition.

Example shape:

```text
BASE:
price = subtotal * tax

HUMAN:
price = subtotal * tax_rate

CLAUDE:
price = round(subtotal * tax, 2)
```

Do not reuse the same lines each time.

Later variants should involve:
- separate functions in the same file;
- same exact line changed differently;
- adjacent edits that Git treats as an overlapping hunk;
- file rename + edit;
- delete vs edit;
- two stale editor tabs;
- stale hash without textual overlap;
- Claude shell edit discovered only at `Stop`;
- crash before `os.replace()`;
- crash after `os.replace()` but before metadata commit;
- clean three-way merge;
- a new merge base after one side commits.

### Architecture-defense exercise

You must defend:

> Why not let Claude and the human edit the same physical working tree?

> Why aren't file locks alone sufficient?

> Why do we need a base version/hash?

> Why three-way merge instead of last-write-wins?

> Why is `PreToolUse` not sufficient by itself?

> Why is `FileChanged` observation not a blocking guarantee?

> Why reconcile immediately on manual saves / Claude file-tool edits *and* sweep again at `Stop`?

> Why recompute the Git merge base instead of assuming the original session-start commit forever?

> Why use an atomic replace after the logical conflict check?

> Why is a write-intent/recovery record needed if the file replace itself is atomic?

> Why is provenance stored as immutable change history rather than permanent per-line ownership?

> What failures are still outside BuildLens's guarantee?

A strong answer should distinguish **three separate protections**:

```text
WORKTREE ISOLATION
prevents physical overwrite between actors

VERSION + THREE-WAY MERGE
prevents logical lost updates

ATOMIC FILE REPLACE
prevents partial/torn manual writes
```

### WHERE YOU SHOULD BE

This is the first time BuildLens should feel genuinely VS Code-like.

You can watch Claude's changes live, open the same logical source file, and write your own version.

But the implementation must make this statement true:

> **Seeing and editing the same logical file never means sharing an uncoordinated physical write target.**

By now you should be able to trace an edit from:

```text
keystroke
→ editor buffer
→ version-checked save request
→ human worktree
→ reconciliation
→ conflict or clean merged version
→ updated diff/timeline
```

### Claude assistance level

INTERVIEWER / ADVERSARIAL REVIEWER.

Claude should actively try to find lost-update races and ambiguous ownership.

---

## Phase 14 — Architecture Views and Decision Ledger

### High-level idea

Architecture is a set of decisions serving requirements and quality attributes, not a diagram of folders.

### Build

Add architecture/decision records.

For consequential decisions record:

```text
Problem
Constraints
Quality attributes
Alternatives
Decision
Mechanism
Tradeoff
Evidence
Failure modes
Reversal condition
```

Maintain multiple views:

```text
module
runtime
data
deployment
failure
```

### You learn

Architecture views, architectural drivers, quality attributes, risks, sensitivities, and tradeoffs.

### Knowledge gate

Rebuild one architecture view from memory.

Then defend a real BuildLens choice and attack the same choice.

At least one required ADR must cover collaborative editing:

```text
ADR — Separate worktrees + optimistic reconciliation

Problem:
human and Claude may edit the same logical code concurrently

Rejected:
single shared worktree + last-write-wins
single shared worktree + advisory lock only

Chosen:
separate worktrees from a common base
+ content-version checks
+ three-way merge
+ explicit conflict state
+ atomic replacement for manual writes

Tradeoff:
more Git/worktree/reconciliation complexity

Benefit:
no supported path silently discards either actor's edit

Reversal condition:
a future editor/agent protocol provides a single authoritative transactional
document model with equivalent provenance and conflict guarantees
```

The learner must be able to defend this ADR without reading it.

### WHERE YOU SHOULD BE

You should now be able to give a serious architecture interview about BuildLens without needing a prepared script.

The diagrams document a model already in your head.

### Claude assistance level

HOSTILE REVIEWER.

---

## Phase 15 — Interview / Oral Defense Mode

### High-level idea

The final test is whether understanding transfers to explanation under pressure.

### Build

Create an interview mode that selects:

```text
a feature
a code path
a design decision
a failure
an unfamiliar transfer problem
```

Claude must not simply repeat the reasoning that produced the implementation.

Where possible, use a separate reviewer/examiner context.

### Exam sequence

```text
1. Explain the product.
2. Draw the architecture.
3. Trace one user/event path.
4. Locate the implementing files/functions.
5. Trace one value/state transition.
6. Explain a failure path.
7. Defend a decision.
8. Attack your own decision.
9. State the reversal condition.
10. Review unfamiliar code using the same principles.
```

### WHERE YOU SHOULD BE

You are finished when you can move without hesitation among:

```text
PRODUCT
   ↕
ARCHITECTURE
   ↕
MODULE
   ↕
FUNCTION
   ↕
DATA / STATE
   ↕
FAILURE
   ↕
TRADEOFF
```

The end goal is **not** knowing the BuildLens repository by memorization.

The end goal is having learned a reusable method for understanding and defending software systems.

---


# 5A. Evolving Exercise Curriculum — Academic Idea → Current Project → Transfer Project

BuildLens must evolve the *source* of its exercises as the codebase grows.

The learner should not spend the whole project solving disconnected textbook snippets. Early exercises use small academic-style examples because the code must fit in working memory. As the learner gains fluency, Claude should increasingly derive exercises from:

1. the BuildLens code that was just written;
2. Argos Control Tower;
3. Datum;
4. Trellis AI Agent;
5. later, an unfamiliar but related repository or synthetic transfer domain.

The progression is deliberate:

```text
ACADEMIC MICRO-PROBLEM
        ↓
SAME IDEA IN BUILDLENS
        ↓
SAME IDEA IN ARGOS
        ↓
SAME IDEA IN DATUM
        ↓
SAME IDEA IN TRELLIS
        ↓
BLIND / UNFAMILIAR TRANSFER
```

This follows the learning principle that the learner must identify the **deep structure** of a problem instead of memorizing superficial features.

## Curriculum ladder

| Build stage | Primary exercise source | Why |
|---|---|---|
| Phases 0–2 | CMU/Berkeley-inspired synthetic Python | Keep execution small enough to trace completely. |
| Phases 1–4 | Current BuildLens functions | Immediately connect concepts to code the learner is building. |
| Phases 3–7 | Argos Control Tower | Deterministic state projection, data transformation, ordering, aggregation, missing data, and evidence are concrete and visual. |
| Phases 4–10 | Datum | Reconciliation, set/union reasoning, natural keys, explicit boundaries, domain models, deterministic ordering, and architecture decisions add complexity. |
| Phases 7–15 | Trellis AI Agent | Trust boundaries, typed tool contracts, authorization, idempotency, transactions, retry/failure behavior, and concurrency belong later. |
| Phases 10–15 | Unfamiliar/adjacent repo | Proves transfer beyond memorized personal projects. |

### Difficulty constraint

Claude must never choose a reference-project exercise because it is interesting if it introduces several concepts that the learner has not reached.

Examples:

- Argos `_optional_string()` or a simplified `_build_quality()`-style accumulator is appropriate early.
- Argos `project_factory_state()` is appropriate after state, ordering, and module tracing have been learned.
- Datum `_field_discrepancies()` is appropriate after lists/dicts/sets and explicit data models.
- Trellis lease acquisition and replay logic is **not** an early Python tracing exercise. It belongs after state, boundaries, persistence, transactions, and failure tracing.

The source repository must serve the curriculum, not dictate it.

---

# 5B. Reference-Project Exercise Mining Protocol

Before generating a repository-derived exercise, Claude should:

```text
1. Select ONE concept currently being learned.
2. Read the relevant source file and nearby tests/documentation.
3. Identify the deep skill.
4. Remove project-specific complexity not needed to test that skill.
5. Generate a related but different problem.
6. Require a prediction before execution.
7. Evaluate both result and explanation.
8. Generate a transfer variant using a different context.
9. Ask what underlying principle both variants share.
10. Record any misconception for future spaced retrieval.
```

## Source-fidelity rule

Claude may use a real repository to understand a pattern, but it should not make the gate an exercise in memorizing that repository.

A generated exercise should generally change:

- names;
- values;
- domain vocabulary;
- ordering;
- concrete data;
- non-essential control-flow shape.

It should preserve:

- the core execution concept;
- the important state relationship;
- the architectural principle;
- the failure/tradeoff being tested.

## Repository freshness rule

`docs/REFERENCE_PROJECTS.md` contains verified reference files and a last-checked commit.

When GitHub access is available, Claude should resolve the current default-branch version before mining a new exercise.

When it is unavailable, Claude may use the last verified reference, but must say the exercise is based on the documented snapshot rather than implying that it inspected current code.

---

# 5C. Concrete Exercise Families from the Reference Projects

## Argos Control Tower — deterministic transformation and projection

Use Argos first because its control flow is comparatively easy to visualize.

Representative concepts from `backend/app/projection.py`:

```text
NormalizedEvent[]
      ↓ sorted(timestamp, ingestion_index)
creation events
      ↓
per-job accumulator
      ↓ lifecycle transitions
JobState[]
      ↓
overview / quality / attention projections
```

Good generated exercises include:

### Early
- write/trace a helper that accepts an unknown object and returns a string or `None`;
- trace a loop that counts defect codes;
- predict an inspection pass-rate aggregation;
- design tests for missing vs invalid quantity data.

### Middle
- trace one job through `created → started → blocked → unblocked → completed`;
- predict the final state when two events have the same timestamp but different ingestion indices;
- identify which event should be evidence for an active block;
- design a test proving terminal completion prevents later lifecycle changes.

### Later
- follow one value such as `good_quantity` into aggregate yield;
- explain why manufacturing rules belong in projection rather than React/API;
- identify the consequences of replacing deterministic sorting with source-file order;
- reconstruct the projection pipeline without opening the repository.

Do not reuse Argos's literal dataset values as the answer key. Create new jobs/events that test the same rules.

---

## Datum — reconciliation, representation, and boundaries

Representative concepts from `datum/reconcile/diff.py`:

```text
MatchResult
   ├── matched pairs
   ├── declared orphans
   └── discovered orphans
          ↓
ordered comparison
          ↓
union of attribute keys
          ↓
field discrepancies + orphan discrepancies
```

Good generated exercises include:

### Early-middle
- union two dictionaries' keys and identify differences;
- sort resources by a natural key before producing output;
- distinguish a missing key from a key explicitly containing `None`;
- predict discrepancy output for declared/discovered objects.

### Middle-late
- teach a simplified reconciliation file aloud;
- explain why declared and discovered state should remain separate;
- trace a resource from an external representation across a validation/trust boundary;
- compare full-rebuild projection with incremental mutation using explicit tradeoffs;
- identify which domain fact belongs in a typed field versus unstructured attributes.

### Architecture-defense variants
Ask:

```text
Why are declared and discovered state separate?
What bug becomes possible if a query silently blends them?
What requirement would justify changing the design?
```

Claude should generate a different domain (for example desired package versions vs installed versions) to test whether the learner recognizes the same reconciliation pattern.

---

## Trellis AI Agent — trust boundaries, authorization, idempotency, and transactions

Use Trellis late.

Representative concepts from `backend/app/idempotency.py`:

```text
tool call
  ↓
lease insert
  ├── inserted → EXECUTE
  └── conflict
         ↓
      inspect state/hash
         ├── completed → REPLAY
         ├── failed → guarded reacquire
         ├── pending → wait / resolve
         └── different hash → CONFLICT
```

Good generated exercises include:

### Middle-late
- trace a simplified finite-state lease machine;
- decide which values must be part of an idempotency key;
- predict whether a retry executes, replays, waits, or conflicts;
- design tests for same key/same arguments versus same key/different arguments.

### Late
- explain why mutation + audit event + lease completion belong in one transaction;
- identify the race in `SELECT state → unguarded UPDATE`;
- trace a lost-response scenario;
- explain why a browser/model is not authoritative state;
- defend the separation between framework approval UI and server-recorded authorization.

Transfer domains should not always be AI agents. Claude can use:

- payment retries;
- job-queue workers;
- webhook delivery;
- manufacturing command execution;
- inventory reservations.

The learner passes only if the same principle survives the domain change.

---

# 5D. Mandatory Small Learning Pauses

These are not optional enrichment activities. They are distributed throughout implementation so the learner repeatedly stops building and retrieves what they know.

## Pause A — Predict → Run → Modify → Predict Again

**Cadence:** every phase through Phase 8; after Phase 8 use it for unfamiliar snippets rather than every patch.

For one relevant snippet:

```text
1. Predict output/state by hand.
2. Commit to the answer.
3. Run it.
4. Explain any mismatch.
5. Change one meaningful condition/operation/input.
6. Predict again before running.
```

The modification must change reasoning, not merely rename variables.

## Pause B — Write Tests Before Seeing Tests

**Cadence:** at least once per implementation phase that adds behavior.

Before Claude reveals its test plan, the learner must propose:

```text
normal
boundary
empty/missing
invalid
failure
```

Only categories relevant to the feature are required.

The learner must explain **which assumption each test attacks**.

## Pause C — Teach One File Aloud

**Cadence:** once after each new meaningful module is introduced and at least once per week.

The explanation must cover:

```text
purpose
inputs
outputs
dependencies
callers
state changes
important branches
assumptions
failure modes
design reason
```

Do not accept a filename-level summary.

## Pause D — Weekly Architecture Reset

**Cadence:** once every 7 calendar days of active BuildLens work, or before a major phase transition if that occurs first.

Procedure:

```text
1. Close the repository and previous diagram.
2. Delete or hide the current architecture diagram.
3. Recreate it from memory.
4. Draw relationships/arrows, not just boxes.
5. Compare against current code.
6. Mark every missing/incorrect box or arrow.
7. Add those gaps to CURRENT_STATE.md as study targets.
```

Difficulty evolves:

```text
Week 1: functions and data
Week 2: state and module calls
Week 3: one full runtime/data path
Week 4: module + runtime views
Later: module + runtime + data + deployment + failure
```

An architecture diagram is not "passed" because it looks neat. It is passed when the important responsibilities and relationships match the implementation.

---


## Pause E — Unfamiliar Code Review

**Cadence:** once per week after Phase 5.

Use `docs/CODE_READING_DEBUGGING_PLAYBOOK.md`.

Claude supplies or selects a small unfamiliar file/path appropriate to the current level.

The learner must identify:

```text
purpose
call path
important state
invariant
failure
test
design concern
```

Do not reveal the walkthrough first.

## Pause F — Oral Design Review

**Cadence:** at every major phase transition and once per week after Phase 7.

Use `docs/DESIGN_REVIEW_RUBRIC.md`.

Start with the repository closed for architecture questions.

Claude scores the explanation but must cite concrete gaps rather than giving a vague "good job."


# 5E. Spaced Mastery Schedule

Concepts must recur after the phase that introduced them.

For every important concept:

```text
T0     learn it in a small academic-style problem
T0     use it in the current BuildLens patch
+2 phases   solve a different-looking reference-project transfer
weekly      cold retrieval question
final       blind interview/code-review transfer
```

Example:

```text
ALIASES / COPIES

CMU-style list
     ↓
BuildLens Session.changes
     ↓
Argos event/timeline list
     ↓
cold weekly question
     ↓
unfamiliar repository
```

A concept is not marked "mastered" after one correct answer.

Recommended mastery rule:

```text
3 correct unseen variants
across at least 2 contexts
with one delayed attempt
and a correct explanation of the underlying principle
```

---

# 5F. Project Evolution Checkpoints

Claude should tell the learner what the repository *should feel like* at each checkpoint.

```text
CHECKPOINT A — tiny Python
Phases 0–2
"I can hold the whole program in my head."

CHECKPOINT B — stateful Python
Phases 3–5
"I understand who owns state and what crosses module boundaries."

CHECKPOINT C — complete headless application
Phases 6–9
"I can trace one external event all the way through the system."

CHECKPOINT D — learning product
Phases 10–12
"The system now tests my understanding and preserves what I learned."

CHECKPOINT E — visual control tower
Phases 13–14
"The UI visualizes a backend I already understand."

CHECKPOINT F — interview simulator
Phase 15
"I can defend the system and transfer the reasoning to unfamiliar code."
```

At each checkpoint Claude must explicitly compare the actual repository to this expected shape and report if the project has drifted ahead or behind the curriculum.


# 6. The "Where Am I?" Note Claude Must Maintain

At the end of every implementation session, Claude updates a short lifecycle note.

Template:

```text
BUILDLENS LIFECYCLE

Current phase:
Phase N — <name>

What exists:
<plain-English description of the working software>

What does NOT exist yet:
<important future pieces Claude must not prematurely add>

Current execution path:
<input> → <component> → <component> → <output>

What I should know cold:
<3–5 concepts/code paths>

Current weak concepts:
<from failed or uncertain gates>

Next knowledge gate:
<concept, not literal repeated question>

Gate source ladder:
<academic / BuildLens / Argos / Datum / Trellis / blind transfer, and why it is appropriate now>

Next implementation milestone:
<smallest code change after gate passes>

End-game relationship:
<one sentence explaining how this phase contributes to final BuildLens>
```

This note is not decorative documentation. It is the primary guard against losing track of where the project is in its lifecycle.

---

# 7. Recommended Repository Structure at End State

```text
BuildLens/
├── .claude/
│   └── settings.json
│
├── docs/
│   ├── LEARNING_SOURCES.md
│   ├── ARCHITECTURE.md
│   └── decisions/
│       ├── ADR-001-*.md
│       └── ...
│
├── learning/
│   ├── archetypes/
│   │   ├── sequential-tracing.yaml
│   │   ├── function-calls.yaml
│   │   ├── loop-state.yaml
│   │   ├── aliasing.yaml
│   │   ├── test-design.yaml
│   │   ├── module-tracing.yaml
│   │   ├── debugging.yaml
│   │   ├── failure-tracing.yaml
│   │   └── architecture-defense.yaml
│   └── LEARNING_RULES.md
│
├── backend/
│   ├── buildlens/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── adapters/
│   │   │   ├── git/
│   │   │   ├── claude/
│   │   │   └── persistence/
│   │   ├── api/
│   │   └── learning/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── features/
│   │   ├── components/
│   │   └── api/
│   └── tests/
│
├── scripts/
│   └── claude_hook_relay.py
│
├── IMPLEMENTATION_PLAN.md
├── CLAUDE.md
└── README.md
```

This is a destination.

Do **not** create this entire tree at project initialization.

The Git history should visibly show the architecture growing into this shape.

---

# 8. What Claude Must Optimize For

Claude's priorities, in order:

```text
1. learner understanding
2. behavioral correctness
3. clarity
4. testability
5. reliability
6. appropriate architecture
7. development speed
```

Claude must not optimize LOC/hour.

When a patch introduces more than one major conceptual jump, split it.

When the learner cannot explain the previous step, stop implementation and generate a targeted transfer exercise.

When a new abstraction is proposed, explain the concrete problem it solves only **after** the learner has attempted to identify that problem.

When a technology is proposed, require the learner to state:

```text
problem
constraint
alternative
choice
tradeoff
reversal condition
```

before treating the choice as understood.

---

# 9. Definition of Done for BuildLens

The product is technically complete when it can reliably:

```text
observe Claude development
→ reconstruct meaningful file/code changes
→ organize them into sessions
→ show Claude diffs live
→ let the learner edit the same logical code in a separate managed worktree
→ preserve human and Claude provenance separately
→ reject stale manual saves
→ cleanly three-way merge compatible edits
→ force explicit resolution of overlapping edits
→ never silently discard either side in the managed workflow
→ generate source-grounded unseen knowledge gates
→ track concept mastery and misconceptions
→ preserve history
→ visualize execution/state/architecture
→ record design decisions
→ run an architecture/code-defense interview
```

The learning project is complete only when the developer can explain how those capabilities are implemented and why the major decisions were made.

That second definition of done is the one that matters most.
