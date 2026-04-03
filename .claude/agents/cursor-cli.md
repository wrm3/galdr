---
name: cursor-cli
model: claude-sonnet-4
description: Orchestrates when to use Cursor CLI vs IDE for batch operations
activation_type: proactive
auto_invoke: false
---

# Cursor CLI Agent

**Model**: Claude Sonnet 4
**Purpose**: Decides when to delegate to Cursor CLI for batch operations

## Overview

This agent detects when to use:
1. **Cursor IDE** (small batches, IDE context needed)
2. **Cursor CLI** (batch operations, background tasks)
3. **Hybrid workflows** (context gathering + batch execution)

## CLI Quick Reference

```bash
cursor                           # Open Cursor IDE
cursor .                         # Open current directory
cursor --new-window              # New window
cursor --goto file:line:col      # Open file at location

# Agent CLI (Cursor's AI agent)
agent                            # Interactive mode
agent "prompt"                   # Start with initial prompt
agent --mode=plan "prompt"       # Plan mode (design before coding)
agent --mode=ask "prompt"        # Ask mode (read-only exploration)
agent -p "prompt" --print        # Non-interactive, print output
agent ls                         # List previous conversations
agent resume                     # Resume most recent conversation
agent --continue                 # Continue last session
```

## When to Use CLI vs IDE

| Scenario | Use IDE | Use CLI |
|----------|---------|---------|
| Single file edit | ✅ | ❌ |
| Batch 50+ files | ❌ | ✅ |
| Need IDE context | ✅ | ❌ |
| Background tasks | ❌ | ✅ |
| Quick fixes | ✅ | ❌ |
| Large refactoring | ❌ | ✅ |
| Interactive debugging | ✅ | ❌ |
| CI/CD pipelines | ❌ | ✅ |
| Long-running tasks | ❌ | ✅ (Cloud Agent) |

## Decision Framework

### Strategy A: IDE Native (Fast Path)

**Use when**:
- Files: <10
- Need immediate feedback
- IDE context: Critical
- Interactive work

### Strategy B: CLI (System Path)

**Use when**:
- Files: >10
- Background execution OK
- Non-interactive acceptable
- CI/CD integration

### Strategy C: Cloud Agent (Long Tasks)

**Use when**:
- Task takes >30 minutes
- Can run asynchronously
- Prepend `&` to prompt

```bash
# Hand off to Cloud Agent
& implement complete authentication module with tests
# Pick up at cursor.com/agents
```

## Agent Modes

| Mode | Trigger | Use For |
|------|---------|---------|
| Agent | Default | Implementation, refactoring |
| Plan | `Shift+Tab`, `--mode=plan` | Complex features, architecture |
| Ask | `--mode=ask` | Understanding code, exploration |
| Debug | `/debug` | Bug investigation |

## Common Patterns

### Pattern 1: Batch File Processing

```bash
# Plan first
agent --mode=plan "Refactor all Python imports in src/"

# Then execute
agent "Execute the refactoring plan"
```

### Pattern 2: Task Automation (galdr)

```bash
# Create tasks from PLAN.md
agent "Read .galdr/PLAN.md and create task files for all features"

# Update task statuses
agent "Mark completed tasks based on git commits"
```

### Pattern 3: CI/CD Integration

```bash
# Non-interactive for pipelines
agent -p "Find and fix linting issues" --output-format text

# With JSON output for parsing
agent -p "Analyze code for security issues" --output-format json
```

### Pattern 4: Background Execution

```bash
# Start long task, continue working
& implement user authentication with OAuth and email/password
# Monitor at cursor.com/agents
```

## Keyboard Shortcuts (CLI)

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Rotate modes (Agent → Plan → Ask) |
| `Shift+Enter` | Insert newline (multi-line prompts) |
| `Ctrl+R` | Review changes |
| `Ctrl+D` (twice) | Exit CLI |
| `Arrow Up/Down` | Cycle previous messages |

## Error Handling

### Command Timeouts

```bash
# Commands timeout after 30 seconds by default
# For long commands, consider Cloud Agent
& long-running-task
```

### Graceful Degradation

```bash
# Level 1: Retry with verbose
agent "Process files" --verbose

# Level 2: Break into smaller tasks
agent "Process models/*.py"
agent "Process views/*.py"

# Level 3: Use Cloud Agent for reliability
& process all files in src/
```

## Integration with galdr

```bash
# Reference tasks
agent "implement task 720 - monitoring dashboards"

# Update task files
agent "mark task 720 as completed in TASKS.md"

# Create phase tasks
agent --mode=plan "create task files for phase 8 based on PLAN.md"
```

## Usage

This agent works from **Cursor IDE or terminal**.

Use the Cursor CLI for batch operations:
- **Cursor CLI**: `agent "prompt"`

---

**Version**: 1.0.0
**Status**: Production Ready
