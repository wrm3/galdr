# GitHub Integration Skill - Workflow Examples

Practical examples for common GitHub operations using this skill.

## Repository Metadata Management

### Example 1: Update Repository Topics

**Scenario:** You've just finished building a Cursor skill and want to add proper topics for discoverability.

**User Request:**
> "Can you add these topics to my repository: Cursor, AI Assistant, Task Management, MCP, and Jira Integration?"

**Workflow:**

1. **Normalize topics:**
   ```
   "Cursor" → "cursor"
   "AI Assistant" → "ai-assistant"
   "Task Management" → "task-management"
   "MCP" → "mcp"
   "Jira Integration" → "jira-integration"
   ```

2. **Check current topics:**
   ```bash
   gh repo view --json repositoryTopics --jq '.repositoryTopics[].name'
   ```

3. **Add new topics:**
   ```bash
   gh repo edit --add-topic claude-code,cursor,ai-assistant,task-management,mcp,jira-integration
   ```

4. **Verify addition:**
   ```bash
   gh repo view --json repositoryTopics
   ```

**Response Template:**
```
I'll add these topics to your repository.

Normalized topics:
- claude-code
- cursor
- ai-assistant
- task-management
- mcp
- jira-integration

Adding topics...

✓ Successfully added 6 topics!

Current topics: claude-code, cursor, ai-assistant, task-management, mcp, jira-integration

Repository URL: https://github.com/owner/repo
```

### Example 2: Complete Repository Metadata Update

**User Request:**
> "Update my repository description to explain it's a template project, add a homepage URL, and add relevant topics"

**Workflow:**

1. **Get current state:**
   ```bash
   gh repo view --json description,homepageUrl,repositoryTopics
   ```

2. **Update description:**
   ```bash
   gh repo edit --description "AI assistant integration template for Cursor with task management, MCP tools, and IDE support"
   ```

3. **Update homepage:**
   ```bash
   gh repo edit --homepage "https://github.com/owner/repo#readme"
   ```

4. **Add topics:**
   ```bash
   gh repo edit --add-topic claude-code,cursor,ai-assistant,project-template,mcp,task-management
   ```

5. **Verify all updates:**
   ```bash
   gh repo view
   ```

**Response:**
```
I'll update your repository metadata.

Updates:
- Description: "AI assistant integration template for Cursor..."
- Homepage: https://github.com/owner/repo#readme
- Topics: claude-code, cursor, ai-assistant, project-template, mcp, task-management

✓ All updates completed successfully!

View your repository: https://github.com/owner/repo
```

### Example 3: Remove Outdated Topics

**User Request:**
> "Remove the old 'python2' and 'deprecated' topics from my repo"

**Workflow:**

1. **View current topics:**
   ```bash
   gh repo view --json repositoryTopics
   ```

2. **Remove topics:**
   ```bash
   gh repo edit --remove-topic python2,deprecated
   ```

3. **Verify removal:**
   ```bash
   gh repo view --json repositoryTopics --jq '.repositoryTopics[].name'
   ```

**Response:**
```
Removing outdated topics...

✓ Removed topics: python2, deprecated

Current topics: python, claude-code, ai-assistant, automation

Repository: https://github.com/owner/repo
```

## Issue Management Workflows

### Example 4: Create Bug Report

**User Request:**
> "Create a bug report for the authentication timeout issue we discussed"

**Workflow:**

1. **Create issue with details:**
   ```bash
   gh issue create \
     --title "Authentication timeout after 5 minutes of inactivity" \
     --label bug,authentication \
     --body "$(cat <<'EOF'
   ## Description
   Users are being logged out after 5 minutes of inactivity, which is too aggressive.

   ## Steps to Reproduce
   1. Log into the application
   2. Leave browser idle for 5 minutes
   3. Attempt to perform action
   4. Observe logout

   ## Expected Behavior
   Session should remain active for at least 30 minutes.

   ## Actual Behavior
   Session expires after 5 minutes.

   ## Environment
   - Browser: Chrome 120
   - OS: Windows 11
   - Version: 2.1.0
   EOF
   )"
   ```

2. **Get issue number and URL from response**

**Response:**
```
Created bug report for authentication timeout.

Issue #247: Authentication timeout after 5 minutes of inactivity
URL: https://github.com/owner/repo/issues/247
Labels: bug, authentication

Would you like me to:
1. Assign this to someone
2. Add it to a milestone
3. Link to related issues
```

### Example 5: Bulk Issue Triage

**User Request:**
> "Show me all open bugs labeled 'high-priority' and assign them to the appropriate team members"

**Workflow:**

1. **List high-priority bugs:**
   ```bash
   gh issue list --label bug,high-priority --state open --json number,title,author
   ```

2. **Review issues and assign:**
   ```bash
   # Assign authentication bugs to security team
   gh issue edit 247 --add-assignee security-team-lead

   # Assign UI bugs to frontend team
   gh issue edit 248 --add-assignee frontend-team-lead
   ```

3. **Verify assignments:**
   ```bash
   gh issue list --label bug,high-priority --assignee security-team-lead
   gh issue list --label bug,high-priority --assignee frontend-team-lead
   ```

**Response:**
```
Found 5 high-priority bugs:

Authentication Issues (assigned to @security-team-lead):
- #247: Authentication timeout after 5 minutes
- #249: OAuth redirect fails on Safari

Frontend Issues (assigned to @frontend-team-lead):
- #248: Button alignment broken on mobile
- #250: Modal dialog not responsive
- #251: Dark mode colors inconsistent

All issues have been assigned!
```

### Example 6: Close Issues with Context

**User Request:**
> "Close issue #247, it was fixed in PR #256"

**Workflow:**

1. **Close issue with reference:**
   ```bash
   gh issue close 247 --comment "Fixed in PR #256. Authentication timeout extended to 30 minutes as specified in requirements."
   ```

2. **Verify closure:**
   ```bash
   gh issue view 247 --json state,closedAt
   ```

**Response:**
```
✓ Closed issue #247

Added comment: "Fixed in PR #256. Authentication timeout extended to 30 minutes..."

Issue: https://github.com/owner/repo/issues/247
Status: Closed
```

## Pull Request Workflows

### Example 7: Create Feature PR

**User Request:**
> "Create a pull request for my authentication-timeout-fix branch"

**Workflow:**

1. **Get commit history for PR description:**
   ```bash
   git log main..authentication-timeout-fix --oneline
   ```

2. **Create PR with comprehensive description:**
   ```bash
   gh pr create \
     --base main \
     --head authentication-timeout-fix \
     --title "Fix: Extend authentication timeout to 30 minutes" \
     --body "$(cat <<'EOF'
   ## Summary
   Extended session timeout from 5 minutes to 30 minutes to improve user experience.

   ## Changes
   - Updated session configuration in `config/auth.py`
   - Modified timeout constant from 300s to 1800s
   - Added environment variable override support
   - Updated tests for new timeout value

   ## Test Plan
   - [x] Unit tests pass
   - [x] Manual testing with 30-minute idle session
   - [x] Environment variable override tested
   - [x] No breaking changes to API

   ## Related Issues
   Fixes #247

   ## Breaking Changes
   None - backward compatible change
   EOF
   )" \
     --reviewer security-team-lead,frontend-team-lead \
     --label enhancement,authentication
   ```

3. **Get PR number and URL**

**Response:**
```
Created pull request!

PR #256: Fix: Extend authentication timeout to 30 minutes
Branch: authentication-timeout-fix → main
URL: https://github.com/owner/repo/pull/256

Reviewers: @security-team-lead, @frontend-team-lead
Labels: enhancement, authentication
Linked issues: Fixes #247

Waiting for CI checks to complete...
```

### Example 8: PR Review and Approval Workflow

**User Request:**
> "Review PR #256, check if tests pass, and approve if everything looks good"

**Workflow:**

1. **View PR details:**
   ```bash
   gh pr view 256
   ```

2. **Check CI/CD status:**
   ```bash
   gh pr checks 256
   ```

3. **View changes:**
   ```bash
   gh pr diff 256
   ```

4. **If tests pass and changes look good, approve:**
   ```bash
   gh pr review 256 --approve --body "LGTM! Tests pass, code looks clean, and timeout value makes sense. Approved for merge."
   ```

**Response:**
```
Reviewed PR #256: Fix: Extend authentication timeout to 30 minutes

CI/CD Status: ✓ All checks passed
- Test Suite: ✓ Passed (45 tests)
- Linting: ✓ Passed
- Security Scan: ✓ No issues found

Changes reviewed:
- config/auth.py: Timeout increased to 1800s
- tests/test_auth.py: Tests updated
- .env.example: New SESSION_TIMEOUT variable

✓ Approved with comment: "LGTM! Tests pass..."

PR is ready to merge!
```

### Example 9: Merge Pull Request

**User Request:**
> "Merge PR #256 using squash merge and delete the branch"

**Workflow:**

1. **Verify PR is approved:**
   ```bash
   gh pr view 256 --json reviewDecision,statusCheckRollup
   ```

2. **Merge with squash:**
   ```bash
   gh pr merge 256 \
     --squash \
     --delete-branch \
     --subject "Fix: Extend authentication timeout to 30 minutes (#256)" \
     --body "Fixes #247"
   ```

3. **Verify merge:**
   ```bash
   gh pr view 256 --json state,merged,mergedAt
   ```

**Response:**
```
✓ Merged PR #256 successfully!

Strategy: Squash and merge
Branch: authentication-timeout-fix (deleted)
Merge commit: a1b2c3d
Closed issues: #247

PR: https://github.com/owner/repo/pull/256
```

### Example 10: Draft PR for Early Feedback

**User Request:**
> "Create a draft PR for my work-in-progress feature so the team can give early feedback"

**Workflow:**

1. **Create draft PR:**
   ```bash
   gh pr create \
     --draft \
     --title "WIP: Add real-time notifications feature" \
     --body "$(cat <<'EOF'
   ## Status
   🚧 Work in Progress - Early feedback requested

   ## Summary
   Implementing real-time notifications using WebSocket.

   ## Completed
   - [x] WebSocket server setup
   - [x] Basic connection handling
   - [x] Authentication middleware

   ## In Progress
   - [ ] Notification event handlers
   - [ ] Frontend integration
   - [ ] Testing

   ## Questions for Reviewers
   1. Should we use Redis for pub/sub or stick with in-memory?
   2. Rate limiting strategy for notifications?
   3. Browser compatibility concerns?

   ## Next Steps
   - Complete event handlers
   - Add integration tests
   - Update documentation
   EOF
   )" \
     --label wip,enhancement \
     --reviewer team-lead
   ```

**Response:**
```
Created draft PR for early feedback!

PR #257: WIP: Add real-time notifications feature
Status: Draft (not ready to merge)
URL: https://github.com/owner/repo/pull/257

Reviewer: @team-lead
Labels: wip, enhancement

Questions highlighted for reviewer feedback.
```

## Release Workflows

### Example 11: Create Production Release

**User Request:**
> "Create release v1.5.0 with auto-generated release notes and upload the distribution files"

**Workflow:**

1. **Verify tag doesn't exist:**
   ```bash
   git tag -l v1.5.0
   ```

2. **Create release with auto-generated notes:**
   ```bash
   gh release create v1.5.0 \
     --title "Version 1.5.0 - Enhanced Authentication" \
     --generate-notes \
     dist/app-v1.5.0.zip \
     dist/app-v1.5.0.tar.gz \
     dist/checksums.txt
   ```

3. **Verify release:**
   ```bash
   gh release view v1.5.0
   ```

**Response:**
```
✓ Created release v1.5.0!

Title: Version 1.5.0 - Enhanced Authentication
Tag: v1.5.0
URL: https://github.com/owner/repo/releases/tag/v1.5.0

Release notes auto-generated from commits.

Assets uploaded:
- app-v1.5.0.zip (12.5 MB)
- app-v1.5.0.tar.gz (11.8 MB)
- checksums.txt (348 bytes)

Release is now public!
```

### Example 12: Create Pre-release

**User Request:**
> "Create a beta release for v2.0.0-beta.1 so early adopters can test"

**Workflow:**

1. **Create pre-release:**
   ```bash
   gh release create v2.0.0-beta.1 \
     --title "Version 2.0.0 Beta 1" \
     --prerelease \
     --notes "$(cat <<'EOF'
   ## 🚧 Beta Release - Testing Required

   This is a pre-release of v2.0.0 for early testing.

   ### New Features
   - Real-time notifications via WebSocket
   - Enhanced authentication with MFA support
   - Improved dashboard performance

   ### Breaking Changes
   - API endpoint structure changed (see migration guide)
   - Minimum Python version now 3.10

   ### Known Issues
   - #301: WebSocket connection drops on Safari
   - #302: Dashboard flickering on slow connections

   ### Migration Guide
   See docs/migration-v2.md for upgrade instructions.

   **⚠️ Not recommended for production use yet!**
   EOF
   )" \
     dist/app-v2.0.0-beta.1.zip
   ```

**Response:**
```
✓ Created pre-release v2.0.0-beta.1!

Title: Version 2.0.0 Beta 1
Tag: v2.0.0-beta.1
Status: Pre-release (not production ready)
URL: https://github.com/owner/repo/releases/tag/v2.0.0-beta.1

Assets: app-v2.0.0-beta.1.zip

⚠️ Marked as pre-release for testing only.
```

### Example 13: Edit Release Notes

**User Request:**
> "Update the release notes for v1.5.0 to add a security warning"

**Workflow:**

1. **Get current release notes:**
   ```bash
   gh release view v1.5.0 --json body --jq '.body'
   ```

2. **Update release notes:**
   ```bash
   gh release edit v1.5.0 \
     --notes "$(cat <<'EOF'
   ## Version 1.5.0 - Enhanced Authentication

   ### ⚠️ Security Notice
   Users on v1.4.x or earlier should upgrade immediately due to session timeout vulnerability (CVE-2024-XXXX).

   ### Features
   - Extended authentication timeout to 30 minutes
   - Added environment variable for timeout configuration
   - Improved session management

   ### Bug Fixes
   - Fixed authentication timeout issue (#247)
   - Resolved OAuth redirect on Safari (#249)

   ### Security
   - Patched session timeout vulnerability
   - Enhanced token validation

   Full changelog: https://github.com/owner/repo/compare/v1.4.0...v1.5.0
   EOF
   )"
   ```

**Response:**
```
✓ Updated release v1.5.0 notes!

Added security warning for users on older versions.

Release: https://github.com/owner/repo/releases/tag/v1.5.0
```

## Batch Operations

### Example 14: Update Multiple Repositories

**User Request:**
> "Add the 'archived' topic to all my old repositories that haven't been updated in 2 years"

**Workflow:**

1. **List all repositories:**
   ```bash
   gh repo list --json name,updatedAt,nameWithOwner --limit 100
   ```

2. **Filter repos not updated in 2 years:**
   ```bash
   # Get current date minus 2 years
   cutoff_date=$(date -d '2 years ago' +%Y-%m-%d)

   # Filter and update each repo
   gh repo list --json nameWithOwner,updatedAt --jq --arg cutoff "$cutoff_date" \
     '.[] | select(.updatedAt < $cutoff) | .nameWithOwner' | \
   while read repo; do
     echo "Updating $repo..."
     gh repo edit "$repo" --add-topic archived
   done
   ```

3. **Verify updates:**
   ```bash
   gh repo list --json nameWithOwner,repositoryTopics | \
     jq '.[] | select(.repositoryTopics | any(.name == "archived"))'
   ```

**Response:**
```
Found 8 repositories not updated in 2+ years.

Updating repositories...
✓ owner/old-project-1 (added 'archived' topic)
✓ owner/old-project-2 (added 'archived' topic)
✓ owner/legacy-tool (added 'archived' topic)
... (5 more)

All old repositories now tagged with 'archived' topic.
```

### Example 15: Sync Topics Across Related Repos

**User Request:**
> "Add the 'claude-code' and 'ai-assistant' topics to all my Claude-related repositories"

**Workflow:**

1. **Find Claude-related repos:**
   ```bash
   gh repo list --json nameWithOwner,description | \
     jq '.[] | select(.description | contains("Claude") or contains("claude")) | .nameWithOwner'
   ```

2. **Add topics to each:**
   ```bash
   # List of repos
   repos=("owner/claude-tools" "owner/claude-integration" "owner/mcp-server")

   for repo in "${repos[@]}"; do
     gh repo edit "$repo" --add-topic claude-code,ai-assistant,anthropic
   done
   ```

3. **Verify:**
   ```bash
   for repo in "${repos[@]}"; do
     echo "Topics for $repo:"
     gh repo view "$repo" --json repositoryTopics --jq '.repositoryTopics[].name'
   done
   ```

**Response:**
```
Found 3 Claude-related repositories.

Adding topics: claude-code, ai-assistant, anthropic

✓ owner/claude-tools
✓ owner/claude-integration
✓ owner/mcp-server

All repositories updated with consistent topics!
```

## GitHub Actions Workflows

### Example 16: Trigger Workflow with Inputs

**User Request:**
> "Run the deployment workflow for the staging environment"

**Workflow:**

1. **List available workflows:**
   ```bash
   gh workflow list
   ```

2. **Trigger deployment workflow:**
   ```bash
   gh workflow run deploy.yml \
     -f environment=staging \
     -f version=v1.5.0 \
     -f notify=true
   ```

3. **Get run ID and watch:**
   ```bash
   run_id=$(gh run list --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId')
   gh run watch "$run_id"
   ```

**Response:**
```
Triggered deployment workflow!

Workflow: deploy.yml
Inputs:
  - environment: staging
  - version: v1.5.0
  - notify: true

Run ID: 12345
Status: In progress...

Watching run: https://github.com/owner/repo/actions/runs/12345
```

### Example 17: Check Workflow Status and Download Artifacts

**User Request:**
> "Check if the latest build succeeded and download the artifacts"

**Workflow:**

1. **Get latest run:**
   ```bash
   gh run list --workflow build.yml --limit 1 --json databaseId,status,conclusion
   ```

2. **Check status:**
   ```bash
   gh run view 12345
   ```

3. **If successful, download artifacts:**
   ```bash
   if [ "$(gh run view 12345 --json conclusion --jq '.conclusion')" = "success" ]; then
     gh run download 12345 --dir ./artifacts
   fi
   ```

**Response:**
```
Latest build status:

Run #12345
Status: Completed
Result: ✓ Success
Duration: 8m 42s

Artifacts downloaded to ./artifacts/:
- build-artifacts.zip (45 MB)
- test-results.xml (128 KB)
- coverage-report.html (2.5 MB)

Build: https://github.com/owner/repo/actions/runs/12345
```

## Error Handling Examples

### Example 18: Handle Rate Limiting

**User Request:**
> "Update topics for 50 repositories"

**Workflow with rate limit handling:**

```bash
#!/bin/bash

# Check rate limit before starting
remaining=$(gh api rate_limit --jq '.resources.core.remaining')
echo "Rate limit remaining: $remaining"

if [ "$remaining" -lt 100 ]; then
  reset_time=$(gh api rate_limit --jq '.resources.core.reset')
  wait_seconds=$((reset_time - $(date +%s)))
  echo "Rate limit low. Waiting $wait_seconds seconds..."
  sleep "$wait_seconds"
fi

# Process repos with rate limit checks
for repo in "${repos[@]}"; do
  gh repo edit "$repo" --add-topic claude-code || {
    # If failed, check if rate limited
    remaining=$(gh api rate_limit --jq '.resources.core.remaining')
    if [ "$remaining" -lt 10 ]; then
      echo "Rate limited. Pausing..."
      sleep 60
      # Retry
      gh repo edit "$repo" --add-topic claude-code
    fi
  }
done
```

**Response:**
```
Processing 50 repositories...

Rate limit remaining: 4850
Progress: 25/50 repositories updated...
Progress: 50/50 repositories updated...

✓ Successfully updated all 50 repositories!
Rate limit remaining: 4800
```

---

## Quick Reference

### Most Common Operations

```bash
# Update repository metadata
gh repo edit --description "..." --homepage "..." --add-topic topic1,topic2

# Create issue
gh issue create --title "..." --body "..." --label bug

# Create PR
gh pr create --title "..." --body "..." --reviewer username

# Merge PR
gh pr merge <number> --squash --delete-branch

# Create release
gh release create v1.0.0 --title "..." --generate-notes file.zip

# Trigger workflow
gh workflow run workflow.yml -f input=value

# Check workflow status
gh run list --workflow workflow.yml --limit 5
```

For more details, see the reference documentation in the `reference/` directory.
