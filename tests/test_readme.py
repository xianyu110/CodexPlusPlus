from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_chinese_readme_includes_core_branding_and_badges():
    text = read("README.md")

    assert "# Codex++" in text
    assert '<img src="docs/images/codex-plus-plus.png"' in text
    assert 'width="160"' in text
    assert '<a href="README_EN.md">English</a>' in text
    assert "[English](README_EN.md)" not in text
    assert "img.shields.io/github/v/release/BigPizzaV3/CodexPlusPlus" in text
    assert "img.shields.io/github/stars/BigPizzaV3/CodexPlusPlus" in text
    assert "img.shields.io/github/license/BigPizzaV3/CodexPlusPlus" in text


def test_chinese_readme_documents_current_core_sections():
    text = read("README.md")

    for heading in [
        "## 快速使用",
        "## 功能亮点",
        "## 痛点与解决",
        "## 工作方式",
        "## Provider 同步",
        "## 常用命令",
        "## 数据位置",
        "## 常见问题",
        "## 开发",
        "## Codex国内使用",
        "## 说明",
    ]:
        assert heading in text


def test_chinese_readme_documents_provider_sync_as_no_session_loss():
    text = read("README.md")

    assert "Provider 同步" in text
    assert "切换 model_provider" in text
    assert "不丢历史会话" in text
    assert "Desktop 和 `/resume`" in text


def test_chinese_readme_includes_feature_screenshots():
    text = read("README.md")

    for image in [
        "docs/images/pain-plugin-disabled.png",
        "docs/images/pain-no-delete-button.png",
        "docs/images/solution-plugin-and-delete.png",
        "docs/images/backend-status-indicator.png",
        "docs/images/settings-panel.png",
    ]:
        assert image in text
        assert Path(image).exists()


def test_english_readme_matches_chinese_structure_and_core_content():
    text = read("README_EN.md")

    assert "# Codex++" in text
    assert '<a href="README.md">中文</a>' in text
    assert "[中文](README.md)" not in text
    assert "Provider Sync" in text
    assert "switch `model_provider` or providers without losing historical conversations" in text

    for heading in [
        "## Quick Start",
        "## Highlights",
        "## Pain Points and Fixes",
        "## How It Works",
        "## Provider Sync",
        "## Common Commands",
        "## Data Locations",
        "## FAQ",
        "## Development",
        "## Codex Usage in China",
        "## Notes",
    ]:
        assert heading in text


def test_english_readme_keeps_image_and_domestic_usage_links_synced():
    text = read("README_EN.md")

    assert "docs/images/pain-plugin-disabled.png" in text
    assert "docs/images/pain-no-delete-button.png" in text
    assert "docs/images/solution-plugin-and-delete.png" in text
    assert "docs/images/backend-status-indicator.png" in text
    assert "docs/images/settings-panel.png" in text
    assert "https://codex.chatgpt-plus.top/login" in text
    assert "https://github.com/user-attachments/assets/272ce57d-3750-482e-9e9e-026bac4a0743" in text

