/* galdr shared utilities */

async function api(path, opts = {}) {
  const url = path.startsWith("http") ? path : path;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...opts.headers },
    ...opts,
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`${res.status} ${res.statusText}: ${body}`);
  }
  return res.json();
}

function escHtml(str) {
  if (str == null) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function fmt(value) {
  if (value === null || value === undefined)
    return '<span class="null">NULL</span>';
  if (value === true)
    return '<span class="text-green">true</span>';
  if (value === false)
    return '<span class="text-red">false</span>';
  if (typeof value === "object") {
    const s = JSON.stringify(value);
    return escHtml(s.length > 100 ? s.slice(0, 97) + "..." : s);
  }
  const s = String(value);
  return escHtml(s.length > 140 ? s.slice(0, 137) + "..." : s);
}

function grid(rows, cols) {
  if (!rows || rows.length === 0) {
    return '<div class="empty-state"><span class="icon">∅</span><span>No data</span></div>';
  }
  const headers = cols || Object.keys(rows[0]);
  let html = "<table><thead><tr>";
  for (const col of headers) html += `<th>${escHtml(col)}</th>`;
  html += "</tr></thead><tbody>";
  for (const row of rows) {
    html += "<tr>";
    for (const col of headers) html += `<td>${fmt(row[col])}</td>`;
    html += "</tr>";
  }
  html += "</tbody></table>";
  return html;
}

function timeAgo(dateStr) {
  if (!dateStr) return "";
  const now = Date.now();
  const then = new Date(dateStr).getTime();
  if (isNaN(then)) return dateStr;
  const diff = now - then;
  const sec = Math.floor(diff / 1000);
  if (sec < 60) return "just now";
  const min = Math.floor(sec / 60);
  if (min < 60) return `${min}m ago`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr}h ago`;
  const days = Math.floor(hr / 24);
  if (days < 30) return `${days}d ago`;
  const months = Math.floor(days / 30);
  return `${months}mo ago`;
}

function formatCron(expr) {
  if (!expr) return "";
  const parts = expr.trim().split(/\s+/);
  if (parts.length < 5) return expr;
  const [min, hour, dom, mon, dow] = parts;

  if (min.startsWith("*/"))
    return `Every ${min.slice(2)} minutes`;
  if (hour.startsWith("*/"))
    return `Every ${hour.slice(2)} hours`;

  const hh = hour.padStart(2, "0");
  const mm = min.padStart(2, "0");
  const time = `${hh}:${mm}`;

  const ampm = (h, m) => {
    const hi = parseInt(h, 10);
    const suffix = hi >= 12 ? "PM" : "AM";
    const h12 = hi === 0 ? 12 : hi > 12 ? hi - 12 : hi;
    return `${h12}:${m.padStart(2, "0")} ${suffix}`;
  };

  if (dom === "*" && mon === "*" && dow === "*")
    return `Daily at ${ampm(hour, min)}`;
  if (dom === "*" && mon === "*" && dow === "1-5")
    return `Weekdays at ${ampm(hour, min)}`;
  if (dom === "*" && mon === "*" && dow === "0")
    return `Sundays at ${ampm(hour, min)}`;
  if (dom === "1" && mon === "*" && dow === "*")
    return `Monthly (1st) at ${ampm(hour, min)}`;

  return `${expr} (${time})`;
}

function healthColor(score) {
  if (score == null) return "var(--text-muted)";
  if (score >= 70) return "var(--accent-green)";
  if (score >= 40) return "var(--accent-amber)";
  return "var(--accent-red)";
}

function healthLabel(score) {
  if (score == null) return "Unknown";
  if (score >= 70) return "Healthy";
  if (score >= 40) return "Degraded";
  return "Critical";
}

function statusBadge(status) {
  if (!status) return '<span class="badge badge-muted">—</span>';
  const s = String(status).toLowerCase();
  const map = {
    healthy: "success", running: "success", completed: "success", active: "success",
    warning: "warning", degraded: "warning", pending: "warning", paused: "warning",
    critical: "danger", failed: "danger", error: "danger", offline: "danger",
  };
  const cls = map[s] || "muted";
  return `<span class="badge badge-${cls}">${escHtml(status)}</span>`;
}

function debounce(fn, ms = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), ms);
  };
}
