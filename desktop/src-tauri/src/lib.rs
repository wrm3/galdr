use tauri::{
    Manager,
    menu::{Menu, MenuItem},
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
    Url,
};

const SERVER_URL: &str = "http://localhost:8092";
const UI_URL: &str = "http://localhost:8092/static/index.html";
const STATUS_URL: &str = "http://localhost:8092/api/status";

#[tauri::command]
async fn check_server_health() -> Result<serde_json::Value, String> {
    let client = reqwest::Client::new();
    match client
        .get(STATUS_URL)
        .timeout(std::time::Duration::from_secs(5))
        .send()
        .await
    {
        Ok(resp) => {
            if resp.status().is_success() {
                resp.json::<serde_json::Value>()
                    .await
                    .map_err(|e| e.to_string())
            } else {
                Err(format!("Server returned {}", resp.status()))
            }
        }
        Err(e) => Err(e.to_string()),
    }
}

#[tauri::command]
async fn trigger_heartbeat(routine: String) -> Result<serde_json::Value, String> {
    let client = reqwest::Client::new();
    let body = serde_json::json!({ "routine": routine });
    match client
        .post(format!("{}/api/heartbeat/trigger", SERVER_URL))
        .json(&body)
        .timeout(std::time::Duration::from_secs(10))
        .send()
        .await
    {
        Ok(resp) => resp
            .json::<serde_json::Value>()
            .await
            .map_err(|e| e.to_string()),
        Err(e) => Err(e.to_string()),
    }
}

/// Spawn a background task that polls the server and navigates the
/// WebView to the Docker-served UI once it responds.
fn spawn_server_poller(app_handle: tauri::AppHandle) {
    tauri::async_runtime::spawn(async move {
        let client = reqwest::Client::new();
        for _ in 0..20 {
            tokio::time::sleep(std::time::Duration::from_secs(2)).await;
            if let Ok(resp) = client
                .get(STATUS_URL)
                .timeout(std::time::Duration::from_secs(3))
                .send()
                .await
            {
                if resp.status().is_success() {
                    if let Some(w) = app_handle.get_webview_window("main") {
                        let url = UI_URL.parse::<Url>().unwrap();
                        let _ = w.navigate(url);
                    }
                    return;
                }
            }
        }
    });
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            check_server_health,
            trigger_heartbeat,
        ])
        .setup(|app| {
            let show_i = MenuItem::with_id(app, "show", "Show galdr", true, None::<&str>)?;
            let health_i =
                MenuItem::with_id(app, "health", "Check Health", true, None::<&str>)?;
            let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&show_i, &health_i, &quit_i])?;

            let _tray = TrayIconBuilder::new()
                .tooltip("galdr")
                .menu(&menu)
                .on_menu_event(|app, event| match event.id.as_ref() {
                    "show" => {
                        if let Some(w) = app.get_webview_window("main") {
                            let _ = w.show();
                            let _ = w.set_focus();
                        }
                    }
                    "health" => {
                        if let Some(w) = app.get_webview_window("main") {
                            let _ = w.eval("window.location.hash = '#health'");
                        }
                    }
                    "quit" => {
                        app.exit(0);
                    }
                    _ => {}
                })
                .on_tray_icon_event(|tray, event| {
                    if let TrayIconEvent::Click {
                        button: MouseButton::Left,
                        button_state: MouseButtonState::Up,
                        ..
                    } = event
                    {
                        let app = tray.app_handle();
                        if let Some(w) = app.get_webview_window("main") {
                            let _ = w.show();
                            let _ = w.set_focus();
                        }
                    }
                })
                .build(app)?;

            // Poll the Docker server from Rust and navigate when ready
            spawn_server_poller(app.handle().clone());

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running galdr desktop");
}
