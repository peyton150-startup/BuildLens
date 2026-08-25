# BuildLens — Collaborative Editing Architecture

## 1. Non-negotiable product contract

BuildLens must let the learner:

```text
watch Claude's code changes live
→ see Claude's diff
→ open the same logical source file
→ make a manual edit
→ see the manual diff separately
→ reconcile both change streams
```

And it must guarantee, within the managed workflow:

> **No supported save, merge, or synchronization path silently discards either the learner's or Claude's edit.**

If both actors change the same line or an overlapping merge hunk, BuildLens pauses automatic promotion for that file and requires explicit reconciliation.

There is no last-write-wins path.

---

# 2. What the learner sees

The UI must keep three concepts visually separate.

```text
┌──────────────────── CLAUDE DIFF ────────────────────┐
│ exact additions/removals made in Claude's worktree │
└─────────────────────────────────────────────────────┘

┌──────────────────── HUMAN EDITOR ───────────────────┐
│ editable source + human-only unsaved/saved diff    │
└─────────────────────────────────────────────────────┘

┌────────────────── INTEGRATION RESULT ───────────────┐
│ clean candidate OR explicit BASE/HUMAN/CLAUDE      │
│ conflict view                                      │
└─────────────────────────────────────────────────────┘
```

Every change timeline event names its provenance:

```text
CLAUDE
HUMAN
SYSTEM-MERGE
SYSTEM-CONFLICT
HUMAN-RESOLUTION
```

The learner must never infer ownership from line color alone.

---

# 3. Why separate worktrees

Claude Code Desktop currently uses isolated Git worktrees for Git-backed sessions. Git itself supports multiple linked working trees for one repository.

BuildLens should preserve that isolation.

```text
                    repository
                  /            \
                 /              \
        HUMAN WORKTREE      CLAUDE WORKTREE
```

This solves **physical writer isolation**:

- Claude is not writing over the learner's physical file.
- The learner is not writing over Claude's physical file.
- Both can progress independently until BuildLens reconciles them.

It does **not** solve logical conflicts. That is the job of version checking and three-way merge.

---

# 4. File/version model

Every observed file version records at least:

```text
repo_id
repo_relative_path
worktree_id
git_tip
git_blob_or_none
content_sha256
provenance
observed_sequence
observed_at
```

SHA-256 is used as a deterministic equality/version token, not as a claim that source-code integrity depends on cryptographic collision resistance.

Python `hashlib.file_digest()` may be used for file hashing.

---

# 5. Synchronization state machine

Every logical path has one explicit synchronization state:

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

Automatic promotion is forbidden from:

```text
CONFLICT
STALE_BUFFER
RECOVERY_REQUIRED
```

Typical transitions:

```text
SYNCED
  ├── human save  → HUMAN_CHANGED
  └── Claude edit → CLAUDE_CHANGED

HUMAN_CHANGED + Claude edit
  → reconcile
  ├── clean → BOTH_CHANGED_CLEAN
  └── overlap → CONFLICT

BOTH_CHANGED_CLEAN
  → MERGE_PENDING
  → APPLYING
  → SYNCED

CONFLICT
  → explicit learner resolution
  → MERGE_PENDING
  → APPLYING
  → SYNCED
```

---

# 6. Manual editor: optimistic version check

The editor buffer opens against a specific content hash.

Save request:

```text
path
new_content
expected_hash
human_worktree_id
```

Backend:

```text
current_bytes = read(path)
current_hash  = sha256(current_bytes)

if current_hash != expected_hash:
    return STALE_BUFFER
```

BuildLens must not silently replace the newer file.

Claude Desktop's own file editor warns when a file changed on disk after it was opened. BuildLens keeps that stale-buffer protection but makes reconciliation the normal recovery path rather than a blind override.

Two stale browser/editor tabs are therefore safe: the second save is rejected against the new hash.

---

# 7. Safe publication of one file

Logical conflict detection happens first.

If the version is safe to publish:

```text
1. create temporary file in destination directory
2. write complete bytes
3. flush and close
4. os.replace(temp, destination)
5. re-hash destination
```

Python documents that a successful `os.replace()` is atomic as a POSIX requirement and notes that replacement may fail across filesystems. Therefore the temp file must be created in the destination directory / same filesystem.

Atomic publication solves:

> "Can a reader observe a half-written destination?"

It does not solve:

> "Did human and Claude make incompatible logical edits?"

Those are separate concerns.

---

# 8. Crash-recovery journal

Atomic file replacement does not atomically update BuildLens metadata.

Use a small persisted write-intent record:

```text
WriteIntent
- id
- path
- expected_hash
- result_hash
- temp_path
- status = PENDING | COMMITTED | RECOVERY_REQUIRED
```

Apply flow:

```text
persist PENDING intent
→ write temp
→ replace destination
→ verify destination hash
→ mark COMMITTED
```

On restart:

```text
for each PENDING intent:
    compare destination hash with expected_hash/result_hash

    destination == result_hash
        → finish metadata commit

    destination == expected_hash
        → previous apply did not publish; safe to retry/abandon

    anything else
        → RECOVERY_REQUIRED
        → no automatic promotion
```

This is recovery logic, not a claim of a cross-database/filesystem transaction.

---

# 9. Three-way reconciliation

Never assume the original session-start commit is still the correct base forever.

At reconciliation time:

```text
H_tip = human worktree Git tip
C_tip = Claude worktree Git tip

merge_base = git merge-base(H_tip, C_tip)

BASE   = file at merge_base
HUMAN  = current human bytes
CLAUDE = current Claude bytes
```

Then use a three-way merge:

```text
merge(current=HUMAN, base=BASE, other=CLAUDE)
```

Git's `git merge-file` is explicitly a three-way file merge.

Outcomes:

```text
only human changed
→ human result

only Claude changed
→ Claude result

both changed, non-overlapping
→ clean combined candidate

same/overlapping hunk changed
→ CONFLICT
```

A "same line" collision is therefore represented as the more precise engineering concept: an overlapping merge hunk/conflict.

---

# 10. Conflict is application state

A conflict is never only temporary UI text.

Persist:

```text
Conflict
- repo
- path
- base_version
- human_version
- claude_version
- detected_at
- status = OPEN | RESOLVED
- resolution_version
- resolved_at
```

While `OPEN`:

- automatic promotion for that path is blocked;
- the UI shows BASE / HUMAN / CLAUDE;
- BuildLens may ask Claude to reason about the conflict;
- Claude does not get to silently choose the resolution;
- the learner must explicitly resolve or choose a side.

Resolution itself becomes a new version/change event.

---

# 11. Claude Code hook strategy

Hooks improve responsiveness and add a second guard. They are not the primary isolation boundary.

## `PreToolUse`

Runs before Claude's tool call and can deny it.

For `Edit|Write`, `tool_input.file_path` is absolute.

Use it to block known unresolved-conflict paths from Claude file-tool edits.

Do **not** treat it as complete enforcement because shell tools can modify files too.

## `PostToolUse`

Runs after a successful tool call.

For `Edit|Write`, immediately:

```text
record Claude provenance
hash file
compute Claude diff
reconcile affected logical path
update UI
```

## `FileChanged`

Runs when a watched file changes on disk, regardless of which process wrote it.

Useful for:

```text
mark path dirty
hash observed content
trigger reconciliation
```

But Claude Code documentation states that FileChanged has no decision control, so it cannot be the blocking boundary.

## `Stop`

Runs when the main agent finishes responding.

Run a full repository sweep:

```text
git status --porcelain
untracked files
renames/deletes
modified paths
```

Compare against the last observed BuildLens snapshot.

This catches shell-created/modified files and events that the fast path missed.

A user interrupt does not fire the normal `Stop` hook, so BuildLens must also reconcile when the session/app next resumes or on other lifecycle signals rather than assuming every turn ends cleanly.

---

# 12. Reconciliation cadence

```text
MANUAL SAVE
→ immediate version check + affected-file reconcile

CLAUDE Edit|Write PostToolUse
→ immediate affected-file reconcile

FileChanged
→ immediate/queued affected-file reconcile

Stop
→ complete repository sweep

BUILDLENS START / SESSION RESUME
→ recovery + repository sweep before auto-promotion
```

Fast paths reduce how long a conflict goes unnoticed.

The full sweeps provide completeness.

---

# 13. Immutable provenance

Do not attempt to permanently tag every final source line as "human" or "Claude"; refactors and merges make that ambiguous.

Instead preserve immutable events:

```text
ClaudeChange
HumanChange
MergeAttempt
ConflictDetected
ConflictResolved
VersionApplied
```

Claude diff and human diff can always be reconstructed from the relevant Git/version snapshots and events.

---

# 14. Required tests

## Unit

- same bytes → same hash
- changed bytes → changed hash
- stale expected hash → `STALE_BUFFER`
- version state machine rejects illegal transitions
- only-human change → clean
- only-Claude change → clean
- non-overlapping changes → clean merge
- same-line/overlapping hunk → `CONFLICT`
- temp file is created on target filesystem
- apply does not call replace until logical checks pass
- pending write-intent recovery classifies destination hash correctly

## Integration

- Claude worktree edit never changes human physical file
- human worktree edit never changes Claude physical file
- Claude diff remains visible independently
- human diff remains visible independently
- manual save triggers immediate reconcile
- `PostToolUse(Edit|Write)` triggers immediate reconcile
- shell edit is discovered through `FileChanged` or full sweep
- `Stop` finds modified, deleted, renamed, and untracked paths
- conflict blocks promotion
- explicit resolution creates a new version
- stale editor tab cannot overwrite a newer human save
- restart preserves/reconstructs unresolved conflicts
- restart resolves pending write intents before automatic promotion

## Adversarial

- exact same line edited differently
- adjacent edits that merge algorithm treats as conflict
- rename vs edit
- delete vs edit
- Claude commit advances its tip before reconcile
- human commit advances its tip before reconcile
- two stale human tabs
- crash before replace
- crash after replace / before metadata commit
- interrupted Claude turn where normal Stop does not run
- external process modifies managed human worktree
- untracked file created only through shell

---

# 15. Later architecture-defense exercise

The learner must be able to defend this architecture without reading this document.

Questions:

1. Why not let Claude and the learner edit one physical worktree?
2. What problem do worktrees solve?
3. What problem do worktrees *not* solve?
4. Why does the editor carry an expected content hash?
5. Why can't the hash merge two versions?
6. Why is three-way merge better than last-write-wins?
7. Why do we recompute the Git merge base?
8. Why is an overlapping hunk a stop condition?
9. Why is `PreToolUse` useful but insufficient?
10. Why does `FileChanged` not provide authority?
11. Why reconcile after file-tool edits and sweep again at `Stop`?
12. Why use an atomic replace after logical merge checks?
13. Why does atomic replacement still need a recovery journal?
14. Why keep provenance as change history instead of permanent line ownership?
15. What guarantees are inside BuildLens's boundary, and what external processes remain outside it?
16. What future capability would justify replacing this design?

A strong answer separates:

```text
WORKTREE ISOLATION
→ protects physical writer separation

VERSION HASH
→ prevents stale write/lost update

THREE-WAY MERGE
→ reconciles logical concurrent edits

CONFLICT STATE
→ prevents arbitrary winner selection

ATOMIC REPLACE
→ publishes complete file bytes

RECOVERY JOURNAL
→ reconciles file bytes with BuildLens metadata after crashes

HOOKS + SWEEPS
→ fast observation plus completeness
```

---

# 16. Documentation basis

Claude Code Desktop:
https://code.claude.com/docs/en/desktop

Relevant behavior:
- Git-backed sessions use isolated worktrees.
- Desktop has file-by-file diff review.
- Its file editor warns when a file changed on disk after opening.

Claude Code hooks:
https://code.claude.com/docs/en/hooks

Relevant behavior:
- `PreToolUse` runs before tool calls and can block.
- `Write`/`Edit` paths are absolute.
- `PostToolUse` observes successful tool calls.
- `FileChanged` observes on-disk changes but has no decision control.
- `Stop` is a turn-boundary hook, but normal Stop does not run for user interrupts.

Git worktrees:
https://git-scm.com/docs/git-worktree

Git three-way merge:
https://git-scm.com/docs/git-merge-file
https://git-scm.com/docs/git-merge-base

Python:
https://docs.python.org/3/library/hashlib.html
https://docs.python.org/3/library/tempfile.html
https://docs.python.org/3/library/os.html#os.replace
