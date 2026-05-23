import json

import pytest

from codex_session_delete.relay_config import apply_relay_config, clear_relay_config, relay_status


def test_apply_relay_config_writes_codex_provider(tmp_path):
    codex_home = tmp_path / ".codex"
    (codex_home / "config.toml").parent.mkdir(parents=True)
    (codex_home / "config.toml").write_text(
        'model = "gpt-5"\n\n[profiles.default]\nmodel = "gpt-5"\n',
        encoding="utf-8",
    )

    result = apply_relay_config("https://relay.example.com/v1/", "sk-test", codex_home)

    contents = (codex_home / "config.toml").read_text(encoding="utf-8")
    assert result.configured is True
    assert result.to_dict()["status"] == "ok"
    assert 'model_provider = "CodexPlusPlus"' in contents
    assert "[model_providers.CodexPlusPlus]" in contents
    assert 'wire_api = "responses"' in contents
    assert "requires_openai_auth = true" in contents
    assert 'base_url = "https://relay.example.com/v1"' in contents
    assert 'experimental_bearer_token = "sk-test"' in contents
    assert contents.index("[model_providers.CodexPlusPlus]") < contents.index("[profiles.default]")


def test_apply_relay_config_replaces_legacy_provider(tmp_path):
    codex_home = tmp_path / ".codex"
    codex_home.mkdir()
    (codex_home / "config.toml").write_text(
        'model_provider = "CodexPP"\n\n[model_providers.CodexPP]\nbase_url = "https://old.example.com/v1"\n',
        encoding="utf-8",
    )

    apply_relay_config("https://new.example.com/v1", "sk-new", codex_home)

    contents = (codex_home / "config.toml").read_text(encoding="utf-8")
    assert "CodexPP" not in contents
    assert 'base_url = "https://new.example.com/v1"' in contents


def test_relay_status_detects_chatgpt_auth_without_printing_token(tmp_path):
    codex_home = tmp_path / ".codex"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text(
        json.dumps(
            {
                "auth_mode": "chatgpt",
                "email": "user@example.com",
                "tokens": {"access_token": "secret-token"},
            }
        ),
        encoding="utf-8",
    )
    apply_relay_config("https://relay.example.com/v1", "sk-test", codex_home)

    status = relay_status(codex_home)

    assert status.authenticated is True
    assert status.account_label == "user@example.com"
    assert status.configured is True
    assert "secret-token" not in str(status.to_dict())


def test_clear_relay_config_removes_provider_and_auth_api_key(tmp_path):
    codex_home = tmp_path / ".codex"
    codex_home.mkdir()
    apply_relay_config("https://relay.example.com/v1", "sk-test", codex_home)
    (codex_home / "auth.json").write_text(
        json.dumps({"OPENAI_API_KEY": "sk-test", "auth_mode": "chatgpt", "tokens": {"access_token": "token"}}),
        encoding="utf-8",
    )

    result = clear_relay_config(codex_home)

    contents = (codex_home / "config.toml").read_text(encoding="utf-8")
    auth = json.loads((codex_home / "auth.json").read_text(encoding="utf-8"))
    assert result.configured is False
    assert result.to_dict()["status"] == "ok"
    assert result.message == "中转配置已清理"
    assert "CodexPlusPlus" not in contents
    assert "model_provider" not in contents
    assert "OPENAI_API_KEY" not in auth
    assert auth["auth_mode"] == "chatgpt"


def test_clear_relay_config_preserves_non_codex_plus_model_provider(tmp_path):
    codex_home = tmp_path / ".codex"
    codex_home.mkdir()
    (codex_home / "config.toml").write_text(
        '\n'.join(
            [
                'model_provider = "OtherProvider"',
                "",
                "[model_providers.OtherProvider]",
                'base_url = "https://other.example.com/v1"',
                "",
                "[model_providers.CodexPlusPlus]",
                'base_url = "https://relay.example.com/v1"',
                'experimental_bearer_token = "sk-test"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    clear_relay_config(codex_home)

    contents = (codex_home / "config.toml").read_text(encoding="utf-8")
    assert 'model_provider = "OtherProvider"' in contents
    assert "[model_providers.OtherProvider]" in contents
    assert "[model_providers.CodexPlusPlus]" not in contents
    assert "sk-test" not in contents


def test_apply_relay_config_requires_base_url_and_key(tmp_path):
    with pytest.raises(ValueError, match="Base URL"):
        apply_relay_config("", "sk-test", tmp_path)
    with pytest.raises(ValueError, match="API Key"):
        apply_relay_config("https://relay.example.com/v1", "", tmp_path)
