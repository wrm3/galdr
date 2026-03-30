---
description: "Activate workflow management for task expansion and sprint planning"
---

Activate workflow management: $ARGUMENTS

## What This Command Does

Activates the workflow management system for task expansion, sprint planning, and methodology integration.

## Workflow Features

### 1. Task Complexity Assessment
I'll evaluate tasks using these criteria (1-10+ scale):
- **Estimated Effort** (4 pts): Task takes >2-3 developer days
- **Cross-Subsystem Impact** (3 pts): Affects multiple subsystems
- **Multiple Components** (3 pts): Changes across unrelated modules
- **High Uncertainty** (2 pts): Requirements unclear
- **Multiple Outcomes** (2 pts): Several distinct deliverables
- **Dependency Blocking** (2 pts): Large prerequisite for other tasks

**Complexity Matrix:**
- 0-3 points: Simple Task → Proceed normally
- 4-6 points: Moderate Task → Consider expansion
- 7-10 points: Complex Task → **Expansion required**
- 11+ points: High Complex → **Must expand before creation**

### 2. Task Expansion
For complex tasks (score ≥7), I'll:
- Break down into logical sub-tasks
- Align sub-tasks with subsystem boundaries
- Create sub-task files: `task{parent_id}-{sub_id}_name.md`
- Update parent task with references

### 3. Sprint Planning
I'll help organize work into sprints:
- **Story Point Estimation**:
  - 1 SP: Minor fixes (< 1 hour)
  - 2 SP: Small tasks (1-4 hours)
  - 3 SP: Medium complexity (4-8 hours)
  - 5 SP: Complex features (1-2 days)
  - 8 SP: Large tasks (needs expansion)
- **Capacity Planning**: Target 70% of velocity
- **Priority Mapping**: Critical/High priority first
- **Dependency Ordering**: Respect task dependencies

### 4. Kanban Flow Management
**Default WIP Limits:**
- Pending: unlimited
- In Progress: 3
- Review: 2
- Testing: 2
- Deployment: 1

**Metrics Tracked:**
- Lead Time: Creation to completion
- Cycle Time: Start to completion
- Throughput: Tasks per period
- Flow Efficiency: Active vs total time

### 5. Workflow Visualization
I can generate Mermaid diagrams for:
- Task dependency graphs
- System architecture
- Process workflows
- Data flow diagrams

## When to Use
- Managing complex tasks that need breakdown
- Setting up sprint planning
- Analyzing work flow bottlenecks
- Generating system visualizations
- Optimizing team workflow

## What I Need From You
- Current task or area of focus
- Specific workflow concern (optional)
- Sprint duration preference (optional)

Let's optimize your workflow!
