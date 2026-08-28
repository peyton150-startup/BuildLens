# BuildLens — Learning Rules

These rules govern Claude while BuildLens is being built and later govern the knowledge-gate generator.

## Prime directive

Do not let implementation speed outrun learner understanding.

A patch is not complete because tests pass.

It is complete when:
- behavior works;
- the learner can trace it;
- the learner can explain it;
- the learner can place it in the architecture;
- the learner passes an unseen transfer variant.

---

# 1. Exercise source order

Prefer the least complex source that genuinely tests the current skill:

```text
academic micro-example
→ BuildLens
→ Argos
→ Datum
→ Trellis
→ blind transfer
```

Do not use advanced code early simply because it is available.

---

# 2. Related-but-not-the-same rule

Never repeat a source exercise verbatim.

Extract:

```text
deep concept
required state relationship
required control-flow property
required design principle
```

Then vary:
- identifiers;
- constants;
- order;
- domain;
- data;
- superficial syntax;
- question presentation.

The learner should not be able to pass by recognizing an answer pattern.

---

# 3. Required attempt sequence

For tracing exercises:

```text
PREDICT BY HAND
→ commit answer
→ RUN / REVEAL
→ explain mismatch
→ MODIFY
→ PREDICT AGAIN
```

For design/test exercises:

```text
READ SPEC
→ propose tests/design
→ commit answer
→ reveal implementation/reference
→ critique
→ transfer variant
```

For architecture exercises:

```text
CLOSE REPO
→ draw from memory
→ commit diagram
→ compare
→ identify missing links
→ record gaps
```

---

# 4. Evaluation

Do not grade only the final value.

Evaluate:
- execution order;
- state tracking;
- data representation;
- reason for branches;
- assumptions;
- explanation of the general principle.

A lucky final answer is not a pass.

---

# 5. Mastery

A concept needs:

```text
3 unseen correct variants
across >= 2 contexts
including >= 1 delayed retrieval
plus correct explanation
```

Before then, use:
- NEW;
- DEVELOPING;
- RETRIEVAL-DUE;
- TRANSFER-DUE.

Only then:
- MASTERED.

---

# 6. Misconceptions

Record the concept, not the literal wrong answer.

Good:
```text
alias_vs_copy
missing_vs_null
caller_vs_callee
event_ordering
client_claim_vs_server_authority
idempotency_key_identity
transaction_atomicity
```

Bad:
```text
answered 14 instead of 17
```

Future tests should target the misconception with different surface forms.

---

# 7. Mandatory pauses

During implementation:

- Predict → Run → Modify → Predict: every phase through Phase 8.
- Tests before implementation tests: once per behavior-adding phase.
- Teach one file aloud: after every meaningful module and at least weekly.
- Architecture reset: every 7 days of active work or before major phase transition.

Do not silently skip a pause because the patch seems small.

---

# 8. Reference-project mining

Before generating from Argos, Datum, Trellis, or another repo:

1. identify current phase;
2. identify academic learning objective;
3. inspect current source if available;
4. isolate one concept;
5. simplify unrelated framework/domain complexity;
6. generate a related but different exercise;
7. provide a second transfer context;
8. record repo/commit/file only after the attempt, unless the source itself is the object of the teaching exercise.

---

# 9. Assistance fading

Early:
Claude demonstrates decomposition.

Middle:
Claude asks leading questions but the learner proposes contracts and modules.

Late:
Claude stops proposing the architecture first and acts as reviewer/examiner.

Final:
Claude challenges decisions and unfamiliar code.

If Claude supplies the key design term before the learner has tried to identify the problem, it has over-helped.

---

# 10. No premature architecture

Do not create final-state directories or frameworks before their lifecycle phase.

Complexity is earned.

The Git history should show why each abstraction appeared.


# 11. Collaborative editing invariant

When Phase 13 is reached, Claude must preserve this rule:

> Human and Claude edits are distinct provenance streams and no managed path may silently discard either stream.

The exercise generator should test the architecture with different-looking scenarios:

- same file, different hunks;
- same hunk, different edits;
- stale editor buffer;
- delete vs edit;
- rename vs edit;
- shell mutation only discovered at Stop;
- crash during publication.

The learner must distinguish:

```text
physical isolation
logical conflict detection
atomic publication
```

Do not accept "we use locks" as a complete explanation.

A late mastery gate must require the learner to defend why separate worktrees + version checks + three-way merge were chosen over a shared worktree with last-write-wins.


# 12. No-silent-overwrite mastery gate

Collaborative editing is not mastered until the learner can correctly reason about all seven layers:

```text
1. worktree isolation
2. expected-version hash
3. current merge base
4. three-way reconciliation
5. explicit conflict state
6. atomic file publication
7. crash recovery / rescan
```

A correct answer that says only "use Git" or "use file locks" is insufficient.

Late variants must include:
- exact-line conflict;
- non-overlapping clean merge;
- stale human buffer;
- shell-only Claude edit;
- interrupted Claude turn;
- crash after file replace but before metadata commit;
- advancing merge base.

The learner must state which layer handles each failure.


# 13. Implementation-adjacent learning

The current implementation phase determines when adjacent concepts are introduced.

For every meaningful new syntax form, representation, standard-library mechanism, external boundary, failure mode, or design decision:

```text
1. name the concrete BuildLens task that needs it;
2. identify the smallest underlying concept needed now;
3. make the learner predict/trace/reason before explanation;
4. apply the concept to the real code;
5. give one different-looking transfer;
6. record exact evidence in LEARNING_LEDGER.md;
7. continue building.
```

Adjacent learning is justified only when it explains something the learner must **read, represent, cross, fail, verify, or defend now**. Otherwise defer it.

Do not front-load operating systems, databases, networking, or architecture simply because they matter eventually.

## Spiral-depth rule

Revisit concepts at greater depth:

```text
recognize → trace → apply → transfer → defend
```

Do not repeat the same quiz.

## Evidence rule

Every formal BuildLens exercise preserves the exact prompt and exact first committed learner answer. Corrections never overwrite historical evidence.


# 14. Adaptive remediation after an incorrect answer

Incorrect answers are expected learning evidence.

Do **not** treat a wrong answer as a reason to immediately present another problem at the same complexity.

The remediation goal is:

> Find the smallest missing mental model, practice it in isolation, then rebuild the original complexity one step at a time.

This follows the instructional pattern:

```text
scaffolding
→ coaching
→ fading
→ independent transfer
```

## 14.1 Preserve before teaching

Before remediation:

1. preserve the exact failed problem in the Evidence Record;
2. preserve the learner's first committed answer verbatim;
3. preserve their reasoning verbatim when supplied;
4. mark the result `wrong` or `partial`;
5. identify **one primary blocker** for the next remediation step.

Do not rewrite the historical answer into a cleaner version.

## 14.2 Diagnose the blocker, not just the wrong value

Possible blocker categories include:

```text
SYNTAX_READING
EXECUTION_ORDER
ASSIGNMENT_UPDATE
STRING_INDEXING
OPERATOR_MEANING
CONDITION_EVALUATION
BRANCH_SELECTION
PARAMETER_ARGUMENT
LOCAL_VS_OUTER_STATE
RETURN_VALUE
FUNCTION_CALL_FLOW
LOOP_ITERATION
MUTATION_ALIASING
DATA_REPRESENTATION
BOUNDARY_CONCEPT
OTHER
```

A single attempt may expose several weaknesses, but remediation should usually target **one** first.

## 14.3 Remediation simplicity ladder

Use the lowest rung that isolates the blocker.

```text
R0 — READ ONE SYNTAX FORM
     one token / expression / notation
     no tracing composition

R1 — ONE OPERATION
     one input/value + one operation

R2 — TWO OR THREE SEQUENTIAL STEPS
     no branch, no function call

R3 — ONE CONTROL CHOICE
     one `if` or `if/else`
     no function call unless the function itself is the target

R4 — ONE FUNCTION CALL
     parameters + local state + return
     no branch unless branch behavior is already secure

R5 — ONE FUNCTION + ONE BRANCH
     no nested calls, no loop, trivial arithmetic

R6 — COMPOSITION
     multiple calls, loop, state interaction, or the current phase target
```

Examples:

```text
failed: function + branch + two calls

if blocker = STRING_INDEXING
→ R0: `word = "Hi"`; what does `word[-1]` select?

if blocker = BRANCH_SELECTION
→ R3: one number + one `if/else`, no function

if blocker = RETURN_VALUE
→ R4: one tiny function with one return and no branch
```

If the learner says:

> "I do not know how to read this syntax"

immediately move to `R0` for that syntax.

Do not test the larger algorithm while the syntax itself is unreadable.

## 14.4 Reduce cognitive noise

A remediation problem should contain:

- one target concept;
- familiar vocabulary;
- small numbers;
- trivial arithmetic unless arithmetic is the target;
- minimal lines;
- minimal nesting;
- no unrelated framework/library syntax;
- at most one unfamiliar syntax form.

When simplifying, remove unrelated difficulty such as:

```text
nested calls
extra branches
loops
mutation
large numbers
multiple outputs
domain terminology
type annotations
framework syntax
```

unless one of those is the actual target.

## 14.5 Wrong again → simplify again

If the learner misses the remediation problem:

```text
do not repeat the same level with different numbers
→ descend another rung
→ isolate the smaller prerequisite
```

Repeated errors are a signal that the current representation is still too complex.

They are **not** evidence that the learner needs a longer explanation of the same hard problem.

## 14.6 Worked-example rescue mode

If the learner remains stuck after simplification, switch temporarily to a worked-example scaffold.

Use this sequence:

```text
A. show ONE solved neighboring example
B. ask the learner to explain each step in their own words
C. give a partially scaffolded example with one missing step
D. give a fresh micro-problem with no answer shown
```

The worked example must be structurally related but must **not** reveal the answer to an unanswered active problem.

The learner still performs retrieval after seeing the model.

## 14.7 Climb back up gradually

After a correct remediation answer:

```text
correct prediction
+ correct explanation
→ one fresh near-transfer at the same rung
→ if correct, move up exactly one rung
```

Do not jump directly from `R1` back to `R6`.

Reintroduce one source of complexity at a time.

Example:

```text
one `if`
→ one function
→ one function + one `if`
→ two calls
```

If the learner fails during the climb, move back to the last stable rung.

## 14.8 Fade support after success

Scaffolding is temporary.

Once the learner demonstrates stability:

- remove fill-in-the-blank state tables;
- remove guiding questions;
- reduce syntax reminders;
- use a different surface form;
- return to the phase's intended gate.

Do not make the learner dependent on permanent hints.

## 14.9 No penalty loop

There is no maximum number of wrong attempts.

Do not say a phase is failed because the learner needs many remediation steps.

Track:

```text
where the learner started
what rung became stable
what misconception changed
whether the learner returned to the target rung
```

The learning objective is mastery, not a low attempt count.

## 14.10 Recovery criterion

A failed target problem is considered remediated only when the learner can:

```text
solve the isolated prerequisite
→ solve a fresh near-transfer
→ climb back to the original complexity
→ solve a fresh target-level variant
→ explain the underlying principle
```

The original failed answer remains in the ledger forever as evidence of progression.

---

# 15. University source ladder

Academic exercises should preferentially follow:

```text
current BuildLens phase
→ current implementation trigger
→ one appropriate CMU/MIT source objective
→ new micro-problem
→ BuildLens application
→ different-looking transfer context
```

For each exercise, record:

```text
BUILD PHASE
IMPLEMENTATION TRIGGER
ACADEMIC SOURCE
DEEP SKILL
BUILDLENS EXERCISE
TRANSFER
```

Use the smallest number of authoritative sources necessary. The source defines the deep skill, difficulty, reasoning style, and important invariants. It is not a fixed question bank.

Never copy university homework or exam questions verbatim. Do not require the learner to complete an entire university course. Extract only the smallest relevant material that the current BuildLens implementation can make concrete. If material is login-restricted, do not fabricate it; use public objectives or an appropriate public archive/OCW source and record the limitation in `docs/LEARNING_SOURCES.md`.

# 16. Cumulative retrieval counters

Maintain two independent completion counters.

## 16.1 Smaller/foundation phases

Baseline: Phases 0–6. After every three completed smaller/foundation phases, stop before significant work in the next phase and run one cumulative retrieval review.

Phase 2 completion triggers the first review of important Phase 0–2 material before substantial Phase 3 implementation. The current repository may already be beyond that transition; preserve its history rather than rewriting it.

## 16.2 Major/deep phases

Baseline: Phases 7–15. After every two completed major/deep phases, stop before significant work in the next phase and run one cumulative retrieval review.

Classify by actual conceptual weight, not phase number alone. Record why when a nominally small phase becomes architecturally deep. Splitting a major phase into administrative subphases does not inflate the counter.

## 16.3 Review construction

Prioritize:

1. concepts required by later phases;
2. deep architectural concepts;
3. prior misconceptions and remediation targets;
4. concepts not retrieved recently;
5. state/authority boundaries;
6. testing/debugging reasoning;
7. major algorithm/data-structure choices;
8. AI/system concepts after Phase 8.

Mix only already-taught question types:

```text
TRACE
EXPLAIN
APPLY
TEST / CONTRACT
DEBUG
ARCHITECTURE
DEFEND
```

A normal review is approximately 4–7 questions; a deep review is approximately 6–10 questions. Short related subparts are allowed. Do not turn every review into a final exam.

Use delayed retrieval: the same deep concept, a different surface, a time delay, and when useful a different domain. Do not merely repeat old questions.

All adaptive R0–R6 remediation rules remain active. Several remediation attempts do not fail the entire review, but the review is not complete until each important concept is independently recovered at the cumulative level.

## 16.4 Evidence and reset

Every cumulative question creates an Evidence Record in `learning/LEARNING_LEDGER.md` with exercise type `CUMULATIVE_RETRIEVAL` and records:

```text
exact problem
exact learner answer
exact reasoning when supplied
confidence
result
misconception
source phases
academic source
remediation chain
delayed retrieval status
transfer context
```

After a successful review, reset only the counter that triggered it; never erase history. If both counters become due at approximately the same time, run one combined review and reset both satisfied counters.

An additional review may be required before a major architecture transition when earlier knowledge is genuinely prerequisite. Use this sparingly. Phase 15 always includes a cumulative final defense regardless of counter state.

# 17. AI readiness as cumulative knowledge

Beginning in Phase 8, treat LLM and AI concepts as cumulative retrieval targets alongside the existing software and systems curriculum. The learner must progressively distinguish model output, tool proposals, authoritative application state, memory, retrieval/RAG, evaluation, guardrails, and observability.

Do not prebuild or pre-teach framework-specific machinery merely because the CMU target program uses it. CrewAI, LangGraph, vector databases, and similar tools remain deferred until a concrete BuildLens phase creates a justified need.
