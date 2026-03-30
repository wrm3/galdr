---
name: g-idea-capture
description: Capture a new idea to IDEA_BOARD.md immediately. Triggered by user saying "make a note", "idea:", "what if we", "someday", "for later", "remember this".
---
# galdr-idea-capture

## Steps

1. **Determine next IDEA ID**: read `.galdr/IDEA_BOARD.md`, find highest IDEA-NNN, increment

2. **Classify the idea**:
   - `feature` — new user-facing capability
   - `monetization` — revenue or pricing
   - `ux` — user experience improvement
   - `technical` — architecture, performance, tooling
   - `architecture` — structural/infrastructure change
   - `business` — strategy, positioning

3. **Add entry to IDEA_BOARD.md** under "## Active Ideas":
```markdown
### IDEA-NNN: [Title — concise but specific]
**Status**: raw
**Category**: feature | monetization | ux | technical | architecture | business
**Captured**: YYYY-MM-DD
**Source**: user | AI | session

**Description**:
[The idea in 1-3 sentences. Specific enough to reconstruct intent later.]

**Potential Value**:
[Why this is worth keeping — problem solved, revenue potential, etc.]

**When Ready**:
[What prerequisites or triggers would make this worth developing?]

---
```

4. **Confirm immediately**: "Captured as IDEA-{NNN}: {title}"

5. **Continue current work** — do NOT derail the session

## Rules
- NEVER auto-promote to task — requires explicit user decision
- Capture first, evaluate later
- AI-identified scope creep → offer capture: "Should I add this to IDEA_BOARD? It could derail the current task."
