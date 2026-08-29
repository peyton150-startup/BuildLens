# HANDOFF — Continue the Fundamentals Quiz

Read `CLAUDE.md`, `CURRENT_STATE.md`, and the end of `QUIZZES.md` before continuing.
`CURRENT_STATE.md` is authoritative; this is only a quick starting point.

## Scope

Continue quizzing the learner only on completed **Phases 0, 1, and 2**. Focus on Python and
BuildLens fundamentals. Do not quiz Phase 3, begin Phase 4, or change product code.

Ask one question at a time. Require a confidence score from 0–100, let the learner commit before
revealing the answer, and adapt down only when a genuine conceptual gap appears. Do not penalize
spelling, missing spaces in displayed lists, capitalization typos, or other harmless formatting.
The learner has explicitly asked for harder questions and less nitpicking.

For harder questions, use a small ASCII picture or state diagram when it materially helps, especially
for aliases and mutation. Do not let the picture reveal the answer before the learner predicts it.

## Current understanding

The learner is strong on:

- output versus return values, including implicit `None`;
- exit status versus terminal output;
- list mutation, `.sort()` versus `sorted()`, and mutator return values;
- longest-prefix-first branch precedence;
- diff-line classification and summary accumulators;
- local accumulator reset across separate function calls;
- dictionary key/value lookup and shared mutation through aliases.

Recent recovery: the learner correctly traced two updates through three names pointing to one shared
dictionary. They also correctly explained that mutating an external counter makes a function impure,
while using a fresh local counter can be pure.

## Resume here

Begin with one moderately difficult, unfamiliar **state-tracing problem** that combines two or three
already-learned ideas. Ask for the state after each line and the final returned/printed value. A good
target combines aliasing, dictionary or list mutation, a local variable, and a return value without
introducing new syntax.

If correct, remove the table or diagram on the next problem. Later, retrieve purity in a different
domain and require the learner to inspect every object a function can change—not only its explicit
input. Per-item branch enumeration is also still worth testing: require one answer per input rather
than accepting a group-level answer.

The learner has said that adding one extra state-changing step can make them lose track even when
each individual rule is understood. Treat that as a composition-tracking issue. Freeze state line by
line, then fade that support after success instead of restarting basic syntax drills.

## Recording and close

Append every formal prompt and the learner's verbatim first committed answer to
`learning/LEARNING_LEDGER.md`; also append the readable transcript to `QUIZZES.md` and update
`CURRENT_STATE.md`. Follow the session-close and publishing rules in `CLAUDE.md`.

Last published quiz commit reported before this session: `6d4ff74` on `main`. The ordinary workspace is not
the publishing clone; use the verified temporary-clone workflow documented in the existing project
state when the learner asks to push.

## Latest pause — lunch, 2026-08-29

The learner requested three final super-hard questions before finishing Phase 3. Question 1 was
partial and its short recovery passed. Question 2 (`EV-P1-COMPOSE-174`) failed because `.sort()` was
treated as non-mutating and list-returning under heavy composition. On return, give one short
`.sort()` versus `sorted()` checkpoint and one alias near-transfer, then ask super-hard question 3
of 3. Do not skip the recovery, and do not begin Phase 3 yet.

## Latest pause — location change, 2026-08-29

The `.sort()`/`sorted()` checkpoint and alias near-transfer both passed. Super-hard question 3
(`EV-P1-COMPOSE-177`) was partial and entered remediation. The learner recovered routing, cumulative
counters, the correct sorted ticket order, second-call labels, core returned state, and the principle
that several names can point to one mutable object.

The remaining primary blocker is whole-program list-object counting. The learner counted elements
inside the returned outer list instead of counting the original input, local lists, and outer list
as separate objects. A worked-example rescue was shown:

```python
base = [1]
inner = []
wrapper = [inner, None]
```

The learner left before explaining it. Resume with exactly one prompt:

> In your own words, why is the count three rather than one or four?

Then require the learner to complete one missing allocation step and solve a fresh micro-example
before returning to the BuildLens first-call count. Do not reveal the BuildLens total first. After
object counting recovers, finish the impurity inventory: passed-list mutation, shared counter
mutation, and output through the called `route` function. Super-hard question 3 and its recovery are
not complete; do not advance Phase 3.

## Review completion update — 2026-08-29

The location-change resume sequence is complete. The learner explained the worked example, passed a
missing-step check, passed a fresh independent transfer, and recovered the BuildLens whole-program
count of seven list objects. They also completed the impurity inventory: passed-list mutation,
passed-dictionary mutation, and terminal output inherited through the called `route` function.

All three requested super-hard questions and their remediation chains are now complete. Do not
restart this review or mark its concepts permanently mastered. Before implementation, read the
authoritative current phase/task and cumulative-review counters in `CURRENT_STATE.md` and
`learning/LEARNING_RULES.md`, then present the learner with the exact next BuildLens step and its
required knowledge gate.

## Exact next BuildLens step

Phase 2 implementation is already complete. Phase 3 `Session` code, five automated tests, state
movie, and knowledge gate are complete, but its milestone still owes:

```text
learner explanation  — teach session.py in their own words
transfer variant     — fresh alias/copy problem outside the session domain
```

Resume with the `session.py` teach-back, not Phase 2 implementation and not Phase 4 code. Require the
learner to explain ownership, ordered mutation through `record`, snapshot creation through
`list(self.changes)`, why the returned list cannot mutate the session, the remaining public-attribute
limitation, and the leak test that proves copying matters. Then give one unrelated transfer. Only
after both pass may Phase 4 planning begin.

The just-completed fundamentals review was not historically tagged `CUMULATIVE_RETRIEVAL`. Do not
retroactively rewrite its exercise types or silently reset a formal counter. Audit the counter before
substantial Phase 4 work and combine any due review with the milestone where possible.

## Counter audit result

Phase 3 is complete, including teach-back and unrelated transfer. The foundation counter remains due
because no previous question was recorded with exercise type `CUMULATIVE_RETRIEVAL`; do not
retroactively relabel attempts. Before Phase 4 code, run four formal questions: classification
debug/test, return/output/local-state trace, summary contract/boundary apply, and an architecture
defense. Use the fourth as the pre-Phase-4 architecture reset. Avoid alias/snapshot/purity repetition.
Reset only the foundation counter after all four pass.

## Latest pause — moving locations, cumulative checkpoint

The concise replace-in-place `CURRENT_STATE.md` cleanup is complete. Formal cumulative questions 1–3
are complete:

```text
Q1 classifier debug/test       passed after leading-space recovery
Q2 return/output/local state   passed at confidence 90
Q3 summary contract/boundary   passed after multiline/explicit-return remediation
```

Resume with cumulative question 4 of 4 only. It is the architecture defense and doubles as the
required pre-Phase-4 architecture reset. After it passes, reset only the foundation counter, record
Phase 3 as 1/3 toward the next foundation checkpoint, and begin Phase 4 intent discussion. Do not
repeat question 3 or start product code first.

## Session completion — cumulative checkpoint and Phase 4 handoff

The four-question formal foundation cumulative checkpoint is complete. Question 4 passed after
adaptive remediation at confidence 90. Reset only the Phase 0–2 foundation counter; Phase 3 now
counts as 1/3 toward the next checkpoint after Phase 5. The pre-Phase-4 architecture reset is also
complete.

Current architecture decision: keep `classify.py`, `summarize.py`, `session.py`, and their tests in
the existing flat structure. No observed responsibility currently requires multiple related modules.
The accepted downside is later file moves and import churn. Reconsider packaging when one
responsibility genuinely expands across several related modules or another concrete boundary/import
problem appears.

Start the next session with a brief Phase 4 code-reading audit, not a refactor or a repeated quiz.
Ask the learner to trace `"+tea = 2"` through:

```text
summarize_diff input
→ splitlines()
→ classify_diff_line
→ "added"
→ lines_added increment
→ returned DiffSummary
```

Then ask them to explain the responsibility of each module and confirm that `summarize.py` depends
on `classify.py`. Record the formal Evidence Record before advancing. No quiz is currently open.

## Phase 4 completion update — 2026-08-29

The Phase 4 audit and transfer are complete:

```text
EV-P4-READ-191      cross-module value trace                 passed at confidence 60
EV-P4-ARCH-192      responsibilities/dependency/refactor     passed at confidence 80
EV-P4-TRANSFER-193  unrelated decomposition transfer         passed at confidence 80
```

Decision: keep the existing flat modules. The learner correctly explained that `summarize.py`
depends on `classify.py`, transferred the decomposition to a parcel-manifest domain, and concluded
that possible future work is not present architectural evidence. No product-code patch was earned.

Do not repeat Phase 4 or restructure the project. `CURRENT_STATE.md` is authoritative. Begin Phase 5
with an intent/contract audit. Phases 3 and 4 count as 2/3 toward the next foundation checkpoint;
Phase 5 completion triggers that review before substantial Phase 6 work.

## Phase 5 location-change pause — 2026-08-29

Phase 5 began with `EV-P5-CONTRACT-194`, comparing a documented string contract with runtime
behavior for an integer. The learner initially predicted fallback `"context"`, then completed the
full adaptive chain through method lookup, prefix/suffix reading, assignment/rebinding, branch
execution, function call/return, and validation-versus-operation-failure.

The fresh R5 `classify_tag(12)` target passed at confidence 100 after one omitted-item follow-up. The
learner correctly stated that the docstring enforces nothing; refine their word “annotation” because
a docstring is documentation, while `tag: str` would be a type annotation. Neither validates by
itself in ordinary Python.

Phase 5 is not complete and no product patch is justified. Resume with one BuildLens cross-module
application:

> Without running it, trace `summarize_diff(42)`. Which operation fails first, in which function and
> module? Is `classify_diff_line` ever called? What does this reveal about the boundary contract?
> Confidence: 0–100.

Then provide a different-surface transfer and continue auditing the types/values crossing existing
module boundaries. Do not implement validation or type hints until the learner identifies a concrete
contract ambiguity and proposes the intended behavior.
