# Cursor IDE Structure Reference

**Last verified**: 2026-02-19
**Source**: https://docs.cursor.com/context/rules

## Self-Update Instructions

This file should be periodically refreshed by fetching the official docs listed below. When this skill is invoked, check if `Last verified` is older than 30 days — if so, re-fetch and update.

### Official Doc URLs to Fetch

| URL | Section to Extract |
|---|---|
| https://docs.cursor.com/context/rules | Rule format, .mdc schema, new features |
| https://docs.cursor.com/context/context-types | Context types, file handling |
| https://docs.cursor.com/chat/agents | Agent mode, capabilities |
| https://docs.cursor.com/context/model-context-protocol | MCP config format |
| https://docs.cursor.com/troubleshooting/troubleshooting | Known issues |

## Known File Structure (as of 2026-02-19)

### Project-Level Files
- `.cursorrules` — Legacy single-file rules (deprecated)
- `.cursor/mcp.json` — MCP server config
- `.cursor/rules/*.mdc` — Numbered rule files with YAML frontmatter
- `.cursor/rules/README.md` — Numbering convention docs
- `.cursor/agents/*.md` — Agent definitions with YAML frontmatter
- `.cursor/commands/*.md` — Slash commands with $ARGUMENTS
- `.cursor/skills/*/SKILL.md` — Skills with optional reference/, scripts/, assets/

### NOT Natively Supported by Cursor
- Hooks / lifecycle automation
- Granular tool permissions
- Auto-memory / MEMORY.md
- Persistent agent memory
- Personal overrides (local.json)
- Managed/IT-enforced settings
- Git worktree integration

## .mdc Frontmatter Schema

```yaml
description: string (required)  — Rule picker text
globs: array (optional)         — File patterns for auto-activation
alwaysApply: boolean (required) — true = always loaded
```

## Agent Frontmatter Schema

```yaml
name: string (required)         — kebab-case identifier
description: string (required)  — One-line purpose
tools: string (required)        — Comma-separated tool list
model: string (required)        — sonnet, opus, haiku
```

## Skill Frontmatter Schema

```yaml
name: string (required)         — Skill identifier
description: string (required)  — When/how to use
triggers: array (optional)      — Auto-activation keywords
agents: array (optional)        — Which agents use this skill
version: string (optional)      — Semantic version
```

## MCP Config Format

```json
{
  "mcpServers": {
    "name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": { "KEY": "value" }
    }
  }
}
```

## Rule Numbering Convention

00-09: Universal | 10-19: App core | 20-29: Reserved | 30-39: Platform
40-49: Database | 50-59: DevOps | 60-69: Business | 70-79: Workflows | 80-89: Domain

## Context Budget

Total ~200K tokens. Rules <2%. Skills lazy-loaded. Keep files <100 lines.
