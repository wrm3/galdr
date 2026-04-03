---
name: cursor-cli
description: Cursor CLI (`agent`) — modes, Cloud Agent, API, multi-agent, permissions, sessions, and Claude Code cross-use.
---

# Cursor CLI

Complete reference for the `agent` command-line interface (Cursor CLI). Self-updating -- check official docs before making structural changes.

## Self-Update Protocol

Before making changes to CLI-related configurations, fetch latest docs:
1. https://cursor.com/docs/cli/overview
2. https://cursor.com/docs/cli/using
3. https://cursor.com/docs/agent
4. https://cursor.com/docs/cloud-agent
5. https://cursor.com/docs/cloud-agent/api/endpoints
6. https://cursor.com/docs/api

---

## Installation

Cursor CLI is bundled with Cursor IDE. The `agent` command is available once Cursor is installed.

---

## Core Commands

| Command | Description |
|---------|-------------|
| `agent` | Start interactive REPL |
| `agent "query"` | Interactive with initial prompt |
| `agent -p "query"` | Non-interactive (print mode) |
| `agent --mode=plan "query"` | Plan mode (design, no code changes) |
| `agent --mode=ask "query"` | Ask mode (read-only exploration) |
| `agent ls` | List previous conversations |
| `agent resume` | Resume most recent session |
| `agent --resume="id"` | Resume specific session |
| `agent -c "query"` | Send directly to Cloud Agent |
| `agent acp` | ACP server mode (JSON-RPC over stdio) |

---

## Modes

### Agent Mode (Default)
Full tool access -- implementation, refactoring, bug fixes. Requires approval for shell commands.

### Plan Mode
Design approach before coding. Asks clarifying questions, generates implementation strategy.
- Invoke: `--mode=plan`, `--plan`, `/plan`, or `Shift+Tab`
- No file modifications

### Ask Mode
Read-only exploration for code comprehension. Zero side effects.
- Invoke: `--mode=ask`, `/ask`, or `Shift+Tab` twice

### Debug Mode
Hypothesis generation, log instrumentation, root cause analysis.
- Invoke: `/debug`

### Mode Switching
- `Shift+Tab` rotates: Agent -> Plan -> Ask -> Agent
- Slash commands (`/plan`, `/ask`, `/debug`) switch immediately

---

## CLI Flags

| Flag | Description |
|------|-------------|
| `--mode=plan\|ask` | Set agent mode |
| `--plan` | Shorthand for `--mode=plan` |
| `-p "prompt"` | Non-interactive mode |
| `--output-format text\|json` | Output format (with `-p`) |
| `--model "model-name"` | Choose model |
| `-c, --cloud` | Send to Cloud Agent |
| `--continue` | Resume previous conversation |
| `--resume="id"` | Resume specific session |
| `--sandbox enabled\|disabled` | Control sandbox behavior |
| `@file` / `@dir` | Include specific files/folders as context |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Rotate modes (Agent -> Plan -> Ask) |
| `Shift+Enter` | Insert newline (multi-line prompt) |
| `Ctrl+R` | Review changes before approval |
| `Ctrl+C` (twice) | Exit CLI session |
| `Arrow Up/Down` | Cycle through previous messages |
| `Tab` | Add command to permanent allowlist |
| `y` / `n` | Approve / reject shell command |
| `i` (in review) | Add follow-up instructions |
| `Ctrl+O` | Expand truncated output |

---

## Cloud Agent Handoff

Cloud Agents run on isolated VMs independent of your local machine. They can build, test, and interact with software autonomously.

### Handoff Methods

```bash
# Method 1: Ampersand prefix (mid-conversation)
& implement complete auth module with tests

# Method 2: Cloud flag
agent -c "long-running data migration task"

# Method 3: Monitor at cursor.com/agents
```

### Cloud Agent Properties
- Always runs in **Max Mode** (cannot disable)
- Isolated VM environment with full dev tools
- Can use the software it creates (browser, terminal)
- Produces merge-ready PRs with artifacts (screenshots, videos, logs)
- Survives terminal/machine disconnect

### Access Points
| Platform | How |
|----------|-----|
| Web | cursor.com/agents (full dashboard) |
| Desktop | Cursor IDE |
| Slack | `@cursor` commands |
| GitHub | `@cursor` on PRs/issues |
| GitLab | `@cursor` on MRs/issues |
| Linear | `@cursor` on issues |
| Mobile | Progressive Web App |
| API | REST endpoints (see below) |

---

## Cloud Agents API

### Authentication

```bash
# Get API key from: cursor.com/settings > API Keys
# Auth method: Basic (base64 of "api_key:")
CURSOR_AUTH=$(echo -n "$CURSOR_API_KEY:" | base64)
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v0/agents` | List all agents |
| `GET` | `/v0/agents/{id}` | Get agent status |
| `GET` | `/v0/agents/{id}/conversation` | Get chat history |
| `GET` | `/v0/agents/{id}/artifacts` | List generated files |
| `GET` | `/v0/agents/{id}/artifacts/download` | Download artifact |
| `POST` | `/v0/agents` | Launch new agent |
| `POST` | `/v0/agents/{id}/followup` | Add instructions to running agent |
| `POST` | `/v0/agents/{id}/stop` | Stop agent |
| `DELETE` | `/v0/agents/{id}` | Delete agent |
| `GET` | `/v0/me` | API key info |
| `GET` | `/v0/models` | List available models |
| `GET` | `/v0/repositories` | List connected repos |

### Launch Agent

```bash
curl -s -X POST "https://api.cursor.com/v0/agents" \
  -H "Authorization: Basic $CURSOR_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Implement user authentication with JWT",
    "repository": "github.com/org/project",
    "branch": "feature/auth",
    "model": "auto"
  }'
```

### Monitor Agent

```bash
curl -s "https://api.cursor.com/v0/agents/AGENT_ID" \
  -H "Authorization: Basic $CURSOR_AUTH" | jq
```

### Add Follow-Up

```bash
curl -s -X POST "https://api.cursor.com/v0/agents/AGENT_ID/followup" \
  -H "Authorization: Basic $CURSOR_AUTH" \
  -H "Content-Type: application/json" \
  -d '{"message": "Also add error handling and input validation"}'
```

### Rate Limits
- Standard endpoints: 20 requests/minute
- Analytics API: 100 requests/minute (team), 50 (user)
- ETags supported: 304 responses don't count against limits

---

## Multi-Agent / Cursor 2.0

### Parallel Agents
- Up to **8 simultaneous agents**
- Automatic git worktree management (each agent gets isolated copy)
- Available via Cloud Agents API and IDE
- Multiple models can work same problem for better output quality

### Local Multi-Agent Pattern

```bash
# Terminal 1
cd ../project-worktree-1 && agent "implement API layer"

# Terminal 2
cd ../project-worktree-2 && agent "implement UI components"

# After both complete, merge from main repo
git merge worktree-1-branch --no-edit
git merge worktree-2-branch --no-edit
```

### API Multi-Agent Pattern

```bash
# Launch multiple agents via API
for TASK in "implement auth" "implement database" "implement UI"; do
  curl -s -X POST "https://api.cursor.com/v0/agents" \
    -H "Authorization: Basic $CURSOR_AUTH" \
    -H "Content-Type: application/json" \
    -d "{\"task\": \"$TASK\", \"repository\": \"github.com/org/repo\"}" &
done
wait
echo "All agents launched"
```

---

## Background Agents / Sandbox

### Sandbox Model
- Background/Cloud agents auto-execute commands within sandbox
- Only ask approval when stepping outside sandbox boundaries:
  - Internet/external API access
  - System resources outside project
  - Protected system commands

### Secrets Management
- Store secrets in Cursor Settings > Secrets tab
- Available to Cloud Agents as environment variables
- Never stored in code or config files

### Permission Config Files

```json
// .cursor/cli.json (project-level)
{
  "allow": [
    "Read(src/**/*)",
    "Write(src/**/*.ts)",
    "Shell(npm test)"
  ],
  "deny": [
    "Write(package.json)",
    "Shell(rm)"
  ]
}
```

```json
// ~/.cursor/cli-config.json (global)
{
  "permissions": {
    "shell": {
      "always_approve": ["git", "npm test"],
      "always_deny": ["rm -rf", "sudo"],
      "prompt": ["python", "docker"]
    }
  }
}
```

---

## Permissions & Approval

### Interactive Approval Flow
```
Agent wants to run: npm test
  y  → approve this command
  n  → reject this command
  Tab → add to permanent allowlist (approve all similar)
```

### Non-Interactive Mode
Full write access when using `-p` flag. Commands execute without prompts.

### Sandbox Control
- `/sandbox` → interactive sandbox configuration menu
- `--sandbox enabled|disabled` → CLI flag

---

## Session Management

| Action | Command |
|--------|---------|
| List sessions | `agent ls` |
| Resume last | `agent resume` |
| Resume specific | `agent --resume="session-id"` |
| Compress context | `/compress` (in session) |
| Switch mode | `Shift+Tab` or `/plan` `/ask` |

---

## Cross-Invocation: Calling Claude Code from Cursor

### Via Terminal (Bash tool)

```bash
# Launch Claude Code on a task
claude -p "implement database migration" --output-format json

# With permission bypass for unattended execution
claude -p "fix all lint errors" \
  --dangerously-skip-permissions \
  --allowedTools "Read" "Edit" "Bash(npx eslint *)" \
  --max-turns 20

# Continue a Claude Code session
claude -c -p "add tests for the migration"
```

### Via Claude Agent SDK (Python)

```python
from claude_agent_sdk import query, ClaudeAgentOptions
import anyio

async def run_claude_agent():
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        allowed_tools=["Read", "Edit", "Bash(npm test)"],
        max_turns=20,
    )
    async for msg in query("Fix failing tests", options):
        print(msg.content if hasattr(msg, 'content') else msg)

anyio.run(run_claude_agent)
```

### Coordination via galdr

Both CLIs can read/write `.galdr/TASKS.md`. Use it as shared task state:
1. Cursor agent marks task `[🔄]` in TASKS.md
2. Claude Code reads TASKS.md, picks up `[📋]` tasks
3. Both update atomically when done
4. Multi-agent concurrency rules (TTL, timestamps) prevent conflicts

---

## Configuration

### Rules Loading
CLI automatically loads:
- `.cursor/rules/*.mdc` — rule files
- `AGENTS.md` — project root instructions
- `CLAUDE.md` — project root instructions

### MCP Configuration
- `.cursor/mcp.json` — project-level MCP servers
- MCP not yet supported by Cloud Agents API (use separate MCP servers)

### Context Inclusion
- `@file.ts` or `@src/` — include specific files/folders
- `/compress` — reduce context window usage

---

## Community SDK

The `@nothumanwork/cursor-agents-sdk` (npm) provides a TypeScript wrapper:

```bash
npm install @nothumanwork/cursor-agents-sdk
```

```typescript
import { CursorAgentsSDK } from "@nothumanwork/cursor-agents-sdk";

const sdk = new CursorAgentsSDK({ apiKey: process.env.CURSOR_API_KEY });

const agent = await sdk.createAgent({
  task: "Implement database migrations",
  repository: "github.com/user/repo",
});

const status = await sdk.getAgentStatus(agent.id);
await sdk.addFollowup(agent.id, "Also add error handling");
```

**Note**: This is a community package, not officially maintained by Cursor.

---

## Troubleshooting

- **Windows**: Use `;` not `&&` for command chaining
- **Terminal newlines**: Run `/setup-terminal` to configure `Option+Enter` / `Alt+Enter`
- **Hung commands**: `Ctrl+C` to cancel, avoid interactive prompts
- **Truncated output**: `Ctrl+O` to expand
- **Context overflow**: Use `/compress` to summarize and free space
