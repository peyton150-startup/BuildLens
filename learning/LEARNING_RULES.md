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
