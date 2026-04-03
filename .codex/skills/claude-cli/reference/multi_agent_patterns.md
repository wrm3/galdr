# Multi-Agent Patterns

Patterns for running multiple Claude Code agents in coordination. Covers dynamic subagents, file-based agents, parallel worktrees, team mode, and cross-invocation with Cursor CLI.

Official docs: https://docs.anthropic.com/en/docs/claude-code/sub-agents

---

## 1. Dynamic Subagents (`--agents` flag)

```bash
claude --agents '{
  "agents": [
    {
      "name": "security-reviewer",
      "description": "Reviews code for security vulnerabilities",
      "instructions": "Focus on OWASP Top 10, injection, XSS, auth issues",
      "tools": ["Read", "Grep", "Glob"],
      "model": "sonnet"
    },
    {
      "name": "test-writer",
      "description": "Writes unit tests for changed files",
      "tools": ["Read", "Write", "Bash(npm test)"],
      "model": "sonnet"
    }
  ]
}'
```

### Subagent JSON Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | kebab-case identifier |
| `description` | Yes | When to use this agent |
| `instructions` | No | System prompt addition |
| `tools` | No | Allowed tools list |
| `disallowedTools` | No | Blocked tools |
| `model` | No | Model override |
| `skills` | No | Skills to load |
| `mcpServers` | No | MCP servers available |
| `maxTurns` | No | Turn limit |

---

## 2. File-Based Agents (`.claude/agents/*.md`)

```markdown
---
name: backend-developer
description: Backend APIs, business logic, database work
tools: ["Read", "Edit", "Write", "Bash", "Grep", "Glob"]
model: sonnet
---

# Backend Developer

You are a backend specialist. Focus on API design, database queries,
and server-side logic. Follow project conventions in CLAUDE.md.
```

---

## 3. Parallel Execution via Worktrees

```bash
claude -w backend-work -p "Implement user API endpoints" \
  --dangerously-skip-permissions --allowedTools "Read" "Edit" "Write" "Bash(npm *)" &

claude -w frontend-work -p "Build user profile component" \
  --dangerously-skip-permissions --allowedTools "Read" "Edit" "Write" "Bash(npm *)" &

wait

git merge backend-work --no-edit
git merge frontend-work --no-edit
git worktree remove .claude/worktrees/backend-work
git worktree remove .claude/worktrees/frontend-work
```

---

## 4. Agent Teams (`--teammate-mode`)

Enables coordination between agents via shared task state:

```bash
claude --teammate-mode -p "Coordinate implementation of auth feature" \
  --agents '{"agents": [
    {"name": "api-dev", "description": "Backend API", "tools": ["Read","Edit","Bash(npm *)"]},
    {"name": "ui-dev", "description": "Frontend UI", "tools": ["Read","Edit","Bash(npm *)"]}
  ]}'
```

---

## Cross-Invocation: Calling Cursor from Claude Code

### Via Bash Tool

```bash
agent -p "implement database migration" --output-format json

agent -c "long-running refactor task"
```

### Via Cursor Cloud Agents API

```bash
CURSOR_AUTH=$(echo -n "$CURSOR_API_KEY:" | base64)

curl -s -X POST "https://api.cursor.com/v0/agents" \
  -H "Authorization: Basic $CURSOR_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Implement user authentication",
    "repository": "github.com/org/repo",
    "branch": "feature/auth"
  }'
```

### Coordination via galdr

Both CLIs can read/write `.galdr/TASKS.md`. Use it as shared task state:
1. Claude Code marks task `[🔄]` in TASKS.md
2. Cursor agent reads TASKS.md, picks up `[📋]` tasks
3. Both update atomically when done
