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
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue">
</p>

Codex++ is an external enhancement launcher for the Codex App: it does not modify the original installation files, and injects enhancement scripts through the Chromium DevTools Protocol.

## Quick Start

On Windows, double-click `setup.bat` in the project root and choose:

```text
[1] Install Codex++
```

After installation, double-click the desktop `Codex++.lnk` shortcut to launch.

Command-line install/launch:

```bash
python -m pip install -e .
python -m codex_session_delete setup
python -m codex_session_delete launch
```

macOS:

```bash
python -m codex_session_delete setup
```

After installation, `/Applications/Codex++.app` will be created.



## Highlights

- Top-bar `Codex++` menu: manage enhancement features in one place.
- Plugin entry unlock: show and enable the plugin entry in API Key mode.
- Forced special plugin installation: bypass frontend disablement caused by App unavailable states.
- Session deletion: show a delete button on hover, confirm before deletion, and support undo.
- Markdown export: export local rollouts as timestamped conversation Markdown.
- Session project move: move conversations to regular chats or other local projects.
- Conversation Timeline: show user question markers on the right, preview summaries on hover, and jump on click.
- Provider Sync: switch `model_provider` or providers without losing historical conversations.
- Windows shortcuts, uninstall entries, optional watcher takeover, and GitHub Release updates.
- macOS `/Applications/Codex++.app` generation.

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

## Provider Sync

When `Provider Sync` is enabled, Codex++ synchronizes local session metadata before launch so historical conversations remain visible in Desktop and `/resume` after switching providers.

The sync covers rollout files, SQLite thread records, and project path caches. It only fixes visibility-related metadata and does not rewrite message content. If a file is locked or SQLite is busy, Codex++ skips it and continues launching.

## Common Commands

```bash
# Install dependencies
python -m pip install -e .

# Launch
python -m codex_session_delete launch

# Install shortcut / app bundle
python -m codex_session_delete setup

# Remove
python -m codex_session_delete remove

# Also delete logs and backups
python -m codex_session_delete remove --remove-data

# Check for updates / update
python -m codex_session_delete check-update
python -m codex_session_delete update

# Windows watcher takeover
python -m codex_session_delete watch-install
python -m codex_session_delete watch-remove
python -m codex_session_delete watch-disable
python -m codex_session_delete watch-enable
```

Specify the Codex installation directory directly:

```bash
python -m codex_session_delete launch \
  --app-dir "C:/Program Files/WindowsApps/OpenAI.Codex_xxx/app" \
  --debug-port 9229 \
  --helper-port 57321
```

## Data Locations

- Codex local database: `~/.codex/state_5.sqlite`
- Delete backups: `~/.codex-session-delete/backups`
- Provider Sync backups: `~/.codex/backups_state/provider-sync`
- Launch failure logs: `~/.codex-session-delete/launcher.log`
- Watcher logs: `%USERPROFILE%\.codex-session-delete\watcher.log`

## FAQ

### Double-clicking Codex++ does nothing

Check the log: `%USERPROFILE%\.codex-session-delete\launcher.log`

Common causes: Codex App is not installed or its path changed, port 9229 is already in use, or Python is unavailable.

### The Codex++ menu does not appear

Make sure you launched from the `Codex++` shortcut instead of the original Codex. You can also check whether Codex has `--remote-debugging-port=9229`.

### Skill recommendations fail to load

If you see `git fetch failed` or cannot connect to GitHub, your network usually cannot reach GitHub directly. Codex++ inherits proxy environment variables and also auto-detects common local proxy ports. You can specify one manually:

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"
python -m codex_session_delete launch
```

### Old conversations disappear after switching providers

Open the `Codex++` settings panel, enable `Provider Sync`, then restart Codex++.

## Development

```bash
python -m pip install -e .[test]
python -m pytest -q
```

Main structure:

```text
codex_session_delete/
  cli.py                 CLI entry point
  launcher.py            Launches Codex and injects scripts
  cdp.py                 CDP communication and bridge
  helper_server.py       Local helper service
  storage_adapter.py     Local SQLite delete/undo
  provider_sync.py       Provider Sync
  settings_store.py      Codex++ backend settings
  windows_installer.py   Windows shortcuts and uninstall entries
  macos_installer.py     macOS app bundle setup
  watcher.py             Windows watcher (optional)
  inject/renderer-inject.js

tests/                   Automated tests
```



## Codex Usage in China

https://codex.chatgpt-plus.top/login

<img width="520" height="520" alt="image" src="https://github.com/user-attachments/assets/272ce57d-3750-482e-9e9e-026bac4a0743" />



## Notes

Codex++ is an external enhancement tool and does not modify original Codex App files. If a future Codex App update changes page structure, the injection script may need updates.

