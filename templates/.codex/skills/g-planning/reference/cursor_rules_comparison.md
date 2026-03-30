# Cursor Rules and Skills Integration - Planning

## Overview

This document describes how the galdr planning system integrates with Cursor's rules and skills architecture for PRD creation and phase management.

## Cursor Features Used

### Rules (`.cursor/rules/`)
- **Location**: `.cursor/rules/galdr/rules/plans.mdc`
- **Activation**: Always active for planning operations

### Skills (`.cursor/skills/`)
- **Location**: `.cursor/skills/g-planning/SKILL.md`
- **Activation**: Mentions of "plan", "PRD", "requirements", "phases"

### Commands (`.cursor/commands/`)
- **Command**: `@g-plan`
- **Purpose**: Guided PRD creation

## File Format Standards

### PLAN.md Structure
```markdown
# PRD: Project Name

## 1. Product overview
### 1.1 Document title and version
### 1.2 Product summary

## 2. Goals
### 2.1 Business goals
### 2.2 User goals
### 2.3 Non-goals

## 3. User personas
## 4. Phases
## 5. User experience
## 6. Narrative
## 7. Success metrics
## 8. Technical considerations
## 9. Milestones & sequencing
## 10. User stories
```

### Phase Document
```markdown
# Phase N: Phase Name

## Overview
## Task ID Range
## Objectives
## Deliverables
## Technical Considerations
## Acceptance Criteria
## Related Tasks
```

## Workflow Integration

### Creating a PRD
1. User: "Create a PRD for user authentication"
2. Skill activates and asks scope validation questions
3. Creates PLAN.md with 10 sections
4. Creates phase documents

### Using Commands
1. User: `@g-plan`
2. Command guides PRD creation process
3. Creates structured documentation

## Feature Matrix

| Feature | Supported | Notes |
|---------|-----------|-------|
| PRD Template (10 sections) | ✅ | Standard format |
| Phase Documents | ✅ | In phases/ folder |
| Scope Validation (5 Q) | ✅ | Prevents over-engineering |
| Planning Questionnaire (27 Q) | ✅ | Comprehensive requirements |
| Over-engineering Prevention | ✅ | Built-in guidelines |
| Codebase Analysis | ✅ | For existing projects |
| User Stories | ✅ | In PRD section 10 |
| Technical Considerations | ✅ | In PRD section 8 |
| Success Metrics | ✅ | In PRD section 7 |

## Best Practices

### 1. Shared Planning Files
- Keep `.galdr/PLAN.md` in version control
- Phase documents in `.galdr/phases/`

### 2. Use Commands for Quick Access
- `@g-plan` for PRD creation
- `@g-phase-add` for new phases

### 3. Skill Activation
- Mention "plan", "PRD", "requirements" for natural activation

## Summary

the galdr planning system provides structured PRD creation and phase management through Cursor's rules, skills, and commands.
