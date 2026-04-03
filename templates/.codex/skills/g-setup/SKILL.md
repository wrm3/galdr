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
   □ PROJECT_CONTEXT.md has non-template content?
   → YES: EXISTING project → ask: Merge / Skip / Reset (DESTRUCTIVE)
   → NO: FRESH install → proceed
   ```

2. **Call galdr_install MCP tool** (if available):
   ```python
   galdr_install(project_path="{absolute_path}", use_v2=True)
   ```

3. **If galdr_install unavailable**, create manually:
   - Folders: `.galdr/`, `.galdr/tasks/`, `.galdr/phases/`, `.galdr/config/`, `.galdr/project/`, `.galdr/experiments/`, `.galdr/reports/`, `.galdr/tracking/`, `.galdr/subsystems/`, `.galdr/linking/`, `docs/`, `temp_scripts/`
   - Files: Use galdr-project-manager INITIALIZE mode for all file generation

4. **Generate .project_id**:
   ```bash
   python -c "import uuid; print(uuid.uuid4())" > .galdr/.project_id
   ```

5. **Verify structure**:
   ```
   .galdr/ ✅
   ├── TASKS.md ✅
   ├── PRD.md ✅
   ├── SUBSYSTEMS.md ✅
   ├── .project_id ✅
   ├── config/ ✅
   │   ├── HEARTBEAT.md ✅
   │   └── SPRINT.md ✅
   ├── project/ ✅
   │   ├── PROJECT_CONTEXT.md ✅
   │   ├── PROJECT_GOALS.md ✅
   │   ├── PROJECT_CONSTRAINTS.md ✅
   │   └── PROJECT_TOPOLOGY.md ✅  ← cross-project coordination
   ├── experiments/ ✅
   │   ├── HYPOTHESIS.md ✅
   │   └── SYSTEM_EXPERIMENTS.md ✅
   ├── reports/ ✅
   │   └── CLEANUP_REPORT.md ✅
   ├── tracking/ ✅
   │   ├── BUGS.md ✅
   │   ├── IDEA_BOARD.md ✅
   │   └── INBOX.md ✅             ← cross-project message queue
   ├── subsystems/ ✅              ← per-subsystem spec files
   ├── linking/ ✅               ← shared contract specs
   │   └── README.md ✅
   ├── tasks/ ✅
   └── phases/ ✅
   docs/ ✅
   temp_scripts/ ✅
   ```

6. **Create cross-project files** (if not already present from galdr_install):
   - `.galdr/project/PROJECT_TOPOLOGY.md` — from template, starts with `relationships: none`
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
   - Review PROJECT_CONTEXT.md and confirm mission
   - Review SUBSYSTEMS.md and adjust detected components
   - Review subsystem spec files in `.galdr/subsystems/` for accuracy
   - Create first task with @g-task-new
   - Start Phase 0 planning
   - Declare cross-project relationships with @g-project-linking (when ready)
