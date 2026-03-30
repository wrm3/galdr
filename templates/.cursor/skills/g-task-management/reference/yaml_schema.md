# YAML Frontmatter Schema

## Overview

This document provides the complete specification for YAML frontmatter used in galdr task files. All task files must include valid YAML frontmatter to ensure proper parsing and compatibility across IDEs.

## Required Fields

### id
- **Type:** Integer or String (for sub-tasks)
- **Required:** Yes
- **Description:** Unique identifier for the task
- **Format:** 
  - Main tasks: Integer (e.g., `1`, `42`, `100`)
  - Sub-tasks: String with dot notation (e.g., `"42.1"`, `"42.2"`)
- **Examples:**
  ```yaml
  id: 1
  id: 42
  id: "42.1"  # Sub-task (must be quoted)
  ```

### title
- **Type:** String
- **Required:** Yes
- **Description:** Brief, descriptive title for the task
- **Format:** Single-quoted string, 5-100 characters
- **Best Practices:**
  - Start with action verb (Create, Implement, Fix, Update)
  - Be specific but concise
  - Avoid redundant prefixes like "Task to..."
- **Examples:**
  ```yaml
  title: 'Implement user authentication'
  title: 'Fix login button not responding'
  title: '[BUG] Database connection timeout'
  title: '[RETROACTIVE] Optimized query performance'
  ```

### status
- **Type:** String (enum)
- **Required:** Yes
- **Description:** Current state of the task
- **Valid Values:**
  - `pending` - Not yet started
  - `in-progress` - Currently being worked on
  - `completed` - Successfully finished
  - `failed` - Attempted but failed
  - `blocked` - Cannot proceed due to dependencies
  - `cancelled` - No longer needed
- **Examples:**
  ```yaml
  status: pending
  status: in-progress
  status: completed
  ```

### priority
- **Type:** String (enum)
- **Required:** Yes
- **Description:** Importance/urgency level
- **Valid Values:**
  - `critical` - Must be done immediately
  - `high` - Important, should be done soon
  - `medium` - Normal priority
  - `low` - Nice to have, can wait
- **Examples:**
  ```yaml
  priority: critical
  priority: high
  priority: medium
  priority: low
  ```

## Optional Fields

### type
- **Type:** String (enum)
- **Required:** No (defaults to `feature`)
- **Description:** Category of task
- **Valid Values:**
  - `feature` - New functionality
  - `bug_fix` - Fixing a bug
  - `retroactive_fix` - Documenting completed fix
  - `refactor` - Code improvement
  - `documentation` - Documentation work
  - `testing` - Test creation/improvement
  - `infrastructure` - DevOps/infrastructure
- **Examples:**
  ```yaml
  type: feature
  type: bug_fix
  type: retroactive_fix
  ```

### feature
- **Type:** String
- **Required:** No
- **Description:** Name of the feature this task belongs to
- **Format:** Should match a feature name in `.galdr/features/`
- **Examples:**
  ```yaml
  feature: User Authentication
  feature: Payment Processing
  feature: Admin Dashboard
  ```

### subsystems
- **Type:** Array of Strings
- **Required:** No (but recommended)
- **Description:** List of affected system components
- **Format:** YAML array, lowercase with underscores
- **Examples:**
  ```yaml
  subsystems: [authentication, database]
  subsystems: [frontend, api, database]
  subsystems: [skills_system, file_io]
  ```

### project_context
- **Type:** String
- **Required:** No (but recommended)
- **Description:** Brief explanation of how task relates to project goals
- **Format:** Single-quoted string, 1-2 sentences
- **Examples:**
  ```yaml
  project_context: 'Enables secure user access, supporting the core security goal'
  project_context: 'Improves performance by 50%, addressing scalability concerns'
  ```

### dependencies
- **Type:** Array of Integers/Strings
- **Required:** No (defaults to empty array)
- **Description:** List of task IDs that must be completed first
- **Format:** YAML array of task IDs
- **Examples:**
  ```yaml
  dependencies: []
  dependencies: [1, 2, 3]
  dependencies: [42, "42.1", "42.2"]
  ```

### parent_task
- **Type:** Integer
- **Required:** No (only for sub-tasks)
- **Description:** ID of the parent task (for sub-tasks only)
- **Format:** Integer matching parent task ID
- **Examples:**
  ```yaml
  parent_task: 42  # This is sub-task 42.1 or 42.2
  ```

## Bug Fix Specific Fields

When `type: bug_fix`, include these additional fields:

### bug_reference
- **Type:** String
- **Required:** Yes (for bug fixes)
- **Description:** Reference to bug entry in BUGS.md
- **Format:** `BUG-{number}`
- **Examples:**
  ```yaml
  bug_reference: BUG-001
  bug_reference: BUG-042
  ```

### severity
- **Type:** String (enum)
- **Required:** Yes (for bug fixes)
- **Description:** Bug severity level
- **Valid Values:** `critical`, `high`, `medium`, `low`
- **Examples:**
  ```yaml
  severity: critical
  severity: high
  ```

### source
- **Type:** String (enum)
- **Required:** Yes (for bug fixes)
- **Description:** How the bug was discovered
- **Valid Values:**
  - `user_reported` - Reported by end user
  - `development` - Found during development
  - `testing` - Found during QA
  - `production` - Found in live environment
- **Examples:**
  ```yaml
  source: user_reported
  source: production
  ```

### reproduction_steps
- **Type:** String
- **Required:** No (but recommended for bugs)
- **Description:** Step-by-step instructions to reproduce
- **Format:** Single-quoted string with numbered steps
- **Examples:**
  ```yaml
  reproduction_steps: '1. Navigate to login page\n2. Click login button\n3. Observe no response'
  ```

### expected_behavior
- **Type:** String
- **Required:** No (but recommended for bugs)
- **Description:** What should happen
- **Examples:**
  ```yaml
  expected_behavior: 'Login modal should appear'
  ```

### actual_behavior
- **Type:** String
- **Required:** No (but recommended for bugs)
- **Description:** What actually happens
- **Examples:**
  ```yaml
  actual_behavior: 'Button click has no effect'
  ```

## Date Tracking Fields

### created_date
- **Type:** String (ISO 8601 date)
- **Required:** Yes (all tasks)
- **Description:** When the task was created
- **Format:** `YYYY-MM-DD`
- **Set by:** Task creation workflow (galdr-task-new)
- **Examples:**
  ```yaml
  created_date: '2026-03-18'
  ```

### completed_date
- **Type:** String (ISO 8601 date or empty)
- **Required:** Yes (all tasks — empty string until completed)
- **Description:** When the task was completed
- **Format:** `YYYY-MM-DD` when completed, `''` when pending/in-progress
- **Set by:** Task completion workflow (galdr-task-update)
- **Examples:**
  ```yaml
  completed_date: ''             # Not yet completed
  completed_date: '2026-03-18'   # Completed
  ```

## Retroactive Fix Specific Fields

When `type: retroactive_fix`, `created_date` and `completed_date` are typically set to the same value (the fix was already done).

### estimated_effort
- **Type:** String
- **Required:** No
- **Description:** Time spent on the fix
- **Format:** Human-readable duration
- **Examples:**
  ```yaml
  estimated_effort: '2 hours'
  estimated_effort: '1 day'
  ```

### actual_effort
- **Type:** String
- **Required:** No
- **Description:** Same as estimated_effort (for retroactive)
- **Format:** Human-readable duration
- **Examples:**
  ```yaml
  actual_effort: '2 hours'
  ```

## Complete Examples

### Basic Feature Task
```yaml
---
id: 1
title: 'Implement user authentication'
status: pending
priority: high
type: feature
feature: User Authentication
subsystems: [authentication, database, api]
project_context: 'Enables secure user access, core security requirement'
dependencies: []
---
```

### Bug Fix Task
```yaml
---
id: 15
title: '[BUG] Fix login button not responding'
type: bug_fix
status: in-progress
priority: critical
feature: User Authentication
subsystems: [frontend, authentication]
project_context: 'Resolves critical login issue affecting all users'
bug_reference: BUG-001
severity: critical
source: production
reproduction_steps: '1. Navigate to login page\n2. Click login button\n3. No response'
expected_behavior: 'Login modal should appear'
actual_behavior: 'Button click has no effect'
dependencies: []
---
```

### Sub-task
```yaml
---
id: "42.1"
title: 'Setup database schema'
type: feature
status: pending
priority: high
parent_task: 42
feature: Data Migration
subsystems: [database]
project_context: 'First step in data migration, establishes schema structure'
dependencies: []
---
```

### Retroactive Fix
```yaml
---
id: 16
title: '[RETROACTIVE] Fixed database query performance'
type: retroactive_fix
status: completed
priority: high
created_date: '2025-10-19'
completed_date: '2025-10-19'
project_context: 'Documents performance optimization reducing query time from 5s to 0.2s'
subsystems: [database, api]
estimated_effort: '2 hours'
actual_effort: '2 hours'
---
```

## Validation Rules

### Field Constraints
1. **id**: Must be unique across all tasks
2. **title**: Must be 5-100 characters
3. **status**: Must be one of valid enum values
4. **priority**: Must be one of valid enum values
5. **subsystems**: Each item must be lowercase with underscores
6. **dependencies**: Must reference existing task IDs
7. **parent_task**: Must reference existing parent task

### Required Field Combinations
- All tasks: `id`, `title`, `status`, `priority`
- Bug fixes: Add `bug_reference`, `severity`, `source`
- Retroactive: Add `created_date`, `completed_date`
- Sub-tasks: Add `parent_task`

### YAML Syntax Rules
1. Use `---` to start and end YAML block
2. Quote string values with single quotes
3. Quote numeric strings (sub-task IDs)
4. Use arrays with square brackets: `[item1, item2]`
5. Use proper indentation (2 spaces)
6. No tabs, only spaces

## Common Mistakes

### ❌ Incorrect
```yaml
---
id: 42.1  # Should be quoted for sub-tasks
title: Implement feature  # Should be quoted
status: In Progress  # Should be lowercase with hyphen
priority: CRITICAL  # Should be lowercase
subsystems: frontend, api  # Should be array format
---
```

### ✅ Correct
```yaml
---
id: "42.1"
title: 'Implement feature'
status: in-progress
priority: critical
subsystems: [frontend, api]
---
```

## Best Practices

1. **Always quote strings** - Prevents YAML parsing issues
2. **Use lowercase enums** - Consistent with system conventions
3. **Be specific in titles** - Makes tasks easy to identify
4. **Include project_context** - Helps maintain focus on goals
5. **List all subsystems** - Improves impact analysis
6. **Document dependencies** - Prevents blocked tasks
7. **Use appropriate types** - Helps with filtering and reporting
8. **Keep it simple** - Only include fields you need

## Tools for Validation

### Manual Validation
1. Check YAML syntax with online validator
2. Verify all required fields present
3. Confirm enum values are valid
4. Ensure IDs are unique

### Automated Validation
- Cursor validates YAML on file read
- Invalid YAML will cause parsing errors
- Check IDE error messages for specific issues

## Summary

The YAML frontmatter provides structured metadata for tasks, enabling:
- Consistent task tracking across IDEs
- Automated status updates
- Dependency management
- Feature integration
- Bug tracking
- Quality metrics

Follow this schema strictly to ensure proper task management in Cursor.

