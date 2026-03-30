---
name: g-inbox
description: Review and action all incoming cross-project coordination items — conflicts (block planning), requests from children, broadcasts from parents, and peer syncs from siblings.
---
# galdr-inbox

## When to Use
`@g-inbox` command. Session start when INBOX items exist. After receiving a cross-project task.

## Steps

1. **Read `.galdr/INBOX.md`**
   - If empty or not exists → "INBOX clear — no cross-project items pending"
   - Categorize items: CONFLICT | request | broadcast | peer_sync

2. **Display grouped by urgency**:
   ```
   INBOX — [project_id]

   ⚠️  CONFLICTS (gate planning until resolved): N
   📨 REQUESTS from children needing parent action: N
   📢 BROADCASTS from parents (tasks already created): N
   🔄 PEER SYNCS from siblings (contract updates): N
   ✅ DONE (recent, audit trail): N
   ```

3. **Handle CONFLICTS first** (⚠️ — these gate planning):
   - Show both conflicting instructions side by side
   - Show which subsystem is affected
   - Prompt human: "How to resolve? Options: Follow A / Follow B / Follow both / Ignore both / Custom"
   - Record resolution in INBOX.md: `**Resolution:** [human's answer]` + `**Resolved by:** [date]`
   - Change status from `[CONFLICT]` to `[DONE]`
   - If task was created for conflicted subsystem: update it with the resolution

4. **Handle REQUESTS** (child needs parent to act):
   - Show: who is asking, what they need, which task is blocking them
   - Offer: `Action (create task here) / Defer (keep open) / Reject (close with note)`
   - If actioned: create task in `.galdr/tasks/` with reference to child's blocking task
   - If accessible: write `parent_action_status: completed` to child's task file
   - Mark INBOX entry `[DONE]`

5. **Handle BROADCASTS** (parent sent work):
   - Confirm the task created by `@g-broadcast` exists in `.galdr/tasks/`
   - If task missing: create it now from the INBOX entry details
   - Show task status and offer to start work

6. **Handle PEER SYNCS** (sibling contract changed):
   - Show: which sibling, which contract, what changed
   - Confirm task exists (created when peer_sync arrived)
   - Open the contract for review: `.galdr/contracts/<name>.md`
   - After human updates the contract: mark task complete, update INBOX to `[DONE]`
   - If sibling path accessible: write completion notice to sibling's INBOX.md

7. **Update INBOX.md** — change reviewed items to `[DONE]`, add resolution notes

8. **Report**:
   ```
   INBOX processed:
   - 1 conflict resolved ✅
   - 2 requests actioned (tasks created) ✅
   - 1 peer sync completed ✅
   - 0 broadcasts pending
   INBOX clear ✅
   ```
