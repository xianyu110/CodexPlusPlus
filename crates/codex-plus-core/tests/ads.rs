use codex_plus_core::ads::{empty_ad_payload, fetch_ad_list};
use serde_json::json;

#[test]
fn ad_payload_is_always_empty() {
    assert_eq!(empty_ad_payload(), json!({ "version": 1, "ads": [] }));
}

#[tokio::test]
async fn ad_loader_never_performs_remote_loading() {
    assert_eq!(
        fetch_ad_list()
            .await
            .expect("disabled ad loader should succeed"),
        json!({ "version": 1, "ads": [] })
    );
}

#[test]
fn renderer_has_no_ad_or_sponsor_runtime() {
    let script = codex_plus_core::assets::renderer_script();
    for forbidden in [
        "BigPizzaV3/Ad-List",
        "codexPlusAds",
        "data-codex-plus-panel=\"sponsor\"",
        "请作者喝咖啡",
        "赞助商推荐",
    ] {
        assert!(
            !script.contains(forbidden),
            "found forbidden runtime marker: {forbidden}"
        );
    }
}
