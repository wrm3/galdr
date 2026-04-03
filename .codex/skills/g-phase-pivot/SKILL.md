---
name: g-phase-pivot
description: Pivot project direction — pause old phase, create new phase with pivot context documented.
---
# galdr-phase-pivot

## When to Use
Project direction changes. @g-phase-pivot or "pivot to new direction".

## Steps

1. **Identify the pivoting-from phase** (current active phase):
   - Which phase is currently `status: in_progress`?
   - What tasks are incomplete in that phase?

2. **Pause old phase**:
   - Update `phases/phaseN_old.md` YAML: `status: paused`
   - Update TASKS.md header: `## Phase N: Name [⏸️]`

3. **Document incomplete tasks**:
   - List all `[🔄]` and `[📋]` tasks from old phase
   - For any `[🔄]` tasks: set to `status: paused` in task files

4. **Create new phase file** with pivot context:
```yaml
---
phase: M
name: 'New Direction Name'
status: in_progress
subsystems: [affected_subsystems]
task_range: 'M00-M99'
prerequisites: []
started_date: 'YYYY-MM-DD'
completed_date: ''
pivoted_from: N
pivot_reason: 'Why pivot occurred — user requirements changed, etc.'
---
```

5. **Add new phase header to TASKS.md**:
```markdown
## Phase M: New Direction [🔄]
> Pivoted from Phase N: [reason]
```

6. **Update CLAUDE.md** if it exists:
```markdown
## Current Phase
- **Phase M**: New Direction
- **Status**: In Progress
- **Pivoted From**: Phase N — [reason]
- **New Objectives**: [from phase file]
```

7. **Print pivot summary**:
```
📊 Pivot Summary:
- Phase N [⏸️] paused — N tasks incomplete
- Phase M [🔄] created — pivot_reason: [reason]
- CLAUDE.md updated
```
