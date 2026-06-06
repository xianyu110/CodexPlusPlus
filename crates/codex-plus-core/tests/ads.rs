use codex_plus_core::ads::{domestic_relay_payload, fetch_ad_list, normalize_ad_payload};
use serde_json::json;

#[test]
fn domestic_relay_payload_contains_china_codex_entries() {
    let payload = domestic_relay_payload();
    let ads = payload["ads"].as_array().unwrap();

    assert_eq!(payload["version"], json!(1));
    assert_eq!(ads.len(), 2);
    assert_eq!(ads[0]["type"], json!("relay"));
    assert_eq!(ads[0]["url"], json!("https://codex.chatgpt-plus.top/login"));
    assert_eq!(ads[1]["url"], json!("https://codex2.chatgpt-plus.top/login"));
}

#[test]
fn normalizes_domestic_relay_entries_for_plugin_and_manager_rendering() {
    let payload = normalize_ad_payload(json!({
        "version": 1,
        "ads": [
            {
                "id": "relay",
                "type": "relay",
                "title": "Codex 国内使用",
                "description": "国内入口",
                "url": "https://codex.chatgpt-plus.top/login",
                "highlights": ["稳定"]
            },
            {
                "id": "normal",
                "type": "normal",
                "title": "备用入口",
                "description": "国内入口",
                "url": "https://codex2.chatgpt-plus.top/login"
            },
            {
                "id": "external",
                "type": "external",
                "title": "外部推荐",
                "description": "不应保留",
                "url": "https://example.invalid"
            },
            {
                "id": "broken",
                "type": "relay",
                "title": "",
                "description": "missing title",
                "url": "https://example.invalid"
            }
        ]
    }));

    assert_eq!(payload["version"], json!(1));
    assert_eq!(payload["ads"].as_array().unwrap().len(), 2);
    assert_eq!(payload["ads"][0]["type"], json!("relay"));
    assert_eq!(payload["ads"][1]["type"], json!("normal"));
}

#[tokio::test]
async fn fetch_ad_list_returns_builtin_domestic_relays() {
    let payload = fetch_ad_list().await.unwrap();
    let ads = payload["ads"].as_array().unwrap();

    assert_eq!(ads.len(), 2);
    assert_eq!(ads[0]["url"], json!("https://codex.chatgpt-plus.top/login"));
    assert_eq!(ads[1]["url"], json!("https://codex2.chatgpt-plus.top/login"));
}
