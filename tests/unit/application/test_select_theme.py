# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_scan.application.commands.select_render_profile import select_render_profile
from omega_scan.application.commands.select_theme import select_theme
from omega_scan.core.enums import RenderProfile
from omega_scan.core.results import Err, Ok
from omega_scan.domain.errors import ValidationError
from tests.unit.application.conftest import FakeSettingsStore


def test_select_theme_persists_valid_name():
    settings = FakeSettingsStore()
    result = select_theme(settings_store=settings, theme_name="omega-neon")

    assert isinstance(result, Ok)
    assert settings.get("theme") == "omega-neon"


def test_select_theme_rejects_unknown_name():
    settings = FakeSettingsStore()
    result = select_theme(settings_store=settings, theme_name="not-a-real-theme")

    assert isinstance(result, Err)
    assert isinstance(result.error, ValidationError)
    assert settings.get("theme") is None


def test_select_render_profile_override_and_reset_to_auto():
    settings = FakeSettingsStore()

    select_render_profile(settings_store=settings, render_profile=RenderProfile.MONO)
    assert settings.get("render_profile_override") == "mono"

    select_render_profile(settings_store=settings, render_profile=None)
    assert settings.get("render_profile_override") == ""
