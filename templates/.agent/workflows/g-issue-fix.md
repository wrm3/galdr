---
description: "Fix a GitHub issue in the project"
---

Fix GitHub issue: $ARGUMENTS

## What This Command Does

Analyzes and fixes a GitHub issue with proper documentation and testing.

## Issue Fix Workflow

### 1. Understand the Issue
I'll:
- Read the issue description thoroughly
- Identify expected vs actual behavior
- Note reproduction steps provided
- Check for related issues or PRs
- Review any error messages or logs

### 2. Locate Relevant Code
I'll:
- Search for files/functions mentioned in the issue
- Use grep/search to find related code
- Review recent changes that might have caused the issue
- Check git blame for context on problematic code

### 3. Implement the Fix
I'll:
- Make minimal, focused changes
- Follow project coding standards
- Add comments explaining non-obvious fixes
- Consider edge cases
- Avoid introducing new issues

### 4. Test the Fix
I'll:
- Verify the fix resolves the reported issue
- Run existing tests to prevent regressions
- Add new tests if coverage is lacking
- Test edge cases mentioned in the issue

### 5. Document the Solution
I'll:
- Create clear commit message
- Reference the issue number
- Explain what was changed and why
- Update any affected documentation

## Commit Message Format
```
fix: [Brief description] (#ISSUE_NUMBER)

Problem:
- [What was broken]

Solution:
- [What was changed]
- [Why this approach]

Testing:
- [How it was verified]

Resolves #ISSUE_NUMBER
```

## Integration with galdr

If this is a significant fix, I'll also:
1. Create retroactive task documenting the fix
2. Update TASKS.md with completed status
3. Add to BUGS.md if it was a bug

## What I Need From You
- GitHub issue number or URL
- Any additional context about the issue
- Preferred approach (if you have one)

Let's fix this issue!
