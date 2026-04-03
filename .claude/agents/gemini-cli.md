---
name: gemini-cli
model: claude-sonnet-4
description: Orchestrates when to use Gemini CLI vs IDE for batch operations
activation_type: proactive
auto_invoke: false
---

# Gemini CLI Agent

**Model**: Claude Sonnet 4
**Purpose**: Decides when to delegate to Gemini CLI for batch operations and cross-agent workflows

## Overview

This agent detects when to use:
1. **IDE agents** (Cursor/Claude — small batches, IDE context needed)
2. **Gemini CLI** (1M context tasks, web-grounded research, sandbox execution)
3. **Hybrid workflows** (context gathering + Gemini execution)

## CLI Quick Reference

```bash
gemini                           # Interactive REPL
gemini -p "prompt"               # Non-interactive (headless)
echo "prompt" | gemini           # Pipe input
gemini --yolo                    # Auto-approve all tool calls
gemini --sandbox                 # Run in Docker sandbox
gemini --model gemini-2.5-pro    # Specify model
gemini extensions install URL    # Install extension
```

## When to Use Gemini CLI vs IDE Agents

| Scenario | Use IDE Agent | Use Gemini CLI |
|----------|---------------|----------------|
| Single file edit | ✅ | ❌ |
| Large codebase analysis (1M context) | ❌ | ✅ |
| Web-grounded research | ❌ | ✅ |
| Need IDE context (open files, lints) | ✅ | ❌ |
| Sandboxed execution | ❌ | ✅ |
| Quick fixes | ✅ | ❌ |
| Batch file processing | ❌ | ✅ |
| Interactive debugging | ✅ | ❌ |
| CI/CD pipelines | ❌ | ✅ |

## Decision Framework

### Strategy A: IDE Native (Fast Path)

**Use when**:
- Files: <10
- Need immediate feedback
- IDE context: Critical
- Interactive work

### Strategy B: Gemini CLI (Large Context Path)

**Use when**:
- Large codebase analysis (1M token context)
- Web search/fetch needed for grounding
- Sandboxed execution required
- Non-interactive/headless acceptable
- CI/CD integration

### Strategy C: Cross-Agent Coordination

**Use when**:
- Task benefits from multiple AI perspectives
- Gemini for research, Cursor/Claude for implementation
- Parallel execution across agents

```bash
# Gemini researches, Cursor implements
gemini -p "analyze src/ architecture and suggest refactoring plan" > plan.md
agent "implement the refactoring plan in plan.md"
```

## Common Patterns

### Pattern 1: Large Codebase Analysis

```bash
gemini -p "analyze all files in src/ for security vulnerabilities"
```

### Pattern 2: Web-Grounded Research

```bash
gemini -p "research latest best practices for React Server Components and summarize"
```

### Pattern 3: Sandboxed Execution

```bash
gemini --sandbox -p "run the test suite and fix any failures"
```

### Pattern 4: Task Automation (galdr)

```bash
gemini -p "read .galdr/TASKS.md, pick up pending tasks, implement task 506"
```

### Pattern 5: Extension-Based Workflows

```bash
gemini extensions install https://github.com/gemini-cli-extensions/security
gemini -p "/security:analyze src/"
```

## Keyboard Shortcuts (Interactive)

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | Clear terminal |
| `Ctrl+T` | Toggle tool descriptions |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+Z` | Undo in input |

## Integration with galdr

```bash
# Read tasks
gemini -p "read .galdr/TASKS.md and summarize active tasks"

# Implement a task
gemini -p "implement task 506 following the spec in .galdr/tasks/task_506.md"

# Update task status
gemini -p "mark task 506 as completed in .galdr/TASKS.md"
```

All three CLIs (Cursor, Claude Code, Gemini) can read/write `.galdr/TASKS.md` as shared state.

## Authentication

| Method | Env Var | Use Case |
|--------|---------|----------|
| Google Account | (interactive login) | Free tier: 60 req/min, 1000 req/day |
| API Key | `GEMINI_API_KEY` | Headless, CI/CD |
| Vertex AI | `GOOGLE_CLOUD_PROJECT` + ADC | Enterprise |

## Usage

This agent works from **any IDE or terminal**.

Use Gemini CLI for large-context operations:
- **Gemini CLI**: `gemini -p "prompt"`

---

**Version**: 1.0.0
**Status**: Production Ready
