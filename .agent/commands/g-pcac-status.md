Show cross-project coordination status: $ARGUMENTS

## What This Command Does

Displays the full PCAC (Project Command and Control) status: this project's topology role, linked project health, and open INBOX summary. Delegates to `g-agnt-pcac-coordinator`.

## Output Format

```
PCAC STATUS — {project_name}
────────────────────────────────────────
Role: {parent | child | sibling | standalone}
Project: {project_path}

Parent: {name} at {path} [accessible ✅ | inaccessible ⚠️ | none]

Children ({N}):
  - {name} at {path} [accessible ✅ | inaccessible ⚠️]

Siblings ({N}):
  - {name} at {path} [accessible ✅ | inaccessible ⚠️]

────────────────────────────────────────
INBOX: {N open items}
  {c} conflicts  ⚠️  (BLOCKS all other coordination work)
  {r} requests
  {b} broadcasts
  {s} syncs
────────────────────────────────────────
```

## Workflow

### 1. Load Topology
Read `.galdr/linking/link_topology.md`.

If missing → "Topology not configured. Complete task007 to set up the linking/ directory."

### 2. Check Project Accessibility
For each linked project, check if path is accessible on the current machine.

### 3. Read INBOX
Read `.galdr/linking/INBOX.md` and count items by type.

### 4. Report
Display the status block above. If CONFLICTs exist, recommend running `@g-pcac-read` immediately.

## Usage Examples

```
@g-pcac-status
```

## Delegates To
`g-agnt-pcac-coordinator`
