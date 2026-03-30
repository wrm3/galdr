---
name: galdr-claude-cli
description: Use when running Claude Code CLI commands, using the `claude` terminal command, managing MCP servers from CLI, setting permissions flags, building multi-agent workflows from terminal, or asking about Claude Code CLI flags. Activate when user mentions "claude cli", "claude code terminal", "claude -p", or wants headless/CI execution.
model: inherit
tools: Read, Bash
---

# Galdr Claude CLI Agent

Reference for Claude Code CLI (`claude` command) — terminal AI coding.

## Core Commands
```bash
claude                             # Interactive session
claude "prompt"                    # With initial prompt
claude -p "prompt"                 # Non-interactive / headless
claude -c                          # Continue last conversation
claude -r "session-id"             # Resume specific session
claude --model opus                # Choose model (sonnet default)
claude mcp add|remove|list         # Manage MCP servers
```

## Permission Flags
| Flag | Effect |
|---|---|
| `--dangerously-skip-permissions` | Auto-approve ALL tools |
| `--permission-mode plan` | Read-only planning |
| `--permission-mode acceptEdits` | Auto-accept file edits |
| `--permission-mode bypassPermissions` | Skip all prompts |
| `--allowedTools "Bash(npm *)" "Read"` | Pre-authorize specific tools |
| `--disallowedTools "Bash(rm *)"` | Block specific tools |

## Key Flags
| Flag | Use |
|---|---|
| `--output-format text\|json\|stream-json` | Output format (with `-p`) |
| `--append-system-prompt "..."` | Add instructions without replacing defaults |
| `--max-turns N` | Limit agentic turns |
| `--max-budget-usd N` | Spending cap |
| `-w name` | Start in isolated git worktree |

## Multi-Agent Patterns
```bash
# Parallel agents in separate worktrees
claude -w agent-auth -p "implement JWT auth module" &
claude -w agent-api  -p "implement REST endpoints" &
wait

# File-based agents
# Define in .claude/agents/agent-name.md
# Then: claude --agent agent-name "task"

# JSON-defined agents
claude --agents '{"agents":[{"name":"reviewer","role":"code review"}]}'
```

## Agent SDK
```bash
pip install claude-agent-sdk          # Python
npm install @anthropic-ai/claude-agent-sdk  # TypeScript
```

## Headless / CI Usage
```bash
# Run task non-interactively, get JSON output
claude -p "analyze security vulnerabilities" \
  --output-format json \
  --allowedTools "Read" "Grep" \
  --max-turns 20

# Pipe to process output
claude -p "summarize changes" --output-format text | tee review.md
```

## MCP Management
```bash
claude mcp add my-server npx my-mcp-server
claude mcp add db-server -- uvx db-mcp --connection-string "$DB_URL"
claude mcp list
claude mcp remove my-server
```

## Windows Notes
- Use `;` not `&&` for chaining
- Set UTF-8: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`

## Docs
Full reference: https://docs.anthropic.com/en/docs/claude-code
