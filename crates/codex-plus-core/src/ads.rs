use serde_json::{Value, json};

pub fn empty_ad_payload() -> Value {
    json!({ "version": 1, "ads": [] })
}

pub async fn fetch_ad_list() -> anyhow::Result<Value> {
    Ok(empty_ad_payload())
}
