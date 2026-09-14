## EV-P7-GIT-SPEC-281

DATE: 2026-09-02

BUILD PHASE:
Phase 7 — Git boundary specification

ACADEMIC SOURCE:
`CMU-15213-SYSTEMS`; `PY-SUBPROCESS`; `PY-PATHLIB`

DEEP SKILL:
Identify which process-boundary inputs are explicit arguments and which are inherited execution
context before designing an external-system adapter.

EXERCISE TYPE:
DESIGN_SPECIFICATION

PROMPT:
Choose whether `buildlens analyze` inspects the repository containing the current working directory,
requires an explicit repository path, or supports both through an optional path. Explain why.

LEARNER ANSWER (verbatim):

```text
i am leaning towards a but am not sure can we discuss this further
```

EVALUATION:
Tentative preference for current-working-directory behavior. Do not treat it as approval. Clarify
the intended operational workflow: BuildLens launched inside the repository versus a central
inspector launched elsewhere. Continue one question at a time before presenting approaches/design.

NEXT REQUIRED STEP:
Ask which of those two operational workflows Phase 7 should optimize for. Do not implement.

WORKFLOW CLARIFICATION PROMPT:
Should Phase 7 optimize for a developer opening a shell inside the target repository, or for
BuildLens inspecting repositories from a separate central location?

LEARNER ANSWER (verbatim):

```text
the developer opens a shell inside the target repository
```

EVALUATION:
PASS / committed specification choice. The Phase 7 CLI should support `buildlens analyze` from
inside the target repository. Preserve adapter testability by resolving the CLI's current directory
and passing that repository path explicitly into the Git adapter rather than letting adapter logic
read ambient process state invisibly.

NEXT REQUIRED STEP:
Clarify which Git comparison supplies Phase 7 input: unstaged working-tree changes, staged index
changes, or both. Do not implement.

GIT COMPARISON PROMPT:
Choose whether Phase 7 summarizes unstaged tracked changes (`git diff`), staged tracked changes
(`git diff --cached`), or the combined tracked-file state relative to HEAD (`git diff HEAD`). Explain
why; untracked files remain a separate decision.

LEARNER ANSWER (verbatim):

```text
c, if we want to see what the worktree looks like in the current state to make changes then it makes sense to do so, can we talk about this further this is a gut instict
```

EVALUATION:
Tentative preference for combined `git diff HEAD`. The rationale maps to seeing the net current
tracked-file state relative to the last commit. Explain the tradeoff: one combined patch includes
staged and unstaged content but collapses the distinction between those Git states. Do not treat the
choice as approved until the learner decides whether that provenance loss is acceptable for Phase 7.

NEXT REQUIRED STEP:
Ask whether Phase 7 needs to tell staged from unstaged changes, or only needs the combined tracked
result. Do not implement.

LEARNER REQUIREMENT REFINEMENT (verbatim):

```text
i want to see the most recent edits, so if claude code made the edits i can see them in real time, i cannot do that with staged edits, but that would be nice to do so i can double check the code before we push, so both seem needed, so we would need to go with a and b so that we can see the most recent and check before pushes and maybe make a filter for that or something, we need to keep talking abou thsi.
```

EVALUATION:
The learner identifies two distinct product needs: inspect active working-tree changes and review
the staged commit candidate. This argues for preserving separate unstaged and staged comparisons
rather than collapsing them with `git diff HEAD`. Correct two mental-model points before interface
design: staged/unstaged are repository states, not chronological recency, and Phase 7 command
execution is a snapshot rather than continuous real-time observation. Filters and live monitoring
remain separate later decisions.

NEXT REQUIRED STEP:
Explain HEAD → index → working-tree comparisons and the non-additivity of their line counts. Then ask
whether Phase 7 should expose two labeled snapshots without yet designing filter syntax.

TWO-SNAPSHOT DESIGN APPROVAL / QUESTION (verbatim):

```text
yes, i was jumping the gun, so for continous realtime observation that is actually observing files correct not summaires?
```

EVALUATION:
The learner approves two separately labeled staged and unstaged snapshots for Phase 7 and correctly
separates the later live-observation concern. Refine the architecture: a watcher or lifecycle event
is only a signal that repository state may have changed; BuildLens then inspects authoritative Git
state, derives diffs, and recomputes summaries. Summaries may update in near real time, but they are
outputs rather than observers. Keep continuous observation out of Phase 7.

APPROVED DESIGN SO FAR:

```text
invocation        buildlens analyze from inside target repository
repository input  CLI resolves current directory and passes path explicitly to adapter
Git views         separate unstaged and staged diffs
presentation      two labeled summaries; do not sum their counts
live observation  deferred; Phase 7 is command-triggered snapshot inspection
```

NEXT REQUIRED STEP:
Clarify whether untracked files are reported or explicitly out of scope for Phase 7. Do not
implement.

UNTRACKED-FILE SCOPE PROMPT:
Git's normal diff commands omit brand-new untracked files. Must Phase 7 include files Claude created
but Git has never tracked, or should support be deferred?

LEARNER ANSWER (verbatim):

```text
i have no idea
```

ADAPTATION:
The behavior is new. Reduce to one concrete repository state: a tracked file is edited and one new
source file is created. Explain that `git diff` shows the tracked edit while `git status` separately
reports the new file as untracked. Ask whether a BuildLens snapshot that omits the new file would
meet the learner's observation goal. Do not discuss implementation mechanisms yet.

NEXT REQUIRED STEP:
Use the concrete two-file scenario and ask one product-expectation question.

CONCRETE UNTRACKED SCENARIO ANSWER (verbatim):

```text
no, if the helper is needed for the app.py the snapshot is needed and it gives an incomplete snapshot
```

EVALUATION:
PASS / requirement established. A snapshot that omits a newly created dependency is incomplete even
if it includes the tracked caller edit. Phase 7 must discover untracked files. Before selecting a
mechanism, clarify whether completeness requires only their paths or their contents/line counts in
the same analysis pipeline.

NEXT REQUIRED STEP:
Ask whether Phase 7 should list untracked filenames only or represent each new text file as entirely
added content for diff summarization. Do not implement.

UNTRACKED REPRESENTATION ANSWER (verbatim):

```text
B, this shows the complete timeline as well as gives the user context as to why app.py has the changes made to it, like if we changed summarize for another module and the other module was not tracked the user would only see half the picture
```

EVALUATION:
PASS / committed requirement. Phase 7 must include untracked text-file contents as entirely added
content in the unstaged diff/summary, not merely list paths. The rationale correctly identifies a
cross-file dependency: a tracked caller edit without its new untracked dependency is only half the
change picture. Refine wording from complete timeline to complete point-in-time snapshot; Git diffs
do not establish chronological edit order.

NEXT REQUIRED STEP:
Clarify whether failure to obtain any component of staged/unstaged/untracked state invalidates the
whole snapshot or permits explicitly partial output. Do not choose commands or implement yet.

OPERATOR WORKFLOW CLARIFICATION (verbatim):

```text
ok the situation we are trying to go for is claude code on the left half and build lens on the right half of the screen, when claude makes a change we wait a few seconds and then call buildlens analyze and then we get the summary
```

EVALUATION:
This defines Phase 7 as repeated, operator-triggered point-in-time inspection beside Claude Code,
not automatic monitoring. Waiting briefly reduces transient write races but does not prove a stable
snapshot. Because the command is cheap to rerun and completeness is required, recommend failing the
whole snapshot with a readable diagnostic if any required component cannot be obtained, rather than
presenting a misleading partial summary. Require explicit learner approval before design adoption.

APPROVED WORKFLOW SO FAR:

```text
Claude Code edits in one pane
→ learner waits for a reasonable command boundary
→ learner runs buildlens analyze in the repository
→ BuildLens captures one complete point-in-time snapshot
→ BuildLens prints separately labeled unstaged and staged summaries
```

NEXT REQUIRED STEP:
Ask whether fail-whole-snapshot plus manual retry fits this workflow. Do not implement.

FAILURE-ATOMICITY APPROVAL (verbatim):

```text
yes, as long as they know to try again
```

EVALUATION:
PASS / approved design. If any required staged, tracked-unstaged, or untracked component cannot be
captured, Phase 7 prints no partial summary, writes a readable diagnostic to stderr, returns 1, and
explicitly tells the learner to rerun `buildlens analyze`. The retry instruction is part of the
user-facing contract, not incidental wording.

NEXT REQUIRED STEP:
Clarify successful output when both staged and unstaged snapshots contain zero changes. Do not
implement.

CLEAN-REPOSITORY OUTPUT APPROVAL (verbatim):

```text
yes this works
```

EVALUATION:
PASS / approved design. A clean repository returns 0 and prints both labeled sections with zero
files changed, lines added, and lines removed. Empty Git output is therefore a successful empty
snapshot, not an error or ambiguous blank display.

NEXT REQUIRED STEP:
Requirements are sufficient to compare Git capture approaches. Present 2–3 approaches with
tradeoffs and a recommendation, then obtain approval before writing the design spec.

CAPTURE-APPROACH DECISION (verbatim):

```text
yeah git native is the correct choice here
```

EVALUATION:
PASS / approved design direction. Use a Git-native, read-only approach: separate Git commands for
tracked unstaged and staged diffs, Git discovery for untracked paths, and Git no-index diffing to
represent untracked contents without mutating the index. Accept extra child processes and
command-specific interpretation of no-index status 1. Reject intent-to-add because an observation
command must not mutate developer staging state.

NEXT REQUIRED STEP:
Present the module/data-flow design section for approval. Do not implement.

MODULE-DESIGN SYNTAX QUESTION (verbatim):

```text
what is cwd()
```

ADAPTATION:
Pause architecture evaluation. Explain only that `Path.cwd()` means current working directory and
returns a Path object naming the directory in which the Python process is currently operating. It
takes no argument and does not change directories. Give one shell-location example and require a
fresh path prediction before returning to the design.

NEXT REQUIRED STEP:
Given a shell currently in one repository directory, ask what `Path.cwd()` returns and whether it
changes the directory.

CWD MICRO-CHECK ANSWER (verbatim):

```text
it represents `C:\projects\Argos`   and it does not change directories, 90
```

EVALUATION:
PASS. `Path.cwd()` returns a Path representing the current process directory and performs no
directory-changing side effect. Resume evaluation of the module/data-flow design.

NEXT REQUIRED STEP:
Re-present the compact boundary: CLI resolves Path.cwd, adapter returns staged/unstaged diff text,
existing core summarizes. Ask for approval or revision. Do not implement.

MODULE/DATA-FLOW APPROVAL (verbatim):

```text
yes, each midule still has the correct respoinsiblities and boundaries are upheld, 90
```

EVALUATION:
PASS / approved design. The learner correctly defends the module split through responsibility and
boundary preservation: CLI owns orchestration/process-facing presentation, the Git adapter owns
external Git knowledge, and the existing deterministic core remains Git-unaware.

NEXT REQUIRED STEP:
Present error handling and subprocess semantics for approval: argument-list execution without a
shell, timeout, text decoding, command-specific statuses, atomic snapshot failure, and CLI recovery.

SUBPROCESS SYNTAX QUESTION (verbatim):

```text
can you explain each line?in run
```

ADAPTATION:
Pause design approval. Explain only the multiline `subprocess.run(...)` call: function call and
returned CompletedProcess, command list, child-only cwd, captured stdout/stderr, text decoding,
timeout, shell exclusion, and trailing commas. Then require one small call-reading prediction before
returning to the error-contract design.

NEXT REQUIRED STEP:
Explain each line without solving the surrounding adapter, then give one non-Git subprocess call and
ask for executable/arguments, child directory, output representation, and timeout.

SUBPROCESS CALL-READING ANSWER (verbatim):

```text
tool
inspect , --short
repository path
string
5 seconds
90
```

EVALUATION:
PASS. The learner correctly identifies the executable, both arguments, child working directory,
string output representation, and timeout. The multiline subprocess call is readable. Resume the
subprocess/error-contract design approval.

NEXT REQUIRED STEP:
Re-present the compact error contract and ask whether the learner approves argument-list execution,
captured UTF-8 text, shell exclusion, ten-second timeout, command-specific statuses, whole-snapshot
failure, and retry guidance.

LEARNER PROCESS OBJECTION / PROVISIONAL APPROVAL (verbatim):

```text
yes, but werent you supposed to teach me this first?
```

EVALUATION:
The objection is correct. Only multiline call syntax was taught; the design approval also depends on
untaught process semantics: parent versus child process, captured channels, timeout control, and
command-specific status interpretation. Treat approval as provisional and restore the mandatory
teaching sequence from the smallest prerequisite. Academic objective: trace Python process → child
process → stdout/stderr/status → Python interpretation (`CMU-15213-SYSTEMS`, `PY-SUBPROCESS`).

NEXT REQUIRED STEP:
Ask one prediction first: whether invoking Git through `subprocess.run` executes Git inside the
existing Python process or starts a separate child process. Do not explain or approve the design
until the learner commits.

PARENT/CHILD PREDICTION PROMPT:
For `subprocess.run(["git", "--version"])`, predict whether Git executes inside the existing
BuildLens Python process or the operating system starts a separate Git process; name the relationship
if known. Confidence: 0–100.

LEARNER ANSWER (verbatim):

```text
i have no idea, 5
```

ADAPTATION:
Descend to one concept only. The running BuildLens Python program is the parent process. The
operating system starts the requested executable as a separate child process. `subprocess.run`
waits for that child to finish before returning. Defer channels, statuses, timeout, memory, and Git
semantics. Require one unrelated parent/child labeling check.

NEXT REQUIRED STEP:
Use Python launching a generic formatter tool. Ask which is parent and which is child.

PARENT/CHILD REMEDIATION ANSWER (verbatim):

```text
so run git starts it as a sepreate child process and then the parent or buildlens process waits until the child is done beofre continueing exectuoin, 90
```

EVALUATION:
PASS on the BuildLens surface. Git runs as a separate child process; the BuildLens Python parent
waits inside `subprocess.run` and resumes after the child finishes. Require one unrelated same-rung
transfer before adding channels.

NEXT REQUIRED STEP:
Use a Python backup program launching a compressor executable. Ask for parent, child, and which waits.

PARENT/CHILD TRANSFER ANSWER (verbatim):

```text
python program is the parent, compressor is the child process, parent waits for child, python program coninutes when the compressor finishies with the archive.data, 90
```

EVALUATION:
PASS. Parent, child, waiting process, and resume condition all transfer correctly to a non-Git
surface. Parent/child remediation is closed. Add captured stdout/stderr as the next single concept.

NEXT REQUIRED STEP:
Before explaining, ask where one normal child message and one error child message appear when
`capture_output=True` and the returned object is named `result`.

CAPTURED-CHANNELS PREDICTION ANSWER (verbatim):

```text
it is inside result in the stdout stream&#x20;
it is inside result in the stderr stream
strings
90
```

EVALUATION:
PASS. The parent reads normal text from `result.stdout`, error text from `result.stderr`, and both
are strings because text mode is enabled. Add only numeric child completion status next.

NEXT REQUIRED STEP:
With no `check=True`, ask what `result.returncode` contains when the child exits 3 and whether
`subprocess.run` automatically raises for that nonzero status.

RETURN-CODE PREDICTION ANSWER (verbatim):

```text
i have no idea
```

ADAPTATION:
Descend to one default rule. When `check=True` is not supplied, a child that starts and finishes
with nonzero status still produces a returned CompletedProcess; the integer is stored in
`result.returncode`. The parent code decides what that command-specific number means. Defer every
other exception source and require one new numeric fill-in.

NEXT REQUIRED STEP:
Use a child exiting 4 with no `check=True`. Ask for `result.returncode` and whether run returns
normally.

RETURN-CODE REMEDIATION ATTEMPT 1 ANSWER (verbatim):

```text
3
yes
90
it runs normally and lets the parent process decide what the returncode menas
```

EVALUATION:
The control model passes: run returns normally and the parent interprets the code. The exact integer
was carried over from the modeled status-3 example. In this fresh case the child exited 4, so
`result.returncode` must be 4. Ask only for that value before adding complexity.

NEXT REQUIRED STEP:
State “the child exits 4” and require only `result.returncode`.

RETURN-CODE REMEDIATION ATTEMPT 2 ANSWER (verbatim):

```text
4
```

EVALUATION:
PASS. The child's exact nonzero status is preserved as `result.returncode`; combined with the prior
reasoning, run returns normally and the parent interprets it. Move to Git-specific status semantics.

NEXT REQUIRED STEP:
Ask whether `git diff --no-index` status 1 with diff text is a valid “different” result or a Git
adapter failure. Require reasoning from the command contract.

NO-INDEX FIRST RESPONSE (verbatim):

```text
is it just saying that helper.py is empty?
```

ADAPTATION:
Clarify only the comparison. `<empty-file>` names a separate known-empty baseline; it does not
describe `helper.py`. A nonempty helper differs from that baseline, so Git emits its contents as
additions and returns no-index status 1. The question exposes a real edge case: an actually empty
untracked file may produce no content diff and needs explicit design handling to avoid silent
omission. Defer that design choice until the basic comparison passes.

NEXT REQUIRED STEP:
Ask whether the empty baseline is the object being compared with `helper.py`, then replace the
placeholder with explicit contents before asking for status interpretation.

NO-INDEX CLARIFICATION QUESTION (verbatim):

    ```csharp
    <empty-file> is what git compares helper.py with?
    ```

FACILITATOR CLARIFICATION:
Yes. `<empty-file>` was an undefined placeholder for the left-hand filesystem path; `helper.py` is
the right-hand path. No-index compares those two paths without consulting the repository index. A
nonempty right-hand file therefore appears as added content relative to the empty baseline. The
earlier notation was ambiguous; replace it with explicit contents before requiring the prediction.

NEXT REQUIRED STEP:
Give explicit empty-baseline and one-line-helper contents. Ask same/different, added line, and whether
documented status 1 is valid data or failure.

LEARNER RESPONSE (verbatim):

```text
i still do not understand
```

EVALUATION:
The no-index surface remains unclear. Descend below Git, files, and statuses to one before/after text
comparison: before is empty; after contains one line. Ask only whether that line was added or removed.

PRIMARY BLOCKER:
direction of a comparison from an empty before-state to a nonempty after-state

NEXT REQUIRED STEP:
Use `before = ""` and `after = "hello\n"`. Ask only whether `hello` is added or removed.

VISUAL-EXPLANATION REQUEST (verbatim):

```text
can you describe with pictures
```

ADAPTATION:
Provide a two-panel visual containing only the reduced concept: an empty BEFORE baseline on the left
and `helper.py` containing `print("ready")` in the AFTER state on the right. Label the line with `+`
as added. Do not reintroduce Git, `--no-index`, or status codes until the direction is recovered.

NEXT REQUIRED STEP:
After the pause, show the visual again if needed and ask only: is `print("ready")` added or removed?
Then use one fresh empty-before/nonempty-after transfer before returning to no-index status 1.

SESSION STOP — 2026-09-02:
The learner requested a commit/push and a two-sentence handoff for a new session. No Phase 7 product
code exists. Resume at the visual remediation question above; do not skip ahead to implementation.

VISUAL DIRECTION REMEDIATION ANSWER (verbatim):

```text
added
```

EVALUATION:
PASS. From an empty BEFORE state to an AFTER state containing `print("ready")`, the learner correctly
identified the line as added. The primary comparison-direction blocker passed on this reduced
BuildLens-adjacent surface.

NEXT REQUIRED STEP:
Give one fresh empty-before/nonempty-after transfer with different content. Ask only whether the new
line was added or removed. Do not reintroduce Git or status codes until that transfer passes.

VISUAL DIRECTION TRANSFER ANSWER (verbatim):

```text
added
```

EVALUATION:
PASS. From an empty BEFORE state to an AFTER state containing `status = "online"`, the learner
correctly identified the new line as added. Comparison direction transferred to a fresh surface.

NEXT REQUIRED STEP:
Return to the explicit no-index scenario: Git compares a known-empty file with a one-line
`helper.py`, emits that line as added content, and returns documented status 1 because the files
differ. Ask whether status 1 is valid difference data or an adapter failure.

NO-INDEX STATUS INTERPRETATION ANSWER (verbatim):

```text
difference data, it means that the helper.py is not emprty because if it was it would not return 1
```

EVALUATION:
PASS. Status 1 is valid difference data under the `git diff --no-index` command contract, not a
generic adapter failure. The learner correctly connected the known-empty baseline to the nonempty
right-hand file and predicted status 0 for identical empty contents. Precision: status 1 directly
means the compared paths differ; nonemptiness follows here because one path is known empty.

NEXT REQUIRED STEP:
Introduce only timeout behavior. Ask whether `subprocess.run(..., timeout=10)` returns a normal
`CompletedProcess` or raises `subprocess.TimeoutExpired` when Git has not finished after ten seconds.

TIMEOUT PREDICTION ANSWER (verbatim):

```text
rasie
```

EVALUATION:
PASS. When the child does not finish within the supplied timeout, `subprocess.run` raises
`subprocess.TimeoutExpired` instead of returning a normal `CompletedProcess`. This is distinct from
a child that finishes with a nonzero status when `check=True` is absent.

NEXT REQUIRED STEP:
Use an unrelated parent program launching a compressor with `timeout=5`. Ask what the Python parent
receives if the compressor is still running after five seconds, and why it does not receive a normal
completed result.

TIMEOUT TRANSFER ANSWER (verbatim):

```text
the timeoutexpired error  is what it receives and it is becasue a completed process would be completed before the 5 seconds are up
```

EVALUATION:
PASS. The learner transferred timeout behavior to an unrelated compressor process: the Python
parent receives `subprocess.TimeoutExpired`, and no normal `CompletedProcess` exists because the
child did not complete within the configured limit.

NEXT REQUIRED STEP:
Present the complete Phase 7 subprocess/error contract for explicit approval or revision:
argument-list execution without a shell; child cwd set to the repository; captured text channels;
ten-second timeout; command-specific return-code interpretation including no-index status 1;
whole-snapshot failure with no partial summary; readable stderr telling the learner to rerun
`buildlens analyze`.

LEARNER SUBPROCESS/ERROR CONTRACT REVISION (verbatim):

````text
can we add this in: I checked the BuildLens Phase 7 material and CMU material. There **is one worthwhile revision pass left**, but I would keep it small rather than expanding Phase 7.

BuildLens explicitly says Phase 7 should exercise **executable-not-found, non-zero exit, timeout, and valid-process/malformed-output cases**. Your proposed contract covers almost everything except **malformed output** and makes executable-launch failure only implicit. The curriculum also deliberately wants you to understand the full `Python → child process → stdout/stderr → return code → interpretation` path.

The actual CMU Agentic AI program doesn't add anything useful at this particular level. Its curriculum begins much higher up—LLMs, agent architecture, tools, RAG, multi-agent systems, evaluation, guardrails, logging, and observability. ([Executive Online](https://execonline.cs.cmu.edu/agentic-ai-program?utm_source=chatgpt.com)) So I would **not hold up Phase 7 trying to force Agentic-AI concepts into subprocess handling**.

I would revise your contract to this:
```text
BuildLens invokes Git with an argument list and no shell
→ Git is launched as a child process with the target repository as its working directory
→ failure to launch Git is a command failure
→ stdout and stderr are captured as text
→ each command has a 10-second timeout
→ return codes are interpreted according to that specific Git command's contract
→ git diff --no-index status 1 means valid difference data, not failure
→ successful execution does not automatically mean valid data
→ malformed or unusable Git output is a snapshot failure
→ any launch failure, genuine command error, malformed required output, or timeout rejects the whole snapshot
→ no partial summary is printed
→ stderr identifies which snapshot component failed, preserves useful Git diagnostic information, and says to rerun buildlens analyze
→ CLI returns status 1
```

### Why I think those additions matter

The strongest addition is:

> **successful execution does not automatically mean valid data**

That is an important engineering distinction. You now have **two layers of success**:
```text
PROCESS CONTRACT
Did Git execute successfully?

        ↓

DATA CONTRACT
Did Git produce output BuildLens can actually use?
```

A process can return something that passes its process-level contract while still violating what BuildLens expects from the data. Your own learning plan specifically calls for the `valid-process/malformed-output` case, so leaving that out would skip one of the exercises Phase 7 was designed to teach.

I'd also explicitly add:

> **failure to launch Git is a command failure**

because this is different from:
```text
Git launched → Git returned 128
```

versus:
```text
BuildLens tried to launch Git
→ operating system could not start Git at all
```

That distinction gets you closer to the systems-level reasoning BuildLens is trying to develop instead of treating every failure as merely "nonzero return code."

I **would not add** retries, logging infrastructure, kill trees, concurrency, elaborate observability, configurable timeout policies, or recovery state here. Those are useful concepts, but your curriculum deliberately moves deeper reliability/concurrency/reconciliation concepts into later phases. Phase 9 onward covers things such as timeouts, retries, idempotency, partial failure, stale state, and reconciliation.

So my recommendation is: **make those two/three small revisions, test the four failure classes, defend them, and move on from the contract.**

Your Phase 7 test matrix should essentially be:

| SituationExpected interpretation          |                  |
| ----------------------------------------- | ---------------- |
| Git returns expected `0`                  | valid            |
| `git diff --no-index` returns `1`         | valid difference |
| Git returns genuine error code            | reject snapshot  |
| Git executable can't launch               | reject snapshot  |
| Git exceeds 10 sec                        | reject snapshot  |
| Git runs but required output is malformed | reject snapshot  |

Once you can explain **why&#x20;****`1`****&#x20;can mean data for one command but failure for another**, and **why process success ≠ data validity**, I don't see much educational value in continuing to revise this contract. **Then move on.**
````

EVALUATION:
PASS / approved revision. The learner found the two omissions already named by the Phase 7
curriculum: executable launch failure and valid-process/malformed-output. They correctly separated
the process contract from the data contract, distinguished launch failure from a launched Git child
returning a genuine error status, supplied a focused failure matrix, and explicitly deferred later
reliability and Agentic-AI concerns. The contract is now recorded in `IMPLEMENTATION_PLAN.md`.

NEXT REQUIRED STEP:
Require one non-Git transfer: a child process exits with its documented success status but emits
output that the parent application cannot parse. Ask whether the process contract, data contract,
both, or neither passed, and what the parent should do.

PROCESS/DATA CONTRACT TRANSFER ATTEMPT 1 ANSWER (verbatim):

```text
the contract did not pass or it would have been status 1, the data contract aslo did not pass since it should have been a numeric temperature and the parent should raise an error so the user can take a look
```

EVALUATION:
PARTIAL. The learner correctly identified the data-contract failure and the need for the parent to
reject/surface the unusable result. The process-contract conclusion is incorrect: the exercise
defined status 0 as the weather command's documented success status. Status 1 is not a universal
success code; meanings belong to each command's contract.

PRIMARY BLOCKER:
Keeping the child's documented completion status separate from the parent's later validation of the
returned data.

ADAPTATION:
Descend to R1 with no malformed data and no Git-specific status. State that a generic tool's
contract defines status 0 as successful completion and that the tool returns 0. Ask only whether the
process contract passed.

NEXT REQUIRED STEP:
Ask the R1 process-only check. After it passes, use a fresh process-success/data-failure near-transfer
before returning to Phase 7 specification.

R1 DOCUMENTED-STATUS ANSWER (verbatim):

```text
pass, i thought for the git diff if it returned 1 that was a pass or am i imagining that
```

EVALUATION:
PASS. For the generic tool whose documented contract defines status 0 as successful completion,
returned status 0 satisfies the process contract. The learner also correctly recalled the special
Git rule that prompted the confusion: `git diff --no-index` uses 0 for no differences and 1 for
differences found, so the adapter accepts both as valid command outcomes. Status meanings are
command-specific; status 1 is not universal success.

NEXT REQUIRED STEP:
Give a fresh non-Git near-transfer in which a child returns its documented success status 0 but
emits syntactically unusable application data. Ask separately whether the process contract and data
contract passed. Do not ask for exception mechanics yet.

PROCESS/DATA CONTRACT NEAR-TRANSFER ANSWER (verbatim):

```text
the process contract passed bu the data contract dud not, 90
```

EVALUATION:
PASS. The inventory child returned its documented success status 0, so the process contract passed;
its `not-json` output violated the parent's required JSON representation, so the data contract
failed. The learner independently separated process completion from application-data validity at
confidence 90. The remediation chain is closed.

NEXT REQUIRED STEP:
Return to the Phase 7 empty-untracked-file edge case. Ask whether an empty newly created file should
be omitted or represented in the UNSTAGED snapshot as one changed file with zero added/removed
lines. Require reasoning from the already-approved completeness requirement.

VOCABULARY QUESTION (verbatim):

```text
what does omit mean
```

ADAPTATION:
Pause the surrounding design choice. Explain only that “omit” means leave out or not include, then
give an R0 report-membership example and ask whether `placeholder.py` was included or omitted.

EMPTY-UNTRACKED-FILE CHOICE (verbatim):

```text
show it as unstaged and have them be zeros for added and removed
```

EVALUATION:
CORRECT CHOICE / REASONING DUE. The learner chose to preserve the empty untracked file in the
UNSTAGED snapshot as one changed file with zero added and zero removed lines. This also demonstrates
the vocabulary distinction: the file is not omitted. Require the reason from the approved
completeness requirement before treating the specification decision as complete.

NEXT REQUIRED STEP:
Ask only why the file should remain visible when both line counts are zero.

SESSION PAUSE — 2026-09-02:
The learner paused for dinner and requested a commit and push. Resume with the single reasoning
question above. No Phase 7 product code exists.

EMPTY-UNTRACKED-FILE REASONING ATTEMPT 1 ANSWER (verbatim):

```text
i do not know
```

EVALUATION:
UNANSWERED. The learner selected the correct representation earlier but could not yet explain why
an empty file must remain visible despite zero added/removed lines.

PRIMARY BLOCKER:
Distinguishing the fact that a file exists from the separate fact that its content contains zero
lines.

ADAPTATION:
Descend to R1 with no Git vocabulary and no counts. Show a folder before and after creation of an
empty file. Ask only whether the folder state changed.

NEXT REQUIRED STEP:
Ask the R1 presence-versus-content question. After it passes, use a near-transfer that reconnects
file presence to a complete snapshot.

R1 EMPTY-FILE PRESENCE ANSWER (verbatim):

```text
yes
```

EVALUATION:
PASS. Creating an empty `placeholder.py` changed the folder state because a new path now exists,
even though the new file contains zero lines. File presence and content line count are separate
facts.

NEXT REQUIRED STEP:
Ask whether a snapshot claiming to show every folder change is complete if it hides the newly
created empty file. Require only complete/incomplete and a short reason.

EMPTY-FILE COMPLETENESS NEAR-TRANSFER ANSWER (verbatim messages):

```text
so we show the empy file because it is a change in state
```

```text
and that is apart of the snapshot
```

EVALUATION:
PASS. The learner correctly connected the file's changed existence to the snapshot's completeness
contract. An empty untracked file is a file-level state change even though it contributes zero added
and zero removed content lines. The Phase 7 requirement is approved: show it in UNSTAGED as one
changed file with zero line counts. The remediation chain is closed.

NEXT REQUIRED STEP:
Compare implementation mechanisms for preserving the empty file without weakening the approved
adapter/core boundary. Do not write Phase 7 product code until the learner understands and approves
the mechanism.

FILE-PRESENCE EVIDENCE ATTEMPT 1 ANSWER (verbatim):

```text
the content line counter, if no lines are ever added then it will be empty , i am not sure
```

EVALUATION:
INCORRECT / UNCERTAIN. The content-line counter cannot establish whether an empty file exists. Both
“no file created” and “empty file created” yield zero added and zero removed content lines, so those
counts collapse two repository states that Phase 7 must distinguish.

PRIMARY BLOCKER:
Recognizing that a representation is insufficient when two relevant real states produce the same
represented value.

ADAPTATION:
Descend to R1. Present two cases that both have added=0 and removed=0, with only one containing a new
empty file. Ask whether line counts alone can tell the cases apart.

NEXT REQUIRED STEP:
Ask only the R1 distinguishability question. After it passes, return to choosing which evidence owns
file presence.

R1 ZERO-LINES/TWO-STATES ANSWER (verbatim):

```text
no
```

EVALUATION:
PASS. Identical `added = 0` and `removed = 0` values cannot distinguish the state in which no file
was created from the state in which a new empty file exists. The learner now recognizes the
information loss in content counts alone.

NEXT REQUIRED STEP:
Show the untracked-path discovery results for the same two cases—no paths in Case A and
`placeholder.py` in Case B—and ask whether that evidence can distinguish them.

LEARNER EVIDENCE-BOUNDARY QUESTION (verbatim):

```text
but how would path disocervy tell you it is empty
```

FACILITATOR CLARIFICATION:
It would not. Path discovery proves only that a new untracked path exists. Content inspection
separately determines how many lines the file contains. Together they preserve both the file-level
state change and its content counts.

FILE-PRESENCE/CONTENT-EVIDENCE ANSWER (verbatim):

```text
so we would need path discovery to show a file is there, then we would need content inspection to see how many lines the file has and finally the counts would show us if there is a change in the file
```

EVALUATION:
PASS WITH PRECISION. The learner correctly assigns existence to path discovery and line measurement
to content inspection. Precision: for an untracked file, discovery already proves the file-level
change; content counts describe its content and may be zero. This remediation chain is closed.

NEXT REQUIRED STEP:
Inspect the exact current summary representation, then present the smallest candidate Phase 7
representation that can preserve staged/unstaged separation, untracked path presence, and content
counts without making line counts infer file existence. Require learner approval before code.

LEARNER COUNT-AUTHORITY FOLLOW-UP (verbatim):

```text
but after the file level change the counts will be needed to see there is a change
```

EVALUATION:
PARTIAL. Counts are needed to describe changed content, but not to establish every file-level
change. The existing summarizer increments `files_changed` from a `diff --git` header independently
of `+` and `-` content lines.

VERIFIED LOCAL GIT PROBE:

```text
git diff --no-index -- /dev/null .claude-flow/data/pending-insights.jsonl

diff --git a/.claude-flow/data/pending-insights.jsonl b/.claude-flow/data/pending-insights.jsonl
new file mode 100644
index 0000000..e69de29
RETURN_CODE=1
```

The compared right-hand file was empty. Git represented creation with a file header and metadata,
returned the documented “different” status 1, and emitted no added/removed content lines. This
preserves the exact facts needed by the existing core: one file changed, zero lines added, zero lines
removed.

DESIGN CORRECTION:
The earlier reduced explanation used an existing empty baseline to teach comparison direction. That
was useful for the line-direction remediation but is not sufficient as the final empty-file
mechanism because two existing empty files compare equal. The implementation candidate uses
`/dev/null` as the conventional “did not exist before” side, which preserves file creation even
when the created file is empty.

NEXT REQUIRED STEP:
Show the three-line verified Git output and ask the learner to trace the exact `DiffSummary` through
the existing classifier/summarizer: `diff --git` increments files, while metadata increments neither
line counter.

INDEX-LINE SYNTAX QUESTION (verbatim):

```text
so index 00000000 is the number of lines in the file?
```

ADAPTATION:
Pause the surrounding summary trace. Explain only the unified-diff `index old..new` form:
abbreviated Git object identifiers, not line counts; left is BEFORE, right is AFTER; all-zero old
identifier represents no prior file object here; `e69de29` identifies Git's empty blob. Ask which
side is BEFORE.

INDEX SYNTAX MICRO-CHECK + EMPTY-FILE TRACE ANSWER (verbatim):

```text
before is the left and after is the right ok i understand, and the new file mode is how we know it is new, and the files changes is 1 and the lines added and removed are zero so all of that tells us it is empty
```

EVALUATION:
PASS. The learner correctly read left as BEFORE and right as AFTER, identified `new file mode` as
creation metadata, and traced the output through the existing summarizer to
`DiffSummary(files_changed=1, lines_added=0, lines_removed=0)`. The syntax-only interruption and the
surrounding trace are both closed.

NEXT REQUIRED STEP:
Ask whether the learner approves using Git's `/dev/null`-to-untracked-file no-index comparison for
new files, including empty ones, with command-specific acceptance of status 1 and unchanged use of
the existing diff summarizer. Do not implement until approved.

REPRESENTATION CLARIFICATION REQUEST (verbatim):

```text
can you explain both so i know what they actually mean i am reading the changes and it is going over my head
```

FACILITATOR CORRECTION:
The earlier “hardened versus structured” comparison mixed two independent decisions. Malformed-output
validation is required under either representation. The real choice is validated plain diff text
versus a validated record containing named fields such as path, diff text, and return code.

REPRESENTATION DECISION (verbatim):

```text
it seems liek the strucutred result is overkill, since we only need the plain diff text, check me on that
```

EVALUATION:
PASS / APPROVED FOR THE PER-COMMAND ADAPTER BOUNDARY. The current downstream consumer needs only
validated unified-diff text. The adapter may use path, return code, and stderr internally to validate
the command and output without exporting them in a new object. Introducing a structured result now
would add a type and caller step without a current consumer requirement. Precision: the overall
snapshot must still preserve separately labeled UNSTAGED and STAGED captures.

ACCEPTED DOWNSIDE:
The returned string does not carry the validation evidence or source path as named fields. That
information remains internal to the adapter operation.

NEXT REQUIRED STEP:
Ask what concrete future requirement would make the structured result worth introducing. Require a
reversal condition tied to a consumer need, not “cleaner code.”

PLAIN-DIFF MECHANISM APPROVAL (verbatim):

```text
sounds good to me
```

EVALUATION:
APPROVED. Phase 7 will use validated plain unified-diff text for each Git capture, including real
`/dev/null`-to-file output for untracked files. The adapter retains process/path/diagnostic evidence
internally while the unchanged summarizer receives only validated diff text.

NEXT REQUIRED STEP:
Ask for one concrete reversal condition that would justify replacing the string boundary with a
structured result later.

STRUCTURED-RESULT REVERSAL ANSWER (verbatim):

```text
the return code, i am not sure
```

EVALUATION:
PASS WITH PRECISION. The exact return code can justify a structured result if a downstream consumer
gains a concrete requirement to receive it, such as displaying diagnostics or persisting an audit
record. Its mere existence inside the adapter does not justify exporting it; the adapter already
uses it to validate the command-specific process contract.

REVERSAL CONDITION:
Replace the validated-string boundary when a real downstream feature must consume process/path/
diagnostic metadata that cannot be obtained from the diff text without recreating Git knowledge
outside the adapter.

NEXT REQUIRED STEP:
Give one unrelated transfer: an image converter currently returns validated image bytes, but a new
UI must display codec and dimensions. Ask whether a structured result is now justified and why.

STRUCTURED-RESULT TRANSFER ANSWER (verbatim):

```text
yes, because we need more than just the image we need the width and height, i still am not sure what data type we would need to add to a downstream caller
```

EVALUATION:
PASS. The learner correctly identified a new consumer requirement for multiple related values and
therefore justified reversing from a bytes-only return to a structured result. The design principle
transferred outside Git.

SYNTAX/REPRESENTATION QUESTION:
The learner is unsure what data type would cross the boundary. Explain only that the adapter can
define and return a small record type, such as a Python dataclass, and the caller receives one
instance and reads named fields. Do not suggest adding that type to current Phase 7 code.

NEXT REQUIRED STEP:
Show a minimal `ImageResult(data, width, height)` dataclass and one returned instance. Ask what
`result.width` evaluates to.

BYTES-LITERAL SYNTAX QUESTION (verbatim):

```text
is this a typo: (b"image bytes", 800, 600)
```

FACILITATOR CLARIFICATION:
No. The `b` prefix creates a `bytes` literal rather than a `str`; image payloads are binary data in
this transfer example. The positional arguments map to `data`, `width`, and `height` in declaration
order.

FIELD-ACCESS MICRO-CHECK ANSWER (verbatim):

```text
800
```

EVALUATION:
PASS. `800` is assigned to `width`, so `result.width` evaluates to `800`. The syntax-only interruption
is closed. No structured result is introduced into Phase 7; validated plain diff text remains the
approved per-command boundary.

NEXT REQUIRED STEP:
Present one narrowly scoped first Phase 7 implementation patch for learner approval. The patch must
introduce only the process-running boundary and its focused tests, leaving multi-command snapshot
composition, untracked discovery, `/dev/null` capture, CLI replacement, and final output formatting
for later patches.

STAGED-CAPTURE SCOPE QUESTION (verbatim):

```text
so are we creating the staged capture later?
```

FACILITATOR CLARIFICATION:
Yes. Patch splitting changes sequence, not the approved final behavior. The planned order is tracked
UNSTAGED capture, tracked STAGED capture, untracked discovery plus `/dev/null` diffs, then labeled
CLI composition.

FIRST PATCH SCOPE APPROVAL (verbatim):

```text
yes
```

EVALUATION:
APPROVED. The first Phase 7 product patch is limited to one tracked-UNSTAGED capture function and
focused tests. It does not implement staged capture, untracked files, `/dev/null`, CLI integration,
or final formatting. Those remain explicit later slices.

NEXT REQUIRED STEP:
Complete the test-strategy section of the architectural design. Compare controlled subprocess-result
tests against temporary-real-repository tests, explain the tradeoff in plain language, and ask the
learner to approve one approach before any product code.

FIRST-PATCH TEST-STRATEGY APPROVAL (verbatim):

```text
yes lets do the subprocess tests
```

EVALUATION:
APPROVED. The first patch will use controlled subprocess results to verify exact arguments, child
working directory, text capture, timeout, accepted status, returned stdout, and unexpected-status
rejection without mutating a real repository. The accepted downside is that this does not prove real
Git integration. A small real-Git integration test is deferred until the capture paths are assembled.

DESIGN RECORD:
`docs/superpowers/specs/2026-09-02-phase-7-git-boundary-design.md`

SELF-REVIEW:
No placeholders remain. The design preserves separate UNSTAGED/STAGED output, read-only Git capture,
validated plain diff text, whole-snapshot failure, and later untracked empty-file support. The first
slice is explicitly narrower than the final Phase 7 behavior and is not wired into the CLI.

NEXT REQUIRED STEP:
Ask the learner to review and approve the written design. Do not create an implementation plan or
write product code until that approval is explicit.

WRITTEN DESIGN APPROVAL (verbatim):

```text
everything looks good
```

EVALUATION:
APPROVED. The Phase 7 Git-boundary design is ready for implementation planning. No product code has
been written.

NEXT REQUIRED STEP:
Before the implementation plan exposes controlled-subprocess test syntax, ask one prerequisite
prediction: if the test temporarily replaces `subprocess.run` with a stand-in that returns a prepared
result, whether the operating system starts a real Git child process. Record the answer before
showing mock/patch syntax.

CONTROLLED-STAND-IN PREDICTION ANSWER (verbatim):

```text
no, but the beginner mechanism is waht we need to make sure works before intorducing a child process
```

EVALUATION:
PASS WITH PRECISION. No real Git child starts when the test substitutes a stand-in for
`subprocess.run`. The learner correctly values stabilizing the simpler parent-side mechanism first.
Precision: the controlled test proves how BuildLens constructs and interprets the boundary call; it
does not prove operating-system launch or real Git behavior. That evidence comes from the deferred
real-Git integration test.

NEXT REQUIRED STEP:
Ask for one fact the controlled test can prove and one fact it cannot prove. After that passes, show
the smallest `unittest.mock.patch` syntax needed by the implementation plan.

CONTROLLED-TEST EVIDENCE ANSWER (verbatim):

```text
that the subprocess run when called will return the stand in, so when we want to call a child process which we cannot prove it can call git yet, but it will attempt to call the chile process
```

EVALUATION:
PASS WITH PRECISION. The learner identifies that the controlled call returns the prepared stand-in
result and that the test cannot prove real Git launch. The stand-in's recorded call can prove that
BuildLens attempted the expected invocation; a later integration test must prove the operating-system
and real-Git path.

NEXT REQUIRED STEP:
Show one minimal `with patch(..., return_value=prepared) as fake_run:` example. Explain only that the
replacement is active inside the indented block and that `fake_run` records calls. Ask what value the
function receives from `subprocess.run` inside the block.

SESSION PAUSE — 2026-09-02:
The learner needed to move locations and requested a commit and push. Resume at the exact minimal
`mock.patch` syntax check above. Do not skip to implementation-plan code or Phase 7 product code.

MINIMAL MOCK.PATCH TRACE ATTEMPT 1 ANSWER (verbatim):

```text
the git adapter that is the subprocess but not the actaul git subprocess, after the phase 7 implementation we are going to move ot a new session, 90
```

EVALUATION:
PARTIAL. The learner correctly explains that the call reaches the patched Git-adapter stand-in and
does not launch a real Git child. The exact value assigned to `received` was not supplied.

PRIMARY BLOCKER:
Tracing `return_value=prepared` through the replacement call to the assignment target.

SESSION TRANSITION REQUEST:
After Phase 7 implementation is complete, move to a new session. Do not transition before the Phase
7 automated tests, learner trace, explanation, transfer, and required completion gate are finished.

NEXT REQUIRED STEP:
Re-show only `prepared = "controlled result"`, `return_value=prepared`, and
`received = ...`. Ask for the exact value of `received`; do not re-ask process semantics.

PATCHED RETURN-VALUE REMEDIATION ANSWER (verbatim):

```text
it is the controlled result, so when the git subprocess actually works recieved will recieve the git diff etc, does that mean recived is a record type?
```

EVALUATION:
PASS for the exact toy value: `received == "controlled result"`.

SYNTAX/REPRESENTATION QUESTION:
The learner asks whether the received value is a record type in real execution. The toy example was
ambiguous because it replaced `subprocess.run` with a string directly. In the actual adapter,
`subprocess.run` returns a `CompletedProcess` record-like object containing `stdout`, `stderr`, and
`returncode`; `capture_unstaged_diff` extracts and returns the `stdout` string. This preserves the
approved validated-plain-string downstream boundary.

NEXT REQUIRED STEP:
Show `process_result = subprocess.run(...)` followed by `diff_text = process_result.stdout`. Ask
which variable is the `CompletedProcess` and which is the string.

SUBPROCESS-RESULT/STRING MAPPING ANSWER (verbatim):

```text
the completedprocesss is held by process result and the diff text holds the string
```

EVALUATION:
PASS. `process_result` references the `CompletedProcess`; `diff_text` references the stdout string
extracted from that object. The learner correctly distinguishes the subprocess boundary value from
the adapter's downstream return value.

NEXT REQUIRED STEP:
Show a realistic controlled test where `prepared` is a `CompletedProcess`, `patch` makes
`subprocess.run` return it, and `capture_unstaged_diff` returns `prepared.stdout`. Ask for both return
values before exposing this pattern in the implementation plan.

REALISTIC CONTROLLED-TEST TRACE ATTEMPT 1 ANSWER (verbatim):

```text
it returns the diff text&#x20;
it would get the diff for any unstaged files
90
```

EVALUATION:
PARTIAL. The second answer has the correct adapter-output intent; in this controlled example its
exact value is `"DIFF TEXT"`. The first answer incorrectly skips the intermediate object. Patched
`subprocess.run` returns `prepared`, which is the `CompletedProcess`; `capture_unstaged_diff` then
extracts `prepared.stdout`.

PRIMARY BLOCKER:
Maintaining the two distinct return boundaries when both appear in realistic `patch` syntax.

ADAPTATION:
Remove the adapter call and ask only what `return_value=prepared` makes the patched function return.

NEXT REQUIRED STEP:
Show `prepared = CompletedProcess(...)` and `return_value=prepared`. Ask only what patched
`subprocess.run(...)` returns.

ISOLATED PATCHED-RETURN ANSWER (verbatim):

```text
the object from completedprocess
```

EVALUATION:
PASS. The patched `subprocess.run(...)` returns the prepared `CompletedProcess` object.

NEXT REQUIRED STEP:
Rebuild the full trace once without answer labels: patched subprocess call → local `process_result`
→ `.stdout` → adapter return. Ask for the type/value at each boundary.

FULL CONTROLLED-RESULT TRACE ANSWER (verbatim):

```text
it hold the recordtype which has all the results from git diff if it were in a real git child process, the adapter returns "DIFF TEXT"
```

EVALUATION:
PASS. `process_result` holds the prepared `CompletedProcess`, and the adapter returns its exact stdout
string `"DIFF TEXT"`. The two-step remediation chain is closed.

COMPLETEDPROCESS TYPE QUESTION (verbatim):

```text
but what type is completeed process
```

FACILITATOR CLARIFICATION:
`CompletedProcess` is a class defined by Python's `subprocess` module. A value returned by
`subprocess.run` is an instance of that class with named attributes including `args`, `returncode`,
`stdout`, and `stderr`.

RETURNCODE ATTRIBUTE TYPE ANSWER (verbatim):

```text
that makes returncode an integer object inside a processresult object, 90
```

EVALUATION:
PASS WITH PRECISION. `process_result` is a `CompletedProcess` object, and its `returncode` attribute
references an integer object. More precisely, attributes refer to objects rather than objects being
physically nested “inside” one another.

OBJECT-REFERENCE QUESTION (verbatim):

```text
so are they all objects? and they exst as objects inside of eachother?
```

FACILITATOR CLARIFICATION:
Python values here are objects. The `CompletedProcess` has attributes that refer to the argument-list,
integer, and string objects. `diff_text = process_result.stdout` makes `diff_text` refer to the stdout
string, not to the surrounding `CompletedProcess`.

STDOUT-REFERENCE ANSWER (verbatim):

```text
it refers to only its string
```

EVALUATION:
PASS. `diff_text` refers only to the `.stdout` string. The object/attribute boundary is stable enough
for the controlled-subprocess test plan.

IMPLEMENTATION PLAN:
`docs/superpowers/plans/2026-09-03-phase-7-git-boundary.md`

PLAN SELF-REVIEW:
The initial draft overreached into every remaining Phase 7 slice. It was narrowed to the learner-
approved tracked-UNSTAGED patch only. The plan has exact interfaces, test code, implementation code,
commands, expected RED/GREEN outcomes, a post-GREEN learner gate, transfer, evidence update, and
commit boundary. Later Phase 7 requirements remain explicit but require fresh plans and gates.

NEXT REQUIRED STEP:
Ask the learner to review the first-slice plan, then choose subagent-driven or inline execution. Do
not execute either approach until the learner explicitly chooses.

SCOPE/OBJECT QUESTION (verbatim):

```text
so if you are referiung to an object that is inside a function that object is only able to be referered inside of that function and similarly if an object only exsts inside of a module you have to first refer/import to the module to then refer to that object
```

FACILITATOR CLARIFICATION:
Scope controls where a name binding is available, not where an object may exist. A function-local
name normally disappears after the function returns, but an object returned or stored elsewhere can
remain reachable. A module-level name is available through an imported module attribute or through a
direct import.

FUNCTION-LOCAL/RETURNED-OBJECT ANSWER (verbatim):

```text
the object istelf is refered to but the name of the obkject goes from localname to now weh nthe caller refers to it it will be outsidename
```

EVALUATION:
PASS WITH PRECISION. The caller's `outside_name` refers to the returned list object after the local
binding is gone. The object is not itself renamed; `local_name` and `outside_name` are separate name
bindings that exist in different scopes/times.

NEXT REQUIRED STEP:
Give one module access transfer: after `import git_adapter`, ask for the exact expression used to
refer to the module-level `capture_unstaged_diff` function. Then return to the plan execution choice.

OBJECT-BINDING PRECISION RESTATEMENT (verbatim):

```text
not renamed just refered to in a different way
```

EVALUATION:
PASS. The learner now states the precise principle: the object is not renamed; another name binding
refers to it.

MODULE ACCESS TRANSFER ANSWER (verbatim):

```text
gitadapter.captureunstageddiff()
```

EVALUATION:
PARTIAL. The module-qualified access structure is correct, but Python identifiers must match their
declared spelling exactly. The actual module is `git_adapter` and the function is
`capture_unstaged_diff`.

PRIMARY BLOCKER:
Exact underscore spelling in Python identifiers.

NEXT REQUIRED STEP:
Show `git_adapter.capture_unstaged_diff()` and ask the learner to reproduce that exact expression.

EXACT IDENTIFIER ATTEMPT 1 ANSWER (verbatim):

```text
git\_adapter.capture\_unstaged\_diff()
```

EVALUATION:
PARTIAL. Every underscore is now correctly placed, but the literal backslashes used to escape
underscores in Markdown would be invalid Python syntax. The source expression contains `_` directly.

NEXT REQUIRED STEP:
Ask the learner to enter the expression inside a Python code block with no backslashes.

EXACT IDENTIFIER ATTEMPT 2 ANSWER (verbatim):

```text
git\_adapter.capture\_unstaged\_diff()
```

EVALUATION:
FORMATTING-AMBIGUOUS. The identifier structure and underscore placement remain correct, but the
response again contains Markdown escapes. Do not infer continued Python misunderstanding from a
formatting-sensitive input loop.

ADAPTATION:
Descend to one binary R0 syntax question: whether Python source contains a backslash before `_`.

NEXT REQUIRED STEP:
Ask only whether the backslash belongs in the Python source expression: yes or no.

LEARNER SKIP REQUEST (verbatim):

```text
skip this it is a nitpick
```

EVALUATION:
SKIPPED BY LEARNER REQUEST. The module-dot-function access structure and underscore positions were
correct. The remaining ambiguity was Markdown presentation rather than a load-bearing Phase 7
concept, so no further remediation is required.

NEXT REQUIRED STEP:
Return to the saved first-slice implementation plan and ask the learner to choose subagent-driven or
inline execution. Do not implement until the choice is explicit.

PLAN EXECUTION CHOICE (verbatim):

```text
1, i want to learn how it is done
```

EVALUATION:
Inline execution selected. Preserve every RED/GREEN and learner checkpoint in this session; do not
delegate implementation.

WORKTREE SETUP REQUEST (verbatim):

```text
ok can you commit and push and then we will work on an isolated worktree
```

EVALUATION:
Approved. Commit and publish the planning/evidence checkpoint, then create an isolated worktree on
`codex/phase-7-unstaged-capture`. Verify the clean baseline before writing the failing test.

NEXT REQUIRED STEP:
Commit and push the documentation checkpoint, establish the isolated worktree safely, run the four
existing suites there, then resume Step 2 of the first-slice plan: the learner predicts the controlled
subprocess call before any test code is written.

---

## EV-P7-PREPATCH-CALL-282 — pre-patch real subprocess call prediction

BASELINE:
Worktree `codex/phase-7-unstaged-capture` created at `C:/Users/nicol/BuildLens_wt/phase-7-unstaged-capture`.
All four existing suites passed there on 2026-09-03 before any Phase 7 code.

EXACT PROMPT:
Read this call and say what each part does. The function body is deliberately not shown.

```text
process_result = subprocess.run(
    ["git", "diff", "--no-ext-diff", "--no-color", "--"],
    cwd=repository,
    capture_output=True,
    text=True,
    timeout=10,
    shell=False,
)
```

Call:

```text
capture_unstaged_diff(Path("C:/projects/example"))
```

Fill in every field:

```text
Executable that is launched =
Arguments passed to that executable =
Child process working directory =
What capture_output=True plus text=True make available, and as what type =
What happens if the child has not finished after 10 seconds =
Type/kind of object stored in process_result =
Value that capture_unstaged_diff returns to its caller =
Confidence =
```

FIRST COMMITTED ANSWER (verbatim):

```text
. this is the real subprocess, before we tested a test subprcess to make sure we could call the
subprocess and to teach me that each subporcess calls a completed reuslt object that refers to ither
objects inside of it, like the cwd caputre output and text,
```

EVALUATION:
ORIENTING STATEMENT, NOT A FIELD ANSWER. No confidence supplied. Two separable parts:

- CORRECT: this is the real production call; the earlier controlled stand-in proved call construction
  and result interpretation, not operating-system launch or real Git behavior.
- INCORRECT: `cwd`, `capture_output`, and `text` were named as objects the returned
  `CompletedProcess` refers to. They are keyword arguments supplied TO `subprocess.run`, not fields
  read back off the returned object.

PRIMARY BLOCKER:
Separating arguments passed into a call from the fields stored on the object that call returns.

ADAPTATION:
Descend below subprocess to one generic call whose keyword inputs and returned record fields are
deliberately different names. Do not re-ask the seven-field subprocess prediction yet.

NEXT REQUIRED STEP:
Ask only which names are inputs to the call and which names are fields on the returned object, on
the reduced non-subprocess surface.

### EV-P7-PREPATCH-CALL-282A — reduced inputs-versus-returned-fields surface

PROMPT (non-subprocess `measure`/`Reading` surface): name the call's inputs, the fields on the
returned object, whether `result.units` exists, and the expression reading the measured number.

ANSWER (verbatim):

```text
."bolt_A", units="cm", strict=False go into the call as the input, i have no idea, i have no idea,
i have no idea
```

EVALUATION:
PARTIAL. Inputs correct. Three remaining fields unknown; they collapse to one blocker — knowing
which fields a returned object actually has.

ADAPTATION:
Descend to R0: one class, one attribute, no function wrapper.

### EV-P7-PREPATCH-CALL-282B — R0 single-attribute read

PROMPT: for `class Ticket` with `self.number = number` and `t = Ticket(7)`, name the field created
and the expression reading 7 back.

ANSWER (verbatim):

```text
. it has a number on it, it is self.number for this ticket instance, we would have to write a
print(t) for it to print out 7 and to read it into 7 you have the t = teickjet(7)
70
```

EVALUATION:
PARTIAL at confidence 70. Field name correct. Reading expression incorrect: construction
(`t = Ticket(7)`) and `print(t)` were given instead of an attribute expression. `print(t)` prints the
object, not 7.

ADAPTATION:
Narrow to one blank at the same rung: `t.______`.

NARROWED ANSWER (verbatim):

```text
t.number
90
```

EVALUATION:
PASSED at confidence 90.

### EV-P7-DEFAULT-PARAMETERS-283 — syntax-only help, default parameter values

LEARNER QUESTION (verbatim):

```text
. what is throwing me off is that the inputs for scan are deep=true and timeout=30, how are they
inputs if they have a value already?
```

EVALUATION:
Genuine syntax prerequisite, not a distraction. Syntax-only help activated: `name=value` in a `def`
line is a default used when the caller leaves the argument out; the same shape in a call line is the
caller supplying a value, which wins.

PROMPT: for `def brew(bean, strength=3)`, predict `brew("kona")`, `brew("kona", strength=9)`, and say
what 3 is used for.

ANSWER (verbatim):

```text
. it prints kona, the seoncd call prints kona and 9, 3 could be a placeholder or to show the caller
it is an integer object
90
```

EVALUATION:
PARTIAL at confidence 90. Second call correct. First call omitted the printed `3`. The default was
described as a placeholder or type signal rather than the value actually bound.

ADAPTATION:
Narrow to one blank: `kona ____`.

NARROWED ANSWER (verbatim):

```text
kona,3, so it would also be there as a placeholder if the caller has no other input
```

EVALUATION:
PASSED on behavior. Wording refined: the default is not a stand-in, it IS the value the parameter
holds for that call.

FOLLOW-UP QUESTION (verbatim):

```text
.so it is 3 unless you input another integer value?
```

EVALUATION:
CORRECT with one precision supplied: the caller's value need not be an integer. The default
communicates intent but does not validate — the same annotation-versus-runtime-validation
distinction already held on `Session.record`.

VOCABULARY:
"Omit" was asked again and re-defined as "leave out." Second occurrence; prefer "leave out" in
future prompts.

### EV-P7-PREPATCH-CALL-282C — rebuilt scan/Batch target

ANSWER (verbatim):

```text
. folder, deep=True, timeout=30, /logs", deep=False, timeout=5, yes it is 5, b.count, 90
```

EVALUATION:
PARTIAL at confidence 90. Inputs and `b.count` correct. `b.timeout` was said to exist with value 5 —
the exact target misconception: a call's arguments were treated as fields on the object that call
returned.

ADAPTATION:
Isolate the prerequisite — field names come only from the `self.` lines in the object's own
`__init__`. Present `Batch` with `scan` removed.

PREREQUISITE ANSWER (verbatim):

```text
.  it has a count and a label, self.count and self.label
90
```

EVALUATION:
PASSED at confidence 90.

REBUILT TARGET ANSWER (verbatim):

```text
. no it only has a timeout inside of scan once scan has returned batch then timeout is not there
regardless b has no timeout, 90
```

EVALUATION:
PASSED at confidence 90. The learner independently used parameter locality and lifetime: `timeout`
is local to `scan` and gone after it returns, so `b` carries only what `Batch.__init__` set. This
correctly reuses the earlier scope-controls-names-not-object-lifetime recovery.

CHAIN STATUS:
CLOSED. Call arguments versus returned-object fields is recovered on a non-subprocess surface.

NEXT REQUIRED STEP:
Re-present the original seven-field real-`subprocess.run` prediction from EV-P7-PREPATCH-CALL-282.
No Phase 7 product code exists.

### EV-P7-PREPATCH-CALL-282D — first full target attempt on the real call

ANSWER (verbatim):

```text
. subprocess.run, the path, not sure, it makes the output of the subprocess available and it is a
string, you get a timeout error, it is a subprocess object, it returns a string that is the unstaged
diff fro mthe path, 50
```

EVALUATION:
PARTIAL at confidence 50, well calibrated. PASSED: captured output available as strings; timeout
produces a timeout error (`subprocess.TimeoutExpired` named correctly on an earlier surface); adapter
returns the diff text as a string. FAILED: the launched executable was given as `subprocess.run`
(the Python function doing the launching, not the program launched); arguments were given as "the
path"; child cwd unknown. `process_result` type was imprecise.

PRIMARY BLOCKER:
Reading an argument list — element 0 is the program, the rest are its arguments — and separating that
from the Python function performing the launch.

### EV-P7-ARGV-LIST-284 — argument-list role reading

REDUCED SURFACE: `subprocess.run(["zip", "-r", "backup.zip", "notes"], cwd=folder)`

ANSWER 1 (verbatim):

```text
. process result is a record type object, run, subprocess, ["zip", "-r", "backup.zip", "notes"],
cwd=folder, folder, 60
```

EVALUATION:
Field mapping ambiguous; not graded as a whole. `process_result` repaired to "record type object".
`cwd=folder` → `folder` correct. Program/arguments split unresolved.

NARROWED ANSWER (verbatim):

```text
. -r
20
```

EVALUATION:
FAILED at confidence 20. `-r` is an option, not the program name.

ADAPTATION:
Worked-example rescue on a command the learner types daily: `python test_cli.py` as
`["python", "test_cli.py"]`.

WORKED-EXAMPLE EXPLANATION (verbatim):

```text
. python is where the program is launched and testcli is the argument that is handeed to it, it is
argv[1], 90
```

EVALUATION:
PASSED at confidence 90. Naming index 1 as `argv[1]` is apt — the list becomes the child's argv.

MISSING-STEP ANSWER (verbatim, after one restatement):

```text
. -x adn archive.tar, i assume -x is the command or action and archive.tar is the path, 90
```

EVALUATION:
PASSED at confidence 90 after the first attempt repeated the supplied program name `tar` into the
arguments slot. Roles of option and operand were read correctly.

FRESH UNAIDED ANSWER (verbatim):

```text
.  zip
["zip", "-r", "backup.zip", "notes"], cwd=folder
folder
90
```

EVALUATION:
PARTIAL. Program and cwd correct; the arguments field still included the program and the `cwd`
keyword.

LEARNER QUESTION (verbatim):

```text
ok so i would remove zip and folder as arguments because we already used them in the call?
```

EVALUATION:
Correct exclusions, wrong reason. Corrected to role: a program is not handed to itself, and `cwd`
is an instruction to `subprocess.run` that the child program never receives as an argument. The
learner restated the role-based reason correctly, then committed `"-r", "backup.zip", "notes"`.
PASSED. Rescue sequence complete.

### EV-P7-PREPATCH-CALL-282E — narrowed target retry

ANSWER (verbatim):

```text
. git
"diff", "--no-ext-diff", "--no-color", "--"
repositiory
record type
90
```

EVALUATION:
PASSED at confidence 90 on program, arguments, and child cwd. Spelling treated as transcription
noise. The exact class name remained unretrieved.

### EV-P7-COMPLETEDPROCESS-285 — returned class name

ANSWER 1 (verbatim):

```text
subprocess.run
90
```

EVALUATION:
FAILED. The called function was named instead of the returned object's class.

ADAPTATION:
Return to the already-passed `Batch`/`scan` surface.

ANSWER 2 (verbatim):

```text
. it is a processresult object
```

EVALUATION:
FAILED — recurrence of the documented procedural blocker: carrying a previous scenario into a new
program. `processresult` appears nowhere in the shown code. Full code restated with no omissions,
which has cleared this blocker every prior time.

R0 ANSWER (verbatim):

```text
. batch
```

CLIMB ANSWER (verbatim):

```text
. batch
class batch
100
```

EVALUATION:
PASSED at confidence 100. Precision added: `class Batch` establishes the class; `return Batch(...)`
is the line establishing what `scan` hands back. For `subprocess.run` the body is unreadable, so the
return type comes from documentation — the same source rule already used for `SystemExit.code`.

TARGET RETRY (verbatim):

```text
. subprocess object
30
```

EVALUATION:
NOT RETRIEVED at confidence 30, honestly calibrated. The concept (returned record-like object with
its own fields, distinct from the function called) is held; only the proper noun was missing.
Supplied rather than drilled, with live evidence from a real Git child run in the isolated worktree:

```text
class name : CompletedProcess
fields     : ['args', 'check_returncode', 'returncode', 'stderr', 'stdout']
returncode : 0
stdout     : ''
```

The field list independently confirms the original EV-P7-PREPATCH-CALL-282 correction: `cwd`,
`capture_output`, and `text` are inputs and do not appear on the returned object.

WATCH ITEM:
`CompletedProcess` as a name requires one delayed retrieval on a fresh surface before Phase 7 closes.
The underlying distinction does not need re-teaching.

CHAIN STATUS:
EV-P7-PREPATCH-CALL-282 is CLOSED after remediation, not as a first-attempt pass. Plan Step 2 is
satisfied.

NEXT REQUIRED STEP:
Plan Step 3 — write `test_git_adapter.py` as the failing controlled-subprocess test and verify RED
before `git_adapter.py` exists.

## EV-P7-ADAPTER-RED-GREEN-286 — first Phase 7 product patch

RED (verbatim):

```text
ModuleNotFoundError: No module named 'git_adapter'
exit status 1
```

Observed before `git_adapter.py` existed, at the test's import line.

GREEN: `test_git_adapter.py` passed. All five suites pass in the worktree
`codex/phase-7-unstaged-capture`. `classify.py`, `summarize.py`, `session.py`, and `cli.py` unchanged.
NOT COMMITTED — plan Step 8/9 gates pending.

### EV-P7-PATH-BINDING-287 — argument binding and constructor calls

LEARNER QUESTION (verbatim):

```text
. also for the call is the path the repository or what is it ?
```

ATTEMPT 1 (verbatim):

```text
. ok so the repo is path
```

ATTEMPT 2 (verbatim):

```text
. it hold the value path not the args.path object, 90
```

EVALUATION:
FAILED at confidence 90, miscalibrated. `args.path` belongs to a different program — recurrence of
the carry-over blocker.

ADAPTATION AND FACILITATOR ERROR:
Descended to `greet("Ada")`, then `show(str(42))`. Both passed. The `str(42)` choice was a PROMPT-
DESIGN ERROR: a constructor returning a string was used immediately before asking about a constructor
returning a Path, signalling the wrong answer shape.

LEARNER OBJECTION (verbatim):

```text
. so my orginal assumption was correct and you let me down a rabbit hole for no reason, i assumed
that path was an object and you led me to beleive it was a string which started all of this, maybe i
should have stopped you earlier on me, path is a path object that has the value C:/projects/example
as a string and the repo hold that as a value object, 90
```

EVALUATION:
PASSED, and the objection is PARTLY UPHELD. The `str(42)` example did signal "string." The descent
itself was justified by the ambiguous attempt 2. Precision added: the Path object is not a string
with extras; the string is its underlying representation.

STANDING INSTRUCTION ADOPTED:
When descending toward a constructor call, do not use a constructor whose result is a different type
than the target. The learner is explicitly invited to halt a descent when they already hold the
concept; assistance must fade.

FURTHER QUESTION (verbatim):

```text
. is it the same way path could be the key and the lookup value is C:/projects/example
```

EVALUATION:
Correctly rejected. `Path` is a class being called to construct a new object, not a key into a
lookup table. Counter-evidence supplied: `Path("does/not/exist")` succeeds with no table to find,
and two identical calls build two objects.

### EV-P7-ADAPTER-TRACE-288 — post-GREEN learner trace

ANSWER (verbatim):

```text
. git is launched and it starts in "C:/projects/example"
a completedprocess obejct and the return code is 0
it is entered if there is a git failure status
processresult returns the standard output which would be the unstaged diff text as a string
90
```

EVALUATION:
STRONG PARTIAL at confidence 90. Program, child directory, returned object, returncode, and returned
string all correct. `CompletedProcess` was retrieved UNAIDED, closing the EV-P7-COMPLETEDPROCESS-285
watch item on first delayed retrieval. Field 3 stated the general rule instead of this run's outcome —
the same capability-versus-this-call pattern seen earlier in the session.

NARROWED ANSWER (verbatim):

```text
. it is not entered for this run since it passed
90
```

EVALUATION:
PASSED. Precision added: `0 != 0` evaluates to the literal `False`.

TRACE STATUS: CLOSED.

### EV-P7-ADAPTER-BOUNDARY-289 — boundary explanation and design defense

ATTEMPT 1 (verbatim):

```text
. becauwe that is the git adapters responsilbity and we nned to uphold the boudary, we would need to
write the git adapter subprocess into summarize.py, that we are on the right track in terms of
boundary and repsosiblity, 90
```

EVALUATION:
PARTIAL. Field 1 CIRCULAR — named the boundary as its own justification, which the design-review
rubric does not accept. Field 2 answered the inverse question.

NARROWED ANSWER (verbatim):

```text
. string
no
we would have to make sure that the git ouptut is properly formatted for summarize.py
90
```

EVALUATION:
Fields 1-2 PASSED. Field 3 substituted the data contract for the line count. The data-validity
instinct is CORRECT and correctly belongs to the adapter — it is the next planned slice.

REDUCED TWO-CALLER ANSWER (verbatim):

```text
. no, as long as the text from git is still serpated on lines by \n
```

EVALUATION:
PASSED. Zero lines of `summarize.py` change. The learner independently named the real content
contract — newline-separated unified-diff text — and correctly located it as the adapter's
obligation rather than a check inside `summarize_diff`.

DEFENSE ANSWER (verbatim):

```text
. we have to check to see where the string we are putting into summarize came from
that the 2 inputs are giving a string that can still be digested by summarze and give a correct output
not sure
90
```

EVALUATION:
Fields 1-2 PASSED. Sharper cost supplied: with the subprocess inside `summarize.py`, testing the
counting logic would require launching or faking a Git child, where `test_summarize.py` currently
runs a pure function on a string with no repository and no Git installed.

ADVERSARIAL FIELD:
`not sure` twice. Scaffolded with an explicit World A / World B choice after linking to the learner's
own Phase 4 evidence-based decision not to create packages.

ANSWER (verbatim):

```text
.  if git was the only input, then we can assume that every input comes from gitand a real repo
exsits and plan only for that, 90
```

EVALUATION:
PASSED. World A. A single permanent input source makes the adapter an option nobody exercises.

CLOSING ANSWER (verbatim):

```text
. world b we have 2 inputs and have to check each to make sure that there is something that exsts in
each
```

EVALUATION:
PASSED on the load-bearing field — BuildLens has two input sources today with more planned. The
"check each" clause is loose; the decisive fact is source multiplicity plus Git-free testability.

GATE STATUS:
Plan Step 8 CLOSED after remediation. Reversal condition required explicit scaffolding and is NOT
yet independently generated — carry it forward.

NEXT REQUIRED STEP:
Plan Step 9 — one non-Git transfer: a parent program running a formatter child, receiving a completed
result, rejecting an unexpected status, and returning stdout text. The learner must distinguish the
subprocess result object from the adapter's returned string. Commit only after it passes.

### EV-P7-ADAPTER-TRANSFER-290 — non-Git formatter-child transfer

SURFACE: `format_source(project_dir)` running a `blackline` formatter child, raising `FormatError`
on nonzero status and returning `outcome.stdout`. No Git, new names, timeout 20.

ANSWER (verbatim):

```text
blackline
"--stdout", "--quiet", "src"
project_dir
completedprocess object
no
it returns outcome.stdout it is a string "FORMATTED SORUCE"
i do not know
80
```

EVALUATION:
SIX OF SEVEN PASSED UNAIDED at confidence 80 on an unseen surface. Program, arguments, child
directory, returned class, this-run branch outcome, and returned value/type all correct. Notably
clean on both procedural patterns flagged the previous session: no carry-over from the Git program,
and the branch field answered THIS run rather than restating the rule.

Field 7 — what the function does NOT hand back — unknown.

NARROWED ANSWER (verbatim):

```text
. it is only handed back the string that is the stdout not the entire outcome object
```

EVALUATION:
PASSED. One further field requested.

ANSWER (verbatim):

```text
. the return code
70
```

EVALUATION:
PASSED. The learner independently named the exact field their own approved reversal condition
depends on.

### EV-P7-ADAPTER-PRINCIPLE-291 — shared principle and unscaffolded reversal condition

FIRST ANSWER (verbatim):

```text
. they both run a subprocess using arguemtns that are similar they both have a returncode that tells
you if the subprocess was succesful or a failure
they both only give the string that is neededd for cli to then pass the string and get the count from
summarize
i am not sure
70
```

EVALUATION:
PARTIAL. The first clause described surface similarity rather than the deep principle, and the
second stated the principle in BuildLens-specific terms that do not survive the surface change.
Reversal condition unknown despite having produced its key ingredient one turn earlier.

NARROWED ANSWER (verbatim):

```text
. they run a program using arguements and then return a string, they do not return the returncode
whic h could be a later issue if the user requires the exact exti status of git, the change that
would be needed would be that we would need to retunr more than just the string and the functuion
call would then have to be called again to get the string and the return code
90
```

EVALUATION:
PRINCIPLE PASSED — stated without naming Git, cli, or summarize. Reversal trigger and change
direction correct. One clause wrong: a second call to obtain the return code.

SELF-CORRECTION (verbatim):

```text
no the function the callers object so it would be top = format_source(Path("D:/work/reports")) and
then we would need to run top.returncode and top.returnedstring
```

EVALUATION:
PASSED, self-corrected without being told the answer. One call returning a structured object whose
fields the caller reads — the `ImageResult` shape from the original design decision. Field naming
refined: a declared field such as `diff_text`, not `returnedstring`.

Precision supplied after the learner had already moved past it: two calls launch Git twice, so a
displayed return code could belong to a different run than the counted diff — two snapshots reported
as one.

CARRIED-FORWARD ITEM CLOSED:
The adapter reversal condition was generated WITHOUT the World A / World B scaffolding, satisfying
the debt recorded against EV-P7-ADAPTER-BOUNDARY-289. It required one correction, so it is not a
clean first-attempt pass.

GATE STATUS:
Plan Step 9 CLOSED. Task 1 of the first-slice plan is complete in every required dimension:

```text
implementation       complete
automated tests      complete — five suites pass
learner trace        complete — EV-P7-ADAPTER-TRACE-288
learner explanation  complete — EV-P7-ADAPTER-BOUNDARY-289
transfer variant     complete — EV-P7-ADAPTER-TRANSFER-290, EV-P7-ADAPTER-PRINCIPLE-291
```

NEXT REQUIRED STEP:
Commit the completed patch. The next Phase 7 slice is STAGED capture, then untracked discovery with
`/dev/null` new-file diffs, then multi-command composition, then CLI integration. Launch failure and
timeout normalization remain deferred to their own slice.

## EV-P7-STAGED-DESIGN-292 — duplication versus parameterization at the adapter boundary

PROMPT: choose between two full near-duplicate capture functions (Option A) and one shared `_capture`
helper called by two thin public functions (Option B); state the cost accepted and the reversal
condition.

FIRST ANSWER (verbatim):

```text
. i like oiption b it makes iut so we call git one time and only then do we spilt the sanoshot into
unstaged asnd staged, the cost would be we would have to difreretiate the 2 from eachother, not sure 80
```

EVALUATION:
CHOICE PLAUSIBLE, REASON WRONG. Option B shares the Python function body, not the Git run. `_capture`
is called twice and reaches `subprocess.run` twice. Sharing code reduces how many times something is
WRITTEN, never how many times it RUNS.

ADAPTATION:
Isolate definition-versus-execution with `stamp()` called twice.

MICRO ANSWER (verbatim):

```text
. ran is printed twice
twice
80
```

then, narrowed to the def-line count:

```text
1
```

EVALUATION:
PASSED. One definition, two executions.

REBUILT COUNT (verbatim):

```text
. option a is 2 git child ... and option b is the same
90
```

EVALUATION:
PASSED. Two Git children under both options. The original reason was voided and the decision reopened.

LEARNER QUESTION (verbatim):

```text
. i am still leaning towards option a then because im not sure the purpsoe of capture then
```

EVALUATION:
Legitimate. The purpose of an extracted helper only appears under CHANGE. Reframed as a concrete
timeout change from 10 to 30 seconds affecting both captures.

RESOLVING ANSWER (verbatim):

```text
wait, are you saying that the capture is the function that calls the git subporcess and the 2
capturediff  functions call the capture and then differentiate based on unstaged and staged, if that
is the case then b is the correct answer, if i want something to change in the subprocess i can then
make one change instead of 2 it is more convienent
```

EVALUATION:
PASSED. Structure understood and the correct benefit named. Sharpened beyond convenience: under
Option A the two bodies can DRIFT, so UNSTAGED and STAGED could run under different contracts while
both claiming to be one snapshot — a correctness risk, not a typing cost.

COST AND REVERSAL (verbatim):

```text
. so leading underscore most likely means a helper function, it would have to not raise on certain
status, if the number of changes to _capture and the paramters grow to much, but i assume for this
project it will not
90
```

EVALUATION:
PASSED. The learner independently read the leading underscore as an internal-helper convention, and
correctly predicted that the coming untracked slice forces `_capture` to stop raising on every
nonzero status. Reversal condition stated as parameter and branch accumulation. Precision added: the
underscore is convention, not enforcement — the same supported-API-versus-language-guarantee
distinction already held for `_changes` in `session.py`.

The indirection cost was SUPPLIED, not generated: a reader must follow one extra hop to learn what
`capture_staged_diff` does.

DECISION: Option B.

## EV-P7-STAGED-RED-GREEN-293 — staged capture patch

RED (verbatim):

```text
ImportError: cannot import name 'capture_staged_diff' from 'git_adapter'
exit status 1
```

Distinguished from the previous slice's `ModuleNotFoundError`: the module now exists, the name inside
it does not.

GREEN: four adapter tests pass; all five suites pass. The two PRE-EXISTING unstaged tests passed
unchanged after the body moved into `_capture`, which is the evidence the refactor preserved behavior.

### EV-P7-STAGED-TRACE-294 — post-GREEN trace

FIRST ANSWER (verbatim):

```text
. so the repository is the path/cwd, the etraargs is the differentiator for whether you are calling
capture for unstaged or for staged, label is the string that will tell you what we are looking for/
which function we are calling _capture from
```

EVALUATION:
ROLES CORRECT, FIELDS UNANSWERED. Third occurrence this session of describing what something is FOR
instead of what it IS on this call. Pattern named explicitly to the learner for self-correction.

`extra_args` for the unstaged caller was then given exactly as `[]` at confidence 90.

LIST CONCATENATION (new syntax) — FIRST ANSWER (verbatim):

```text
.["git", "diff", "--no-ext-diff", "--no-color"] + []+ ["--"]
3
90
```

EVALUATION:
FAILED. The expression was restated with the variable substituted but never evaluated; the count was
wrong.

R0 ANSWER (verbatim):

```text
. [1,2,3,]
3
so for the git diff it would be 6 elements inside the list
```

EVALUATION:
R0 PASSED. The generalization named the staged count while the line under discussion was the unstaged
one. After the per-part element counts were laid out, the learner self-corrected:

```text
. ok so for the unstaged it is 5 and 6 is for the staged
```

FINAL LISTS (verbatim):

```text
["git", "diff", "--no-ext-diff", "--no-color", "--"]
["git", "diff", "--no-ext-diff", "--no-color","--cached", "--"]
```

EVALUATION:
PASSED, exactly matching both test assertions.

### EV-P7-MESSAGE-ASSEMBLY-295 — error message construction

FIRST ANSWER (verbatim):

```text
.  not a repository
": Git failed with status "
    + str(process_result.returncode) + not a repository
not sure
20
```

EVALUATION:
FAILED at confidence 20, well calibrated. `detail` dropped the `fatal:` prefix, and the concatenation
was restated rather than evaluated.

`.strip()` isolated as syntax-only help. ANSWER (verbatim):

```text
.  fatal: not a repository
no
90
```

PASSED — strip removes surrounding whitespace only.

String concatenation was restated unevaluated a second time. The learner then said:

```text
ok i know what it evaluates to i was being lazy
```

This claim was ACCEPTED and tested directly on the real target rather than drilled, because every
reduced form had been evaluated correctly and immediately. Noted to the learner that an unevaluated
expression is indistinguishable from not knowing, and costs turns.

TARGET ANSWER (verbatim):

```text
. staged tracked: git failed with status 128
90
```

EVALUATION:
PARTIAL. First assignment exact; the `if detail:` body was not applied. Truthiness of a non-empty
string was supplied as the one missing rule.

FINAL ANSWER (verbatim):

```text
.staged tracked: git failed with status 128: fatal: not a repository
```

EVALUATION:
PASSED, matching the test assertion. Capitalization treated as transcription noise.

RECURRING PATTERN TO WATCH:

```text
restating an expression with variables substituted, instead of evaluating it to a value
```

Appeared on both list and string concatenation in the same session. Reduced forms were always
evaluated correctly.

GATE STATUS:
Staged-capture slice CLOSED. This is a slice, not a phase milestone; the Phase 7 milestone transfer
is owed at phase close.

NEXT REQUIRED STEP:
Untracked discovery slice: path discovery plus `git diff --no-index -- /dev/null <path>`, where
status 0 and status 1 are BOTH valid. This forces `_capture` to accept a per-caller status rule and
is the concrete test of the reversal condition recorded in EV-P7-STAGED-DESIGN-292.

### EV-P7-UNTRACKED-DESIGN-296 — PRESENTED, NOT ANSWERED

SESSION INTERRUPTION: the learner reported a possible battery failure and requested commit/push
before answering. The prompt below was presented and is UNATTEMPTED. It must not be graded, and its
answer must not be revealed on resumption.

The untracked work was split in two because it carries two new ideas. This patch is path discovery
only; the `--no-index` accepted-status rule is a separate later patch.

EXACT PROMPT:

```text
git ls-files --others --exclude-standard
```

prints one untracked path per line and exits 0.

`_capture` currently hard-codes:

```text
["git", "diff", "--no-ext-diff", "--no-color"] + extra_args + ["--"]
```

The new command shares `git`, `cwd`, `capture_output`, `text`, `timeout`, `shell`, and the
nonzero-is-failure rule. It does NOT share `diff`, `--no-ext-diff`, `--no-color`, or the trailing
`--`.

```text
Does capture_untracked_paths go through _capture, yes or no =
If yes, name what _capture must stop hard-coding =
If no, name what gets duplicated instead =
Which cost you would rather pay, and why =
Confidence =
```

CONTEXT FOR RESUMPTION:
This is the reversal-condition test the learner predicted in EV-P7-STAGED-DESIGN-292, arriving one
patch earlier than expected. They anticipated the pressure coming from the status rule; it arrives
first from the subcommand and argument shape instead.

NEXT REQUIRED STEP:
Re-present the prompt above verbatim. Do not implement before the learner's decision.

## EV-P7-UNTRACKED-DESIGN-296 — RESUMED AND CLOSED

FIRST ANSWER (verbatim):

```text
. yes, the arguemtns, not sure about the cost, it just makes sense to have the _capture be the
subprocess responsiblity
```

EVALUATION:
CHOICE AND REASON PASSED. The responsibility line was drawn well: `_capture` owns PROCESS MECHANICS
(launch, capture, timeout, status check), not WHICH Git command. Cost unknown.

The cost was posed concretely: with the full argument list pushed to callers, `_capture` no longer
guarantees `--no-color` / `--no-ext-diff`.

ANSWER (verbatim):

```text
no, if we need the arguemtns to be a certain way we have to input it that way or create soemthing
that will take the arguemtns in and test to see which list fo arguemtns it should use to run the
subprocesses
```

EVALUATION:
The exposure was named correctly. The second proposal — inspecting arguments to select a list —
would return command knowledge to `_capture` as a branch, undoing the extraction.

Two resolutions were offered. Resolution 1 (each caller writes its own full list) and Resolution 2
(`_diff_args` builds the shared diff flags; the ls-files caller bypasses it).

The learner chose Resolution 1 without naming its cost, then restated its benefit twice when asked to
count duplicate occurrences of `--no-color`. Descent to a literal counting task passed: 2 under
Resolution 1, 1 under Resolution 2.

The learner then said `but then why not just make it so that each of the 3 has their own` and
`i am not seeing it`. FACILITATOR JUDGMENT: Resolution 1 is genuinely defensible at two callers, and
this was stated plainly to the learner. The rubric requirement is naming the tradeoff, not choosing
Resolution 2. The drift failure was therefore SUPPLIED as a worked scenario: adding `--no-textconv`
to fix an external-diff-tool bug, editing one diff caller and missing the other, producing correct
UNSTAGED counts and wrong STAGED counts under one snapshot heading, with no crash.

The learner then answered `o fine lets do r2`, which was CHALLENGED as capitulation rather than a
decision, per the rubric's rejection of "Claude chose it."

RESOLVING ANSWER (verbatim):

```text
ok i read that incorrectly when you first presented them, do _diff_args would give the arguemtn that
would change the list in _capture from unstaged to staged, i think that is a good idea and it will
make it so if we need to make changes we have one place to llook instad of 3
```

EVALUATION:
PASSED as an own decision — the earlier choice rested on a misreading of Resolution 2. Precision
corrected: `_diff_args` is one place for the TWO diff callers; `capture_untracked_paths` never uses
it.

REVERSAL CONDITION (verbatim):

```text
. if we decided not to track unsatged or staged an only track one
```

EVALUATION:
PASSED, unscaffolded. One diff caller means nothing is shared and the helper stops earning its place.

DECISION: Resolution 2.

## EV-P7-UNTRACKED-RED-GREEN-297 — untracked path discovery patch

The untracked work was SPLIT because it carries two new ideas. This patch is path discovery only.

RED (verbatim):

```text
ImportError: cannot import name 'capture_untracked_paths' from 'git_adapter'
exit status 1
```

GREEN: seven adapter tests pass; all five suites pass. `_capture` was restructured to take the full
argument list and prepend `"git"` itself, and the four PRE-EXISTING tests passed UNCHANGED — the
second refactor-safety demonstration in this phase.

### EV-P7-UNTRACKED-TRACE-298 — output representation trace

FIRST ANSWER (verbatim):

```text
. so there is are 2 file in the notes folder new.py then the read.me
the string for the stdout or the diff text, is a list that has been splitlined so every entry is a
line of the output, wouldn't that mean there are no files in the repo?, not sure, 90
```

EVALUATION:
PARTIAL. Corrections supplied: `readme.md` is at the repository root, not in `notes/`; empty output
means no UNTRACKED files, not no files. The two return values were merged into one.

ANSWER (verbatim):

```text
. it is a processcompleted object and splitlines produces a list that has all of the outputs/ results
from the git subprocess, 90
```

EVALUATION:
FAILED on the first field — a regression on the distinction closed at EV-P7-COMPLETEDPROCESS-285.
`_capture` returns `process_result.stdout`, a string.

RECOVERED (verbatim):

```text
so it gets  a string that could be a few lines and then the splitlines turns that string into a list
with each \n seperating the entires, output is a string , 90
```

EXACT VALUES (verbatim):

```text
notes/new.py\nreadme.md\n
notes/new.py
readme.md
""
""
90
```

EVALUATION:
THREE OF FOUR PASSED, including the correct judgement that the trailing newline produces NO third
empty entry. `"".splitlines()` was given as `""`; corrected on one narrowed prompt to `[]` at
confidence 90.

### EV-P7-REPRESENTATION-CHOICE-299 — why the adapter chooses a list

ANSWER (verbatim):

```text
because ls-files returns a list of the files instead of a string
```

EVALUATION:
FAILED, and the correction is load-bearing for the boundary: `ls-files` returns a STRING, exactly as
`diff` does. No child process can hand Python a list. The list is BUILDLENS'S CHOICE, made by the
`.splitlines()` call. The adapter decides what representation crosses the boundary; Git supplies only
text.

ADAPTATION:
Descend to iteration shape — a loop over a list versus a loop over a string.

MICRO ANSWER (verbatim):

```text
. 2 lines
one line
90
```

FAILED on the string case. After the rule was supplied that a `for` over a string visits one
character at a time, the learner produced `a b c d` correctly.

TRANSFER ANSWER (verbatim):

```text
.  it would run each character in the string but if we give it a list it would be each entry in the
list
```

EVALUATION:
PASSED. Principle stated to close the gate: the adapter converts Git's text into the representation
the domain needs, ONCE, so no caller has to remember to split it — the duplication argument in a
different form.

WATCH ITEMS:

```text
process_result versus process_result.stdout regressed once after passing; retrieve again later
answering with roles/generalities instead of the exact value on this call recurred again
```

GATE STATUS:
Untracked path-discovery slice CLOSED.

NEXT REQUIRED STEP:
The second untracked patch — one `git diff --no-index -- /dev/null <path>` per discovered path, where
status 0 AND status 1 are BOTH valid. This forces a per-caller accepted-status rule into `_capture`
and is the direct test of the reversal condition in EV-P7-STAGED-DESIGN-292. The empty-untracked-file
edge case approved on 2026-09-02 must be preserved: one changed file, zero added, zero removed.

## EV-P7-SNAPSHOT-COST-300 — learner-initiated architecture and cost reasoning

The learner asked, unprompted, whether untracked paths feed `summarize` the way staged and unstaged
do. Clarified: nothing is wired to `summarize` yet, and paths are an INTERMEDIATE — not diff text —
that the next patch converts into per-file `--no-index` diffs counted as added content in UNSTAGED.

PROCESS COUNT (verbatim, after one narrowing):

```text
3+ n , 23
```

PASSED. Three fixed commands plus one per untracked file; linear growth.

MEASUREMENT taken because the plan requires evidence over adjectives:

```text
20 git child processes : 1187 ms   (~59 ms each)
20 summarize_diff calls:   21 ms   (~1 ms each, 1734-line input)
ratio                  :   58 x
```

JUDGEMENT (verbatim):

```text
i do not think 1.4 seconds for 20 untracked files is worth changing the design now, if it were not
linear work i would say something but most of thetime it will be 3 or 4 files max which is 5 or 6
subprocesses
```

EVALUATION:
STRONGEST ARCHITECTURE JUDGEMENT TO DATE. Measurement, expected workload, growth shape, and a
reversal trigger in one answer. Reversal recorded: revisit if untracked counts routinely reach tens
of files, or if per-call cost stops being flat.

## EV-P7-ENCODING-301 — decoding as part of the data contract

DISCOVERY: a `UnicodeDecodeError` while reading a project file revealed that the adapter's `text=True`
decodes Git output with the LOCALE encoding, which is `cp1252` on this machine.

Evidence gathered:

```text
git bytes  b'caf\xc3\xa9 \xe2\x80\x93 dash'
utf-8   -> 'caf\xe9 \u2013 dash'                correct
cp1252  -> 'caf\xc3\xa9 \xe2\u20ac\u201c dash'  WRONG, silent, no error
b'path\x9dname' + cp1252 -> UnicodeDecodeError
```

Both failure modes were live: sometimes a crash, sometimes silently wrong text that `summarize_diff`
would count.

SCHEDULING DECISION (verbatim):

```text
next patch, this one seems like we could run into it later on and getting on top of it now also will
help later with the live coding past that i do not knwo
```

ENCODING POLICY (verbatim):

```text
option A seems like the besst if we went with option b then we might not get the correct count and
the data becomes untrustworthy
```

PASSED. Strict UTF-8 chosen over `errors="replace"`, because lossy decoding trades a crash for wrong
numbers that nothing flags. The learner explicitly accepted the cost that one latin-1 file makes
every snapshot fail.

EXCEPTION SURFACE: the learner first chose to let `UnicodeDecodeError` reach the caller alongside
`GitCaptureError`. Challenged with the caller's growing `except` clause and the fact that
`UnicodeDecodeError` carries no component label. Revised (verbatim):

```text
then one, if we keep acting on this precident if there are more similar errorrs the except could get
really big
```

PASSED. One normalized exception type; the caller stays decoupled from adapter internals.

## EV-P7-MOCK-LIMIT-302 — FACILITATOR BUG, CAUGHT BY REAL GIT

The first encoding patch used `encoding="utf-8"` with `text=True` and wrapped `subprocess.run` in
`except UnicodeDecodeError`. All eight tests passed. Verification against a REAL repository
containing a latin-1 file proved the patch did not work at all:

```text
returncode : 0
stdout     : None
stderr     : "warning: ...LF will be replaced by CRLF..."
```

`subprocess.run` decodes in a background reader thread. The `UnicodeDecodeError` is raised, printed,
and DISCARDED inside that thread; `run` returns normally with `stdout` as `None` and status 0. The
`except` clause never fired, the status check passed, and the adapter returned `None` as text — the
caller then failed far away with `TypeError: object of type 'NoneType' has no len()`.

The test passed because its stand-in raised an exception that real `subprocess.run` never raises. A
GREEN test asserting fiction.

This is the concrete realization of the limitation the learner articulated at
`EV-P7-PREPATCH-CALL-282`: a controlled test proves call construction and result interpretation, not
operating-system or real-tool behavior.

LEARNER QUESTION (verbatim):

```text
but is None different than an empty repository or no files changed?
```

EVALUATION:
Exactly the distinguishability test the learner established for "no file created" versus "empty file
created". Measured:

```text
clean repo          returncode 0   stdout ''
valid change        returncode 0   stdout <106 chars>
undecodable change  returncode 0   stdout None
```

`None` IS distinguishable, so checking for it was technically viable.

LEARNER PROPOSAL (verbatim):

```text
could we then document in the contract or somewher that if it is a Nonetype then there are a certain
number of possiblities that it could be,
```

EVALUATION:
Good instinct, wrong target. Documenting YOUR OWN contract binds you because you control the code
upholding it; documenting an assumption about someone else's library is a written-down belief that
does not travel with their implementation. Second problem: the possibilities are not enumerable —
one path to `None` was observed, others are unknown.

DECISION (verbatim):

```text
ok so option B seems the best route becasue we then can be sure it is an encoding error
```

PASSED. Capture raw bytes; decode with `.decode("utf-8")` in BuildLens's own code so the failure is
raised by a documented method at a line we wrote.

TEST DISPOSITION (verbatim):

```text
it should be adjusted, the stand in should just have the bytes retunred
```

PASSED. The stand-in now returns a `CompletedProcess` whose `stdout` is invalid UTF-8 BYTES, and the
adapter's own decode raises.

REAL-GIT VERIFICATION after the fix:

```text
clean repo     returned str, length 0
valid utf-8    returned str, length 106
undecodable    GitCaptureError -> UNSTAGED tracked: Git output was not valid UTF-8 text
```

DELIBERATE ASYMMETRY, disclosed to the learner: `stderr` is decoded with `errors="replace"` because
it is only ever a human diagnostic and never counted data. `stdout` remains strict.

STANDING RULE ADOPTED:
Any adapter behavior that depends on how a real external tool or the operating system actually
behaves must be verified against the real tool at least once. Controlled tests alone are not
sufficient evidence for such a claim, and a passing controlled test can encode a false belief.

RECOMMENDATION CARRIED FORWARD:
The plan deferred a real-Git integration test until the capture paths were assembled. Three capture
paths now exist, and this bug is exactly what such a test would have caught. Propose adding one.

NEXT REQUIRED STEP:
The `--no-index` new-file diff patch, where status 0 AND status 1 are both valid, forcing a
per-caller accepted-status rule into `_capture`.

## EV-P7-INTEGRATION-TEST-303 — real-Git test file, and a repository-resolution finding

TEST-SCOPE SORT. The learner sorted five candidate assertions between the controlled and real-Git
files. ANSWER (verbatim):

```text
3, 4, 1
2,5
20
```

EVALUATION:
FOUR OF FIVE at confidence 20 — underconfident, a recurring calibration note. Item 4 (a latin-1 file
in a real working tree) was placed with the controlled tests. Distinguished for the learner:

```text
controlled  prepared BYTES produce a GitCaptureError
item 4      a real latin-1 FILE causes Git to emit those bytes
```

CORRECTED ANSWER (verbatim):

```text
the git test, we need the real latin1 file inside git to actually test thsi
90
```

PASSED. Final division: controlled owns exact call construction and interpretation of prepared
results; real-Git owns whether Git accepts the arguments and what it actually outputs.

### FINDING — repository resolution reaches an unintended ancestor

The `not a repository` integration case FAILED, and investigation showed why: `C:/Users/nicol` is
itself a Git repository, so every temp directory under `AppData/Local/Temp` resolves to it.
`git rev-parse --show-toplevel` from a temp directory returned `C:/Users/nicol`. Running
`git ls-files --others --exclude-standard` there had to be killed after two minutes as it walked the
entire home directory.

Product implication: `buildlens analyze` run anywhere under the home directory would inspect the home
repository. The approved 10-second timeout means it fails rather than printing wrong numbers, but the
user is given no indication which repository was chosen. In a smaller ancestor repository it would
silently produce plausible counts for the wrong project.

DECISIONS (verbatim):

```text
no
yes, i think the repo root should be a directory and it should report it on analyze, if this is a big
bug we need to make sure we are on top of it, this could affect anyone and we would never know
otherwisse, 90
```

The answer combined two options with very different costs, which were separated for the learner:
REPORT the resolved root costs one line of output; REQUIRE the directory to be the root rejects the
normal and legitimate practice of running from a subdirectory.

FINAL DECISION (verbatim):

```text
ok reprot only then and if they do not like the results then they will change where they run analyze
```

PASSED. Visibility over restriction, with control left to the user — consistent with every other
failure decision in this phase.

IMPLEMENTED: `capture_repository_root(repository) -> str` runs `git rev-parse --show-toplevel`
through `_capture` with label `ROOT resolution` and strips the trailing newline. Two controlled tests
and two real-Git tests, including one that deliberately demonstrates upward resolution from a nested
directory.

The learner declined to drop the not-a-repository case. It cannot be constructed anywhere under this
home directory, so it was REPLACED rather than deleted, by a constructible test of the behavior the
learner actually cares about: that a nested directory resolves to an ancestor root that is not itself.

TEST INVENTORY:

```text
test_git_adapter.py              10 controlled tests, bytes stand-ins, no Git required
test_git_adapter_integration.py   8 real-Git tests, throwaway repositories, ~6 s
```

CARRIED FORWARD TO THE CLI SLICE:
`buildlens analyze` must print the resolved repository root before the UNSTAGED and STAGED sections.
The adapter capability exists; the display does not.

WINDOWS DETAIL RECORDED:
Git marks files under `.git/objects` read-only, so `tempfile.TemporaryDirectory` needs
`ignore_cleanup_errors=True` or cleanup fails.

NEXT REQUIRED STEP:
The `--no-index` new-file diff patch, where status 0 AND status 1 are both valid, forcing a
per-caller accepted-status rule into `_capture`.

## EV-P7-NOINDEX-DESIGN-304 — per-caller status rule, the predicted reversal test

This is the pressure the learner predicted at EV-P7-STAGED-DESIGN-292: `--no-index` documents status
1 as "the files differ", a valid result, while every other caller treats 1 as failure.

FIRST ANSWER (verbatim):

```text
it seems like option a makes mroe sense and is less work, if we haveto wire the subprocess inot a
completely different function, my question about option a is that if we have the status for a
paramter does that mean that that is one more paprameter for every function to call?
```

EVALUATION:
Option A chosen. The question is a genuine one and was answered by callback to the learner's own
default-parameter work in EV-P7-DEFAULT-PARAMETERS-283 rather than by assertion.

ANSWER (verbatim):

```text
. no, we can set it as a default and then if it is needed then we can change it to {0,1} ok that
seems pretty handy, it holds {0}, that seems like less work than creating and wiring and testing an
entierly new function
```

PASSED. Existing callers unchanged; the default supplies the value.

PARAMETER COUNT: first given as 5, corrected unprompted to `its 4 and the fourth is optional`.

COHERENCE JUDGEMENT (verbatim):

```text
. no it does not change what _capture does, only how it judges one run, it would make the input be
sometimes a string and sometimes a list whic his changing the output, yes
90
```

PASSED at confidence 90, and this is the strongest cohesion reasoning recorded. Given a contrast
between `accepted_statuses` and a hypothetical `split_lines`, the learner produced the criterion
themselves: a parameter that varies HOW ONE RUN IS JUDGED keeps the job single, while one that varies
WHAT COMES BACK would split it. `_capture` remains one coherent job by that test.

DECISION: Option A. `accepted_statuses: tuple[int, ...] = (0,)`. A tuple rather than a set, because a
default is evaluated once at definition time and an immutable default closes the mutable-default trap
by construction rather than by discipline.

## EV-P7-NOINDEX-REAL-GIT-305 — real-Git probe BEFORE writing the test

Per the standing rule adopted at EV-P7-MOCK-LIMIT-302, real Git was probed before any test was
written, so the test could not encode a false belief. Git 2.55.0.windows.3:

```text
helper.py (nonempty)  status 1  new file mode, --- /dev/null, @@ -0,0 +1 @@, +print("ready")
empty.py              status 1  diff --git, new file mode, index 0000000..e69de29, NO hunk
```

`/dev/null` works on Windows Git. Both cases return status 1.

The requirement the learner defended on 2026-09-02 was then verified end to end against the real
summarizer:

```text
helper.py   DiffSummary(files_changed=1, lines_added=1, lines_removed=0)
empty.py    DiffSummary(files_changed=1, lines_added=0, lines_removed=0)
```

The empty untracked file reports as one changed file with zero lines, because the file header exists
and no hunk does — exactly the completeness argument the learner made.

RED: `ImportError: cannot import name 'capture_new_file_diff'`.
GREEN: 14 controlled tests and 10 real-Git tests pass; all six suites pass.

A guard test was added in the same patch: `test_status_1_still_fails_for_the_tracked_diff_captures`
asserts the default was not widened for everyone.

### EV-P7-NOINDEX-TRACE-306 — same status, two verdicts

ANSWER (verbatim):

```text
.  call a will return status 1 for scuess
call b will also be a sucess the status 1
the if branch will be called
the if branch will be not  called
since accepted status is = to (0,1) b will not call the if
b will return the untracked path
the call a did not specify the accepted statueses but call b did
90
```

EVALUATION:
STRONG PARTIAL at confidence 90. Both branch verdicts correct, and the mechanism stated exactly: A
never specified `accepted_statuses`, B did. Two errors: A's value was not given, and call B was said
to return the untracked PATH rather than the diff TEXT — a recurrence of the returned-representation
confusion, with the path being the argument going IN.

NARROWED ANSWER (verbatim):

```text
. 0
1 and a diff text for brand_new.py
90
```

PASSED. Precision added: the value is the tuple `(0,)`, not the integer `0`, because
`returncode not in 0` would raise `TypeError`.

GATE STATUS:
`--no-index` slice CLOSED. All four capture paths now exist.

NEXT REQUIRED STEP:
Composition — assemble UNSTAGED (tracked plus untracked new-file diffs) and STAGED into one snapshot,
with whole-snapshot rejection on any component failure. Then CLI integration, which must also print
the resolved repository root. Launch failure and timeout normalization remain a separate later slice.

## EV-P7-COMPOSITION-DESIGN-307 — where orchestration lives

PLACEMENT. Three options offered: composition inside `git_adapter` (A), a new `snapshot.py` (B), or
inside `cli.py` (C). The distinction put at the centre was the learner's own decision history:

```text
POLICY     untracked content belongs inside the UNSTAGED view
           the two views are never summed
           any component failing rejects the whole snapshot

MECHANISM  /dev/null comparison, --no-index, ls-files, status rules
```

FIRST ANSWER (verbatim):

```text
i am leaning towards git_adatpor but want tot alk further
```

Then (verbatim):

```text
c would have to make you re-implemnt the policy, i was thinking option A becasue the git adapter i
was giving it the git boundary responsilbity and all of the captures are already in there so we
would not need to import anything to call the snapshot function,
```

EVALUATION:
C correctly rejected for forcing every future front end to re-implement policy. The stated reason for
A was CHALLENGED: B also avoids duplication, and "no import needed" is nearly free — `summarize.py`
already imports `classify`, a dependency the learner previously called healthy.

COHESION TEST APPLIED: `git_adapter`'s one-sentence job today covers all five functions exactly.
Adding `capture_snapshot` forces an "and also" into that sentence — the same signal the learner used
to reject a hypothetical `split_lines`.

DECISION (verbatim):

```text
B, it seems like we would be adding too much to the responsilbity of git adapter, 90
```

PASSED at confidence 90. Noted as CONSISTENT with the Phase 4 refusal to split without evidence:
there was no observed problem then; here there are two — the "and also" in the sentence, and the
testing cost of mocking four Git commands to test one policy rule.

RETURN REPRESENTATION. Two options: a Snapshot carrying diff TEXT (front ends summarize), or a
Snapshot carrying SUMMARIES (front ends only present).

FIRST ANSWER (verbatim):

```text
for option 1 it seems like more compute but for option 2 it seems like more could go wrong
```

EVALUATION:
BOTH PREMISES CORRECTED. Compute is identical — both call `summarize_diff` exactly twice on the same
two strings; only the call site differs, and the learner's own measurement puts `summarize_diff` at
about 1 ms against 59 ms per Git process. "More could go wrong" was not made concrete.

Then (verbatim):

```text
i cant see any reason one way or the other
```

ADAPTATION:
Made concrete with the Phase 12 API scenario, transferring the learner's own successful rejection of
Option C: under Option 1 a second front end re-implements both the summarizing and the never-sum rule.

DECISION (verbatim):

```text
ok lets go with option 2
```

REASON, on request (verbatim):

```text
there are less hoops for the data to jump through, the serializing at the end and the must know not
to sum them seems like another test we would need to run
```

PASSED on the second clause, which is the load-bearing one: the never-sum rule is stated and tested
ONCE, in `snapshot.py`, rather than once per front end.

## EV-P7-COMPOSITION-RED-GREEN-308 — snapshot.py

RED (verbatim):

```text
ModuleNotFoundError: No module named 'snapshot'
```

GREEN: six snapshot tests pass; all seven suites pass. `snapshot.py` runs no Git command, so its
tests patch the five capture functions rather than subprocess — mechanism is tested in
`test_git_adapter*`, policy here.

Verified against a real repository as well as the patched tests.

FACILITATOR ERROR RECORDED:
The real-repository result was PRINTED BEFORE the learner was asked to predict it, violating the rule
that the answer is never revealed before the learner commits. That scenario is spent. A fresh
scenario was substituted.

### EV-P7-SNAPSHOT-TRACE-309 — PRESENTED, NOT ANSWERED

SESSION PAUSE: the learner stopped for the night before answering. UNATTEMPTED — must not be graded,
and its answer must not be revealed on resumption.

EXACT PROMPT. Repository built from a base commit containing `a.txt` with three lines `1`, `2`, `3`:

```text
a.txt      tracked, edited in the working tree, now reads  1 / x / 3
b.txt      brand new, added to the index with  git add,  contains  p / q
c.py       created, never added, contains three lines
d.py       created, never added, completely empty
```

```text
Number of Git child processes this snapshot launches =
UNSTAGED  files_changed, lines_added, lines_removed =
STAGED    files_changed, lines_added, lines_removed =
Which of the four files contribute to UNSTAGED =
Confidence =
```

The learner asked to see `capture_snapshot` before answering, which was granted — this is a trace,
not a memory test.

NEXT REQUIRED STEP:
Re-present the prompt above verbatim, then build the real repository and compare. After it passes,
the CLI slice: wire `capture_snapshot` into `main`, print the resolved repository root followed by
separately labelled UNSTAGED and STAGED sections, status 0 on success, and on any GitCaptureError
write the message to stderr with a rerun instruction and return 1.

## EV-P7-SNAPSHOT-TRACE-309 — RESUMED AND CLOSED

The trace required a long detour through Git vocabulary before the counting could begin.

GIT MODEL PREREQUISITE. The learner asked (verbatim):

```text
the wording is throwing me off, tracked is unstaged but in the worktree and added is staged but not
committed and then never added means unstaged?
```

Two independent axes were supplied: tracked-versus-untracked (does Git know the file at all) and
staged-versus-unstaged (for tracked files, is the change in the index or only the working tree). The
trap named: `git add` on a brand-new file makes it TRACKED.

Further vocabulary questions, all answered and all legitimate:

```text
recorded in the index means you git added it or is it you git committed it?
```

Answered with the three-place model: working tree -> git add -> index -> git commit -> history.

The learner then generalized correctly and unprompted (verbatim):

```text
so i need to be careful about where the most recent verson of the file is becasue there could be a
staged verson but you could make a small change to that and now you have an unstaged verson of a file
that one verson ago is currently staged
```

PASSED — three versions coexist (HEAD, index, working tree) and the two diffs compare adjacent pairs.
This is also the concrete reason the two views cannot be summed: they measure different gaps.

VIEW MEMBERSHIP (verbatim):

```text
unstaged
staged
unstaged
unstaged
90
```

PASSED. a.txt, c.py, d.py to UNSTAGED; b.txt to STAGED.

PROCESS COUNT required several narrowings. The learner correctly recalled the earlier `3 + n` formula
and was told it predated `capture_repository_root`. They first counted 5 call SITES, then correctly
separated sites from executions (their own lesson from the staged slice), then identified 4 fixed
calls. They initially listed a.txt among the untracked files; corrected by showing the three real Git
commands and their actual output, which is what finally resolved it.

FINAL ANSWER (verbatim):

```text
6
3
4
1
100
```

VERIFIED against a real repository built to the exact scenario. Every field matched, including the
six child processes in issue order.

## EV-P7-NAMING-DETOUR-310 — FACILITATOR ERROR, learner-corrected

The learner objected (verbatim):

```text
but the label is still unstaged_parts that is what is throwing me off
```

This was treated as a naming DEFECT and escalated into a rename: `unstaged_parts` ->
`unstaged_view_parts` -> a full rename of the view to WORKING, agreed with the learner, applied, and
all suites re-run green.

The learner then reverted the decision (verbatim):

```text
ok so go back and undo all the renaming changes, i think the better expliation wouqld have been to
tell me to look at the function that git adater was running to catagorize whAT IS WHERE
```

UPHELD. The question was comprehension — which command emits which file — and it was in fact resolved
by showing the three commands' real output, not by renaming anything. All rename changes were
reverted; the worktree returned to ab2206d with all seven suites passing.

SECOND FACILITATOR ERROR, also learner-corrected (verbatim):

```text
so then working and unstaged would be the same thin in buildlens please be more specific next time
instead of a blanekt statment especially when this affects so much
```

UPHELD. The statement "working and unstaged are not synonyms" was made without saying WHOSE
vocabulary was meant. Inside BuildLens they name the same view; the real contrast is against GIT's
term:

```text
GIT unstaged          a.txt              tracked, changed in working tree, not in index
BUILDLENS UNSTAGED    a.txt, c.py, d.py  Git's unstaged plus untracked files
BUILDLENS WORKING     a.txt, c.py, d.py  rejected alternative name for the same view
```

STANDING INSTRUCTIONS ADOPTED:

```text
qualify every ambiguous term with whose vocabulary it belongs to — Git's or BuildLens's
answer a comprehension question by showing what the code or command actually produces,
    before considering whether a name should change
do not escalate a learner's confusion into a design change without first checking that
    the confusion is not simply unanswered
```

NEXT REQUIRED STEP:
The CLI slice — wire `capture_snapshot` into `main`, print the resolved repository root followed by
separately labelled UNSTAGED and STAGED sections, status 0 on success, and on any GitCaptureError
write the message to stderr with a rerun instruction and return 1.

## EV-P7-CLI-DESIGN-311 — replacing the CLI contract

DECISION 1 — the orphaned `read_diff`. Verified unused first: its only caller was the line being
removed, plus one test existing solely to cover it.

ANSWER (verbatim):

```text
for d1 i am leaning towards a if it is truely unsued and we could think about restating it later that
seems like the best move because keeping dead code might confuse soeone later who is reading this back
```

PASSED. Deleted. The learner's condition — "if it is truly unused" — was checked rather than assumed.

DECISION 2 — output format. The learner approved the proposal and then asked for one reasonable
objection to consider. Supplied: the `Repository:` line existed to expose the wrong-repository hazard,
but appeared only on success, while the hazard bites hardest on failure (the home-directory case ends
in a timeout).

ANSWER (verbatim):

```text
i think it si a good idea to add it to the failure output as well , when the root resolution is the
failure itself it makes sense to have the error message reflect that and then the user can go back
and check to see if the bug is happeneing, i do not think this is a huge issue
```

PASSED and ADOPTED into the contract. The plumbing choice followed: `GitCaptureError` carries the
resolved root, rather than the CLI resolving it separately.

ANSWER (verbatim):

```text
option b is the one i was thinking of before you even wrote it
```

and, on the reasoning:

```text
no extra git call and the optional None is the tell for the user that something went wrong as well as
the raise and the error message
```

PASSED on the mechanism. Precision supplied: `None` is not a signal to the USER, who never sees it;
it is how `cli.py` knows there is no repository line to print.

## EV-P7-CLI-RED-GREEN-312 — first complete vertical slice with real Git

RED (verbatim):

```text
cli.py: error: the following arguments are required: path
SystemExit code: 2
```

GREEN: all seven suites pass. Verified END TO END against real repositories, both paths:

```text
SUCCESS   Repository: <root>
          UNSTAGED 3/4/1, STAGED 1/2/0, exit 0
          matching the learner's own prediction in EV-P7-SNAPSHOT-TRACE-309

FAILURE   Repository: <root>
          UNSTAGED tracked: Git output was not valid UTF-8 text
          Run buildlens analyze again.
          exit 1, stdout empty
```

Every clause of the contract the learner specified across prior sessions is now demonstrated in
running code: whole-snapshot rejection, the component named, the rerun instruction, status 1, no
partial output, and the repository line present in both outcomes.

### EV-P7-CLI-BOUNDARY-313 — end-to-end responsibility trace

ANSWER (verbatim):

```text
the repository
git adapter
git adapter
summarize
how we ingest the diff string if the other verson control tool was giving strings a different way or
as a list
90
```

EVALUATION:
PARTIAL. The `--no-index` status rule was correctly placed in `git_adapter`. Two fields misplaced a
decision: the untracked-goes-in-UNSTAGED policy belongs to `snapshot`, and the "Files changed: 3"
formatting belongs to `cli`.

ADAPTATION:
Rather than explaining, the learner was asked which FILE contains two specific lines. Both answered
correctly (`snapshot`, `cli`), which settled the boundary without a lecture — applying the standing
instruction adopted earlier this session.

FACILITATOR CLAIM WITHDRAWN:
The two misplacements were described as a pattern of "moving a decision toward the data producer".
The learner asked for the reasoning. On inspection, two instances is thin evidence, and the simpler
explanation is that the learner had not read `snapshot.py` or the new `cli.py`, both written minutes
earlier by Claude. The claim was withdrawn rather than recorded as a finding about the learner.

FINAL FIELD — what changes in `cli.py` if Git were replaced (verbatim):

```text
you would also need to change the imports becasue we would need to write another adapter so we would
neeed to have a function that accoiunts for git and the other verson control tool
```

PASSED on the import, which is the exact answer: `from git_adapter import GitCaptureError` names Git
in the boundary module, while `import snapshot` would not change. The dispatcher idea was flagged as
speculative generality, the same thing the learner correctly refused in Phase 4.

## EV-P7-GIT-IS-A-REQUIREMENT-314 — learner overturns a facilitator premise

The Git-named exception in `cli.py` was offered as a leak, with three options including a rename.

ANSWER (verbatim):

```text
ther will never be another tool so why rename for no reason
```

UPHELD, and the reasoning is stronger than the question. Phase 13 depends on Git worktrees, and
Claude Code itself uses them. Git is an architectural REQUIREMENT of BuildLens, not a swappable
implementation choice, so naming it at the boundary is accurate rather than leaky.

FACILITATOR ERROR: a generic principle — boundaries should not name the outside tool — was applied
without checking whether it held for this system.

ARCHITECTURAL ASSUMPTION NOW STATED EXPLICITLY:

```text
Git is a requirement of BuildLens, not a choice.
Naming Git in module and type names is therefore accurate, not a boundary leak.
```

NEXT REQUIRED STEP:
Phase 7 milestone transfer variant on a different surface, then the phase-close review. The delayed
argparse parser-versus-Namespace retrieval is also still owed.

## EV-P7-MILESTONE-TRANSFER-315 — Phase 7 milestone transfer, PASSED

FACILITATOR ERROR 1: the transfer was first set in a lab-assay domain. The learner objected
(verbatim):

```text
but assay spectra in geneeral?
```

UPHELD. A transfer changes surface features; it must not add domain vocabulary the learner has to
decode first, which would hide the concept being tested. Re-set in a linter domain the learner works
in daily. RULE ADOPTED: choose transfer surfaces from domains the learner already knows.

The learner also asked why the transfer was needed. Answered concretely rather than by citing the
contract: several correct answers this session arrived with code on screen, after narrowing, or by
looking up which file a line lived in, and Phase 8 adds a second external system that asks the same
layering question immediately.

SURFACE: a Lint Report tool shelling out to pylint, which really does exit 1 when it finds problems.
Required report has TRACKED and NEW sections, counted separately, never combined, whole-report
rejection on any component failure. No code written; design and reasoning only.

MODULE PLACEMENT (verbatim):

```text
lint_adater.py
filter.py
```

PASSED. The process owner was separated from the module deciding which section a file lands in — the
git_adapter/snapshot split, transferred. Note offered without drilling: `filter` implies removal,
while that module composes sections and enforces all-or-nothing.

STATUS RULE (verbatim):

```text
it would be in lint adapter
```

then, on the mechanism:

```text
could you write in the accepted statuses tuple so that is normally stored as (0,) and when it is a
new file scan you have to input (0, 1, ) 90
```

PASSED UNAIDED at confidence 90. The exact mechanism from EV-P7-NOINDEX-DESIGN-304, reproduced on a
new surface: a default that keeps strict callers strict, overridden only by the caller that needs it.

PROCESS COUNT (verbatim):

```text
n + 2 with n = 4 so it would be 6
30
```

FACILITATOR ERROR 2: the prompt never specified how the TRACKED section was produced, leaving the
count genuinely underdetermined. The learner inferred one tracked-report command plus
`--list-unchecked` plus one scan per new file, which is the sensible reading, and their confidence of
30 was well calibrated to the ambiguity. Graded as CORRECT under that reading; the ambiguity was
mine.

REPRESENTATION (verbatim):

```text
it would not need it becasue the probelsm are printed to stdout , 90
```

PASSED. The surface was deliberately chosen so the exit code LOOKED meaningful (0 clean, 1 problems).
The learner correctly reasoned that empty stdout already distinguishes those cases, so the return
code is redundant for this consumer — the same conclusion they reached for BuildLens, on a surface
built to tempt the opposite answer.

REVERSAL CONDITION (verbatim):

```text
if the probelsm were not printed out to stdout
90
```

PASSED, and SHARPER than the BuildLens version. Theirs is falsifiable by observing the tool: if the
evidence source disappears from stdout, the exit code becomes the only signal.

TEST LIMITS (verbatim):

```text
it rpoves the subprocess will be called it does not prove that pylint will work yet
90
```

PASSED. Precision supplied: a stand-in proves the code ATTEMPTED the expected call and interpreted a
prepared result; nothing is launched at all.

OVERALL: PASSED with fading assistance — no code on screen, no file lookups, no scaffolding beyond
restating fields. This is the strongest independent performance recorded in the project.

PHASE 7 MILESTONE STATUS:

```text
implementation       complete — git_adapter, snapshot, cli vertical slice
automated tests      complete — seven suites, controlled and real-Git
learner trace        complete — EV-P7-SNAPSHOT-TRACE-309, EV-P7-CLI-BOUNDARY-313
learner explanation  complete — EV-P7-CLI-BOUNDARY-313, EV-P7-GIT-IS-A-REQUIREMENT-314
transfer variant     complete — EV-P7-MILESTONE-TRANSFER-315
```

STILL OWED BEFORE PHASE 7 CLOSES:

```text
delayed argparse parser-versus-Namespace retrieval on a fresh surface
```

The Git model taught this session (tracked vs untracked, the index as a third place, which diff
compares which pair) was SUPPLIED, not retrieved, and needs one delayed retrieval before it can be
called held.

NEXT REQUIRED STEP:
The owed argparse retrieval, then Phase 7 close. The major/deep Phase 7-15 counter starts at 1/2 once
Phase 7 closes.

## EV-P7-ARGPARSE-DELAYED-316 — owed delayed retrieval, parser versus Namespace

Fresh surface, no scaffolding: an archive tool with `mode` and `target` positionals.

ANSWER (verbatim):

```text
. parser
args
target
args = Namespaec(mode = retore , target = vault.tar)
it prints usage and error text
90
```

EVALUATION:
FOUR OF FIVE. Parser-versus-Namespace — the item actually owed since Phase 6 — PASSED cleanly:
`parser` holds the rules, `args` holds the parsed values, and the representation included the
`Namespace(...)` wrapper with both fields. Spelling and quotes treated as typing noise per the
learner's standing request.

Field 3 gave the field NAME rather than the retrieval expression; narrowed once, answered
`args.target` correctly.

Field 5 described what the user sees but not the effect on the running program.

DELAYED RETRIEVAL OF SystemExit(2): FAILED (verbatim `not sure`), then recovered by reading the
learner's own `expect_system_exit_2` helper in `test_cli.py`. Recovery by lookup, not retrieval.

This fact has now needed support three times: EV-P6-ARGPARSE-SYNTAX-278 (taught),
EV-P6-ARGPARSE-REVIEW-279 (recalled as "returns 1", corrected), and here.

IMPORTANT DISTINCTION, recorded so the record stays accurate:

```text
HELD      the concept — malformed syntax should carry a status distinct from other
          user errors. The learner chose this policy themselves in
          EV-P6-ARGPARSE-POLICY-280 and defended it against returning 1.

NOT HELD  the specific values SystemExit and 2, as a recalled fact.
```

The concept is the load-bearing part; the values are looked up in one line of their own test suite.
Treat this as a lookup-able fact, not a mental model gap, and do not re-teach the policy.

CARRIED FORWARD: one more delayed retrieval of SystemExit(2) on a fresh surface, unprompted. If it
lapses again, stop re-testing it — the fact is documented in `cli.py` and `test_cli.py`, and the
concept it serves is held.

## PHASE 7 CLOSED

```text
implementation       complete — git_adapter, snapshot, cli vertical slice
automated tests      complete — seven suites, controlled and real-Git
learner trace        complete — EV-P7-SNAPSHOT-TRACE-309, EV-P7-CLI-BOUNDARY-313
learner explanation  complete — EV-P7-CLI-BOUNDARY-313, EV-P7-GIT-IS-A-REQUIREMENT-314
transfer variant     complete — EV-P7-MILESTONE-TRANSFER-315
owed retrieval       complete — EV-P7-ARGPARSE-DELAYED-316
```

The major/deep Phase 7-15 counter now stands at 1/2. A cumulative review is due after the second
completed major phase, so it is NOT due before Phase 8.

STILL OPEN, carried into Phase 8:

```text
SystemExit(2) delayed retrieval, one more attempt on a fresh surface
the Git model taught 2026-09-04 was SUPPLIED, not retrieved; needs one delayed retrieval
launch failure (FileNotFoundError) and timeout (TimeoutExpired) normalization, a deferred slice
session.py is not wired to the snapshot path and holds no snapshot state
```

NEXT REQUIRED STEP:
Phase 8 — the Claude Code adapter. A second external system entering through the same layering the
learner just defended, with hook payloads introducing JSON and the trust boundary
`MODEL OUTPUT != AUTHORITATIVE APPLICATION STATE`.

