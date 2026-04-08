---
name: g-skl-pcac-sync
description: Initiate or respond to sibling contract sync — advisory only, non-blocking. Both sides update local peer topology copies.
---
# g-skl-pcac-sync

## When to Use
`@g-pcac-sync` command. When a shared contract with a sibling needs updating, or when responding to a SYNC item in INBOX.md.

## Key Principle
**Peer syncs are advisory.** Neither sibling has authority over the other. Work in this project proceeds regardless. The sync surfaces as an advisory in `@g-status` until resolved.

## Steps

### Initiating a Sync (I changed a contract)

1. **Read `.galdr/linking/link_topology.md`** — get siblings list
2. **Select target sibling and contract**
3. **Update local peer copy** at `.galdr/linking/peers/{sibling_name}.md`:
   - Bump version number
   - Update content (the spec that changed)
   - Update `last_synced` date
   - Set `sync_status: current` on your copy
4. **Write to `sibling/.galdr/linking/INBOX.md`** (if path accessible):
   ```markdown
   ## [OPEN] SYNC-XXX — from: [this project] — YYYY-MM-DD
   **Type:** peer_sync
   **Contract:** [contract_name]
   **Version:** [old] → [new]
   **Change:** [brief description of what changed and why]
   **Your action:** Update your copy at `.galdr/linking/peers/[name].md`
   **Canonical spec path:** [this project]/.galdr/linking/peers/[name].md
   **Status:** action_needed
   ```
5. **Create task in sibling's `.galdr/`** (if path accessible):
   ```yaml
   title: '[Peer Sync] Update [contract_name] from [this project] — v[new]'
   delegation_type: peer_sync
   peer_sync_partner: [this project_id]
   peer_sync_status: action_needed
   ```
6. **Create local task** tracking that sync was initiated:
   ```yaml
   title: '[Peer Sync] Notified [sibling] of [contract_name] change — awaiting ack'
   delegation_type: peer_sync
   peer_sync_partner: [sibling_id]
   peer_sync_status: pending_partner
   ```
7. **If sibling path not accessible**: stage the notification at `.galdr/linking/pending_requests/sync_[sibling].md`

### Responding to a Sync (Sibling notified me)

1. **Read INBOX item** (`SYNC-XXX` in INBOX.md) or check the created task
2. **Read their updated contract** (if path accessible) at `sibling/.galdr/linking/peers/{name}.md`
3. **Update local peer copy** at `.galdr/linking/peers/{sibling_name}.md`:
   - Match their version number
   - Update content to match canonical
   - Set `sync_status: current`
4. **Close the local peer_sync task**: status → completed
5. **Mark INBOX item** `[DONE]`
6. **If sibling path accessible**: update their INBOX entry to note your sync is complete

### Report (both directions)
```
Peer sync complete:
- Contract: [name] — v[new]
- Local peer copy updated: .galdr/linking/peers/[sibling_name].md ✅
- Sibling notified/confirmed: [sibling_id] ✅
- Tasks created/closed ✅
```
