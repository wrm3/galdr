# GitHub Integration Skill - Implementation Rules

## Skill Activation

Activate this skill when user requests involve:
- Updating repository topics/tags/description
- Creating or managing GitHub repositories
- Working with GitHub issues or pull requests
- Creating releases and managing tags
- GitHub Actions workflows
- Repository settings and permissions
- GitHub CLI operations

**Do NOT activate for:**
- Local git operations only (use Bash tool directly)
- GitLab or Bitbucket operations (different platforms)
- Generic version control questions (no GitHub context)

## Core Workflow

### Step 1: Identify Operation Type

Determine which GitHub operation is needed:

**Repository Metadata** - Keywords: topics, tags, description, homepage, about
**Issues** - Keywords: issue, ticket, bug report, feature request
**Pull Requests** - Keywords: PR, pull request, merge, code review
**Releases** - Keywords: release, tag, version, publish
**Actions** - Keywords: workflow, CI/CD, automation, GitHub Actions

### Step 2: Verify GitHub CLI Installation & Authentication

**CRITICAL:** Always check if GitHub CLI is installed before any operation.

**Installation Check Workflow:**

1. **Check if `gh` is installed:**
   ```bash
   gh --version
   ```

2. **If command not found, detect platform and provide installation instructions:**

   **Windows:**
   ```
   GitHub CLI is not installed. Installing now...

   Please run:
   winget install GitHub.cli

   Or download from: https://cli.github.com/
   ```

   **macOS:**
   ```
   GitHub CLI is not installed. Installing now...

   Please run:
   brew install gh

   Or download from: https://cli.github.com/
   ```

   **Linux (Debian/Ubuntu):**
   ```
   GitHub CLI is not installed. Installing now...

   Please run:
   sudo apt install gh

   Or see: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
   ```

   **Linux (Fedora/RHEL):**
   ```
   GitHub CLI is not installed. Installing now...

   Please run:
   sudo dnf install gh
   ```

   **Linux (Arch):**
   ```
   GitHub CLI is not installed. Installing now...

   Please run:
   sudo pacman -S github-cli
   ```

3. **After installation, check authentication:**
   ```bash
   gh auth status
   ```

4. **If not authenticated, guide user through authentication:**
   ```
   GitHub CLI is installed but not authenticated.

   Please run:
   gh auth login

   Follow the prompts to:
   1. Choose GitHub.com or GitHub Enterprise
   2. Choose HTTPS or SSH
   3. Authenticate via browser or token

   Then we can proceed with the GitHub operation.
   ```

5. **Only proceed with GitHub operations after both installation and authentication are confirmed.**

### Step 3: Identify Target Repository

Determine which repository to operate on:
1. Check current directory for git remote
2. Use explicitly provided repo name (owner/repo)
3. Ask user if ambiguous

### Step 4: Execute Operation

Use appropriate `gh` command with proper error handling and validation.

### Step 5: Confirm and Report

- Verify operation succeeded
- Return relevant URLs for user to review
- Provide next steps if applicable

## Repository Topics Management

### Adding Topics

**Workflow:**
```
1. Get current repository info:
   gh repo view --json repositoryTopics

2. Validate new topics:
   - Lowercase with hyphens
   - Max 50 characters each
   - Max 20 topics total
   - No spaces (use hyphens)

3. Add topics:
   gh repo edit --add-topic topic1,topic2,topic3

4. Verify topics added:
   gh repo view --json repositoryTopics

5. Return success with updated topic list
```

**Topic Formatting Rules:**
- Convert spaces to hyphens: "Cursor IDE" → "cursor-ide"
- Lowercase only: "AI-Assistant" → "ai-assistant"
- Remove special characters except hyphens
- Combine multi-word terms: "task management" → "task-management"

**Example Conversation:**
```
User: "Add topics Cursor IDE and AI Assistant"

Process:
1. Normalize topics:
   - "Cursor IDE" → "cursor-ide"
   - "AI Assistant" → "ai-assistant"

2. Get current topics:
   gh repo view --json repositoryTopics

3. Add new topics (preserving existing):
   gh repo edit --add-topic claude-code,cursor-ide,ai-assistant

4. Confirm:
   "Added 3 topics to repository. Current topics: claude-code, cursor-ide, ai-assistant, [existing topics]"
```

### Removing Topics

**Workflow:**
```
1. List current topics
2. Identify topics to remove
3. Remove topics:
   gh repo edit --remove-topic topic1,topic2
4. Verify removal
5. Return updated topic list
```

### Replacing All Topics

**Workflow:**
```
1. Get desired final topic list
2. Clear existing topics (if needed)
3. Set new topics:
   gh repo edit --add-topic topic1,topic2,topic3
4. Return final topic list
```

## Repository Description & Homepage

### Update Description

**Workflow:**
```
1. Get current description (optional):
   gh repo view --json description

2. Update description:
   gh repo edit --description "New description text"

3. Verify update:
   gh repo view

4. Return confirmation
```

**Best Practices:**
- Keep under 350 characters
- Be descriptive and searchable
- Include key technologies/features
- Avoid marketing jargon

**Example:**
```
Bad: "The best AI tool ever made!"
Good: "AI assistant integration template for Cursor with task management, MCP tools, and IDE support"
```

### Update Homepage URL

**Workflow:**
```
1. Validate URL format
2. Update homepage:
   gh repo edit --homepage "https://example.com"
3. Verify update
4. Return confirmation
```

## Issue Management

### Create Issue

**Workflow:**
```
1. Gather issue details:
   - Title (required)
   - Body (optional but recommended)
   - Labels (optional): --label bug,enhancement
   - Assignees (optional): --assignee username
   - Milestone (optional): --milestone "v1.0"

2. Use template if available:
   gh issue create --template bug_report.md

3. Create issue:
   gh issue create --title "Title" --body "Description" --label bug

4. Return issue number and URL
```

### Query Issues

**Workflow:**
```
1. Build query with filters:
   --state open/closed/all
   --label labelname
   --assignee username
   --author username
   --mention username

2. Execute search:
   gh issue list --state open --label bug

3. Format results for user
4. Return list with issue numbers and titles
```

### Update Issue

**Workflow:**
```
1. Get issue number
2. Determine what to update:
   - Title: --title "New title"
   - Body: --body "New description"
   - Labels: --add-label or --remove-label
   - State: gh issue close <number>
   - Assignee: --add-assignee or --remove-assignee

3. Update issue:
   gh issue edit <number> [options]

4. Return confirmation
```

### Common Issue Patterns

**Find my open issues:**
```bash
gh issue list --assignee @me --state open
```

**Find high-priority bugs:**
```bash
gh issue list --label bug,high-priority --state open
```

**Close multiple issues:**
```bash
gh issue close 123 124 125
```

## Pull Request Operations

### Create Pull Request

**Workflow:**
```
1. Verify current branch is pushed to remote
2. Determine base branch (usually main/master)
3. Generate title from branch name or commits
4. Generate description:
   - Summary of changes
   - Test plan
   - Related issues (Fixes #123)

5. Create PR:
   gh pr create --base main --head feature-branch --title "Title" --body "Description"

6. Add reviewers if specified:
   --reviewer username1,username2

7. Return PR number and URL
```

**PR Description Template:**
```markdown
## Summary
- Brief description of changes

## Changes
- List of main changes
- Feature additions
- Bug fixes

## Test Plan
- How to test the changes
- What scenarios were tested

## Related Issues
Fixes #123
Related to #456
```

### Review Pull Request

**Workflow:**
```
1. Get PR number
2. View PR details:
   gh pr view <number>

3. Check changes:
   gh pr diff <number>

4. Check CI status:
   gh pr checks <number>

5. Add review:
   gh pr review <number> --approve
   gh pr review <number> --request-changes --body "Comments"
   gh pr review <number> --comment --body "General comment"

6. Return review status
```

### Merge Pull Request

**Workflow:**
```
1. Verify PR is approved
2. Check CI/CD status (all checks passing)
3. Check for merge conflicts
4. Choose merge strategy:
   --merge (merge commit)
   --squash (squash and merge)
   --rebase (rebase and merge)

5. Merge PR:
   gh pr merge <number> --squash --delete-branch

6. Return merge commit hash or confirmation
```

### Check PR Status

**Workflow:**
```
1. Get PR details:
   gh pr view <number>

2. Check CI/CD status:
   gh pr checks <number>

3. Check reviews:
   gh pr view <number> --json reviews

4. Format status report:
   - State (open/closed/merged)
   - Checks (passing/failing)
   - Reviews (approved/changes requested)
   - Conflicts (yes/no)

5. Return comprehensive status
```

## Release Management

### Create Release

**Workflow:**
```
1. Verify tag doesn't exist:
   git tag -l v1.0.0

2. Determine release type:
   - Production: Standard release
   - Pre-release: --prerelease flag
   - Draft: --draft flag

3. Generate release notes:
   - Auto-generate from commits: --generate-notes
   - Manual notes: --notes "Release notes"
   - From file: --notes-file CHANGELOG.md

4. Create release:
   gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"

5. Upload assets (if any):
   gh release upload v1.0.0 file1.zip file2.tar.gz

6. Return release URL
```

**Version Naming Best Practices:**
- Use semantic versioning: v1.2.3 (vMAJOR.MINOR.PATCH)
- Pre-releases: v1.0.0-alpha.1, v1.0.0-beta.2
- Prefix with 'v': v1.0.0 not 1.0.0

### Upload Release Assets

**Workflow:**
```
1. Get release tag
2. Prepare assets (files to upload)
3. Upload assets:
   gh release upload v1.0.0 asset1.zip asset2.tar.gz

4. Verify upload:
   gh release view v1.0.0

5. Return asset URLs
```

### Edit Release

**Workflow:**
```
1. Get release tag
2. Update fields:
   --title "New title"
   --notes "Updated notes"
   --draft false (publish draft)
   --prerelease false (mark as production)

3. Update release:
   gh release edit v1.0.0 [options]

4. Return updated release URL
```

## GitHub Actions

### Trigger Workflow

**Workflow:**
```
1. List available workflows:
   gh workflow list

2. Identify workflow to trigger (by name or file)
3. Trigger workflow:
   gh workflow run workflow-name.yml

4. With inputs (if workflow accepts):
   gh workflow run workflow.yml -f input1=value1 -f input2=value2

5. Get run ID:
   gh run list --workflow workflow-name.yml --limit 1

6. Return run URL and ID
```

### Check Workflow Status

**Workflow:**
```
1. Get run ID or list recent runs:
   gh run list --limit 10

2. View run details:
   gh run view <run-id>

3. Check run status:
   - queued
   - in_progress
   - completed (success/failure)

4. View logs if needed:
   gh run view <run-id> --log

5. Return status report
```

### Download Artifacts

**Workflow:**
```
1. Get run ID
2. List artifacts:
   gh run view <run-id> --json artifacts

3. Download artifact:
   gh run download <run-id> -n artifact-name

4. Return downloaded file path
```

## Error Handling

### Authentication Errors

**401 Unauthorized:**
```
Recovery:
1. Check authentication:
   gh auth status

2. If not authenticated:
   gh auth login

3. If authenticated but still failing:
   - Check token scopes
   - Regenerate token
   - Re-authenticate

4. Report to user with instructions
```

**403 Forbidden:**
```
Recovery:
1. Check repository permissions
2. Verify user has required access (read/write/admin)
3. Check if repository is private and user has access
4. Report specific permission needed
```

### Repository Errors

**404 Not Found:**
```
Recovery:
1. Verify repository name format (owner/repo)
2. Check if repository exists
3. Verify user has access to repository
4. Check for typos in repository name
5. Report error with suggestions
```

**Validation Errors:**
```
Recovery:
1. Parse error message for specific issue
2. Common issues:
   - Topic format invalid (use lowercase, hyphens only)
   - Too many topics (max 20)
   - Topic too long (max 50 characters)
3. Correct issue and retry
4. Report what was corrected
```

### Rate Limiting

**403 Rate Limit Exceeded:**
```
Recovery:
1. Check rate limit status:
   gh api rate_limit

2. Wait for rate limit reset (shown in error)
3. Implement exponential backoff for retries
4. Use authenticated requests (higher limits)
5. Report wait time to user
```

## Best Practices

### Repository Management

**Topics:**
1. ✅ Add 5-15 relevant topics (not too few, not max)
2. ✅ Use established topic names (check popular repos)
3. ✅ Include primary language/framework
4. ✅ Include purpose/category
5. ✅ Use hyphens not underscores

**Description:**
1. ✅ Clear and concise (under 350 chars)
2. ✅ Include key features/technologies
3. ✅ Make it searchable
4. ✅ Update when project evolves

**Homepage:**
1. ✅ Link to documentation site
2. ✅ Link to demo/live site
3. ✅ Ensure URL is accessible
4. ✅ Use HTTPS

### Issue Management

**Creating Issues:**
1. ✅ Use descriptive titles
2. ✅ Provide context in body
3. ✅ Add relevant labels
4. ✅ Use templates when available
5. ✅ Link related issues

**Labeling:**
1. ✅ Create consistent label scheme
2. ✅ Use color coding
3. ✅ Categories: type (bug/feature), priority, status
4. ✅ Keep label count manageable

### Pull Requests

**Creating PRs:**
1. ✅ Descriptive title (what, not how)
2. ✅ Detailed description with context
3. ✅ Link to related issues (Fixes #123)
4. ✅ Request appropriate reviewers
5. ✅ Ensure CI checks pass

**Reviewing:**
1. ✅ Review promptly
2. ✅ Provide constructive feedback
3. ✅ Approve when satisfied
4. ✅ Request changes if needed
5. ✅ Use inline comments for specific issues

**Merging:**
1. ✅ Ensure all checks pass
2. ✅ Resolve conflicts before merging
3. ✅ Use appropriate merge strategy
4. ✅ Delete branch after merge
5. ✅ Squash commits if many small commits

### Releases

**Creating Releases:**
1. ✅ Use semantic versioning
2. ✅ Write clear release notes
3. ✅ Include changelog
4. ✅ Attach relevant assets
5. ✅ Tag properly (v1.0.0 format)

**Release Notes:**
1. ✅ Summarize changes
2. ✅ Group by type (features, fixes, breaking)
3. ✅ Credit contributors
4. ✅ Link to PRs/issues
5. ✅ Highlight breaking changes

## User Communication

### Initial Response Template

```
I'll help you [operation] for [repository].

Details:
- Repository: owner/repo
- Operation: [Specific action]
- Current state: [Current value if applicable]

Proceeding with operation...
```

### Success Report Template

```
Operation completed successfully!

Result:
- [Specific result with values]
- URL: [Direct link]

Current state:
- [Updated values]

Would you like me to:
1. [Follow-up option 1]
2. [Follow-up option 2]
```

### Error Report Template

```
Operation failed: [Error summary]

Error: [Detailed error message]
Cause: [Root cause analysis]

To fix:
1. [Action 1]
2. [Action 2]

Would you like me to:
- Retry with corrections
- Try alternative approach
- Help troubleshoot
```

## Security Considerations

### Token/Credential Management

**DO:**
- ✅ Use `gh auth login` for authentication
- ✅ Store tokens via GitHub CLI credential manager
- ✅ Use environment variables for tokens if needed
- ✅ Verify token scopes match requirements

**DON'T:**
- ❌ Commit tokens to repository
- ❌ Log tokens in output
- ❌ Share tokens in plain text
- ❌ Use tokens with excessive permissions

### Repository Operations

**Safe Operations:**
- ✅ Adding topics (non-destructive)
- ✅ Updating description (reversible)
- ✅ Creating issues/PRs (can be closed)
- ✅ Adding comments (can be edited/deleted)

**Require Confirmation:**
- ⚠️ Deleting repository
- ⚠️ Transferring ownership
- ⚠️ Changing visibility (public/private)
- ⚠️ Force pushing
- ⚠️ Deleting branches

### Best Practices Summary

**Authentication:**
1. ✅ Use GitHub CLI authentication
2. ✅ Verify auth status before operations
3. ✅ Use tokens with minimum required scopes
4. ✅ Rotate tokens periodically

**Operations:**
1. ✅ Validate inputs before GitHub API calls
2. ✅ Use batch operations when possible
3. ✅ Handle rate limiting gracefully
4. ✅ Provide clear error messages

**User Experience:**
1. ✅ Explain what will happen before executing
2. ✅ Confirm destructive operations
3. ✅ Provide progress updates for long operations
4. ✅ Return actionable results with URLs

---

**Remember:** Always verify GitHub CLI is installed and authenticated before performing operations. Guide users through `gh auth login` if needed.
