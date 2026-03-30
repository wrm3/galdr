"""
admin_db_rest.py — Portable Database Explorer for galdr

Starlette routes + psycopg2. No SQLAlchemy, no FastAPI required.

Routes (added to ADMIN_ROUTES list, merged into server.py's Starlette app):
  GET  /admin/db                               — Browser UI (self-contained HTML)
  GET  /admin/db/tables                        — Schema introspection JSON
  GET  /admin/db/tables/{schema}/{table}/data  — Paginated rows JSON
  POST /admin/db/query                         — Read-only SQL runner JSON
  GET  /admin/galdr                            — Task dependency visualizer UI
  GET  /admin/galdr/data                       — Task graph data JSON
  GET  /admin/galdr/task/{task_id}             — Raw task file content JSON
"""
import os
import re
import glob as _glob
import time
import logging
import uuid as _uuid
from datetime import datetime as _dt, date as _date
from decimal import Decimal as _Dec
from typing import Optional

import yaml

from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route

logger = logging.getLogger(__name__)

ALLOWED_SCHEMAS = ("public",)
MAX_QUERY_ROWS = 1000
_VALID_IDENT = re.compile(r"^[a-z_][a-z0-9_]*$")
_DANGEROUS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|COPY|EXECUTE|CALL)\b",
    re.IGNORECASE,
)

# JSONB-related error patterns for user-friendly hints
_JSONB_ERROR_PATTERNS = [
    ("operator does not exist: jsonb", "JSONB columns cannot use ~ directly. Try:\n  column::text ~ 'pattern'\nor\n  column @> '{\"key\":\"value\"}'::jsonb"),
    ("jsonb ~", "Use ::text cast for regex on JSONB: column::text ~ 'pattern'"),
    ("cannot cast type json", "Cast JSONB to text first: column::text"),
    ("operator does not exist: jsonb =", "For JSONB equality use: column @> '{\"key\":\"val\"}'::jsonb"),
    ("invalid input syntax for type json", "Check your JSONB literal — must be valid JSON in single quotes: '{\"key\":\"val\"}'::jsonb"),
]

# Default galdr project path (override via GALDR_PROJECT_PATH env var)
_GALDR_PROJECT_PATH = os.environ.get("GALDR_PROJECT_PATH", "")

_db = None


def init_admin_db(db) -> None:
    """Wire in the shared RAGDatabase instance from server.py."""
    global _db
    _db = db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _validate_readonly(sql: str) -> Optional[str]:
    stripped = sql.strip().rstrip(";").strip()
    if not stripped:
        return "Empty query"
    if _DANGEROUS.search(stripped):
        return "Only SELECT queries are allowed"
    upper = stripped.upper()
    if not (upper.startswith("SELECT") or upper.startswith("WITH") or upper.startswith("EXPLAIN")):
        return "Query must start with SELECT, WITH, or EXPLAIN"
    return None


def _safe_val(v):
    """Serialize a psycopg2 value to a JSON-safe Python type."""
    if v is None:
        return None
    if isinstance(v, _uuid.UUID):
        return str(v)
    if isinstance(v, (_dt, _date)):
        return v.isoformat()
    if isinstance(v, _Dec):
        return float(v)
    if isinstance(v, (bytes, memoryview)):
        return bytes(v).hex()
    # pgvector returns a list-like — truncate for display
    if hasattr(v, "__iter__") and not isinstance(v, (str, dict, list)):
        try:
            lst = list(v)
            return f"[vector({len(lst)})]"
        except Exception:
            return str(v)
    return v


def _rows_to_json(rows_raw) -> list[dict]:
    return [{k: _safe_val(v) for k, v in row.items()} for row in rows_raw]


# ---------------------------------------------------------------------------
# Embedded single-page HTML UI (dark theme, vanilla JS, no build step)
# ---------------------------------------------------------------------------

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>galdr DB Explorer</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:monospace;background:#0f172a;color:#e2e8f0;font-size:13px;height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{background:#1e293b;padding:10px 16px;display:flex;align-items:center;gap:14px;border-bottom:1px solid #334155;flex-shrink:0}
header h1{font-size:14px;color:#38bdf8;font-weight:600}
#st{font-size:11px;color:#64748b}
.main{display:flex;flex:1;overflow:hidden}
.sidebar{width:210px;background:#1e293b;border-right:1px solid #334155;overflow-y:auto;flex-shrink:0;display:flex;flex-direction:column}
.sidebar h2{font-size:10px;color:#475569;padding:9px 12px 5px;text-transform:uppercase;letter-spacing:.06em;flex-shrink:0}
.titem{padding:5px 12px;cursor:pointer;display:flex;justify-content:space-between;border-bottom:1px solid #0f172a;font-size:12px;align-items:center}
.titem:hover,.titem.active{background:#0f172a;color:#38bdf8}
.rc{font-size:10px;color:#475569}
.content{flex:1;display:flex;flex-direction:column;overflow:hidden}
.tabs{display:flex;background:#1e293b;border-bottom:1px solid #334155;flex-shrink:0}
.tab{padding:7px 16px;cursor:pointer;font-size:12px;color:#94a3b8;border-bottom:2px solid transparent;user-select:none}
.tab.active{color:#38bdf8;border-bottom-color:#38bdf8}
.panel{flex:1;overflow:auto;display:none;flex-direction:column}
.panel.active{display:flex}
table{width:100%;border-collapse:collapse;font-size:12px}
th{background:#1e293b;position:sticky;top:0;padding:5px 10px;text-align:left;color:#94a3b8;font-weight:500;white-space:nowrap;border-bottom:1px solid #334155;z-index:1}
td{padding:4px 10px;border-bottom:1px solid #1e293b;white-space:nowrap;max-width:260px;overflow:hidden;text-overflow:ellipsis;vertical-align:top}
tr:hover td{background:#1e293b}
.null{color:#334155;font-style:italic}.bt{color:#4ade80}.bf{color:#f87171}
.pg{display:flex;align-items:center;gap:8px;padding:6px 12px;background:#1e293b;border-top:1px solid #334155;font-size:11px;color:#64748b;flex-shrink:0}
.btn{background:#1e40af;color:#e2e8f0;border:none;padding:3px 10px;border-radius:3px;cursor:pointer;font-size:11px;font-family:monospace}
.btn:hover{background:#1d4ed8}.btn:disabled{opacity:.35;cursor:not-allowed}
.sc-row{display:grid;grid-template-columns:180px 1fr 90px;gap:0;border-bottom:1px solid #1e293b;padding:5px 10px;font-size:12px;align-items:center}
.sc-row:hover{background:#1e293b}
.badge{font-size:9px;border-radius:2px;padding:1px 4px;margin-left:4px;vertical-align:middle}
.pk{background:#78350f;color:#fde68a}.fk{background:#2e1065;color:#ddd6fe}.nullable{background:#0c4a6e;color:#7dd3fc}
.sql-pane{height:100%;display:flex;flex-direction:column}
.sql-bar{display:flex;gap:8px;padding:7px 12px;background:#1e293b;border-bottom:1px solid #334155;align-items:center;font-size:11px;color:#64748b;flex-shrink:0;flex-wrap:wrap}
textarea{flex:0 0 120px;background:#0f172a;color:#e2e8f0;border:none;border-bottom:1px solid #334155;padding:8px 12px;font-family:monospace;font-size:12px;resize:vertical;outline:none;width:100%;min-height:80px}
.qres{flex:1;overflow:auto}
.msg{padding:24px;color:#334155;text-align:center;font-size:12px}
.err{color:#f87171}
.hint{color:#fbbf24;font-size:11px;background:#1c1700;border:1px solid #78350f;border-radius:3px;padding:6px 10px;margin:8px 12px;white-space:pre-wrap;font-family:monospace}
.pgcode{color:#94a3b8;font-size:10px}
.err-box{background:#1a0505;border:1px solid #7f1d1d;border-radius:3px;padding:8px 12px;margin:8px 12px;color:#f87171;font-family:monospace;font-size:11px;white-space:pre-wrap;text-align:left;cursor:text;user-select:text}
.sh{padding:4px 12px;font-size:10px;color:#475569;background:#1e293b;border-bottom:1px solid #334155;flex-shrink:0}
.badge-type{font-size:9px;border-radius:2px;padding:1px 4px;margin-left:4px;vertical-align:middle;background:#0c4a6e;color:#7dd3fc}
.badge-jsonb{background:#4c1d95;color:#ddd6fe}
.badge-text{background:#052e16;color:#86efac}
.badge-int{background:#1c1917;color:#d6d3d1}
.badge-ts{background:#0c1a2e;color:#93c5fd}
.snip-select{background:#1e293b;color:#94a3b8;border:1px solid #334155;border-radius:3px;font-size:11px;padding:2px 6px;cursor:pointer;font-family:monospace}
.snip-select option{background:#1e293b;color:#e2e8f0}
</style>
</head>
<body>
<header>
  <h1>⬡ galdr DB Explorer</h1>
  <span id="st">connecting…</span>
  <span style="margin-left:auto;font-size:10px;color:#334155">read-only · SELECT only</span>
</header>
<div class="main">
  <div class="sidebar">
    <h2>Tables</h2>
    <div id="tlist" style="overflow-y:auto;flex:1"><div class="msg">…</div></div>
  </div>
  <div class="content">
    <div class="tabs">
      <div class="tab active" onclick="showTab('data')">Data</div>
      <div class="tab" onclick="showTab('schema')">Schema</div>
      <div class="tab" onclick="showTab('sql')">SQL Runner</div>
    </div>
    <div id="panel-data" class="panel active"><div class="msg">Select a table from the sidebar</div></div>
    <div id="panel-schema" class="panel"><div class="msg">Select a table from the sidebar</div></div>
    <div id="panel-sql" class="panel sql-pane">
      <div class="sql-bar">
        <button class="btn" onclick="runQ()">▶ Run (Ctrl+Enter)</button>
        <select class="snip-select" onchange="insertSnippet(this)" title="JSONB query helpers">
          <option value="">📄 JSONB snippets…</option>
          <option value="WHERE {col}::text ~ '{pattern}'">Regex on JSONB column</option>
          <option value="WHERE {col} @> '{&quot;key&quot;:&quot;val&quot;}'::jsonb">Match JSON key/value</option>
          <option value="WHERE {col} ? 'key'">Has JSON key</option>
          <option value="WHERE {col} #>> '{key,nested}' = 'value'">Nested JSON path</option>
          <option value="{col}::text AS {col}_text">Cast JSONB to text</option>
          <option value="jsonb_pretty({col}) AS {col}_pretty">Pretty-print JSONB</option>
          <option value="jsonb_array_length({col})">Array length</option>
          <option value="jsonb_object_keys({col})">List all keys</option>
        </select>
        <span id="qmeta"></span>
      </div>
      <textarea id="qbox" placeholder="Write a SELECT query…"
        onkeydown="if(event.ctrlKey&&event.key==='Enter'){event.preventDefault();runQ();}"></textarea>
      <div class="qres" id="qres"><div class="msg">Write a SELECT query above and press ▶ Run</div></div>
    </div>
  </div>
</div>
<script>
'use strict';
let tables=[],active=null,page=1;
async function api(path,opts){
  const r=await fetch(path,opts);
  if(!r.ok){const e=await r.json().catch(()=>({error:r.statusText}));throw new Error(e.error||r.statusText);}
  return r.json();
}
function showTab(n){
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',['data','schema','sql'][i]===n));
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('active',p.id==='panel-'+n));
}
function fmt(v){
  if(v===null||v===undefined)return '<span class="null">NULL</span>';
  if(v===true)return '<span class="bt">true</span>';
  if(v===false)return '<span class="bf">false</span>';
  if(typeof v==='object')return JSON.stringify(v).slice(0,100);
  const s=String(v);return s.length>140?s.slice(0,140)+'…':s;
}
function grid(rows,cols){
  if(!rows.length)return '<div class="msg">No rows</div>';
  const ths=cols.map(c=>`<th>${c}</th>`).join('');
  const trs=rows.map(r=>'<tr>'+cols.map(c=>`<td>${fmt(r[c])}</td>`).join('')+'</tr>').join('');
  return `<table><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table>`;
}
async function loadTables(){
  try{
    const d=await api('/admin/db/tables');
    tables=d.tables;
    document.getElementById('st').textContent=`${d.total} tables`;
    document.getElementById('tlist').innerHTML=d.tables.map(t=>
      `<div class="titem" id="ti-${t.table_name}" onclick="sel('${t.schema}','${t.table_name}')">
        <span>${t.table_name}</span><span class="rc">${t.estimated_rows.toLocaleString()}</span>
      </div>`).join('');
  }catch(e){document.getElementById('st').innerHTML=`<span class="err">${e.message}</span>`;}
}
async function sel(schema,tname){
  active={schema,tname};page=1;
  document.querySelectorAll('.titem').forEach(el=>el.classList.toggle('active',el.id==='ti-'+tname));
  // Build SELECT query — auto-cast JSONB columns to ::text for usability
  const t=tables.find(x=>x.schema===schema&&x.table_name===tname);
  let selectCols='*';
  if(t&&t.columns){
    const cols=t.columns.map(c=>{
      const dt=(c.data_type||'').toLowerCase();
      if(dt==='jsonb'||dt==='json')return `"${c.name}"::text AS "${c.name}"`;
      return `"${c.name}"`;
    });
    if(cols.some(c=>c.includes('::text')))selectCols=cols.join(', ');
  }
  const qbox=document.getElementById('qbox');
  if(qbox)qbox.value=`SELECT ${selectCols}\nFROM ${tname}\nORDER BY 1 DESC\nLIMIT 20`;
  loadData();loadSchema(schema,tname);
}
function insertSnippet(sel){
  if(!sel.value)return;
  const ta=document.getElementById('qbox');
  const pos=ta.selectionStart,val=ta.value;
  ta.value=val.slice(0,pos)+' '+sel.value+val.slice(pos);
  ta.focus();ta.selectionStart=ta.selectionEnd=pos+sel.value.length+1;
  sel.value='';
}
async function loadData(){
  if(!active)return;
  const pnl=document.getElementById('panel-data');
  pnl.innerHTML='<div class="msg">loading…</div>';
  try{
    const d=await api(`/admin/db/tables/${active.schema}/${active.tname}/data?page=${page}&page_size=50`);
    const nav=`<div class="pg">
      <button class="btn" onclick="pg(-1)" ${page===1?'disabled':''}>← Prev</button>
      <span>Page ${d.page} · ${d.total_count.toLocaleString()} rows total</span>
      <button class="btn" onclick="pg(1)" ${!d.has_more?'disabled':''}>Next →</button>
    </div>`;
    pnl.innerHTML=`<div style="flex:1;overflow:auto">${grid(d.rows,d.columns)}</div>${nav}`;
  }catch(e){pnl.innerHTML=`<div class="msg err">${e.message}</div>`;}
}
function pg(dir){page=Math.max(1,page+dir);loadData();}
function loadSchema(schema,tname){
  const t=tables.find(x=>x.schema===schema&&x.table_name===tname);
  if(!t)return;
  const cols=t.columns.map(c=>{
    const dt=(c.data_type||'').toLowerCase();
    let typeBadge='';
    if(dt==='jsonb'||dt==='json'){
      typeBadge=`<span class="badge-type badge-jsonb">${dt.toUpperCase()}</span>`;
    } else if(dt.includes('text')||dt.includes('varchar')||dt.includes('char')){
      typeBadge=`<span class="badge-type badge-text">TEXT</span>`;
    } else if(dt.includes('int')||dt.includes('serial')||dt.includes('numeric')||dt.includes('float')){
      typeBadge=`<span class="badge-type badge-int">NUM</span>`;
    } else if(dt.includes('timestamp')||dt.includes('date')||dt.includes('time')){
      typeBadge=`<span class="badge-type badge-ts">TS</span>`;
    }
    const b=[
      c.is_primary_key?'<span class="badge pk">PK</span>':'',
      c.is_nullable?'<span class="badge nullable">NULL</span>':'',
      typeBadge,
    ].filter(Boolean).join('');
    return `<div class="sc-row"><span>${c.name}${b}</span><span style="color:#64748b">${c.data_type}</span></div>`;
  }).join('');
  const fks=t.foreign_keys.length?`<div class="sh" style="color:#a78bfa">FOREIGN KEYS</div>`+
    t.foreign_keys.map(f=>`<div class="sc-row"><span style="color:#a78bfa">${f.column}</span><span style="color:#475569;font-size:10px">→ ${f.references_table}.${f.references_column}</span></div>`).join(''):'';
  const ixs=t.indexes.length?`<div class="sh" style="color:#94a3b8">INDEXES</div>`+
    t.indexes.map(ix=>`<div class="sc-row"><span style="color:#94a3b8">${ix.name}</span><span style="color:#475569;font-size:10px">${ix.columns.join(', ')}${ix.is_unique?' · UNIQUE':''}</span></div>`).join(''):'';
  document.getElementById('panel-schema').innerHTML=
    `<div class="sh" style="color:#e2e8f0">${tname}</div>
     <div class="sh" style="color:#38bdf8">COLUMNS (${t.columns.length})</div>${cols}${fks}${ixs}`;
}
async function runQ(){
  const sql=document.getElementById('qbox').value.trim();if(!sql)return;
  const res=document.getElementById('qres'),meta=document.getElementById('qmeta');
  res.innerHTML='<div class="msg">running…</div>';meta.textContent='';
  try{
    const r=await fetch('/admin/db/query',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sql})});
    const d=await r.json();
    if(!r.ok||d.error){
      let html=`<div class="err-box">${escHtml(d.error||'Query failed')}</div>`;
      if(d.pgcode)html+=`<div style="padding:2px 12px 4px"><span class="pgcode">SQLSTATE: ${d.pgcode}</span></div>`;
      if(d.hint)html+=`<div class="hint">💡 ${escHtml(d.hint)}</div>`;
      res.innerHTML=html;
      return;
    }
    meta.textContent=`${d.row_count} rows · ${d.execution_ms}ms${d.truncated?' (truncated at 1000)':''}`;
    res.innerHTML=grid(d.rows,d.columns);
  }catch(e){res.innerHTML=`<div class="err-box">${escHtml(e.message)}</div>`;}
}
function escHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
loadTables();
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

async def handle_admin_ui(request: Request) -> HTMLResponse:
    return HTMLResponse(_HTML)


async def handle_list_tables(request: Request) -> JSONResponse:
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)
    schemas_in = "(" + ", ".join(f"'{s}'" for s in ALLOWED_SCHEMAS) + ")"
    try:
        with _db.get_cursor() as cur:
            cur.execute(f"""
                SELECT schemaname AS schema_name, relname AS table_name,
                       COALESCE(n_live_tup, 0) AS estimated_rows
                FROM pg_stat_user_tables WHERE schemaname IN {schemas_in}
                ORDER BY schemaname, relname
            """)
            tables_raw = cur.fetchall()

            cur.execute(f"""
                SELECT c.table_schema, c.table_name, c.column_name,
                       c.data_type, c.udt_name, c.is_nullable,
                       c.column_default, c.character_maximum_length,
                       CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END AS is_pk
                FROM information_schema.columns c
                LEFT JOIN (
                    SELECT kcu.table_schema, kcu.table_name, kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name=kcu.constraint_name
                        AND tc.table_schema=kcu.table_schema
                    WHERE tc.constraint_type='PRIMARY KEY'
                ) pk ON c.table_schema=pk.table_schema
                     AND c.table_name=pk.table_name
                     AND c.column_name=pk.column_name
                WHERE c.table_schema IN {schemas_in}
                ORDER BY c.table_schema, c.table_name, c.ordinal_position
            """)
            cols_raw = cur.fetchall()

            cur.execute(f"""
                SELECT tc.table_schema, tc.table_name, kcu.column_name,
                       ccu.table_schema AS ref_schema,
                       ccu.table_name   AS ref_table,
                       ccu.column_name  AS ref_column
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name=kcu.constraint_name AND tc.table_schema=kcu.table_schema
                JOIN information_schema.constraint_column_usage ccu
                    ON ccu.constraint_name=tc.constraint_name AND ccu.table_schema=tc.constraint_schema
                WHERE tc.constraint_type='FOREIGN KEY' AND tc.table_schema IN {schemas_in}
            """)
            fks_raw = cur.fetchall()

            cur.execute(f"""
                SELECT schemaname, tablename, indexname, indexdef FROM pg_indexes
                WHERE schemaname IN {schemas_in} ORDER BY schemaname, tablename, indexname
            """)
            idx_raw = cur.fetchall()

        # Build lookup maps
        col_map: dict = {}
        for c in cols_raw:
            key = (c["table_schema"], c["table_name"])
            dtype = c["udt_name"] if c["data_type"] == "USER-DEFINED" else c["data_type"]
            col_map.setdefault(key, []).append({
                "name": c["column_name"],
                "data_type": dtype,
                "is_nullable": c["is_nullable"] == "YES",
                "column_default": c["column_default"],
                "is_primary_key": bool(c["is_pk"]),
                "max_length": c["character_maximum_length"],
            })

        fk_map: dict = {}
        for f in fks_raw:
            key = (f["table_schema"], f["table_name"])
            fk_map.setdefault(key, []).append({
                "column": f["column_name"],
                "references_schema": f["ref_schema"],
                "references_table": f["ref_table"],
                "references_column": f["ref_column"],
            })

        idx_map: dict = {}
        for ix in idx_raw:
            key = (ix["schemaname"], ix["tablename"])
            is_unique = "UNIQUE" in (ix["indexdef"] or "").upper()
            col_match = re.search(r"\((.+?)\)", ix["indexdef"] or "")
            cols_list = [c.strip().strip('"') for c in col_match.group(1).split(",")] if col_match else []
            idx_map.setdefault(key, []).append({
                "name": ix["indexname"], "columns": cols_list, "is_unique": is_unique,
            })

        tables = [
            {
                "schema": t["schema_name"],
                "table_name": t["table_name"],
                "estimated_rows": t["estimated_rows"],
                "columns": col_map.get((t["schema_name"], t["table_name"]), []),
                "foreign_keys": fk_map.get((t["schema_name"], t["table_name"]), []),
                "indexes": idx_map.get((t["schema_name"], t["table_name"]), []),
            }
            for t in tables_raw
        ]
        return JSONResponse({"tables": tables, "total": len(tables)})

    except Exception as e:
        logger.error("list_tables error: %s", e)
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_get_table_data(request: Request) -> JSONResponse:
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    schema = request.path_params["schema"]
    table = request.path_params["table"]
    if not (_VALID_IDENT.match(schema) and _VALID_IDENT.match(table)):
        return JSONResponse({"error": "Invalid schema or table name"}, status_code=400)

    page = max(1, int(request.query_params.get("page", 1)))
    page_size = min(max(1, int(request.query_params.get("page_size", 25))), 100)
    order_by = request.query_params.get("order_by")
    order_dir = request.query_params.get("order_dir", "asc")

    try:
        with _db.get_cursor() as cur:
            cur.execute(
                "SELECT 1 FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
                (schema, table),
            )
            if not cur.fetchone():
                return JSONResponse({"error": f"Table {schema}.{table} not found"}, status_code=404)

            cur.execute(f'SELECT COUNT(*) AS cnt FROM "{schema}"."{table}"')
            total = cur.fetchone()["cnt"]

            order_clause = ""
            if order_by and _VALID_IDENT.match(order_by):
                direction = "DESC" if order_dir == "desc" else "ASC"
                order_clause = f'ORDER BY "{order_by}" {direction} NULLS LAST'

            offset = (page - 1) * page_size
            cur.execute(
                f'SELECT * FROM "{schema}"."{table}" {order_clause} LIMIT %s OFFSET %s',
                (page_size, offset),
            )
            rows_raw = cur.fetchall()

        columns = list(rows_raw[0].keys()) if rows_raw else []
        rows = _rows_to_json(rows_raw)
        return JSONResponse({
            "columns": columns, "rows": rows, "total_count": total,
            "page": page, "page_size": page_size,
            "has_more": (offset + page_size) < total,
        })

    except Exception as e:
        logger.error("get_table_data error: %s", e)
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_query(request: Request) -> JSONResponse:
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    sql = body.get("sql", "").strip()
    err = _validate_readonly(sql)
    if err:
        return JSONResponse({"error": err}, status_code=400)

    start = time.monotonic()
    try:
        with _db.get_cursor() as cur:
            cur.execute("SET LOCAL statement_timeout = '10s'")
            cur.execute(sql)
            rows_raw = cur.fetchall() or []

        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        columns = list(rows_raw[0].keys()) if rows_raw else []
        truncated = len(rows_raw) > MAX_QUERY_ROWS
        rows = _rows_to_json(rows_raw[:MAX_QUERY_ROWS])
        return JSONResponse({
            "columns": columns, "rows": rows,
            "row_count": len(rows_raw), "execution_ms": elapsed_ms, "truncated": truncated,
        })

    except Exception as e:
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        first_line = str(e).split("\n")[0]
        err_str = str(e).lower()

        # Extract PostgreSQL SQLSTATE code if available
        pgcode = getattr(e, "pgcode", None)

        # Match against known JSONB / type error patterns for helpful hints
        hint = None
        for pattern, msg in _JSONB_ERROR_PATTERNS:
            if pattern.lower() in err_str:
                hint = msg
                break

        response_body: dict = {
            "error": f"Query error ({elapsed_ms}ms): {first_line}",
            "elapsed_ms": elapsed_ms,
        }
        if pgcode:
            response_body["pgcode"] = pgcode
        if hint:
            response_body["hint"] = hint

        return JSONResponse(response_body, status_code=400)


# ---------------------------------------------------------------------------
# galdr task Visualizer
# ---------------------------------------------------------------------------

_GALDR_VIZ_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>galdr task Visualizer</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:monospace;background:#0f172a;color:#e2e8f0;font-size:13px;height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{background:#1e293b;padding:10px 16px;display:flex;align-items:center;gap:14px;border-bottom:1px solid #334155;flex-shrink:0}
header h1{font-size:14px;color:#a78bfa;font-weight:600}
#st{font-size:11px;color:#64748b}
.toolbar{display:flex;gap:8px;padding:6px 12px;background:#1e293b;border-bottom:1px solid #334155;flex-shrink:0;align-items:center;font-size:11px}
.btn{background:#1e40af;color:#e2e8f0;border:none;padding:3px 10px;border-radius:3px;cursor:pointer;font-size:11px;font-family:monospace}
.btn:hover{background:#1d4ed8}
.btn.active{background:#5b21b6}
.main{display:flex;flex:1;overflow:hidden}
#canvas{flex:1;overflow:auto;position:relative;padding:16px}
.sidebar{width:220px;background:#1e293b;border-left:1px solid #334155;overflow-y:auto;flex-shrink:0;font-size:11px}
.sidebar h2{padding:8px 12px;font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:.06em;border-bottom:1px solid #334155}
#detail{padding:10px 12px;white-space:pre-wrap;color:#94a3b8;font-size:10px}
/* DAG nodes */
.phase-lane{background:#0d1526;border:1px solid #1e3a5f;border-radius:6px;padding:10px 14px;margin-bottom:16px}
.phase-title{font-size:11px;font-weight:600;color:#38bdf8;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid #1e3a5f}
.nodes-grid{display:flex;flex-wrap:wrap;gap:8px}
.node{border-radius:4px;padding:6px 10px;cursor:pointer;border:1px solid transparent;min-width:140px;max-width:200px;font-size:11px;transition:border-color .15s;position:relative}
.node:hover{border-color:#64748b}
.node.selected{border-color:#a78bfa;box-shadow:0 0 0 1px #a78bfa}
.node-id{font-size:9px;color:#64748b;margin-bottom:2px}
.node-title{font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.node-badges{margin-top:3px;display:flex;gap:3px;flex-wrap:wrap}
.badge{font-size:8px;padding:1px 4px;border-radius:2px}
/* Status colors */
.s-completed{background:#052e16;border-color:#166534;color:#86efac}
.s-in-progress{background:#0c1a4a;border-color:#1e40af;color:#93c5fd}
.s-awaiting-verification{background:#1a0d4a;border-color:#5b21b6;color:#ddd6fe}
.s-pending{background:#0f172a;border-color:#334155;color:#94a3b8}
.s-failed{background:#2d0505;border-color:#7f1d1d;color:#fca5a5}
.s-ghost{background:#0c0f16;border-color:#1e293b;color:#475569;border-style:dashed}
.s-archived{background:#1a1209;border-color:#78350f;color:#fcd34d;opacity:.75}
/* Priority badges */
.p-critical{background:#7f1d1d;color:#fca5a5}
.p-high{background:#431407;color:#fdba74}
.p-medium{background:#0c2a1a;color:#86efac}
.p-low{background:#1e293b;color:#64748b}
.archived-badge{background:#78350f;color:#fcd34d}
/* Legend */
.legend{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-left:auto;font-size:10px}
.l-item{display:flex;align-items:center;gap:4px}
.l-dot{width:8px;height:8px;border-radius:2px}
</style>
</head>
<body>
<header>
  <h1>&#9670; galdr task Visualizer</h1>
  <span id="st">loading…</span>
  <div class="legend">
    <div class="l-item"><div class="l-dot s-completed"></div>done</div>
    <div class="l-item"><div class="l-dot s-in-progress"></div>active</div>
    <div class="l-item"><div class="l-dot s-awaiting-verification"></div>verify</div>
    <div class="l-item"><div class="l-dot s-pending"></div>pending</div>
    <div class="l-item"><div class="l-dot s-failed"></div>failed</div>
    <div class="l-item"><div class="l-dot s-archived" style="opacity:1"></div>archived</div>
    <div class="l-item"><div class="l-dot s-ghost"></div>ghost</div>
  </div>
</header>
<div class="toolbar">
  <button class="btn active" id="btn-phase" onclick="setView('phase')">Phase Swimlanes</button>
  <button class="btn" id="btn-flat" onclick="setView('flat')">Flat List</button>
  <button class="btn" onclick="location.reload()">↻ Refresh</button>
  <span style="margin-left:auto;color:#475569">Click a task node for details</span>
</div>
<div class="main">
  <div id="canvas"><div style="padding:24px;color:#334155">Loading task data…</div></div>
  <div class="sidebar">
    <h2>Task Detail</h2>
    <div id="detail">Select a node</div>
  </div>
</div>
<script>
'use strict';
let data=null,view='phase',selected=null;
async function load(){
  try{
    const r=await fetch('/admin/galdr/data');
    data=await r.json();
    document.getElementById('st').textContent=`${data.nodes.length} tasks · ${data.phases.length} phases`;
    render();
  }catch(e){
    document.getElementById('st').textContent='Error: '+e.message;
    document.getElementById('canvas').innerHTML=`<div style="padding:24px;color:#f87171">${e.message}</div>`;
  }
}
function setView(v){
  view=v;
  document.getElementById('btn-phase').classList.toggle('active',v==='phase');
  document.getElementById('btn-flat').classList.toggle('active',v==='flat');
  render();
}
function statusClass(s){
  const m={'completed':'s-completed','in-progress':'s-in-progress','in_progress':'s-in-progress',
    'awaiting-verification':'s-awaiting-verification','awaiting_verification':'s-awaiting-verification',
    'pending':'s-pending','failed':'s-failed','ghost':'s-ghost','archived':'s-archived'};
  return m[s]||'s-pending';
}
function statusEmoji(s){
  const m={completed:'✅','in-progress':'🔄','in_progress':'🔄','awaiting-verification':'🔍',
    'awaiting_verification':'🔍',pending:'📋',failed:'❌',ghost:'👻',archived:'📦'};
  return m[s]||'📋';
}
function nodeHtml(n){
  const sc=statusClass(n.status)+(n.archived?' s-archived':'');
  const pc=n.priority?`<span class="badge p-${n.priority}">${n.priority}</span>`:'';
  const br=n.blast_radius&&n.blast_radius!=='low'?`<span class="badge" style="background:#4c1d95;color:#ddd6fe">${n.blast_radius}</span>`:'';
  const ar=n.archived?`<span class="badge archived-badge">📦 archived</span>`:'';
  const sel=selected===n.id?' selected':'';
  return `<div class="node ${sc}${sel}" id="nd-${n.id}" onclick="selectNode('${n.id}')">
    <div class="node-id">#${n.id}</div>
    <div class="node-title" title="${escHtml(n.title)}">${statusEmoji(n.status)} ${escHtml(n.title||'').slice(0,40)}</div>
    <div class="node-badges">${pc}${br}${ar}</div>
  </div>`;
}
function render(){
  if(!data)return;
  const canvas=document.getElementById('canvas');
  if(view==='phase'){
    const byPhase={};
    data.nodes.forEach(n=>{
      const ph=n.phase!=null?n.phase:'?';
      if(!byPhase[ph])byPhase[ph]=[];
      byPhase[ph].push(n);
    });
    const phases=Object.keys(byPhase).sort((a,b)=>Number(a)-Number(b));
    canvas.innerHTML=phases.map(ph=>{
      const pname=(data.phases.find(p=>String(p.phase)===String(ph))||{}).name||'';
      const nodes=byPhase[ph].map(nodeHtml).join('');
      const total=byPhase[ph].length;
      const done=byPhase[ph].filter(n=>n.status==='completed'||n.archived).length;
      return `<div class="phase-lane">
        <div class="phase-title">Phase ${ph}: ${escHtml(pname)} (${done}/${total})</div>
        <div class="nodes-grid">${nodes}</div>
      </div>`;
    }).join('');
  } else {
    const nodes=data.nodes.map(nodeHtml).join('');
    canvas.innerHTML=`<div class="nodes-grid">${nodes}</div>`;
  }
}
async function selectNode(id){
  selected=id;
  render();
  const det=document.getElementById('detail');
  det.textContent='Loading…';
  try{
    const r=await fetch('/admin/galdr/task/'+encodeURIComponent(id));
    const d=await r.json();
    if(d.error){det.textContent=d.error;return;}
    let out=`ID: ${d.id}\nTitle: ${d.title}\nStatus: ${d.status}\nPriority: ${d.priority||'—'}\nPhase: ${d.phase||'—'}\nBlast: ${d.blast_radius||'—'}\nFile: ${d.file||'—'}\n`;
    if(d.dependencies&&d.dependencies.length)out+=`\nDeps: ${d.dependencies.join(', ')}`;
    if(d.subsystems&&d.subsystems.length)out+=`\nSubsystems: ${d.subsystems.join(', ')}`;
    if(d.project_context)out+=`\n\nContext:\n${d.project_context}`;
    det.textContent=out;
  }catch(e){det.textContent=e.message;}
}
function escHtml(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
load();
</script>
</body>
</html>"""


def _parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end < 0:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except Exception:
        return {}


async def handle_GALDR_ui(request: Request) -> HTMLResponse:
    """Serve the galdr task visualizer UI."""
    return HTMLResponse(_GALDR_VIZ_HTML)


async def handle_GALDR_data(request: Request) -> JSONResponse:
    """Return task graph data — nodes (tasks) and phases."""
    project_path = request.query_params.get("project", _GALDR_PROJECT_PATH)
    if not project_path:
        return JSONResponse({"error": "No project path configured. Set GALDR_PROJECT_PATH env var."}, status_code=400)

    GALDR_dir = os.path.join(project_path, ".galdr")
    if not os.path.isdir(GALDR_dir):
        return JSONResponse({"error": f".galdr/ not found at: {GALDR_dir}"}, status_code=404)

    nodes: list[dict] = []
    file_ids: set[str] = set()

    # Scan active task files
    active_files = _glob.glob(os.path.join(GALDR_dir, "tasks", "*.md"))
    # Scan archived task files in phases/phaseN/ subfolders
    archived_files = _glob.glob(os.path.join(GALDR_dir, "phases", "*", "*.md"))

    for fpath in active_files + archived_files:
        fname = os.path.basename(fpath)
        if not fname.startswith("task"):
            continue
        is_archived = "phases" + os.sep in fpath.replace(GALDR_dir, "")

        try:
            with open(fpath, encoding="utf-8") as f:
                meta = _parse_yaml_frontmatter(f.read())
        except Exception:
            meta = {}

        task_id = str(meta.get("id", fname.split("_")[0].replace("task", "")))
        file_ids.add(task_id)

        nodes.append({
            "id": task_id,
            "title": meta.get("title", fname),
            "status": meta.get("status", "pending"),
            "priority": meta.get("priority", ""),
            "phase": meta.get("phase"),
            "subsystems": meta.get("subsystems") or [],
            "dependencies": [str(d) for d in (meta.get("dependencies") or [])],
            "blast_radius": meta.get("blast_radius", "low"),
            "ai_safe": meta.get("ai_safe", True),
            "archived": is_archived,
            "file": os.path.relpath(fpath, project_path).replace("\\", "/"),
        })

    # Parse TASKS.md for ghost nodes (in TASKS.md but no task file)
    tasks_md = os.path.join(GALDR_dir, "TASKS.md")
    if os.path.isfile(tasks_md):
        with open(tasks_md, encoding="utf-8") as f:
            current_phase = None
            for line in f:
                pm = re.match(r"^#+\s+Phase\s+(\d+):", line)
                if pm:
                    current_phase = int(pm.group(1))
                    continue
                tm = re.match(r"^\|\s*\[.+?\]\s*\|\s*(\d+)\s*\|(.+?)\|", line)
                if tm:
                    tid = tm.group(1)
                    if tid not in file_ids:
                        nodes.append({
                            "id": tid,
                            "title": tm.group(2).strip()[:80],
                            "status": "ghost",
                            "priority": "",
                            "phase": current_phase,
                            "subsystems": [],
                            "dependencies": [],
                            "blast_radius": "low",
                            "ai_safe": True,
                            "archived": False,
                            "file": None,
                        })

    # Parse phase definition files
    phases: list[dict] = []
    for pfile in _glob.glob(os.path.join(GALDR_dir, "phases", "phase*.md")):
        # Skip if it's inside a phaseN/ subfolder (those are archived tasks)
        if os.path.dirname(pfile) != os.path.join(GALDR_dir, "phases"):
            continue
        try:
            with open(pfile, encoding="utf-8") as f:
                pmeta = _parse_yaml_frontmatter(f.read())
            if "phase" in pmeta:
                phases.append({
                    "phase": pmeta["phase"],
                    "name": pmeta.get("name", ""),
                    "status": pmeta.get("status", "planning"),
                })
        except Exception:
            continue

    return JSONResponse({"nodes": nodes, "phases": phases, "project": project_path})


async def handle_GALDR_task_detail(request: Request) -> JSONResponse:
    """Return task file metadata by task ID."""
    task_id = request.path_params["task_id"]
    project_path = request.query_params.get("project", _GALDR_PROJECT_PATH)
    if not project_path:
        return JSONResponse({"error": "No project path configured"}, status_code=400)

    GALDR_dir = os.path.join(project_path, ".galdr")

    # Search active then archived
    search_patterns = [
        os.path.join(GALDR_dir, "tasks", f"task{task_id}_*.md"),
        os.path.join(GALDR_dir, "phases", "*", f"task{task_id}_*.md"),
    ]
    found_file = None
    for pattern in search_patterns:
        matches = _glob.glob(pattern)
        if matches:
            found_file = matches[0]
            break

    if not found_file:
        return JSONResponse({"error": f"Task {task_id} not found"}, status_code=404)

    try:
        with open(found_file, encoding="utf-8") as f:
            content = f.read()
        meta = _parse_yaml_frontmatter(content)
        meta["file"] = os.path.relpath(found_file, project_path).replace("\\", "/")
        meta["id"] = task_id
        return JSONResponse(meta)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ---------------------------------------------------------------------------
# Project-scoped and User-scoped web routes
# ---------------------------------------------------------------------------

_PROJECT_TASKS_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><title>galdr — {project_id} Tasks</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:monospace;background:#0f172a;color:#e2e8f0;font-size:13px;padding:20px}
h1{color:#a78bfa;font-size:16px;margin-bottom:16px}
.meta{color:#64748b;font-size:11px;margin-bottom:20px}
.task{background:#1e293b;border:1px solid #334155;border-radius:4px;padding:10px 14px;margin-bottom:8px}
.task-id{color:#64748b;font-size:10px}.task-title{color:#e2e8f0;font-size:12px;margin:3px 0}
.task-status{font-size:10px;padding:1px 6px;border-radius:2px;display:inline-block}
.s-completed{background:#052e16;color:#86efac}.s-pending{background:#1e293b;color:#94a3b8;border:1px solid #334155}
.s-in-progress,.s-in_progress{background:#0c1a4a;color:#93c5fd}
.s-failed{background:#2d0505;color:#fca5a5}
.empty{color:#334155;padding:40px;text-align:center}
a{color:#38bdf8;text-decoration:none}a:hover{text-decoration:underline}
</style>
</head>
<body>
<h1>&#9670; {project_id}</h1>
<div class="meta">Task data from server · <a href="/admin/galdr">Full Visualizer</a></div>
<div id="tasks"><div class="empty">Loading…</div></div>
<script>
fetch('/projects/{project_id}/tasks/data').then(r=>r.json()).then(d=>{
  if(!d.tasks||!d.tasks.length){document.getElementById('tasks').innerHTML='<div class="empty">No tasks synced yet</div>';return;}
  document.getElementById('tasks').innerHTML=d.tasks.map(t=>{
    const sc='s-'+(t.status||'pending').replace(/ /g,'-');
    return `<div class="task"><span class="task-id">#${t.id||'?'}</span>
      <div class="task-title">${t.title||t.path||'Untitled'}</div>
      <span class="task-status ${sc}">${t.status||'pending'}</span></div>`;
  }).join('');
});
</script>
</body></html>"""

_USER_SESSIONS_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><title>galdr — User Sessions</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:monospace;background:#0f172a;color:#e2e8f0;font-size:13px;padding:20px}
h1{color:#38bdf8;font-size:16px;margin-bottom:16px}
.meta{color:#64748b;font-size:11px;margin-bottom:20px}
.session{background:#1e293b;border:1px solid #334155;border-radius:4px;padding:10px 14px;margin-bottom:8px}
.sess-id{color:#64748b;font-size:10px}.sess-summary{color:#94a3b8;font-size:11px;margin-top:4px}
.sess-meta{color:#475569;font-size:10px;margin-top:3px}
.badge{font-size:9px;padding:1px 5px;border-radius:2px;background:#0c4a6e;color:#7dd3fc;margin-left:4px}
.empty{color:#334155;padding:40px;text-align:center}
</style>
</head>
<body>
<h1>&#9670; User Sessions</h1>
<div class="meta">user_id: {user_id}</div>
<div id="sessions"><div class="empty">Loading…</div></div>
<script>
fetch('/users/{user_id}/sessions/data').then(r=>r.json()).then(d=>{
  if(!d.sessions||!d.sessions.length){document.getElementById('sessions').innerHTML='<div class="empty">No sessions found</div>';return;}
  document.getElementById('sessions').innerHTML=d.sessions.map(s=>{
    const ts=s.ended_at?s.ended_at.slice(0,16):'ongoing';
    return `<div class="session"><span class="sess-id">${s.conversation_id||'?'}</span>
      <span class="badge">${s.platform||'?'}</span>
      <span class="badge">${s.capture_tier||'?'}</span>
      <div class="sess-summary">${s.session_summary||'(no summary)'}</div>
      <div class="sess-meta">${ts} · ${s.turn_count||0} turns · ${s.project_name||''}</div></div>`;
  }).join('');
});
</script>
</body></html>"""


async def handle_project_tasks_ui(request: Request) -> HTMLResponse:
    pid = request.path_params["project_id"]
    html = _PROJECT_TASKS_HTML.replace("{project_id}", pid)
    return HTMLResponse(html)


async def handle_project_tasks_data(request: Request) -> JSONResponse:
    """Return task data for a project from project_files or filesystem."""
    pid = request.path_params["project_id"]

    tasks: list[dict] = []

    # Try project_files table first (WebSocket-synced data)
    if _db:
        try:
            with _db.get_cursor() as cur:
                cur.execute(
                    """
                    SELECT file_path, content, version, updated_at
                    FROM project_files
                    WHERE project_id = %s AND file_type = 'galdr'
                      AND file_path LIKE 'tasks/%%'
                    ORDER BY file_path
                    """,
                    (pid,),
                )
                for row in cur.fetchall():
                    meta = _parse_yaml_frontmatter(row["content"] or "")
                    tasks.append({
                        "id": meta.get("id", ""),
                        "title": meta.get("title", row["file_path"]),
                        "status": meta.get("status", "pending"),
                        "priority": meta.get("priority", ""),
                        "phase": meta.get("phase"),
                        "path": row["file_path"],
                        "version": row["version"],
                    })
        except Exception as e:
            logger.warning("project_tasks_data DB error: %s", e)

    # Fallback to filesystem if no synced data
    if not tasks and _GALDR_PROJECT_PATH:
        galdr_dir = os.path.join(_GALDR_PROJECT_PATH, ".galdr", "tasks")
        if os.path.isdir(galdr_dir):
            for fname in sorted(os.listdir(galdr_dir)):
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(galdr_dir, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        meta = _parse_yaml_frontmatter(f.read())
                    tasks.append({
                        "id": meta.get("id", ""),
                        "title": meta.get("title", fname),
                        "status": meta.get("status", "pending"),
                        "priority": meta.get("priority", ""),
                        "phase": meta.get("phase"),
                        "path": f"tasks/{fname}",
                    })
                except Exception:
                    continue

    return JSONResponse({"project_id": pid, "tasks": tasks, "total": len(tasks)})


async def handle_project_status(request: Request) -> JSONResponse:
    """Return project dashboard: phase progress, task counts."""
    pid = request.path_params["project_id"]
    status_counts: dict[str, int] = {}
    phase_counts: dict[str, dict] = {}

    if _db:
        try:
            with _db.get_cursor() as cur:
                cur.execute(
                    """
                    SELECT file_path, content
                    FROM project_files
                    WHERE project_id = %s AND file_type = 'galdr'
                      AND file_path LIKE 'tasks/%%'
                    """,
                    (pid,),
                )
                for row in cur.fetchall():
                    meta = _parse_yaml_frontmatter(row["content"] or "")
                    st = meta.get("status", "pending")
                    ph = str(meta.get("phase", "?"))
                    status_counts[st] = status_counts.get(st, 0) + 1
                    if ph not in phase_counts:
                        phase_counts[ph] = {"total": 0, "completed": 0}
                    phase_counts[ph]["total"] += 1
                    if st == "completed":
                        phase_counts[ph]["completed"] += 1
        except Exception as e:
            logger.warning("project_status DB error: %s", e)

    return JSONResponse({
        "project_id": pid,
        "status_counts": status_counts,
        "phase_progress": phase_counts,
    })


async def handle_user_sessions_ui(request: Request) -> HTMLResponse:
    uid = request.path_params["user_id"]
    html = _USER_SESSIONS_HTML.replace("{user_id}", uid)
    return HTMLResponse(html)


async def handle_user_sessions_data(request: Request) -> JSONResponse:
    """Return session list for a user."""
    uid = request.path_params["user_id"]
    limit = min(max(1, int(request.query_params.get("limit", 50))), 200)

    sessions: list[dict] = []
    if _db:
        try:
            with _db.get_cursor() as cur:
                cur.execute(
                    """
                    SELECT s.conversation_id, s.platform, s.capture_tier,
                           s.status, s.session_summary, s.ended_at,
                           p.project_id, p.display_name AS project_name,
                           COUNT(t.id) AS turn_count
                    FROM agent_sessions s
                    JOIN agent_projects p ON p.id = s.project_id
                    LEFT JOIN agent_turns t ON t.session_id = s.id
                    WHERE s.user_id = %s
                    GROUP BY s.id, p.project_id, p.display_name
                    ORDER BY s.ended_at DESC NULLS LAST
                    LIMIT %s
                    """,
                    (uid, limit),
                )
                for row in cur.fetchall():
                    sessions.append({
                        "conversation_id": row["conversation_id"],
                        "platform": row["platform"],
                        "capture_tier": row["capture_tier"],
                        "status": row["status"],
                        "session_summary": row["session_summary"],
                        "ended_at": str(row["ended_at"]) if row["ended_at"] else None,
                        "project_id": row["project_id"],
                        "project_name": row["project_name"],
                        "turn_count": row["turn_count"],
                    })
        except Exception as e:
            logger.warning("user_sessions_data error: %s", e)

    return JSONResponse({"user_id": uid, "sessions": sessions, "total": len(sessions)})


async def handle_user_memory_data(request: Request) -> JSONResponse:
    """Return captured insights for a user."""
    uid = request.path_params["user_id"]
    limit = min(max(1, int(request.query_params.get("limit", 50))), 200)

    captures: list[dict] = []
    if _db:
        try:
            with _db.get_cursor() as cur:
                cur.execute(
                    """
                    SELECT c.summary, c.category, c.scope, c.topic,
                           c.created_at, p.project_id, p.display_name
                    FROM agent_memory_captures c
                    JOIN agent_projects p ON p.id = c.project_id
                    WHERE c.user_id = %s
                    ORDER BY c.created_at DESC
                    LIMIT %s
                    """,
                    (uid, limit),
                )
                for row in cur.fetchall():
                    captures.append({
                        "summary": row["summary"],
                        "category": row["category"],
                        "scope": row["scope"],
                        "topic": row["topic"],
                        "created_at": str(row["created_at"]) if row["created_at"] else None,
                        "project_id": row["project_id"],
                        "project_name": row["display_name"],
                    })
        except Exception as e:
            logger.warning("user_memory_data error: %s", e)

    return JSONResponse({"user_id": uid, "captures": captures, "total": len(captures)})


# ---------------------------------------------------------------------------
# Route list — imported by server.py
# ---------------------------------------------------------------------------
ADMIN_ROUTES = [
    Route("/admin/db",                                    handle_admin_ui,          methods=["GET"]),
    Route("/admin/db/tables",                             handle_list_tables,       methods=["GET"]),
    Route("/admin/db/tables/{schema}/{table}/data",       handle_get_table_data,    methods=["GET"]),
    Route("/admin/db/query",                              handle_query,             methods=["POST"]),
    Route("/admin/galdr",                                 handle_GALDR_ui,          methods=["GET"]),
    Route("/admin/galdr/data",                            handle_GALDR_data,        methods=["GET"]),
    Route("/admin/galdr/task/{task_id}",                  handle_GALDR_task_detail, methods=["GET"]),
    # Project-scoped routes
    Route("/projects/{project_id}/tasks",                 handle_project_tasks_ui,  methods=["GET"]),
    Route("/projects/{project_id}/tasks/data",            handle_project_tasks_data, methods=["GET"]),
    Route("/projects/{project_id}/status",                handle_project_status,    methods=["GET"]),
    # User-scoped routes
    Route("/users/{user_id}/sessions",                    handle_user_sessions_ui,  methods=["GET"]),
    Route("/users/{user_id}/sessions/data",               handle_user_sessions_data, methods=["GET"]),
    Route("/users/{user_id}/memory",                      handle_user_memory_data,  methods=["GET"]),
]
