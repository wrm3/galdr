---
description: "Create or update PROJECT_GOALS.md with strategic project goals"
---

Update project goals: {{args}}

## What This Workflow Does

Creates or updates `.galdr/PROJECT_GOALS.md` to reflect the project's
current strategic direction. Goals are loaded into every session to
steer AI decisions and validate work.

## Workflow

### If PROJECT_GOALS.md Does NOT Exist — Create It

**Step 1: Gather information**
I'll ask (or infer from context):
- What is this project trying to achieve? (Vision)
- What are the 2-4 primary measurable goals?
- What is explicitly out of scope? (Non-Goals)
- How will we know when we've succeeded? (Success Metrics)

**Step 2: Write PROJECT_GOALS.md**
```markdown
# PROJECT_GOALS.md

## Vision
[1-2 sentences]

## Primary Goals
| ID   | Goal    | Target / Metric  | Status |
|------|---------|------------------|--------|
| G-01 | [name]  | [metric]         | active |

## Secondary Goals
## Non-Goals
## Success Metrics

## Goal Log
| Date       | Change             | Reason        |
|------------|--------------------|---------------|
| {today}    | Initial goals      | Project setup |
```

### If PROJECT_GOALS.md EXISTS — Update It

**Parse `{{args}}`** for the type of change:
- `add G-03: ...` — add a new goal
- `update G-01: ...` — update an existing goal
- `retire G-02: ...` — mark a goal as retired
- `non-goal: ...` — add something to Non-Goals

**Process:**
1. Read current PROJECT_GOALS.md
2. Make the specified change
3. Add a dated entry to the Goal Log
4. Write updated file
5. Confirm: "Updated: [summary of change]"

## Examples

```
/g-goal-update
/g-goal-update add G-03: Launch monetization — Stripe checkout live by Q2
/g-goal-update retire G-02: MVP shipped, goal complete
/g-goal-update non-goal: We are not building mobile apps in v1
```
