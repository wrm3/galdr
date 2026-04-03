---
name: gemini-cli
description: Gemini CLI reference for Google's terminal AI agent. Covers installation, authentication, commands, MCP config, extensions, checkpointing, and cross-invocation with Cursor/Claude agents.
---

# Gemini CLI

Complete reference for the `gemini` command-line interface — Google's open-source terminal AI agent powered by Gemini 2.5 Pro with 1M token context. Self-updating -- check official docs before making structural changes.

## Self-Update Protocol

Before making changes to CLI-related configurations, fetch latest docs:
1. https://google-gemini.github.io/gemini-cli/docs/
2. https://google-gemini.github.io/gemini-cli/docs/cli/commands
3. https://google-gemini.github.io/gemini-cli/docs/get-started/authentication
4. https://google-gemini.github.io/gemini-cli/docs/get-started/configuration
5. https://google-gemini.github.io/gemini-cli/docs/tools/
6. https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server
7. https://google-gemini.github.io/gemini-cli/docs/extensions/

---

## Installation

```bash
# NPX (no install, always latest)
npx @google/gemini-cli

# Global install
npm install -g @google/gemini-cli
gemini

# macOS Homebrew
brew install gemini-cli

# Latest commit from GitHub
npx https://github.com/google-gemini/gemini-cli

# Docker sandbox
docker run --rm -it us-docker.pkg.dev/gemini-code-dev/gemini-cli/sandbox:0.1.1
```

---

## Authentication

| Method | Setup | Best For |
|--------|-------|----------|
| Google Account (OAuth) | `gemini` → select "Login with Google" | Individual devs, free tier (60 req/min, 1000 req/day) |
| Gemini API Key | `export GEMINI_API_KEY="..."` | Headless/CI, scripting |
| Vertex AI (ADC) | `gcloud auth application-default login` + `GOOGLE_CLOUD_PROJECT` | Enterprise, custom models |
| Vertex AI (Service Account) | `GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"` | CI/CD, non-interactive |
| Vertex AI (API Key) | `export GOOGLE_API_KEY="..."` | Quick Vertex access |

Persistent env vars: add to `~/.gemini/.env` or shell rc file. The CLI searches upward for `.env` files.

---

## Core Commands

| Command | Description |
|---------|-------------|
| `gemini` | Start interactive REPL |
| `gemini -p "query"` | Non-interactive (headless) mode |
| `echo "query" \| gemini` | Pipe input for non-interactive use |
| `gemini extensions install URL` | Install an extension |
| `gemini extensions list` | List installed extensions |
| `gemini extensions update --all` | Update all extensions |

### Slash Commands (Interactive)

| Command | Description |
|---------|-------------|
| `/help` or `/?` | Show available commands |
| `/tools [desc]` | List available tools (with optional descriptions) |
| `/mcp [desc\|schema]` | List MCP servers, tools, and schemas |
| `/memory show\|add\|refresh\|list` | Manage GEMINI.md hierarchical memory |
| `/chat save\|resume\|list\|delete\|share` | Checkpoint conversation state |
| `/compress` | Summarize chat to save tokens |
| `/restore [id]` | Restore files to pre-tool-call state |
| `/theme` | Change visual theme |
| `/stats` | Show token usage and session stats |
| `/settings` | Open settings editor |
| `/auth` | Change authentication method |
| `/about` | Show version info |
| `/clear` | Clear terminal (also `Ctrl+L`) |
| `/copy` | Copy last output to clipboard |
| `/editor` | Select preferred editor |
| `/extensions` | List active extensions |
| `/init` | Generate a GEMINI.md for current project |
| `/vim` | Toggle vim keybinding mode |
| `/bug` | File a GitHub issue |
| `/privacy` | View/set data collection consent |
| `/quit` or `/exit` | Exit the CLI |

### Input Shortcuts

| Prefix | Description |
|--------|-------------|
| `@path/to/file` | Inject file content into prompt |
| `@path/to/dir/` | Inject directory contents (git-aware) |
| `!command` | Execute shell command directly |
| `!` (alone) | Toggle persistent shell mode |

---

## CLI Flags

| Flag | Description |
|------|-------------|
| `-p, --prompt "text"` | Non-interactive mode |
| `--model NAME` | Choose model |
| `--sandbox` | Run tools in Docker sandbox |
| `--debug` | Enable debug logging |
| `--resume TAG` | Resume a saved chat checkpoint |
| `--yolo` | Auto-approve all tool calls (like `--dangerously-skip-permissions`) |
| `--non-interactive` | Disable interactive prompts |
| `--allowedTools TOOL [...]` | Pre-authorize specific tools |
| `--checkpointing` | Enable file checkpointing before tool calls |
| `--include-directories DIR [...]` | Add directories to workspace context |

---

## Configuration

### GEMINI.md (Project Instructions)

Hierarchical memory loaded from `GEMINI.md` files:
- `~/.gemini/GEMINI.md` — global (all projects)
- `PROJECT_ROOT/GEMINI.md` — project-level
- Subdirectory `GEMINI.md` files — scoped context

Equivalent to `CLAUDE.md` for Claude Code or `.cursor/rules/` for Cursor.

### .gemini/ Folder Structure

```
.gemini/
├── settings.json          # Project settings (overrides user settings)
├── .env                   # Environment variables (API keys, etc.)
├── sandbox-macos-custom.sb  # Custom sandbox profile (macOS)
├── sandbox.Dockerfile     # Custom sandbox profile (Docker)
└── extensions/            # Installed extensions
```

### Settings Precedence

1. System defaults → 2. User (`~/.gemini/settings.json`) → 3. Project (`.gemini/settings.json`) → 4. System overrides → 5. Env vars → 6. CLI flags

---

## MCP Integration

Add MCP servers in `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my/mcp-server"],
      "env": {
        "API_KEY": "$MY_API_KEY"
      },
      "timeout": 30000
    }
  }
}
```

Use `/mcp` to inspect connected servers and `/mcp schema` for tool parameter schemas.

---

## Cross-Invocation: Calling Gemini from Cursor/Claude

### From Cursor (Shell tool)

```bash
gemini -p "analyze src/ for security vulnerabilities" 2>&1
```

### From Claude Code (Bash tool)

```bash
gemini -p "refactor database layer for connection pooling" --yolo
```

### Coordination via galdr

All three CLIs can read/write `.galdr/TASKS.md` as shared task state:
1. Cursor agent marks task `[🔄]`
2. Gemini CLI picks up `[📋]` tasks via `-p` flag
3. Claude Code verifies completed work
4. TTL and timestamp rules prevent conflicts

---

## Reference Index

| File | Contents |
|------|----------|
| `reference/commands.md` | Full slash command reference with examples |
| `reference/tools.md` | Built-in tools, permissions, and sandbox mode |
| `reference/mcp_config.md` | MCP server configuration and settings |
| `reference/extensions.md` | Extension system, creation, and management |
