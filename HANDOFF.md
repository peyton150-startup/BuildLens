# BuildLens — Session Handoff

Paste the block below into a new session.

---

Continue my BuildLens learning-first project from:

https://github.com/peyton150-startup/BuildLens

Before doing anything, completely read the repository documentation in this order:

1. CLAUDE.md
2. IMPLEMENTATION_PLAN.md
3. CURRENT_STATE.md
4. docs/CURRICULUM.md
5. learning/LEARNING_RULES.md
6. docs/CODE_READING_DEBUGGING_PLAYBOOK.md
7. docs/DESIGN_REVIEW_RUBRIC.md
8. learning/LEARNING_LEDGER.md
9. docs/LEARNING_SOURCES.md
10. docs/REFERENCE_PROJECTS.md
11. docs/COLLABORATIVE_EDITING.md
12. README.md

Use these as the authority. `CURRENT_STATE.md` is appended chronologically — **read the end
first**, it is long.

## Where I am

**Phase 3 — State and the State Movie.** MEDIUM assistance. Phase 2 is complete and its
milestone is closed.

Code that exists and works:

```text
classify.py       classify_diff_line(line) -> one of five labels
                  file_header, metadata, added, removed, context
test_classify.py  eight tests, green

summarize.py      DiffSummary dataclass + summarize_diff(diff_text)
                  takes ONE STRING of diff text, returns one DiffSummary
test_summarize.py one test, green
```

Run with `python test_classify.py` and `python test_summarize.py`. No test runner and no package
layout, both deliberate. Validated against real `git diff` output: a three-file diff gave
`DiffSummary(files_changed=3, lines_added=5, lines_removed=1)`, matching my hand count.

## Phase 3 so far — no code yet

I specified the model and passed the alias/copy knowledge gate. Nothing has been built.

My design decision:

```text
Session
└── changes[]
     └── one diff_text string per change
```

The summary is **not** stored — it is recomputed by calling `summarize_diff` when needed, because
derived data goes stale. I can defend this: measured at 0.328 ms to recompute 100 changes, about
2% of one screen frame. My reversal condition is that storing would start to win if summarizing
got expensive or the list got very large.

What I proved at the gate:

```text
p.append(9)     changes the object      every name pointing at it sees it
p = [9]         moves the name          other names stay where they were

immutable   str, int    methods return a new value, original untouched
mutable     list        methods change in place, return None
```

## START HERE — one unanswered question

I was asked this and the session paused before I answered:

> `session.changes` hands out the actual list, not a copy. What could go wrong with that?

**Do not answer it for me.** I have every tool needed. Then build `Session` test-first, and trace
real session state through several operations — that is the second half of the Phase 3 gate.

## How to work with me

- **I am a visual learner. Draw pictures and show code snippets.** This is the single most
  effective change made to this project. Every one of the ~11 recorded prompt defects has the
  same shape: an abstract question producing "what am I looking at?". When you want me to choose,
  SHOW the options as code or diagrams. When you ask what something should contain, draw the
  container first.
- Never reveal an answer before I commit to one.
- **Show whole files, never fragments** — including files you just wrote through a tool call.
  I cannot see those.
- Never print output without the code that produced it in the same message.
- **Never run a suite in the same message that asks me to predict its output.** This spoiled a
  planned assessment once.
- **Never put an invented number beside measured ones.** I caught you doing this with a made-up
  50,000-character figure and it cost you credibility. Measure or say you are guessing.
- Settle factual questions by generating real output, not by asserting.
- When you ask for an expected test value, ask for the NUMBER. If you ask what a function should
  return, I will describe behaviour instead of giving a value.
- Ask me for a confidence number every time, tagged SYNTAX / DESIGN / TRACING.
- When an open question fails repeatedly, convert it to a selection among plausible candidates.
- **If I state a rule correctly and then contradict it, ask whether I know what the words mean
  before re-testing the rule.** This is how `exit code` was finally fixed after two failed
  re-tests — I could recite the rule but had never known what the number was.
- **If my wrong answer names a neighbouring operation, check whether your own examples always
  paired the two.** This is what made `splitlines` fail twice — every demonstration had a print
  loop attached, so I fused them.
- Watch for overconfidence, not just underconfidence. I answered an alias trace WRONG at 100
  confidence right after saying I understood and asking to move on.

## Retrievals I owe

```text
exit status                          unaided, unannounced, NOT a Python test run
branch_precedence                    unaided, after a longer gap, then MASTERED
return_value_is_the_call_expression  after a gap; regressed in Phase 2 after looking stable
```

## Open items carried forward

- **The Phase 7 git-failure decision is mine to make.** When git fails it prints
  `fatal: not a git repository` and exits non-zero. My classifier labels that text `context` and
  summarizes to zeros, so BuildLens would report "Claude changed nothing" when the truth is "we
  failed to look." The exit status carries what the text does not. Record the resolution as an
  explicit decision rather than letting the zeros stand. Do not solve it before Phase 7.
- git is NOT GitHub. I have conflated them twice. `git` is the local program run as a subprocess;
  BuildLens never contacts GitHub.
- Renames and binary changes are invisible in the summary. Not defects against the agreed spec.
- Per-file attribution is impossible from a per-line label; I named the fix (a counter keyed off
  each `file_header`) and argued it should not be built yet.
- A `.gitignore` is still wanted eventually. Low value while syncing copies named files into a
  fresh clone.

## Record keeping

Preserve every prompt, answer, reasoning, misconception, confidence and tool use verbatim in
`learning/LEARNING_LEDGER.md`. Never clean up my wording. Update `CURRENT_STATE.md` as evidence
changes. Record locally after every attempt; push after five attempts or before implementation.

`C:\Users\nicol\BuildLens_Project` intentionally has no `.git`. Sync by cloning into a temporary
child directory inside that workspace, copying changed files in, committing, pushing, verifying
local and origin hashes match, then deleting the clone. Never commit through the enclosing
home-directory repository at `C:\Users\nicol`.

The shell resets its working directory between commands — use `git -C <path>`. Long heredocs
containing apostrophes have broken the ledger append twice; write the block to a scratch file
first, then concatenate.

## What I can defend right now

- Why branch order only matters when one condition's matches are contained in another's.
- Why a per-line label cannot say which file a line belongs to.
- Why `summarize.py` is a separate file from `classify.py`, using the one-sentence test.
- Why `DiffSummary` is a record rather than a tuple, including the reversal condition.
- Why a contract states what the caller can rely on, not how it was built.
- What an exit code is, and why a printed success and a failure code cannot coexist.
- Why a silent wrong answer is worse than a crash — stated generally, in three separate contexts.
- The difference between mutating an object and rebinding a name, including across a function
  boundary.
