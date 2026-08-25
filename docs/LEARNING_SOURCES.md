# BuildLens — Learning and Engineering Sources

This document keeps source material separate from the implementation plan.

BuildLens should reference source IDs in implementation/learning files. Do not reproduce university exercises verbatim. Extract the deep skill and generate related but substantially different variants.

## CMU Programming

### CMU-112
**Carnegie Mellon University — 15-112 Fundamentals of Programming and Computer Science**

https://www.cs.cmu.edu/~112/

Key BuildLens ideas:
- sequential/conditional/loop execution
- code tracing
- top-down design
- debugging
- substantial-program development with increasingly less guidance

Current/future course pages preserve the same core learning objectives.

### CMU-112-ALGO
**CMU 15-112 — Algorithmic Thinking**

https://www.cs.cmu.edu/~112-n22/notes/notes-algorithmic-thinking.html

Key BuildLens ideas:
- define the problem precisely
- generate tests before implementation
- restate the problem in your own words
- use "human computer" reasoning
- compare alternative algorithms
- top-down decomposition
- translate manual steps into code
- review/test after implementation

### CMU-112-Q
**CMU 15-112Q syllabus / learning outcomes**

https://www.cs.cmu.edu/~15112q-f25/syllabus/index.html

Key BuildLens ideas:
- read, write, design, and debug Python
- modular top-down design
- proactively create test cases
- analyze algorithm efficiency
- culminate in a substantial project

---

## CMU Eberly Center — Learning Design

### CMU-EBERLY-RETRIEVAL
**Retrieval Practice for Improved Learning**

https://www.cmu.edu/teaching/resources/instructionalstrategies/activelearningstrategies/retrievalpractice/index.html

Key BuildLens ideas:
- recall from memory instead of passive rereading
- frequent low-stakes practice
- short answer > simple recognition for many learning goals
- peer teaching
- concept maps
- early and repeated retrieval
- feedback after committing to an answer
- transfer to novel contexts

### CMU-EBERLY-CONCEPT-MAPS
**Using Concept Maps**

https://www.cmu.edu/teaching/assessment/assesslearning/conceptmaps.html

Key BuildLens ideas:
- visual representation reveals knowledge organization
- repeatedly recreate maps as understanding develops
- use relationships/links, not merely isolated boxes
- revise maps over time

### CMU-EBERLY-LOW-STAKES
**Concrete Strategies for Frequent, Low-Stakes Practice**

https://www.cmu.edu/teaching/online/designteach/strategies/lowstakespractice.html

Key BuildLens ideas:
- milestone/component tasks before a final deliverable
- repeated-attempt mastery assessments
- scenario-based tests that require synthesis
- weekly/recurring key-skill checks

### CMU-EBERLY-ASSESSMENTS
**Assessments / Inclusive Excellence**

https://www.cmu.edu/teaching/designteach/inclusiveexcellence/assessments/index.html

Key BuildLens ideas:
- divide large deliverables into milestones
- cumulative problem sets combine old and new skills
- provide feedback early
- space low-stakes work to avoid overload

### CMU-EBERLY-SCAFFOLD
**Labs / Studios — apprenticeship and fading**

https://www.cmu.edu/teaching/designteach/teach/instructionalstrategies/labsstudios.html

Key BuildLens ideas:
- expert models first
- coach the learner during practice
- gradually fade assistance
- progress toward independent expert-like performance

### CMU-EBERLY-DEEP-FEATURES
**Students often focus on superficial features instead of underlying principles**

https://www.cmu.edu/teaching/solveproblem/strat-cantapply/cantapply-02.html

Key BuildLens ideas:
- vary surface features while preserving deep structure
- teach recognition of underlying principles
- present multiple superficially different examples
- identify misconceptions
- sometimes test only selection of the correct approach

### CMU-EBERLY-ACTIVE
**Active Learning Strategies**

https://www.cmu.edu/teaching/resources/instructionalstrategies/activelearningstrategies/index.html

Key BuildLens ideas:
- short concept maps
- predict-observe-explain
- brief pauses for consolidation rather than long uninterrupted delivery

---

## UC Berkeley

### UCB-DS200
**UC Berkeley School of Information — Data Science 200: Introduction to Data Science Programming**

https://www.ischool.berkeley.edu/courses/datasci/200

Key BuildLens ideas:
- frequent Python practice
- progression from Python objects/control structures to OOP
- module, class, and function development
- coding hygiene
- major project showing how a larger piece of software is built
- full-cycle development project

### UCB-CS169
**UC Berkeley CS169 — Software Engineering project/design-review material**

https://people.eecs.berkeley.edu/~brewer/cs169/lecture01.pdf

Key BuildLens ideas:
- design, code, and test as distinct activities
- explicit design review before/through iterative implementation
- software engineering learned through project experience
- repeated project presentations/explanations

---

## CMU Software Engineering Institute — Architecture

### CMU-SEI-ATAM
**Architecture Tradeoff Analysis Method collection**

https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/

Key BuildLens ideas:
- business/quality drivers influence architecture
- architecture should be explained in terms of decisions
- scenarios expose risks
- identify sensitivity points and tradeoff points
- architecture documentation should record the basis for decisions

### CMU-SEI-ATAM-2026
**Architecture Tradeoff Analysis Method information sheet (2026)**

https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-atam/

Key BuildLens idea:
Use architecture evaluation as an end-stage reasoning/defense exercise after the concrete implementation is understood.

### CMU-SEI-QAW-ATAM
**SEI Architecture Analysis Techniques and When to Use Them**

https://sei.cmu.edu/library/sei-architecture-analysis-techniques-and-when-to-use-them/

Key BuildLens ideas:
- quality scenarios can be useful even before architecture is fully developed
- later evaluate the developed architecture against quality requirements, risks, sensitivities, and tradeoffs

---

## Claude Code

### CLAUDE-HOOKS
**Claude Code Hooks Reference**

https://code.claude.com/docs/en/hooks

Key BuildLens engineering facts:
- lifecycle events include SessionStart/End, UserPromptSubmit, PreToolUse, PostToolUse, PostToolBatch, Stop/StopFailure, Subagent events, ConfigChange, FileChanged, and others
- PostToolUse contains tool input and response
- hooks may be commands, HTTP endpoints, MCP tools, prompts, or agents depending on event
- FileChanged uses literal filenames for configured watch lists
- project hook configuration can live in `.claude/settings.json`

### CLAUDE-HOOKS-GUIDE
**Automate workflows with hooks**

https://code.claude.com/docs/en/hooks-guide

Key BuildLens engineering facts:
- `PostToolUse` can target `Edit|Write`
- Claude can also change files via Bash
- for broader change coverage, the guide recommends accounting for Bash or scanning the Git working tree at `Stop`
- this supports BuildLens's eventual capture + reconciliation architecture

---

## Source-use rule

For every future BuildLens learning archetype:

```text
source ID
→ exact learning idea
→ deep skill
→ allowed difficulty range
→ required variation dimensions
→ BuildLens lifecycle phase
```

A source is useful only when it changes the curriculum, exercise design, architecture, or implementation decision.

Do not add references simply to increase the number of sources.


---

## Reference Project Sources — Verified Code Snapshots

These are not academic authorities. They are **practice domains** whose real code gives Claude realistic source material for transfer exercises.

Claude should use them only after mapping the exercise back to an academic learning objective above.

### REPO-ARGOS
**Argos Control Tower**

Repository: `peyton150-startup/Argos_Control_Tower`

Last verified default-branch commit during this plan refinement:
`65b560b0fad3a434520ba431ccb04bbcd1feba06`

Primary files:
- `backend/app/projection.py`
- `backend/app/domain.py`
- related projection tests

Why it belongs:
- deterministic event replay
- ordered state transitions
- accumulators
- aggregation
- missing/invalid values
- derived read models
- source-event evidence

Use mainly after basic loops/functions and before advanced concurrency.

### REPO-DATUM
**Datum**

Repository: `peyton150-startup/Datum-Project`

Last verified default-branch commit during this plan refinement:
`3d1d73736bbe149c22b3e88f6a8e3315db1d71e3`

Primary files:
- `datum/reconcile/diff.py`
- `datum/reconcile/matcher.py`
- `datum/reconcile/domain.py`
- `datum/intent/`
- `docs/adr/`

Why it belongs:
- separate representations of declared/discovered truth
- deterministic reconciliation
- set/union reasoning
- natural keys
- explicit domain models
- validation/trust boundaries
- architecture decisions and reversal costs

Use after the learner understands data structures, modules, and contracts.

### REPO-TRELLIS
**Trellis AI Chatbot Task Manager**

Repository: `peyton150-startup/Trellis_AI_Chatbot_Task_Manager`

Last verified default-branch commit during this plan refinement:
`11cf50bc5882b71062b65e83f436b2e9317354b1`

Primary files:
- `backend/app/idempotency.py`
- `backend/app/domain.py`
- `backend/app/agent.py`
- `backend/app/main.py`
- related policy/approval/idempotency tests

Why it belongs:
- probabilistic agent inside deterministic application boundaries
- server-owned authority
- typed tool contracts
- authorization
- human approval
- retry/idempotency state
- transaction boundaries
- auditability
- failure/concurrency reasoning

Use late. Do not simplify advanced concurrency into a misleading early exercise.

---

## Reference Project Use Rule

The reference repository provides a **realistic shape**; the academic source defines the **learning objective**.

Every derived gate should record both:

```text
academic_source: CMU-112-CT
reference_project: REPO-ARGOS
deep_skill: trace accumulator state across a loop
```

or:

```text
academic_source: CMU-EBERLY-DEEP-FEATURES
reference_project: REPO-TRELLIS
deep_skill: recognize idempotency despite a different application domain
```

If Claude cannot name the academic objective and explain why the selected repository example fits the learner's current phase, it should not generate the exercise.


---

## Collaborative Editing / Lost-Update Prevention

### CLAUDE-DESKTOP-WORKTREES
**Claude Code Desktop — session isolation**

https://code.claude.com/docs/en/desktop

BuildLens use:
- Git-backed Desktop sessions use isolated worktrees;
- this is the primary physical-isolation primitive for Claude vs learner edits.

### CLAUDE-HOOKS-EDIT-CONTROL
**Claude Code Hooks — PreToolUse / PostToolUse / Stop / FileChanged**

https://code.claude.com/docs/en/hooks

BuildLens use:
- `PreToolUse` can block a tool call;
- `Edit`/`Write` hook input provides an absolute file path;
- `PostToolUse` observes successful file-tool edits;
- `FileChanged` observes but has no decision control;
- `Stop` provides a turn boundary for actual working-tree reconciliation.

### GIT-WORKTREE
**Git — git-worktree**

https://git-scm.com/docs/git-worktree.html

BuildLens use:
- multiple linked working trees attached to one repository;
- physically isolate human and Claude change streams.

### GIT-THREE-WAY
**Git — git-merge-file / git-merge**

https://git-scm.com/docs/git-merge-file
https://git-scm.com/docs/git-merge

BuildLens use:
- common-base three-way merge;
- overlapping changes surface as explicit conflicts instead of arbitrary overwrite.

### PY-HASHLIB
**Python — hashlib**

https://docs.python.org/3/library/hashlib.html

BuildLens use:
- SHA-256 content fingerprints as optimistic version tokens;
- `file_digest()` is available for file-like objects.

### PY-TEMPFILE
**Python — tempfile**

https://docs.python.org/3/library/tempfile.html

BuildLens use:
- safely create temporary files for complete manual-save output before replacement.

### PY-OS-REPLACE
**Python — os.replace**

https://docs.python.org/3/library/os.html#os.replace

BuildLens use:
- same-filesystem replacement is atomic on POSIX when successful;
- protects against exposing a partially written destination file.

### PY-PATHLIB-REPLACE
**Python — pathlib.Path.replace**

https://docs.python.org/3/library/pathlib.html#pathlib.Path.replace

BuildLens use:
- path-oriented replacement API for the same final promotion step.

### Important distinction

These mechanisms solve different problems:

```text
worktree
→ writer isolation

hash/version token
→ stale-write detection

three-way merge
→ logical reconciliation

atomic replacement
→ complete destination-file publication

hooks
→ observability + additional blocking
```

Do not collapse them into one generic "locking" concept.


### CLAUDE-DESKTOP-EDITOR
**Claude Code Desktop — diff and file editor behavior**

https://code.claude.com/docs/en/desktop

BuildLens use:
- Desktop exposes a file-by-file diff viewer with added/removed line counts;
- Desktop's local/SSH file pane allows manual editing;
- if a file changed on disk after opening, Desktop warns before save.

BuildLens intentionally strengthens the stale-file behavior: a stale buffer enters reload/reconciliation rather than using blind override as the normal path.

### GIT-MERGE-BASE
**Git — git-merge-base**

https://git-scm.com/docs/git-merge-base

BuildLens use:
- recompute the current best common ancestor of human/Claude tips at reconciliation time;
- avoid assuming the original session-start commit remains the correct merge base after either side advances.


---

## Additional Depth Sources

### CMU-213-SYSTEMS
**CMU 15-213 — Introduction to Computer Systems**

https://csd.cs.cmu.edu/15213-introduction-to-computer-systems

BuildLens use:
- add a programmer's systems-level model after basic application reasoning;
- connect Python/framework behavior to machine execution, memory, performance, networking, and concurrent computation;
- ask "what happens underneath this abstraction?" without turning BuildLens into a C course.

### UCB-CS61B-2026
**UC Berkeley CS 61B Spring 2026 — Data Structures**

https://sp26.datastructur.es/

BuildLens use:
- data structures and representation choices;
- testing/debugging as part of larger projects;
- Git as routine development infrastructure.

### UCB-CS61B-TESTING
**UC Berkeley CS 61B — Project Testing**

https://sp26.datastructur.es/proj4/proj4-testing/

BuildLens use:
- test foundational abstractions instead of relying only on end-to-end/manual UI testing;
- use small inputs to make debugging easier to reason about;
- debugger + targeted unit tests complement visual/manual inspection.

### UCB-CS61B-DEBUGGING
**UC Berkeley CS 61B — Debugger introduction**

https://sp26.datastructur.es/homeworks/hw03

BuildLens use:
- call stack;
- variables;
- breakpoints;
- step into / over / out;
- debugger as an explicit later learning mode.

### UCB-CS61B-HELP
**UC Berkeley CS 61B — debugging/help guidance**

https://sp26.datastructur.es/resources/using-ed/

BuildLens use:
- explain why you think something is correct rather than asking "is this correct?";
- state the failing behavior precisely;
- report what debugging has already established;
- isolate the smallest suspicious method/lines when possible.

### UCB-CS61B-GIT
**UC Berkeley CS 61B — Using Git**

https://sp26.datastructur.es/resources/using-git/

BuildLens use:
- understand version control as history of code revisions rather than a deployment-only tool;
- connect BuildLens diff/history/reconciliation features to standard Git mental models.

### UCB-CS162-DESIGN-REVIEW
**UC Berkeley CS 162 — project design review guidance**

https://people.eecs.berkeley.edu/~kubitron/courses/cs162-S19/sp19/static/projects/proj2.pdf

BuildLens use:
- design before implementation;
- oral review of one's own design;
- ability to explain why design choices were made;
- test/edge-case reasoning as part of design ownership.

### UCB-CS162-2026
**UC Berkeley CS 162 Spring 2026 — Learning by Doing**

https://cs162.org/static/lectures/1.pdf

BuildLens use:
- large-codebase comfort;
- debugging-tool fluency;
- design documents as high-level explanations;
- oral questioning as an understanding check.

---

## Practitioner / Social-Media Signals

These are anecdotal. They are useful for exercise realism, not academic authority.

### REDDIT-CODE-REVIEW-INTERVIEW
**Experienced Developers — code-review interview discussion**

https://www.reddit.com/r/ExperiencedDevs/comments/uedzmu/code_review_interview/

BuildLens use:
- unfamiliar code review exercises should include multiple issue classes such as correctness, architecture, security, tests, performance, and unnecessary complexity.

### REDDIT-AI-ERA-INTERVIEWS
**Experienced Developers — interviewing developers in 2026**

https://www.reddit.com/r/ExperiencedDevs/comments/1t9m4cq/how_are_you_effectively_interviewing_devs_now/

BuildLens use:
- reinforce the final ability to review generated code, identify defects, and defend choices rather than merely generate a take-home.

### REDDIT-DEBUGGING-INTERVIEW
**Experienced Developers — debugging interview preparation**

https://www.reddit.com/r/ExperiencedDevs/comments/1mu37g4/

BuildLens use:
- call-stack reading;
- step into/over/out;
- variable/watch inspection;
- deliberate hypothesis-driven debugging.

### REDDIT-RUBBER-DUCK
**Programming discussions — rubber-duck debugging**

https://www.reddit.com/r/programming/comments/ygt105

BuildLens use:
- teach-aloud mode;
- require environment/background, tests attempted, outcomes, and next hypotheses when explaining a bug.


---

## Verified 2026 Curriculum / Defense Sources

### CMU-213-2024-SYLLABUS
**CMU 15-213 / 15-513 syllabus — detailed learning objectives**

https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15213-m24/www/syllabus/syllabus.pdf

Additional BuildLens ideas:
- performance is more than asymptotic complexity;
- process/thread control, virtual memory, networking;
- consequences of crashes, security vulnerabilities, poor CPU/memory performance;
- compilers, analyzers, debuggers, consistency checkers, profilers;
- synchronization for shared resources.

### UCB-CS61B-DESIGN-DOC-2026
**Berkeley CS61B — Technical Design Documents**

https://sp26.datastructur.es/resources/design-doc/

BuildLens use:
- design docs should capture data, data structures, algorithms, complexity, open/closed questions, and a diagram;
- record the reasoning process, not line-for-line pseudocode.

### UCB-CS162-POLICIES-2026
**Berkeley CS162 Fall 2026 — design and oral review**

https://cs162.org/policies/

BuildLens use:
- working code alone is insufficient;
- design should simplify future enhancements;
- design review catches errors early;
- learner must explain and defend approach;
- review assesses actual understanding.

### UCB-CS162-DESIGN-2026
**Berkeley CS162 — Project 3 Design**

https://cs162.org/static/proj/proj-filesys/docs/deliverables/design/

BuildLens use:
- convince the reviewer the design satisfies requirements and edge cases;
- explicitly address shared resources and synchronization;
- simpler/verifiable synchronization is preferable;
- rationale should compare alternatives and shortcomings;
- consider conceptual simplicity, coding effort, time/space complexity, and extensibility.

### UCB-CS162-SYSTEMS-2026
**Berkeley CS162 course topics**

https://cs162.org/policies/
https://cs162.org/

BuildLens use:
- processes, IPC, synchronization;
- memory allocation / virtual memory;
- file systems / storage;
- sockets / networking;
- transactions;
- distributed systems;
- security/privacy;
- reliability.

---

## Public Examples of Technical-Decision Explanations

These are style/examples, not authorities about which technology to choose.

### DEFENSE-EXAMPLE-CONTEXT-CHANGED
**Atithie Engineering — Why We Chose PostgreSQL Over MongoDB**

https://atithie.com/blog/postgres-over-mongodb/

Style lesson:
- explain why the original decision made sense for the MVP;
- explain which later requirements invalidated the original assumptions;
- name migration cost;
- avoid claiming the rejected technology is universally bad;
- state workloads where the rejected option can still be right.

### DEFENSE-EXAMPLE-REQUIREMENTS-FIRST
**Trigger.dev — real-time architecture**

https://trigger.dev/blog/how-we-built-realtime

Style lesson:
- state the obvious initial idea;
- enumerate concrete requirements/problems it failed;
- show how the chosen mechanism addressed those requirements;
- connect architecture to actual workload rather than fashion.

### DEFENSE-EXAMPLE-PLAIN-LANGUAGE
**r/softwarearchitecture — architecture trade-off process (2026)**

https://www.reddit.com/r/softwarearchitecture/comments/1rb69ny/anyone_formalized_their_software_architecture/

Anecdotal style lessons:
- ask "what would have to be true" for each option;
- use a 2 AM failure/operability check;
- consider whether an unfamiliar future developer can debug the design;
- consider the simplest/most boring option that still meets the requirement;
- document the reason in plain language rather than filling a template mechanically.

### DEFENSE-EXAMPLE-REQUIREMENTS-TRADEOFFS
**r/ExperiencedDevs — system design interview discussion (2025)**

https://www.reddit.com/r/ExperiencedDevs/comments/1ntdpkn/elements_of_a_good_system_design_interview/

Anecdotal style lesson:
- tradeoffs should map back to requirements;
- strong system-design discussion can move from a simple ambiguous problem into deeper flows and tradeoffs.

### DEFENSE-EXAMPLE-CODE-WALKTHROUGH
**r/ExperiencedDevs — experienced-hire interview process**

https://www.reddit.com/r/ExperiencedDevs/comments/1c5645d/designing_a_new_interview_process_for_experienced/

Anecdotal style lesson:
- expect questions about why a library was chosen;
- how code could be made more modular;
- how the design would respond to a changed business requirement;
- ability to keep discussing ideas/concerns is a useful signal of genuine ownership.

### DEFENSE-EXAMPLE-INHERITED
**r/ExperiencedDevs — explaining old/inherited decisions (2026)**

https://www.reddit.com/r/ExperiencedDevs/comments/1tuumx4/how_deep_can_you_go_in_your_past_experiences/

BuildLens rule:
- never invent a rationale for a decision you did not make;
- distinguish original historical rationale from your later decision to keep/change the design.


---

## Python implementation-adjacent sources

### PY-CONTROLFLOW-FUNCTIONS
**Python Tutorial — More Control Flow Tools / Defining Functions**  
https://docs.python.org/3/tutorial/controlflow.html

Use for `if`, loops, `def`, parameters/arguments, local names, return values, and function annotation syntax.

### PY-STDTYPES
**Python — Built-in Types**  
https://docs.python.org/3/library/stdtypes.html

Use for strings/sequences, indexing, and prefix/string operations introduced by diff parsing.

### PY-DATACLASSES
**Python — dataclasses**  
https://docs.python.org/3/library/dataclasses.html

Use for named records and the precise meaning/limits of `frozen=True`.

### PY-TYPING
**Python — typing**  
https://docs.python.org/3/library/typing.html

Use for contracts/type hints and the crucial fact that Python runtime does not enforce annotations.

### PY-ARGPARSE
**Python — argparse**  
https://docs.python.org/3/library/argparse.html

Use for Phase 6 command-line argument parsing.

### PY-SUBPROCESS
**Python — subprocess**  
https://docs.python.org/3/library/subprocess.html

Use for Git child processes, arguments, stdout/stderr, return codes, timeout, bytes-vs-text, and process failures.

### PY-PATHLIB
**Python — pathlib**  
https://docs.python.org/3/library/pathlib.html

Use for repository/worktree path representation and filesystem path operations.

### PY-JSON
**Python — json**  
https://docs.python.org/3/library/json.html

Use for JSON↔Python representations, hook/API serialization, and untrusted-input considerations.

### PY-SQLITE3
**Python — sqlite3**  
https://docs.python.org/3/library/sqlite3.html

Use for SQL parameters, transactions, commit/rollback, connection/context-manager behavior, and version-specific transaction semantics.


---

## Adaptive remediation / scaffolding sources

### CMU-SCAFFOLDING-MODEL-FADE
**CMU Eberly Center — Labs / Studios**

https://www.cmu.edu/teaching/designteach/teach/instructionalstrategies/labsstudios.html

BuildLens use:
- modeling;
- scaffolding;
- coaching;
- fading;
- increasing learner independence;
- generalizing from practice to principles.

### CMU-GRADUAL-COMPLEXITY
**CMU Eberly Center — Critical-thinking instructional scaffolding**

https://www.cmu.edu/teaching/solveproblem/strat-criticalthinking/criticalthinking-07.html

BuildLens use:
- assignments should gradually increase difficulty/complexity;
- early tasks may provide explicit structure/prompts;
- supports should be removed as mastery develops;
- the purpose of scaffolding is to progress toward complexity, not permanently avoid it.

### CMU-WORKED-EXAMPLES
**CMU Eberly Center — Concrete Strategies for Active Learning**

https://www.cmu.edu/teaching/online/designteach/strategies/activelearning.html

BuildLens use:
- a solved worked example can provide a more structured task when open problem solving is too demanding;
- require learners to explain each step;
- optionally include incorrect steps for diagnosis;
- follow the worked example with active retrieval rather than passive rereading.

### CMU-MASTERY-INDIVIDUAL-PACE
**CMU Eberly Center — Mastery-based course strategy**

https://www.cmu.edu/teaching/solveproblem/strat-backgroundknowledge/backgroundknowledge-08.html

BuildLens use:
- do not advance to later objectives until the current objective is demonstrated;
- allow individualized pacing;
- provide additional scaffolding to learners who need it.

### CMU-RETRIEVAL-LOW-STAKES
**CMU Eberly Center — Retrieval Practice for Improved Learning**

https://www.cmu.edu/teaching/resources/instructionalstrategies/activelearningstrategies/retrievalpractice/index.html

BuildLens use:
- frequent, low-stakes retrieval;
- use assessments as learning opportunities;
- wrong attempts provide diagnostic information rather than acting as high-stakes failures.

### UCB-CS61A-BASIC-TO-CHALLENGE
**UC Berkeley CS61A — environment/function study guides and discussions**

https://www-inst.eecs.berkeley.edu/~cs61a/fa22/study-guide/environments-hof/
https://www-inst.eecs.berkeley.edu/~cs61a/fa25/disc/disc01/

BuildLens use:
- reason through execution before asking a computer to check;
- use diagrams/state tracking;
- move through basic/easy/challenge practice rather than beginning at maximum complexity;
- check predictions after committing them.

### PYTHON-STRINGS-INDEXING
**Python Tutorial — An Informal Introduction to Python**

https://docs.python.org/3/tutorial/introduction.html

BuildLens use:
- string indexing;
- negative indices;
- slicing;
- immutable string behavior;
- Phase 0/1 `R0` syntax remediation.

### PYTHON-CONTROL-FUNCTIONS
**Python Tutorial — More Control Flow Tools**

https://docs.python.org/3/tutorial/controlflow.html

BuildLens use:
- `if` / `elif` / `else`;
- function definitions;
- formal parameters;
- local symbol tables;
- return behavior;
- use as documentation after a learner attempt, not as an answer key before prediction.
