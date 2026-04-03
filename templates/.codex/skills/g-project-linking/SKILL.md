---
name: g-project-linking
description: Project linking — view or edit cross-project relationships in PROJECT_TOPOLOGY.md (parents, children, siblings).
---
# galdr-project-linking

## When to Use
`@g-project-linking` command. Viewing current relationships. Adding a parent, child, or sibling. Checking if connected projects can be reached.

## Steps

1. **Read `.galdr/project/PROJECT_TOPOLOGY.md`**
   - If file does not exist → create it from template (relationships: none)
   - If `relationships: none` → display "No relationships declared" + offer to add

2. **Display current topology**:
   ```
   PROJECT: [project_id] — [project_name]
   Layer:   [layer_hint]

   Parents:  [id → path | "none"]
   Children: [id → path | "none"]
   Siblings: [id → path (contracts: N) | "none"]
   Contracts: [list of .galdr/linking/ files | "none"]
   ```

3. **If user wants to add/edit a relationship**:

   **Adding a parent:**
   - Prompt: project_id, relative path, what services do you consume from them?
   - Set `cascade_receive: true`, `cascade_max_depth: 2` (defaults)
   - Verify path exists; warn if not accessible (still save the declaration)
   - If parent has PROJECT_TOPOLOGY.md: read it and confirm they don't already list you

   **Adding a child:**
   - Prompt: project_id, relative path, what do you provide to them?
   - Set `cascade_forward: true` (default)
   - Offer to also update the child's PROJECT_TOPOLOGY.md to declare you as their parent

   **Adding a sibling:**
   - Prompt: project_id, relative path
   - Prompt: any shared contracts? (name, who is canonical_owner, direction)
   - If contracts declared: create `.galdr/linking/<name>.md` stub in this project
   - Offer to update sibling's topology to reciprocate the relationship

4. **Remove `relationships: none` line** when first real relationship is added

5. **Verify paths** (relative from project root):
   - If accessible: confirm by checking if their `.galdr/` exists
   - If not accessible: flag as `⚠️ path not reachable from this workspace — topology saved anyway`

6. **Confirm**:
   ```
   Topology updated:
   - PROJECT_TOPOLOGY.md ✅
   - Contracts created: [list or none]
   - Sibling notified: [yes/no — if their path was accessible]
   ```
