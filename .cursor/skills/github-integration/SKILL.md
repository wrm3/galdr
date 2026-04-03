---
name: github-integration
description: GitHub repos, issues, PRs, releases, Actions, API, and gh CLI integration.
---

# GitHub Integration Skill

Complete integration with GitHub for repository management, issue tracking, pull requests, releases, and automation via GitHub API and CLI.

## Overview

The GitHub Integration Skill provides:
- **Repository Management**: Create, update, configure repositories
- **Topics & Metadata**: Add/update topics, description, website
- **Issue Tracking**: Create, update, query, label issues
- **Pull Requests**: Create, review, merge PRs
- **Releases**: Create releases, upload assets, manage tags
- **Actions & Workflows**: Trigger workflows, check runs
- **User/Org Management**: Teams, permissions, collaborators
- **GitHub CLI**: Direct `gh` command integration

## When to Use This Skill

Activate this skill when the user needs to:
- Update repository topics/tags/description
- Create or manage GitHub repositories
- Work with issues and pull requests
- Create releases and tags
- Manage repository settings
- Trigger GitHub Actions workflows
- Manage collaborators and permissions
- Query GitHub data via API

## Capabilities

### Repository Management
- **Create Repository**: Initialize new repos (public/private)
- **Update Settings**: Description, website, topics, visibility
- **Topics/Tags**: Add, remove, replace repository topics
- **Branch Protection**: Configure branch rules
- **Webhooks**: Configure repository webhooks
- **Secrets**: Manage repository secrets (Actions)
- **Collaborators**: Add, remove, manage permissions
- **Transfer**: Transfer ownership
- **Archive/Delete**: Archive or delete repositories

### Topics & Metadata Management
- **Add Topics**: Add tags to repository for discoverability
- **Remove Topics**: Remove outdated or incorrect tags
- **Update Description**: Set repository description
- **Set Homepage**: Configure repository website URL
- **Update README**: Generate or update README.md
- **Social Preview**: Update social media preview image

### Issue Management
- **Create Issues**: Create with templates, labels, assignees
- **Update Issues**: Edit title, body, labels, assignees
- **Query Issues**: Search with filters and queries
- **Labels**: Create, update, delete labels
- **Milestones**: Create and manage milestones
- **Comments**: Add, edit, delete comments
- **Close/Reopen**: Change issue state
- **Lock/Unlock**: Lock conversations

### Pull Request Operations
- **Create PR**: From branch or fork
- **Review PR**: Add review comments, approve/reject
- **Merge PR**: Merge, squash, or rebase
- **Request Reviews**: Assign reviewers
- **Check Status**: CI/CD status, conflicts
- **Draft PRs**: Create draft pull requests
- **Auto-merge**: Enable auto-merge when checks pass

### Release Management
- **Create Release**: Tag and create release
- **Upload Assets**: Attach binaries, archives
- **Pre-release**: Mark as pre-release or draft
- **Release Notes**: Auto-generate from commits
- **Edit Release**: Update release info
- **Delete Release**: Remove releases

### GitHub Actions
- **Trigger Workflows**: Manually trigger workflows
- **Check Runs**: View workflow run status
- **Download Artifacts**: Get workflow artifacts
- **Secrets Management**: Add/update Actions secrets
- **View Logs**: Check workflow logs

## GitHub CLI Integration

This skill uses `gh` (GitHub CLI) for most operations:

### Repository Commands
- `gh repo create` - Create repository
- `gh repo edit` - Update repository settings
- `gh repo view` - View repository details
- `gh repo clone` - Clone repository
- `gh repo fork` - Fork repository

### Issue Commands
- `gh issue create` - Create issue
- `gh issue list` - List issues
- `gh issue view` - View issue details
- `gh issue edit` - Update issue
- `gh issue close` - Close issue

### PR Commands
- `gh pr create` - Create pull request
- `gh pr list` - List pull requests
- `gh pr view` - View PR details
- `gh pr review` - Review PR
- `gh pr merge` - Merge PR
- `gh pr checks` - Check PR status

### Release Commands
- `gh release create` - Create release
- `gh release list` - List releases
- `gh release view` - View release
- `gh release upload` - Upload assets
- `gh release delete` - Delete release

## Usage Examples

### Example 1: Update Repository Topics
```
User: "Add topics claude-code, cursor, ai-assistant to my repo"

Workflow:
1. Identify current repository (from git remote or ask)
2. Get current topics: gh repo view --json repositoryTopics
3. Add new topics: gh repo edit --add-topic claude-code --add-topic cursor --add-topic ai-assistant
4. Verify topics added
5. Return success with updated topics list
```

### Example 2: Update Repository Description & Homepage
```
User: "Update repo description and add homepage URL"

Workflow:
1. Get repository info
2. Ask user for new description
3. Ask user for homepage URL
4. Update: gh repo edit --description "New description" --homepage "https://example.com"
5. Verify changes
6. Return success
```

### Example 3: Create GitHub Issue
```
User: "Create bug issue for login failure"

Workflow:
1. Use issue template if available
2. Gather details:
   - Title: "Login fails on mobile"
   - Body: User description
   - Labels: bug, high-priority
   - Assignee: Optional
3. Create: gh issue create --title "..." --body "..." --label bug
4. Return issue URL
```

### Example 4: Create Pull Request
```
User: "Create PR from feature/login to main"

Workflow:
1. Verify current branch or checkout branch
2. Push branch to remote if needed
3. Generate PR description from commits
4. Create: gh pr create --base main --head feature/login --title "Add login feature" --body "..."
5. Assign reviewers if specified
6. Return PR URL
```

### Example 5: Create Release
```
User: "Create v1.0.0 release with changelog"

Workflow:
1. Verify tag doesn't exist
2. Generate release notes from commits
3. Create: gh release create v1.0.0 --title "Version 1.0.0" --notes "Changelog..."
4. Upload assets if provided
5. Return release URL
```

### Example 6: Set Multiple Repository Topics
```
User: "Tag this repo with Cursor, AI tools"

Workflow:
1. Parse desired topics (normalize: claude-code, cursor, ai-tools)
2. Get current topics
3. Merge with new topics (avoid duplicates)
4. Set all topics: gh repo edit --add-topic claude-code,cursor,ai-tools
5. Return complete topic list
```

### Example 7: Check PR Status
```
User: "What's the status of PR #42?"

Workflow:
1. Get PR details: gh pr view 42
2. Check CI/CD status: gh pr checks 42
3. Check reviews
4. Check merge conflicts
5. Format and return status report
```

### Example 8: Trigger GitHub Actions Workflow
```
User: "Run the deploy workflow"

Workflow:
1. List workflows: gh workflow list
2. Find deploy workflow
3. Trigger: gh workflow run deploy.yml
4. Get run ID
5. Monitor progress
6. Return run status and URL
```

## Configuration

### Automatic GitHub CLI Setup

**IMPORTANT:** This skill requires GitHub CLI (`gh`). The skill will automatically:
1. Check if `gh` is installed
2. If not installed, provide platform-specific installation instructions
3. Guide user through authentication if needed

### GitHub CLI Installation

**Automatic Check:**
Before any GitHub operation, the skill will verify `gh` is installed:
```bash
gh --version
```

**If not installed, provide instructions based on platform:**

**Windows:**
```powershell
winget install GitHub.cli
```

**macOS:**
```bash
brew install gh
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install gh
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install gh
```

**Linux (Arch):**
```bash
sudo pacman -S github-cli
```

### Authentication Setup
After installation, authenticate with GitHub:
```bash
gh auth login

# Set default repository (optional)
gh repo set-default owner/repo
```

### Environment Variables
```bash
# GitHub token (optional, gh auth is preferred)
GITHUB_TOKEN=ghp_your_token_here

# Default repository
GITHUB_REPO=owner/repo
```

### Git Configuration
```bash
# Ensure git is configured
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Repository Topics Guidelines

### Best Practices for Topics

**Topic Format:**
- Lowercase letters, numbers, hyphens
- Max 50 characters per topic
- Max 20 topics per repository
- Use hyphens not spaces: `claude-code` not `claude code`

**Recommended Topics for AI/IDE Projects:**
```
# Primary
claude-code, cursor, anthropic, ai-assistant

# Project Type
project-template, boilerplate, starter-kit

# Technologies
mcp, mcp-server, python, nodejs

# Features
task-management, automation, web-scraping

# Integrations
jira, confluence, github, atlassian
```

**Topic Categories:**
1. **Platform/IDE**: claude-code, cursor, vscode, windsurf
2. **AI/ML**: anthropic, openai, llm, ai-tools
3. **Language**: python, javascript, typescript
4. **Framework**: react, nodejs, playwright
5. **Purpose**: automation, integration, productivity
6. **Domain**: devtools, enterprise, productivity

## Best Practices

### Repository Management
1. **Clear Description**: Write descriptive, searchable descriptions
2. **Relevant Topics**: Add 5-15 relevant topics
3. **Homepage URL**: Link to documentation or project site
4. **README**: Keep README.md updated
5. **License**: Always include LICENSE file
6. **Contributing**: Add CONTRIBUTING.md for contributors

### Issue Management
1. **Templates**: Use issue templates for consistency
2. **Labels**: Create clear, consistent labels
3. **Assignees**: Assign issues to responsible parties
4. **Milestones**: Group issues by milestone
5. **Projects**: Use GitHub Projects for planning

### Pull Requests
1. **Descriptive Titles**: Clear, concise PR titles
2. **Detailed Descriptions**: Explain what and why
3. **Link Issues**: Reference related issues
4. **Request Reviews**: Assign appropriate reviewers
5. **CI/CD**: Ensure checks pass before merging

### Releases
1. **Semantic Versioning**: Use semver (v1.2.3)
2. **Changelog**: Include detailed changelog
3. **Assets**: Attach relevant binaries/archives
4. **Pre-releases**: Mark beta/alpha as pre-release
5. **Release Notes**: Auto-generate from commits

## Troubleshooting

### Authentication Issues

**Problem: gh not authenticated**
```bash
gh auth status
# If not authenticated:
gh auth login
```

**Problem: Insufficient permissions**
- Check token scopes (repo, workflow, etc.)
- Regenerate token with required scopes
- Re-authenticate: gh auth login

### Repository Issues

**Problem: Can't find repository**
- Check repository name/owner
- Verify access permissions
- Use full name: owner/repo

**Problem: Topics not updating**
- Check topic format (lowercase, hyphens)
- Verify max 20 topics limit
- Check repository permissions

### PR/Issue Issues

**Problem: Can't create PR**
- Ensure branch is pushed to remote
- Check base and head branches exist
- Verify no existing PR for branch

**Problem: CI checks failing**
- View logs: gh pr checks <number>
- Check GitHub Actions tab
- Fix issues and push new commits

## Security Considerations

### Token Management
- ✅ Use `gh auth` instead of tokens when possible
- ✅ Store tokens in environment variables
- ✅ Use minimum required scopes
- ✅ Rotate tokens regularly
- ❌ Never commit tokens to repository

### Repository Secrets
- ✅ Use for sensitive data in Actions
- ✅ Never expose in logs
- ✅ Rotate regularly
- ✅ Use environment secrets for sensitive workflows

### Permissions
- ✅ Grant minimum required access
- ✅ Use teams for group permissions
- ✅ Review collaborators periodically
- ✅ Enable branch protection for important branches

## Advanced Features

### Batch Operations
```bash
# Add multiple topics at once
gh repo edit --add-topic topic1,topic2,topic3

# Close multiple issues
gh issue list --state open | xargs -I {} gh issue close {}

# Bulk label issues
gh issue list --label needs-triage | xargs -I {} gh issue edit {} --add-label triaged
```

### Automation with GitHub Actions
```yaml
# Example: Auto-update topics on push
name: Update Topics
on:
  push:
    paths:
      - '.github/topics.txt'
jobs:
  update-topics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Update Topics
        run: |
          topics=$(cat .github/topics.txt | tr '\n' ',')
          gh repo edit --add-topic $topics
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### API Integration
```python
# Example: Update repository via API
import requests

def update_repo_topics(owner, repo, topics):
    url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.mercy-preview+json"
    }
    data = {"names": topics}
    response = requests.put(url, headers=headers, json=data)
    return response.json()
```

## Reference Materials

For detailed implementation information, see:
- [reference/github_cli_guide.md](reference/github_cli_guide.md) - GitHub CLI commands
- [reference/github_api_guide.md](reference/github_api_guide.md) - GitHub API usage
- [reference/topics_guide.md](reference/topics_guide.md) - Repository topics best practices
- [examples/repo_workflows.md](examples/repo_workflows.md) - Common workflows

## Related Skills

- **atlassian-integration**: Similar workflow for Jira/Confluence
- **web-tools**: For scraping GitHub pages
- **galdr-task-management**: Sync GitHub issues with local tasks

---

**Note:** Ensure you have proper permissions before performing repository operations. Always follow your organization's policies for repository management.
