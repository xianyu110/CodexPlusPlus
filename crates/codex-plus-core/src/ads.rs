use serde_json::{Value, json};

pub fn domestic_relay_payload() -> Value {
    json!({
        "version": 1,
        "ads": [
            {
                "id": "codex-chatgpt-plus",
                "type": "relay",
                "title": "Codex 国内使用",
                "description": "国内 Codex 登录和使用入口，适合无法直连官方服务时访问。",
                "url": "https://codex.chatgpt-plus.top/login",
                "highlights": ["国内入口", "Codex"]
            },
            {
                "id": "codex2-chatgpt-plus",
                "type": "relay",
                "title": "Codex 国内使用备用入口",
                "description": "国内 Codex 备用入口，可在主入口不可用时切换使用。",
                "url": "https://codex2.chatgpt-plus.top/login",
                "highlights": ["备用入口", "Codex"]
            }
        ]
    })
}

pub fn normalize_ad_payload(payload: Value) -> Value {
    let version = payload.get("version").and_then(Value::as_u64).unwrap_or(1);
    let ads = payload
        .get("ads")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
        .filter(|ad| {
            let ad_type = ad.get("type").and_then(Value::as_str);
            let title = ad.get("title").and_then(Value::as_str);
            let description = ad.get("description").and_then(Value::as_str);
            let url = ad.get("url").and_then(Value::as_str);
            matches!(ad_type, Some("relay" | "normal"))
                && title.is_some_and(|value| !value.trim().is_empty())
                && description.is_some_and(|value| !value.trim().is_empty())
                && url.is_some_and(|value| !value.trim().is_empty())
        })
        .cloned()
        .collect::<Vec<_>>();
    json!({ "version": version, "ads": ads })
}

pub async fn fetch_ad_list() -> anyhow::Result<Value> {
    Ok(normalize_ad_payload(domestic_relay_payload()))
}
