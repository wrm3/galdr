# GitHub CLI (gh) Command Reference

Complete reference guide for GitHub CLI commands used in this skill.

## Installation

### Windows
```bash
winget install GitHub.cli
```

### macOS
```bash
brew install gh
```

### Linux
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh

# Arch
sudo pacman -S github-cli
```

## Authentication

### Login
```bash
# Interactive login
gh auth login

# Login with token
gh auth login --with-token < token.txt

# Check authentication status
gh auth status

# Logout
gh auth logout
```

## Repository Commands

### View Repository
```bash
# View current repository
gh repo view

# View specific repository
gh repo view owner/repo

# View with specific fields (JSON)
gh repo view --json name,description,repositoryTopics

# View in browser
gh repo view --web
```

### Create Repository
```bash
# Create repository (interactive)
gh repo create

# Create public repository
gh repo create my-repo --public

# Create private repository
gh repo create my-repo --private

# Create with description
gh repo create my-repo --description "My project description"

# Create with homepage
gh repo create my-repo --homepage "https://example.com"

# Create from template
gh repo create my-repo --template owner/template-repo
```

### Edit Repository
```bash
# Update description
gh repo edit --description "New description"

# Update homepage
gh repo edit --homepage "https://example.com"

# Add topics
gh repo edit --add-topic topic1,topic2,topic3

# Remove topics
gh repo edit --remove-topic topic1,topic2

# Change visibility
gh repo edit --visibility public
gh repo edit --visibility private

# Enable/disable features
gh repo edit --enable-issues
gh repo edit --disable-wiki
gh repo edit --enable-projects
```

### Clone Repository
```bash
# Clone repository
gh repo clone owner/repo

# Clone to specific directory
gh repo clone owner/repo path/to/dir
```

### Fork Repository
```bash
# Fork repository
gh repo fork

# Fork specific repository
gh repo fork owner/repo

# Fork and clone
gh repo fork owner/repo --clone
```

### Delete Repository
```bash
# Delete repository (requires confirmation)
gh repo delete owner/repo

# Delete without confirmation
gh repo delete owner/repo --yes
```

### List Repositories
```bash
# List your repositories
gh repo list

# List organization repositories
gh repo list organization-name

# List with filters
gh repo list --public
gh repo list --private
gh repo list --fork
gh repo list --source

# Limit number of results
gh repo list --limit 50
```

## Issue Commands

### Create Issue
```bash
# Interactive create
gh issue create

# Create with title and body
gh issue create --title "Bug report" --body "Description"

# Create with labels
gh issue create --title "Title" --label bug,high-priority

# Create with assignee
gh issue create --title "Title" --assignee username

# Create with milestone
gh issue create --title "Title" --milestone "v1.0"

# Create from template
gh issue create --template bug_report.md

# Create in specific repository
gh issue create --repo owner/repo --title "Title"
```

### List Issues
```bash
# List open issues
gh issue list

# List all issues
gh issue list --state all

# List closed issues
gh issue list --state closed

# Filter by label
gh issue list --label bug

# Filter by assignee
gh issue list --assignee username
gh issue list --assignee @me

# Filter by author
gh issue list --author username

# Filter by mention
gh issue list --mention username

# Limit results
gh issue list --limit 50

# Output as JSON
gh issue list --json number,title,state
```

### View Issue
```bash
# View issue
gh issue view 123

# View in browser
gh issue view 123 --web

# View with comments
gh issue view 123 --comments

# Output as JSON
gh issue view 123 --json number,title,body,state
```

### Edit Issue
```bash
# Edit title
gh issue edit 123 --title "New title"

# Edit body
gh issue edit 123 --body "New description"

# Add labels
gh issue edit 123 --add-label bug,high-priority

# Remove labels
gh issue edit 123 --remove-label low-priority

# Add assignee
gh issue edit 123 --add-assignee username

# Remove assignee
gh issue edit 123 --remove-assignee username

# Set milestone
gh issue edit 123 --milestone "v1.0"
```

### Close/Reopen Issue
```bash
# Close issue
gh issue close 123

# Close with comment
gh issue close 123 --comment "Fixed in PR #456"

# Reopen issue
gh issue reopen 123

# Reopen with comment
gh issue reopen 123 --comment "Still an issue"
```

### Comment on Issue
```bash
# Add comment
gh issue comment 123 --body "Comment text"

# Edit comment (requires comment ID)
gh issue comment 123 --edit-last
```

## Pull Request Commands

### Create Pull Request
```bash
# Interactive create
gh pr create

# Create with title and body
gh pr create --title "Feature" --body "Description"

# Create with base and head branches
gh pr create --base main --head feature-branch

# Create as draft
gh pr create --draft

# Create with reviewers
gh pr create --reviewer user1,user2

# Create with assignees
gh pr create --assignee user1

# Create with labels
gh pr create --label bug,high-priority

# Fill from commits
gh pr create --fill

# Fill verbose (detailed from commits)
gh pr create --fill-verbose
```

### List Pull Requests
```bash
# List open PRs
gh pr list

# List all PRs
gh pr list --state all

# List by author
gh pr list --author username
gh pr list --author @me

# List by assignee
gh pr list --assignee username

# List by label
gh pr list --label bug

# List drafts
gh pr list --draft

# Limit results
gh pr list --limit 50
```

### View Pull Request
```bash
# View PR
gh pr view 123

# View in browser
gh pr view 123 --web

# View with comments
gh pr view 123 --comments

# Output as JSON
gh pr view 123 --json number,title,state,reviews
```

### Edit Pull Request
```bash
# Edit title
gh pr edit 123 --title "New title"

# Edit body
gh pr edit 123 --body "New description"

# Add reviewer
gh pr edit 123 --add-reviewer username

# Remove reviewer
gh pr edit 123 --remove-reviewer username

# Add assignee
gh pr edit 123 --add-assignee username

# Add label
gh pr edit 123 --add-label bug

# Convert to draft
gh pr ready 123 --undo

# Mark as ready
gh pr ready 123
```

### Review Pull Request
```bash
# Approve PR
gh pr review 123 --approve

# Request changes
gh pr review 123 --request-changes --body "Please fix..."

# Add comment
gh pr review 123 --comment --body "Looks good"

# Review with file comments
gh pr review 123 --comment --body-file review.md
```

### Check PR Status
```bash
# Check CI/CD status
gh pr checks 123

# Watch checks (live updates)
gh pr checks 123 --watch

# Check specific check
gh pr checks 123 --check "Test Suite"
```

### Merge Pull Request
```bash
# Merge PR
gh pr merge 123

# Merge with merge commit
gh pr merge 123 --merge

# Squash and merge
gh pr merge 123 --squash

# Rebase and merge
gh pr merge 123 --rebase

# Delete branch after merge
gh pr merge 123 --delete-branch

# Auto-merge when checks pass
gh pr merge 123 --auto

# Merge without confirmation
gh pr merge 123 --squash --delete-branch --yes
```

### Diff Pull Request
```bash
# Show diff
gh pr diff 123

# Show diff for specific file
gh pr diff 123 -- path/to/file.txt
```

### Checkout Pull Request
```bash
# Checkout PR branch
gh pr checkout 123

# Checkout with branch name
gh pr checkout 123 --branch feature-branch
```

### Close Pull Request
```bash
# Close PR
gh pr close 123

# Close with comment
gh pr close 123 --comment "Not needed"

# Reopen PR
gh pr reopen 123
```

## Release Commands

### Create Release
```bash
# Interactive create
gh release create v1.0.0

# Create with title and notes
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"

# Create with notes from file
gh release create v1.0.0 --notes-file CHANGELOG.md

# Auto-generate notes
gh release create v1.0.0 --generate-notes

# Create as draft
gh release create v1.0.0 --draft

# Create as pre-release
gh release create v1.0.0 --prerelease

# Create with assets
gh release create v1.0.0 file1.zip file2.tar.gz
```

### List Releases
```bash
# List releases
gh release list

# Limit results
gh release list --limit 20
```

### View Release
```bash
# View release
gh release view v1.0.0

# View in browser
gh release view v1.0.0 --web

# Output as JSON
gh release view v1.0.0 --json name,tagName,assets
```

### Edit Release
```bash
# Edit title
gh release edit v1.0.0 --title "New title"

# Edit notes
gh release edit v1.0.0 --notes "Updated notes"

# Publish draft
gh release edit v1.0.0 --draft=false

# Mark as production release
gh release edit v1.0.0 --prerelease=false
```

### Upload Assets
```bash
# Upload assets
gh release upload v1.0.0 file1.zip file2.tar.gz

# Upload with label
gh release upload v1.0.0 file.zip#"Download"
```

### Download Assets
```bash
# Download all assets
gh release download v1.0.0

# Download specific asset
gh release download v1.0.0 --pattern "*.zip"

# Download to directory
gh release download v1.0.0 --dir downloads/
```

### Delete Release
```bash
# Delete release (keeps tag)
gh release delete v1.0.0

# Delete release without confirmation
gh release delete v1.0.0 --yes

# Delete release and tag
gh release delete v1.0.0 --yes && git push --delete origin v1.0.0
```

## Workflow Commands

### List Workflows
```bash
# List workflows
gh workflow list

# List all workflows
gh workflow list --all
```

### View Workflow
```bash
# View workflow
gh workflow view workflow-name.yml

# View in browser
gh workflow view workflow-name.yml --web
```

### Run Workflow
```bash
# Run workflow
gh workflow run workflow-name.yml

# Run with inputs
gh workflow run workflow.yml -f input1=value1 -f input2=value2

# Run on specific branch
gh workflow run workflow.yml --ref branch-name
```

### Enable/Disable Workflow
```bash
# Enable workflow
gh workflow enable workflow-name.yml

# Disable workflow
gh workflow disable workflow-name.yml
```

## Run Commands

### List Runs
```bash
# List workflow runs
gh run list

# List runs for specific workflow
gh run list --workflow workflow-name.yml

# Limit results
gh run list --limit 20

# Filter by status
gh run list --status success
gh run list --status failure
gh run list --status in_progress
```

### View Run
```bash
# View run
gh run view 12345

# View run in browser
gh run view 12345 --web

# View run logs
gh run view 12345 --log

# View specific job logs
gh run view 12345 --log --job "Test Suite"
```

### Download Artifacts
```bash
# Download all artifacts
gh run download 12345

# Download specific artifact
gh run download 12345 --name artifact-name

# Download to directory
gh run download 12345 --dir downloads/
```

### Watch Run
```bash
# Watch run (live updates)
gh run watch 12345
```

### Rerun Workflow
```bash
# Rerun workflow
gh run rerun 12345

# Rerun failed jobs only
gh run rerun 12345 --failed
```

### Cancel Run
```bash
# Cancel run
gh run cancel 12345
```

## API Commands

### Make API Request
```bash
# GET request
gh api repos/owner/repo

# POST request
gh api repos/owner/repo/issues -f title="Title" -f body="Body"

# PUT request
gh api repos/owner/repo/topics -X PUT -f names[]=topic1 -f names[]=topic2

# Paginate results
gh api --paginate repos/owner/repo/issues

# Output as JSON
gh api repos/owner/repo --jq .name
```

## Global Options

### Common Flags
```bash
# Specify repository
--repo owner/repo

# Output as JSON
--json field1,field2

# Use JQ query
--jq '.field'

# Template output
--template '{{.field}}'

# Help
--help
```

## Useful Combinations

### Complete PR Workflow
```bash
# Create, review, and merge PR
git checkout -b feature-branch
# Make changes
git push -u origin feature-branch
gh pr create --fill
gh pr checks --watch
gh pr review --approve
gh pr merge --squash --delete-branch
```

### Complete Release Workflow
```bash
# Create release with auto-generated notes
gh release create v1.0.0 --generate-notes
gh release upload v1.0.0 dist/*.zip
```

### Update Repository Metadata
```bash
# Update all metadata at once
gh repo edit \
  --description "New description" \
  --homepage "https://example.com" \
  --add-topic topic1,topic2,topic3
```

---

For more information, visit: https://cli.github.com/manual/
