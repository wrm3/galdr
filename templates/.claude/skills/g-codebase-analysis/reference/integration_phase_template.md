# Phase {N}: {Project} Integration & Verification

## Phase File Template

```yaml
---
phase: {N}
name: '{Project Name} Full Integration & Verification'
status: planning
subsystems: [{list_affected_subsystems}]
task_range: '{N*100}-{N*100+99}'
prerequisites: [{prior_phase_numbers}]
started_date: ''
completed_date: ''
pivoted_from: null
pivot_reason: ''
---
```

## Phase Document Template

```markdown
# Phase {N}: {Project Name} Full Integration & Verification

## Overview
Systematic verification and integration of ALL {Project} components into GaldrWorks.
Every subsystem is mapped, verified, and either integrated, adapted, or documented as 
intentionally skipped.

## Objectives
- {Objective from comparison HIGH priority gaps}
- {Objective from comparison MEDIUM priority gaps}
- Verify all existing integration points work correctly
- Surface all settings and configs in GaldrWorks UI
- Complete documentation of integration decisions

## Deliverables
- [ ] {Deliverable for each HIGH gap}
- [ ] Integration test suite
- [ ] Feature parity checklist

## Acceptance Criteria
- [ ] {Criterion for each HIGH gap}
- [ ] No capability lost in integration
- [ ] All settings configurable

## Notes
- Architecture Map: docs/{architecture_doc}
- Comparison Doc: docs/{comparison_doc}
```

## Task Categories

### Category 1: Integration Verification
Tasks that verify existing integrations work correctly.
```
- [ ] Task {ID}: {Component} verification - test {specific_test} through {integration_path}
```

### Category 2: Missing Capability Implementation  
Tasks for HIGH and MEDIUM priority gaps from comparison.
```
- [ ] Task {ID}: {Component} implementation - {what_to_build} [{PRIORITY}]
```

### Category 3: Settings & Configuration
Tasks for surfacing all external configs in our system.
```
- [ ] Task {ID}: {Setting area} configuration - add {settings} to {location}
```

### Category 4: Protocol & Communication
Tasks for API/messaging integration.
```
- [ ] Task {ID}: {Protocol} integration - {what_to_connect}
```

### Category 5: Security & Auth
Tasks for security feature parity.
```
- [ ] Task {ID}: {Security feature} - {what_to_implement}
```

### Category 6: UI & Management
Tasks for management interfaces.
```
- [ ] Task {ID}: {UI feature} page - {what_it_shows}
```

### Category 7: Testing & Documentation
Always include these closing tasks:
```
- [ ] Task {ID}: Integration test suite - automated tests verifying all components
- [ ] Task {ID}: Feature parity checklist - final verification nothing is lost
- [ ] Task {ID}: Phase completion documentation - decisions, notes, what was skipped and why
```

## Task ID Assignment

- Phase {N} uses IDs {N*100} through {N*100+99}
- Start with verification tasks (lowest IDs)
- Then implementation tasks
- Then config/settings tasks
- End with testing/documentation tasks (highest IDs)

## TASKS.md Entry Format

```markdown
## Phase {N}: {Project} Full Integration & Verification [ ]

*Systematic verification and integration of ALL {Project} components into GaldrWorks.*
*Reference: docs/{architecture_doc}*
*Reference: docs/{comparison_doc}*

### {Category Name}
- [ ] Task {ID}: {Description} [{PRIORITY}]
```
