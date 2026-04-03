---
name: g-planning
description: Create and manage plans, PRDs, and phase docs in .galdr/. For plan, PRD, requirements, phases, scope, project planning.
---

# galdr Planning Skill

Create and manage comprehensive project plans, Product Requirements Documents (PRDs), and phase specifications using the galdr planning system. This Skill provides structured planning workflows that prevent over-engineering while ensuring thorough requirements gathering.

## System Overview

the galdr planning system uses:
- **PLAN.md**: `.galdr/PLAN.md` - Master strategy (above individual PRDs)
- **PRDs**: `.galdr/prds/` - One or more product requirement documents
- **Phases**: `.galdr/phases/` - Optional milestone specifications (organizational; v3 task IDs are sequential)
- **Project**: `.galdr/PROJECT.md` - Mission, goals, and **Project Linking**
- **Constraints**: `.galdr/CONSTRAINTS.md` - Non-negotiable rules
- **Tasks**: Links to `.galdr/TASKS.md` for implementation tracking

## PRD Structure

### File locations
- **Strategy**: `.galdr/PLAN.md` (master plan)
- **PRDs**: `.galdr/prds/*.md` (one or more requirement docs)

### 10-Section PRD Template

#### 1. Product Overview
- **1.1 Document title and version**: PRD title and version number
- **1.2 Product summary**: 2-3 paragraph overview

#### 2. Goals
- **2.1 Business goals**: Business objectives
- **2.2 User goals**: What users aim to achieve
- **2.3 Non-goals**: Explicitly out-of-scope items

#### 3. User Personas
- **3.1 Key user types**: Primary user categories
- **3.2 Basic persona details**: Brief persona descriptions
- **3.3 Role-based access**: Permissions and access levels

#### 4. Phases / milestones
- **4.1 Project phases**: Milestone list (names, objectives). **v3:** task IDs are **sequential** — phases do not own numeric ID bands.
- **4.2 Phase references**: Links to optional `phases/` docs and to `TASKS.md` sections

#### 5. User Experience
- **5.1 Entry points & first-time user flow**: Initial access patterns
- **5.2 Core experience**: Main user workflows
- **5.3 Advanced features & edge cases**: Less common scenarios
- **5.4 UI/UX highlights**: Key design principles

#### 6. Narrative
Single paragraph describing user journey and benefits

#### 7. Success Metrics
- **7.1 User-centric metrics**: Task completion, satisfaction
- **7.2 Business metrics**: Conversion, revenue impact
- **7.3 Technical metrics**: Performance, error rates

#### 8. Technical Considerations
- **8.1 Affected subsystems**: Primary and secondary systems
- **8.2 Integration points**: External system interactions
- **8.3 Data storage & privacy**: Data handling, compliance
- **8.4 Scalability & performance**: Load expectations, targets
- **8.5 Potential challenges**: Risks and technical hurdles

#### 9. Milestones & Sequencing
- **9.1 Project estimate**: Small/Medium/Large with time estimate
- **9.2 Team size & composition**: Required team structure
- **9.3 Suggested phases**: Implementation phases with deliverables

#### 10. User Stories
Individual user stories with:
- **ID**: US-001, US-002, etc.
- **Description**: As a [persona], I want to [action] so that [benefit]
- **Acceptance Criteria**: Specific, measurable outcomes

## Phase Management

### Phase Document Structure
**Location**: `.galdr/phases/phase{N}_{kebab-case-name}.md` (e.g., `phase0_setup.md`, `phase1_foundation.md`)

**Template**:
```markdown
# Phase N: [Phase Name]

## Overview
[Brief description of the phase objectives]

## Task numbering (v3)
- Global **sequential** IDs — next ID = max existing task id + 1 (see `TASKS.md` and `.galdr/tasks/`)
- This phase file does **not** define a reserved ID range

## Objectives
- [Objective 1]
- [Objective 2]

## Deliverables
- [Deliverable 1]
- [Deliverable 2]

## Technical Considerations
- **Subsystems**: [List affected subsystems]
- **Dependencies**: [List phase dependencies]
- **Prerequisites**: [Prior phases that must complete]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Related Tasks
- Links to tasks in TASKS.md that implement this phase
```

### Phase Naming Convention
- Format: `phase{N}_{kebab-case-name}.md`
- Examples: `phase0_setup.md`, `phase1_foundation.md`, `phase2_core-development.md`
- Include phase number prefix with underscore separator
- Use hyphens within the name portion for multi-word names

### Phase-Task Integration
- Tasks reference phases via `phase:` field in YAML
- Phase documents list implementing tasks
- Phase completion tracked through task completion

## Scope Validation

### Mandatory Questions (Ask Before Creating PRD)

**Purpose**: Prevent over-engineering and clarify requirements

#### 1. User Context & Deployment
"Intended for personal use, small team, or broader deployment?"
- **Personal (1 user)**: Simple, file-based, minimal security
- **Small team (2-10)**: Basic sharing, simple user management
- **Broader (10+)**: Full authentication, role management, scalability

#### 2. Security Requirements
"Security expectations?"
- **Minimal**: Basic validation, no authentication
- **Standard**: User auth, session management, basic authorization
- **Enhanced**: Role-based access, encryption, audit trails
- **Enterprise**: SAML/SSO, compliance, advanced security

#### 3. Scalability Expectations
"Performance and scalability expectations?"
- **Basic**: Works for expected load, simple architecture
- **Moderate**: Handles growth, some optimization
- **High**: Speed-optimized, caching, efficient queries
- **Enterprise**: Load balancing, clustering, horizontal scaling

#### 4. Feature Complexity
"How much complexity comfortable with?"
- **Minimal**: Core functionality, keep simple
- **Standard**: Core plus reasonable conveniences
- **Feature-Rich**: Comprehensive with advanced options
- **Enterprise**: Full-featured with extensive configuration

#### 5. Integration Requirements
"Integration needs?"
- **Standalone**: No external integrations
- **Basic**: File import/export, basic API
- **Standard**: REST API, webhooks, common integrations
- **Enterprise**: Comprehensive API, message queues, enterprise systems

### Over-Engineering Prevention Rules

**Apply these defaults unless explicitly requested:**
- **Authentication**: Don't add role permissions unless requested
- **Database**: Use simple file-based unless DB explicitly requested
- **API**: Don't add comprehensive REST beyond required
- **Architecture**: Default monolith unless scale requires separation

## Planning Questionnaire

### 27-Question Framework

Use this comprehensive questionnaire for thorough requirements gathering. Ask questions progressively, not all at once.

#### Phase 1: Project Context (Q1-Q7)

**Q1**: Primary problem this system solves?
- Follow-up: Who experiences it, how handled today?

**Q2**: What does success look like?
- Follow-up: How measured, failure indicators?

**Q3**: Replacing existing or creating new?
- If replacing: pain points
- If new: why needed now?

**Q4**: Primary users?
- End users, Admins, Stakeholders, External

**Q5**: User count?
- Single, 2-10, 11-50, 51-200, 200+

**Q6**: Usage frequency?
- Occasional, Daily, Continuous, Peak periods

**Q7**: Access locations?
- Local, Office, Remote, Internet, Mobile

#### Phase 2: Technical Requirements (Q8-Q16)

**Q8**: Deployment?
- Local desktop, Local server, Cloud, Hybrid, No preference

**Q9**: Maintenance comfort?
- Minimal, Basic, Intermediate, Advanced

**Q10**: Integration needs?
- AD, Databases, Business apps, Monitoring, Backup

**Q11**: Data types?
- Public, Internal, PII, Financial, Healthcare, Regulated

**Q12**: Security requirements?
- Basic, Industry compliance, Government, Custom, None

**Q13**: Access control?
- All see all, Role-based, Department, Individual, External

**Q14**: Performance expectations?
- Basic seconds, Good <1s, High instant, Not critical

**Q15**: Data volume?
- Thousands, Hundreds of thousands, Millions, Billions, Growing

**Q16**: Peak usage?
- Consistent, Business hours, Month/quarter, Seasonal, Event-driven

#### Phase 3: Feature Scope (Q17-Q22)

**Q17**: Essential features (MVP)?
- List core features and deal-breakers

**Q18**: Nice-to-have features?
- List convenience and future enhancements

**Q19**: Features to avoid?
- Over-complexity, specific integrations, approaches

**Q20**: Priority: ease vs power?
- Ease, Power, Balanced, Depends on user

**Q21**: Interface examples you like?
- Reference apps, patterns, accessibility

**Q22**: User training investment?
- Self-explanatory, Brief, Formal, Complex OK

#### Phase 4: Timeline & Resources (Q23-Q27)

**Q23**: Timeline drivers?
- Business deadline, Budget, Competition, Regulatory, Personal

**Q24**: Delivery preference?
- Quick prototype, Phased, Complete, Iterative

**Q25**: Trade-offs?
- Core over polish, Polish over features, Speed over performance

**Q26**: Available resources?
- Dev time, Expertise, Budget, Third-party services

**Q27**: Hard constraints?
- Specific tech, No cloud, Budget limits, Policies

### Questionnaire Best Practices
- Ask 3-5 questions per message to avoid overwhelming
- Start with most important questions
- Follow up based on answers
- Conclude when clear sense of functionality emerges

## Codebase Analysis (Existing Projects)

### When to Use
When initializing galdr in existing projects with code

### Analysis Process

1. **File Structure Analysis**
   - Identify main components and modules
   - Determine project organization patterns
   - Map directory structure to functionality

2. **Dependency Mapping**
   - Map relationships between components
   - Identify external dependencies
   - Document integration points

3. **Phase Extraction**
   - Identify phases from code patterns
   - Determine phase boundaries
   - Group related functionality

4. **Subsystem Identification**
   - Group related functionality into subsystems
   - Define subsystem boundaries
   - Document subsystem responsibilities

5. **Integration Discovery**
   - Find external system connections
   - Identify APIs and services used
   - Document data flows

### Analysis Outputs
- Generate or update `.galdr/PLAN.md` and PRD file(s) under `.galdr/prds/` from current code structure
- Create phase documents for each major milestone (optional)
- Identify subsystems from code organization
- Document current architecture and integration points

## Planning Operations

### Create New PRD

**Process**:
1. Conduct scope validation (5 essential questions)
2. Optionally run planning questionnaire (27 questions)
3. Create or update `.galdr/PLAN.md` (strategy) and write the detailed PRD under `.galdr/prds/` (e.g. `prds/PRD.md` or `prds/<feature>.md`) using the 10-section template
4. Fill in all sections based on gathered requirements
5. Create phase documents in `phases/` folder when milestones need separate specs
6. Cross-link `PLAN.md`, `prds/`, and optional `phases/`

### Update Existing PRD

**Process**:
1. Read current PLAN.md
2. Identify sections to update
3. Make changes while preserving structure
4. Update version number
5. Update related phase documents if needed

### Create Phase Document

**Process**:
1. Determine phase number and name
2. Create `.galdr/phases/phaseN-name.md`
3. Use phase template
4. Fill in objectives, deliverables, criteria
5. Specify technical considerations
6. Add task references
7. Reference in PLAN.md section 4

### View Project Plan

**Process**:
1. Read `.galdr/PLAN.md`
2. Display relevant sections
3. Optionally read related phase documents
4. Show project context from `.galdr/PROJECT.md`

## Integration with Other Systems

### Link to Tasks
- Tasks reference phases via `phase:` YAML field
- Phase documents list implementing tasks
- Track phase progress through task completion

### Link to Bugs
- Bugs reference affected phases
- Phase documents list related bugs
- Phase impact assessment through bug analysis

### Link to project context
- `PLAN.md` and `prds/` align with `.galdr/PROJECT.md` mission and goals
- Optional phases support delivery milestones
- Scope boundaries defined in `PROJECT.md`, `CONSTRAINTS.md`, and PRDs

## File Organization

### Core Planning Files
- `.galdr/PLAN.md` - Master strategy
- `.galdr/prds/` - PRD documents
- `.galdr/phases/` - Optional phase documents
- `.galdr/PROJECT.md` - Mission, goals, project linking
- `.galdr/CONSTRAINTS.md` - Hard constraints

### Auto-Creation
Automatically create missing folders and files:
- `.galdr/` directory
- `.galdr/phases/` subdirectory
- `PLAN.md` with blank template if missing
- `prds/` with a starter PRD if missing
- `PROJECT.md` with template if missing

## Best Practices

### PRD Creation
1. Always conduct scope validation first
2. Use planning questionnaire for complex projects
3. Be specific about non-goals
4. Include concrete user stories
5. Define clear success metrics

### Phase Management
1. One phase per file
2. Clear, descriptive names
3. Link to implementing tasks
4. Track acceptance criteria
5. Update as project evolves

### Scope Control
1. Apply over-engineering prevention rules
2. Default to simplicity
3. Add complexity only when justified
4. Document scope boundaries clearly
5. Regular scope reviews

### Requirements Gathering
1. Ask questions progressively
2. Validate assumptions
3. Clarify ambiguities
4. Document decisions
5. Get stakeholder buy-in

## Common Workflows

### Workflow: Create PRD for New Project

1. User requests: "Create a project plan for a task management app"
2. Ask scope validation questions (5 essential)
3. Optionally ask planning questionnaire questions
4. Create `.galdr/PLAN.md` with 10 sections
5. Fill in sections based on answers
6. Create phase documents for each project phase
7. Link phases in PLAN.md section 4
8. Confirm PRD created

### Workflow: Add Phase to Existing Plan

1. User requests: "Add a new phase for reporting features"
2. Read existing PLAN.md
3. Determine next phase number
4. Ask clarifying questions about phase scope
5. Create `.galdr/phases/phaseN-reporting.md`
6. Fill in phase template
7. Update PLAN.md section 4.1 to include new phase
8. Confirm phase added

### Workflow: Conduct Scope Validation

1. User requests: "Help me plan a new project"
2. Ask: "Intended for personal use, small team, or broader deployment?"
3. Ask: "Security expectations?"
4. Ask: "Performance and scalability expectations?"
5. Ask: "How much complexity comfortable with?"
6. Ask: "Integration needs?"
7. Summarize answers and recommend approach
8. Proceed with PRD creation

### Workflow: Analyze Existing Codebase

1. User requests: "Create a plan for this existing project"
2. Analyze file structure
3. Identify main components
4. Extract phases from code organization
5. Map dependencies
6. Generate PLAN.md based on analysis
7. Create phase documents for major milestones
8. Confirm analysis complete

## Examples

### Example: Create Simple PRD

**User**: "Create a plan for a personal todo list app"

**Action**:
1. Conduct scope validation:
   - Personal use (1 user)
   - Minimal security
   - Basic performance
   - Minimal complexity
   - Standalone

2. Create `.galdr/PLAN.md`:

```markdown
# PRD: Personal Todo List App

## 1. Product overview
### 1.1 Document title and version
- PRD: Personal Todo List App
- Version: 1.0

### 1.2 Product summary
A simple, personal todo list application for managing daily tasks. The app allows a single user to create, organize, and track tasks with basic features like due dates and priorities. Designed for simplicity and ease of use without unnecessary complexity.

## 2. Goals
### 2.1 Business goals
- Provide personal productivity tool
- Maintain simplicity and ease of use
- Minimize maintenance overhead

### 2.2 User goals
- Quickly add and organize tasks
- Track task completion
- Set priorities and due dates
- View tasks at a glance

### 2.3 Non-goals
- Multi-user support
- Team collaboration features
- Complex project management
- Mobile apps (web only)
- Cloud sync

## 3. User personas
### 3.1 Key user types
- Individual user managing personal tasks

### 3.2 Basic persona details
- **Solo User**: Individual managing personal todo list for daily tasks and projects

### 3.3 Role-based access
- Single user with full access to all features

## 4. Phases / milestones
### 4.1 Delivery phases (v3: sequential task IDs — phases are labels only)
- **Phase 0: Setup & Infrastructure**
  - Project setup and environment configuration
  - Basic folder structure
  
- **Phase 1: Foundation**
  - Task data model
  - Basic task persistence
  
- **Phase 2: Core Development**
  - Task creation and editing
  - Task list display
  - Priority and due date support

### 4.2 Phase References
- phase0-setup.md
- phase1-foundation.md
- phase2-core.md

[Continue with remaining sections...]
```

3. Create phase documents in `phases/`
4. Confirm: "Created PRD for Personal Todo List App with 3 project phases"

### Example: Add Phase

**User**: "Add a phase for recurring tasks"

**Action**:
1. Read existing PLAN.md
2. Determine next phase number (e.g., Phase 3)
3. Create `.galdr/phases/phase3-recurring.md`:

```markdown
# Phase 3: Recurring Tasks

## Overview
Allow users to create tasks that automatically repeat on a schedule (daily, weekly, monthly).

## Task numbering (v3)
- Use the next sequential task IDs when creating work in TASKS.md (no fixed 300–399 band).

## Objectives
- Define recurrence pattern (daily, weekly, monthly)
- Automatically create new task instances
- Option to complete or skip individual instances
- Edit or delete recurring series

## Deliverables
- Recurrence UI components
- Recurrence scheduling logic
- Updated persistence layer
- Documentation

## Technical Considerations
- **Subsystems**: Task Management, Task Persistence
- **Dependencies**: Phase 1 (Foundation), Phase 2 (Core)
- **Prerequisites**: Core task features complete

## Acceptance Criteria
- [ ] User can set recurrence pattern when creating task
- [ ] New task instances created automatically
- [ ] User can complete individual instances
- [ ] User can edit or delete entire series
- [ ] Recurrence data persisted correctly

## Related Tasks
- Task 18: Implement recurrence UI (example sequential ID)
- Task 19: Implement recurrence logic
- Task 20: Update persistence layer
```

3. Update PLAN.md (and PRD in `prds/` if applicable) section 4.1:
```markdown
- **Phase 3: Recurring Tasks**
  - Create tasks with recurrence patterns
  - Automatic task instance creation
  - Manage recurring series
```

4. Confirm: "Added Phase 3: Recurring Tasks to plan"

## Compatibility Notes

This Skill works with Cursor's galdr planning system. The system uses:

- Standard markdown format
- Consistent section structure
- Git-friendly plain text files
- Sequential task IDs with optional milestone / phase documentation
