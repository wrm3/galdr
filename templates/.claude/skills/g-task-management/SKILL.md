---
name: g-task-management
description: Manage galdr tasks in .galdr/ — create, update, track, query task files and TASKS.md. For tasks, todos, work items, status.
---

# galdr task Management Skill

Manage project tasks using the galdr task management system. This Skill provides capabilities for creating, updating, tracking, and organizing development tasks in a structured, file-based system compatible with multiple AI IDEs.

## System Overview

The galdr system uses a file-based approach where:
- **Master checklist**: `.galdr/TASKS.md` - Central task list with phase headers and status indicators
- **Individual tasks**: `.galdr/tasks/task{id}_descriptive_name.md` - Detailed task files
- **Phase files**: `.galdr/phases/phase{N}_{name}.md` - Phase details with subsystems and objectives
- **Project context**: `.galdr/PROJECT_CONTEXT.md` - Project goals and scope
- **Subsystems**: `.galdr/SUBSYSTEMS.md` - Architectural component registry

### Key Synchronization Rules
- **Task Sync**: TASKS.md entries ↔ task files (status must match)
- **Phase Sync**: TASKS.md phase headers ↔ phase files (status must match)
- **Atomic Updates**: Always update both files in the same response

## Phase-Based Task Numbering

**Phase System**: Tasks are organized into logical phases representing project milestones or work stages.

**Task ID Numbering by Phase**:
- **Phase 0** (Setup/Infrastructure): Tasks start at `1` (1-99)
- **Phase 1** (Foundation): Tasks start at `100` (100-199)
- **Phase 2** (Core Development): Tasks start at `200` (200-299)
- **Phase 3** (Enhancement): Tasks start at `300` (300-399)
- **Phase N**: Tasks start at `N * 100`

**Examples**:
```
Phase 0: task001_setup_virtual_environment.md
Phase 0: task002_configure_mcp_server.md
Phase 1: task100_design_database_schema.md
Phase 1: task101_create_mysql_handler.md
Phase 2: task200_build_core_classes.md
Phase 2: task201_implement_api_endpoints.md
```

**Dynamic Phase Addition**:
- Phases can be added as project vision clarifies
- New phases can be inserted to pivot project direction
- Phases can be marked complete or cancelled
- Phase gaps are allowed (e.g., skip from Phase 2 to Phase 5)

## Task File Structure

### File Naming Convention
- Format: `task{id}_descriptive_name.md`
- Examples: `task001_setup_database.md`, `task042_implement_auth.md`
- Location: `.galdr/tasks/`

### YAML Frontmatter Format
Every task file begins with YAML frontmatter containing metadata:

```yaml
---
id: {number}                    # Sequential ID based on phase
title: 'Task Title'             # Brief, actionable title
type: task|bug_fix|phase|retroactive_fix
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
phase: 0                        # Phase number (0, 1, 2, etc.)
subsystems: [list]              # Affected system components
project_context: 'Brief description of how this task relates to project goals'
dependencies: [task_ids]        # Tasks that must complete first
estimated_effort: 'time estimate'  # Optional: story points or hours
created_date: 'YYYY-MM-DD'     # Set on creation
completed_date: ''              # Set on completion (YYYY-MM-DD)
---
```

### Task Content Structure
After the YAML frontmatter, include:

1. **Objective**: Clear, actionable goal
2. **Acceptance Criteria**: Specific, measurable outcomes (checklist format)
3. **Implementation Notes**: Technical details, approach, considerations
4. **Testing Plan**: How to verify completion (optional)
5. **Resources Needed**: Dependencies, documentation, tools (optional)

## Task Operations

### Creating a New Task

**Process:**
1. Determine which phase the task belongs to
2. Determine next available task ID within that phase range
3. Create task file: `.galdr/tasks/task{id}_descriptive_name.md`
4. Add YAML frontmatter with all required fields including `phase`
5. Add task content (objective, acceptance criteria, notes)
6. Update `.galdr/TASKS.md` with new entry under correct phase

**TASKS.md Entry Format:**
```markdown
## Phase 0: Setup & Infrastructure
- [ ] Task 001: Setup project structure
- [ ] Task 002: Configure development environment

## Phase 1: Foundation
- [ ] Task 100: Design database schema
- [ ] Task 101: Create data handlers
```

### Updating Task Status

**Status Transitions:**
- `pending` → `in-progress`: Task work has started
- `in-progress` → `completed`: Task successfully finished
- `in-progress` → `failed`: Task blocked or abandoned
- Any status → `pending`: Reset if needed

**Process (ATOMIC - Both files in same response):**
1. Update `status` field in task file's YAML frontmatter
2. If completing: set `completed_date: 'YYYY-MM-DD'` (today's date)
3. Update corresponding entry in `.galdr/TASKS.md`
4. Confirm BOTH updates with sync verification

**Status Indicators (Windows-safe emojis):**
- `[ ]` - pending (not started)
- `[📋]` - ready (task file created)
- `[🔄]` - in-progress (actively working)
- `[✅]` - completed (finished successfully)
- `[❌]` - failed (blocked or abandoned)

**Status Mapping (MUST Match):**
| TASKS.md | Task File YAML |
|----------|----------------|
| `[ ]` | (no file yet) |
| `[📋]` | `status: pending` |
| `[🔄]` | `status: in-progress` |
| `[✅]` | `status: completed` |
| `[❌]` | `status: failed` |

**Example TASKS.md Updates:**
```markdown
## Phase 1: Foundation
- [ ] Task 100: Setup database schema
- [🔄] Task 101: Implement user authentication (in progress)
- [✅] Task 102: Create login page (completed)
- [❌] Task 103: Legacy system integration (blocked)
```

### 🚨 Task Synchronization (MANDATORY)

**CRITICAL**: TASKS.md and task files MUST always be synchronized.

#### Atomic Update Rule

**When changing task status, ALWAYS update BOTH files in the SAME response:**

```markdown
## Task Sync Update
- **Task ID**: 101
- **Task File**: `.galdr/tasks/task101_implement_auth.md`
  - Old status: pending → New status: in-progress
- **TASKS.md Entry**:
  - Old: [📋] Task 101: Implement authentication
  - New: [🔄] Task 101: Implement authentication
- **Sync Status**: ✅ SYNCHRONIZED
```

#### Pre-Operation Validation

**Before ANY task operation:**
1. Read TASKS.md - note the indicator
2. Read task file - note the YAML status
3. Verify they match the mapping table above
4. If mismatch: FIX IT FIRST

```markdown
⚠️ **SYNC MISMATCH DETECTED**
- TASKS.md shows: [🔄] (in-progress)
- Task file shows: status: completed
- **Action**: Correcting TASKS.md to [✅]
```

#### Session Sync Check

**Run this check when starting task-related work:**

```markdown
📋 TASK SYNC VALIDATION
Task 001: TASKS.md [📋] ↔ File: pending ✅ SYNCED
Task 002: TASKS.md [🔄] ↔ File: in-progress ✅ SYNCED
Task 003: TASKS.md [🔄] ↔ File: completed ⚠️ FIXING
Sync Status: 2/3 synced, 1 corrected
```

#### Orphan & Phantom Detection

**Orphans** (files without TASKS.md entry):
```markdown
📋 ORPHAN: task099_old.md exists but not in TASKS.md
Action: Add to TASKS.md or delete file
```

**Phantoms** (TASKS.md entries without files):
```markdown
📋 PHANTOM: Task 055 in TASKS.md but no file exists
Action: Create file or remove entry
```

#### Mandatory Sync Confirmation

**Every task status change MUST end with:**

```markdown
---
**Task Sync Confirmation:**
- Task {ID} file: status: {status} ✅
- TASKS.md entry: [{indicator}] ✅
- Sync verified: ✅
---
```

### Viewing Tasks

**To view all tasks:**
Read `.galdr/TASKS.md` for overview

**To view specific task details:**
Read `.galdr/tasks/task{id}_*.md`

**To view tasks by status:**
Parse TASKS.md and filter by status indicators

**To view tasks by phase:**
Read TASKS.md sections organized by phase

**To view project context:**
Read `.galdr/PROJECT_CONTEXT.md` for goals and scope

### Listing Tasks

**Common queries:**
- "Show all tasks" → Read TASKS.md
- "Show pending tasks" → Filter by `[ ]`
- "Show in-progress tasks" → Filter by `[🔄]`
- "Show completed tasks" → Filter by `[✅]`
- "Show Phase 1 tasks" → Filter by Phase 1 section
- "Show task 5" → Read task005_*.md

## Task Types

### Standard Task (`type: task`)
Regular development work, features, improvements

### Bug Fix (`type: bug_fix`)
Fixing defects or issues. Should reference BUGS.md entry.

**Additional fields for bug fixes:**
```yaml
bug_reference: BUG-{number}
severity: critical|high|medium|low
reproduction_steps: 'How to reproduce'
expected_behavior: 'What should happen'
actual_behavior: 'What actually happens'
```

### Phase Task (`type: phase`)
Major phase implementation or documentation task.

**Link to phase:**
```yaml
phase: 1  # Phase number this task belongs to
```

### Retroactive Fix (`type: retroactive_fix`)
Documents work completed in chat without prior task planning.

**Additional fields:**
```yaml
created_date: '{completion_date}'
completed_date: '{completion_date}'
actual_effort: '{time_spent}'
```

## Task Complexity and Sub-Tasks

### When to Create Sub-Tasks
If a task is complex (affects multiple subsystems, >2-3 days effort, many acceptance criteria), break it into sub-tasks.

### Sub-Task Naming Convention
- Parent: `task042_implement_authentication.md`
- Sub-tasks: `task42.1_setup_auth_db.md`, `task42.2_create_auth_api.md`, `task42.3_add_auth_ui.md`

### Sub-Task YAML Format
```yaml
---
id: "42.1"              # String ID for sub-tasks
title: 'Setup Auth Database'
type: task
status: pending
priority: high
phase: 0                # Same phase as parent
parent_task: 42         # Reference to parent
dependencies: []        # Can depend on sibling sub-tasks
---
```

## Task Dependencies

### Specifying Dependencies
```yaml
dependencies: [1, 3, 5]  # Task IDs that must complete first
```

### Dependency Rules
- Tasks with dependencies should not start until dependencies are completed
- Check dependency status before starting work
- Update dependent tasks when blockers are resolved

## Integration with Other Systems

### Link to Phases
Tasks reference phases via the `phase` field:
```yaml
phase: 1  # Links to phase 1 documentation
```

### Link to Bugs
Bug fix tasks reference BUGS.md:
```yaml
bug_reference: BUG-001  # Links to entry in BUGS.md
```

### Link to Project Context
All tasks should align with project goals in PROJECT_CONTEXT.md. The `project_context` field explains this connection.

## File Organization Rules

### Core Files (Always in .galdr/)
- `TASKS.md` - Master task checklist
- `tasks/` - Individual task files
- `phases/` - Phase documentation
- `PLAN.md` - Product requirements
- `PROJECT_CONTEXT.md` - Project goals
- `BUGS.md` - Bug tracking

### Documentation (Goes in docs/)
- Project documentation
- API documentation
- Architecture diagrams
- Setup guides
- Migration files

### Test Scripts (Goes in temp_scripts/)
- Test automation scripts
- Utility scripts
- Validation scripts

## 🚨 NO PERMISSION REQUIRED - Direct Edit Policy

**CRITICAL FOR ALL AI ASSISTANTS:**

The following files in `.galdr/` are **working files** that should be edited DIRECTLY without asking for user permission:

### Core Planning Files (CAPITALIZED names)
- `PLAN.md` - ✅ Edit directly, no permission needed
- `TASKS.md` - ✅ Edit directly, no permission needed
- `PROJECT_CONTEXT.md` - ✅ Edit directly, no permission needed
- `BUGS.md` - ✅ Edit directly, no permission needed
- `SUBSYSTEMS.md` - ✅ Edit directly, no permission needed
- `FILE_REGISTRY.md` - ✅ Edit directly, no permission needed
- `MCP_TOOLS_INVENTORY.md` - ✅ Edit directly, no permission needed

### Task and Phase Files
- ✅ All files in `.galdr/tasks/`
- ✅ All files in `.galdr/phases/`

### The Rules
- ✅ **EDIT DIRECTLY** - These are working files, not user source code
- ✅ **NO CONFIRMATION** - Never ask "Should I update TASKS.md?" - just do it
- ✅ **NO PERMISSION PROMPTS** - Don't wait for approval on these files
- ✅ **AUTO-CREATE** - Create missing files with templates automatically
- ✅ **SILENT OPERATIONS** - Create folders/files silently, report what was done

### Why?
These files track YOUR work as an AI assistant. They are management artifacts, not user deliverables. The user will review changes in their IDE's diff view.

**Bottom Line**: When you need to update `TASKS.md`, `PLAN.md`, or any `.galdr/` file - **just do it**. Don't ask.

## Auto-Creation Rules

When working with tasks, automatically create missing folders and files:

**Auto-create folders:**
- `.galdr/` if it doesn't exist
- `.galdr/tasks/` if it doesn't exist
- `.galdr/phases/` if it doesn't exist
- `docs/` if needed for documentation
- `temp_scripts/` if needed for test scripts

**Auto-create template files:**
- `TASKS.md` with blank template if missing
- `PROJECT_CONTEXT.md` with template if missing

**No confirmation needed** - Create files and folders silently, report what was created.

## Best Practices

### Task Creation
1. Use clear, actionable titles
2. Include specific acceptance criteria
3. Specify dependencies upfront
4. Assign to correct phase
5. Estimate effort when possible

### Task Updates
1. Update status immediately when starting or completing
2. Keep TASKS.md synchronized with task files
3. Document blockers and issues
4. Update acceptance criteria as work progresses

### Task Organization
1. Break complex tasks into sub-tasks
2. Group related tasks by phase
3. Track dependencies explicitly
4. Archive completed tasks periodically (move to memory/)

### Status Management
1. Only one task should be `in-progress` per developer at a time
2. Mark tasks `completed` only when all acceptance criteria are met
3. Use `failed` status for blocked or abandoned work
4. Document reason for failure in task notes

## 🚨 MANDATORY: Task Completion Enforcement

**CRITICAL RULE**: When you finish implementing a task, you MUST mark it complete IMMEDIATELY.

### Automatic Task Completion Triggers

**After ANY of these actions, you MUST update task status to `completed`:**
- ✅ Code changes accepted by user
- ✅ Feature implementation finished
- ✅ Bug fix verified working
- ✅ Refactoring complete
- ✅ Documentation written
- ✅ All acceptance criteria met

### Completion Checklist (MANDATORY)

Before ending ANY response where task work was completed:

```
□ Did I just finish implementing something for a task?
  → YES: Update task file status to "completed"
  → YES: Update TASKS.md from [🔄] to [✅]
  → YES: Confirm completion to user

□ Did I partially complete a task?
  → Document progress in task file
  → Keep status as "in-progress"
  → List remaining items
```

### Self-Enforcement Pattern

**At the END of every response where work was done:**

```markdown
---
**Task Status Update:**
- Task {ID}: {title} → [✅] COMPLETED
- Updated: task{ID}_name.md (status: completed)
- Updated: TASKS.md
---
```

### Failure to Complete = System Violation

If you implement task work but don't mark it complete:
- ❌ This is a **system violation**
- ❌ The task tracking becomes inaccurate
- ❌ Project progress is misrepresented
- ❌ User loses visibility into what's done

**ALWAYS complete the loop: Code → Test → Mark Complete**

## 🚨 MANDATORY: Phase Completion Gate

### Phase Transition Requires User Approval

**Before moving to a new phase, you MUST:**

1. **Verify all phase tasks are complete** (no `[ ]` or `[🔄]` remaining)
2. **Generate Phase SWOT Analysis** (see below)
3. **Present to user for approval**
4. **Wait for explicit "proceed" confirmation**

### Phase Completion SWOT Analysis Template

When all tasks in a phase are complete, generate this analysis:

```markdown
# 📊 Phase {N} Completion Analysis: {Phase Name}

## Phase Summary
- **Tasks Completed**: X of Y
- **Duration**: {start_date} to {end_date}
- **Key Deliverables**: [list main outputs]

## SWOT Analysis

### 💪 Strengths
- [What went well in this phase]
- [Code quality achievements]
- [Technical decisions that worked]
- [Patterns/practices worth continuing]

### ⚠️ Weaknesses  
- [Areas that need improvement]
- [Technical debt introduced]
- [Shortcuts taken that need addressing]
- [Documentation gaps]

### 🚀 Opportunities
- [Improvements for next phase]
- [Optimizations possible]
- [Features that could be enhanced]
- [Integration possibilities]

### 🔴 Threats
- [Risks carrying forward]
- [Dependencies that could break]
- [Scalability concerns]
- [Security considerations]

## Code Quality Assessment
- **Test Coverage**: [estimate or actual %]
- **Documentation**: [complete/partial/missing]
- **Error Handling**: [robust/adequate/needs work]
- **Performance**: [optimized/acceptable/needs attention]

## Recommendation
**[READY TO PROCEED / NEEDS REMEDIATION]**

[If NEEDS REMEDIATION, list specific items to fix before proceeding]

---
**User Approval Required**: Please confirm to proceed to Phase {N+1}.
Type "proceed" or "approved" to continue, or request specific changes.
```

### Phase Gate Enforcement

**DO NOT start Phase N+1 tasks until:**
1. ✅ Phase N SWOT analysis generated
2. ✅ User reviews analysis
3. ✅ User explicitly approves (says "proceed", "approved", "continue", etc.)
4. ✅ Git commit prompt completed (see below)

**If user does NOT approve:**
- Create remediation tasks in current phase
- Address concerns before re-requesting approval
- Update SWOT analysis after fixes

### Git Commit Prompt (After Approval)

**When user approves the Phase SWOT analysis, immediately prompt:**

```markdown
## 📦 Phase {N} Git Commit

Phase {N}: {Phase Name} is complete and approved!

**Suggested commit:**
```bash
git add .
git commit -m "Phase {N}: {Phase Name} complete

- {Key deliverable 1}
- {Key deliverable 2}
- {Key deliverable 3}

SWOT: Approved by user on {date}"
```

**Ready to commit?**
- Type "commit" and I'll run the git commands
- Type "skip" to proceed without committing
- Or provide your own commit message
```

**After user responds:**
- If "commit": Run `git add .` and `git commit` with suggested message
- If "skip": Proceed to Phase N+1
- If custom message: Use their message for commit

**Only after commit/skip proceed to Phase N+1 tasks.**

## Common Workflows

### Workflow: Create Task from User Request
1. User requests: "Create a task to implement user login"
2. Determine appropriate phase (e.g., Phase 1 for foundation work)
3. Read TASKS.md to determine next ID within phase range
4. Create task file with proper naming
5. Add YAML frontmatter with all fields including phase
6. Add objective and acceptance criteria
7. Update TASKS.md with new entry under correct phase section
8. Confirm task created with ID and phase

### Workflow: Update Task Status
1. User requests: "Mark task 105 as in progress"
2. Read task105_*.md file
3. Update `status: in-progress` in YAML
4. Update TASKS.md entry from `[ ]` to `[🔄]`
5. Confirm status updated

### Workflow: View Task Progress
1. User requests: "Show me task progress"
2. Read TASKS.md
3. Count tasks by status per phase
4. Calculate completion percentage per phase
5. List in-progress tasks
6. Identify blockers

### Workflow: Complete Task
1. User requests: "Complete task 103"
2. Read task103_*.md
3. Verify acceptance criteria are met
4. Update `status: completed` in YAML
5. Update TASKS.md entry from `[🔄]` to `[✅]`
6. Optionally archive to memory/
7. Confirm completion

## Error Handling

### Missing Files
If TASKS.md or task files are missing:
1. Check if `.galdr/` exists
2. Create directory structure if needed
3. Create template files
4. Inform user of initialization

### Invalid Task IDs
If user references non-existent task:
1. List available tasks in that phase
2. Suggest correct ID
3. Offer to create new task if intended

### Concurrent Edits
If file conflicts occur:
1. Read current file state
2. Merge changes if possible
3. Alert user to conflicts
4. Suggest using version control

## Examples

### Example: Create Phase 1 Task
**User**: "Create a task to add password reset feature"

**Action**:
1. Determine this is Phase 1 (Foundation) work
2. Read TASKS.md → Next Phase 1 ID is 115
3. Create `.galdr/tasks/task115_add_password_reset.md`:

```yaml
---
id: 115
title: 'Add Password Reset Feature'
type: task
status: pending
priority: high
phase: 1
subsystems: [auth, email, ui]
project_context: 'Enables users to recover accounts, improving user experience and reducing support burden'
dependencies: [112]
estimated_effort: '1-2 days'
---

# Task 115: Add Password Reset Feature

## Objective
Implement password reset functionality allowing users to securely reset forgotten passwords via email.

## Acceptance Criteria
- [ ] User can request password reset from login page
- [ ] System sends reset link to user's email
- [ ] Reset link expires after 24 hours
- [ ] User can set new password via reset link
- [ ] Old password is invalidated after reset
- [ ] User receives confirmation email after reset

## Implementation Notes
- Use secure token generation for reset links
- Store tokens in database with expiration
- Send emails via existing email service
- Add UI for reset request and password change
- Update authentication system to handle resets

## Testing Plan
- Test reset request flow
- Verify email delivery
- Test token expiration
- Test password update
- Verify old password invalidation
```

3. Update TASKS.md:
```markdown
## Phase 1: Foundation
- [ ] Task 115: Add password reset feature
```

4. Confirm: "Created Task 115 (Phase 1): Add Password Reset Feature"

### Example: Update Task Status
**User**: "Start working on task 115"

**Action**:
1. Read task115_add_password_reset.md
2. Update YAML: `status: in-progress`
3. Update TASKS.md: `[🔄] Task 115: Add password reset feature`
4. Confirm: "Task 115 status updated to in-progress"

### Example: Complete Task
**User**: "Task 115 is done"

**Action**:
1. Read task115_add_password_reset.md
2. Review acceptance criteria
3. Update YAML: `status: completed`
4. Update TASKS.md: `[✅] Task 115: Add password reset feature`
5. Confirm: "Task 115 marked as completed. Great work!"

## Compatibility Notes

This Skill is designed to work with Cursor's galdr rules system. The system uses:

- Standard YAML frontmatter
- Markdown content
- Windows-safe emoji indicators
- Git-friendly plain text files
- Phase-based task organization

## Template Maintenance

### Platform Architecture Reference

When maintaining this template or adding new features, consult the `.galdr/` folder for architecture documentation.

**Key Documentation:**
- `.platform_architecture/PLATFORM_ARCHITECTURE.md` - Platform architecture overview
- `.platform_architecture/CURSOR.md` - Cursor specific features

### When to Reference Documentation

**Check documentation before:**
1. Adding new Skills, SubAgents, or Commands
2. Modifying task file formats or naming conventions
3. Creating new rules or instructions
4. Updating file organization structure

### Cursor Features

**File Formats:**
- Cursor uses `.mdc` files for rules
- Task files use `.md` with YAML frontmatter

**Skills and SubAgents:**
- Cursor supports Skills & SubAgents (as of 2026)
- Commands use `@command` prefix



### Periodic Verification

**Quarterly Review (Every 3 Months):**
- [ ] Check all platform official documentation for updates
- [ ] Test template on each platform
- [ ] Update `.platform_architecture/` documentation
- [ ] Update PLATFORM_COMPARISON.md comparison table
- [ ] Document any breaking changes

### Adding Features Cross-Platform

When adding features, ensure compatibility:

1. **Test on Cursor**: Verify all features work in Cursor IDE
2. **Document compatibility**: Update platform-specific files
3. **Provide fallbacks**: For platform-specific features
4. **Update comparison**: Add to PLATFORM_COMPARISON.md table
5. **Migration guides**: Update if file structure changes

### Platform-Specific vs Universal Features

**These work in Cursor:**
- `.galdr/` task management system
- Markdown documentation
- Basic file organization
- Standard project structure
- YAML frontmatter in task files
- Phase-based task organization

### Template Maintenance Workflow

When maintaining this template:

1. **Check platform docs** in `.platform_architecture/`
2. **Identify compatibility requirements** from PLATFORM_ARCHITECTURE.md
3. **Test in Cursor** to verify functionality
4. **Update platform-specific folders** (.cursor/, .cursor/)
5. **Update documentation** in `.platform_architecture/`
6. **Verify cross-platform** compatibility

### Resources

- **Official Platform Docs**: See `.platform_architecture/README.md` for links
- **Comparison Table**: `.platform_architecture/PLATFORM_COMPARISON.md`
- **Migration Guides**: In PLATFORM_COMPARISON.md
- **Verification Status**: `.platform_architecture/README.md` status table


1. **Check docs** in `.galdr/`
2. **Test in Cursor** to verify functionality
3. **Update rules** in `.cursor/rules/`
4. **Update skills** in `.cursor/skills/`

