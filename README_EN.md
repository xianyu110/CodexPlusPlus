# Codex++

<p align="center">
  <img src="docs/images/codex-plus-plus.png" alt="Codex++ icon" width="160">
</p>

<p align="center">
  <a href="README.md">中文</a> | English
</p>

<p align="center">
  <img alt="Release" src="https://img.shields.io/github/v/release/BigPizzaV3/CodexPlusPlus">
  <img alt="Stars" src="https://img.shields.io/github/stars/BigPizzaV3/CodexPlusPlus">
  <img alt="License" src="https://img.shields.io/github/license/BigPizzaV3/CodexPlusPlus">
  <img alt="Rust" src="https://img.shields.io/badge/rust-1.85%2B-orange">
  <img alt="Tauri" src="https://img.shields.io/badge/tauri-2.x-24C8DB">
</p>

Codex++ is an external enhancement launcher and manager for the Codex App: it does not modify the original installation files, and injects enhancement scripts through the Chromium DevTools Protocol.

## Quick Start

Download the latest installer from [GitHub Releases](https://github.com/BigPizzaV3/CodexPlusPlus/releases):

- Windows: `CodexPlusPlus-*-windows-x64-setup.exe`
- macOS Intel: `CodexPlusPlus-*-macos-x64.dmg`
- macOS Apple Silicon: `CodexPlusPlus-*-macos-arm64.dmg`

After installation, there are two entries:

- `Codex++`: silent launcher that starts Codex and injects enhancements without showing the manager UI.
- `Codex++ Manager`: Tauri control panel for launch, diagnostics, repair, updates, enhancement settings, relay injection, and user scripts.

The Windows installer creates desktop and Start Menu shortcuts. The macOS DMG installs `/Applications/Codex++.app` and `/Applications/Codex++ 管理工具.app`.

## Highlights

- Rust backend and silent launcher: no Python runtime required at startup.
- Tauri + React manager: launch, diagnose, repair, update, and manage enhancements in one place.
- Plugin marketplace unlock: expand plugin marketplace requests in API Key mode to show a more complete plugin list.
- Plugin entry unlock: show and enable the plugin entry in API Key mode.
- Forced special plugin installation: bypass frontend disablement caused by App unavailable states.
- Session deletion: show a delete button on hover, confirm before deletion, and support undo.
- Markdown export: export local rollouts as timestamped conversation Markdown.
- Session project move: move conversations to regular chats or other local projects.
- Conversation Timeline: show user question markers on the right, preview summaries on hover, and jump on click.
- User script management: inject custom scripts at launch.
- Relay injection: manage multiple relay profiles, write a `CodexPlusPlus` provider, and switch back to official ChatGPT auth.
- Provider Sync: switch `model_provider` or providers without losing historical conversations.
- Zed open entry: open remote SSH file references directly in Zed Remote Development.
- Upstream worktree creation: create a new worktree from `upstream/<base-branch>` after fetching the latest remote branch.
- GitHub Release auto-update checks for both the manager and silent launcher.
- Windows single instance, no console window, administrator manifest, and desktop path detection.
- macOS x64/arm64 DMGs, with the silent entry hidden from the Dock.

## Pain Points and Fixes

In API Key login mode, the native Codex plugin entry prompts for ChatGPT login, preventing plugin features from working properly:

![Plugin entry unavailable in API Key mode](docs/images/pain-plugin-disabled.png)

The native Codex session list only has an archive entry and no real delete button:

![Native session list lacks delete action](docs/images/pain-no-delete-button.png)

After launching through Codex++, the plugin entry is unlocked and a delete button appears when hovering over a session:

![Codex++ unlocks plugin entry and adds delete button](docs/images/solution-plugin-and-delete.png)

The top bar shows `Codex++`, where you can view backend status and open the settings panel:

![Codex++ backend status indicator](docs/images/backend-status-indicator.png)
![Codex++ settings panel](docs/images/settings-panel.png)

## How It Works

1. Externally launches the Codex App with CDP flags:
   - `--remote-debugging-port=9229`
   - `--remote-allow-origins=http://127.0.0.1:9229`
2. Starts a local helper service for health checks, settings, export, move, delete, and other operations.
3. Injects `renderer-inject.js` through CDP.
4. The renderer calls local services through the CDP bridge. Delete/undo HTTP routes are not exposed by default, preventing accidental triggers from other local pages.
5. Inherits existing proxy environment variables on launch. If none are set, Codex++ automatically detects common local proxy ports to help load GitHub resources.

This approach does not modify Codex `app.asar` and does not write DLL files into the Codex installation directory.

## Relay Injection

Relay injection is for users who have completed official Codex/ChatGPT login and want model requests to go through a custom compatible API.

In the manager's Relay Injection page:

1. Confirm ChatGPT login has been detected.
2. Add one or more relay profiles with Base URL and Key.
3. Select the current profile and apply relay injection.
4. Launch `Codex++`.

Codex++ writes a config like this to `~/.codex/config.toml`:

```toml
model_provider = "CodexPlusPlus"

[model_providers.CodexPlusPlus]
name = "CodexPlusPlus"
wire_api = "responses"
requires_openai_auth = true
base_url = "https://example.com/v1"
experimental_bearer_token = "sk-..."
```

To return to official auth, click clear API mode in the Relay Injection page.

## Provider Sync

When `Provider Sync` is enabled, Codex++ synchronizes local session metadata before launch so historical conversations remain visible in Desktop and `/resume` after switching providers.

The sync covers rollout files, SQLite thread records, and project path caches. It only fixes visibility-related metadata and does not rewrite message content. If a file is locked or SQLite is busy, Codex++ skips it and continues launching.

## Common Commands

```bash
# Frontend checks
cd apps/codex-plus-manager
npm install
npm run check
npm run vite:build

# Rust checks
cd ../..
cargo fmt --check
cargo test
cargo build --release
```

## Data Locations

- Codex configuration: `~/.codex/config.toml`
- Codex auth state: `~/.codex/auth.json`
- Codex local database: `~/.codex/state_5.sqlite`
- Codex++ state and logs: `~/.codex-session-delete/`
- Provider Sync backups: `~/.codex/backups_state/provider-sync`

## FAQ

### The Codex++ menu does not appear

Make sure you launched from the `Codex++` entry instead of the original Codex. You can also open the manager's Diagnostics and Logs pages to inspect injection status.

### The plugin says the backend is disconnected

Test the backend first:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:57321/backend/status -Body "{}" -ContentType "application/json"
```

If the endpoint works but the plugin still times out, it is usually a Codex page CDP bridge or script cache issue. Restart Codex++, or check manager logs for `renderer.script_loaded`, `bridge.request`, and `bridge.response`.

### How is Upstream worktree different from native Codex worktree creation?

Codex++ first updates the remote branch, then runs:

```bash
git worktree add -b <new-branch> <worktree-path> upstream/<base-branch>
```

This creates the new worktree from the latest remote tracking branch instead of the local HEAD used by the current conversation.

### macOS says the app cannot be opened or is damaged

If the package is unsigned or not notarized, macOS Gatekeeper may block it:

![macOS damaged warning](docs/images/macos-damaged-warning.png)

Run these commands to remove the quarantine attribute:

```bash
sudo xattr -rd com.apple.quarantine /Applications/Codex++\ 管理工具.app
sudo xattr -rd com.apple.quarantine /Applications/Codex++.app
```

Then reopen `Codex++` or `Codex++ 管理工具`.

### Does macOS Intel work?

Yes. Releases provide both `macos-x64.dmg` and `macos-arm64.dmg`. Intel Mac users should download x64; Apple Silicon users should download arm64.

## Development

```bash
# Frontend checks
cd apps/codex-plus-manager
npm install
npm run check
npm run vite:build

# Rust checks
cd ../..
cargo fmt --check
cargo test
cargo build --release
```

Main structure:

```text
apps/
  codex-plus-launcher/          Silent launcher entry
  codex-plus-manager/           Tauri manager
assets/inject/
  renderer-inject.js            Enhancement script injected into the Codex renderer
crates/
  codex-plus-core/              Launch, injection, config, update, install, bridge logic
  codex-plus-data/              Session data, export, Provider Sync
scripts/installer/
  windows/CodexPlusPlus.nsi     Windows NSIS installer
  macos/package-dmg.sh          macOS DMG packaging
```

## Codex Usage in China

https://codex.chatgpt-plus.top/login

<img width="520" height="520" alt="image" src="https://github.com/user-attachments/assets/272ce57d-3750-482e-9e9e-026bac4a0743" />

## Notes

Codex++ is an external enhancement tool and does not modify original Codex App files. If a future Codex App update changes page structure, the injection script may need updates.
