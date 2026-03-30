---
name: g-phase-add
description: Add a new project phase atomically — TASKS.md header and phase definition file created together.
---
# galdr-phase-add

## When to Use
Adding a new development phase. @g-phase-add or "add phase N".

## Steps

1. **Determine phase number**:
   - Check existing phase headers in TASKS.md
   - Next phase = highest existing + 1 (gaps allowed)
   - Task ID range = N×100 to N×100+99 (Phase 0: 1-99)

2. **Pre-sync check**:
   - Verify all existing phases have both TASKS.md header AND phase file
   - Fix any mismatches before proceeding

3. **Create phase file** at `.galdr/phases/phaseN_kebab-name.md`:
```yaml
---
phase: N
name: 'Phase Name'
status: planning
subsystems: [subsystem1, subsystem2]
task_range: 'N00-N99'
prerequisites: [0, 1]
started_date: ''
completed_date: ''
pivoted_from: null
pivot_reason: ''
---

# Phase N: Phase Name

## Overview
[Brief description of phase goals and scope]

## Objectives
- [Objective 1]
- [Objective 2]

## Deliverables
- [ ] [Deliverable 1]

## Acceptance Criteria
- [ ] [Criterion 1]
```

4. **Add to TASKS.md** (atomic — same response):
```markdown
## Phase N: Phase Name [📋]

| Status | ID | Task |
|--------|----|----|
| [ ] | N00 | [First task placeholder] |
```

5. **Update CLAUDE.md** if it exists:
```markdown
## Current Phase
- **Phase N**: Phase Name
- **Status**: In Progress
- **Objectives**: [from phase file]
```

6. **Print sync confirmation**:
```
Phase Sync Confirmation:
- TASKS.md header: Phase N ✅
- Phase file: phases/phaseN_name.md ✅
- Sync verified: ✅
```
