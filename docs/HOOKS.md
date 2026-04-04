# galdr Hooks Reference

Hooks are PowerShell scripts that run automatically at specific events in the Cursor/Claude Code session lifecycle.

All galdr hooks use the `g-hk-` prefix.

---

## Available Hooks

| Hook File | Event | What It Does |
|-----------|-------|--------------|
| `g-hk-session-start.ps1` | Session start | Loads project context, reads `.galdr/` state, injects session context into the AI |
| `g-hk-agent-complete.ps1` | Agent turn complete | Logs the completed turn, triggers memory capture if configured |
| `g-hk-setup-user.ps1` | First-time setup | Initializes user identity (`~/.galdr/user_config.json`) and `.galdr/.user_id` |
| `g-hk-validate-shell.ps1` | Pre-tool-use (Shell) | Validates shell commands are safe before execution |

---

## Hook Event Types

Hooks subscribe to specific IDE events:

| Event | When It Fires |
|-------|--------------|
| `preToolUse` | Before a tool call (Shell, Read, etc.) |
| `postToolUse` | After a tool call completes |
| `agentComplete` | When the AI finishes its turn |
| `sessionStart` | When a new chat session begins |

---

## Hook Configuration

Hooks are configured in `hooks.json` in each IDE's configuration folder:

- Cursor: `.cursor/hooks.json`
- Claude Code: `.claude/hooks.json`

Example `hooks.json`:
```json
{
  "hooks": [
    {
      "event": "sessionStart",
      "script": ".cursor/hooks/g-hk-session-start.ps1"
    },
    {
      "event": "agentComplete",
      "script": ".cursor/hooks/g-hk-agent-complete.ps1"
    },
    {
      "event": "preToolUse",
      "matcher": "Shell",
      "script": ".cursor/hooks/g-hk-validate-shell.ps1"
    }
  ]
}
```

---

## Logs

Hook-generated logs are written to `.galdr/logs/` with a date prefix:

```
.galdr/logs/YYYY-MM-DD_agent-audit.log
.galdr/logs/YYYY-MM-DD_shell_commands.log
```

These logs are excluded from git by `.galdr/.gitignore`.

---

## Adding Custom Hooks

1. Create a new `.ps1` file in `.cursor/hooks/` named `g-hk-{your-name}.ps1`
2. Add the hook entry to `.cursor/hooks.json`
3. For cross-IDE parity, copy to `.claude/hooks/`, `.agent/hooks/`, `.codex/hooks/`

---

## Platform Support

| Platform | Hook Support | Config File |
|----------|-------------|-------------|
| Cursor | Full | `.cursor/hooks.json` |
| Claude Code | Full | `.claude/hooks.json` |
| Gemini | Partial | `.agent/hooks/` |
| Codex | Partial | `.codex/hooks/` |
| OpenCode | Limited | `.opencode/` |
