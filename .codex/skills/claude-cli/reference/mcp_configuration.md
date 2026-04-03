# MCP Configuration

Setup and management of MCP (Model Context Protocol) servers for Claude Code. Covers CLI commands, config file priority, and runtime flags.

Official docs: https://docs.anthropic.com/en/docs/claude-code/mcp

---

## CLI Management

```bash
claude mcp add my-server --command "python" --args "server.py"
claude mcp add my-server --url "http://localhost:8080/mcp"
claude mcp list
claude mcp remove my-server
```

---

## Config File Priority (highest to lowest)

1. `.mcp.json` (project root, highest priority)
2. `.claude/settings.local.json` under `mcpServers` key
3. `~/.claude.json` (user-global, lowest priority)

---

## Runtime Flags

```bash
claude --mcp-config ./custom-mcp.json        # Load specific config
claude --strict-mcp-config                     # Fail if servers can't start
claude --env DB_URL=postgres://localhost/mydb   # Env vars for MCP servers
```

---

## Scope Levels

| Scope | File | Committed? | Use Case |
|-------|------|------------|----------|
| Project | `.mcp.json` | Yes | Shared team servers |
| Personal | `.claude/settings.local.json` | No (gitignored) | Personal API keys, local servers |
| Global | `~/.claude.json` | N/A | User-wide defaults |

Lower-priority configs are merged into higher-priority ones. Per-server entries in a higher-priority file completely override the same server in a lower-priority file.
