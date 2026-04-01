Autonomous backlog execution: $ARGUMENTS

## What This Command Does

Works through the task backlog autonomously, completing as many tasks as possible in a single session. All questions, blockers, and decisions that need human input are collected and presented at the end — never interrupting the flow.

## Execution Protocol

### 1. Load Context (Before Touching Anything)

Read the following files to understand the project state:
- `.galdr/docs/PROJECT_CONTEXT.md` — mission and goals
- `.galdr/TASKS.md` — master task list
- `.galdr/docs/ARCHITECTURE_CONSTRAINTS.md` — guardrails (if exists)
- `git log --oneline -10` — recent changes

### 2. Build the Work Queue

From TASKS.md, identify all **workable** tasks:
- Status is `[ ]` (pending) or `[📋]` (ready)
- No unmet dependencies (prerequisite tasks are `[✅]`)
- Not explicitly marked as `ai_safe: false`
- Not blocked by human input

**Priority order:**
1. Critical priority, unblocked
2. High priority, unblocked
3. Medium priority, unblocked
4. Low priority, unblocked

If `$ARGUMENTS` specifies task IDs or a phase, restrict the queue to those.

### 3. Work Through Tasks Sequentially

For each task in the queue:

**a) Read the task file** — understand objective and acceptance criteria
**b) Implement the solution** — write code, make changes, satisfy acceptance criteria
**c) Validate** — run any available tests, check lints, verify the work
**d) Update task status** — mark `[✅]` in both the task file and TASKS.md
**e) Move to next task**

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

### 5. Session Summary (Always End With This)

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
| Respect ARCHITECTURE_CONSTRAINTS.md | Don't violate project guardrails |
| Stop if a task would be destructive (schema drops, data loss) | Safety first — log it as a blocker |

## Usage Examples

**Work everything available:**
```
@g-go
```

**Work only Phase 2 tasks:**
```
@g-go phase 2
```

**Work specific tasks:**
```
@g-go tasks 201, 203, 207
```

**Work only critical/high priority:**
```
@g-go critical and high only
```

## What Makes This Different From @g-sprint

| | @g-go | @g-sprint |
|---|---|---|
| Time limit | None (until done or blocked) | 2 hours |
| Task source | TASKS.md backlog directly | SPRINT.md (pre-filtered) |
| Questions | Saved until end | N/A (ai_safe tasks only) |
| Verification | Self-completes tasks | Submits for separate verification |
| Claim protocol | No git-based claiming | Atomic git claim with TTL |
| Best for | Solo developer sessions | Multi-agent parallel work |

Let's get to work.
