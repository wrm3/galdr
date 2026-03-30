"""
vault_rest.py — Vault Knowledge Graph Browser (DB-backed)

Starlette routes for browsing, searching, and visualizing vault notes
stored in the vault_notes PostgreSQL table.

Routes (added to VAULT_ROUTES list, merged into server.py's Starlette app):
  GET  /vault            — Browser UI (self-contained HTML)
  GET  /vault/tree       — Folder tree JSON
  GET  /vault/note       — Single note content JSON (?path=...)
  GET  /vault/search     — Search notes JSON (?q=...&mode=...)
  GET  /vault/graph      — Knowledge graph data JSON (nodes + edges from [[wikilinks]])
  GET  /vault/stats      — Vault statistics JSON
"""
import json
import logging
from typing import Optional

from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route

logger = logging.getLogger(__name__)

_db = None
_embedding_gen = None


def init_vault_rest(*, db=None, embedding_generator=None):
    global _db, _embedding_gen
    _db = db
    _embedding_gen = embedding_generator
    logger.info("vault_rest initialized (DB-backed)")


def _get_cursor():
    return _db.get_cursor()


# ── API Endpoints ────────────────────────────────────────────────────────────

async def vault_tree(request: Request) -> JSONResponse:
    """Return folder tree structure from vault_notes paths."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    with _get_cursor() as cur:
        cur.execute("""
            SELECT path, title, note_type, tags, updated_at
            FROM vault_notes
            ORDER BY path
        """)
        rows = cur.fetchall()

    tree = {}
    for row in rows:
        parts = row["path"].split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {"_children": {}})["_children"]
        filename = parts[-1]
        node[filename] = {
            "path": row["path"],
            "title": row["title"],
            "type": row["note_type"],
            "tags": row["tags"] or [],
            "updated": str(row["updated_at"]),
        }

    return JSONResponse({"tree": tree, "total": len(rows)})


async def vault_note(request: Request) -> JSONResponse:
    """Return full note content by path."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    path = request.query_params.get("path", "")
    if not path:
        return JSONResponse({"error": "path parameter required"}, status_code=400)

    with _get_cursor() as cur:
        cur.execute("""
            SELECT path, title, note_type, note_date, tags, aliases,
                   url, source, content, body, frontmatter, links,
                   created_at, updated_at
            FROM vault_notes WHERE path = %s
        """, (path,))
        row = cur.fetchone()

    if not row:
        return JSONResponse({"error": f"Note not found: {path}"}, status_code=404)

    return JSONResponse({
        "path": row["path"],
        "title": row["title"],
        "type": row["note_type"],
        "date": str(row["note_date"]) if row["note_date"] else None,
        "tags": row["tags"] or [],
        "aliases": row["aliases"] or [],
        "url": row.get("url", ""),
        "content": row["content"],
        "body": row["body"],
        "frontmatter": row["frontmatter"],
        "links": row["links"] or [],
        "created_at": str(row["created_at"]),
        "updated_at": str(row["updated_at"]),
    })


async def vault_search_api(request: Request) -> JSONResponse:
    """Search vault notes — semantic or keyword."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    q = request.query_params.get("q", "")
    mode = request.query_params.get("mode", "keyword")
    note_type = request.query_params.get("type", "")
    limit = min(int(request.query_params.get("limit", "20")), 100)

    if not q:
        return JSONResponse({"error": "q parameter required"}, status_code=400)

    results = []

    if mode == "semantic" and _embedding_gen:
        try:
            query_embedding = _embedding_gen.generate(q)
            with _get_cursor() as cur:
                type_filter = "AND note_type = %s" if note_type else ""
                params = [query_embedding, query_embedding]
                if note_type:
                    params.insert(1, note_type)
                sql = f"""
                    SELECT path, title, note_type, tags, url,
                           LEFT(body, 300) AS snippet,
                           1 - (embedding <=> %s::vector) AS similarity
                    FROM vault_notes
                    WHERE embedding IS NOT NULL {type_filter}
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """
                params.append(limit)
                cur.execute(sql, params)
                for row in cur.fetchall():
                    results.append({
                        "path": row["path"],
                        "title": row["title"],
                        "type": row["note_type"],
                        "tags": row["tags"] or [],
                        "url": row.get("url", ""),
                        "snippet": row["snippet"],
                        "score": round(float(row["similarity"]), 4),
                    })
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            mode = "keyword"  # fallback

    if mode == "keyword" or (mode == "semantic" and not results):
        with _get_cursor() as cur:
            ts_query = " & ".join(q.split())
            type_filter = "AND note_type = %s" if note_type else ""
            params = [ts_query, ts_query]
            if note_type:
                params.append(note_type)
            params.append(limit)
            sql = f"""
                SELECT path, title, note_type, tags, url,
                       LEFT(body, 300) AS snippet,
                       ts_rank(to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, '')),
                               to_tsquery('english', %s)) AS rank
                FROM vault_notes
                WHERE to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))
                      @@ to_tsquery('english', %s) {type_filter}
                ORDER BY rank DESC
                LIMIT %s
            """
            cur.execute(sql, params)
            for row in cur.fetchall():
                results.append({
                    "path": row["path"],
                    "title": row["title"],
                    "type": row["note_type"],
                    "tags": row["tags"] or [],
                    "url": row.get("url", ""),
                    "snippet": row["snippet"],
                    "score": round(float(row["rank"]), 4),
                })

    return JSONResponse({"query": q, "mode": mode, "count": len(results), "results": results})


async def vault_graph(request: Request) -> JSONResponse:
    """Return knowledge graph data (nodes + edges from [[wikilinks]])."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    with _get_cursor() as cur:
        cur.execute("""
            SELECT path, title, note_type, tags, links
            FROM vault_notes
        """)
        rows = cur.fetchall()

    path_set = {r["path"] for r in rows}
    nodes = []
    edges = []

    for row in rows:
        nodes.append({
            "id": row["path"],
            "label": row["title"] or row["path"].split("/")[-1],
            "type": row["note_type"] or "note",
            "tags": row["tags"] or [],
        })
        for link in (row["links"] or []):
            # Resolve wikilink to path
            target = None
            for p in path_set:
                stem = p.rsplit("/", 1)[-1].replace(".md", "")
                if stem == link or p == link or p.endswith(f"/{link}.md"):
                    target = p
                    break
            if target:
                edges.append({"source": row["path"], "target": target})

    return JSONResponse({
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
    })


async def vault_stats(request: Request) -> JSONResponse:
    """Return vault statistics."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    with _get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM vault_notes")
        total = cur.fetchone()["total"]

        cur.execute("""
            SELECT note_type, COUNT(*) AS cnt
            FROM vault_notes
            GROUP BY note_type
            ORDER BY cnt DESC
        """)
        by_type = {r["note_type"] or "untyped": r["cnt"] for r in cur.fetchall()}

        cur.execute("SELECT COUNT(*) AS cnt FROM vault_notes WHERE embedding IS NOT NULL")
        with_embeddings = cur.fetchone()["cnt"]

        cur.execute("""
            SELECT COUNT(*) AS cnt FROM vault_notes
            WHERE array_length(links, 1) > 0
        """)
        with_links = cur.fetchone()["cnt"]

    return JSONResponse({
        "total_notes": total,
        "by_type": by_type,
        "with_embeddings": with_embeddings,
        "with_links": with_links,
    })


# ── HTML UI ──────────────────────────────────────────────────────────────────

async def vault_ui(request: Request) -> HTMLResponse:
    """Self-contained vault browser UI."""
    return HTMLResponse(_VAULT_HTML)


_VAULT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>galdr Vault</title>
<style>
:root { --bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #e6edf3;
        --muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --orange: #d29922; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
       background: var(--bg); color: var(--text); display: flex; height: 100vh; }
#sidebar { width: 300px; border-right: 1px solid var(--border); overflow-y: auto;
           background: var(--surface); flex-shrink: 0; }
#sidebar h2 { padding: 16px; font-size: 14px; color: var(--muted); border-bottom: 1px solid var(--border); }
#main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
#toolbar { padding: 12px 16px; border-bottom: 1px solid var(--border); display: flex; gap: 8px;
           background: var(--surface); }
#toolbar input { flex: 1; background: var(--bg); border: 1px solid var(--border); color: var(--text);
                 padding: 8px 12px; border-radius: 6px; font-size: 14px; }
#toolbar select { background: var(--bg); border: 1px solid var(--border); color: var(--text);
                  padding: 8px; border-radius: 6px; }
#toolbar button { background: var(--accent); color: #fff; border: none; padding: 8px 16px;
                  border-radius: 6px; cursor: pointer; font-weight: 600; }
#content { flex: 1; overflow-y: auto; padding: 24px; }
.tree-folder { cursor: pointer; padding: 4px 8px; color: var(--muted); font-size: 13px; }
.tree-folder:hover { color: var(--accent); }
.tree-file { padding: 4px 8px 4px 24px; cursor: pointer; font-size: 13px; white-space: nowrap;
             overflow: hidden; text-overflow: ellipsis; }
.tree-file:hover { background: var(--bg); color: var(--accent); }
.note-title { font-size: 24px; margin-bottom: 8px; }
.note-meta { color: var(--muted); font-size: 13px; margin-bottom: 16px; }
.note-meta span { margin-right: 12px; }
.tag { display: inline-block; background: #1f6feb33; color: var(--accent); padding: 2px 8px;
       border-radius: 12px; font-size: 12px; margin-right: 4px; }
.note-body { line-height: 1.7; white-space: pre-wrap; font-family: monospace; font-size: 14px; }
.search-result { padding: 12px; border: 1px solid var(--border); border-radius: 8px;
                 margin-bottom: 8px; cursor: pointer; }
.search-result:hover { border-color: var(--accent); }
.search-result h3 { font-size: 15px; margin-bottom: 4px; }
.search-result .snippet { color: var(--muted); font-size: 13px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
             padding: 16px; text-align: center; }
.stat-card .number { font-size: 32px; font-weight: bold; color: var(--accent); }
.stat-card .label { color: var(--muted); font-size: 13px; margin-top: 4px; }
#graph-container { width: 100%; height: 100%; }
.tab-bar { display: flex; gap: 0; border-bottom: 1px solid var(--border); background: var(--surface); }
.tab { padding: 10px 20px; cursor: pointer; color: var(--muted); border-bottom: 2px solid transparent;
       font-size: 14px; }
.tab:hover { color: var(--text); }
.tab.active { color: var(--accent); border-bottom-color: var(--accent); }
</style>
</head>
<body>
<div id="sidebar">
  <h2>VAULT EXPLORER</h2>
  <div id="tree">Loading...</div>
</div>
<div id="main">
  <div class="tab-bar">
    <div class="tab active" data-tab="browse" onclick="switchTab('browse')">Browse</div>
    <div class="tab" data-tab="search" onclick="switchTab('search')">Search</div>
    <div class="tab" data-tab="graph" onclick="switchTab('graph')">Graph</div>
    <div class="tab" data-tab="stats" onclick="switchTab('stats')">Stats</div>
  </div>
  <div id="toolbar">
    <input id="search-input" placeholder="Search vault..." onkeydown="if(event.key==='Enter')doSearch()">
    <select id="search-mode">
      <option value="keyword">Keyword</option>
      <option value="semantic">Semantic</option>
    </select>
    <button onclick="doSearch()">Search</button>
  </div>
  <div id="content">Select a note from the sidebar or search.</div>
</div>
<script>
const BASE = window.location.pathname.replace(/\\/$/, '');
let currentTab = 'browse';

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  if (tab === 'stats') loadStats();
  if (tab === 'graph') loadGraph();
  if (tab === 'browse') document.getElementById('content').innerHTML = 'Select a note from the sidebar.';
  if (tab === 'search') document.getElementById('content').innerHTML = 'Type a query and press Search.';
}

async function loadTree() {
  const resp = await fetch(BASE + '/tree');
  const data = await resp.json();
  document.getElementById('tree').innerHTML = renderTree(data.tree, 0);
}

function renderTree(node, depth) {
  let html = '';
  for (const [key, val] of Object.entries(node)) {
    if (key === '_children') continue;
    if (val._children) {
      html += '<div class="tree-folder" style="padding-left:' + (8 + depth * 12) + 'px" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display===\\'none\\'?\\'block\\':\\'none\\'">' +
              '📁 ' + key + '</div><div>' + renderTree(val._children, depth + 1) + '</div>';
    } else if (val.path) {
      html += '<div class="tree-file" style="padding-left:' + (8 + depth * 12) + 'px" onclick="loadNote(\\'' +
              val.path.replace(/'/g, "\\\\'") + '\\')">' + (val.title || key) + '</div>';
    }
  }
  return html;
}

async function loadNote(path) {
  switchTab('browse');
  const resp = await fetch(BASE + '/note?path=' + encodeURIComponent(path));
  const note = await resp.json();
  if (note.error) { document.getElementById('content').innerHTML = '<p>' + note.error + '</p>'; return; }
  let tags = (note.tags || []).map(t => '<span class="tag">' + t + '</span>').join('');
  let links = (note.links || []).map(l => '<a href="#" onclick="loadNote(\\'' + l + '.md\\')" style="color:var(--accent)">' + l + '</a>').join(', ');
  document.getElementById('content').innerHTML =
    '<h1 class="note-title">' + (note.title || path) + '</h1>' +
    '<div class="note-meta"><span>' + (note.type || '') + '</span><span>' + (note.date || '') + '</span>' + tags + '</div>' +
    (note.url ? '<div class="note-meta"><a href="' + note.url + '" target="_blank" style="color:var(--accent)">' + note.url + '</a></div>' : '') +
    (links ? '<div class="note-meta">Links: ' + links + '</div>' : '') +
    '<pre class="note-body">' + escapeHtml(note.body || note.content) + '</pre>';
}

async function doSearch() {
  switchTab('search');
  const q = document.getElementById('search-input').value;
  const mode = document.getElementById('search-mode').value;
  if (!q) return;
  const resp = await fetch(BASE + '/search?q=' + encodeURIComponent(q) + '&mode=' + mode);
  const data = await resp.json();
  if (!data.results || data.results.length === 0) {
    document.getElementById('content').innerHTML = '<p>No results found.</p>';
    return;
  }
  document.getElementById('content').innerHTML = data.results.map(r =>
    '<div class="search-result" onclick="loadNote(\\'' + r.path.replace(/'/g, "\\\\'") + '\\')">' +
    '<h3>' + (r.title || r.path) + ' <small style="color:var(--muted)">(' + (r.score || 0) + ')</small></h3>' +
    '<div class="snippet">' + escapeHtml(r.snippet || '') + '</div>' +
    '<div style="margin-top:4px">' + (r.tags || []).map(t => '<span class="tag">' + t + '</span>').join('') + '</div>' +
    '</div>'
  ).join('');
}

async function loadStats() {
  const resp = await fetch(BASE + '/stats');
  const s = await resp.json();
  let typeCards = Object.entries(s.by_type || {}).map(([t, c]) =>
    '<div class="stat-card"><div class="number">' + c + '</div><div class="label">' + (t || 'untyped') + '</div></div>'
  ).join('');
  document.getElementById('content').innerHTML =
    '<div class="stats-grid">' +
    '<div class="stat-card"><div class="number">' + s.total_notes + '</div><div class="label">Total Notes</div></div>' +
    '<div class="stat-card"><div class="number">' + s.with_embeddings + '</div><div class="label">With Embeddings</div></div>' +
    '<div class="stat-card"><div class="number">' + s.with_links + '</div><div class="label">With Links</div></div>' +
    typeCards + '</div>';
}

async function loadGraph() {
  const resp = await fetch(BASE + '/graph');
  const data = await resp.json();
  let html = '<div style="padding:16px"><h2>Knowledge Graph</h2><p style="color:var(--muted)">' +
    data.node_count + ' nodes, ' + data.edge_count + ' edges</p>' +
    '<div style="margin-top:16px">';
  const typeColors = { video_summary: 'var(--green)', harvest: 'var(--orange)', research: 'var(--accent)', platform_docs: '#bc8cff' };
  for (const node of data.nodes.slice(0, 200)) {
    const color = typeColors[node.type] || 'var(--muted)';
    html += '<span style="display:inline-block;margin:4px;padding:4px 10px;border:1px solid ' + color +
      ';border-radius:16px;font-size:12px;color:' + color + ';cursor:pointer" onclick="loadNote(\\'' +
      node.id.replace(/'/g, "\\\\'") + '\\')">' + node.label + '</span>';
  }
  html += '</div></div>';
  document.getElementById('content').innerHTML = html;
}

function escapeHtml(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

loadTree();
</script>
</body>
</html>"""


# ── Route Table ──────────────────────────────────────────────────────────────

VAULT_ROUTES = [
    Route("/vault", vault_ui, methods=["GET"]),
    Route("/vault/tree", vault_tree, methods=["GET"]),
    Route("/vault/note", vault_note, methods=["GET"]),
    Route("/vault/search", vault_search_api, methods=["GET"]),
    Route("/vault/graph", vault_graph, methods=["GET"]),
    Route("/vault/stats", vault_stats, methods=["GET"]),
]
