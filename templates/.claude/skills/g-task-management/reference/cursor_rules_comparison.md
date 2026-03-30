# Cursor Rules and Skills Integration

## Overview

This document describes how the galdr task management system integrates with Cursor's rules and skills architecture.

## Cursor Features Used

### Rules (`.cursor/rules/`)
- **Format**: `.mdc` files (Markdown Cursor)
- **Location**: `.cursor/rules/galdr/rules/`
- **Activation**: Always active or globs-based

### ✅ 100% Compatible


### Skills (`.cursor/skills/`)
- **Format**: `SKILL.md` files with reference/ folders
- **Location**: `.cursor/skills/g-task-management/`
- **Activation**: Natural language triggers

### Commands (`.cursor/commands/`)
- **Format**: `.md` files
- **Prefix**: `@g-*`
- **Examples**: `@g-setup`, `@g-task-new`

## File Format Standards

### Task File Structure
```yaml
---
id: 001
title: 'Task Title'
status: pending
priority: high
phase: 0
subsystems: [subsystem1, subsystem2]
project_context: 'Brief description'
dependencies: []
---

# Task 001: Task Title

## Objective
[Task description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### TASKS.md Format
```markdown
# Project Name - Task List

## Phase 0: Setup & Infrastructure
- [ ] Task 001: Task Title
- [🔄] Task 002: In Progress Task
- [✅] Task 003: Completed Task
```

## Workflow Integration

### Creating a Task
1. User: "Create a task to implement user authentication"
2. Skill activates based on natural language
3. Creates `task001_implement_user_auth.md`
4. Updates `TASKS.md`

### Using Commands
1. User: `@g-task-new`
2. Command guides task creation
3. Creates task file and updates TASKS.md

## Feature Matrix

| Feature | Supported | Notes |
|---------|-----------|-------|
| Task Creation | ✅ | Via skill or command |
| Task Status Update | ✅ | Emoji indicators |
| Sub-task Creation | ✅ | task42.1, 42.2 format |
| Task Dependencies | ✅ | Array in frontmatter |
| YAML Frontmatter | ✅ | Standard format |
| Windows-safe Emojis | ✅ | 🔄 ✅ ❌ |
| Auto-folder Creation | ✅ | Silent operation |
| Phase Organization | ✅ | Phase-based task IDs |
| Bug References | ✅ | Links to BUGS.md |
| Retroactive Tasks | ✅ | Document past work |

## Best Practices

### 1. Shared File Structure
- Keep `.galdr/` in version control
- Task files are plain markdown with YAML

### 2. Use Commands for Quick Access
- `@g-setup` for initialization
- `@g-task-new` for task creation
- `@g-status` for project overview

### 3. Skill Activation
- Mention "task", "todo", "work item" for natural activation
- Skills provide conversational guidance

## Troubleshooting

### Issue: Skill not recognizing task files
**Solution:** Ensure `.cursor/skills/g-task-management/` exists with SKILL.md

### Issue: Rules not applying
**Solution:** Ensure `.cursor/rules/galdr/` exists with rules.mdc

### Issue: Task files not updating
**Solution:** Check file permissions for `.galdr/`

## Summary

The galdr system uses Cursor's rules, skills, and commands architecture to provide comprehensive task management with YAML frontmatter and Windows-safe emoji indicators.
