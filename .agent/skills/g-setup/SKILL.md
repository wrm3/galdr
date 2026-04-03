---
name: g-setup
description: Initialize galdr in a project — folder structure and template files for task management.
---
# galdr-setup

## When to Use
First-time setup of galdr in a project. @g-setup command.

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
   - Folders: `.galdr/`, `.galdr/tasks/`, `.galdr/phases/`, `.galdr/prds/`, `.galdr/bugs/`, `.galdr/config/`, `.galdr/experiments/`, `.galdr/reports/`, `.galdr/tracking/`, `.galdr/subsystems/`, `.galdr/linking/`, `docs/`, `temp_scripts/`
   - **Research-type projects:** when creating `.galdr/experiments/`, add **real starter content** to `EXPERIMENTS.md` and `HYPOTHESIS.md` (not empty placeholders only) so the experiment runner and index stay usable from day one.
   - Files: Use galdr-project-manager INITIALIZE mode for all file generation

4. **Generate .identity**:
   ```bash
   python -c "import uuid; print(uuid.uuid4())" > .galdr/.identity
   ```

5. **Verify structure** (v3 layout):
   ```
   .galdr/ ✅
   ├── TASKS.md ✅
   ├── PLAN.md ✅                 ← master strategy (above PRDs)
   ├── PROJECT.md ✅             ← mission, goals, **Project Linking**
   ├── CONSTRAINTS.md ✅         ← non-negotiable constraints
   ├── BUGS.md ✅                ← bug index (root)
   ├── SUBSYSTEMS.md ✅
   ├── .identity ✅
   ├── prds/ ✅                  ← one or more PRD files
   ├── bugs/ ✅                  ← optional per-bug detail files
   ├── config/ ✅
   │   ├── HEARTBEAT.md ✅
   │   ├── SPRINT.md ✅
   │   └── AGENT_CONFIG.md ✅
   ├── experiments/ ✅
   │   ├── EXPERIMENTS.md ✅      ← experiment index / active list
   │   ├── HYPOTHESIS.md ✅
   │   └── SELF_EVOLUTION.md ✅   ← galdr meta-evolution (not SYSTEM_EXPERIMENTS.md)
   ├── reports/ ✅
   │   └── CLEANUP_REPORT.md ✅
   ├── tracking/ ✅
   │   ├── IDEA_BOARD.md ✅
   │   └── INBOX.md ✅           ← cross-project message queue
   ├── subsystems/ ✅            ← per-subsystem spec files
   ├── linking/ ✅             ← shared contract specs
   │   └── README.md ✅
   ├── tasks/ ✅
   └── phases/ ✅                ← optional phase milestone files
   docs/ ✅
   temp_scripts/ ✅
   ```

6. **Create cross-project scaffolding** (if not already present from galdr_install):
   - `.galdr/PROJECT.md` — include a **Project Linking** section (parents, children, siblings); starts with `relationships: none` or equivalent
   - `.galdr/linking/INBOX.md` — empty template with usage comments
   - `.galdr/linking/README.md` — explanation of contracts pattern

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
   - Create first task with @g-task-new (sequential task IDs)
   - Draft or refine `.galdr/PLAN.md` and PRDs under `prds/` as needed
   - Declare cross-project relationships in **Project Linking** (`@g-project-linking`) when ready
