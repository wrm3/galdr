---
name: g-task-new
description: Create a new task file and TASKS.md entry atomically, step by step.
---
# galdr-task-new

## When to Use
Creating a new task. Triggered by @g-task-new or "create task NNN".

## Steps

1. **Determine task ID**
   - Check TASKS.md for the current phase's highest ID
   - Next ID = highest + 1 within the phase range
   - Phase 0: 1-99 | Phase 1: 100-199 | Phase N: N×100 to N×100+99

2. **Assess complexity** (score 1-10+, see galdr-workflow-manager)
   - Score ≥7: STOP — expand to sub-tasks first using `@g-workflow`

3. **Create task file** at `.galdr/tasks/taskNNN_descriptive_name.md`:
```yaml
---
id: NNN
title: 'Task Title'
type: feature | bug_fix | refactor | documentation
status: pending
priority: critical | high | medium | low
phase: N
subsystems: [component1, component2]
project_context: 'Why this task matters to project goals'
dependencies: []
blast_radius: low | medium | high
requires_verification: false
ai_safe: true
spec_version: "1.0"
execution_cost: low
created_date: 'YYYY-MM-DD'
completed_date: ''
# Cross-project fields (omit if task is purely internal):
# task_source: other-project-id        # project that originated this task
# source_task_id: 187                  # task ID in the source project
# delegation_type: broadcast           # broadcast | request | peer_sync
# cascade_depth_original: 2
# cascade_depth_remaining: 1
# cascade_chain: [source-project]
# cascade_forwarded: false
# requires_parent_action: false
# parent_action_status: null
# parent_action_project: null
# peer_sync_partner: null
# peer_sync_status: null
---

# Task NNN: [Title]

## Objective
[Clear, actionable goal — what is done when this is complete]

## Acceptance Criteria
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Verification requirement]

## Implementation Notes
[Technical approach, constraints, dependencies]

## Verification
- [ ] Code compiles / no lint errors
- [ ] Acceptance criteria tested
- [ ] Documentation updated if needed
```

4. **Add to TASKS.md** (atomic — same response):
   - Find the correct phase section
   - Add: `| [📋] | NNN | Task Title — brief acceptance summary |`

5. **Regenerate dependency graph** (if task has dependencies):
   - If `dependencies: []` is non-empty, regenerate `.galdr/DEPENDENCY_GRAPH.md`
   - Follow the `g-dependency-graph` skill steps
   - Read all task files, build adjacency list, compute critical path, write graph

6. **Confirm**:
```
Task Sync Confirmation:
- Task NNN file: .galdr/tasks/taskNNN_*.md ✅
- TASKS.md entry: [📋] ✅
- Dependency graph: {updated ✅ | no dependencies, skipped}
- Sync verified: ✅
```
