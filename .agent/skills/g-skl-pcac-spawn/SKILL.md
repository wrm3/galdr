---
name: g-skl-pcac-spawn
description: >
  Spawn a new galdr project from the current project. Creates the new project folder
  in the same ecosystem root, installs galdr (matching the current project's install
  type — symlinks or fresh template), seeds it with any passed description/features/code,
  runs galdr-setup, and immediately links both projects via PCAC topology
  (--parent | --sibling | --child).
---

# g-skl-pcac-spawn

**File Owner**: none (creates a new project; source project's topology is updated in place)

**Activate for**: "spawn a new project", "create a new child/sibling/parent project", "extract this into its own repo", "new project from features", `@g-pcac-spawn`

---

## When to Use

When a part of the current project has grown large enough to warrant its own separately
maintained repository, but it currently lives inside this project (as code, features,
specifications, or ideas). This skill orchestrates the full lifecycle:

1. Create the new project folder in the ecosystem root
2. Install galdr (matching current project's install style)
3. Seed the new project with passed context (description, features, code, etc.)
4. Run galdr-setup subsystem discovery in the new project
5. Register PCAC topology link in both projects

---

## Command Syntax

```
@g-pcac-spawn <new_project_name> --sibling [options]
@g-pcac-spawn <new_project_name> --child [options]
@g-pcac-spawn <new_project_name> --parent [options]

Options:
  --description "..."          One-line mission statement for the new project
  --features <subfolder>       Path (relative or absolute) to a features/ subfolder to transfer
  --code <path>                Path to code folder(s) to copy into the new project
  --template slim|full|adv     Which galdr template tier to install (default: matches current)
  --dry-run                    Show what would be created without touching anything
```

**Examples**:
```
@g-pcac-spawn galdr_valhalla --sibling --description "Single-user Docker backend for galdr" --features .galdr/features/galdr_backend
@g-pcac-spawn galdr_payments --child --description "Payment processing subsystem" --code src/payments/
@g-pcac-spawn galdr_platform --parent --description "Platform coordination layer"
```

---

## Pre-Flight Checks

Before doing anything, validate:

```
□ Current project has .galdr/.identity (galdr is installed here)
□ Current project has .galdr/linking/link_topology.md (PCAC is initialized)
□ new_project_name does not already exist in the ecosystem root
□ If --features: the specified path exists and contains at least one .md file
□ If --code: the specified path exists
□ relationship (--sibling/--child/--parent) is specified
```

If `--dry-run`: print a full preview and stop. Do not create anything.

If any non-dry-run check fails → stop and report with fix instructions.

---

## Steps

### Step 0 — Determine ecosystem root

```
Read: .galdr/.identity → project_path
Ecosystem root = parent directory of project_path
Example: G:\galdr_ecosystem\galdr_full → root is G:\galdr_ecosystem\
New project path = <ecosystem_root>\<new_project_name>
```

### Step 1 — Detect current project's galdr install style

```
Check if .cursor/rules/ contains symlinks → PowerShell: (Get-Item .cursor/rules/g-rl-00-always.mdc).LinkType
  "SymbolicLink" → style = "symlink"
  $null or "" → style = "copy"

Check which template tier:
  If template_full/.galdr/ exists in current project → tier = "full"
  Else read .galdr/.identity for galdr_version hints or assume "slim"
```

Store: `$install_style`, `$template_tier` (overridden by `--template` if provided)

### Step 2 — Create new project folder structure

```powershell
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr\tasks"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr\features"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr\bugs"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr\subsystems"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr\reports"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr\logs"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\.galdr\linking"
New-Item -ItemType Directory -Path "<ecosystem_root>\<new_project_name>\docs"
```

Create git repo:
```powershell
cd "<ecosystem_root>\<new_project_name>"
git init
```

### Step 3 — Install galdr (matching style)

**If style = "symlink"**:
  - Determine the symlink target root (usually the galdr_full template path)
  - Create `.cursor/rules/` symlinks pointing to `template_full/.cursor/rules/`
  - Create `.claude/` symlinks or copies as appropriate
  - Create `.cursor/skills/` symlinks pointing to template skills

**If style = "copy"** (default safe path):
  - Read `galdr_full/.galdr/.identity` → locate `template_slim/` or `template_full/` path
  - Copy `.cursor/rules/` from the appropriate template tier
  - Copy `.claude/skills/` from `galdr_full/.claude/skills/` (all PCAC and core skills)
  - Copy `AGENTS.md`, `CLAUDE.md` from the appropriate template or galdr_full root

**In both cases**, create `.galdr/.identity`:
```
project_id=<generate new UUID>
project_name=<new_project_name>
user_id=<copy from current project's .identity>
user_name=<copy from current project's .identity>
galdr_version=<copy from current project's .identity>
vault_location=<copy from current project's .identity>
repos_location=<copy from current project's .identity>
```

### Step 4 — Seed with passed description

Create `.galdr/PROJECT.md` using the `g-skl-project` scaffold, with:
- **Mission**: `--description` value (or `"[PENDING — set mission before starting work]"` if not provided)
- **Project Linking** section pre-populated with the relationship to the spawning project
- **Origin note**: `> Spawned from: <current_project_name> on <YYYY-MM-DD>`

Create `.galdr/PLAN.md`, `TASKS.md`, `FEATURES.md`, `BUGS.md`, `SUBSYSTEMS.md`, `IDEA_BOARD.md`,
`CONSTRAINTS.md` from slim templates (empty, numbered headers only).

### Step 5 — Transfer features (if --features provided)

**Source**: `<current_project>/<features_subfolder>/` (e.g. `.galdr/features/galdr_backend/`)
**Destination**: `<new_project>/.galdr/features/`

```powershell
Copy-Item -Path "<source_features_path>\*" -Destination "<new_project>/.galdr/features/" -Recurse -Force
```

- Copy ALL files/subfolders in the specified features path
- Do NOT delete source yet (Step 11 handles that, after confirmation)
- Update FEATURES.md in the new project: parse copied feat-NNN_*.md files, build the index table

Log in source project's `.galdr/vault/log.md`:
```markdown
## <YYYY-MM-DD> — Spawn: features transferred to <new_project_name>
- source_path: <features_subfolder>
- dest_project: <new_project_name>
- file_count: N
- status: copied (originals kept pending confirmation)
```

### Step 6 — Transfer code (if --code provided)

```powershell
Copy-Item -Path "<source_code_path>" -Destination "<new_project>/<same_relative_subpath>" -Recurse -Force
```

- Mirror the directory structure (e.g., `src/payments/` → `<new_project>/src/payments/`)
- Do NOT delete source yet
- Log in vault/log.md

### Step 7 — Run galdr-setup subsystem discovery in new project

Follow `g-skl-setup` Step 7 (Subsystem Discovery) scoped to the new project's contents:
- Scan code folders (if transferred)
- Scan features/ for subsystem hints
- Create `.galdr/subsystems/` spec files
- Update `.galdr/SUBSYSTEMS.md`

### Step 8 — Initialize PCAC linking in new project

Create `.galdr/linking/link_topology.md` in the new project:

```yaml
---
project_id: "<new UUID>"
project_name: "<new_project_name>"
project_path: "<ecosystem_root>\<new_project_name>"
role: "<sibling | child | parent>"
description: "<--description value>"
parent: {}         # populated below if --child
children: []       # populated below if --parent
siblings: []       # populated below if --sibling
last_updated: "<YYYY-MM-DD>"
---
```

Set relationships:
- `--sibling`: add current project to `siblings[]`; set `role: sibling`
- `--child`: add current project to `parent:`; set `role: child`
- `--parent`: add current project to `children[]`; set `role: parent`

Create `.galdr/linking/INBOX.md`:
```markdown
# INBOX — <new_project_name>

> Cross-project coordination inbox. Maintained by PCAC skills.
> Format: [OPEN] | [ACTIONED] | [CLOSED]

---

## [INFO] Project spawned from <current_project_name> — <YYYY-MM-DD>
**Source**: <current_project_name>
**Relationship**: <sibling | child | parent>
**Seeded with**: <description | features: N files | code: N folders>
**Next step**: Review .galdr/PROJECT.md, curate features, and run @g-tasks to plan first sprint.
```

### Step 9 — Update current project's topology

Update `<current_project>/.galdr/linking/link_topology.md`:

- `--sibling`: add new project to `siblings[]`
- `--child`: add new project to `children[]`
- `--parent`: set new project as `parent:`, update `role: child`

Update `last_updated` to today.

Write `<current_project>/.galdr/linking/peers/<new_project_name>.md`:
```markdown
# Peer: <new_project_name>
relationship: <sibling | child | parent>
project_path: <ecosystem_root>\<new_project_name>
project_id: <new UUID>
spawned_from_here: true
spawned_date: <YYYY-MM-DD>
```

### Step 10 — Initial git commit in new project

```powershell
cd "<new_project>/"
git add -A
git commit -m "feat: galdr scaffold — spawned from <current_project_name> <YYYY-MM-DD>"
```

### Step 11 — Ask about source cleanup

```
New project <new_project_name> is ready at:
  <ecosystem_root>\<new_project_name>

If you transferred features: the originals are still at <source_features_path>.
Delete source features from <current_project_name>? [yes / no / keep for now]
```

If "yes":
- Delete source feature files/folder
- Update `<current_project>/.galdr/FEATURES.md` to remove or stub the transferred features
- Add forwarding comment in FEATURES.md: `> [transferred to <new_project_name> — <YYYY-MM-DD>]`

If code was transferred and source delete confirmed:
- Delete source code folder
- Add forwarding stub at source path

### Step 12 — Final report

```
✅ SPAWN COMPLETE
  New project  : <new_project_name>
  Path         : <ecosystem_root>\<new_project_name>
  galdr        : installed (<style>/<tier>)
  Features     : N files transferred (originals: kept | deleted)
  Code         : N folders transferred (originals: kept | deleted)
  Topology     : linked as <sibling | child | parent> of <current_project_name>
  Git          : initial commit created

Next steps:
  1. Open <new_project_name> in a new IDE window
  2. Review .galdr/PROJECT.md — confirm mission and goals
  3. Curate transferred features (prioritize, merge, assign to subsystems)
  4. Run @g-tasks to plan first sprint
  5. (Optional) Run @g-pcac-order from <current_project_name> to push initial tasks down
```

---

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| Folder already exists at target path | Stop: "Path already exists: <path>. Use a different name or delete the existing folder." |
| No galdr in current project | Stop: "No .galdr/.identity found. Run @g-setup first." |
| No PCAC in current project | Create `.galdr/linking/` in current project; initialize topology; then proceed |
| --features path doesn't exist | Stop: "Features path not found: <path>" |
| --features path is empty | Warn: "No .md files found in <path>. Proceeding without feature transfer." |
| galdr_install MCP available | Prefer calling `galdr_install(project_path=..., use_v2=True)` in Step 3 over manual copy |
| Symlink detection fails | Default to "copy" style (safe fallback) |
| Git init fails | Warn but continue — git can be initialized manually |

---

## Topology Relationship Guide

| Flag | New project role | Current project role becomes |
|------|-----------------|------------------------------|
| `--sibling` | sibling of current | adds new project to siblings[] |
| `--child` | child (current is parent) | adds new project to children[] |
| `--parent` | parent (current becomes child) | sets new project as parent |

---

## Notes on galdr Install Detection

The skill should check in this order:
1. If `galdr_install` MCP tool responds → use it (preferred)
2. If `template_full/` exists in current project → use as copy source
3. If current project has `.cursor/rules/` symlinks → replicate symlink structure
4. Fallback: copy `.cursor/rules/` and `.claude/skills/` from galdr_full if path is known

The goal is that the spawned project has the same level of galdr tooling as the project
that spawned it — no orphaned child left without proper skill coverage.
