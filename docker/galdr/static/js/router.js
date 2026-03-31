/* galdr hash-based SPA router */

const ROUTES = {
  dashboard:  "pages/dashboard.html",
  project:    "pages/project-dashboard.html",
  tasks:      "pages/task-visualizer.html",
  heartbeat:  "pages/heartbeat.html",
  schedules:  "pages/schedules.html",
  health:     "pages/system-health.html",
  db:         "pages/db-explorer.html",
  vault:      "pages/vault-browser.html",
  search:     "pages/knowledge-search.html",
  sessions:   "pages/sessions.html",
};

const DEFAULT_ROUTE = "dashboard";

const pageContent = () => document.getElementById("page-content");

function currentRoute() {
  const hash = location.hash.replace(/^#\/?/, "").split("?")[0];
  return hash || DEFAULT_ROUTE;
}

function setActiveNav(route) {
  document.querySelectorAll(".nav-item").forEach((el) => {
    el.classList.toggle("active", el.dataset.route === route);
  });
}

async function loadPage(route) {
  const container = pageContent();
  if (!container) return;

  const file = ROUTES[route];
  if (!file) {
    container.innerHTML =
      '<div class="empty-state">' +
      '<span class="icon">404</span>' +
      `<span>Page <b>#${escHtml(route)}</b> not found</span>` +
      '<span class="text-muted text-xs">Check the sidebar for valid routes</span>' +
      "</div>";
    return;
  }

  container.innerHTML =
    '<div class="empty-state"><div class="spinner"></div><span class="text-muted">Loading...</span></div>';

  try {
    const res = await fetch(file);
    if (!res.ok) throw new Error(`${res.status}`);
    container.innerHTML = await res.text();

    container.querySelectorAll("script").forEach((old) => {
      const s = document.createElement("script");
      if (old.src) s.src = old.src;
      else s.textContent = old.textContent;
      old.replaceWith(s);
    });

    if (typeof window.pageInit === "function") {
      window.pageInit();
      window.pageInit = undefined;
    }
  } catch (err) {
    container.innerHTML =
      '<div class="empty-state">' +
      '<span class="icon">⚠</span>' +
      `<span>Failed to load <b>${escHtml(route)}</b></span>` +
      `<span class="text-muted text-xs">${escHtml(err.message)}</span>` +
      "</div>";
  }
}

function navigate(route) {
  location.hash = "#" + route;
}

function onHashChange() {
  const route = currentRoute();
  setActiveNav(route);
  loadPage(route);
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".nav-item[data-route]").forEach((el) => {
    el.addEventListener("click", () => navigate(el.dataset.route));
  });

  window.addEventListener("hashchange", onHashChange);
  onHashChange();
});
