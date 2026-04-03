# GitHub API Reference Guide

Direct GitHub REST API usage for advanced integrations when `gh` CLI is insufficient.

## Authentication

### Personal Access Token

**Create Token:**
1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes based on needs
4. Copy token immediately (won't be shown again)

**Token Scopes:**
```
repo          - Full control of private repositories
public_repo   - Access public repositories only
repo:status   - Access commit status
repo_deployment - Access deployment status
read:org      - Read organization data
write:org     - Write organization data
admin:org     - Full organization access
workflow      - Update GitHub Action workflows
```

**Use Token:**
```bash
# In headers
curl -H "Authorization: token ghp_your_token_here" https://api.github.com/user

# Via gh CLI (preferred)
gh auth login --with-token < token.txt
```

## Rate Limits

### Limits by Authentication

**Unauthenticated:**
- 60 requests per hour per IP

**Authenticated (OAuth/Token):**
- 5,000 requests per hour per user
- Some endpoints have additional limits

**GitHub Apps:**
- 5,000 requests per hour per installation

### Check Rate Limit

```bash
# Via gh CLI
gh api rate_limit

# Via curl
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
```

**Response:**
```json
{
  "resources": {
    "core": {
      "limit": 5000,
      "remaining": 4999,
      "reset": 1372700873,
      "used": 1
    }
  }
}
```

## Repository Operations

### Get Repository

**Endpoint:** `GET /repos/{owner}/{repo}`

```bash
gh api repos/owner/repo

# With specific fields
gh api repos/owner/repo --jq '.name,.description,.topics'
```

**Response Fields:**
- `name` - Repository name
- `description` - Repository description
- `homepage` - Homepage URL
- `topics` - Repository topics (array)
- `private` - Public/private status
- `fork` - Is fork
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `pushed_at` - Last push timestamp
- `size` - Repository size in KB
- `stargazers_count` - Star count
- `watchers_count` - Watcher count
- `forks_count` - Fork count
- `open_issues_count` - Open issues count
- `default_branch` - Default branch name

### Update Repository

**Endpoint:** `PATCH /repos/{owner}/{repo}`

```bash
# Update description
gh api repos/owner/repo -X PATCH -f description="New description"

# Update homepage
gh api repos/owner/repo -X PATCH -f homepage="https://example.com"

# Update multiple fields
gh api repos/owner/repo -X PATCH \
  -f description="New description" \
  -f homepage="https://example.com" \
  -F has_issues=true
```

**Updatable Fields:**
- `name` - Repository name
- `description` - Description
- `homepage` - Homepage URL
- `private` - Make public/private
- `has_issues` - Enable/disable issues
- `has_projects` - Enable/disable projects
- `has_wiki` - Enable/disable wiki
- `default_branch` - Change default branch

### Repository Topics

**Get Topics:**
```bash
# Endpoint: GET /repos/{owner}/{repo}/topics
gh api repos/owner/repo/topics \
  -H "Accept: application/vnd.github.mercy-preview+json"
```

**Set Topics:**
```bash
# Endpoint: PUT /repos/{owner}/{repo}/topics
gh api repos/owner/repo/topics -X PUT \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  -f names[]=topic1 -f names[]=topic2 -f names[]=topic3
```

**Note:** The `/topics` endpoint replaces all topics. To add/remove individual topics, get current list, modify it, then set all topics.

### Delete Repository

**Endpoint:** `DELETE /repos/{owner}/{repo}`

```bash
gh api repos/owner/repo -X DELETE
```

**⚠️ Warning:** This is permanent and cannot be undone!

## Issue Operations

### List Issues

**Endpoint:** `GET /repos/{owner}/{repo}/issues`

```bash
# List open issues
gh api repos/owner/repo/issues

# With filters
gh api repos/owner/repo/issues \
  -f state=all \
  -f labels=bug,high-priority \
  -f assignee=username \
  -f creator=username \
  -f sort=created \
  -f direction=desc
```

**Query Parameters:**
- `state` - open, closed, all
- `labels` - Comma-separated list
- `assignee` - Username or "none"
- `creator` - Username
- `mentioned` - Username
- `milestone` - Milestone number or "none" or "*"
- `sort` - created, updated, comments
- `direction` - asc, desc
- `since` - ISO 8601 timestamp
- `per_page` - Results per page (max 100)
- `page` - Page number

### Get Issue

**Endpoint:** `GET /repos/{owner}/{repo}/issues/{issue_number}`

```bash
gh api repos/owner/repo/issues/123
```

### Create Issue

**Endpoint:** `POST /repos/{owner}/{repo}/issues`

```bash
gh api repos/owner/repo/issues -X POST \
  -f title="Issue title" \
  -f body="Issue description" \
  -f labels[]=bug \
  -f labels[]=high-priority \
  -f assignees[]=username1
```

**Required Fields:**
- `title` - Issue title

**Optional Fields:**
- `body` - Issue body/description
- `assignees` - Array of usernames
- `milestone` - Milestone number
- `labels` - Array of label names

### Update Issue

**Endpoint:** `PATCH /repos/{owner}/{repo}/issues/{issue_number}`

```bash
gh api repos/owner/repo/issues/123 -X PATCH \
  -f title="Updated title" \
  -f state="closed" \
  -f labels[]=bug
```

### Add Comment

**Endpoint:** `POST /repos/{owner}/{repo}/issues/{issue_number}/comments`

```bash
gh api repos/owner/repo/issues/123/comments -X POST \
  -f body="Comment text"
```

## Pull Request Operations

### List Pull Requests

**Endpoint:** `GET /repos/{owner}/{repo}/pulls`

```bash
# List open PRs
gh api repos/owner/repo/pulls

# With filters
gh api repos/owner/repo/pulls \
  -f state=all \
  -f head=user:branch \
  -f base=main \
  -f sort=created \
  -f direction=desc
```

**Query Parameters:**
- `state` - open, closed, all
- `head` - Filter by head user/branch (format: user:ref)
- `base` - Filter by base branch
- `sort` - created, updated, popularity, long-running
- `direction` - asc, desc

### Get Pull Request

**Endpoint:** `GET /repos/{owner}/{repo}/pulls/{pull_number}`

```bash
gh api repos/owner/repo/pulls/123
```

### Create Pull Request

**Endpoint:** `POST /repos/{owner}/{repo}/pulls`

```bash
gh api repos/owner/repo/pulls -X POST \
  -f title="PR title" \
  -f body="PR description" \
  -f head="feature-branch" \
  -f base="main"
```

**Required Fields:**
- `title` - PR title
- `head` - Branch containing changes
- `base` - Branch to merge into

**Optional Fields:**
- `body` - PR description
- `draft` - Create as draft (boolean)
- `maintainer_can_modify` - Allow maintainer edits (boolean)

### Update Pull Request

**Endpoint:** `PATCH /repos/{owner}/{repo}/pulls/{pull_number}`

```bash
gh api repos/owner/repo/pulls/123 -X PATCH \
  -f title="Updated title" \
  -f state="closed"
```

### Merge Pull Request

**Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge`

```bash
# Merge commit
gh api repos/owner/repo/pulls/123/merge -X PUT \
  -f commit_title="Merge PR #123" \
  -f merge_method="merge"

# Squash merge
gh api repos/owner/repo/pulls/123/merge -X PUT \
  -f merge_method="squash"

# Rebase merge
gh api repos/owner/repo/pulls/123/merge -X PUT \
  -f merge_method="rebase"
```

**Merge Methods:**
- `merge` - Create merge commit
- `squash` - Squash and merge
- `rebase` - Rebase and merge

### Review Pull Request

**Create Review:**
```bash
# Endpoint: POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
gh api repos/owner/repo/pulls/123/reviews -X POST \
  -f event="APPROVE" \
  -f body="Looks good!"
```

**Review Events:**
- `APPROVE` - Approve PR
- `REQUEST_CHANGES` - Request changes
- `COMMENT` - Comment without approval

## Release Operations

### List Releases

**Endpoint:** `GET /repos/{owner}/{repo}/releases`

```bash
gh api repos/owner/repo/releases
```

### Get Release

**Endpoint:** `GET /repos/{owner}/{repo}/releases/{release_id}`

```bash
# By ID
gh api repos/owner/repo/releases/12345

# By tag
gh api repos/owner/repo/releases/tags/v1.0.0
```

### Create Release

**Endpoint:** `POST /repos/{owner}/{repo}/releases`

```bash
gh api repos/owner/repo/releases -X POST \
  -f tag_name="v1.0.0" \
  -f name="Version 1.0.0" \
  -f body="Release notes" \
  -F draft=false \
  -F prerelease=false
```

**Required Fields:**
- `tag_name` - Git tag for release

**Optional Fields:**
- `name` - Release title
- `body` - Release notes
- `draft` - Create as draft (boolean)
- `prerelease` - Mark as pre-release (boolean)
- `target_commitish` - Commit/branch to tag (default: default branch)

### Update Release

**Endpoint:** `PATCH /repos/{owner}/{repo}/releases/{release_id}`

```bash
gh api repos/owner/repo/releases/12345 -X PATCH \
  -f name="Updated Version 1.0.0" \
  -f body="Updated release notes"
```

### Delete Release

**Endpoint:** `DELETE /repos/{owner}/{repo}/releases/{release_id}`

```bash
gh api repos/owner/repo/releases/12345 -X DELETE
```

## Workflow Operations

### List Workflows

**Endpoint:** `GET /repos/{owner}/{repo}/actions/workflows`

```bash
gh api repos/owner/repo/actions/workflows
```

### Get Workflow

**Endpoint:** `GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}`

```bash
gh api repos/owner/repo/actions/workflows/12345
```

### Trigger Workflow

**Endpoint:** `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches`

```bash
# Without inputs
gh api repos/owner/repo/actions/workflows/12345/dispatches -X POST \
  -f ref="main"

# With inputs
gh api repos/owner/repo/actions/workflows/12345/dispatches -X POST \
  -f ref="main" \
  -f inputs[key1]="value1" \
  -f inputs[key2]="value2"
```

### List Workflow Runs

**Endpoint:** `GET /repos/{owner}/{repo}/actions/runs`

```bash
# All runs
gh api repos/owner/repo/actions/runs

# For specific workflow
gh api repos/owner/repo/actions/workflows/12345/runs
```

### Get Workflow Run

**Endpoint:** `GET /repos/{owner}/{repo}/actions/runs/{run_id}`

```bash
gh api repos/owner/repo/actions/runs/67890
```

### Cancel Workflow Run

**Endpoint:** `POST /repos/{owner}/{repo}/actions/runs/{run_id}/cancel`

```bash
gh api repos/owner/repo/actions/runs/67890/cancel -X POST
```

### Re-run Workflow

**Endpoint:** `POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun`

```bash
# Re-run all jobs
gh api repos/owner/repo/actions/runs/67890/rerun -X POST

# Re-run failed jobs only
gh api repos/owner/repo/actions/runs/67890/rerun-failed-jobs -X POST
```

## Pagination

### Handling Paginated Results

GitHub API returns paginated results for list endpoints.

**Link Header:**
```
Link: <https://api.github.com/repos/owner/repo/issues?page=2>; rel="next",
      <https://api.github.com/repos/owner/repo/issues?page=10>; rel="last"
```

**Using gh CLI:**
```bash
# Auto-paginate (get all results)
gh api --paginate repos/owner/repo/issues

# Manual pagination
gh api repos/owner/repo/issues?per_page=100&page=1
gh api repos/owner/repo/issues?per_page=100&page=2
```

**Query Parameters:**
- `per_page` - Results per page (default: 30, max: 100)
- `page` - Page number (starts at 1)

## Error Handling

### HTTP Status Codes

**Success:**
- `200 OK` - Request succeeded
- `201 Created` - Resource created
- `204 No Content` - Successful deletion

**Client Errors:**
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions or rate limit
- `404 Not Found` - Resource doesn't exist
- `422 Unprocessable Entity` - Validation failed

**Server Errors:**
- `500 Internal Server Error` - GitHub server error
- `503 Service Unavailable` - GitHub temporarily unavailable

### Error Response Format

```json
{
  "message": "Not Found",
  "documentation_url": "https://docs.github.com/rest/reference/repos"
}
```

### Rate Limit Headers

Every API response includes rate limit headers:

```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1372700873
X-RateLimit-Used: 1
```

## Best Practices

### 1. Use gh CLI When Possible

```bash
# Preferred
gh repo view --json repositoryTopics

# Instead of
curl -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  https://api.github.com/repos/owner/repo/topics
```

### 2. Cache Responses

Cache responses for data that doesn't change frequently:
- Repository topics
- User lists
- Issue types
- Labels

### 3. Handle Rate Limits

```bash
# Check before making requests
remaining=$(gh api rate_limit --jq '.resources.core.remaining')
if [ "$remaining" -lt 100 ]; then
  echo "Rate limit low, waiting..."
  sleep 60
fi
```

### 4. Use Conditional Requests

Use `ETag` headers to avoid unnecessary API calls:

```bash
# First request
response=$(gh api repos/owner/repo -i)
etag=$(echo "$response" | grep -i etag | cut -d' ' -f2)

# Subsequent request
gh api repos/owner/repo -H "If-None-Match: $etag"
# Returns 304 Not Modified if unchanged
```

### 5. Batch Operations

Use GraphQL API for batch operations (multiple resources in one request).

### 6. Error Recovery

```bash
response=$(gh api repos/owner/repo 2>&1)
if [ $? -ne 0 ]; then
  if echo "$response" | grep -q "rate limit"; then
    # Handle rate limit
    echo "Rate limited, waiting..."
  elif echo "$response" | grep -q "404"; then
    # Handle not found
    echo "Repository not found"
  else
    # Generic error
    echo "API error: $response"
  fi
fi
```

## Python Example

```python
import requests
import os

class GitHubAPI:
    def __init__(self, token=None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_repo(self, owner, repo):
        url = f'{self.base_url}/repos/{owner}/{repo}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_repo_topics(self, owner, repo, topics):
        url = f'{self.base_url}/repos/{owner}/{repo}/topics'
        headers = {
            **self.headers,
            'Accept': 'application/vnd.github.mercy-preview+json'
        }
        data = {'names': topics}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def create_issue(self, owner, repo, title, body=None, labels=None):
        url = f'{self.base_url}/repos/{owner}/{repo}/issues'
        data = {'title': title}
        if body:
            data['body'] = body
        if labels:
            data['labels'] = labels
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

# Usage
api = GitHubAPI()
repo = api.get_repo('owner', 'repo')
print(f"Repository: {repo['name']}")

# Update topics
topics = ['claude-code', 'cursor', 'ai-assistant']
api.update_repo_topics('owner', 'repo', topics)
```

## Resources

- **GitHub REST API Docs:** https://docs.github.com/en/rest
- **GitHub CLI Manual:** https://cli.github.com/manual/
- **API Rate Limits:** https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
- **GraphQL API:** https://docs.github.com/en/graphql (for advanced batch operations)

---

**Note:** Always use authentication to get higher rate limits and access to all features. Store tokens securely and never commit them to repositories.
