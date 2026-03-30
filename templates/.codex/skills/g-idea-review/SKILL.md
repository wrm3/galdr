---
name: g-idea-review
description: Review and evaluate IDEA_BOARD entries — change status, promote to tasks, or shelve ideas that won't be pursued.
---
# galdr-idea-review

## When to Use
@g-idea-review, "review ideas", "what ideas do we have?". Session planning.

## Steps

1. **Read IDEA_BOARD.md**: list all ideas with status `raw` or `evaluating`

2. **Display ideas**:
   ```
   💡 IDEA BOARD REVIEW
   ────────────────────
   IDEA-001: [Title] (raw) — category: feature
   [Description in 1 line]
   
   IDEA-002: [Title] (evaluating) — category: monetization
   [Description in 1 line]
   
   Total: N active ideas
   ```

3. **For each idea, show options**:
   - **Promote**: Create task/phase from this idea → triggers galdr-task-new
   - **Evaluate**: Needs more discussion → change status to `evaluating`
   - **Shelve**: Set aside → change status to `shelved`, add reason
   - **Keep raw**: Continue parking, check again later

4. **If promoting an idea**:
   - User must explicitly say "promote IDEA-NNN"
   - Create task with connection back: `notes: 'Promoted from IDEA-NNN'`
   - Update IDEA_BOARD: move to `## Promoted Ideas` section with task reference

5. **If shelving an idea**:
   - Move to `## Shelved Ideas` section
   - Add `**Shelved Date**: YYYY-MM-DD`
   - Add `**Reason**: [Why not pursuing]`

6. **Summary after review**:
   ```
   IDEA_BOARD Review Complete:
   - Promoted: N ideas → N tasks created
   - Shelved: N ideas
   - Still evaluating: N ideas
   - Kept raw: N ideas
   ```

## Rules
- NEVER auto-promote — require explicit user confirmation
- Shelved ideas stay in file for historical context
- Review IDEA_BOARD at start of every planning session
