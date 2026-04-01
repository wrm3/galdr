---
name: g-graph
description: Assemble the project graph from topology files. Three hops of detail, then counts. Detects cycles and access issues.
---
# galdr-graph

## When to Use
`@g-graph` command. Understanding the project ecosystem. Auditing relationship declarations. Finding cross-project paths.

## Steps

1. **Read current project's `.galdr/docs/PROJECT_TOPOLOGY.md`**
   - This project is the center of the graph (marked ★)
   - If no topology file → "No topology declared. Run @g-topology first."

2. **Recursive traversal** (max 3 hops from center):
   - Maintain a `visited` set of project IDs (cycle detection)
   - For each hop level, read the topology files of all connected projects
   - At each step: check if project_id already in `visited` → cycle detected → warn and stop that branch
   - Stop traversal at 3 hops; count any projects discovered at hop 4+ but don't read their topologies

3. **Cycle detection**:
   - If Project A declares B as child AND B declares A as parent → valid (normal parent-child)
   - If Project A declares B as child AND B also declares A as child → `⚠️ CYCLE: [A] ↔ [B] both claim each other as child`
   - Warn and continue graph with the cycle flagged

4. **Display the graph** grouped by `layer_hint` (infra → platform → domain_service → experience → utility → unknown):

   ```
   galdr project GRAPH — from: [project_id]
   ([N]-hop view — [M] projects beyond visible range)

   Layer: infra
     [cloud-infra]  ../cloud-infra
       ↑ 0 upstream beyond this

   Layer: platform
     ★ [core-platform] ← YOU ARE HERE
       provides: jwt_auth, rbac, oracle_bridge, postgresql, nav_menu, api_keys
       inbox: 3 open (2 requests, 1 conflict ⚠️)

   Layer: domain_service
     [payments-service]   ../payments-service    ●──● card-service, api-gateway (siblings)
     [card-service]   ../card-service    ●──● payments-service, api-gateway (siblings)
     [api-gateway]   ../api-gateway    ●──● payments-service, card-service (siblings)
     [batch-service] ../batch-service
     [ai-service]    ../ai-service

   Layer: experience
     [ach-ui]    ../ach-ui    (child of payments-service)
       ↓ 2 downstream projects beyond visible range

   ═══════════════════════════════════════════════════
   Total reachable: 14 projects across 4 layers
   Beyond 3-hop horizon: 2 projects (counts only)
   ⚠️  1 conflict across ecosystem (in core-platform INBOX)
   ═══════════════════════════════════════════════════
   ```

5. **Accessibility warnings** (inline):
   - Path declared in topology that can't be read: `[project-id] ⚠️ path not accessible`
   - Still show the project in the graph from declared metadata

6. **Ecosystem health summary** (at the bottom):
   - Total open INBOX items across all accessible projects
   - Any conflicts (⚠️ — surface prominently)
   - Any cycles detected
   - Any inaccessible paths

7. **Optional: export** — offer to write graph summary to `.galdr/ECOSYSTEM_GRAPH.md` for reference
