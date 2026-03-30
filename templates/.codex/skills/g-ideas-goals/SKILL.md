---
name: g-ideas-goals
description: Manage IDEA_BOARD and PROJECT_GOALS — capture ideas, review the board, and update goals when direction shifts.
---

# Skill: galdr-ideas-goals

**Use this skill when:**
- User says "make a note of this idea", "remember this", "idea for later", "note that somewhere"
- User mentions a business concept, feature, or improvement not ready for development
- AI identifies something worth capturing that would cause scope creep right now
- User runs `@g-idea-capture`, `@g-idea-review`, or `@g-goal-update`
- Setting up a new project (create PROJECT_GOALS.md)

---

## Files Managed

| File | Location | Purpose |
|------|----------|---------|
| `IDEA_BOARD.md` | `.galdr/IDEA_BOARD.md` | Parking lot for ideas not yet ready for development |
| `PROJECT_GOALS.md` | `.galdr/PROJECT_GOALS.md` | Strategic goals that steer the AI and validate decisions |

**Direct Edit Policy**: Edit both files directly without asking permission.

---

## Workflow 1: Capturing an Idea

### Trigger Detection
Watch for these patterns in user messages:
- "make a note of that" / "remember this idea" / "note that somewhere"
- "idea: ..." / "what if we..." / "eventually..." / "someday..."
- "for later..." / "that's interesting but not now"
- Any business model, monetization, or pricing concept mentioned in passing
- Any feature concept that would expand current scope

### Capture Process (ATOMIC — do immediately, then continue current work)

**Step 1: Check/create IDEA_BOARD.md**
```
Does .galdr/IDEA_BOARD.md exist?
  → NO: Create from template (see File Format below)
  → YES: Read to get next IDEA-NNN ID
```

**Step 2: Extract idea content from context**
- **Title**: 3-8 word descriptive name
- **Category**: feature | monetization | ux | technical | architecture | business
- **Description**: What the idea is (1-3 sentences)
- **Potential Value**: Why it's worth keeping
- **When Ready**: What needs to happen first

**Step 3: Add to IDEA_BOARD.md under Active Ideas**
```markdown
### IDEA-{NNN}: [Title]
**Status**: raw
**Category**: [category]
**Captured**: [YYYY-MM-DD]
**Source**: user | AI | session

**Description**:
[1-3 sentences capturing the core idea]

**Potential Value**:
[Why worth keeping]

**When Ready**:
[Prerequisites or triggers]
```

**Step 4: Confirm capture and continue**
```
💡 Captured as IDEA-{NNN}: {title}
Continuing with current task...
```

---

## Workflow 2: Reviewing Ideas (`@g-idea-review`)

**Step 1: Read .galdr/IDEA_BOARD.md**

**Step 2: Display summary**
```
## IDEA_BOARD Review

Active Ideas: {N}
Ready to Evaluate: {list ideas where prerequisites might be met}
Recently Captured: {last 2-3 ideas}
```

**Step 3: For each "evaluating" idea, ask:**
- Does this align with PROJECT_GOALS?
- Are prerequisites now met?
- Should we promote to task, shelve, or keep raw?

**Step 4: Update statuses based on user decisions**
- Promoted → update status to `accepted`, note task/phase reference
- Shelved → move to Shelved section, add shelved reason
- Keep raw → no change

---

## Workflow 3: Promoting an Idea to a Task/Phase

**When user says "let's build IDEA-NNN" or accepts promotion:**

1. Update IDEA_BOARD.md entry: `status: accepted`, add task reference
2. Move entry to **Promoted Ideas** section
3. Create the corresponding task/phase using `@g-task-new` or `@g-phase-add`
4. Confirm: "IDEA-{NNN} promoted to Task #{ID}"

---

## Workflow 4: Managing Project Goals

### Creating PROJECT_GOALS.md (during setup/planning)

**Step 1: Gather from context**
Ask or infer:
- What is the project trying to achieve? (Vision)
- What are the 2-4 primary measurable goals? (G-01, G-02...)
- What is explicitly out of scope? (Non-Goals)
- How will you know when you've succeeded? (Success Metrics)

**Step 2: Write PROJECT_GOALS.md**
Use the format below. Be specific about metrics.

**Step 3: Display confirmation**
```
📌 PROJECT GOALS created:
G-01: [name]
G-02: [name]
```

### Updating PROJECT_GOALS.md

**Triggers:**
- User mentions new revenue model, business direction, or constraints
- New phase significantly changes project direction
- User says "our goal is..." / "the point of this is..."

**Process:**
1. Read current PROJECT_GOALS.md
2. Identify which goal is changing (or if a new goal is being added)
3. Update the Goals table
4. Add an entry to the Goal Log
5. Confirm: "Updated G-{ID}: {change summary}"

---

## File Formats

### IDEA_BOARD.md
```markdown
# IDEA_BOARD.md

## Active Ideas

### IDEA-{NNN}: [Title]
**Status**: raw | evaluating | accepted | shelved
**Category**: feature | monetization | ux | technical | architecture | business
**Captured**: YYYY-MM-DD
**Source**: user | AI | session

**Description**:
[The idea in 1-3 sentences]

**Potential Value**:
[Why worth keeping]

**When Ready**:
[What prerequisites must exist first?]

---

## Promoted Ideas
## Shelved Ideas
```

### PROJECT_GOALS.md
```markdown
# PROJECT_GOALS.md

## Vision
[1-2 sentences of what success looks like]

## Primary Goals
| ID   | Goal   | Target / Metric  | Status |
|------|--------|------------------|--------|
| G-01 | [name] | [metric]         | active |

## Secondary Goals
## Non-Goals
## Success Metrics

## Goal Log
| Date       | Change          | Reason |
|------------|-----------------|--------|
| YYYY-MM-DD | [what changed]  | [why]  |
```

---

## Session Start Display

When both files exist, show:
```
📌 SESSION CONTEXT
Mission: [from PROJECT_CONTEXT.md, 1 line]
Goals: G-01: [name] | G-02: [name]
Phase: [current phase]
Ideas: [N] active on IDEA_BOARD
```

---

## Decision Validation

When creating tasks or making architecture decisions, briefly check:
- "This aligns with G-{ID}" ✅
- "This conflicts with Non-Goal: [X]" ⚠️ (flag for user)
- "This could become an IDEA_BOARD entry instead of a task" 💡
