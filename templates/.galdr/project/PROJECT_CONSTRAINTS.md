# PROJECT_CONSTRAINTS.md

## Purpose

This file is loaded at every session start. Constraints listed here are
**non-negotiable** — they govern decisions made throughout the project.

No AI agent may override, work around, or silently ignore a constraint. Constraints
may only be changed or removed with **explicit user approval** as described below.

---

## Change Authority

### Who can change constraints

The user has ultimate authority over all constraints. AI agents may:
- Suggest adding, modifying, or removing a constraint
- Explain the tradeoffs of a proposed change
- Flag when a requested action conflicts with an active constraint

AI agents may NOT:
- Assume silence or inferred agreement is approval
- Modify a constraint based on conversational context alone
- Bypass a constraint temporarily without explicit approval

### What counts as approval

Approval requires an explicit, unambiguous statement from the user in the
current session. Accepted approval phrases include:
  - "yes", "approved", "accept", "go ahead", "confirmed", "do it"
  - Any phrase that clearly authorizes the specific change being proposed

What does NOT count as approval:
  - The user not objecting when the AI describes a plan
  - The user asking a question about the change
  - Approval for a different change in a prior session
  - Silence of any kind

### Logging requirement

Every change to this file must be recorded in the Change Log at the bottom
of this document. The log is append-only. Entries are never removed.

---

## Active Constraints

<!-- Replace the example below with your actual project constraints.
     Delete this comment block and the EXAMPLE constraint when you add real ones.
     Each constraint should have a unique C-NNN ID starting at C-001. -->

### C-001: [Constraint Name] — EXAMPLE, REPLACE THIS

**Non-negotiable**: [yes | no — yes means no exceptions without explicit approval]

**Rationale**: [Why this constraint exists. One to three sentences explaining
the business, technical, or quality reason behind the decision.]

**Applies to**: [Which parts of the codebase or workflow this constraint governs.
Examples: all API endpoints, database schema changes, authentication flows,
third-party integrations, file placement in .galdr/]

**What this means in practice**:
- [Specific behavior required. Start each bullet with an action verb.]
- [Example: All database queries must use parameterized statements, never string concatenation.]
- [Example: New dependencies require justification before being added to pyproject.toml.]
- [Add as many bullets as needed to make the constraint unambiguous.]

**Violation examples**:
- [Describe a concrete example of code or a decision that would violate this constraint.]
- [Example: Using f-strings to build SQL queries.]
- [Example: Installing a package and committing it without noting the reason.]

**Change authority**: [Who proposed this constraint and under what conditions
it may be revisited. Example: "Proposed by user on 2026-01-15. May be
revisited when switching from PostgreSQL to a different database engine."]

---

<!-- Add additional constraints below, following the same format.
     Increment the ID: C-002, C-003, etc. -->

---

## Change Log

All changes to constraints are recorded here. This table is append-only.

| Date | Constraint | Change | Approved By |
|------|------------|--------|-------------|
| [YYYY-MM-DD] | C-001 | Initial constraint added | [User name or "project setup"] |

---

## Session Start Summary

At the start of every session, the AI must display a compact summary of all
active constraints in the following format:

```
ACTIVE CONSTRAINTS:
  C-001: [Constraint Name] — [One-line summary]
  C-002: [Constraint Name] — [One-line summary]
Full constraints: .galdr/project/PROJECT_CONSTRAINTS.md
```

Rules for generating this summary:
- List every constraint whose Non-negotiable field is set to "yes"
- Include constraints set to "no" if they have been referenced in the current task
- The one-line summary must be taken directly from the constraint name and a
  condensed form of the "What this means in practice" section
- If no constraints are defined yet, omit the block entirely (do not show an
  empty list)
- If new constraints were added since the last session, note them with "(new)"
  after the one-line summary

Example output (do not display this literal block — generate it from actual
constraint data):

```
ACTIVE CONSTRAINTS:
  C-001: No raw SQL — all queries must use parameterized statements
  C-002: No new npm dependencies — justify in task file before installing (new)
Full constraints: .galdr/project/PROJECT_CONSTRAINTS.md
```
