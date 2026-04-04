# Galdr Component Naming Convention

**Date**: 2026-04-04
**From**: galdr (slim / source repo)
**Applies to**: galdr_full, galdr_mcp, galdr_forge, and any project using galdr

---

## The Convention

Every galdr component file carries a type prefix so you can instantly identify what something is — in a file tree, in a grep result, or when reading the body of another file.

| Type | Pattern | Example |
|---|---|---|
| Skill | `g-skl-{name}/SKILL.md` | `g-skl-tasks/SKILL.md` |
| Agent | `g-agnt-{name}.md` | `g-agnt-task-manager.md` |
| Command | `g-{name}.md` | `g-task-new.md` |
| Rule | `g-rl-{nnn}-{name}.mdc` | `g-rl-25-galdr_session_start.mdc` |
| Hook | `g-hk-{name}.ps1` | `g-hk-session-start.ps1` |

**Commands get no type prefix** — they are the user-facing entry point. Users type `@g-task-new`. Adding `@g-cmd-task-new` would break muscle memory for no benefit. Everything else is internal and benefits from the prefix.

---

## Why

Before this convention, the same name could mean different things depending on where you looked:
- `g-code-reviewer` was both a skill folder AND an agent file
- Reading a skill body saying "activate g-qa-engineer" — is that a skill or an agent?
- Trying to find all galdr hooks in a project required knowing which `.ps1` files were galdr vs project-owned

Now:
- `g-skl-` in a path → skill
- `g-agnt-` in a path → agent
- `g-rl-` in a path → rule
- `g-hk-` in a path → hook
- `g-` alone → command

---

## What Was Renamed in galdr (slim)

### Skills: `g-{name}/` → `g-skl-{name}/`

| Old | New |
|---|---|
| `g-bugs/` | `g-skl-bugs/` |
| `g-code-reviewer/` | `g-skl-code-review/` *(also merged g-review into this)* |
| `g-dependency-graph/` | `g-skl-dependency-graph/` |
| `g-git-commit/` | `g-skl-git-commit/` |
| `g-ideas/` | `g-skl-ideas/` |
| `g-medkit/` | `g-skl-medkit/` |
| `g-plan/` | `g-skl-plan/` |
| `g-project/` | `g-skl-project/` |
| `g-qa/` | `g-skl-qa/` |
| `g-review/` | *(deleted — merged into g-skl-code-review)* |
| `g-setup/` | `g-skl-setup/` |
| `g-sprint/` | `g-skl-sprint/` |
| `g-status/` | `g-skl-status/` |
| `g-subsystems/` | `g-skl-subsystems/` |
| `g-swot-review/` | `g-skl-swot-review/` |
| `g-tasks/` | `g-skl-tasks/` |
| `g-verify-ladder/` | `g-skl-verify-ladder/` |

### Agents: `g-{name}.md` → `g-agnt-{name}.md`

| Old | New |
|---|---|
| `g-code-reviewer.md` | `g-agnt-code-reviewer.md` |
| `g-ideas-goals.md` | `g-agnt-ideas-goals.md` |
| `g-infrastructure.md` | `g-agnt-infrastructure.md` |
| `g-planner.md` | `g-agnt-planner.md` |
| `g-project-initializer.md` | `g-agnt-project-initializer.md` |
| `g-project-manager.md` | `g-agnt-project-manager.md` |
| `g-qa-engineer.md` | `g-agnt-qa-engineer.md` |
| `g-task-manager.md` | `g-agnt-task-manager.md` |
| `g-verifier.md` | `g-agnt-verifier.md` |

### Rules: `{nnn}_{name}.mdc` → `g-rl-{nnn}-{name}.mdc`

| Old | New |
|---|---|
| `00_always.mdc` | `g-rl-00-always.mdc` |
| `01_documentation.mdc` | `g-rl-01-documentation.mdc` |
| `02_git_workflow.mdc` | `g-rl-02-git_workflow.mdc` |
| `04_code_reusability.mdc` | `g-rl-04-code_reusability.mdc` |
| `08_powershell.mdc` | `g-rl-08-powershell.mdc` |
| `09_python_venv.mdc` | `g-rl-09-python_venv.mdc` |
| `25_galdr_session_start.mdc` | `g-rl-25-galdr_session_start.mdc` |
| `33_enforcement_catchall.mdc` | `g-rl-33-enforcement_catchall.mdc` |
| `34_todo_completion_gate.mdc` | `g-rl-34-todo_completion_gate.mdc` |

**Exception**: `norse_personality.mdc` — project-specific personality rule, no prefix, excluded from parity audits. Same treatment applies to `silicon_valley_personality.mdc` or any other personality variant.

### Hooks: `{name}.ps1` → `g-hk-{name}.ps1`

| Old | New |
|---|---|
| `session-start.ps1` | `g-hk-session-start.ps1` |
| `agent-complete.ps1` | `g-hk-agent-complete.ps1` |
| `validate-shell.ps1` | `g-hk-validate-shell.ps1` |
| `g-setup-user.ps1` | `g-hk-setup-user.ps1` |

### Commands: unchanged

Commands keep `g-{name}.md`. No type prefix.

---

## What galdr_full Needs to Do

### Step 1: Map your current files

Run this in each IDE folder to see what needs renaming:

```powershell
# Skills not yet renamed
Get-ChildItem ".cursor\skills" -Directory | Where-Object { $_.Name -match '^g-(?!skl-)' }

# Agents not yet renamed
Get-ChildItem ".cursor\agents" -File -Filter "*.md" | Where-Object { $_.Name -match '^g-(?!agnt-)' -and $_.Name -ne "README.md" }

# Rules not yet renamed
Get-ChildItem ".cursor\rules" -File | Where-Object { $_.Name -match '^\d+_' }

# Hooks not yet renamed
Get-ChildItem ".cursor\hooks" -File -Filter "*.ps1" | Where-Object { $_.Name -notmatch '^g-hk-' }
```

### Step 2: Rename skills

```powershell
cd {your-repo}
Get-ChildItem ".cursor\skills" -Directory | ForEach-Object {
    $old = $_.Name
    if ($old -match '^g-(?!skl-)') {
        $base = $old -replace '^g-', ''
        Rename-Item $_.FullName "g-skl-$base"
        Write-Output "Renamed: $old → g-skl-$base"
    }
}
```

Repeat the same pattern for `.claude\skills`, `.agent\skills`, `.codex\skills`.

### Step 3: Rename agents

```powershell
Get-ChildItem ".cursor\agents" -File -Filter "*.md" | Where-Object { $_.Name -ne "README.md" } | ForEach-Object {
    $old = $_.Name
    if ($old -match '^g-(?!agnt-)') {
        $base = $_.BaseName -replace '^g-', ''
        Rename-Item $_.FullName "g-agnt-$base.md"
        Write-Output "Renamed: $old → g-agnt-$base.md"
    }
}
```

Repeat for `.claude\agents`, `.agent\agents`, `.codex\agents`.

### Step 4: Rename rules

```powershell
Get-ChildItem ".cursor\rules" -File | Where-Object { $_.Name -match '^\d+_' } | ForEach-Object {
    if ($_.Name -match '^(\d+)_(.+)\.mdc$') {
        $num = $matches[1]; $base = $matches[2]
        Rename-Item $_.FullName "g-rl-$num-$base.mdc"
        Write-Output "Renamed: $($_.Name) → g-rl-$num-$base.mdc"
    }
}
```

For `.claude\rules` and `.agent\rules`, same logic but output is `.md` not `.mdc`.

### Step 5: Rename hooks

```powershell
Get-ChildItem ".cursor\hooks" -File -Filter "*.ps1" | Where-Object { $_.Name -notmatch '^g-hk-' } | ForEach-Object {
    $base = $_.BaseName -replace '^g-', ''
    Rename-Item $_.FullName "g-hk-$base.ps1"
    Write-Output "Renamed: $($_.Name) → g-hk-$base.ps1"
}
```

Repeat for all other IDE hooks folders. Also update `hooks.json` in each IDE folder to reference the new filenames.

### Step 6: Update internal references

After renaming, do a find-and-replace pass across all skill, agent, command, rule, and hook files:

Key replacements (adapt to your full skill/agent list):
```powershell
# Example pattern — run across all .md/.mdc/.ps1 files in all IDE folders
$content = $content -replace '\bg-tasks\b(?!/)', 'g-skl-tasks'
$content = $content -replace '\bg-bugs\b(?!/)', 'g-skl-bugs'
# ... repeat for each skill
$content = $content -replace '\bg-task-manager\.md\b', 'g-agnt-task-manager.md'
# ... repeat for each agent
$content = $content -replace 'session-start\.ps1', 'g-hk-session-start.ps1'
# ... repeat for each hook
```

### Step 7: Update AGENTS.md / CLAUDE.md skills and agents registry tables

The "Available Skills" and "Available Agents" tables in your `AGENTS.md` and `CLAUDE.md` still list old names. Update those tables to reflect the new `g-skl-` and `g-agnt-` prefixes.

### Step 8: Propagate

galdr_full has 9 targets (vs slim's 5):
1. `.cursor/`
2. `.claude/`
3. `.agent/`
4. `.codex/`
5. `.opencode/` (reads `.claude/skills/` natively — commands only)
6. `templates/.cursor/`
7. `templates/.claude/`
8. `templates/.agent/`
9. `templates/.codex/`

Run `scripts/sync-parity.ps1 -Fix` to automate cross-target propagation after renaming `.cursor/` as the source of truth.

---

## galdr_full-Specific Notes

### Extra skills to rename

galdr_full has skills that don't exist in slim. Apply the same pattern:

```
g-vault/            → g-skl-vault/
g-experiment/       → g-skl-experiment/
g-heartbeat/        → g-skl-heartbeat/
g-platform-crawl/   → g-skl-platform-crawl/
g-broadcast/        → g-skl-broadcast/
g-inbox/            → g-skl-inbox/
g-peer-sync/        → g-skl-peer-sync/
g-request/          → g-skl-request/
g-graph/            → g-skl-graph/
g-harvest/          → g-skl-harvest/
g-kpi/              → g-skl-kpi/
g-swarm/            → g-skl-swarm/
... (all g-* skill folders)
```

### Extra agents to rename

```
g-memory.md             → g-agnt-memory.md
g-autonomous.md         → g-agnt-autonomous.md
g-multi-agent.md        → g-agnt-multi-agent.md
g-self-improvement.md   → g-agnt-self-improvement.md
g-workflow-manager.md   → g-agnt-workflow-manager.md
g-codebase-analyst.md   → g-agnt-codebase-analyst.md
... (all g-*.md agent files)
```

### Phase skills in galdr_full

galdr_full still has phase micro-skills (`g-phase-add`, `g-phase-pivot`, etc.). Per the separate skill consolidation plan, these are being folded into `g-skl-plan` as named operations. If that consolidation hasn't happened yet, rename them first (`g-phase-add` → `g-skl-phase-add`), then merge into `g-skl-plan` as a second step.

---

## Alignment Guarantee

The slim galdr and galdr_full must stay naming-aligned so projects can upgrade without breakage. The rule is simple:

**Any skill, agent, rule, or hook that exists in both slim and full must have the same name after the prefix.** The prefix is always `g-skl-`, `g-agnt-`, `g-rl-`, or `g-hk-`. The base name never changes between tiers.

```
slim:  g-skl-tasks    ←→  full: g-skl-tasks     ✅
slim:  g-agnt-verifier ←→  full: g-agnt-verifier  ✅
slim:  g-skl-vault     ←→  full: g-skl-vault       ✅ (full-only, slim has no vault)
```
