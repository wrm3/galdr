---
name: g-task-sync-check
description: Validate TASKS.md entries match .galdr/tasks/ files. For session start or suspected sync issues.
---
# galdr-task-sync-check

## When to Use
Session start, after any bulk task operations, or when "phantom" / "orphan" issues are suspected.

**v3 note:** Task IDs are **sequential** (globally increasing integers), grouped by subsystem in TASKS.md — no phase-based numbering or archive folders.

## Steps

1. **Read TASKS.md** — extract all task entries with their current indicators

2. **List task files**:
   - All tasks: `.galdr/tasks/task*.md`

3. **For each TASKS.md entry**:
```
[✅] entry → look in tasks/
[📋][🔄][🔍] entry → look in tasks/ only
[ ] entry → no file expected (OK)

✅ FOUND   = found in tasks/
⚠️ PHANTOM = not found in tasks/
```

4. **For each task file** in `tasks/`:
```
→ Has matching TASKS.md entry? 
  YES: check status match
  NO: ORPHAN ⚠️
```

5. **Status mismatch check** (for matched pairs):
| File YAML | Expected TASKS.md |
|---|---|
| pending | [📋] |
| in-progress | [🔄] |
| awaiting-verification | [🔍] |
| completed | [✅] |
| failed | [❌] |
| paused | [⏸️] |
→ Mismatch: fix TASKS.md to match file (file is source of truth)

6. **Report**:
```
📋 TASK SYNC VALIDATION

Task 001: tasks/ ✅ FOUND — pending/[📋] match
Task 003: PHANTOM ⚠️ — in TASKS.md [📋] but no file found
Task 099: ORPHAN ⚠️ — task099_*.md exists but not in TASKS.md

Synced: 12/13 | Fixed: 0 | Needs action: 1
```

7. **Auto-fix where safe**:
   - Status mismatches → fix TASKS.md
   - Phantoms and orphans → report and offer fix options
