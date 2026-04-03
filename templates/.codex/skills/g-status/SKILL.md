---
name: g-status
description: Show project status — session context, active tasks, phase progress, goals, ideas.
---
# galdr-status

## When to Use
Session start, checking project health, @g-status command.

## Steps

1. **Load session context** (if files exist):
   ```
   📌 SESSION CONTEXT
   Mission: [1 line from PROJECT_CONTEXT.md]
   Goals: G-01: [name] | G-02: [name]
   Phase: [current phase name and status]
   Ideas: [N] active on IDEA_BOARD
   ```

2. **Run sync validation** (brief):
   - TASKS.md ↔ task files: X synced, Y issues
   - Phase headers ↔ phase files: X synced, Y issues
   - SUBSYSTEMS.md: fresh / stale
   - ACTIVE_BACKLOG.md: fresh (< 26h) / stale

3. **Phase progress summary**:
   ```
   Phase 1: Foundation [🔄] — 3/8 tasks complete (37%)
     🔄 Active:  task102_auth_layer (claimed 2h ago)
     📋 Ready:   task103_api_endpoints, task104_db_migrate
     ❌ Blocked: task105_deploy (waiting on task103)
   ```

4. **Health indicators**:
   - Any tasks in `[🔄]` for > 8 hours → flag as stale
   - Any tasks in `[🔍]` for > 4 hours → flag for verification timeout
   - Phase completion: any phase where all tasks are `[✅]` but not archived
   - Active bugs: count from BUGS.md

5. **Next recommended actions** (top 3):
   - Highest priority unblocked `[📋]` tasks
   - Any `[🔍]` tasks needing verification by different agent
   - Any overdue heartbeats

6. **Cross-project advisories** (if `.galdr/project/PROJECT_TOPOLOGY.md` exists):

   Read `.galdr/linking/INBOX.md` and categorize:

   a. **CONFLICTS** → Surface as `⚠️ WARNING` before anything else (not advisory — these gate planning):
   ```
   ⚠️ CROSS-PROJECT CONFLICT — requires resolution before planning:
     CONF-001: [parent-A] says "[instruction A]" | [parent-B] says "[instruction B]"
     Subsystem: [name] — run @g-inbox to resolve
   ```

   b. **Requests, broadcasts, peer syncs** → Advisory section at the bottom:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Cross-Project Advisories (non-blocking):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     📨 [parent] → broadcast: [subject] [task NNN created]
     🔄 [sibling] → peer sync: [contract] updated [task NNN created]
     💬 [sibling] → advisory: [note, no action yet]
     📤 [child] → request pending: [brief description]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

   If INBOX is empty or has no open items: omit this section entirely.
