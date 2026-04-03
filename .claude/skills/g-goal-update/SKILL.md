---
name: g-goal-update
description: Create or update the Goals section in `.galdr/PROJECT.md` with strategic goals, success metrics, and non-goals. Called when project direction changes or goals need clarification.
---
# galdr-goal-update

## When to Use
@g-goal-update, "update goals", "define success criteria", "what are our goals?". Called during @g-setup and @g-plan.

## Steps

1. **Check `.galdr/PROJECT.md` for a Goals section** (and mission/context in the same file):
   - NO / empty → create or fill from scratch (step 2)
   - Placeholders like `{Goal name}` → regenerate (step 2)
   - Real content → update/extend (step 3)

2. **Gather goals** (ask user if not clear from context):
   - "What is the primary outcome this project must achieve?"
   - "What does success look like in 3-6 months?"
   - "What are we explicitly NOT building?"
   - "How will we measure success?"

3. **Write/update `PROJECT.md`** (keep mission/context in the same file; ensure a **Goals** section exists):
```markdown
# PROJECT.md

## Mission
[existing mission text — preserve]

## Goals

### Vision
[1-2 sentences: what does success look like for this project?]

### Primary Goals
| ID | Goal | Target / Metric | Status |
|---|---|---|---|
| G-01 | [Goal name] | [Measurable outcome] | active |
| G-02 | [Goal name] | [Measurable outcome] | active |

### Secondary Goals
- **[Goal name]**: [How it supports primary goals]

### Non-Goals (Explicitly Out of Scope)
- [Things we are NOT building]
- [Scope boundaries]

### Success Metrics
- [How we know we've achieved the vision]
- [Quantifiable targets]

### Goal Log
| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | [Initial creation] | Project setup |
```

4. **Display at session start** (load into context):
   ```
   📌 PROJECT GOALS
   G-01: [name] — [one line]
   G-02: [name] — [one line]
   ```

5. **Goal change protocol**: Never delete — mark as `complete` or `retired` + add Goal Log entry
