---
name: claude-cli
model: claude-sonnet-4
description: Orchestrates when to use Claude Code CLI vs IDE for batch operations
activation_type: proactive
auto_invoke: false
---

# Claude Code CLI Agent

**Model**: Claude Sonnet 4
**Purpose**: Decides when to delegate to Claude Code CLI for batch operations

## Overview

This agent detects when to use:
1. **IDE Integration** (small batches, IDE context needed)
2. **Claude Code CLI** (batch operations, background tasks)
3. **Hybrid workflows** (context gathering + batch execution)

## CLI Quick Reference

```bash
claude                           # Interactive mode (REPL)
claude "prompt"                  # Start with initial prompt
claude -p "prompt"               # Non-interactive, print result
claude -p "prompt" --output-format json  # JSON output for parsing
claude --continue                # Continue last conversation
claude --resume                  # Resume a specific conversation (interactive picker)

# Configuration
claude config list               # Show all settings
claude config set theme dark     # Set a config value
claude config set model sonnet   # Change default model

# MCP Server Management
claude mcp list                  # List configured MCP servers
claude mcp add <name> -- <cmd>   # Add an MCP server
claude mcp remove <name>         # Remove an MCP server

# Session Management
claude sessions list             # List previous conversations

# Project Setup
claude init                      # Initialize CLAUDE.md for a project
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
| Headless / SSH sessions | ❌ | ✅ |
| Multi-repo operations | ❌ | ✅ |

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
- Headless environment (SSH, containers)

### Strategy C: Non-Interactive (Pipeline Path)

**Use when**:
- Task is well-defined and repeatable
- Output needs to be captured or piped
- Running in CI/CD, cron jobs, or scripts
- No human interaction required

```bash
# Non-interactive with text output
claude -p "Find and fix linting issues in src/" --output-format text

# Non-interactive with JSON output for parsing
claude -p "Analyze code for security issues" --output-format json

# Pipe output to another tool
claude -p "Generate changelog from git log" | tee CHANGELOG.md
```

## CLI Flags Reference

| Flag | Short | Description |
|------|-------|-------------|
| `--print` | `-p` | Non-interactive mode (print and exit) |
| `--output-format` | | Output format: `text`, `json`, `stream-json` |
| `--continue` | `-c` | Continue most recent conversation |
| `--resume` | `-r` | Resume a specific conversation |
| `--model` | | Override model for this session |
| `--max-turns` | | Limit autonomous turns in -p mode |
| `--allowedTools` | | Restrict which tools can be used |
| `--disallowedTools` | | Block specific tools |
| `--permission-mode` | | Set permission level: `default`, `plan`, `bypassPermissions` |
| `--verbose` | | Enable verbose logging |

## Common Patterns

### Pattern 1: Batch File Processing

```bash
# Plan first
claude "Analyze all Python files in src/ and create a refactoring plan"

# Then execute
claude --continue "Execute the refactoring plan"
```

### Pattern 2: Task Automation (galdr)

```bash
# Create tasks from PLAN.md
claude "Read .galdr/PLAN.md and create task files for all features"

# Update task statuses
claude "Mark completed tasks based on git commits"
```

### Pattern 3: CI/CD Integration

```bash
# Non-interactive for pipelines
claude -p "Find and fix linting issues" --output-format text

# With JSON output for parsing
claude -p "Analyze code for security issues" --output-format json

# Limit autonomous actions
claude -p "Fix the failing tests" --max-turns 10
```

### Pattern 4: Multi-Step Workflows

```bash
# Step 1: Analyze
claude -p "Analyze the codebase structure and list all API endpoints" > api_report.txt

# Step 2: Use output as input
claude -p "Based on this API report, generate OpenAPI specs: $(cat api_report.txt)"

# Step 3: Continue previous conversation
claude --continue "Now generate client SDKs from the OpenAPI specs"
```

### Pattern 5: MCP Server Testing

```bash
# Add MCP server for testing
claude mcp add galdr --url http://localhost:8082/sse

# Test with MCP tools
claude "Use the galdr_server_status tool to check server health"
```

## MCP Configuration

### Adding MCP Servers

```bash
# SSE transport (Docker-based servers)
claude mcp add galdr --url http://localhost:8082/sse

# Stdio transport (local process)
claude mcp add my_server -- python my_mcp_server.py

# List configured servers
claude mcp list

# Remove a server
claude mcp remove galdr
```

### MCP Config File Location

Claude Code reads MCP configuration from `.mcp.json` in the project root:

```json
{
  "mcpServers": {
    "galdr": {
      "type": "url",
      "url": "http://localhost:8082/sse"
    }
  }
}
```

## Permission Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `default` | Asks for permission on writes | Interactive development |
| `plan` | Read-only, no file modifications | Code exploration, planning |
| `bypassPermissions` | No permission prompts | CI/CD, trusted automation |

```bash
# Read-only exploration
claude --permission-mode plan "Explain the authentication flow"

# Full automation (use with caution)
claude -p --permission-mode bypassPermissions "Fix all linting errors"
```

## Keyboard Shortcuts (Interactive CLI)

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift+Enter` | Insert newline (multi-line prompts) |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit CLI |
| `Up/Down` | Cycle previous messages |
| `/` | Open command menu |

## Slash Commands (Interactive)

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `/compact` | Summarize and compact conversation |
| `/config` | View/edit configuration |
| `/cost` | Show token usage and cost |
| `/doctor` | Check installation health |
| `/init` | Initialize CLAUDE.md |
| `/login` | Authenticate with Anthropic |
| `/logout` | Sign out |
| `/mcp` | Manage MCP servers |
| `/model` | Switch model |
| `/permissions` | View/manage permissions |
| `/status` | Show current status |
| `/terminal-setup` | Configure terminal integration |

## Error Handling

### Command Timeouts

```bash
# Limit autonomous turns to prevent runaway operations
claude -p "Process files" --max-turns 5

# For long operations, use interactive mode and monitor
claude "Process all migration files"
```

### Graceful Degradation

```bash
# Level 1: Retry with verbose logging
claude "Process files" --verbose

# Level 2: Break into smaller tasks
claude -p "Process models/*.py"
claude -p "Process views/*.py"

# Level 3: Restrict tools for safety
claude --allowedTools "Read,Write,Shell" "Fix the import errors"
```

## Integration with galdr

```bash
# Reference tasks
claude "implement task 720 - monitoring dashboards"

# Update task files
claude "mark task 720 as completed in TASKS.md"

# Create phase tasks
claude "create task files for phase 8 based on .galdr/PLAN.md"

# Run sync checks
claude -p "Check .galdr/TASKS.md sync status" --output-format text
```

## Differences from Cursor CLI

| Feature | Cursor CLI (`agent`) | Claude Code (`claude`) |
|---------|---------------------|----------------------|
| Interactive mode | `agent` | `claude` |
| Non-interactive | `agent -p "prompt"` | `claude -p "prompt"` |
| Continue session | `agent --continue` | `claude --continue` |
| Plan mode | `agent --mode=plan` | `claude --permission-mode plan` |
| Cloud/background | `& prompt` | Not available (use `--max-turns`) |
| MCP management | Via `mcp.json` | `claude mcp add/remove` |
| Config file | `.cursor/mcp.json` | `.mcp.json` (project root) |
| Session list | `agent ls` | `claude sessions list` |

## Usage

This agent works from **any terminal** (no IDE required).

Use Claude Code CLI for batch operations:
- **Claude Code CLI**: `claude "prompt"`
- **Non-interactive**: `claude -p "prompt" --output-format text`

---

**Version**: 1.0.0
**Status**: Production Ready
