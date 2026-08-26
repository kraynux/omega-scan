# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat de lecture/ecriture des preferences globales (settings.json)."""
from __future__ import annotations

from typing import Protocol


class SettingsStore(Protocol):
    """Port consomme par application/ (select_theme, select_render_profile),
    implemente par infrastructure/storage/files/json_settings_store.py."""

    def get(self, key: str, default: str | None = None) -> str | None: ...

    def set(self, key: str, value: str) -> None: ...

    def all(self) -> dict[str, str]: ...
