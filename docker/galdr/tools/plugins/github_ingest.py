"""
github_ingest — Fetch GitHub repo metadata + README and index into vault_notes.

Accepts a GitHub repo URL, fetches metadata via the GitHub API (no auth needed
for public repos), downloads README and optionally other files, generates a
structured vault note with embedding, and stores in vault_notes.
"""
import hashlib
import logging
import os
import re
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

TOOL_NAME = "github_ingest"

TOOL_DESCRIPTION = (
    "Fetch a GitHub repository's metadata, README, and key files, then index "
    "as a vault note with embedding. No auth needed for public repos. "
    "Example: github_ingest(url='https://github.com/anthropics/skills')"
)

TOOL_PARAMS = {
    "url": "GitHub repo URL (e.g. https://github.com/owner/repo) — required",
    "tags": "List of tags (optional — repo topics are auto-added)",
    "refresh_policy": "Refresh policy: 'on_release' (default), 'weekly', 'none'",
    "include_files": "Additional files to fetch beyond README (e.g. ['AGENTS.md', 'pyproject.toml'])",
    "github_token": "GitHub personal access token for private repos (optional)",
}

_db = None
_embedding_gen = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db, _embedding_gen
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")


def _embed(text: str) -> Optional[list]:
    if not _embedding_gen:
        return None
    try:
        result = _embedding_gen.generate(text[:8000])
        return result.tolist() if hasattr(result, "tolist") else list(result)
    except Exception as e:
        _logger.warning("Embedding failed: %s", e)
        return None


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _parse_github_url(url: str) -> tuple[str, str]:
    """Extract owner and repo from a GitHub URL."""
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError(f"Invalid GitHub repo URL: {url}")
    owner = parts[0]
    repo = parts[1].replace(".git", "")
    return owner, repo


async def execute(
    url: str,
    tags: Optional[list] = None,
    refresh_policy: str = "on_release",
    include_files: Optional[list] = None,
    github_token: Optional[str] = None,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not url or not url.strip():
        return {"success": False, "error": "url is required"}

    import httpx

    url = url.strip().rstrip("/")
    tags = tags or []
    include_files = include_files or []

    try:
        owner, repo = _parse_github_url(url)
    except ValueError as e:
        return {"success": False, "error": str(e)}

    vault_path = f"ingested/github/{owner}/{repo}.md"
    api_base = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = github_token or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        async with httpx.AsyncClient(timeout=30, headers=headers, follow_redirects=True) as client:
            repo_resp = await client.get(api_base)
            if repo_resp.status_code == 404:
                return {"success": False, "error": f"Repo not found: {owner}/{repo}", "url": url}
            if repo_resp.status_code == 403:
                remaining = repo_resp.headers.get("X-RateLimit-Remaining", "?")
                limit = repo_resp.headers.get("X-RateLimit-Limit", "?")
                msg = f"GitHub API rate limit exceeded ({remaining}/{limit} remaining)."
                if not token:
                    msg += " Set GITHUB_TOKEN env var for 5000 req/hr."
                return {"success": False, "error": msg}
            repo_resp.raise_for_status()
            repo_data = repo_resp.json()

            readme_text = ""
            readme_resp = await client.get(f"{api_base}/readme", headers={"Accept": "application/vnd.github.v3.raw"})
            if readme_resp.status_code == 200:
                readme_text = readme_resp.text

            tree_items = []
            tree_resp = await client.get(f"{api_base}/git/trees/HEAD")
            if tree_resp.status_code == 200:
                tree_data = tree_resp.json()
                tree_items = [
                    {"path": item["path"], "type": item["type"]}
                    for item in tree_data.get("tree", [])[:50]
                ]

            extra_files = {}
            for fpath in include_files[:5]:
                f_resp = await client.get(
                    f"{api_base}/contents/{fpath}",
                    headers={"Accept": "application/vnd.github.v3.raw"},
                )
                if f_resp.status_code == 200:
                    extra_files[fpath] = f_resp.text[:4000]

    except httpx.HTTPError as e:
        _logger.error("GitHub API error for %s: %s", url, e)
        return {"success": False, "error": f"GitHub API error: {e}", "url": url}

    name = repo_data.get("full_name", f"{owner}/{repo}")
    description = repo_data.get("description", "") or ""
    stars = repo_data.get("stargazers_count", 0)
    language = repo_data.get("language", "")
    topics = repo_data.get("topics", [])
    last_push = repo_data.get("pushed_at", "")
    default_branch = repo_data.get("default_branch", "main")
    license_name = ""
    if repo_data.get("license"):
        license_name = repo_data["license"].get("spdx_id", "")

    all_tags = list(set(tags + topics))
    last_sha = last_push

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    readme_truncated = readme_text[:4000] if readme_text else "*No README found*"

    file_tree = "\n".join(
        f"  {'dir' if item['type'] == 'tree' else 'file'}: {item['path']}"
        for item in tree_items
    )

    extra_sections = ""
    for fpath, fcontent in extra_files.items():
        extra_sections += f"\n\n## {fpath}\n\n```\n{fcontent}\n```"

    frontmatter = (
        f"---\n"
        f'title: "{name}"\n'
        f'date: "{now}"\n'
        f"type: github_repo\n"
        f'source: "github"\n'
        f'url: "{url}"\n'
        f"ingestion_type: github_ingest\n"
        f"refresh_policy: {refresh_policy}\n"
        f"topics: {all_tags}\n"
        f"language: {language}\n"
        f"stars: {stars}\n"
        f'license: "{license_name}"\n'
        f'last_push: "{last_push}"\n'
        f'last_commit_sha: "{last_sha}"\n'
        f"---\n\n"
    )

    body = (
        f"# {name}\n\n"
        f"{description}\n\n"
        f"**Stars**: {stars} | **Language**: {language} | **License**: {license_name}\n\n"
        f"## File Tree\n\n```\n{file_tree}\n```\n\n"
        f"## README\n\n{readme_truncated}"
        f"{extra_sections}"
    )

    content = frontmatter + body
    ch = _content_hash(content)

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT content_hash FROM vault_notes WHERE path = %s", (vault_path,))
                row = cur.fetchone()
                if row:
                    existing_hash = row[0] if isinstance(row, tuple) else row.get("content_hash")
                    if existing_hash == ch:
                        return {
                            "success": True,
                            "path": vault_path,
                            "title": name,
                            "status": "unchanged",
                            "stars": stars,
                            "language": language,
                            "url": url,
                        }

                embedding = _embed(f"{name}\n{description}\n\n{readme_truncated[:3000]}")

                import json as _json
                fm_dict = {
                    "title": name, "date": now, "type": "github_repo",
                    "source": "github", "url": url,
                    "ingestion_type": "github_ingest",
                    "refresh_policy": refresh_policy, "topics": all_tags,
                    "language": language, "stars": stars,
                    "license": license_name, "last_push": last_push,
                }
                cur.execute(
                    """
                    INSERT INTO vault_notes
                        (path, title, content, body, content_hash, embedding,
                         note_type, source, source_type, url, tags,
                         frontmatter, links, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (path) DO UPDATE SET
                        title        = EXCLUDED.title,
                        content      = EXCLUDED.content,
                        body         = EXCLUDED.body,
                        content_hash = EXCLUDED.content_hash,
                        embedding    = EXCLUDED.embedding,
                        tags         = EXCLUDED.tags,
                        frontmatter  = EXCLUDED.frontmatter,
                        updated_at   = NOW()
                    """,
                    (vault_path, name, content, body, ch, embedding,
                     "github_repo", "github", "github_api", url, all_tags,
                     _json.dumps(fm_dict), []),
                )
                conn.commit()

        status = "updated" if row else "created"
        return {
            "success": True,
            "path": vault_path,
            "title": name,
            "status": status,
            "stars": stars,
            "language": language,
            "url": url,
        }
    except Exception as e:
        _logger.error("DB error ingesting %s: %s", url, e)
        return {"success": False, "error": str(e), "url": url}
