---
name: g-workflow
description: Score task complexity, expand into sub-tasks, plan sprints, task dependency visualizations.
---
# galdr-workflow

## When to Use
@g-workflow, "expand task NNN", "plan sprint", "score complexity", "task dependencies".

## Mode A: Complexity Assessment + Expansion

### Score the Task (1-10+ points)
```
Estimated effort > 2-3 dev days           → +4
Affects multiple subsystems               → +3
Changes across unrelated modules          → +3
Requirements unclear/high uncertainty     → +2
Multiple distinct verifiable outcomes     → +2
Blocks many subsequent tasks              → +2
Exceptionally long acceptance criteria    → +1
Assigned > 5 story points                 → +1
```

**Score matrix**:
- 0-3: Proceed normally
- 4-6: Consider expansion
- 7+: MANDATORY expansion

### Expansion Process (Score ≥7)
1. Identify logical sub-goals
2. Check if shared module needed — if yes, sub-task 1 is extraction
3. Create sub-task files: `task{parent}-1_name.md`, `task{parent}-2_name.md`
4. Update parent task: `sub_tasks: ["42-1", "42-2"]`

## Mode B: Sprint Planning
1. Read all `[📋]` tasks from TASKS.md
2. Score each by: priority, dependencies resolved, blast_radius, goal alignment
3. Propose sprint:
   - Target 70% capacity (leave buffer)
   - Group by subsystem to minimize context switching
   - Dependencies respected

Sprint output:
```markdown
## Proposed Sprint (N story points / M days)
1. task5 — DB Schema (3 SP, no blockers)
2. task6 — API Layer (5 SP, needs task5)
3. task7 — Fix lint (1 SP, independent)
```

## Mode C: Dependency Diagram
Generate Mermaid flowchart from task files (see galdr-visualizer for full implementation):
```
flowchart TD
  subgraph M1["Milestone A"]
    T001["✅ task1"]
  end
  T001 --> T005
```
