---
name: g-skl-pcac-order
description: As a parent project, push a task to one or more child projects with configurable cascade depth (1–3). Creates tasks in child .galdr/ folders and an INBOX notification.
---
# g-skl-pcac-order

## When to Use
`@g-pcac-order` command. When a change in this project requires action in child projects.

## Steps

1. **Read `.galdr/linking/link_topology.md`** — get children list
   - If no children declared → warn: "No children in topology. Declare children in link_topology.md first."

2. **Determine target children**:
   - All children (default)
   - Children that `consumes` a specific service (e.g., "all oracle consumers")
   - Specific named children (user specifies)

3. **Collect broadcast details** (prompt if not provided):
   - **Title**: What needs to be done in child projects?
   - **Why**: Context — why is this needed? (critical for child sessions that won't have this context)
   - **Subsystems**: Which subsystems are affected?
   - **Cascade depth**: 1 (children only) | 2 (children + grandchildren) | 3 (three generations)
   - **Source task**: Task ID in this project that triggered the order (if exists)

4. **Conflict check before creating tasks**:
   - For each target child: check if an open broadcast for the same subsystem already exists
   - If conflict detected: create `[CONFLICT]` in child INBOX.md instead of a task
   - Warn user: "Conflict detected in [child-id] — added to their INBOX instead"
   - **NOTE**: `[INFO]` messages in the child INBOX do NOT trigger conflict detection
     (INFO is advisory only; only broadcast/request types are checked for conflicts)

5. **For each accessible target child**:

   a. Read `child/.galdr/TASKS.md` to determine next available task ID

   b. Create task file at `child/.galdr/tasks/taskNNN_[descriptive_name].md`:
   ```yaml
   ---
   id: NNN
   title: '[Broadcast] [task title]'
   type: feature
   status: pending
   priority: high
   subsystems: [affected subsystems]
   project_context: '[Why this was broadcast from parent project]'
   depends_on: []
   created: 'YYYY-MM-DD'
   task_source: [this project_id]
   source_task_id: [source task id or null]
   delegation_type: broadcast
   cascade_depth_original: [depth]
   cascade_depth_remaining: [depth - 1]
   cascade_chain: [[this project_id]]
   cascade_forwarded: false
   ---
   ```

   c. Append to `child/.galdr/TASKS.md`:
   `- [📋] **Task NNN**: [title] — broadcast from [this project]`

   d. Append to `child/.galdr/linking/INBOX.md`:
   ```markdown
   ## [OPEN] BCAST-XXX — from: [this project] — YYYY-MM-DD
   **Type:** broadcast
   **Subject:** [title]
   **Why:** [context]
   **Task created:** taskNNN_[name].md
   **Cascade depth remaining:** [depth - 1]
   **Status:** task_created
   ```

6. **If child path not accessible**: stage the order locally instead of dropping it
   - Write to `.galdr/linking/pending_orders/order_[child_project_name]_[date].md`:
   ```markdown
   ---
   type: pending_order
   target_project: [child project name]
   target_path: [child path]
   created: YYYY-MM-DD
   broadcast_id: BCAST-XXX
   cascade_depth_remaining: N
   ---

   # Pending Order: [title]

   **Target**: [child_project_name] at [child_path]
   **Broadcast ID**: BCAST-XXX
   **Subject**: [title]
   **Why**: [context]
   **Cascade depth remaining**: N
   **Status**: pending_delivery

   ## Task to Create in Target

   [full task YAML that would have been written to child/.galdr/tasks/]

   ## INBOX Entry to Append

   [full INBOX markdown that would have been appended to child INBOX.md]
   ```
   - Report: "📦 [child-project]: order staged in pending_orders/ — will deliver when accessible"

**Step 0 (pre-flight — runs before steps 1-6 above)**:
   - Check `.galdr/linking/pending_orders/` for any staged orders with `Status: pending_delivery`
   - For each staged order where the target path is NOW accessible:
     - Deliver: create the task + append INBOX entry as described in step 5
     - Move staged file to `.galdr/linking/pending_orders/delivered/`
     - Report: "📨 Delivered staged order to [child_project]: [title]"
   - Check for duplicate: if BCAST ID already exists in child INBOX.md, skip (idempotent)

7. **Create tracking task in THIS project** (optional but recommended):
   ```yaml
   title: '[Broadcast tracker] [title]'
   project_context: 'Tracking broadcast to N child projects'
   ```
   Include list of all child task IDs created.
   **Note**: This tracker task will be automatically closeable when children send completion pings
   via `g-skl-pcac-notify` with `subtype: broadcast_completion`. Watch for these in `@g-pcac-read`.

8. **Report**:
   ```
   Order sent (cascade depth: N):
   ✅ [child-project]: taskNNN_[name] created
   ✅ [child-project]: taskNNN_[name] created
   ⚠️  [child-project]: path not accessible — manual delivery needed
   ⚠️  [child-project]: CONFLICT detected — added to INBOX instead

   Cascade: children will forward to grandchildren at next session open if depth > 1
   ```
