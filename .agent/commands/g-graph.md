Display the visible project ecosystem graph: $ARGUMENTS

## What This Command Does

Assembles and displays the visible project dependency graph by reading `PROJECT_TOPOLOGY.md` files from connected projects. Shows up to 3 hops from the current project. Beyond 3 hops, shows only the count of additional projects.

## What Gets Displayed

```
GALDR PROJECT GRAPH — from: core-platform
(3-hop view — 2 projects beyond visible range)

Layer: infra
  [cloud-infra]  ../cloud-infra

Layer: platform
  ★ [core-platform] ← YOU ARE HERE
    inbox: 3 open (1 conflict ⚠️)

Layer: domain_service
  [payments-service]   ●──● card-service, api-gateway (siblings)
  [card-service]   ●──● payments-service, api-gateway (siblings)
  [batch-service]

Layer: experience
  [ach-ui]    (child of payments-service)
    ↓ 2 downstream beyond visible range

Total reachable: 14 projects | ⚠️ 1 conflict | 0 cycles
```

## Features

- **Layer grouping** — projects organized by layer_hint (infra → platform → domain_service → experience → utility)
- **Sibling display** — siblings shown with lateral connectors
- **INBOX health** — open items and conflicts visible at a glance
- **Cycle detection** — warns if a project appears in its own ancestry
- **Accessibility** — flags paths that can't be reached from this workspace
- **Horizon** — projects beyond 3 hops are counted, not shown in detail

## Optional Export

Say "export graph" to write the display to `.galdr/ECOSYSTEM_GRAPH.md`.

Follows the `g-graph` skill.
