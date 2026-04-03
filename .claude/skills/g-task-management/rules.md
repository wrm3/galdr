# Task Management Rules

> Detailed implementation rules for the galdr-task-management Skill.
> These rules are derived from Cursor's galdr system.

## Overview

These rules provide comprehensive guidance for implementing task management using the galdr system. They cover task file formats, YAML validation, status management, file naming conventions, phase-based organization, and integration with the broader project management ecosystem.

## Core Task Management Rules

### Task File Creation

**Location**: `.galdr/tasks/`

**Naming Convention**: `task{id}_descriptive_name.md`
- ID must be within the appropriate phase range
- Phase 0: 1-99, Phase 1: 100-199, Phase 2: 200-299, etc.
- Descriptive name uses underscores, lowercase
- Examples: `task001_setup_database.md`, `task142_implement_auth.md`

**Creation Process**:
1. Determine which phase the task belongs to
2. Determine next available task ID within that phase
3. Create task file with proper naming
4. Add YAML frontmatter with required fields including `phase`
5. Add task content (objective, criteria, notes)
6. Update TASKS.md with new entry under correct phase section

### Phase-Based Task Numbering

**Task ID Numbering by Phase**:
- **Phase 0** (Setup/Infrastructure): Tasks 1-99
- **Phase 1** (Foundation): Tasks 100-199
- **Phase 2** (Core Development): Tasks 200-299
- **Phase 3** (Enhancement): Tasks 300-399
- **Phase N**: Tasks N×100 to N×100+99

**ID Determination**:
1. Identify target phase for the task
2. Read all existing task files in that phase range
3. Extract ID from each filename
4. Find maximum ID within phase range
5. New ID = max ID + 1 (or phase start if first task)

### YAML Frontmatter Validation

**Required Fields**:
```yaml
---
id: {number}                    # Sequential ID within phase range
title: 'Task Title'             # Brief, actionable title
type: task|bug_fix|phase|retroactive_fix
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
phase: {number}                 # Phase number (0, 1, 2, etc.)
---
```

**Optional Fields**:
```yaml
subsystems: [list]              # Affected system components
project_context: 'Brief description'
dependencies: [task_ids]        # Tasks that must complete first
estimated_effort: 'time estimate'
created_date: 'YYYY-MM-DD'
completed_date: 'YYYY-MM-DD'
assigned_to: 'Developer name'
```

**Validation Rules**:
- `id` must be unique across all tasks
- `id` must be within appropriate phase range
- `title` must be non-empty string
- `type` must be one of allowed values
- `status` must be one of allowed values
- `priority` must be one of allowed values
- `phase` must be a valid phase number
- `dependencies` must reference existing task IDs
- Dates must be in ISO format (YYYY-MM-DD)

### Status Management Rules

**Status Lifecycle**:
```
pending → in-progress → completed
                     ↓
                   failed
```

**Status Update Procedure**:
1. **Start Task** (`pending` → `in-progress`):
   - Update task file YAML: `status: in-progress`
   - Update TASKS.md: `[ ]` → `[🔄]`
   - Optional: Add `started_date` field

2. **Complete Task** (`in-progress` → `completed`):
   - Update task file YAML: `status: completed`
   - Update TASKS.md: `[🔄]` → `[✅]`
   - Add `completed_date` field
   - Document actual effort if estimated

3. **Fail Task** (`in-progress` → `failed`):
   - Update task file YAML: `status: failed`
   - Update TASKS.md: `[🔄]` → `[❌]`
   - Add failure reason in task notes
   - Consider creating new task for retry

**Atomic Updates**:
- Task file and TASKS.md must be updated together
- Never update one without the other
- Use transaction-like approach (update both or neither)

### 🚨 MANDATORY Task Completion Enforcement

**CRITICAL**: After completing task work, you MUST mark the task complete IMMEDIATELY.

**Automatic Completion Triggers** (when ANY occur, mark task complete):
- Code changes implemented and accepted
- Feature finished and working
- Bug fixed and verified
- All acceptance criteria satisfied

**Self-Check at END of Every Response**:
```
□ Did I complete work for a task?
  → Update task file: status: completed
  → Update TASKS.md: [🔄] → [✅]
  → Confirm to user
```

**Failure Mode**: If you implement work but don't mark complete = SYSTEM VIOLATION

### 🚨 MANDATORY Phase Completion Gate

**Before starting ANY task in Phase N+1**:
1. Verify ALL Phase N tasks are [✅] complete
2. Generate Phase SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
3. Present analysis to user
4. WAIT for explicit user approval ("proceed", "approved", "continue")
5. **Prompt for git commit** after approval
6. Only then start Phase N+1 tasks

**Git Commit After Approval**:
- Suggest commit message: `Phase {N}: {Phase Name} complete`
- User can: "commit" (run it), "skip" (proceed without), or provide custom message
- Complete commit/skip before starting next phase

**Phase Gate Violation**: Starting Phase N+1 without user approval = BLOCKED

### Windows Emoji Requirements

**Status Indicators**:
- `[ ]` - Pending (checkbox, not emoji)
- `[🔄]` - In Progress (counterclockwise arrows)
- `[✅]` - Completed (check mark button)
- `[❌]` - Failed (cross mark)

**Why These Emojis**:
- Windows-safe (render correctly on Windows 10/11)
- Clear visual distinction
- Supported across all terminals and IDEs
- Part of Unicode standard

**Usage in TASKS.md**:
```markdown
## Phase 0: Setup & Infrastructure
- [ ] Task 001: Setup database
- [🔄] Task 002: Configure environment

## Phase 1: Foundation
- [✅] Task 100: Create data models
- [❌] Task 101: Deploy to production (failed)
```

### TASKS.md Update Procedures

**File Structure**:
```markdown
# Project Name - Task List

## Phase 0: Setup & Infrastructure
- [ ] Task 001: Setup project
- [🔄] Task 002: Configure environment

## Phase 1: Foundation
- [ ] Task 100: Design database
- [ ] Task 101: Implement handlers

## Phase 2: Core Development
- [ ] Task 200: Build core classes
- [ ] Task 201: Create API endpoints

## Completed Tasks
- [✅] Task 000: Initial planning

## Blocked Tasks
- [❌] Task 020: Deploy (blocked by Task 002)
```

**Update Rules**:
- Group tasks by phase
- Keep active tasks at top within each phase
- Move completed tasks to "Completed Tasks" section
- Document blocked tasks with blocking reason
- Maintain consistent formatting

**Atomic Update Pattern**:
```
1. Read current TASKS.md
2. Locate task entry by ID
3. Update status emoji
4. Write back to TASKS.md
5. Verify update succeeded
```

### Sub-Task Creation Rules

**When to Create Sub-Tasks**:
- Task complexity score ≥ 7 (see workflow rules)
- Task spans multiple subsystems
- Task has distinct, sequential phases
- Task estimated > 2-3 developer days

**Sub-Task Structure**:
```
Parent: task142_implement_authentication.md
Sub-tasks:
  - task142.1_setup_database.md
  - task142.2_create_api.md
  - task142.3_build_ui.md
```

**Sub-Task YAML**:
```yaml
---
id: "142.1"              # String ID for sub-tasks
title: 'Setup Database'
type: task
status: pending
priority: high
phase: 1                 # Same phase as parent
parent_task: 142
dependencies: []        # Can depend on other tasks/sub-tasks
---
```

**Parent Task Update**:
- Add `has_subtasks: true` field
- Add `subtasks: [142.1, 142.2, 142.3]` field
- Parent status = `in-progress` when any subtask started
- Parent status = `completed` when all subtasks completed

### Dependency Management

**Dependency Types**:
- **Hard Dependency**: Task cannot start until dependency completes
- **Soft Dependency**: Task can start but may need rework
- **Blocking**: Task blocks another task from starting

**Dependency Declaration**:
```yaml
dependencies: [001, 002, 003]  # Task IDs
```

**Dependency Validation**:
- All dependency IDs must exist
- No circular dependencies allowed
- Dependency graph must be acyclic (DAG)

**Dependency Checking**:
```
Before starting task:
1. Read task file
2. Check dependencies field
3. For each dependency ID:
   - Read dependency task file
   - Verify status = completed
4. If all dependencies completed → can start
5. If any dependency not completed → blocked
```

### Error Handling

**File Not Found**:
- Task file missing → Error, cannot proceed
- TASKS.md missing → Create from template
- Phase file missing → Warning, continue

**Invalid YAML**:
- Syntax error → Fail with clear error message
- Missing required field → Fail with field name
- Invalid field value → Fail with allowed values

**Concurrent Updates**:
- Read-modify-write pattern
- Check file timestamp before write
- Retry on conflict
- Maximum 3 retries

**Validation Failures**:
- Log validation error
- Do not create/update task
- Provide clear error message
- Suggest corrective action

## File Organization Rules

### Working Directory Structure

**Primary Location**: `.galdr/`

**Required Subdirectories**:
```
.galdr/
├── tasks/              # Individual task files
├── phases/             # Phase documentation
└── memory/             # Archived tasks (optional)
```

**Core Files**:
- `TASKS.md` - Master task checklist
- `PLAN.md` - Product Requirements Document
- `BUGS.md` - Bug tracking (subset of tasks)
- `PROJECT_CONTEXT.md` - Project mission and goals
- `SUBSYSTEMS.md` - Component registry
- `FILE_REGISTRY.md` - File documentation
- `MCP_TOOLS_INVENTORY.md` - Available tools

### Auto-Creation Rules

**Folder Creation**:
- Always create missing folders automatically
- No confirmation prompts
- Silent operation (only report what was created)
- Create parent directories as needed

**Template Creation**:
- Create missing `.md` files with blank templates
- Use standard templates for each file type
- Populate with minimal required content
- User can edit after creation

**When to Auto-Create**:
- System initialization
- First task creation
- Missing required files detected
- User requests new phase/subsystem

## Integration with Cursor

These rules maintain 100% compatibility with Cursor's galdr system:

- **File Format**: Identical YAML frontmatter and markdown structure
- **File Locations**: Same directory structure
- **Status Indicators**: Same Windows-safe emojis
- **Naming Conventions**: Same task ID and filename patterns
- **Workflow**: Same task lifecycle and status transitions
- **Phase Organization**: Same phase-based task grouping

**Cursor Rules Source**: `.cursor/rules/galdr/rules/rules.mdc`

## Cross-References

- **Main Skill**: `SKILL.md` - Complete skill documentation
- **Reference Materials**: `reference/` - Detailed schemas and templates
- **Examples**: `examples/` - Working examples of task files
- **Planning Integration**: See `g-planning` Skill
- **QA Integration**: See `g-qa` Skill

## Usage Notes

### Skill Triggers

The `g-task-management` Skill is triggered when:
- User mentions "task", "todo", "work item"
- User requests task creation, update, or status change
- User asks about project tasks or progress

### Cursor Integration

Cursor uses rules from `.cursor/rules/galdr/rules/rules.mdc` which work with the same `.galdr/` files.

### Best Practices

1. **Always update both**: Task file + TASKS.md together
2. **Use descriptive names**: Task titles should be clear and actionable
3. **Track dependencies**: Document blocking relationships
4. **Estimate effort**: Helps with planning and retrospectives
5. **Document context**: Link tasks to phases and project goals
6. **Archive completed**: Move old tasks to memory/ folder periodically
7. **Use correct phase IDs**: Ensure task IDs fall within their phase range

---

*These rules ensure consistent, reliable task management in Cursor.*
