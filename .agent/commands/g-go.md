Autonomous backlog execution: $ARGUMENTS

> ⚠️  **SELF-REVIEW MODE** — g-go runs both implementation AND verification in one session.
> Independent verification is bypassed. For production task completion use two sessions:
>   Session 1: `@g-go-code`  →  Session 2 (new window/agent): `@g-go-review`

## What This Command Does

Works through the task backlog autonomously, completing as many tasks as possible in a single session. All questions, blockers, and decisions that need human input are collected and presented at the end — never interrupting the flow.

## Execution Protocol

### 1. Load Context (Before Touching Anything)

Read the following files **in this order** to understand the project state:
- `.galdr/PROJECT.md` — mission, goals, ecosystem context
- `.galdr/PLAN.md` — current project milestones and development focus
- `.galdr/FEATURES.md` — PRD index (understand delivery intent)
- `.galdr/SUBSYSTEMS.md` — subsystem registry (understand scope before touching files)
- `.galdr/BUGS.md` — open bugs (**read before TASKS** — never implement a fix that re-introduces a known bug)
- `.galdr/TASKS.md` — master task list
- `.galdr/CONSTRAINTS.md` — guardrails (if exists)
- `git log --oneline -10` — recent changes

### 2. Build the Work Queue

**Bugs come before tasks.** If BUGS.md has any open bugs with status `Open` or `In Progress`, those enter the queue first — before any pending tasks. A known broken thing should not be skipped in favor of new work.

Work queue construction order:

**Tier 1 — Open bugs (from BUGS.md + individual bug files in `bugs/`):**
- Severity: Critical bugs first, then High, Medium, Low
- Only bugs with no external blocker (e.g. not waiting on an API key or upstream fix)

**Tier 2 — Pending tasks (from TASKS.md):**
- Status is `[ ]` (pending) or `[📋]` (ready)
- No unmet dependencies (prerequisite tasks are `[✅]`)
- Not explicitly marked as `ai_safe: false`
- Not blocked by human input
- Priority: Critical → High → Medium → Low

If `$ARGUMENTS` restricts the queue, supported filters:
- Task IDs: `@g-go tasks 7, 9, 12`
- Bug IDs: `@g-go bugs BUG-003, BUG-007`
- Subsystem: `@g-go subsystem vault-hooks-automation`
- Tier only: `@g-go bugs-only` / `@g-go tasks-only`
- Combined: `@g-go subsystem cross-project bugs-only`


### 3. Work Through Tasks Sequentially

For each task in the queue:

**a) Read the task file** — understand objective and acceptance criteria
**b) Implement the solution** — write code, make changes, satisfy acceptance criteria
**b2) AC gate** — before moving on, walk every `- [ ]` acceptance criterion in the task spec:
  - Each criterion confirmed met in actual files/code? → continue
  - Any unmet criterion → return to **(b)** and address it
  - Cannot meet a criterion this session → log as Blocker in step 4 and skip this task (no partial marking)
  - **Stub/TODO scan**: search files modified for this task for bare `# TODO`, `// TODO`, `pass` (non-abstract), `raise NotImplementedError`, `throw new Error("not implemented")` — each is an unmet criterion until annotated `TODO[TASK-X→TASK-Y]` with a follow-up task (see `g-rl-34`)
  - **Bug-discovery check**: pre-existing bugs → BUG entry + `BUG[BUG-{id}]` comment; current-task bugs → fix inline before `[🔍]` (see `g-rl-35`)
**c) Validate** — run any available tests, check lints, verify the work
**d) Record decisions** — if you chose approach A over B, append to `.galdr/DECISIONS.md`
**e) Update subsystem Activity Log** — for each subsystem in the task's `subsystems:` field, append a row to `.galdr/subsystems/{name}.md` Activity Log: `| {date} | TASK | {id} | {title} | — |`. If the spec file doesn't exist, create a stub (see `g-skl-subsystems` CREATE SUBSYSTEM SPEC).
**f) Update task status** — mark `[🔍]` in task file + TASKS.md; mark `[✅]` only after independent self-review confirms the work
**f2) Docs check** (only when marking `[✅]`) — does this task add/remove/change user-facing behavior?
  - **YES** → append entry to `CHANGELOG.md` under `[Unreleased]`; update `README.md` if a relevant section exists
  - **NO** (internal refactor, task housekeeping, bug fix with no interface change) → skip
  - See `g-rl-26-readme-changelog.mdc` for qualifying criteria and format
**g) Move to next task**

### 4. Question & Blocker Collection

**DO NOT** stop to ask questions during execution. Instead, maintain a running log:

```markdown
## Deferred Items

### Questions (Need Human Answer)
- Q1: [question] (encountered during task #X)
- Q2: [question] (encountered during task #Y)

### Blockers (Could Not Proceed)
- B1: Task #X — [why it's blocked]
- B2: Task #Y — [missing dependency / credentials / unclear spec]

### Decisions Made (FYI)
- D1: Task #X — chose approach A over B because [reason]
- D2: Task #Y — interpreted ambiguous spec as [interpretation]
```

### 5. Record Decisions

Before writing the session summary, append any new architectural or workflow decisions to
`.galdr/DECISIONS.md`:

> If you chose approach A over B, deferred a feature, changed a convention, or made any
> decision that should inform future agents — append it to `.galdr/DECISIONS.md` using
> the ID format `D{NNN}` (next sequential ID after the last existing entry).

### 6. Session Summary (Always End With This)

After completing as many tasks as possible, present:

```markdown
## Backlog Execution Summary

### Completed
- [✅] Task #X: {title}
- [✅] Task #Y: {title}

### Skipped (Blocked)
- Task #Z: {reason — dependency, needs human, unclear spec}

### Failed (Attempted but couldn't finish)
- Task #W: {what went wrong}

### Deferred Questions & Blockers
{the collected questions and blockers from step 4}

### Recommended Next Steps
1. [what to do next]
2. [what to do next]

### Git Status
- Changes committed: Yes/No
- Uncommitted changes: {list if any}
```

## Behavioral Rules

| Rule | Why |
|------|-----|
| Never ask questions mid-execution | The whole point is uninterrupted autonomous work |
| Log every decision you make autonomously | User needs to review what you decided |
| Skip tasks you can't complete, don't fail the whole run | Maximize total output |
| Commit after each completed task (if user allows) | Preserve progress incrementally |
| Respect CONSTRAINTS.md | Don't violate project guardrails |
| Stop if a task would be destructive (schema drops, data loss) | Safety first — log it as a blocker |
| For independent verification: use g-go-code + g-go-review across two sessions | Self-review mode (`g-go`) skips the independence gate |

## Usage Examples

**Work everything available:**
```
@g-go
```

**Work specific tasks:**
```
@g-go tasks 7, 9, 12
```

**Work specific bugs:**
```
@g-go bugs BUG-003, BUG-007
```

**Work a specific subsystem (bugs + tasks):**
```
@g-go subsystem vault-hooks-automation
```

**Bugs only:**
```
@g-go bugs-only
```

**Work only critical/high priority:**
```
@g-go critical and high only
```

**For independent two-session workflow (recommended):**
```
Session 1:  @g-go-code
Session 2 (new agent window):  @g-go-review
```

Let's get to work.
