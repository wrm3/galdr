---
name: claude-cli
description: Claude Code CLI reference — flags, headless and Agent SDK use, MCP, sessions, permissions, multi-agent workflows, Cursor integration.
---

# Claude Code CLI

Complete reference for the `claude` command-line interface. Self-updating -- check official docs before making structural changes.

## Self-Update Protocol

Before making changes to CLI-related configurations, fetch latest docs:
1. https://docs.anthropic.com/en/docs/claude-code/cli-reference
2. https://docs.anthropic.com/en/docs/claude-code/headless
3. https://docs.anthropic.com/en/docs/claude-code/sub-agents
4. https://docs.anthropic.com/en/docs/claude-code/permissions
5. https://docs.anthropic.com/en/docs/claude-code/mcp
6. https://docs.claude.com/en/api/agent-sdk/overview

---

## Installation

```bash
npm install -g @anthropic-ai/claude-code
```

---

## Core Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive REPL |
| `claude "query"` | Interactive with initial prompt |
| `claude -p "query"` | Non-interactive (print mode) |
| `claude -c` / `--continue` | Resume most recent conversation |
| `claude -r ID` / `--resume ID` | Resume specific session |
| `claude update` | Update to latest version |
| `claude auth login` | Authenticate |
| `claude auth status` | Check auth state |
| `claude mcp add NAME` | Add MCP server |
| `claude mcp list` | List MCP servers |
| `claude mcp remove NAME` | Remove MCP server |
| `claude agents` | List configured subagents |

---

## CLI Flags Reference

### Session Flags
| Flag | Description |
|------|-------------|
| `-c, --continue` | Resume last conversation |
| `-r, --resume ID` | Resume specific session by ID or name |
| `--fork-session` | Branch from existing session (keeps history, new thread) |
| `--session-id UUID` | Use specific session UUID |
| `--from-pr NUMBER` | Resume session linked to a PR |
| `--no-session-persistence` | Don't save session (ephemeral) |

### Permission Flags
| Flag | Description |
|------|-------------|
| `--dangerously-skip-permissions` | Auto-approve ALL tools (no prompts) |
| `--permission-mode MODE` | Set permission behavior (see `reference/permissions_hooks.md`) |
| `--allowedTools TOOL [TOOL...]` | Pre-authorize specific tools |
| `--disallowedTools TOOL [TOOL...]` | Block specific tools |
| `--tools TOOL [TOOL...]` | Restrict available tool set entirely |

### System Prompt Flags (mutually exclusive groups)
| Flag | Description |
|------|-------------|
| `--system-prompt TEXT` | Replace ALL default instructions |
| `--system-prompt-file PATH` | Replace from file |
| `--append-system-prompt TEXT` | Add to defaults (recommended) |
| `--append-system-prompt-file PATH` | Append from file |

### Output Flags
| Flag | Description |
|------|-------------|
| `--output-format text\|json\|stream-json` | Output format (with `-p`) |
| `--input-format text\|stream-json` | Input format for piping |
| `--json-schema SCHEMA` | Validate output against JSON schema |
| `--verbose` | Enable detailed logging |

### Execution Flags
| Flag | Description |
|------|-------------|
| `--model NAME` | Choose model (opus, sonnet, haiku) |
| `--max-turns N` | Limit agentic turns (with `-p`) |
| `--max-budget-usd N` | Spending cap |
| `--max-input-tokens N` | Input token limit |
| `-w, --worktree NAME` | Start in isolated git worktree |
| `--cwd PATH` | Set working directory |

### Agent Flags
| Flag | Description |
|------|-------------|
| `--agents JSON` | Define subagents via JSON object |
| `--teammate-mode` | Enable agent team coordination |

### MCP Flags
| Flag | Description |
|------|-------------|
| `--mcp-config PATH` | Load MCP config from file |
| `--strict-mcp-config` | Fail if MCP servers can't start |
| `--env KEY=VALUE` | Set env vars for MCP servers |

---

## Output Formats

| Format | Use Case |
|--------|----------|
| `text` | Human-readable (default) |
| `json` | Machine parsing — single JSON object on completion |
| `stream-json` | Real-time streaming — newline-delimited JSON messages |

```bash
claude -p "List endpoints" --output-format json
cat src/app.ts | claude -p "Review this" --output-format stream-json
```

---

## Session Management

| Action | Command |
|--------|---------|
| Continue last | `claude -c` or `claude --continue` |
| Resume by ID | `claude -r "session-id"` |
| Resume interactively | `claude --resume` (shows picker) |
| Fork session | `claude --fork-session` |
| Resume from PR | `claude --from-pr 123` |
| Named session | `claude --session-id "my-uuid"` |
| Ephemeral (no save) | `claude -p "query" --no-session-persistence` |

---

## Slash Commands (Interactive Mode)

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `/compact` | Summarize conversation to save context |
| `/init` | Create starter CLAUDE.md |
| `/allowed-tools` | Manage allowed tools |
| `/resume` | Pick session to continue |
| `/rename` | Rename current session |

---

## Troubleshooting

- **Windows**: Use `;` not `&&` for command chaining. Set UTF-8: `$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8`
- **Permission denied**: Use `--allowedTools` to pre-authorize, or `--dangerously-skip-permissions` in sandboxed environments
- **MCP timeout**: Set `MCP_TIMEOUT=60000` env var for slow-starting servers
- **Context overflow**: Use `/compact` to summarize and free context space

---

## Reference Index

Detailed content extracted into focused reference files:

| File | Contents |
|------|----------|
| `reference/agent_sdk.md` | Python + TypeScript Agent SDK, `ClaudeAgentOptions`, permission modes |
| `reference/multi_agent_patterns.md` | Orchestrator, pipeline, fan-out, worktree parallelism, cross-invocation with Cursor |
| `reference/mcp_configuration.md` | MCP server setup, config file priority, runtime flags |
| `reference/headless_ci.md` | Headless mode, CI/CD pipeline patterns, Docker usage |
| `reference/permissions_hooks.md` | Permission modes, `allowedTools` syntax, settings files, slash commands |
