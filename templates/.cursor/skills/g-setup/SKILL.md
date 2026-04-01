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
   - Folders: `.galdr/`, `.galdr/tasks/`, `.galdr/phases/`, `.galdr/templates/`, `.galdr/config/`, `.galdr/docs/`, `.galdr/tracking/`, `.galdr/subsystems/`, `docs/`, `temp_scripts/`
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
   ├── docs/ ✅
   │   ├── PROJECT_CONTEXT.md ✅
   │   ├── PROJECT_GOALS.md ✅
   │   ├── ARCHITECTURE_CONSTRAINTS.md ✅
   │   ├── PROJECT_TOPOLOGY.md ✅  ← cross-project coordination
   │   └── SYSTEM_EXPERIMENTS.md ✅
   ├── tracking/ ✅
   │   ├── BUGS.md ✅
   │   ├── IDEA_BOARD.md ✅
   │   └── INBOX.md ✅             ← cross-project message queue
   ├── subsystems/ ✅              ← per-subsystem spec files
   ├── contracts/ ✅               ← shared contract specs
   │   └── README.md ✅
   ├── tasks/ ✅
   └── phases/ ✅
   docs/ ✅
   temp_scripts/ ✅
   ```

6. **Create cross-project files** (if not already present from galdr_install):
   - `.galdr/docs/PROJECT_TOPOLOGY.md` — from template, starts with `relationships: none`
   - `.galdr/tracking/INBOX.md` — empty template with usage comments
   - `.galdr/contracts/README.md` — explanation of contracts pattern

7. **Print next steps**:
   - Review PROJECT_CONTEXT.md and confirm mission
   - Review SUBSYSTEMS.md and adjust detected components
   - Create first task with @g-task-new
   - Start Phase 0 planning
   - Declare cross-project relationships with @g-topology (when ready)
