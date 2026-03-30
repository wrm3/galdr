---
description: "Review IDEA_BOARD.md and evaluate ideas for promotion or shelving"
---

Review IDEA_BOARD.md: {{args}}

## What This Workflow Does

Reviews all active ideas on the IDEA_BOARD, evaluates readiness, and helps
decide what to promote, shelve, or keep for later.

## Review Workflow

### 1. Load Context
- Read `.galdr/IDEA_BOARD.md`
- Read `.galdr/PROJECT_GOALS.md` (if exists)
- Read `.galdr/TASKS.md` to understand current phase/progress

### 2. Display Summary
```
## IDEA_BOARD Review

Active Ideas: {N}
Evaluating: {list}
Recently Captured: {last 3}

### Ideas That May Be Ready
[Ideas where "When Ready" conditions appear to be met]
```

### 3. Evaluate Each Active Idea
For each idea, assess:
- **Goal Alignment**: Does this align with PROJECT_GOALS?
- **Prerequisites Met**: Are the "When Ready" conditions satisfied?
- **Phase Fit**: Could this be added to the current or next phase?

### 4. Present Options
For each idea, offer:
1. **Promote** — create a task or phase for it
2. **Shelve** — set aside with a reason
3. **Keep raw** — not ready yet, no change
4. **Refine** — update the description or When Ready conditions

### 5. Execute Decisions
- **Promoted**: Update status to `accepted`, add task reference, move to Promoted section, create task via `/g-task-new`
- **Shelved**: Add shelved reason, move to Shelved section
- **Kept**: No change

## Arguments
- `{{args}}` can specify a filter: `feature`, `monetization`, `ready`, `all`, or a specific IDEA-NNN
- Default (no args): show all active ideas

## Examples
```
/g-idea-review
/g-idea-review monetization
/g-idea-review IDEA-003
```
