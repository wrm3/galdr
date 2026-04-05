---
name: g-skl-plan
description: Own and manage PLAN.md (master strategy) and prds/ (individual PRD files) — create plans, write PRDs, validate scope, and keep the deliverable index current.
---
# g-plan

**Files Owned**: `.galdr/PLAN.md`, `.galdr/PRDS.md`, `.galdr/prds/prdNNN_*.md`

**Activate for**: "create plan", "write PRD", "define requirements", "what's the plan", "update PLAN.md", "new PRD".

**Hierarchy**: `PLAN.md` is the master strategy above individual PRDs. `PRDS.md` is the index. Each `prds/prdNNN_*.md` is a focused requirements document.

---

## Operation: CREATE / UPDATE PLAN.md

`PLAN.md` is the one-page strategy doc — deliverable index, build order, milestone history. Kept short; details live in PRDs.

```markdown
# PLAN.md — {project_name} Master Plan

## Current Focus
{Describe current development focus — 1-2 sentences}

## Deliverable Index

| ID | Title | Status | Subsystems | Notes |
|----|-------|--------|------------|-------|
| PRD-001 | Foundation | active | task-mgmt, setup | Started 2026-01-01 |

## Build Order

### Active Work
{List active PRDs with priority}

### Completed
{List completed PRDs}

## Milestone History
{Record major direction changes with dates}
```

> **MANDATORY FOLLOW-THROUGH**: If you add any PRD rows to the Deliverable Index,
> you MUST in the same response:
> 1. Create each referenced PRD file at `.galdr/prds/prdNNN_descriptive_name.md` (use the CREATE PRD operation below)
> 2. Add each PRD to `PRDS.md` index
>
> Do NOT leave PLAN.md referencing PRDs that don't have files. "Draft or refine as needed" is NOT acceptable during initial setup — create them now.

---

## Operation: CREATE PRD

1. **Scope validation** (ask before writing anything):
   1. Personal / small team (2-10) / broader deployment (10+)?
   2. Security: minimal / standard / enhanced / enterprise?
   3. Scalability: basic / moderate / high / enterprise?
   4. Feature complexity: minimal / standard / feature-rich?
   5. Integrations: standalone / basic / standard?

2. **Determine next PRD ID**: read `PRDS.md`, find highest PRD-NNN → increment

3. **Gather requirements** (27-question framework if needed):
   - Project context (Q1-7): problem, success, users, scale, frequency
   - Technical (Q8-16): deployment, security, performance, data
   - Features (Q17-22): MVP, nice-to-have, avoid, priorities
   - Timeline (Q23-27): drivers, delivery, constraints

4. **Identify shared modules** BEFORE writing feature sections:
   "What logic will be needed by 2+ features/subsystems?" → plan extraction to `lib/` first

5. **Create PRD file** at `.galdr/prds/prdNNN_descriptive_name.md`:
```markdown
---
id: NNN
title: 'PRD Title'
status: draft | active | completed | cancelled
subsystems: [affected-subsystems]
created_date: 'YYYY-MM-DD'
---

# PRD-NNN: [Title]

## 1. Product Overview
### 1.1 Summary
### 1.2 Goals
- **Business**: [outcome]
- **User**: [outcome]
- **Non-Goals**: [what we're NOT building]

## 2. User Personas
[Who uses this feature]

## 3. Acceptance Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## 4. Milestones
| Milestone | Tasks | Target |
|---|---|---|
| M1: [name] | Task NNN, NNN | YYYY-MM-DD |

## 5. Technical Considerations
### Shared Modules
[Logic needed by 2+ subsystems — extract before implementing]

## 6. Success Metrics
[How we know this PRD is done]
```

6. **Add to PRDS.md** index (atomic):
   ```
   | PRD-NNN | Title | draft | subsystem1, subsystem2 | |
   ```

7. **Add to PLAN.md** Deliverable Index

8. **Offer initial tasks** — activate g-tasks CREATE for first milestone tasks

---

## Operation: UPDATE PRD STATUS

Update status in the PRD file YAML and sync to `PRDS.md` index row.

Status flow: `draft → active → completed | cancelled`

---

## PRDS.md Structure

```markdown
# PRDS.md — {project_name}

## PRD Index

| ID | Title | Status | Subsystems | Notes |
|----|-------|--------|------------|-------|

<!-- Status: draft | active | completed | cancelled -->
```
