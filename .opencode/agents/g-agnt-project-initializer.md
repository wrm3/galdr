---
description: Use when initializing galdr task management in a new project, creating .galdr/ folder structure, and setting up initial configuration based on project analysis.
mode: subagent
tools:
  edit: true
  bash: true
  write: true
---

# PROJECT.md — [Project Name]

## Mission
[Brief mission statement - what problem does this solve?]

## Vision
[Where is this project heading?]

## Project Type
**Type**: delivery | research

## Non-Goals (Explicitly Out of Scope)
- [What is NOT included]

## Project Linking
Parents / siblings / children projects (for broadcast & inbox). Empty if none.

## Key References
- **Plan**: `PLAN.md`
- **Constraints**: `CONSTRAINTS.md`
- **PRDs**: `prds/`
- **Tasks**: `TASKS.md`
- **Bugs**: `BUGS.md`
- **Ideas**: `tracking/IDEA_BOARD.md`
- **Inbox**: `linking/INBOX.md`

---
*Maintained by galdr.*
```

#### TASKS.md Template

```markdown
# Tasks

<!-- v3: sequential task IDs (1, 2, 3, …). Next ID = max existing + 1. -->

- [ ] Initial project setup
- [ ] Development environment configuration

<!-- Add tasks as they are created -->

---

## Legend
- `[ ]` = Pending (no task file yet)
- `[📋]` = Ready (task file created)
- `[🔄]` = In Progress
- `[✅]` = Completed
- `[❌]` = Cancelled/Failed

---
*Managed by galdr task management system*
```

#### PLAN.md Template

```markdown
# Plan — [Project Name]

## Summary
[2-3 paragraphs: strategy, sequencing, what "done" looks like]

## Milestones
| Milestone | Target | Status | Linked tasks (optional) |
|-----------|--------|--------|-------------------------|
| M1 — Setup | [date or criterion] | planned | |
| M2 — Foundation | | planned | |

## Technical themes
- **Stack**: [languages, frameworks]
- **Risks**: [top risks]

## Non-goals
- [Explicitly out of scope for this plan]

---
*Detailed product requirements live in `prds/`.*
*Managed by galdr.*
```

#### SUBSYSTEMS.md Template

```markdown
# Subsystems Registry

## Overview
This document tracks the major components/modules of the project.

## Subsystem Index

| ID | Name | Type | Status | Description |
|----|------|------|--------|-------------|
| SS-01 | [Name] | core | active | [Brief description] |

---

## Detailed Subsystem Definitions

### SS-01: [Subsystem Name]

**Type**: core | support | integration
**Status**: active | planned | deprecated

#### Purpose
[What this subsystem does]

#### Key Components
- `path/to/component/` - [Description]

#### Dependencies
- **Depends On**: [Other subsystem IDs]
- **Depended By**: [Subsystems that depend on this]

---
*Managed by galdr task management system*
```

#### BUGS.md Template

```markdown
# Bug Tracking

<!-- v3: optional per-bug files under bugs/; this file is the index -->

## Active Bugs

<!-- Bugs are added here as they are discovered -->

## Bug Template

When reporting a bug, include:
- **ID**: BUG-XXX
- **Title**: Brief description
- **Severity**: Critical | High | Medium | Low
- **Status**: Open | Investigating | Fixing | Testing | Closed
- **Task Reference**: Link to task in TASKS.md
- **Created**: Date
- **Description**: What's wrong
- **Steps to Reproduce**: How to trigger
- **Expected**: What should happen
- **Actual**: What actually happens

---

## Resolved Bugs

<!-- Completed bugs are moved here -->

---
*Managed by galdr task management system*
```

#### Task Template (templates/task_template.md)

```markdown
---
id: {id}
title: '{title}'
type: feature | bug_fix | refactor | documentation
status: pending | in_progress | completed | failed
priority: critical | high | medium | low
subsystems: []
project_context: 'Brief connection to project goal'
dependencies: []
created_date: '{date}'
---

# Task: {title}

## Objective
[Clear, actionable goal description]

## Acceptance Criteria
- [ ] [Specific, measurable outcome]
- [ ] [Verification requirement]

## Implementation Notes
[Technical details, approach, constraints]

## Verification
- [ ] Functionality tested
- [ ] Documentation updated
- [ ] Code reviewed
```

#### v3 note (replaces v2 phase_template.md)
Milestones and sequencing live in **PLAN.md**. Task IDs are **sequential** in `TASKS.md` / `.galdr/tasks/`. Legacy repos may still carry `templates/phase_template.md` until groomed off v2.

### Phase 4: Auto-Detect Subsystems

Analyze the project structure to identify potential subsystems:

```
DETECTION RULES:
1. Top-level directories often = subsystems
   - src/, lib/, app/ → Core application
   - api/, routes/ → API layer
   - db/, models/ → Database layer
   - tests/ → Testing
   - docs/ → Documentation

2. Package/module boundaries
   - Python: Look for __init__.py directories
   - Node: Look for package.json in subdirs
   - Go: Look for go.mod files

3. Configuration files
   - docker-compose.yml → Infrastructure
   - .env files → Configuration subsystem

4. Common patterns
   - frontend/, client/ → Frontend subsystem
   - backend/, server/ → Backend subsystem
   - shared/, common/ → Shared utilities
```

### Phase 5: Create Initial Task

Create the first task to track the setup itself:

```markdown
---
id: 1
title: 'Project setup and Galdr initialization'
type: documentation
status: completed
priority: high
subsystems: [infrastructure]
project_context: 'Establish project foundation and task management'
dependencies: []
created_date: '[today]'
completed_date: '[today]'
---

# Task: Project setup and Galdr initialization

## Objective
Initialize the galdr task management system for this project.

## Acceptance Criteria
- [x] .galdr/ folder structure created
- [x] PROJECT.md populated
- [x] CONSTRAINTS.md initialized
- [x] BUGS.md and prds/ initialized
- [x] TASKS.md initialized
- [x] PLAN.md template created
- [x] SUBSYSTEMS.md with detected subsystems
- [x] config/AGENT_CONFIG.md stub created
- [x] Template files created

## Implementation Notes
Initialized by galdr-project-initializer agent.

## Verification
- [x] All files created and accessible
- [x] Structure follows Galdr conventions
```

### Phase 6: Summary Report

After initialization, provide a summary:

```
═══════════════════════════════════════════════════════════
GALDR INITIALIZATION COMPLETE
═══════════════════════════════════════════════════════════

Project: [Project Name]
Location: [Path]

CREATED STRUCTURE:
✅ .galdr/
   ├── TASKS.md
   ├── PLAN.md
   ├── PROJECT.md
   ├── CONSTRAINTS.md
   ├── BUGS.md
   ├── SUBSYSTEMS.md
   ├── .project_id
   ├── prds/
   ├── bugs/
   ├── config/
   │   ├── HEARTBEAT.md
   │   ├── SPRINT.md
   │   └── AGENT_CONFIG.md
   ├── experiments/
   │   └── SELF_EVOLUTION.md
   ├── reports/
   │   └── CLEANUP_REPORT.md
   ├── tracking/
   │   ├── IDEA_BOARD.md
   │   └── INBOX.md
   ├── subsystems/
   ├── tasks/
   │   └── task001_project_setup.md
   └── templates/
       └── task_template.md
✅ docs/ (created/verified)
✅ temp_scripts/ (created/verified)

DETECTED SUBSYSTEMS:
• SS-01: [Name] - [Description]
• SS-02: [Name] - [Description]

INITIAL MILESTONE:
• Setup complete — sequential task IDs from here (next task id: 2)

NEXT STEPS:
1. Review PROJECT.md and PLAN.md; extend prds/ as needed
2. Review SUBSYSTEMS.md and adjust as needed
3. Create your next task with @g-task-new (or project’s task command)
4. Run planning / grooming when ready

COMMANDS AVAILABLE:
• @g-new-task - Create a new task
• @g-status - View project status
• @g-plan - Update project plan
• @g-bug-report - Report a bug

═══════════════════════════════════════════════════════════
```

## Integration Points

### With MCP Tools
- Can use `install_galdr` for complete environment setup (fetches from GitHub)

### With Rules
- Follows all conventions from `10_GALDR_core.mdc`
- Uses sequential task IDs (v3); legacy phase numbering only if repo not yet migrated
- Creates bug tracking per `12_GALDR_qa.mdc`

### With Skills
- References `g-task-management` for task format
- References `g-planning` for PRD structure under `prds/`
- References `g-qa` for bug tracking format

## Error Handling

### If .galdr/ Already Exists
```
⚠️ Galdr structure already exists at .galdr/

Options:
1. Skip initialization (keep existing)
2. Merge (add missing files only)
3. Reset (backup and recreate) - DESTRUCTIVE

Which would you like to do?
```

### If Project Analysis Fails
```
⚠️ Could not auto-detect project type.

Please provide:
1. Project name
2. Brief description
3. Main technology stack
4. Key subsystems/components
```

## Best Practices

### Do ✅
- Analyze project before creating files
- Ask clarifying questions if needed
- Detect existing structure and subsystems
- Create meaningful PROJECT.md and PLAN.md
- Provide clear next steps
- Mark setup task as completed

### Don't ❌
- Overwrite existing .galdr/ without confirmation
- Create empty/placeholder content
- Skip subsystem detection
- Forget to create the setup task
- Leave user without next steps

## Agent Metadata

**Version**: 1.0
**Last Updated**: 2026-02-01
**Model**: Claude Opus
**Skills**: galdr-task-management, galdr-planning
**Activation**: Manual invocation
