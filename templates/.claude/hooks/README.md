# Claude Code Hooks

This folder contains PowerShell hooks for Claude Code that provide lifecycle management, auditing, and security validation.

## Configuration

Hooks are configured in `.claude/hooks.json`. The configuration defines which scripts run at each lifecycle event.

## Available Hooks

### session-start.ps1
- **Event**: `sessionStart`
- **Purpose**: Initializes session, logs session start, injects galdr context
- **Logs to**: `.claude/logs/{date}_session_lifecycle.log`

### agent-complete.ps1
- **Event**: `stop`
- **Purpose**: Logs when the agent loop ends, records completion metrics
- **Logs to**: `.claude/logs/{date}_agent_lifecycle.log`, `.claude/metrics/{date}_completions.csv`

### audit.ps1
- **Event**: Multiple (preToolUse, postToolUse, afterFileEdit, sessionEnd)
- **Purpose**: Generic audit logging for all events
- **Logs to**: `.claude/logs/{date}_agent-audit.log`

### validate-shell.ps1
- **Event**: `beforeShellExecution`
- **Purpose**: Validates shell commands, blocks dangerous patterns
- **Logs to**: `.claude/logs/{date}_shell_commands.log`
- **Security**: Exit code 2 blocks dangerous commands

## Log File Naming Convention

All log files are prefixed with the date in `yyyy-MM-dd` format for easy cleanup:

```
.claude/
├── logs/
│   ├── 2026-01-26_agent-audit.log       # Today's audit events
│   ├── 2026-01-26_agent_lifecycle.log   # Today's agent events
│   ├── 2026-01-26_session_lifecycle.log # Today's session events
│   ├── 2026-01-26_shell_commands.log    # Today's shell commands
│   ├── 2026-01-25_agent-audit.log       # Yesterday's audit (can delete)
│   └── ...
└── metrics/
    ├── 2026-01-26_completions.csv       # Today's completion metrics
    └── ...
```

### Cleanup Old Logs

To delete logs older than 7 days:

```powershell
# Delete log files older than 7 days
Get-ChildItem ".claude/logs" -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | Remove-Item

# Delete metrics files older than 30 days
Get-ChildItem ".claude/metrics" -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item
```

Or delete by date prefix:

```powershell
# Delete all logs from a specific date
Remove-Item ".claude/logs/2026-01-20_*"
```

## Customization

### Adding Dangerous Command Patterns

Edit `validate-shell.ps1` to add patterns to the `$dangerousPatterns` array:

```powershell
$dangerousPatterns = @(
    "rm -rf /",
    "your-dangerous-pattern-here"
)
```

### Enabling Notifications

Uncomment and configure the notification sections in the hook scripts to send Slack/email alerts.

## Platform Compatibility

These PowerShell hooks work on Windows with Claude Code (VSCode extension and CLI).

| Hook | Purpose |
|------|---------|
| session-start.ps1 | Session initialization |
| agent-complete.ps1 | Agent completion logging |
| audit.ps1 | Generic audit logging |
| validate-shell.ps1 | Shell command validation |
