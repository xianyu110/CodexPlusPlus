from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


RELAY_PROVIDER = "CodexPlusPlus"
LEGACY_RELAY_PROVIDER = "CodexPP"


@dataclass(frozen=True)
class RelayStatus:
    authenticated: bool
    auth_source: str
    account_label: str | None
    configured: bool
    requires_openai_auth: bool
    has_bearer_token: bool
    config_path: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "authenticated": self.authenticated,
            "authSource": self.auth_source,
            "accountLabel": self.account_label,
            "configured": self.configured,
            "requiresOpenaiAuth": self.requires_openai_auth,
            "hasBearerToken": self.has_bearer_token,
            "configPath": str(self.config_path),
        }


@dataclass(frozen=True)
class RelayApplyResult:
    config_path: Path
    configured: bool
    status: str
    message: str

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "message": self.message,
            "configPath": str(self.config_path),
            "configured": self.configured,
        }


def default_codex_home() -> Path:
    return Path.home() / ".codex"


def relay_status(codex_home: Path | None = None) -> RelayStatus:
    home = codex_home or default_codex_home()
    config_path = home / "config.toml"
    contents = _read_text(config_path)
    provider = _table_values(contents, f"model_providers.{RELAY_PROVIDER}") or {}
    requires_openai_auth = provider.get("requires_openai_auth", "").strip() == "true"
    has_bearer_token = bool(_unquote(provider.get("experimental_bearer_token", "")).strip())
    has_base_url = bool(_unquote(provider.get("base_url", "")).strip())
    configured = (
        _root_key_string(contents, "model_provider") == RELAY_PROVIDER
        and requires_openai_auth
        and has_bearer_token
        and has_base_url
    )
    authenticated, account_label = _chatgpt_auth_status(home / "auth.json")
    return RelayStatus(
        authenticated=authenticated,
        auth_source=str(home / "auth.json") if authenticated else "",
        account_label=account_label,
        configured=configured,
        requires_openai_auth=requires_openai_auth,
        has_bearer_token=has_bearer_token,
        config_path=config_path,
    )


def apply_relay_config(base_url: str, api_key: str, codex_home: Path | None = None) -> RelayApplyResult:
    base_url = base_url.strip().rstrip("/")
    api_key = api_key.strip()
    if not base_url:
        raise ValueError("中转 Base URL 不能为空")
    if not api_key:
        raise ValueError("中转 API Key 不能为空")

    home = codex_home or default_codex_home()
    home.mkdir(parents=True, exist_ok=True)
    config_path = home / "config.toml"
    existing = _read_text(config_path)
    updated = _upsert_model_provider(existing, base_url, api_key)
    _atomic_write(config_path, updated)
    status = relay_status(home)
    return RelayApplyResult(
        config_path=config_path,
        configured=status.configured,
        status="ok" if status.configured else "failed",
        message="中转配置已启用" if status.configured else "中转配置写入后未通过状态检查",
    )


def clear_relay_config(codex_home: Path | None = None) -> RelayApplyResult:
    home = codex_home or default_codex_home()
    home.mkdir(parents=True, exist_ok=True)
    _clear_api_key_from_auth_json(home / "auth.json")
    config_path = home / "config.toml"
    existing = _read_text(config_path)
    current_provider = _root_key_string(existing, "model_provider")
    updated = _remove_table(
        _remove_table(existing, f"model_providers.{RELAY_PROVIDER}"),
        f"model_providers.{LEGACY_RELAY_PROVIDER}",
    )
    if current_provider in {RELAY_PROVIDER, LEGACY_RELAY_PROVIDER}:
        updated = _remove_root_key(updated, "model_provider")
    updated = _remove_root_key(updated, "OPENAI_API_KEY")
    _atomic_write(config_path, updated)
    status = relay_status(home)
    return RelayApplyResult(
        config_path=config_path,
        configured=status.configured,
        status="failed" if status.configured else "ok",
        message="中转配置已清理" if not status.configured else "中转配置清理后仍处于启用状态",
    )


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _atomic_write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp")
    temp_path.write_text(contents, encoding="utf-8")
    os.replace(temp_path, path)


def _chatgpt_auth_status(path: Path) -> tuple[bool, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, None
    if not isinstance(payload, dict):
        return False, None
    if str(payload.get("auth_mode", "")).lower() != "chatgpt":
        return False, None
    tokens = payload.get("tokens")
    if not isinstance(tokens, dict):
        return False, None
    has_token = any(str(tokens.get(key, "")).strip() for key in ("access_token", "id_token", "refresh_token"))
    if not has_token:
        return False, None
    label = payload.get("email") or payload.get("account") or payload.get("name")
    return True, str(label).strip() if label else None


def _upsert_model_provider(contents: str, base_url: str, api_key: str) -> str:
    updated = _upsert_root_key(contents, "model_provider", f'"{_toml_escape(RELAY_PROVIDER)}"')
    updated = _remove_table(updated, f"model_providers.{RELAY_PROVIDER}")
    updated = _remove_table(updated, f"model_providers.{LEGACY_RELAY_PROVIDER}")

    lines = updated.splitlines()
    insert_at = next(
        (index for index, line in enumerate(lines) if line.strip().startswith("[") and not line.strip().startswith("[model_providers.")),
        len(lines),
    )
    provider_lines = [
        f"[model_providers.{RELAY_PROVIDER}]",
        f'name = "{_toml_escape(RELAY_PROVIDER)}"',
        'wire_api = "responses"',
        "requires_openai_auth = true",
        f'base_url = "{_toml_escape(base_url)}"',
        f'experimental_bearer_token = "{_toml_escape(api_key)}"',
        "",
    ]
    lines[insert_at:insert_at] = provider_lines
    output = "\n".join(lines)
    return output if output.endswith("\n") else f"{output}\n"


def _upsert_root_key(contents: str, key: str, value: str) -> str:
    lines = contents.splitlines()
    root_end = next((index for index, line in enumerate(lines) if line.strip().startswith("[")), len(lines))
    for index in range(root_end):
        if _root_line_key(lines[index]) == key:
            lines[index] = f"{key} = {value}"
            break
    else:
        lines.insert(root_end, f"{key} = {value}")
    output = "\n".join(lines)
    return output if output.endswith("\n") else f"{output}\n"


def _remove_root_key(contents: str, key: str) -> str:
    lines = []
    in_root = True
    for line in contents.splitlines():
        if line.strip().startswith("["):
            in_root = False
        if in_root and _root_line_key(line) == key:
            continue
        lines.append(line)
    output = "\n".join(lines)
    return output if not output or output.endswith("\n") else f"{output}\n"


def _remove_table(contents: str, table: str) -> str:
    header = f"[{table}]"
    lines = []
    skipping = False
    for line in contents.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            if stripped == header:
                skipping = True
                continue
            skipping = False
        if not skipping:
            lines.append(line)
    output = "\n".join(lines)
    return output if not output or output.endswith("\n") else f"{output}\n"


def _clear_api_key_from_auth_json(path: Path) -> None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    if not isinstance(payload, dict) or "OPENAI_API_KEY" not in payload:
        return
    payload.pop("OPENAI_API_KEY", None)
    _atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _root_key_string(contents: str, key: str) -> str:
    for line in contents.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            return ""
        if not stripped or stripped.startswith("#"):
            continue
        if _root_line_key(stripped) == key:
            return _unquote(stripped.split("=", 1)[1])
    return ""


def _root_line_key(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or stripped.startswith("["):
        return None
    if "=" not in stripped:
        return None
    return stripped.split("=", 1)[0].strip()


def _table_values(contents: str, table: str) -> dict[str, str] | None:
    header = f"[{table}]"
    in_table = False
    values: dict[str, str] = {}
    for line in contents.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            if in_table:
                break
            in_table = stripped == header
            continue
        if not in_table or not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values if in_table else None


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value


def _toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
