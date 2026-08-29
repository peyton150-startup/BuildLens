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

Last published quiz commit before this handoff: `a444efa` on `main`. The ordinary workspace is not
the publishing clone; use the verified temporary-clone workflow documented in the existing project
state when the learner asks to push.

## Latest pause — lunch, 2026-08-29

The learner requested three final super-hard questions before finishing Phase 3. Question 1 was
partial and its short recovery passed. Question 2 (`EV-P1-COMPOSE-174`) failed because `.sort()` was
treated as non-mutating and list-returning under heavy composition. On return, give one short
`.sort()` versus `sorted()` checkpoint and one alias near-transfer, then ask super-hard question 3
of 3. Do not skip the recovery, and do not begin Phase 3 yet.
