---
description: "galdr task Update"
---

Update task status: $ARGUMENTS

## What This Command Does

Updates task status in the galdr system, ensuring BOTH the task file AND TASKS.md are updated.

## Task Update Workflow

### 1. Identify Task
I'll:
- Find the task file in `.galdr/tasks/`
- Read current task details
- Confirm task identity

### 2. Update Status
**Valid Status Transitions:**
- `pending` → `in-progress` (starting work)
- `in-progress` → `completed` (finished successfully)
- `in-progress` → `failed` (blocked or abandoned)
- `pending` → `completed` (retroactive documentation)

### 3. CRITICAL: Update BOTH Files

**Task File** (`.galdr/tasks/task{ID}_name.md`):
```yaml
---
status: completed              # Update this
completed_date: '2026-03-18'   # ALWAYS set when completing (today's date)
actual_effort: '2 hours'       # Add if completing
---
```

**TASKS.md** (`.galdr/TASKS.md`):
```markdown
# Before
- [ ] Task 001: Setup environment

# After starting
- [🔄] Task 001: Setup environment

# After completing
- [✅] Task 001: Setup environment
```

### 4. Status Indicators in TASKS.md
- `[ ]` → Task listed, NO file created yet (BLOCKED)
- `[📋]` → Task file created, ready to start
- `[🔄]` → In Progress (actively working)
- `[✅]` → Completed
- `[❌]` → Failed or cancelled

### 5. Completion Documentation
When completing a task, I'll also:
- Add completion notes to task file
- Record actual effort vs estimated
- Note any lessons learned
- Check for dependent tasks that can now proceed

## MANDATORY: Dual Update Rule

**I MUST update BOTH files in the SAME response:**
1. ✅ Update task file YAML frontmatter (status, dates)
2. ✅ Update TASKS.md entry (emoji indicator)

**Failure to update BOTH = System violation**

## What I Need From You
- Task ID or title to update
- New status (in-progress, completed, failed)
- Completion notes (if finishing)

Let's update this task!
