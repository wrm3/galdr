# galdr Desktop

Tauri 2.0 wrapper for the galdr web UI served by the Docker container.

## What This Is

A lightweight native desktop shell that loads the galdr web interface from `http://localhost:8092`. When the Docker container isn't running, a fallback page with auto-retry logic is shown instead.

## Prerequisites

- **Rust** — [rustup.rs](https://rustup.rs)
- **Node.js** >= 18
- **Tauri CLI** — installed via `npm install` (devDependency)
- **galdr Docker container** running on port 8092

### Windows-specific

The MSVC C++ build tools and WebView2 are required. See [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/).

## Development

```bash
cd desktop
npm install
npm run dev
```

This opens the app pointing at the live Docker server (`http://localhost:8092/static/index.html`). Hot-reload applies to the Rust backend; frontend changes come from the Docker container.

## Production Build

```bash
npm run build
```

Produces a platform-specific installer in `src-tauri/target/release/bundle/`.

## Architecture

```
┌─────────────────────────────┐
│  Tauri WebView (native)     │
│  ┌───────────────────────┐  │
│  │ galdr web UI           │  │
│  │ (served by Docker)     │  │
│  └───────────────────────┘  │
│                             │
│  Rust backend               │
│  • check_server_health()    │
│  • trigger_heartbeat()      │
│  • System tray integration  │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  galdr Docker container     │
│  localhost:8092             │
└─────────────────────────────┘
```

## Tray Icon

Right-click the system tray icon for:

| Action | Description |
|--------|-------------|
| **Show galdr** | Bring the window to front |
| **Check Health** | Navigate to health view |
| **Quit** | Exit the application |

Left-click the tray icon to show/focus the window.

## Tauri Commands (Rust → JS bridge)

| Command | Description |
|---------|-------------|
| `check_server_health` | GET `/api/status` — returns server health JSON |
| `trigger_heartbeat` | POST `/api/heartbeat/trigger` — fires a named heartbeat routine |

Call from the frontend via `@tauri-apps/api`:

```javascript
import { invoke } from '@tauri-apps/api/core';

const health = await invoke('check_server_health');
const result = await invoke('trigger_heartbeat', { routine: 'cleanup' });
```

## Future

- **Mobile builds** — Tauri 2.0 supports iOS and Android targets
- **Auto-update** — Tauri's built-in updater for desktop releases
- **Deep linking** — `galdr://` protocol handler for cross-app integration
