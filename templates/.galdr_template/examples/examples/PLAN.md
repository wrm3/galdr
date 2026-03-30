# PRD: Example Project Plan

## 1. Product overview

### 1.1 Document title and version
- PRD: Example Project Plan
- Version: 1.0

### 1.2 Product summary
This is an example PRD demonstrating the galdr task management system structure. It shows how to organize project requirements, phases, and user stories using the standardized template. The galdr system works with Cursor IDE to provide AI-assisted task management with phase-based organization.

## 2. Goals

### 2.1 Business goals
- Demonstrate PRD template usage
- Provide example for new users
- Showcase phase-based organization
- Illustrate user story format

### 2.2 User goals
- Understand PRD structure
- Learn task organization patterns
- See example phase definitions
- Follow template for new projects

### 2.3 Non-goals
- Production-ready implementation
- Complete feature set
- Detailed technical specifications
- Performance benchmarking

## 3. User personas

### 3.1 Key user types
- New galdr users
- Project managers
- Development team leads
- Solo developers

### 3.2 Basic persona details
- **New User**: Learning galdr, needs clear examples
- **Project Manager**: Tracking team progress, needs visibility
- **Tech Lead**: Planning development, needs structure
- **Solo Developer**: Managing personal projects, needs simplicity

### 3.3 Role-based access
- **Developer**: Full read/write access to tasks and plans
- **Project Manager**: Read/write access to plans and tasks
- **Contributor**: Read access to plans, write access to assigned tasks

## 4. Phases

### 4.1 Phase Overview

Project work is organized into phases with reserved task ID ranges:

- **Phase 0: Setup & Infrastructure** (Task IDs: 1-99)
  - Environment setup and configuration
  - Initial folder structure creation
  - Status: [ ] Pending

- **Phase 1: Foundation** (Task IDs: 100-199)
  - Core functionality implementation
  - Database schema design
  - Status: [ ] Pending

- **Phase 2: Core Development** (Task IDs: 200-299)
  - Main feature development
  - API implementation
  - Status: [ ] Pending

### 4.2 Phase References
- Phase documents: `.galdr/phases/`
- Phase template: `.galdr/templates/phase_template.md`

### 4.3 Adding New Phases
- Use `@g-phase-add` in Cursor
- Phases can be added at any time as project vision clarifies
- Gaps in numbering allowed for pivots

## 5. User experience

### 5.1 Entry points & first-time user flow
**For New Users:**
1. Copy galdr template to project
2. Run `@g-setup` to initialize
3. Create first task using natural language
4. View TASKS.md for task overview

**For Existing Users:**
1. Open project in Cursor
2. Use `@g-status` for overview
3. Create/update tasks as needed

### 5.2 Core experience
**Creating a Task:**
1. User describes task in natural language
2. galdr-task-management skill activates
3. Task file created in `.galdr/tasks/`
4. TASKS.md updated with new entry

**Tracking Progress:**
1. View TASKS.md for task list
2. Check individual task files for details
3. Update status as work progresses

### 5.3 Advanced features & edge cases
- Sub-task creation for complex work
- Bug tracking with BUGS.md integration
- Phase completion gates with SWOT analysis
- Retroactive task documentation

### 5.4 UI/UX highlights
- Natural language interaction
- Windows-safe emoji indicators
- YAML frontmatter for structure
- Markdown for human readability

## 6. Narrative
A developer starts a new project and copies the galdr template. They run `@g-setup` in Cursor, which creates the folder structure and initial files. When they describe their first feature, the skill creates a task file with proper YAML frontmatter. As they work, they update task status, and TASKS.md reflects current progress with emoji indicators. When a phase completes, they receive a SWOT analysis and commit prompt before moving to the next phase.

## 7. Success metrics

### 7.1 User-centric metrics
- Time to create first task: < 2 minutes
- Task creation success rate: > 95%
- User satisfaction: > 4/5

### 7.2 Business metrics
- Template adoption rate
- Tasks completed per project
- Phase completion rate

### 7.3 Technical metrics
- File format compliance: 100%
- Skill activation accuracy: > 90%
- Zero data corruption incidents

## 8. Technical considerations

### 8.1 Affected subsystems
- **Primary subsystems**:
  - Cursor rules system
  - Skill activation
  - File I/O operations

- **Secondary subsystems**:
  - Git version control
  - Markdown rendering

### 8.2 Integration points
- Cursor rules (`.cursor/rules/`)
- Cursor skills (`.cursor/skills/`)
- Cursor commands (`.cursor/commands/`)
- File system for data storage
- Git for version control

### 8.3 Data storage & privacy
- All data stored locally in project directory
- No cloud sync required
- Standard file permissions apply
- Git handles versioning

### 8.4 Scalability & performance
- File-based system scales to hundreds of tasks
- Minimal memory footprint
- Fast file I/O operations

### 8.5 Potential challenges
- Large task lists may need filtering
- Complex dependencies need visualization
- Team coordination across files

## 9. Milestones & sequencing

### 9.1 Project estimate
- **Small**: 1-2 weeks for basic implementation

### 9.2 Team size & composition
- Solo developer or small team (1-3 people)

### 9.3 Suggested phases

- **Phase 0: Setup** (1-2 days)
  - Key deliverables:
    - Folder structure
    - Initial configuration
    - Template files

- **Phase 1: Foundation** (3-5 days)
  - Key deliverables:
    - Core functionality
    - Basic workflows
    - Testing setup

- **Phase 2: Enhancement** (5-7 days)
  - Key deliverables:
    - Advanced features
    - Documentation
    - Polish

## 10. User stories

### 10.1 Task Creation
- **ID**: US-001
- **Description**: As a developer, I want to create tasks using natural language, so that I can focus on work instead of syntax.
- **Acceptance Criteria**:
  - Task created with proper YAML frontmatter
  - TASKS.md updated with new entry
  - Task file follows naming convention

### 10.2 Status Tracking
- **ID**: US-002
- **Description**: As a project manager, I want to view task status at a glance, so that I can track project progress.
- **Acceptance Criteria**:
  - TASKS.md shows emoji status indicators
  - Task files include status field
  - Status updates are immediate

### 10.3 Phase Organization
- **ID**: US-003
- **Description**: As a tech lead, I want to organize work into phases, so that I can plan milestones effectively.
- **Acceptance Criteria**:
  - Tasks assigned to phases by ID range
  - Phase documents in phases/ folder
  - Phase completion gates enforced
