# g-skl-constraints

**Skill**: `g-skl-constraints`
**Owner**: File-centric owner of `.galdr/CONSTRAINTS.md`
**Trigger**: `@g-constraints`, `@g-constraint-add`, `@g-constraint-check`

---

## Operations

### ADD — Create a new constraint

Use when the user wants to add a new architectural rule to the project.

**Steps**:
1. Assign the next sequential C-ID (check the Constraint Index for the highest current ID)
2. Gather the following fields from context or ask the user:
   - **Name**: 2-5 hyphenated words, descriptive
   - **Rationale**: 2-3 sentences explaining the core reason
   - **Applies to**: which files, behaviors, or agents
   - **In practice**: 3-6 specific rules
   - **Violation examples**: 2-4 concrete examples of what NOT to do
   - **Enforcement**: how/when this is checked
3. Add a row to `## Constraint Index`:
   ```
   | C-{ID} | active | {name} | {one-line summary} |
   ```
4. Add a full `### C-{ID}: {name}` block in `## Constraint Definitions` following the established format
5. Append an entry to `## Change Log`:
   ```
   | {today} | C-{ID} | Initial constraint created — {name} | user |
   ```
6. Confirm completion: "Constraint C-{ID} ({name}) added. ID it in future task YAMLs as `{slug}`."

---

### UPDATE — Modify an existing constraint

Use when an existing constraint needs to change (wording, scope, in-practice rules).

**Steps**:
1. STOP — display the current constraint text verbatim
2. State the proposed change and rationale
3. **WAIT** for explicit user approval. Required phrases: "yes", "approved", "go ahead", "confirmed", "do it"
4. Do NOT proceed on inferred agreement, silence, or conversational context alone
5. After approval: apply the change to both the `## Constraint Index` summary row and the `## Constraint Definitions` block
6. Append an entry to `## Change Log`:
   ```
   | {today} | C-{ID} | {description of change} | user |
   ```

---

### CHECK — Validate current work against active constraints

Use during `g-go-code` AC gate step (b2), or on demand before claiming a task.

**Steps**:
1. Read all rows in `## Constraint Index` where Status = `active`
2. For each active constraint, evaluate: does the current task/implementation potentially violate any rule?
3. Report verdicts:
   - `✅ PASS` — no conflict found
   - `⚠️ POSSIBLE` — implementation touches this area; review carefully
   - `🚫 VIOLATION` — implementation would violate this constraint
4. Any `🚫 VIOLATION` → **block task completion**; return to implementation step
5. Any `⚠️ POSSIBLE` → note it; agent must confirm the concern is addressed before marking `[🔍]`

**Output format**:
```
CONSTRAINT CHECK:
  C-001 [file-first vault]: ✅ PASS
  C-009 [10-target propagation]: ⚠️ POSSIBLE — skill added to template_full; confirm root copies exist
  C-007 [secrets]: ✅ PASS
  ...
```

---

### LIST — Display active constraints at session start

Use at every session start (called by `g-rl-25`) to surface the active constraint summary.

**Output format**:
```
ACTIVE CONSTRAINTS (12):
  C-001 [file-first vault]: Vault works without Docker or MCP
  C-002 [obsidian-markdown]: Standard MD + [[wikilinks]]; tags: not topics:
  C-003 [path-via-identity]: Resolve vault_location from .identity before writes
  C-004 [mirrors-outside-vault]: Raw repo clones go to repos_location, not vault
  C-005 [schema-first]: Update VAULT_SCHEMA.md before adding folders/fields
  C-006 [log-operations]: Append to vault/log.md after non-trivial mutations
  C-007 [no-secrets]: No tokens/passwords in vault notes or task files
  C-008 [self-hosting-parity]: Repo works as live project AND install template
  C-009 [10-target-propagation]: Framework changes go to all 10 IDE targets
  C-010 [bidirectional-parity]: Public content in root ↔ template_full
  C-011 [structural-independence]: No symlinks/junctions between targets
  C-012 [galdr-contract-parity]: template_full/.galdr/ matches root .galdr/ structure
Full detail: .galdr/CONSTRAINTS.md
```

---

## Format Reference

Each constraint definition block follows this template:

```markdown
### C-{ID}: {Name}

**Status**: active | superseded | retired
**Established**: YYYY-MM-DD
**Rationale**: [2-3 sentences]

**Applies to**: [files, behaviors, agents]

**In practice**:
- [Rule 1]
- [Rule 2]
- [Rule 3]

**Violation examples**:
- [Concrete example of what NOT to do]
- [Concrete example of what NOT to do]

**Enforcement**: [How/when checked — g-go-code AC gate, session start, parity sync, etc.]
```

---

## Constraint Naming Convention

New constraint names must:
- Be 2-5 hyphenated words
- Describe what the rule *enforces*, not just what it *is*
- Read naturally as a bullet point in a project README
- Be immediately understood by a developer reading it cold

**Good**: `file-first-vault`, `10-target-propagation`, `schema-before-changes`
**Bad**: `vault`, `parity`, `no-docker`

---

## Notes for Implementers

- CONSTRAINTS.md is loaded at **every session start** — it must remain a single file, fully in-context
- Never split into individual `constraints/` files — the single-file model is intentional (D028)
- The file has four sections: Governance, Constraint Index, Constraint Definitions, Change Log — do not add or remove sections
- The Change Log is append-only — the `g-go-verify` agent uses it to detect unauthorized constraint changes
