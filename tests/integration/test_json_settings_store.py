# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests d'integration de JsonSettingsStore, sur un fichier reel."""
from __future__ import annotations

from pathlib import Path

from omega_scan.infrastructure.storage.files.json_settings_store import JsonSettingsStore


def test_get_on_missing_file_returns_default(tmp_path: Path):
    store = JsonSettingsStore(tmp_path / "settings.json")

    assert store.get("theme", default="omega-base") == "omega-base"


def test_set_then_get_roundtrips(tmp_path: Path):
    store = JsonSettingsStore(tmp_path / "settings.json")

    store.set("theme", "omega-neon")

    assert store.get("theme") == "omega-neon"


def test_set_persists_across_instances(tmp_path: Path):
    path = tmp_path / "settings.json"
    JsonSettingsStore(path).set("render_profile", "reduced")

    reloaded = JsonSettingsStore(path)

    assert reloaded.get("render_profile") == "reduced"


def test_all_returns_every_stored_key(tmp_path: Path):
    store = JsonSettingsStore(tmp_path / "settings.json")
    store.set("theme", "omega-base")
    store.set("render_profile", "complete")

    assert store.all() == {"theme": "omega-base", "render_profile": "complete"}
