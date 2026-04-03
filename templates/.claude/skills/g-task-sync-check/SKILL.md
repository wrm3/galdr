---
name: g-task-sync-check
description: Validate TASKS.md entries match .galdr/tasks/ files. For session start or suspected sync issues.
---
# galdr-task-sync-check

## When to Use
Session start, after any bulk task operations, or when "phantom" / "orphan" issues are suspected.

**v3 note:** Task IDs are **sequential** (globally increasing integers). Archived copies may still live under `phases/phase*/` depending on project hygiene.

## Steps

1. **Read TASKS.md** — extract all task entries with their current indicators

2. **List task files**:
   - Active: `.galdr/tasks/task*.md`
   - Archived: `.galdr/phases/phase*/task*.md`

3. **For each TASKS.md entry**:
```
[✅] entry → look in tasks/ AND phases/phase*/
[📋][🔄][🔍] entry → look in tasks/ only
[ ] entry → no file expected (OK)

✅ ACTIVE   = found in tasks/
📦 ARCHIVED = found in phases/phase*/
⚠️ PHANTOM  = not found in either location
```

4. **For each task file** (tasks/ and phases/phase*/):
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

Task 001: tasks/ ✅ ACTIVE — pending/[📋] match
Task 002: phases/phase0/ 📦 ARCHIVED — completed/[✅] match
Task 003: PHANTOM ⚠️ — in TASKS.md [📋] but no file found
Task 099: ORPHAN ⚠️ — task099_*.md exists but not in TASKS.md

Synced: 12/15 | Fixed: 2 | Needs action: 1
```

7. **Auto-fix where safe**:
   - Status mismatches → fix TASKS.md
   - Archived [✅] tasks → no action (archived is correct state)
   - Phantoms and orphans → report and offer fix options
