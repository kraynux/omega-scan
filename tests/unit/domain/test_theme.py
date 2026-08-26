# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.core.enums import RenderProfile
from omega_scan.domain.theme.policies import DEFAULT_TUI_THEME, TUI_THEMES
from omega_scan.domain.theme.service import resolve_applied_theme, resolve_palette


def test_catalog_has_10_tui_themes_and_5_export_palettes():
    from omega_scan.domain.theme.policies import EXPORT_PALETTES
    assert len(TUI_THEMES) == 10
    assert len(EXPORT_PALETTES) == 5


def test_resolve_applied_theme_known_theme_no_fallback():
    applied = resolve_applied_theme("omega-neon", RenderProfile.COMPLETE)
    assert applied.theme_name == "omega-neon"
    assert applied.fell_back_from is None


def test_resolve_applied_theme_unknown_theme_falls_back_to_default():
    applied = resolve_applied_theme("does-not-exist", RenderProfile.STANDARD)
    assert applied.theme_name == DEFAULT_TUI_THEME
    assert applied.fell_back_from == "does-not-exist"


def test_resolve_palette_mono_converts_to_grayscale():
    palette = resolve_palette("omega-base", RenderProfile.MONO)
    assert palette.background.startswith("#")
    r, g, b = palette.background[1:3], palette.background[3:5], palette.background[5:7]
    assert r == g == b


def test_resolve_palette_reduced_flattens_surface_and_panel_on_background():
    palette = resolve_palette("omega-base", RenderProfile.REDUCED)
    assert palette.surface == palette.background
    assert palette.panel == palette.background


def test_resolve_palette_complete_keeps_original():
    definition = TUI_THEMES["omega-base"]
    palette = resolve_palette("omega-base", RenderProfile.COMPLETE)
    assert palette == definition.palette
