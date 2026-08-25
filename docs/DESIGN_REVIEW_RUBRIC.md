# BuildLens — Design Review & Oral Defense Rubric

## Purpose

Berkeley CS162 design reviews explicitly require students to know their own design document, discuss why they made design decisions, and reason about testing/edge cases.

BuildLens uses the same basic idea throughout the project.

A design is not "owned" until you can defend it without Claude speaking for you.

---

# How a Strong Engineering Defense Should Sound

The goal is **not** to recite an ADR template.

The goal is to sound like an engineer explaining a real decision to another engineer.

Online engineering write-ups and experienced-developer discussions repeatedly use a similar conversational shape:

```text
CONTEXT
"The thing that mattered here was ..."

ALTERNATIVES
"I considered ..."

CHOICE + MECHANISM
"I went with ... because it gives us ... by ..."

COST
"The downside is ..."

EVIDENCE
"We checked / measured / tested ..."

BOUNDARY
"I would revisit it if ..."
```

This is consistent with Berkeley CS162's design-review standard: convince the reviewer that the design satisfies the requirements and edge cases, explain why it is better than alternatives, acknowledge shortcomings, and reason about complexity/extensibility.

It also matches CMU ATAM's architecture reasoning:

```text
stimulus / requirement
→ architectural mechanism
→ measurable response
→ sensitivity / tradeoff
```

## The default spoken form

For a 30–60 second answer, prefer:

> **"Given [actual constraint], I optimized for [important quality]. I considered [credible alternative], but chose [decision] because [specific mechanism]. The tradeoff is [real downside], which was acceptable because [current condition]. I validated that with [test/measurement/evidence]. If [specific requirement changes], I'd revisit it."**

Do not memorize the exact sentence. Memorize the reasoning order.

## Better wording habits

Prefer:

> "For this workload, I chose..."

over:

> "X is better."

Prefer:

> "The failure I was trying to prevent was..."

over:

> "This is more reliable."

Prefer:

> "The mechanism is..."

over:

> "It scales."

Prefer:

> "I accepted..."

over pretending there was no downside.

Prefer:

> "At our current scale..."

over claiming the decision is universally correct.

Prefer:

> "I don't have evidence for that yet; I would measure..."

over inventing certainty.

## Start short, then drill down

Do not give a ten-minute monologue to a one-line question.

Use layers:

```text
30 sec
constraint → choice → reason → tradeoff

then if challenged:
mechanism

then:
evidence / test

then:
failure / edge case

then:
counterfactual / reversal condition
```

A good interviewer can pull you deeper.

Your job is to have depth available.

---

# Real-World Defense Patterns to Practice

These examples are **new BuildLens examples inspired by the reasoning style** in public engineering write-ups and practitioner discussions; they are not copied answers.

## Pattern A — The workload changed

Public engineering write-ups often explain a decision as appropriate for one phase and wrong for another.

Practice answer:

> "The initial version optimized for getting the workflow working quickly, so the simpler storage choice was reasonable. Once the data became strongly relational and we needed constraints and multi-record transactions, that assumption changed. I moved to the relational design because the database could enforce invariants we were otherwise rebuilding in application code. The cost was a migration and stricter schema management. If the workload were still independent documents with few relationships, I wouldn't claim the migration was automatically better."

What makes this strong:

```text
decision is contextual
requirements changed
mechanism is named
migration cost is admitted
alternative remains legitimate
```

## Pattern B — Start from the failure

Practitioners often explain architecture more convincingly by naming the failure they refused to accept.

BuildLens example:

> "I didn't let Claude and the human editor write into one physical worktree because the failure I cared about was a lost update that looked successful. Separate worktrees remove the physical write race; version hashes and a three-way merge handle the logical concurrency problem. That adds reconciliation complexity, which I accepted because silent source loss is worse. I'd revisit it if the editor/agent platform eventually exposed one authoritative transactional document model with equivalent conflict guarantees."

Notice that this does **not** say:

> "Worktrees are best practice."

It says what failure drove the design and how the mechanism addresses it.

## Pattern C — The boring solution is sufficient

Experienced engineers often defend simplicity by stating the requirement that makes additional infrastructure unnecessary.

BuildLens example:

> "I kept persistence local with SQLite because BuildLens is initially a single-user local application and the state we need is relational session/history data. PostgreSQL would work, but it would add a server, credentials, deployment, and operational failure modes without solving a current requirement. The tradeoff is that SQLite isn't the architecture I'd choose for many remote concurrent writers. If BuildLens becomes a shared multi-user service, that is a clear trigger to revisit the storage layer."

## Pattern D — Initial instinct rejected by concrete requirements

Strong engineering posts often start with the obvious technology, then show which requirements it failed.

Practice answer:

> "My first thought was a bidirectional socket because the UI is live. But most BuildLens updates are service-to-viewer events; editing commands are explicit request/response operations. Starting with one-way streaming plus ordinary save/reconcile requests keeps the protocol and recovery model simpler. The cost is that if we later need genuinely bidirectional low-latency collaboration semantics, we'd need to revisit the transport."

## Pattern E — Defending a decision you inherited

If you were **not** the original decision-maker, never fabricate ownership.

Use:

> "I didn't make the original choice, so I wouldn't claim its original rationale. What I can explain is why I kept it when I worked on the system: under the constraints I saw, X still gave us Y, while changing to Z would have cost A without addressing an observed problem. If I were making the decision fresh today, I'd verify B and C before keeping it."

This is much stronger than inventing a historical reason.

---

# The Five Challenge Rounds

For important choices, Claude should not stop after "why?"

## Round 1 — Requirement

> "Which requirement or constraint actually made this decision matter?"

## Round 2 — Mechanism

> "How does your choice technically produce the property you claim?"

## Round 3 — Alternative

> "Make the strongest case for the option you rejected."

## Round 4 — Evidence / Failure

> "What test, measurement, incident, or code invariant supports your claim? What happens when it fails?"

## Round 5 — Counterfactual

> "What would have to become true for you to change your mind?"

If the learner can answer all five, the decision is probably understood rather than memorized.

---

# Review Modes

## 1. Micro Review — 5 minutes

After a small patch.

Answer:

```text
What changed?
Why?
What input/output changed?
What test proves it?
What remains unchanged?
```

## 2. File Review — 10 minutes

Pick one file.

Explain:

```text
responsibility
dependencies
callers
state
important branches
failure modes
design assumptions
```

## 3. Feature Review — 15 minutes

Trace:

```text
user/event
→ entrypoint
→ domain logic
→ persistence/external system
→ response/UI
```

Then defend one choice.

## 4. Architecture Review — 20–30 minutes

No code initially.

Draw:
- module view;
- runtime view;
- data/state flow;
- deployment view;
- failure path.

Then open code and verify.

---

# Rubric

Score each dimension 0–3.

## A. Behavior

**0** Cannot state what the feature does.  
**1** Gives a vague product summary.  
**2** Correctly describes normal behavior.  
**3** Describes normal + boundary/failure behavior precisely.

## B. Execution

**0** Cannot trace code.  
**1** Knows files but not call order.  
**2** Traces main call chain.  
**3** Traces calls, branches, representations, and return path.

## C. State / Authority

**0** Does not know where truth lives.  
**1** Names storage but not ownership rules.  
**2** Identifies state owner and mutations.  
**3** Explains invariants, stale/concurrent behavior, and authority boundaries.

## D. Tests

**0** "Tests pass."  
**1** Can name existing test.  
**2** Can design normal + edge test.  
**3** Can explain which assumption each test attacks and identify missing coverage.

## E. Failure

**0** Only happy path.  
**1** Names generic exception.  
**2** Traces a concrete failure.  
**3** Explains partial state, retry, user impact, logging/evidence, and recovery.

## F. Design Decision

**0** "Claude chose it" / generic technology slogan.  
**1** Names a choice and a plausible reason.  
**2** Connects a real requirement/constraint to the choice and volunteers a downside.  
**3** Fairly compares alternatives, explains the causal mechanism, cites evidence/measurement, identifies the important failure/tradeoff, and gives a concrete reversal condition.

## G. Systems Depth

**0** Framework magic.  
**1** Knows another process/network/database exists.  
**2** Explains representation/process/network/persistence boundaries correctly.  
**3** Can connect application behavior to bytes/processes/threads/memory/I/O/network/persistence/concurrency/performance at the appropriate level, while clearly stating what has and has not been verified.

## H. Communication

**0** Cannot organize explanation.  
**1** Correct facts but scattered.  
**2** Clear ordered explanation.  
**3** Adjusts depth, answers challenges directly, and says what is uncertain instead of bluffing.


## I. Security / Trust

**0** Treats every input/component as equally trusted.  
**1** Recognizes an external input.  
**2** Identifies validation/authorization/authority boundaries.  
**3** Explains when data becomes trusted, what decisions it may influence, what could leak if checks happen late, and how the design limits authority.

## J. Operability / Evidence

**0** Can only reason from source code.  
**1** Says "check the logs."  
**2** Identifies useful runtime state/log/metric/test evidence.  
**3** Explains how a new engineer would diagnose the failure, correlate events, distinguish symptom from cause, and recover safely.

---

# Passing Standard

Early project:

```text
mostly 1–2
no zero in Behavior or Execution
```

Middle project:

```text
mostly 2
no zeros
```

Late project:

```text
mostly 2–3
Design Decision / Failure / State ≥ 2
```

Final interview mode:

```text
all applicable dimensions ≥ 2
at least five dimensions = 3

Design Decision must be ≥ 3 for any major architectural choice being defended.
```

---

# Adversarial Questions

Claude should gradually introduce questions such as:

```text
What requirement drove this?
Why is this function here instead of the caller?
Why not combine these modules?
What makes this value authoritative?
What exact mechanism gives you the property you're claiming?
What happens if this call runs twice?
What happens if it times out after the remote side succeeded?
What happens if it dies halfway through?
Which test would fail if your assumption were wrong?
What runtime evidence would tell you what happened?
What would 10× load change?
Is the bottleneck algorithmic, CPU, memory, I/O, network, or database?
Why this database?
Why not the simpler alternative?
Why not a queue?
Why not a shared worktree?
Where exactly is this invariant enforced?
What is the strongest argument against your design?
What would have to be true for the rejected option to win?
What would make you reverse this architecture?
```

The goal is not to "win" against the interviewer.

The goal is to make the reasoning explicit.

---

# Counterargument Round

For every important ADR:

Round 1:
> Defend the chosen design in 45 seconds.

Round 2:
> Explain the mechanism: why does it actually produce the claimed quality?

Round 3:
> Make the strongest case against it.

Round 4:
> Name the evidence you have — test, measurement, invariant, incident, or current workload.

Round 5:
> State the exact requirement/constraint change that would make the alternative better.

This trains strong but conditional engineering opinions rather than technology loyalty.

---

# Code Review Interview Mode

Recent practitioner discussions increasingly describe code review/debugging as a useful interview format in the AI-coding era. Treat that as anecdotal industry input.

Claude provides unfamiliar code containing several classes of issue:

```text
correctness
missing edge case
bad authority boundary
unnecessary abstraction
performance issue
weak test
failure-handling issue
```

You narrate priorities and recommendations aloud.

Do not optimize for spotting the greatest number of style nits.

Optimize for:
- severity;
- reasoning;
- evidence;
- communication.
