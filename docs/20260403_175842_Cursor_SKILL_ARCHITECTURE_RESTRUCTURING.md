# Galdr Skill Architecture — File-Centric Restructuring

**Date**: 2026-04-03
**Author**: galdr-core-team
**Applies to**: galdr (lite), galdr_full, galdr_mcp, galdr_forge, and any project using galdr

---

## Why This Change Was Made

The original galdr skill set grew organically: every time a new operation was needed, a new micro-skill was created (`g-task-new`, `g-task-update`, `g-task-sync-check`, `g-workflow`, `g-bug-report`, `g-bug-fix`, etc.). This created a system that was:

- **Hard to find**: "where do I look when task creation is broken?" — any of 4 skills
- **Hard to maintain**: fixing a task behavior required locating and updating multiple files
- **Hard to extend**: adding a new operation to the task system meant deciding which skill gets it, or creating another micro-skill
- **Disconnected**: skill `g-bug-report` didn't know about `g-bug-fix` even though they shared `BUGS.md`

The new architecture is **file-centric**: every `.galdr/` file or folder has exactly one owning skill that knows everything about that file.

---

## The New Skill Map

Each skill owns one or more `.galdr/` files/folders. When something is wrong with a file, you know exactly which skill to check.

| Skill | Owns | Operations |
|-------|------|------------|
| `g-tasks` | `TASKS.md`, `tasks/` | CREATE, UPDATE STATUS, SYNC CHECK, EXPAND, SPRINT PLAN |
| `g-bugs` | `BUGS.md`, `bugs/` | REPORT BUG, FIX BUG, QUALITY REPORT |
| `g-ideas` | `IDEA_BOARD.md` | CAPTURE, REVIEW, FARM (proactive scan) |
| `g-plan` | `PLAN.md`, `PRDS.md`, `prds/` | CREATE PLAN, CREATE PRD, UPDATE PRD STATUS |
| `g-project` | `PROJECT.md`, `CONSTRAINTS.md` | CREATE/UPDATE PROJECT.MD, CREATE/UPDATE CONSTRAINTS.MD |
| `g-subsystems` | `SUBSYSTEMS.md`, `subsystems/` | DISCOVER, CREATE SPEC, UPDATE ACTIVITY LOG, SYNC CHECK |

---

## What Was Removed

These 12 micro-skills have been consolidated into the 6 skills above:

| Removed Skill | Moved Into |
|---|---|
| `g-task-new` | `g-tasks` → CREATE TASK |
| `g-task-update` | `g-tasks` → UPDATE STATUS |
| `g-task-sync-check` | `g-tasks` → SYNC CHECK |
| `g-workflow` | `g-tasks` → EXPAND + SPRINT PLAN |
| `g-bug-report` | `g-bugs` → REPORT BUG |
| `g-bug-fix` | `g-bugs` → FIX BUG |
| `g-qa-report` | `g-bugs` → QUALITY REPORT |
| `g-idea-capture` | `g-ideas` → CAPTURE |
| `g-idea-review` | `g-ideas` → REVIEW |
| `g-idea-farm` | `g-ideas` → FARM |
| `g-ideas-goals` | `g-ideas` + `g-project` |
| `g-goal-update` | `g-project` → UPDATE PROJECT.MD (Goals) |

---

## Commands Remain — They Now Delegate

Commands (`@g-task-new`, `@g-bug-report`, etc.) still exist. They are now thin wrappers that activate the owning skill's specific operation. Users don't need to change their habits.

```
@g-task-new    → activates g-tasks, CREATE operation
@g-bug-report  → activates g-bugs, REPORT BUG operation
@g-idea-capture → activates g-ideas, CAPTURE operation
@g-goal-update → activates g-project, UPDATE PROJECT.MD (Goals) operation
```

---

## How To Add Something New to the System

**Adding a new `.galdr/` file or folder:**

1. Create the skill directory: `.cursor/skills/g-{name}/`
2. Write `SKILL.md` with:
   - `Files Owned:` header listing exactly what this skill owns
   - `Activate for:` trigger phrases
   - One `## Operation: NAME` section per supported operation
   - File format template(s) at the bottom
3. Propagate to all 4 other IDE targets: `.claude/skills/`, `.agent/skills/`, `.codex/skills/`, `.opencode/skills/` (opencode reads from `.claude/skills/` natively)
4. If it needs a command shortcut: create `.cursor/commands/g-{name}.md` as a thin delegating wrapper, propagate to all command folders

**Adding a new operation to an existing file:**

1. Open the owning skill's `SKILL.md`
2. Add a new `## Operation: NAME` section
3. Propagate the updated skill to all IDE targets
4. Optionally add a command wrapper

**Finding where to look when something is broken:**

| Problem | Skill to check |
|---|---|
| Task creation, status, sync | `g-tasks` |
| Bug logging, bug fixes | `g-bugs` |
| Ideas not capturing | `g-ideas` |
| PRD or plan issues | `g-plan` |
| Goals, constraints | `g-project` |
| Subsystem drift | `g-subsystems` |
| Health check, nightly | `g-cleanup` |
| Initial setup | `g-setup` |
| Placeholder healing, sync | `g-grooming` |

---

## Full Current Skill List (After Restructuring)

| Skill | Role |
|-------|------|
| `g-tasks` | Task CRUD + sprint |
| `g-bugs` | Bug lifecycle + quality |
| `g-ideas` | Idea capture + review |
| `g-plan` | Plans + PRDs |
| `g-project` | Project identity + constraints |
| `g-subsystems` | Subsystem registry + specs |
| `g-setup` | First-time project init |
| `g-grooming` | Health checks + placeholder repair |
| `g-cleanup` | Nightly autonomous maintenance |
| `g-status` | Session context display |
| `g-sprint` | Autonomous 2-hour work sprint |
| `g-review` | Code review |
| `g-code-reviewer` | Deep code quality analysis |
| `g-qa` | QA activation |
| `g-git-commit` | Structured commits |
| `g-dependency-graph` | Task dependency visualization |
| `g-verify-ladder` | Multi-level task verification |
| `g-swot-review` | Weekly SWOT analysis |

---

## Propagation Rule (C-007)

Changes to skills must be propagated to all active IDE targets. There are 5 targets in galdr (lite):

1. `.cursor/skills/` (source)
2. `.claude/skills/`
3. `.agent/skills/`
4. `.codex/skills/`
5. `.opencode/skills/` (or reads from `.claude/skills/` if no native folder)

Use `scripts/sync-parity.ps1 -Fix` in galdr_full/galdr_forge to automate this, or copy manually.

---

## Impact on Sibling Repos

This restructuring should be applied to `galdr_full`, `galdr_mcp`, and `galdr_forge` as well. Steps:

1. Copy the 6 new skill folders from `galdr/.cursor/skills/` → `{repo}/.cursor/skills/`
2. Remove the 12 deprecated micro-skill folders listed in the "What Was Removed" table
3. Update commands in `{repo}/.cursor/commands/` to match the thin-wrapper pattern
4. Propagate to `.claude/`, `.agent/`, `.codex/` within each repo

The new architecture is strictly additive from a user perspective — all existing `@g-task-new`, `@g-bug-report` etc. commands still work unchanged.
