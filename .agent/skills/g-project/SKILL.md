---
name: g-project
description: Own and manage PROJECT.md (mission, goals, project linking) and CONSTRAINTS.md (non-negotiable architectural rules). Single source of truth for project identity and guardrails.
---
# g-project

**Files Owned**: `.galdr/PROJECT.md`, `.galdr/CONSTRAINTS.md`

**Activate for**: "update goals", "define constraints", "what's the mission", "project linking", "add constraint", "update PROJECT.md", setup/planning steps that need project context.

---

## Operation: CREATE / UPDATE PROJECT.MD

`PROJECT.md` is the project identity document. It holds mission, goals, and cross-project linking. Agents read it at session start to orient themselves.

```markdown
# PROJECT.md — {project_name}

## Mission
[One sentence: what this project does and why it exists]

## Current Focus
[Active development area — updated each phase/sprint]

## Goals

### Vision
[1-2 sentences: what success looks like]

### Primary Goals
| ID | Goal | Target / Metric | Status |
|---|---|---|---|
| G-01 | [Goal name] | [Measurable outcome] | active |
| G-02 | [Goal name] | [Measurable outcome] | active |

### Secondary Goals
- **[Goal name]**: [How it supports primary goals]

### Non-Goals (Explicitly Out of Scope)
- [Things we are NOT building]

### Success Metrics
- [Quantifiable targets]

### Goal Log
| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | Initial creation | Project setup |

## Project Linking
<!-- Cross-project relationships — see g-project-linking -->
relationships: none
parents: []
children: []
siblings: []
```

**Gather goals** (ask if not clear from context):
- "What is the primary outcome this project must achieve?"
- "What does success look like in 3-6 months?"
- "What are we explicitly NOT building?"
- "How will we measure success?"

**Goal change protocol**: never delete — mark old goals as `complete` or `retired` + add Goal Log entry.

---

## Operation: CREATE / UPDATE CONSTRAINTS.MD

`CONSTRAINTS.md` holds architectural rules that agents must never violate. Each constraint has a rationale, violation examples, and enforcement note.

```markdown
# CONSTRAINTS.md — {project_name}

## Architectural Constraints

### C-001: [Constraint Name]
**Status**: active
**Rationale**: [Why this rule exists]
**Applies to**: [What code/files/actions this governs]

**Rules**:
- [Specific rule 1]
- [Specific rule 2]

**Violation Examples**:
- [What NOT to do]

**Enforcement**: [How violations are detected — g-cleanup parity audit, g-grooming check, etc.]

---

## Constraint Log
| Date | Constraint | Change | Author |
|---|---|---|---|
| YYYY-MM-DD | C-001 | Initial creation | user |
```

**When to add a constraint**:
- A pattern keeps being violated and needs a rule
- An architectural decision has been finalized
- A past mistake should never recur
- User says "that should never happen" / "always do X"

---

## Session Start Display

When PROJECT.md exists, surface:
```
📌 SESSION CONTEXT
Mission: [1 line from PROJECT.md]
Goals: G-01: [name] | G-02: [name]
Constraints: [N] active
```

---

## Decision Validation

When creating tasks or making architecture decisions, briefly check:
- "This aligns with G-{ID}" ✅
- "This conflicts with Non-Goal: [X]" ⚠️ — flag for user
- "This violates C-{ID}" 🚫 — stop and explain
