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

Codex++ 是面向 Codex App 的外部增强启动器和管理工具。它不修改 Codex App 原始安装文件，而是通过外部 launcher 启动 Codex，并使用 Chromium DevTools Protocol 注入增强脚本。

## 快速使用

从 [GitHub Releases](https://github.com/xianyu110/CodexPlusPlus/releases) 下载最新版安装包：

- Windows：`CodexPlusPlus-*-windows-x64-setup.exe`
- macOS Intel：`CodexPlusPlus-*-macos-x64.dmg`
- macOS Apple Silicon：`CodexPlusPlus-*-macos-arm64.dmg`

安装后会有两个入口：

- `Codex++`：静默启动入口，不显示管理界面，只负责启动 Codex 并注入增强功能。
- `Codex++ 管理工具`：Tauri 控制面板，用于启动、检查、修复、更新、配置中转注入、管理增强功能和用户脚本。

Windows 安装包会创建桌面和开始菜单快捷方式。macOS DMG 会安装 `/Applications/Codex++.app` 和 `/Applications/Codex++ 管理工具.app`。

## 国内官网入口

国内用户可通过直连入口访问：

- [国内官网入口（直连）](https://codex.maynor1024.live/login)

## 主要功能

- Rust 后端和静默 launcher，启动时不依赖额外运行时。
- Tauri + React 管理工具，支持深色/浅色切换。
- 外部 CDP 注入，不改 `app.asar`，不向 Codex 安装目录写入 DLL。
- 中转注入模式：支持多个中转配置，写入 `CodexPlusPlus` provider，并可切回官方 ChatGPT 登录态。
- 传统增强模式：插件市场解锁、会话删除、Markdown 导出、项目移动等。
- 粘贴修复：从 Word 等富文本来源粘贴到 Codex composer 时只保留纯文本，避免被识别为图片/文件附件。默认关闭，启用后需重启 Codex 才生效。
  - **使用提示**：管理工具里勾选后需点「保存增强设置」按钮才会写盘，然后重启 Codex++ 才会生效。
- Stepwise 下一步建议：在 Codex 对话页显示可拖动的 Stepwise 浮层，基于当前用户意图和最新助手回复生成后续操作建议；可配置独立 Base URL、API Key、模型、建议数量和是否点击后直接发送。
- 用户脚本独立管理，可在启动时注入自定义脚本。
- Provider 同步：启动前同步本地会话 metadata，切换供应商后旧会话仍可见。
- Zed 打开入口：识别远程 SSH 上下文后，可从 Codex 直接打开对应文件到 Zed Remote Development。
- 按模型粒度配置上下文窗口：「模型列表」分为左右两列，左侧填模型名，右侧填上下文窗口（如 `1M`、`200K` 或 `1000000`）；Codex++ 自动生成 `model_catalog_json` 并注入 `config.toml`，切换模型即生效。右侧留空则使用 Codex 默认长度。
- Upstream worktree 创建：可从 `upstream/<base-branch>` 创建新 worktree，创建前自动 fetch 远端分支，降低从陈旧本地 HEAD 派生导致的冲突风险。
- GitHub Release 自动更新，管理工具和静默启动器都会检测可用更新。
- Windows 单实例、无黑框启动、管理员权限清单、系统桌面路径识别。
- macOS x64/arm64 分架构 DMG，静默入口隐藏 Dock 图标。

## 痛点与解决

API Key 登录模式下，Codex 原生插件市场会提示需要登录 ChatGPT，导致插件功能无法正常使用：

![API Key 模式下插件市场不可用](docs/images/pain-plugin-disabled.png)

Codex 原生会话列表只有归档入口，没有真正的删除按钮：

![原生会话列表缺少删除能力](docs/images/pain-no-delete-button.png)

Codex++ 启动后会解锁插件市场能力，并在会话列表悬停时显示删除按钮：

![Codex++ 解锁插件市场并添加删除按钮](docs/images/solution-plugin-and-delete.png)

顶部菜单栏会出现 `Codex++`，可以查看后端状态并打开设置面板：

![Codex++ 后端状态指示灯](docs/images/backend-status-indicator.png)
![Codex++ 设置面板](docs/images/settings-panel.png)

## 中转注入

中转注入适合已经在 Codex/ChatGPT 中完成官方账号登录，同时希望把模型请求转到自定义兼容 API 的场景。

这种混合模式的边界是：

- 官方 ChatGPT/Codex 登录态继续负责 Codex App 的账号能力和插件入口。
- 中转配置只接管模型请求使用的 Base URL、Key 和模型名称。
- 兼容 API 供应商不需要固定为某一家；只要上游协议和 Codex 配置匹配即可。
- 清除 API 模式后应能回到官方登录态，继续使用官方账号和插件。

应用中转注入前建议先做一次最小检查：

1. 先确认 Codex 已检测到 ChatGPT 登录状态，插件入口可用。
2. 确认自定义 Base URL 可访问，并且支持所选上游协议（例如 Responses 兼容接口）。
3. 用目标 Key 做一次最小认证测试，例如模型列表或很短的消息请求。
4. 只记录 Key 是否存在和认证结果，不要把真实 Key 写入日志、截图或 issue。
5. 确认 `~/.codex/config.toml` 已有备份，便于清除 API 模式后回滚。

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

## 增强功能

增强功能在管理工具中统一开关。默认开启增强注入；关闭后不会注入 Codex++ 菜单和脚本。

如果启用中转注入模式，插件市场解锁不再需要，界面会提示“中转注入模式下无需开启”。会话删除、导出、移动、粘贴修复和用户脚本等增强仍可继续使用。

## 自动更新与安装包

Codex++ 通过 GitHub Release 发布安装包。Windows 会生成 NSIS 安装程序，macOS 会生成 Intel x64 和 Apple Silicon arm64 两个 DMG。

管理工具的“关于”页可以检查并启动更新。静默启动器发现新版本时会拉起管理工具并进入更新提示。

## 数据位置

- Codex 配置：`~/.codex/config.toml`
- Codex 登录状态：`~/.codex/auth.json`
- Codex 本地数据库：优先读取 `~/.codex/sqlite/*.db`，旧版回退到 `~/.codex/state_5.sqlite`
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

这样新 worktree 从最新的远端跟踪分支开始，而不是从当前会话所在的本地 HEAD 开始。如果 Codex++ 无法安全识别当前 Codex 版本的原生 worktree 创建表单，请从 Codex++ 菜单中手动填写仓库路径、分支名、worktree 路径、remote 和 base branch。

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

## 说明

Codex++ 是外部增强工具，不修改 Codex App 原始文件。Codex App 更新后，如果页面结构变化，可能需要更新注入脚本。
