---
name: g-skl-pcac-read
description: Review and action all incoming cross-project coordination items — conflicts (block planning), requests from children, broadcasts from parents, and peer syncs from siblings.
---
# g-skl-pcac-read

## When to Use
`@g-pcac-read` command. Session start when INBOX items exist. After receiving a cross-project task. After `g-hk-pcac-inbox-check.ps1` reports items.

## Steps

1. **Read `.galdr/linking/INBOX.md`**
   - If empty or not exists → "INBOX clear — no cross-project items pending"
   - Categorize items: CONFLICT | request | broadcast | peer_sync | info

2. **Display grouped by urgency**:
   ```
   INBOX — [project_id]

   ⚠️  CONFLICTS (gate all work until resolved): N
   📨 REQUESTS from children needing parent action: N
   📢 BROADCASTS from parents (tasks already created): N
   🔄 PEER SYNCS from siblings (contract updates): N
   ℹ️  INFO (no action required): N
   ✅ DONE (recent, audit trail): N
   ```

3. **Handle CONFLICTS first** (⚠️ — these gate ALL work):
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
   - Confirm the task created by `@g-pcac-order` exists in `.galdr/tasks/`
   - If task missing: create it now from the INBOX entry details
   - Show task status and offer to start work
   - Check for `broadcast_completion` INFO subtypes: display alongside broadcasts as "✅ {title} completed [child_name]"
   - If `broadcast_completion` received: offer to mark the parent's tracker task `[✅]`

6. **Handle PEER SYNCS** (sibling contract changed):
   - Show: which sibling, which contract, what changed
   - Confirm task exists (created when peer_sync arrived)
   - Open the peer copy for review: `.galdr/linking/peers/{sibling_name}.md`
   - After human updates the contract: mark task complete, update INBOX to `[DONE]`
   - If sibling path accessible: write completion notice to sibling's INBOX.md

7. **Handle INFO items** (ℹ️ — no action required):
   - Display each INFO item with sender, subject, and detail
   - No task to create, no approval needed
   - Ask: "Acknowledge and mark done? [y/n]" (default: yes)
   - On acknowledgment: change `[OPEN]` to `[DONE]` in INBOX.md
   - Staging: after INBOX processing, report any pending staged info entries:
     "⚠️ N staged INFO notification(s) in pending_requests/ for [project] — not yet delivered"
   - Also check `pending_orders/` and surface count: "⚠️ N broadcast(s) staged in pending_orders/ for [project] — not yet accessible"

8. **Update INBOX.md** — change reviewed items to `[DONE]`, add resolution notes

9. **Report**:
   ```
   INBOX processed:
   - 1 conflict resolved ✅
   - 2 requests actioned (tasks created) ✅
   - 1 peer sync completed ✅
   - 0 broadcasts pending
   - 3 INFO items acknowledged ✅
   INBOX clear ✅
   ```
