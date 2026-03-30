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

## Branch Naming
- Feature: `feature/{task-id}-brief-description`
- Bug fix: `fix/{bug-id}-brief-description`
- Release: `release/v{major}.{minor}.{patch}`

## Windows (PowerShell)
```powershell
$msg = "feat(api): implement auth`n`nTask: #103`nPhase: 1"
git commit -m $msg
```
