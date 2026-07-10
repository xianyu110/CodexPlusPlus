# Codex++

<p align="center">
  <img src="docs/images/codex-plus-plus.png" alt="Codex++ icon" width="160">
</p>

<p align="center">
  <a href="README.md">中文</a> | English
</p>

<p align="center">
  <img alt="Release" src="https://img.shields.io/github/v/release/xianyu110/CodexPlusPlus">
  <img alt="Stars" src="https://img.shields.io/github/stars/xianyu110/CodexPlusPlus">
  <img alt="License" src="https://img.shields.io/github/license/xianyu110/CodexPlusPlus">
  <img alt="Rust" src="https://img.shields.io/badge/rust-1.85%2B-orange">
  <img alt="Tauri" src="https://img.shields.io/badge/tauri-2.x-24C8DB">
</p>

Codex++ is an external enhancement launcher and manager for the Codex App. It does not modify the original Codex installation. Instead, it starts Codex externally and injects enhancements through the Chromium DevTools Protocol.

## Quick Start

Download the latest installer from [GitHub Releases](https://github.com/xianyu110/CodexPlusPlus/releases):

- Windows: `CodexPlusPlus-*-windows-x64-setup.exe`
- macOS Intel: `CodexPlusPlus-*-macos-x64.dmg`
- macOS Apple Silicon: `CodexPlusPlus-*-macos-arm64.dmg`

After installation, two entry points are available:

- `Codex++`: a silent launcher. It does not show the manager UI and only starts Codex with Codex++ injection.
- `Codex++ Manager`: a Tauri control panel for launch, diagnostics, repair, updates, relay injection, enhancements, and user scripts.

The Windows installer creates desktop and Start Menu shortcuts. The macOS DMG installs `/Applications/Codex++.app` and `/Applications/Codex++ 管理工具.app`.

## China Official Website

Users in China can use the direct login entry:

- [China official website (direct)](https://codex.maynor1024.live/login)

## Highlights

- Rust backend and silent launcher with no extra runtime requirement.
- Tauri + React manager with dark/light theme support.
- External CDP injection. No `app.asar` patching and no DLL writes into the Codex installation.
- Relay injection mode with multiple relay profiles, `CodexPlusPlus` provider configuration, and a one-click switch back to official ChatGPT login mode.
- Traditional enhancement mode with plugin marketplace unlock, session delete, Markdown export, project move, and more.
- Paste fix: when pasting from Word or other rich-text sources into the Codex composer, only keep the plain text so Codex does not treat the clipboard content as an image or file attachment. Off by default; requires a Codex relaunch to take effect.
  - **Usage note**: after toggling in the manager, click the "保存增强设置" / "Save enhancement settings" button to persist, then restart Codex++ for the change to take effect.
- Independent user script management with startup injection.
- Provider Sync to keep historical sessions visible after switching providers.
- Zed open entry detects remote SSH context and opens the matching remote file in Zed Remote Development from Codex.
- Per-model context window configuration: the "Model list" is split into two columns, model name on the left and context window (e.g. `1M`, `200K`, or `1000000`) on the right. Codex++ auto-generates `model_catalog_json` and injects it into `config.toml`; the matching window is applied when you switch models. Leave the window empty to use Codex's default length.
- Upstream worktree creation: create new worktrees from `upstream/<base-branch>` after fetching the remote branch, reducing conflicts caused by stale local HEAD state.
- GitHub Release updates. Both the manager and silent launcher can detect available updates.
- Windows single instance, no console window, administrator manifest, and system Desktop path detection.
- Separate macOS x64 and arm64 DMGs. The silent launcher hides its Dock icon.

## Relay Injection

Relay injection is for users who are already logged in with an official ChatGPT account in Codex/ChatGPT and want model requests to go through a custom compatible API.

The boundary of this hybrid mode is:

- The official ChatGPT/Codex login state still owns Codex App account features and the plugin entry.
- The relay profile only controls the Base URL, key, and model names used for model requests.
- The compatible API provider is not tied to any specific vendor; it only needs to match the selected upstream protocol and Codex configuration.
- Clearing API mode should return Codex to the official login mode so the official account and plugins keep working.

Before applying relay injection, run a minimal preflight:

1. Make sure Codex has detected the ChatGPT login state and the plugin entry is available.
2. Confirm the custom Base URL is reachable and supports the selected upstream protocol, such as a Responses-compatible endpoint.
3. Test the target key with the smallest useful auth probe, such as a model-list request or a short message request.
4. Only record whether the key exists and whether auth passed. Do not paste real keys into logs, screenshots, or issues.
5. Make sure `~/.codex/config.toml` has a backup so clearing API mode can safely roll back.

In the manager's Relay Injection page:

1. Make sure ChatGPT login status is detected.
2. Add one or more relay profiles with Base URL and Key.
3. Select the active profile and apply relay injection.
4. Launch `Codex++`.

Codex++ writes configuration similar to this into `~/.codex/config.toml`:

```toml
model_provider = "CodexPlusPlus"

[model_providers.CodexPlusPlus]
name = "CodexPlusPlus"
wire_api = "responses"
requires_openai_auth = true
base_url = "https://example.com/v1"
experimental_bearer_token = "sk-..."
```

To return to the official login mode, use the clear API mode button in the Relay Injection page. This removes `OPENAI_API_KEY` related configuration and switches Codex back to official ChatGPT authentication.

## Enhancements

Enhancements are controlled in the manager. Enhancement injection is enabled by default. When disabled, Codex++ will not inject its menu or scripts.

When relay injection mode is active, plugin marketplace unlock is unnecessary, and the UI will say so. Other enhancements, including session delete, export, move, paste fix, and user scripts, can still be used.

## Updates and Packages

Codex++ publishes installers through GitHub Releases. Windows builds an NSIS installer, while macOS builds separate Intel x64 and Apple Silicon arm64 DMGs.

The manager's About page can check and start updates. When the silent launcher finds a new version, it opens the manager directly on the update prompt.

## Data Locations

- Codex config: `~/.codex/config.toml`
- Codex auth state: `~/.codex/auth.json`
- Codex local database: prefers `~/.codex/sqlite/*.db`, falls back to legacy `~/.codex/state_5.sqlite`
- Codex++ state and logs: `~/.codex-session-delete/`
- Provider Sync backups: `~/.codex/backups_state/provider-sync`

## FAQ

### The Codex++ menu does not appear

Make sure Codex was launched from the `Codex++` entry instead of the original Codex entry. You can also inspect the Diagnostics and Logs pages in the manager.

### The plugin says the backend is disconnected

First test the helper endpoint:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:57321/backend/status -Body "{}" -ContentType "application/json"
```

If the endpoint works but the plugin still times out, it is usually a Codex page CDP bridge or script cache issue. Restart Codex++, or check manager logs for `renderer.script_loaded`, `bridge.request`, and `bridge.response`.

### How is Upstream worktree different from Codex native creation?

Codex++ updates the remote branch first, then creates the worktree as if you ran:

```bash
git worktree add -b <new-branch> <worktree-path> upstream/<base-branch>
```

The new worktree starts from the fresh remote tracking branch instead of the local HEAD used by the current session. If Codex++ cannot safely recognize the current Codex version's native worktree form, use the Codex++ menu entry and enter the repository path, branch name, worktree path, remote, and base branch manually.

### macOS says the app cannot be opened or is damaged

Unsigned and unnotarized builds may be blocked by Gatekeeper. Allow the app in System Settings -> Privacy & Security. For formal distribution, configure Apple Developer ID signing and notarization.

### Does it support Intel Macs?

Yes. Releases provide both `macos-x64.dmg` and `macos-arm64.dmg`. Intel Macs should use the x64 package, while Apple Silicon Macs should use the arm64 package.

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

Project structure:

```text
apps/
  codex-plus-launcher/          Silent launcher
  codex-plus-manager/           Tauri manager
assets/inject/
  renderer-inject.js            Enhancement script injected into Codex
crates/
  codex-plus-core/              Launch, injection, config, update, install, bridge
  codex-plus-data/              Session data, export, Provider Sync
scripts/installer/
  windows/CodexPlusPlus.nsi     Windows NSIS installer
  macos/package-dmg.sh          macOS DMG packager
```

## Notes

Codex++ is an external enhancement tool and does not modify original Codex App files. If a future Codex App update changes page structure, the injection script may need updates.
