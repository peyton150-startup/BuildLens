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

Use these documents as the authority. Read the END of `CURRENT_STATE.md` first — it is
appended to chronologically and the last sections are current.

## Where I am

Phase 2 — Data Representation and Test Design. The Phase 2 knowledge gate passed at
`EV-P2-CASES-063`; I specified all four cases before seeing any test.

Code that exists and works:

```text
classify.py       classify_diff_line(line) -> one of five labels
                  file_header, metadata, added, removed, context
test_classify.py  eight tests, green

summarize.py      count_added_lines, count_removed_lines, count_changed_files
                  each takes a list of diff lines, returns one number
test_summarize.py three green tests plus ONE FAILING ONE, see below
```

Run with `python test_classify.py` and `python test_summarize.py`. There is no test runner and
no package layout; both are deliberate.

## The repo is PAUSED RED on purpose

`test_summarize.py` contains a test for `summarize_diff`, which does not exist yet:

```python
def test_summarize_diff_reports_all_three_counts():
    result = summarize_diff(TWO_FILE_DIFF)
    assert result.files_changed == 2
    assert result.lines_added == 3
    assert result.lines_removed == 2
```

**START HERE.** I was asked which error this produces and at which line, and I had not answered
when the session ended.

SPOILED, and Claude's fault, recorded so it is not repeated: Claude ran the suite to verify the
red state in the same message, so I saw the answer before committing to a prediction. The
unspoiled question is gone. Do not re-ask it as though it were open.

The salvageable version, which is a better question anyway — ask me to EXPLAIN why the failure
is `ImportError` at the import line rather than `NameError` at the call site, given that in both
cases the name is missing from a file that exists. Then give me one FRESH unspoiled prediction
before building anything.

General rule this produced: verify a red state BEFORE writing the test into the conversation, or
not at all. Do not run a suite in the same message that asks me to predict its output.

My five-member error taxonomy, built up over the last two sittings:

```text
ModuleNotFoundError   the file is not there
ImportError           the file is there, the name is not, caught at the import line
NameError             the name is not there, caught where it is used
AttributeError        the object exists, the field on it does not
AssertionError        everything exists, the value is wrong
```

## Then, one idea per patch

```text
1. build DiffSummary and summarize_diff, test-first
2. delete the three single-count functions once nothing calls them
3. splitlines boundary, one diff string -> list of lines
```

`DiffSummary` is a dataclass holding `files_changed`, `lines_added`, `lines_removed`. I chose it
over a plain tuple and defended the choice at `EV-P2-RECORD-081`: named access removes position
as a way in, so a misspelled field fails loudly instead of silently returning the wrong number.
The reversal condition I gave is that a tuple wins when the order is obvious and the count is
small.

## How to work with me

- Never reveal an answer before I commit to one.
- **Show whole files, never a fragment** — including files you have just written yourself
  through a tool call. I cannot see those. This has caused three separate wasted exchanges.
- Never print output without the code that produced it in the same message.
- Settle factual questions about tools by generating real output, not by asserting.
- Do not ask me open "what do you notice" questions. They produce "what am I looking for?"
  every time. **Ask for something countable or concrete instead** — that works immediately.
- When you want an expected value for a test, ask for the NUMBER. If you ask what the function
  should return, I will describe the behaviour instead of giving a value.
- Support is faded: questions only, no hints, unless I say I am stuck.
- Ask me for a confidence number every time, tagged SYNTAX / DESIGN / TRACING.
- When an open question fails repeatedly, convert it to a selection among plausible candidates.
- Wrong answers are expected evidence. Descend a rung, do not repeat the same difficulty.
- **If I state a rule correctly and then immediately contradict it, ask whether I know what the
  words mean before re-testing the rule.** This is how `exit code` was finally fixed after two
  failed re-tests — I could recite the rule but had never known what the number was.

## Retrievals I owe

- `splitlines` — failed its first delayed retrieval at `EV-P2-RETR-076`; I asked what it does.
  Re-learned, not banked. One unaided attempt after a gap.
- exit status — root cause found at `EV-P2-EXIT-078`. One unaided retrieval in a form that is
  NOT a Python test run, ideally a real command writing to stderr. Do not announce it.
- `branch_precedence` — three variants across two contexts already. One delayed retrieval after
  a longer gap, then it can be marked MASTERED.

## Open items carried forward

- The Phase 7 git-failure decision is MINE to make and is now much closer. When git fails it
  prints `fatal: not a git repository` and exits non-zero. My classifier labels that text
  `context` and summarizes to zeros, so BuildLens would report "Claude changed nothing" when the
  truth is "we failed to look." Those are opposite statements. The exit status carries the
  information the text does not. Record the resolution as an explicit decision rather than
  letting the zeros stand by default. Do not solve it before Phase 7.
- Renames and binary changes are invisible in the summary. Not defects against the agreed spec,
  but I should be able to say why when defending the design.
- A `.gitignore` is still wanted eventually. Low value while syncing copies named files into a
  fresh clone.
- Known limitation, accepted deliberately: `--- notes` as prose is indistinguishable from a file
  header one line at a time.

## Record keeping

Preserve every prompt, answer, reasoning, misconception, confidence and tool usage verbatim in
`learning/LEARNING_LEDGER.md`. Never clean up my original wording. Update `CURRENT_STATE.md` as
evidence changes. Record locally after every attempt; push after every five new attempts or
immediately before implementation, whichever comes first.

`C:\Users\nicol\BuildLens_Project` intentionally has no `.git` directory. Sync by creating a
temporary child clone inside that workspace, copying the changed files into it, committing and
pushing, verifying that local and origin hashes match, then deleting the temporary clone. Never
commit through the enclosing home-directory repository at `C:\Users\nicol`.

The shell resets its working directory between commands. Use `git -C <path>` with explicit
paths. A `cd` in one command does not persist to the next.

Long heredocs containing apostrophes have broken twice when appending to the ledger. Write the
block to a scratch file first, then concatenate it on.

## What I can defend right now

- Why the metadata prefixes are tested before `added` and `removed`, and why branch order only
  matters when one condition's matches are contained in another's.
- Why `diff --git` is the countable file marker and `@@` is not.
- Why a per-line label cannot say which file a line belongs to.
- Why non-diff input returns zeros instead of raising, and what that costs.
- Why `summarize.py` is a separate file from `classify.py`.
- Why `DiffSummary` is a record rather than a tuple, including the reversal condition.
- What an exit code is, and why a printed success and a failure code cannot coexist.
