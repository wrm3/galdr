# Claude Code Structure Reference

**Last verified**: 2026-02-19
**Source**: https://docs.anthropic.com/en/docs/claude-code/overview

## Self-Update Instructions

This file should be periodically refreshed by fetching the official docs listed below and updating this content. When this skill is invoked, check if `Last verified` is older than 30 days — if so, re-fetch and update.

### Official Doc URLs to Fetch

| URL | Section to Extract |
|---|---|
| https://docs.anthropic.com/en/docs/claude-code/overview | Feature list, new capabilities |
| https://docs.anthropic.com/en/docs/claude-code/settings | settings.json schema, new fields |
| https://docs.anthropic.com/en/docs/claude-code/hooks | Hook events, hook types |
| https://docs.anthropic.com/en/docs/claude-code/sub-agents | Agent frontmatter fields |
| https://docs.anthropic.com/en/docs/claude-code/skills | Skill format, new features |
| https://docs.anthropic.com/en/docs/claude-code/memory | Memory, rules, CLAUDE.md |
| https://docs.anthropic.com/en/docs/claude-code/permissions | Permission patterns |
| https://docs.anthropic.com/en/docs/claude-code/mcp | MCP config format |

## Known File Structure (as of 2026-02-19)

### Project-Level Files
- `CLAUDE.md` — Project instructions (root or .claude/)
- `CLAUDE.local.md` — Personal prefs (gitignored)
- `.mcp.json` — MCP server config (project root)
- `.claude/settings.json` — Project settings
- `.claude/settings.local.json` — Personal overrides (gitignored)
- `.claude/rules/*.md` — Modular instructions (v2.0.64+)
- `.claude/agents/*.md` — Subagent definitions
- `.claude/skills/*/SKILL.md` — Skills with optional resources
- `.claude/commands/*.md` — Legacy commands (deprecated)
- `.claude/agent-memory/{agent}/MEMORY.md` — Persistent memory
- `.claude/worktrees/` — Git worktree sessions (auto)

### User-Level Files
- `~/.claude/settings.json` — User settings
- `~/.claude/CLAUDE.md` — Personal instructions (all projects)
- `~/.claude/keybindings.json` — Keyboard shortcuts
- `~/.claude/.credentials.json` — API credentials
- `~/.claude/rules/` — Personal rules
- `~/.claude/agents/` — Personal agents
- `~/.claude/skills/` — Personal skills
- `~/.claude/projects/{hash}/memory/MEMORY.md` — Auto-memory

### Managed Settings (IT-enforced)
- macOS: `/Library/Application Support/ClaudeCode/`
- Linux: `/etc/claude-code/`
- Windows: `C:\Program Files\ClaudeCode\`

## settings.json Fields

```
permissions.allow          — Array of tool patterns to auto-allow
permissions.ask            — Array of tool patterns requiring confirmation
permissions.deny           — Array of tool patterns to block
permissions.defaultMode    — acceptEdits|askEdits|askTools|denyAll|bypassPermissions
permissions.additionalDirectories — Array of paths outside project
permissions.disableBypassPermissionsMode — disable|enable
env                        — Object of environment variables
hooks                      — Object of hook event arrays
sandbox.enabled            — Boolean
sandbox.autoAllowBashIfSandboxed — Boolean
sandbox.network.allowedDomains — Array of domains
model                      — Default model
availableModels            — Array of allowed models
enableAllProjectMcpServers — Boolean
enabledMcpjsonServers      — Array of server names
disabledMcpjsonServers     — Array of server names
```

## Hook Events (11)

SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, SubagentStart, SubagentStop, Stop, PreCompact, SessionEnd

## Hook Types (3)

command, prompt, agent

## NOT Recognized (Community Only)

SOUL.md, USER.md, AGENTS.md, CONTEXT.md, STYLE.md — must be referenced manually from CLAUDE.md to have any effect.
