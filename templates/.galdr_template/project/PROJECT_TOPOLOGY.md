---
project_id: '{project_id}'
project_name: '{project_name}'
layer_hint: domain_service
# layer_hint values:
#   infra           → lowest level infrastructure (OCI, Terraform, bare metal)
#   platform        → core shared services (auth hub, API gateway, Oracle bridge)
#   domain_service  → business domain apps (payment, billing, processing)
#   experience      → user-facing (web UI, mobile apps, chatbots)
#   utility         → cross-cutting tools (shared libraries, SDKs, CLIs)

relationships: none
# No cross-project relationships declared yet.
# When ready, uncomment and fill in the sections below.
# Run @g-topology to add parents, children, or siblings interactively.

# ─── PARENTS (I depend on these / they have authority over me) ──────────
# parents:
#   - id: parent-project-id
#     path: ../parent-project          # relative path from THIS project's root
#     consumes:
#       - service_name_1
#       - service_name_2
#     cascade_receive: true            # accept broadcasts from this parent
#     cascade_max_depth: 2             # max depth I'll forward their cascades

# ─── SIBLINGS (lateral dependencies / shared contracts) ─────────────────
# siblings:
#   - id: sibling-project-id
#     path: ../sibling-project
#     contracts:
#       - name: contract_name
#         local_copy: .galdr/contracts/contract_name.md
#         canonical_owner: sibling-project-id   # who maintains the source of truth
#         direction: bidirectional              # bidirectional | i_consume | they_consume

# ─── CHILDREN (these depend on me / I have authority over them) ─────────
# children:
#   - id: child-project-id
#     path: ../child-project
#     provides:
#       - service_name_1
#     cascade_forward: true            # forward received cascades to this child

# ─── CASCADE DEFAULTS ───────────────────────────────────────────────────
# cascade_defaults:
#   receive_from_parents: true
#   forward_to_children: true
#   default_depth: 1                   # depth when THIS project originates a broadcast
---
