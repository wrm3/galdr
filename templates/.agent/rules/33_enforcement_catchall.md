---
description: "Ambient enforcement guardrails — always active regardless of which agent is loaded"
globs:
alwaysApply: true
---

# Enforcement Catchall

These rules fire on EVERY response, even when no galdr agent is explicitly active.

## Error Reporting (Zero Tolerance)

If your response mentions ANY of the following — create a `BUGS.md` entry immediately:
- "error", "warning", "pre-existing", "was already there", "unrelated error"
- "lint error", "TypeScript error", "compile error", "exception"

"Pre-existing" and "unrelated" are NOT exemptions. If it's worth mentioning, it's worth logging.

**Fast-path entry** (takes 30 seconds):
```markdown
### BUG-NNN
- **Title**: [brief]
- **Severity**: Low/Medium/High/Critical
- **Status**: Open
- **File**: path/to/file (line N)
- **Note**: Pre-existing. Not blocking current task.
- **Created**: YYYY-MM-DD
```

| Rationalization | Reality |
|---|---|
| "It's pre-existing, not related to my changes" | Pre-existing = undocumented. Log it anyway. |
| "It's just a warning, not a real error" | Warnings become errors. Log it now. |
| "I'll log it after I finish this task" | You won't. Log it before moving on. |
| "It's in someone else's code" | Still in this codebase. Still needs a record. |
| "The user probably already knows" | Then the log takes 30 seconds and confirms it. |
| "It's too minor to bother with" | BUG-NNN with severity:Low costs nothing and creates an audit trail. |

## Task Completion (Mandatory Commit Offer)

If work was just completed on any task — offer a git commit before ending the response.
Never end a response after task completion without this offer.

| Rationalization | Reality |
|---|---|
| "The user will commit when they're ready" | Your job is to offer it. Offer it. |
| "It's a small change, not worth committing" | Small changes get lost. Offer the commit. |
| "I already mentioned it earlier in the conversation" | Offer it again at completion. Every time. |

## .galdr/ Folder Gate (HARD RULE)

**NEVER read or write any file inside `.galdr/` without an active galdr agent.**

Before any `.galdr/` operation, select the most appropriate agent:

| Operation | Agent |
|---|---|
| Create/update/complete tasks, TASKS.md | `g-task-manager` |
| Create task, spec it out, "please task" | `g-task-manager` |
| Bugs, errors, BUGS.md | `g-qa-engineer` |
| PRD, phases, planning, PLAN.md | `g-planner` |
| Ideas, goals, IDEA_BOARD.md | `g-ideas-goals` |
| Grooming, sync, health checks | `g-project-manager` |
| PROJECT_CONTEXT.md, SUBSYSTEMS.md | `g-infrastructure` |

If unsure which agent — default to `g-task-manager`.
**No exceptions. No "quick reads." No "just checking."**

| Rationalization | Reality |
|---|---|
| "I'm just reading, not writing" | Reads without agent = no enforcement = sync drift. Use the agent. |
| "It's a quick status check" | 10-second agent selection prevents hours of sync cleanup. |
| "I know what's in the file already" | You might be wrong. The agent reads and enforces. You don't. |

### Task Creation Trigger Phrases (always route to `g-task-manager`)
Any of these → full task creation workflow (file first, TASKS.md second, YAML, phase numbering):
`"create a task"` | `"add a task"` | `"make a task"` | `"task and spec"` | `"spec it out"` |
`"please task"` | `"add to tasks"` | `"task this"` | `"create a task(2)"` | `"task them"`

## Delegation Hint

If the user mentions a task ID (e.g., "task 42", "#103") without explicitly invoking a galdr agent:
→ Activate `g-task-manager` behavior for that operation.

If the user reports a bug or describes unexpected behavior without invoking `g-qa-engineer`:
→ Apply bug logging rules from `g-qa-engineer` immediately.
