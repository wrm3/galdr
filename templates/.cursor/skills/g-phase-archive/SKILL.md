---
name: g-phase-archive
description: Archive completed phase tasks into .galdr/phases/phaseN/. For retroactive archive or missed automatic archive.
---
# galdr-phase-archive

## When to Use
@g-phase-archive [phase_number]
Manual archiving of a completed/cancelled phase.

## Steps

1. **Get phase number** (prompt if not given):
   "Which phase to archive? (e.g., 0, 1, 2)"

2. **Validate phase exists**:
   - Check TASKS.md for `## Phase N:` header
   - Check `.galdr/phases/phaseN_*.md` exists

3. **Find task files to archive**:
   - Glob `.galdr/tasks/task*.md`
   - Filter: YAML `phase: N` OR task ID in range (Phase 0: 1-99, Phase N: N×100 to N×100+99)

4. **Safety check** (show table if any incomplete):
   ```
   □ ALL files have status: completed OR status: cancelled?
   
   If NO:
   ⛔ Cannot archive Phase N — these tasks are not complete:
   
   | Task | Title | Status |
   |------|-------|--------|
   | 042  | Build API | in-progress |
   
   Options:
   1. Force archive anyway (requires explicit "yes, force")
   2. Cancel
   ```

5. **Check existing archive**:
   - Does `.galdr/phases/phaseN/` already exist with files?
   - If YES: "Archive folder exists with N files. Merge? (yes/no)"

6. **Execute move**:
   ```
   Create: .galdr/phases/phaseN/  (if not exists)
   Move:   tasks/taskNNN_*.md → phases/phaseN/taskNNN_*.md
   ```
   Preserve exact filename and file contents.

7. **Print move report**:
   ```
   📦 Phase N Task Archive
   Moved 3 files → .galdr/phases/phaseN/
     ✅ task001_init_project.md
     ✅ task002_setup_env.md
     ✅ task003_configure_db.md
   
   .galdr/tasks/ now contains 12 active task files.
   ```

8. **Update TASKS.md**: Add under phase header:
   ```
   > 📦 Archived: .galdr/phases/phaseN/ (YYYY-MM-DD)
   ```

9. **Offer git commit**:
   ```bash
   git add .galdr/phases/phaseN/ .galdr/TASKS.md
   git commit -m "chore(phase-N): archive completed task files
   
   Moved N task files to .galdr/phases/phaseN/
   Phase: N — Phase Name"
   ```

## File Naming Convention Note
Archive folder is `phaseN/` (number only, not full name) — stable even if phase gets renamed.
The phase DEFINITION file (`phaseN_name.md`) stays at `.galdr/phases/` root and is NEVER moved.
