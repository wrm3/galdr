---
name: g-request
description: Child project requests parent action — writes parent INBOX.md and local blocked task with cross-project metadata.
---
# galdr-request

## When to Use
`@g-request` command. When this project needs a parent project to DO something before work here can proceed.

## Steps

1. **Read `.galdr/PROJECT_TOPOLOGY.md`** — get parents list
   - If no parents declared → "No parents in topology. Run @g-topology to declare a parent first."

2. **Select target parent** (if multiple parents):
   - Which parent is being asked?
   - Which service/area does this request relate to? (helps parent route it)

3. **Collect request details** (prompt if not provided):
   - **What do you need the parent to do?** (specific action, e.g., "Add payments-service to VALID_SYSTEMS in postgres.py")
   - **Why?** (context — what local work does this unblock?)
   - **Is this blocking your local work?** (yes → local task status = blocked)

4. **Create local task** in `.galdr/tasks/taskNNN_[name].md`:
   ```yaml
   ---
   id: NNN
   title: '[Waiting] [description of what parent must do]'
   type: feature
   status: blocked
   priority: high
   phase: [current phase]
   subsystems: [affected subsystems]
   project_context: 'Waiting for [parent] to [action] before this can proceed'
   dependencies: []
   created_date: 'YYYY-MM-DD'
   completed_date: ''
   delegation_type: request
   task_source: [this project_id]
   requires_parent_action: true
   parent_action_status: pending
   parent_action_project: [parent project_id]
   ---
   ```

5. **Write to `parent/.galdr/INBOX.md`** (if path accessible):
   ```markdown
   ## [OPEN] REQ-XXX — from: [this project_id] — YYYY-MM-DD
   **Type:** request
   **Subject:** [brief title]
   **Detail:** [full description of what's needed]
   **Context:** [why this is needed, what it unblocks]
   **Blocking task:** [this project]/.galdr/tasks/taskNNN_[name].md
   **Status:** open
   ```

6. **If parent path not accessible**:
   - Save request details to a local staging file: `.galdr/pending_requests/req_[parent].md`
   - Warn: "Parent path not accessible. Request staged at `.galdr/pending_requests/req_[parent].md`. Deliver manually or next time parent session has access to this path."

7. **Add local task to TASKS.md** under current phase

8. **Report**:
   ```
   Request sent:
   - Target parent: [parent_id]
   - INBOX entry: parent/.galdr/INBOX.md (REQ-XXX) ✅
   - Local task: taskNNN_[name].md created (status: blocked) ✅
   - Local TASKS.md: updated ✅

   Your local task taskNNN is blocked until [parent_id] actions this request.
   It will appear as an advisory in your @g-status output.
   ```

## When Parent Completes the Request

Parent will either:
- Write `parent_action_status: completed` directly to your task file (if they have path access)
- Or notify you via your INBOX.md

When `parent_action_status: completed` is set → change local task status from `blocked` to `pending` and proceed.
