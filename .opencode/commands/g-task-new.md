Create a new task: $ARGUMENTS

## What This Command Does

Creates a properly structured task in the galdr system.

## Task Creation Workflow

### 1. Gather Information
I'll determine:
- **Task Type**: feature, bug_fix, refactor, documentation
- **Priority**: critical, high, medium, low
- **Target Phase**: Phase 0 (1-99), Phase 1 (100-199), Phase 2 (200-299), etc.
- **Affected Subsystems**: Which components are involved
- **Dependencies**: Other tasks that must complete first

### 2. Create Task File
I'll generate a task file in `.galdr/tasks/` with:

**Filename**: `task{ID}_{descriptive_name}.md`

**YAML Frontmatter**:
```yaml
---
id: {task_id}
title: 'Task Title'
type: feature
status: pending
priority: medium
phase: 0
subsystems: [affected_subsystems]
project_context: How this task relates to project goals
dependencies: []
created_date: '{YYYY-MM-DD}'
completed_date: ''
---
```

**Content Sections**:
- Objective: Clear, actionable goal
- Acceptance Criteria: Specific, measurable outcomes
- Implementation Notes: Technical details
- Testing Plan: How to verify completion

### 3. Update TASKS.md
I'll add the task entry with:
- Status indicator: `[ ]` (pending, no file yet) → `[📋]` (file created)
- Task ID and title
- Correct phase section

### 4. CRITICAL: Dual Update
**I MUST update BOTH:**
1. ✅ Task file in `.galdr/tasks/`
2. ✅ Entry in `.galdr/TASKS.md`

## Phase-Based Task IDs
- **Phase 0** (Setup): Task IDs 1-99
- **Phase 1** (Foundation): Task IDs 100-199
- **Phase 2** (Core Development): Task IDs 200-299
- **Phase N**: Task IDs N×100 to N×100+99

## What I Need From You
- Brief description of what needs to be done
- Which phase this task belongs to
- Any specific requirements or constraints
- Related subsystems or components

Let's create this task!
