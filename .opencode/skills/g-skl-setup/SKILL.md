---
name: g-skl-setup
description: Initialize galdr in a project — folder structure and template files for task management.
---
# galdr-setup

## When to Use
First-time setup of galdr in a project. @g-setup command.

## Slim vs Full — Know Which You Are Installing

**This skill creates the SLIM layout.** Do not create the folders marked "full only" below.

| Folder | Slim | Full (galdr_full only) |
|--------|------|------------------------|
| `tasks/`, `bugs/`, `prds/`, `subsystems/`, `reports/`, `logs/` | ✅ | ✅ |
| `config/` (HEARTBEAT.md, SPRINT.md, AGENT_CONFIG.md) | ❌ | ✅ |
| `experiments/` (EXPERIMENTS.md, HYPOTHESIS.md, SELF_EVOLUTION.md) | ❌ | ✅ |
| `linking/` (README.md, INBOX.md) | ❌ | ✅ |
| `vault/` | ❌ | ✅ |
| `phases/` (legacy v2) | ❌ | ✅ |

## Steps

1. **Detect if existing** (check before creating anything):
   ```
   □ .galdr/TASKS.md exists AND > 20 lines?
   □ .galdr/tasks/ has > 5 files?
   □ PROJECT.md has non-template content?
   → YES: EXISTING project → ask: Merge / Skip / Reset (DESTRUCTIVE)
   → NO: FRESH install → proceed
   ```

2. **Call galdr_install MCP tool** (if available):
   ```python
   galdr_install(project_path="{absolute_path}", use_v2=True)
   ```

3. **If galdr_install unavailable**, create manually:
   - Folders: `.galdr/`, `.galdr/tasks/`, `.galdr/prds/`, `.galdr/bugs/`, `.galdr/subsystems/`, `.galdr/reports/`, `.galdr/logs/`, `.galdr/specifications_collection/`
   - Create `.galdr/specifications_collection/README.md` with the index template (see template in `template_full/.galdr/specifications_collection/README.md`)
   - Create `.galdr/learned-facts.md` from the template in `template_full/.galdr/learned-facts.md`
   - If `.galdr/.identity` contains `vault_location`, create `{vault_location}/log.md` as a seed file (one header line — `append_log()` will populate it on first ingest)
   - If `.galdr/.identity` contains `vault_location`, create `{vault_location}/projects/{project_name}/` directory; this is where `repos.txt` and `repo_tracker.json` will live when `github_sync.py` runs
   - If `.galdr/.identity` contains `vault_location` **and** `{vault_location}/obsidian_setup.md` does not already exist, copy `template_full/.galdr/vault/obsidian_setup.md` (or the installed equivalent at `{skill_root}/reference/obsidian_setup.md`) to `{vault_location}/obsidian_setup.md`. This seeds the one-page Obsidian setup guide so vault users can find it immediately.
   - **Research-type projects:** when creating `TASKS.md`, add a research log section below the task list
   - Files: Use g-project (CREATE PROJECT.MD) and g-plan (CREATE PLAN.MD) for all file generation

4. **Generate .identity**:
   ```bash
   python -c "import uuid; print(uuid.uuid4())" > .galdr/.identity
   ```

5. **Verify structure** (slim v3 layout — ground truth from G:\galdr\.galdr):
   ```
   .galdr/ ✅
   ├── .identity ✅
   ├── .gitignore ✅
   ├── TASKS.md ✅
   ├── PLAN.md ✅                 ← master strategy (above PRDs)
   ├── PROJECT.md ✅             ← mission, goals, Project Linking
   ├── CONSTRAINTS.md ✅         ← non-negotiable constraints
   ├── BUGS.md ✅                ← bug index (root)
   ├── SUBSYSTEMS.md ✅
   ├── IDEA_BOARD.md ✅
   ├── PRDS.md ✅                ← PRD index
   ├── learned-facts.md ✅       ← agent-captured learning (updated via /g-learn)
   ├── prds/ ✅                  ← individual PRD files
   ├── bugs/ ✅                  ← optional per-bug detail files
   ├── reports/ ✅
   ├── logs/ ✅
   ├── subsystems/ ✅            ← per-subsystem spec files
   ├── specifications_collection/ ✅  ← incoming specs from stakeholders
   └── tasks/ ✅
   docs/ ✅
   ```

   > **NOT in slim:** `config/`, `experiments/`, `linking/`, `vault/`, `phases/`
   > These belong in `galdr_full` only. Do not create them here.

6. **Create PROJECT.MD scaffolding**:
   - `.galdr/PROJECT.md` — include a **Project Linking** section (parents, children, siblings); starts with `relationships: none`

7. **Subsystem Discovery** (run after folder creation):
   Scan the project to identify subsystems. For each, create a spec file in `.galdr/subsystems/`:
   
   **What to scan:**
   - Top-level directories and `src/` subdirectories → candidate subsystems
   - Database schema files → table groups suggest subsystems
   - Config files → each config suggests a consuming subsystem
   - API route files → each route group suggests a subsystem
   - Docker services → each container is likely its own subsystem
   - External service integrations → integration entries in host subsystem
   
   **For each identified subsystem, create spec with:**
   ```yaml
   locations:
     code: [source file paths]
     skills: [relevant galdr skills]
     agents: [relevant galdr agents]
     commands: [relevant galdr commands]
     config: [config files]
     db_tables: [owned tables]
   ```
   Plus: Responsibility, Data Flow, Architecture Rules, When to Modify sections.
   
   **Classify as:**
   - **Subsystem** (own code + state + lifecycle) → top-level entry + spec file
   - **Sub-feature** (shares parent's code/state) → documented in parent spec
   - **Integration** (external adapter) → listed in host subsystem spec
   
   Update SUBSYSTEMS.md with the index table, sub-features table, integrations table, and mermaid interconnection graph.

8. **Print next steps**:
   - Review `.galdr/PROJECT.md` and confirm mission and goals
   - Review SUBSYSTEMS.md and adjust detected components
   - Review subsystem spec files in `.galdr/subsystems/` for accuracy
   - Create first task with @g-tasks (CREATE) (sequential task IDs)
   - Draft or refine `.galdr/PLAN.md` and PRDs under `prds/` as needed
   - Declare cross-project relationships in **Project Linking** (`@g-project (Project Linking section)`) when ready
   - **Optional**: Install domain-specific skill packs from `skill_packs/` directory — run `.\skill_packs\{pack}\install.ps1` for infrastructure, ai-ml-dev, startup-tools, and other packs
