---
name: g-plan
description: Create or update PRD files under `.galdr/prds/` with 27-question process, scope validation, subsystems, and planning (align with `.galdr/PLAN.md`).
---
# galdr-plan

## When to Use
@g-plan, "create plan", "define requirements", "write PRD". New projects or major feature planning.

## Steps

1. **Scope validation questions** (ask first, before writing anything):
   1. Personal use / small team (2-10) / broader deployment (10+)?
   2. Security level: minimal / standard / enhanced / enterprise?
   3. Scalability: basic / moderate / high / enterprise?
   4. Feature complexity: minimal / standard / feature-rich?
   5. Integrations: standalone / basic / standard / enterprise?

2. **Gather requirements** (ask 27-question framework if needed):
   - Project context (Q1-7): problem, success, users, scale, frequency
   - Technical (Q8-16): deployment, maintenance, security, performance, data
   - Features (Q17-22): MVP, nice-to-have, avoid, priorities
   - Timeline (Q23-27): drivers, delivery, constraints

3. **Identify shared modules** (BEFORE writing feature sections):
   "What logic will be needed by 2+ features/subsystems?"
   → Plan extraction to `lib/` before implementation begins

4. **Write PRD file(s)** under `.galdr/prds/` (e.g. `.galdr/prds/PRD.md` for a single doc, or `.galdr/prds/<topic>.md` for multiple). Ensure `.galdr/PLAN.md` stays the master strategy doc above individual PRDs.
   ```markdown
   # PRD: [Project Name]
   
   ## 1. Product Overview
   ### 1.1 Document Title and Version
   ### 1.2 Product Summary
   
   ## 2. Goals
   ### 2.1 Business Goals
   ### 2.2 User Goals
   ### 2.3 Non-Goals
   
   ## 3. User Personas
   ## 4. Milestones / sequencing (reference TASKS.md; v3 uses sequential task IDs)
   ## 5. User Experience
   ## 6. Narrative
   ## 7. Success Metrics
   ## 8. Technical Considerations
   ### 8.6 Shared Modules and Reusability
   ## 9. Milestones & Sequencing
   ## 10. User Stories
   ```

5. **Generate TASKS.md skeleton** with initial tasks (sequential IDs; optional milestone section headers)

6. **Create SUBSYSTEMS.md** with detected/defined subsystems

7. **Offer `.galdr/CONSTRAINTS.md`** creation for non-negotiable constraints
