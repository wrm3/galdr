---
description: "Capture an idea to IDEA_BOARD.md"
---

Capture an idea to IDEA_BOARD.md: {{args}}

## What This Workflow Does

Captures an idea to `.galdr/IDEA_BOARD.md` so it isn't lost.
Ideas are NOT tasks — they sit in a parking lot until consciously promoted.

## Capture Workflow

### 1. Parse the Idea
Extract from `{{args}}` (or ask if unclear):
- **Title**: 3-8 word descriptive name
- **Category**: feature | monetization | ux | technical | architecture | business
- **Description**: What the idea actually is (1-3 sentences)
- **Potential Value**: Why it's worth keeping
- **When Ready**: What needs to happen before this could be developed

### 2. Check IDEA_BOARD.md
- If `.galdr/IDEA_BOARD.md` doesn't exist: create it from the template
- Read to determine next IDEA-NNN ID

### 3. Add the Entry
Under **## Active Ideas**, add:
```markdown
### IDEA-{NNN}: [Title]
**Status**: raw
**Category**: [category]
**Captured**: [YYYY-MM-DD]
**Source**: user

**Description**:
[The idea in 1-3 sentences]

**Potential Value**:
[Why worth keeping]

**When Ready**:
[Prerequisites or triggers]
```

### 4. Confirm and Continue
```
💡 Captured as IDEA-{NNN}: {title}
```

## Examples

```
/g-idea-capture Add premium theme packs as $35 paywall upsell
/g-idea-capture Export scene as shareable GIF for social media
```

## Remember
- Ideas are NOT tasks — never create a task file from this workflow
- Capture first, evaluate later
