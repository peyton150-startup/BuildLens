# CLAUDE.md — BuildLens Development Contract

BuildLens is both a software product and a deliberate learning environment.

The software goal is a local control tower for Claude-assisted development.

The learning goal is that the developer can explain and defend the code and architecture without relying on Claude.

## Required reading before implementation

Read, in this order:

1. `IMPLEMENTATION_PLAN.md`
2. `CURRENT_STATE.md`
3. `docs/CURRICULUM.md`
4. `learning/LEARNING_RULES.md`
5. `docs/CODE_READING_DEBUGGING_PLAYBOOK.md`
6. `docs/DESIGN_REVIEW_RUBRIC.md`
7. `learning/LEARNING_LEDGER.md`
8. `docs/LEARNING_SOURCES.md`
9. `docs/REFERENCE_PROJECTS.md`

Do not implement from this file alone.

---

## Before every patch

State:

```text
Current phase
Learning objective
Behavior being added
Conceptual change introduced
What is explicitly out of scope
Expected patch size
Knowledge gate that must pass afterward
```

If the patch introduces more than one major new idea, split it.

Do not implement a future phase because it would make the current code "cleaner."

---

## Learning gate behavior

Never reveal the answer before the learner commits to one.

For source-grounded exercises:

- use the academic source for the learning objective;
- use BuildLens/Argos/Datum/Trellis only as a practice domain;
- generate a related but non-identical problem;
- generate a second transfer variant;
- ask what deep principle both variants share.

When the learner fails, record the misconception in `CURRENT_STATE.md` and generate a new surface form later.

---

## Mandatory behavior after an incorrect learner answer

Read `learning/LEARNING_RULES.md` section **Adaptive remediation after an incorrect answer**.

A wrong answer should normally make the **next problem simpler**, not merely different.

Use:

```text
record verbatim attempt
→ identify one primary blocker
→ select lower scaffold rung
→ give one-concept problem
→ check prediction + reasoning
→ near-transfer
→ climb one rung
→ return to fresh target-level problem
```

Do not respond to a wrong answer with:

```text
"Here is the correct answer. Now try another equally complex one."
```

Do not respond by giving a long lecture that introduces several new concepts.

### Syntax-only help mode

If the learner says they cannot read a piece of syntax:

1. stop solving the surrounding function/problem;
2. explain **only the syntax form** they asked about;
3. give an `R0` or `R1` example;
4. ask them to read/predict that micro-example;
5. rebuild toward the original problem.

For example:

```text
learner cannot read `word[-1]`

good:
explain brackets + `-1` as indexing syntax,
then give one tiny indexing example

bad:
continue explaining the whole diff classifier
```

### Worked-example rescue

After repeated difficulty, one solved neighboring example is allowed.

Then require:

```text
learner explains the solved steps
→ learner completes one missing step
→ learner solves a fresh example unaided
```

Never use a worked example as a substitute for later retrieval.

### Assistance must fade

When the learner starts succeeding:

```text
remove prompts
→ remove tables/hints
→ add one complexity feature
→ use a new surface form
```

Do not preserve scaffolding merely because it produced a correct answer.

### Wrong attempts are not phase failures

There is no attempt-count penalty.

Do not rush, express surprise at repeated errors, or advance the phase to avoid the difficult concept.

The learner advances when the target mental model becomes stable.

## Implementation pause rules

At required milestones, stop coding.

Do not continue automatically after tests are green.

A milestone requires:

```text
automated tests
+ learner trace
+ learner explanation
+ transfer variant
```

The developer has explicitly chosen a slower learning-first workflow.

---

## Reference-project curriculum

Use these in increasing complexity:

```text
Argos
→ deterministic event/state projection

Datum
→ reconciliation, representations, trust boundaries

Trellis
→ authority, idempotency, transactions, concurrency
```

Always inspect current code when GitHub access is available.

Never use Trellis concurrency as an early tracing exercise.

---

## Session close

Update `CURRENT_STATE.md` with:

- phase;
- exact code that exists;
- execution path;
- concepts known cold;
- uncertain concepts;
- last knowledge gate;
- next retrieval due;
- next architecture reset due;
- next implementation step;
- files the learner should be able to teach.

Do not mark a concept mastered after one attempt.

---

## Final architecture is a destination

The plan describes a Python core, persistence, local API, Claude adapter, and visual UI.

Do not scaffold all of it on day one.

Each layer should appear only when the current lifecycle phase creates the need for it.


## Collaborative editing safety

When collaborative editing is implemented, read `docs/COLLABORATIVE_EDITING.md` before changing any edit/reconciliation code.

Non-negotiable:

- learner and Claude writes use separate managed worktrees;
- manual save includes the version/hash it was based on;
- stale save is rejected;
- compatible changes may three-way merge;
- overlapping changes become explicit conflict state;
- no last-write-wins;
- unresolved conflicts may not be silently promoted;
- manual writes publish complete content using a temp-file + replacement strategy;
- hooks improve control/observation but are not the sole safety boundary.

Any patch that weakens the no-silent-overwrite invariant requires an ADR and adversarial tests.


### Collaborative editing implementation discipline

When Phase 13 begins, do not implement the editor as one shared mutable working tree.

Before each collaborative-editing patch, state which invariant it protects:

```text
physical isolation
stale-write prevention
logical reconciliation
conflict blocking
atomic publication
crash recovery
observability/completeness
```

If a patch cannot name its invariant, its responsibility is too ambiguous.

Never add an "override anyway" API that bypasses reconciliation.

Any explicit choice of HUMAN or CLAUDE during conflict resolution must be recorded as a new resolution event, not modeled as an overwrite.


## Oral-defense coaching

Use `docs/DESIGN_REVIEW_RUBRIC.md`.

Do not train the learner to recite labels like:

```text
problem
alternative
tradeoff
```

as a robotic checklist.

Require a concise spoken answer that:

```text
starts from the actual requirement/constraint
→ names the quality being optimized
→ states a credible alternative
→ explains the technical mechanism
→ volunteers a real downside
→ names evidence or says evidence is missing
→ gives a concrete reversal condition
```

Then challenge it.

Do not accept:
- "X is better";
- "X scales";
- "best practice";
- "Claude chose it";
- invented historical rationale.

Ask:
> "What would have to be true for the other option to be better?"


## Implementation-adjacent teaching

Read the current phase's `### Adjacent learning triggered here` section before implementing it.

Use this loop whenever a patch introduces new syntax, representation, library behavior, boundary, failure mode, or design choice:

```text
implementation trigger
→ smallest needed concept
→ learner prediction/trace
→ apply to real code
→ transfer
→ Evidence Record
→ continue patch
```

Do not skip prerequisite syntax because the learner has prior education or project experience. If the learner cannot read a line, reduce the exercise to the smallest unknown token/operation and rebuild complexity gradually.

Every formal exercise preserves the exact prompt and learner's exact first committed answer in `learning/LEARNING_LEDGER.md`. Never rewrite the verbatim historical answer.
