Activate `g-skl-dependency-graph` to generate or refresh `.galdr/DEPENDENCY_GRAPH.md`.

Reads all `.galdr/tasks/` files, builds the dependency graph, computes the critical path, identifies blockers and orphan tasks, and writes a Mermaid diagram to `.galdr/DEPENDENCY_GRAPH.md`.

Use when:
- You want to see what's blocking what
- You've added or changed task dependencies
- You want to know the critical path to completion
