# Task Templates

## Overview

This document provides ready-to-use templates for different types of tasks in the galdr system. Copy these templates and customize them for your needs.

## Feature Task Template

Use this template for implementing new functionality.

```markdown
---
id: {next_id}
title: '{Action verb} {specific feature}'
type: feature
status: pending
priority: {critical|high|medium|low}
feature: {Feature Name}
subsystems: [{subsystem1}, {subsystem2}]
project_context: '{How this task supports project goals}'
dependencies: []
---

# Task {id}: {Title}

## Objective
{Clear, specific description of what needs to be accomplished}

## Background
{Context about why this task is needed, any relevant history}

## Acceptance Criteria
- [ ] {Specific, measurable outcome 1}
- [ ] {Specific, measurable outcome 2}
- [ ] {Specific, measurable outcome 3}
- [ ] Tests written and passing
- [ ] Documentation updated

## Implementation Notes
{Technical details, approach, constraints, considerations}

## Testing Plan
1. {Test scenario 1}
2. {Test scenario 2}
3. {Test scenario 3}

## Resource Requirements
- {Required tools, libraries, access}
- {Team members needed}
- {External dependencies}

## Success Metrics
- {How to measure success}
- {Performance targets}
- {Quality standards}
```

**Example:**
```markdown
---
id: 1
title: 'Implement user authentication'
type: feature
status: pending
priority: high
feature: User Authentication
subsystems: [authentication, database, api]
project_context: 'Enables secure user access, supporting core security requirements'
dependencies: []
---

# Task 1: Implement User Authentication

## Objective
Create a secure authentication system allowing users to register, login, and manage their sessions.

## Background
The application currently has no user authentication. This is required before implementing user-specific features planned for Q2.

## Acceptance Criteria
- [ ] Users can register with email and password
- [ ] Users can login with credentials
- [ ] Sessions are managed securely with JWT tokens
- [ ] Password reset functionality works
- [ ] Tests cover all authentication flows
- [ ] API documentation updated

## Implementation Notes
- Use bcrypt for password hashing
- JWT tokens expire after 24 hours
- Implement rate limiting on login endpoint
- Follow OWASP authentication best practices

## Testing Plan
1. Test successful registration flow
2. Test login with valid/invalid credentials
3. Test session expiration
4. Test password reset flow
5. Security testing for common vulnerabilities

## Resource Requirements
- bcrypt library
- JWT library
- Email service for password reset
- Security review from team lead

## Success Metrics
- 100% test coverage on auth flows
- No security vulnerabilities in scan
- Login response time < 500ms
```

## Bug Fix Task Template

Use this template for fixing bugs.

```markdown
---
id: {next_id}
title: '[BUG] {Brief description of the issue}'
type: bug_fix
status: pending
priority: {critical|high|medium|low}
feature: {Affected Feature}
subsystems: [{affected_subsystems}]
project_context: 'Resolves {bug_type} affecting {system_component}, maintaining {expected_behavior}'
bug_reference: BUG-{number}
severity: {critical|high|medium|low}
source: {user_reported|development|testing|production}
reproduction_steps: '{Step-by-step instructions}'
expected_behavior: '{What should happen}'
actual_behavior: '{What actually happens}'
dependencies: []
---

# Task {id}: [BUG] {Description}

## Objective
Fix {bug_type} that causes {problem}

## Bug Details
**Bug Reference**: BUG-{number}
**Severity**: {level}
**Source**: {source}
**Environment**: {OS, browser, version}

## Reproduction Steps
1. {Step 1}
2. {Step 2}
3. {Step 3}
**Result**: {What happens}

## Expected vs Actual Behavior
**Expected**: {what_should_happen}
**Actual**: {what_actually_happens}

## Root Cause Analysis
{Investigation findings, why the bug occurs}

## Fix Implementation
{Technical approach to fix the issue}

## Acceptance Criteria
- [ ] Bug can no longer be reproduced
- [ ] Fix doesn't introduce regressions
- [ ] Tests added to prevent recurrence
- [ ] Documentation updated if needed

## Testing Plan
- Test original reproduction steps
- Test related functionality
- Run regression tests
- Verify in production-like environment

## Related Issues
- {Links to related bugs or tasks}
```

**Example:**
```markdown
---
id: 15
title: '[BUG] Login button not responding to clicks'
type: bug_fix
status: in-progress
priority: critical
feature: User Authentication
subsystems: [frontend, authentication]
project_context: 'Resolves critical login issue affecting all users, maintaining user access capability'
bug_reference: BUG-001
severity: critical
source: production
reproduction_steps: '1. Navigate to login page\n2. Click "Login" button\n3. Nothing happens'
expected_behavior: 'Login modal should appear'
actual_behavior: 'Button click has no effect'
dependencies: []
---

# Task 15: [BUG] Login Button Not Responding

## Objective
Fix critical bug preventing users from accessing login functionality.

## Bug Details
**Bug Reference**: BUG-001
**Severity**: Critical
**Source**: Production
**Environment**: All browsers, Windows 11, macOS

## Reproduction Steps
1. Navigate to homepage (https://app.example.com)
2. Click "Login" button in top-right corner
3. Observe no response
**Result**: Button appears clickable but nothing happens

## Expected vs Actual Behavior
**Expected**: Login modal should appear with email/password fields
**Actual**: Button click has no visual or functional effect

## Root Cause Analysis
Event listener was removed during refactoring in commit abc123. The button element exists but has no click handler attached.

## Fix Implementation
1. Restore click event listener in `auth.js`
2. Add unit test to verify listener is attached
3. Add integration test for login flow

## Acceptance Criteria
- [ ] Login button responds to clicks
- [ ] Login modal appears correctly
- [ ] Unit test confirms event listener present
- [ ] Integration test covers full login flow
- [ ] Fix verified in production

## Testing Plan
- Test on Chrome, Firefox, Safari, Edge
- Test on Windows, macOS, Linux
- Test on mobile devices
- Verify no console errors
- Check analytics for successful logins

## Related Issues
- Related to refactoring in Task 12
```

## Sub-task Template

Use this template for breaking down complex tasks.

```markdown
---
id: "{parent_id}.{sub_number}"
title: '{Specific sub-task action}'
type: feature
status: pending
priority: {same_as_parent}
parent_task: {parent_id}
feature: {Same Feature}
subsystems: [{specific_subsystems}]
project_context: '{How this sub-task contributes to parent task goal}'
dependencies: []
---

# Task {parent_id}.{sub_number}: {Title}

## Objective
{Specific, focused objective for this sub-task}

## Parent Task
This is a sub-task of Task {parent_id}: {Parent Title}

## Scope
{What this sub-task covers, what it doesn't}

## Acceptance Criteria
- [ ] {Specific outcome 1}
- [ ] {Specific outcome 2}
- [ ] {Specific outcome 3}

## Implementation Notes
{Technical details specific to this sub-task}

## Dependencies
{Other sub-tasks or tasks this depends on}
```

**Example:**
```markdown
---
id: "42.1"
title: 'Setup database schema for migration'
type: feature
status: pending
priority: high
parent_task: 42
feature: Data Migration
subsystems: [database]
project_context: 'First step in data migration, establishes schema structure for user data transfer'
dependencies: []
---

# Task 42.1: Setup Database Schema

## Objective
Create and validate the database schema required for migrating user data from legacy system.

## Parent Task
This is a sub-task of Task 42: Migrate User Data from Legacy System

## Scope
**Includes:**
- Creating new tables for user data
- Defining indexes for performance
- Setting up foreign key constraints
- Creating migration tracking table

**Excludes:**
- Actual data migration (Task 42.2)
- Data validation (Task 42.3)

## Acceptance Criteria
- [ ] All tables created with correct schema
- [ ] Indexes created on frequently queried columns
- [ ] Foreign key constraints properly defined
- [ ] Migration tracking table ready
- [ ] Schema validated against requirements
- [ ] Database migration script tested

## Implementation Notes
- Use Alembic for schema migrations
- Follow naming conventions: `user_`, `legacy_`
- Add created_at, updated_at to all tables
- Use UUID for primary keys

## Dependencies
- Database server must be provisioned (infrastructure task)
- Access credentials must be configured
```

## Retroactive Fix Template

Use this template for documenting fixes completed in chat.

```markdown
---
id: {next_id}
title: '[RETROACTIVE] {Description of fix/improvement}'
type: retroactive_fix
status: completed
priority: {original_urgency_level}
created_date: '{fix_completion_date}'
completed_date: '{fix_completion_date}'
project_context: 'Documents previously completed {solution_type} that addressed {project_need}, maintaining {system_capability}'
subsystems: [{affected_subsystems}]
estimated_effort: '{actual_time_spent}'
actual_effort: '{actual_time_spent}'
---

# Task {id}: [RETROACTIVE] {Description}

## Objective
Document {fix_type} that was completed in chat session

## What Was Fixed
{Description of the problem that was solved}

## Solution Implemented
{Description of the solution and approach}

## Files Changed
- {file1}
- {file2}
- {file3}

## Impact
{How this fix improves the system}

## Lessons Learned
{Insights for preventing similar issues}

## Testing Performed
{What testing was done to verify the fix}

## Documentation Updated
{What documentation was updated}
```

**Example:**
```markdown
---
id: 16
title: '[RETROACTIVE] Fixed database query performance issue'
type: retroactive_fix
status: completed
priority: high
created_date: '2025-10-19'
completed_date: '2025-10-19'
project_context: 'Documents performance optimization that reduced query time from 5s to 0.2s, maintaining system responsiveness'
subsystems: [database, api]
estimated_effort: '2 hours'
actual_effort: '2 hours'
---

# Task 16: [RETROACTIVE] Database Query Performance

## Objective
Document the database query optimization completed during chat debugging session.

## What Was Fixed
User search queries were taking 5+ seconds to complete, causing timeouts and poor user experience. The issue affected all search operations across the application.

## Solution Implemented
1. Added composite index on (last_name, first_name, email)
2. Rewrote query to use index-friendly WHERE clauses
3. Implemented query result caching for common searches
4. Added query performance monitoring

## Files Changed
- `database/migrations/add_user_search_index.sql`
- `api/services/user_search.py`
- `api/utils/cache.py`
- `tests/test_user_search.py`

## Impact
- Query time reduced from 5s to 0.2s (96% improvement)
- User search now instant and responsive
- Reduced database load by 80%
- Improved overall application performance

## Lessons Learned
- Always profile queries before optimization
- Composite indexes are powerful for multi-column searches
- Caching common queries significantly reduces load
- Monitor query performance in production

## Testing Performed
- Benchmarked query performance before/after
- Tested with 100,000 user records
- Verified cache invalidation works correctly
- Load tested with concurrent searches

## Documentation Updated
- Added performance optimization guide
- Updated API documentation with caching behavior
- Documented index maintenance procedures
```

## Quick Reference

### Choosing the Right Template

| Situation | Template | Key Fields |
|-----------|----------|------------|
| New feature | Feature Task | type: feature |
| Fixing a bug | Bug Fix Task | type: bug_fix, bug_reference |
| Large task | Sub-task Template | parent_task, id: "X.Y" |
| Documenting completed work | Retroactive Fix | type: retroactive_fix, completed_date |

### Common Task Types

- `feature` - New functionality
- `bug_fix` - Fixing bugs
- `retroactive_fix` - Documenting completed fixes
- `refactor` - Code improvement
- `documentation` - Documentation work
- `testing` - Test creation
- `infrastructure` - DevOps work

### Priority Levels

- `critical` - Drop everything, fix now
- `high` - Important, do soon
- `medium` - Normal priority
- `low` - Nice to have

### Status Values

- `pending` - Not started
- `in-progress` - Currently working
- `completed` - Done
- `failed` - Attempted but failed
- `blocked` - Waiting on dependencies
- `cancelled` - No longer needed

