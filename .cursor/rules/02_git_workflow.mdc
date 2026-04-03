---
description: "Git workflow conventions — commit message format and branch standards"
globs:
alwaysApply: false
---

# Git Workflow

## Commit Message Format
```
{type}({scope}): {brief description}

{optional body}

Task: #{id}
Phase: {N}
```

## Commit Types
| Type | Use For |
|---|---|
| `feat` | New feature or task |
| `fix` | Bug fix |
| `refactor` | Code refactor, no behavior change |
| `docs` | Documentation only |
| `test` | Tests only |
| `chore` | Config, build, maintenance |
| `phase` | Phase completion commit |

## Rules
- Subject line ≤ 72 characters
- Use imperative mood: "add" not "added" or "adds"
- Reference task ID in every task-related commit
- Never commit secrets, API keys, or passwords
- Run `git status` before committing to verify staged files

## Protected Files (NEVER commit these)

Before every `git add` or `git commit`, verify NONE of these are staged:

| Pattern | Why |
|---|---|
| `/.agent/` | Personal IDE config (gitignored) |
| `/.claude/` | Personal IDE config (gitignored) |
| `/.codex/` | Personal IDE config (gitignored) |
| `/.cursor/` | Personal IDE config (gitignored) |
| `/.opencode/` | Personal IDE config (gitignored) |
| `/.galdr/` | Live project state (gitignored) |
| `/.galdr_template/` | Root-level template copy (gitignored) |
| `/temp_docs/` | Scratch files (gitignored) |
| `/temp_scripts/` | Scratch files (gitignored) |
| `/AGENTS.md` | Personalized per-user (gitignored) |
| `/CLAUDE.md` | Personalized per-user (gitignored) |
| `/GEMINI.md` | Personalized per-user (gitignored) |
| `/GUARDRAILS.md` | Personalized per-user (gitignored) |
| `/.env` | Secrets (gitignored) |
| `/.mcp.json` | Machine-specific MCP config (gitignored) |

If `git status` shows ANY of these as staged or untracked-to-be-added:
1. **STOP** — do not commit
2. Remove from staging: `git reset HEAD <file>`
3. Verify `.gitignore` still contains the entry
4. Warn the user that a protected file was almost committed

## Branch Naming
- Feature: `feature/{task-id}-brief-description`
- Bug fix: `fix/{bug-id}-brief-description`
- Release: `release/v{major}.{minor}.{patch}`

## Windows (PowerShell)
```powershell
$msg = "feat(api): implement auth`n`nTask: #103`nPhase: 1"
git commit -m $msg
```
