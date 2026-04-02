---
name: g-broadcast
description: As a parent project, push a task to one or more child projects with configurable cascade depth (1–3). Creates tasks in child .galdr/ folders and an INBOX notification.
---
# galdr-broadcast

## When to Use
`@g-broadcast` command. When a change in this project requires action in child projects.

## Steps

1. **Read `.galdr/project/PROJECT_TOPOLOGY.md`** — get children list
   - If no children declared → warn: "No children in topology. Run @g-topology to declare children first."

2. **Determine target children**:
   - All children (default)
   - Children that `consumes` a specific service (e.g., "all oracle consumers")
   - Specific named children (user specifies)

3. **Collect broadcast details** (prompt if not provided):
   - **Title**: What needs to be done in child projects?
   - **Why**: Context — why is this needed? (critical for child sessions that won't have this context)
   - **Subsystems**: Which subsystems are affected?
   - **Cascade depth**: 1 (children only) | 2 (children + grandchildren) | 3 (three generations)
   - **Source task**: Task ID in this project that triggered the broadcast (if exists)

4. **Conflict check before creating tasks**:
   - For each target child: check if an open broadcast for the same subsystem already exists
   - If conflict detected: create `[CONFLICT]` in child INBOX.md instead of a task
   - Warn user: "Conflict detected in [child-id] — added to their INBOX instead"

5. **For each accessible target child**:

   a. Read `child/.galdr/TASKS.md` to determine next available task ID for their current phase

   b. Create task file at `child/.galdr/tasks/taskNNN_[descriptive_name].md`:
   ```yaml
   ---
   id: NNN
   title: '[Broadcast] [task title]'
   type: feature
   status: pending
   priority: high
   phase: [child's current phase]
   subsystems: [affected subsystems]
   project_context: '[Why this was broadcast from parent project]'
   dependencies: []
   created_date: 'YYYY-MM-DD'
   completed_date: ''
   task_source: [this project_id]
   source_task_id: [source task id or null]
   delegation_type: broadcast
   cascade_depth_original: [depth]
   cascade_depth_remaining: [depth - 1]
   cascade_chain: [[this project_id]]
   cascade_forwarded: false
   ---
   ```

   c. Append to `child/.galdr/TASKS.md` under their current phase:
   `- [📋] **Task NNN**: [title] — broadcast from [this project]`

   d. Append to `child/.galdr/tracking/INBOX.md`:
   ```markdown
   ## [OPEN] BCAST-XXX — from: [this project] — YYYY-MM-DD
   **Type:** broadcast
   **Subject:** [title]
   **Why:** [context]
   **Task created:** taskNNN_[name].md
   **Cascade depth remaining:** [depth - 1]
   **Status:** task_created
   ```

6. **If child path not accessible**: log a warning message for human to manually deliver

7. **Create tracking task in THIS project** (optional but recommended):
   ```yaml
   title: '[Broadcast tracker] [title]'
   project_context: 'Tracking broadcast to N child projects'
   ```
   Include list of all child task IDs created.

8. **Report**:
   ```
   Broadcast complete (depth: N):
   ✅ payments-service: task209_[name] created
   ✅ card-service: task315_[name] created
   ⚠️  batch-service: path not accessible — manual delivery needed
   ⚠️  api-gateway: CONFLICT detected — added to INBOX instead

   Cascade: children will forward to grandchildren at next session open if depth > 1
   ```
