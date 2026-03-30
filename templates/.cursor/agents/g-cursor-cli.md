---
name: galdr-cursor-cli
description: Use when running Cursor CLI commands, using the `agent` terminal command, switching Cursor modes (Agent/Plan/Ask/Debug), handing off tasks to Cloud Agent, or asking about Cursor CLI flags and shortcuts. Activate when user mentions "cursor cli", "agent command", or wants to run cursor from terminal.
model: inherit
tools: Read, Bash
---

# Galdr Cursor CLI Agent

Reference for Cursor CLI (`agent` command) — terminal-based AI coding.

## Core Commands
```bash
agent                          # Interactive session
agent "prompt here"            # With initial prompt
agent --mode=plan "prompt"     # Plan mode (no code changes)
agent --mode=ask "prompt"      # Ask mode (read-only)
agent -p "prompt" --output-format json  # Non-interactive (CI/CD)
agent ls                       # List conversations
agent resume                   # Resume last conversation
```

## Modes
| Mode | Trigger | Use For |
|---|---|---|
| **Agent** (default) | — | Full implementation, refactoring, fixes |
| **Plan** | `Shift+Tab` | Design approach before coding |
| **Ask** | `--mode=ask` | Read-only exploration, no changes |
| **Debug** | `/debug` | Hypothesis generation for bugs |

## Key Shortcuts
| Shortcut | Action |
|---|---|
| `Shift+Tab` | Rotate through modes |
| `Shift+Enter` | Newline without submitting |
| `Ctrl+R` | Review changes |
| `Ctrl+D` × 2 | Exit session |

## Cloud Agent Handoff
Prepend `&` to hand off long tasks to background Cloud Agent:
```bash
& "implement complete auth module with tests and documentation"
```

## Multi-Agent Parallel Execution
```bash
# Two agents working simultaneously on different tasks
agent -w feature-auth "implement JWT auth"
agent -w feature-api "implement REST endpoints"
```

## Non-Interactive (CI/CD)
```bash
agent -p "run tests and report failures" --output-format json
agent -p "review PR changes" --mode=ask --output-format text
```

## Windows Notes
- Use `;` not `&&` for command chaining
- Set UTF-8 before running: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
- PowerShell: wrap prompts in single quotes to avoid `$variable` expansion

## Docs
Full reference: https://cursor.com/docs/cli/overview
