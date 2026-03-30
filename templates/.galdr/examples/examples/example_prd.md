# Example PRD: Task Management Web Application

**This is a complete, real-world example of a PRD created using the galdr planning system.**
**File location in real projects**: `.galdr/PLAN.md`

---

# PRD: Task Management Web Application

## 1. Product Overview

### 1.1 Document Title and Version
- PRD: Task Management Web Application
- Version: 1.0
- Created: 2026-01-15

### 1.2 Product Summary

A web-based task management application designed for small teams (2-10 users) to organize, track, and collaborate on projects. The application provides a simple, intuitive interface for creating tasks, assigning them to team members, tracking progress, and managing deadlines. Built with React frontend and Python/Flask backend, using PostgreSQL for data persistence.

The application focuses on simplicity and ease of use, avoiding complex project management overhead in favor of core task tracking that teams can adopt immediately without extensive training.

---

## 2. Goals

### 2.1 Business Goals
- Provide a lightweight alternative to complex project management tools
- Enable small teams to track work without administrative overhead
- Create a solid foundation for future feature expansion
- Maintain low operational and maintenance costs

### 2.2 User Goals
- Quickly create and organize tasks
- Assign tasks to specific team members
- Track task progress and completion status
- Set and monitor deadlines
- Filter and search through task history

### 2.3 Non-Goals
- Complex project hierarchies or sub-projects
- Time tracking or billing features
- Gantt charts or advanced visualizations
- Native mobile apps (web-responsive only)
- Real-time collaborative editing
- Third-party integrations (v1.0 scope)

---

## 3. User Personas

### 3.1 Key User Types
- Team members (individual contributors)
- Team leads (task creators and work coordinators)
- Project managers (progress viewers and reporters)

### 3.2 Basic Persona Details
- **Team Member (Maya)**: Individual contributor who creates personal tasks and updates status on tasks assigned to her. Values speed — wants to log work and move on.
- **Team Lead (Carlos)**: Creates tasks for the sprint, assigns to team members, and checks daily progress. Needs clear overview of who is working on what.
- **Project Manager (Priya)**: Monitors overall project status and produces weekly status reports. Rarely creates tasks — primarily a read-only viewer.

### 3.3 Role-Based Access
- **Team Member**: Create own tasks, view assigned tasks, update own task status
- **Team Lead**: All team member permissions + create tasks for others, view all team tasks, reassign tasks
- **Project Manager**: Read-only access to all tasks, export reports

---

## 4. Phases

### 4.1 Phase Overview

| Phase | Tasks | Focus | Duration |
|-------|-------|-------|----------|
| Phase 0: Setup | 1-99 | Project structure, CI/CD, database setup | 1 week |
| Phase 1: Foundation | 100-199 | Auth, user mgmt, core API, data models | 2 weeks |
| Phase 2: Core Features | 200-299 | Task CRUD, assignment, status UI | 3 weeks |
| Phase 3: Enhancement | 300-399 | Search, filtering, reporting, polish | 2 weeks |

### 4.2 Phase Files
- `.galdr/phases/phase0_setup.md`
- `.galdr/phases/phase1_foundation.md`
- `.galdr/phases/phase2_core-features.md`
- `.galdr/phases/phase3_enhancement.md`

---

## 5. User Experience

### 5.1 Entry Points and First-Time User Flow
- Navigate to application URL
- Login page (email/password)
- First-time users see a brief onboarding screen (3 steps, skippable)
- After login: dashboard showing assigned tasks and upcoming deadlines

### 5.2 Core Experience
- **Dashboard**: Overview of assigned tasks, recent activity, tasks due today
- **Task List**: Filterable/sortable list of tasks (mine, assigned by me, all team)
- **Task Creation**: Simple form — title, description, assignee, priority, due date
- **Task Detail**: View full details, update status, leave comments, view history
- **Task Board**: Kanban-style view (Pending / In Progress / Done columns)

### 5.3 Advanced Features and Edge Cases
- Bulk task operations (mark multiple as complete)
- Task templates for recurring work
- CSV export of task history
- Task archiving for completed projects

### 5.4 UI/UX Highlights
- Clean, minimal design (Todoist-inspired)
- Responsive layout (desktop + tablet priority, mobile functional)
- Keyboard shortcuts for power users (N = new task, / = search)
- Color-coded priority levels (Critical=red, High=orange, Medium=blue, Low=gray)

---

## 6. Narrative

Carlos starts his Monday by opening the task board to review the sprint. He creates three new tasks for the week's goals, assigns two to Maya and one to himself, and sets due dates. Throughout the day, Maya updates her task statuses as she makes progress, and Carlos can see the board changing in real-time. On Friday, Priya logs in to review the week's completed work and generates a brief status report for leadership — all from the same simple interface that the team uses daily. Nobody needed training, nothing fell through the cracks.

---

## 7. Success Metrics

### 7.1 User-Centric Metrics
- Task completion rate: > 80% of tasks completed by their due date
- User adoption: 90% of team actively using the tool within 2 weeks of launch
- Tasks created per user per week: 5-10 (indicates active use)
- User satisfaction score: > 4.0/5.0 (quarterly survey)

### 7.2 Business Metrics
- Time saved vs. previous method: > 2 hours/week per user
- Missed deadlines reduction: > 30% reduction in first 3 months
- Onboarding time: New team member productive within 30 minutes

### 7.3 Technical Metrics
- Page load time: < 2 seconds (Lighthouse performance > 80)
- API response time: < 500ms for p95
- Uptime: > 99.5% monthly
- Error rate: < 0.1% of requests

---

## 8. Technical Considerations

### 8.1 Affected Subsystems

**Primary (directly implemented):**
- **Frontend (React + TypeScript)**: Task UI components, state management, routing
- **Backend (Python/Flask)**: Task API endpoints, authentication, business logic
- **Database (PostgreSQL)**: Task schema, user schema, relationships, indexes

**Secondary (integrated with):**
- **Authentication System**: User roles and JWT session management
- **Email System**: Task assignment notifications (future)
- **File Storage**: Task attachments (future)

### 8.2 Integration Points
- Email service (SMTP or SendGrid) for notifications — Phase 3
- File storage (S3 or local) for attachments — Phase 3

### 8.3 Data Storage and Privacy
- All user data stored in PostgreSQL with encryption at rest
- No PII beyond email addresses and names
- GDPR-compliant data deletion on user request
- Daily automated backups, 30-day retention

### 8.4 Scalability and Performance
- Expected load: 2-10 concurrent users (small team scope)
- Database: PostgreSQL with connection pooling (pgbouncer)
- Frontend: React with code splitting for fast initial load
- Static assets: served via CDN

### 8.5 Potential Challenges
- Real-time task updates without WebSockets (polling or SSE in Phase 3)
- Mobile responsiveness on very small screens
- Search performance with large task backlogs (> 10,000 tasks)

---

## 9. Milestones and Sequencing

### 9.1 Project Estimate
- **Medium**: 8 weeks for full implementation (all 4 phases)
- Core usable product (Phase 0-2): 6 weeks

### 9.2 Team Composition
- 1 Full-Stack Developer (primary)
- 1 Part-Time Frontend Reviewer
- 1 Part-Time PM (requirements, testing, acceptance)

### 9.3 Phase Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 0: Setup | 1 week | Project structure, CI/CD, database setup |
| Phase 1: Foundation | 2 weeks | Authentication, user management, base API |
| Phase 2: Core Features | 3 weeks | Task CRUD, assignment, status tracking, board view |
| Phase 3: Enhancement | 2 weeks | Search, filtering, reporting, accessibility |

---

## 10. User Stories

### US-001: Create Task
- **As a** team lead, **I want to** create a new task with title, assignee, and due date **so that** I can delegate work and track its progress.
- **Acceptance Criteria**:
  - Task creation form includes: title (required), description, assignee, priority, due date
  - Form validates required fields before submission
  - Created task immediately appears in the task list
  - Assignee receives in-app notification

### US-002: Update Task Status
- **As a** team member, **I want to** update my task's status **so that** my team can see my progress without me needing to send status updates.
- **Acceptance Criteria**:
  - Task detail page shows status dropdown (Pending, In Progress, Completed)
  - Status change saves immediately (no separate save button)
  - Status history is recorded with timestamp and user
  - Completed tasks move to the Done column on the board view

### US-003: View Team Tasks
- **As a** team lead, **I want to** see all team tasks in one view **so that** I can identify blockers and redistribute work as needed.
- **Acceptance Criteria**:
  - Task list can be filtered by assignee, status, priority, and date range
  - Default view shows all team tasks sorted by due date
  - Overdue tasks are visually highlighted
  - Task count shows per filter combination

### US-004: Search Tasks
- **As a** team member, **I want to** search for tasks by keyword **so that** I can quickly find related work or past decisions.
- **Acceptance Criteria**:
  - Search is available on the task list page (keyboard shortcut: `/`)
  - Search matches against task titles and descriptions
  - Results appear within 500ms
  - Works across all tasks the user has access to

### US-005: Export Task Report
- **As a** project manager, **I want to** export a task report to CSV **so that** I can create status updates for stakeholders who don't have access to the tool.
- **Acceptance Criteria**:
  - Export button available on the task list view
  - CSV includes: id, title, assignee, status, priority, due date, completed date
  - Exported data respects the current filter state
  - File downloads immediately without server-side processing delay

---

*This PRD was generated using the galdr planning system and demonstrates the full 10-section template.*
*Real PRDs live at `.galdr/PLAN.md` in the project repository.*
