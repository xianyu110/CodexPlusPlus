//! DreamSkin compatibility hooks. Community skin assets are intentionally not bundled.

use crate::settings::DreamSkinThemeConfig;

pub fn sync_default_dream_skin_base_theme(
    _enabled: bool,
    _theme: &DreamSkinThemeConfig,
) -> anyhow::Result<()> {
    Ok(())
}

pub fn is_managed_dream_skin_image(
    _path: &std::path::Path,
    _state_dir: &std::path::Path,
) -> bool {
    false
}
