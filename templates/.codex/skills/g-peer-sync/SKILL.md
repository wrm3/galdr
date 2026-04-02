---
name: g-peer-sync
description: Initiate or respond to sibling contract sync; advisory only, non-blocking. Both sides update local contract copies.
---
# galdr-peer-sync

## When to Use
`@g-peer-sync` command. When a shared contract with a sibling needs updating. When responding to a SYNC item in INBOX.md.

## Key Principle
**Peer syncs are advisory.** Neither sibling has authority over the other. Work in this project proceeds regardless. The sync surfaces as an advisory in `@g-status` until resolved.

## Steps

### Initiating a Sync (I changed a contract)

1. **Read `.galdr/project/PROJECT_TOPOLOGY.md`** — get siblings + their contracts
2. **Select target sibling and contract**
3. **Update local contract file** at `.galdr/contracts/<name>.md`:
   - Bump version number
   - Update content (the spec that changed)
   - Update `last_synced` date
   - Set `sync_status: current` on your copy
4. **Write to `sibling/.galdr/tracking/INBOX.md`** (if path accessible):
   ```markdown
   ## [OPEN] SYNC-XXX — from: [this project] — YYYY-MM-DD
   **Type:** peer_sync
   **Contract:** [contract_name]
   **Version:** [old] → [new]
   **Change:** [brief description of what changed and why]
   **Your action:** Update your copy at `.galdr/contracts/[name].md`
   **Canonical spec path:** [this project]/.galdr/contracts/[name].md
   **Your task:** [will be created below]
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
7. **If sibling path not accessible**: stage the notification at `.galdr/pending_requests/sync_[sibling].md`

### Responding to a Sync (Sibling notified me)

1. **Read INBOX item** (`SYNC-XXX` in INBOX.md) or check the created task
2. **Read their updated contract** (if path accessible) at `sibling/.galdr/contracts/<name>.md`
3. **Update local copy** at `.galdr/contracts/<name>.md`:
   - Match their version number
   - Update content to match canonical
   - Set `sync_status: current`
4. **Close the local peer_sync task**: status → completed
5. **Mark INBOX item** `[DONE]`
6. **If sibling path accessible**: update their INBOX entry to note your sync is complete:
   - Find `SYNC-XXX` in sibling's INBOX, add note: `Partner [this project] synced on YYYY-MM-DD`
   - Update sibling's tracking task: `peer_sync_status: partner_completed`

### Report (both directions)
```
Peer sync complete:
- Contract: [name] — v[new]
- Local copy updated: .galdr/contracts/[name].md ✅
- Sibling notified/confirmed: [sibling_id] ✅
- Tasks created/closed ✅
```
