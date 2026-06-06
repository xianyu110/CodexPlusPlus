# Codex++

<p align="center">
  <img src="docs/images/codex-plus-plus.png" alt="Codex++ 图标" width="160">
</p>

<p align="center">
  中文 | <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img alt="Release" src="https://img.shields.io/github/v/release/xianyu110/CodexPlusPlus">
  <img alt="Stars" src="https://img.shields.io/github/stars/xianyu110/CodexPlusPlus">
  <img alt="License" src="https://img.shields.io/github/license/xianyu110/CodexPlusPlus">
  <img alt="Rust" src="https://img.shields.io/badge/rust-1.85%2B-orange">
  <img alt="Tauri" src="https://img.shields.io/badge/tauri-2.x-24C8DB">
</p>

Codex++ 是面向 Codex App 的外部增强启动器和管理工具：不修改原始安装文件，通过 Chromium DevTools Protocol 注入增强脚本。

## 快速使用

从 [GitHub Releases](https://github.com/xianyu110/CodexPlusPlus/releases) 下载最新版安装包：

- Windows：`CodexPlusPlus-*-windows-x64-setup.exe`
- macOS Intel：`CodexPlusPlus-*-macos-x64.dmg`
- macOS Apple Silicon：`CodexPlusPlus-*-macos-arm64.dmg`

安装后会有两个入口：

- `Codex++`：静默启动入口，不显示管理界面，只负责启动 Codex 并注入增强功能。
- `Codex++ 管理工具`：Tauri 控制面板，用于启动、检查、修复、更新、管理增强功能、中转注入和用户脚本。

Windows 安装包会创建桌面和开始菜单快捷方式。macOS DMG 会安装 `/Applications/Codex++.app` 和 `/Applications/Codex++ 管理工具.app`。

## 功能亮点

- Rust 后端和静默 launcher：启动时不依赖 Python 运行时。
- Tauri + React 管理工具：集中启动、诊断、修复、更新和管理增强功能。
- 插件市场解锁：API Key 模式下扩展插件市场请求，尽量显示完整插件列表。
- 插件入口解锁：API Key 模式下显示并启用插件入口。
- 特殊插件强制安装：解除 App unavailable / 应用不可用导致的前端安装禁用。
- 会话删除：悬停显示删除按钮，删除前确认并支持撤销。
- Markdown 导出：按本地 rollout 导出带时间戳的会话 Markdown。
- 会话项目移动：把会话移动到普通对话或其他本地项目。
- 对话 Timeline：右侧显示用户提问时间线，悬停摘要，点击跳转。
- 用户脚本独立管理：可在启动时注入自定义脚本。
- 中转注入：支持多个中转配置，写入 `CodexPlusPlus` provider，并可切回官方 ChatGPT 登录态。
- Provider 同步：切换 model_provider 或供应商时不丢历史会话。
- Zed 打开入口：识别远程 SSH 上下文后，可从 Codex 直接打开对应文件到 Zed Remote Development。
- Upstream worktree 创建：可从 `upstream/<base-branch>` 创建新 worktree，创建前自动 fetch 远端分支。
- GitHub Release 自动更新，管理工具和静默启动器都会检测可用更新。
- Windows 单实例、无黑框启动、管理员权限清单、系统桌面路径识别。
- macOS x64/arm64 分架构 DMG，静默入口隐藏 Dock 图标。

## 痛点与解决

API Key 登录模式下，Codex 原生插件入口会提示需要登录 ChatGPT，导致插件功能无法正常使用：

![API Key 模式下插件入口不可用](docs/images/pain-plugin-disabled.png)

Codex 原生会话列表只有归档入口，没有真正的删除按钮：

![原生会话列表缺少删除能力](docs/images/pain-no-delete-button.png)

Codex++ 启动后会解锁插件入口，并在会话列表悬停时显示删除按钮：

![Codex++ 解锁插件入口并添加删除按钮](docs/images/solution-plugin-and-delete.png)

顶部菜单栏会出现 `Codex++`，可以查看后端状态并打开设置面板：

![Codex++ 后端状态指示灯](docs/images/backend-status-indicator.png)
![Codex++ 设置面板](docs/images/settings-panel.png)

## 工作方式

1. 外部启动 Codex App，并附加 CDP 参数：
   - `--remote-debugging-port=9229`
   - `--remote-allow-origins=http://127.0.0.1:9229`
2. 启动本地 helper 服务，用于健康检查、设置、导出、移动、删除等操作。
3. 通过 CDP 注入 `renderer-inject.js`。
4. 渲染端通过 CDP bridge 调用本地服务；默认不开放 HTTP 删除/撤销入口，避免本机其他页面误触发。
5. 启动时继承现有代理环境变量；若未设置，会自动探测常见本地代理端口帮助加载 GitHub 资源。

这种方式不会修改 Codex 的 `app.asar`，也不需要往 Codex 安装目录写 DLL。

## 中转注入

中转注入适合已经在 Codex/ChatGPT 中完成官方账号登录，同时希望把模型请求转到自定义兼容 API 的场景。

在管理工具的“中转注入”页面：

1. 确认已经检测到 ChatGPT 登录状态。
2. 添加一个或多个中转配置，填写 Base URL 和 Key。
3. 选择当前配置并应用中转注入。
4. 启动 `Codex++`。

Codex++ 会在 `~/.codex/config.toml` 中写入类似配置：

```toml
model_provider = "CodexPlusPlus"

[model_providers.CodexPlusPlus]
name = "CodexPlusPlus"
wire_api = "responses"
requires_openai_auth = true
base_url = "https://example.com/v1"
experimental_bearer_token = "sk-..."
```

如果需要回到官方登录态，在“中转注入”页面点击清除 API 模式即可移除 `OPENAI_API_KEY` 相关配置并切回官方 ChatGPT 登录模式。

## Provider 同步

启用 `Provider 同步` 后，Codex++ 会在启动前同步本地会话 metadata，让切换供应商后历史会话仍能在 Desktop 和 `/resume` 中显示。

同步范围包括 rollout 文件、SQLite 线程记录和项目路径缓存；只修复会话可见性 metadata，不改写消息内容。遇到文件锁或 SQLite 忙碌时会跳过并继续启动。

## 常用命令

```bash
# 前端检查
cd apps/codex-plus-manager
npm install
npm run check
npm run vite:build

# Rust 检查
cd ../..
cargo fmt --check
cargo test
cargo build --release
```

## 数据位置

- Codex 配置：`~/.codex/config.toml`
- Codex 登录状态：`~/.codex/auth.json`
- Codex 本地数据库：`~/.codex/state_5.sqlite`
- Codex++ 状态与日志：`~/.codex-session-delete/`
- Provider 同步备份：`~/.codex/backups_state/provider-sync`

## 常见问题

### Codex++ 菜单没出现

确认是从 `Codex++` 入口启动，而不是原版 Codex。也可以打开管理工具的“诊断”和“日志”页面查看注入状态。

### 插件内显示后端连不上

先在浏览器或 PowerShell 里测试：

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:57321/backend/status -Body "{}" -ContentType "application/json"
```

如果接口正常，但插件仍显示超时，通常是 Codex 页面里的 CDP bridge 或脚本缓存问题。重启 Codex++，或在管理工具里查看日志中的 `renderer.script_loaded`、`bridge.request`、`bridge.response`。

### Upstream worktree 和 Codex 原生创建有什么区别

Codex++ 的 Upstream worktree 功能等价于先更新远端分支，再执行：

```bash
git worktree add -b <new-branch> <worktree-path> upstream/<base-branch>
```

这样新 worktree 从最新的远端跟踪分支开始，而不是从当前会话所在的本地 HEAD 开始。

### macOS 提示无法打开或已损坏

当前安装包未签名/未公证时，macOS Gatekeeper 可能拦截，出现“已损坏，无法打开”的提示：

![macOS 提示 Codex++ 管理工具已损坏](docs/images/macos-damaged-warning.png)

如果遇到该提示，可以在终端执行下面两条命令，解除苹果系统的安全隔离限制：

```bash
sudo xattr -rd com.apple.quarantine /Applications/Codex++\ 管理工具.app
sudo xattr -rd com.apple.quarantine /Applications/Codex++.app
```

执行后重新打开 `Codex++` 或 `Codex++ 管理工具` 即可。

### macOS Intel 能用吗

可以。Release 会分别提供 `macos-x64.dmg` 和 `macos-arm64.dmg`。Intel Mac 下载 x64 包，Apple Silicon 下载 arm64 包。

## 开发

```bash
# 前端检查
cd apps/codex-plus-manager
npm install
npm run check
npm run vite:build

# Rust 检查
cd ../..
cargo fmt --check
cargo test
cargo build --release
```

主要结构：

```text
apps/
  codex-plus-launcher/          静默启动入口
  codex-plus-manager/           Tauri 管理工具
assets/inject/
  renderer-inject.js            注入到 Codex 渲染端的增强脚本
crates/
  codex-plus-core/              启动、注入、配置、更新、安装、桥接等核心逻辑
  codex-plus-data/              会话数据、导出、Provider 同步
scripts/installer/
  windows/CodexPlusPlus.nsi     Windows NSIS 安装包
  macos/package-dmg.sh          macOS DMG 打包
```

## Codex国内使用

https://codex.chatgpt-plus.top/login

https://codex2.chatgpt-plus.top/login
<img width="260" height="260" alt="image" src="https://github.com/user-attachments/assets/cf6ecb47-9a32-4410-adc0-f3b489e4c6d6" />

## 说明

Codex++ 是外部增强工具，不修改 Codex App 原始文件。Codex App 更新后，如果页面结构变化，可能需要更新注入脚本。
