---
name: g-phase-sync-check
description: Validate TASKS.md phase headers match .galdr/phases/ definition files.
---
# galdr-phase-sync-check

## When to Use
Before any phase operation, at session start, or when phase sync issues are suspected.

**v3 note:** Task IDs are **sequential** (no Phase 0 = 1–99 / Phase N = N×100 bands). Phase headers and `phases/` files are optional **milestone** metadata; they do not imply ID ranges.

## Steps

1. **Read TASKS.md** — extract all phase headers:
   ```
   ## Phase 0: Setup & Infrastructure [✅]
   ## Phase 1: Foundation [🔄]
   ```

2. **List phase definition files** in `.galdr/phases/`:
   - Pattern: `phaseN_*.md` (NOT task files — those are `task*.md`)
   - Note: `phases/phase0/` subfolders contain archived tasks — ignore those

3. **For each TASKS.md phase header**:
   ```
   Phase N → look for phases/phaseN_*.md
   → FOUND: check status match (see mapping below)
   → NOT FOUND: PHANTOM ⚠️ — offer to create stub
   ```

4. **For each phase definition file**:
   ```
   phases/phaseN_*.md → look for Phase N header in TASKS.md
   → FOUND: OK
   → NOT FOUND: ORPHAN ⚠️ — offer to add header or delete file
   ```

5. **Status mapping check**:
   | TASKS.md | Phase YAML `status:` |
   |---|---|
   | `[✅]` | completed |
   | `[🔄]` | in_progress |
   | `[⏸️]` | paused |
   | `[❌]` | cancelled |
   | (no indicator) | planning |

6. **Report**:
   ```
   📋 PHASE SYNC VALIDATION
   Phase 0: TASKS.md [✅] ↔ phase0_setup.md status:completed ✅
   Phase 1: TASKS.md [🔄] ↔ phase1_foundation.md status:in_progress ✅
   Phase 2: TASKS.md header exists ↔ NO FILE ⚠️ — creating stub
   
   Synced: 2/3 | Fixed: 1
   ```
