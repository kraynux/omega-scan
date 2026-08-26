# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : choisir un theme TUI parmi le catalogue partage de la suite
(ARCHITECTURE.md §8)."""
from __future__ import annotations

from omega_scan.core.results import Err, Ok, Result
from omega_scan.domain.errors import ValidationError
from omega_scan.domain.theme.policies import TUI_THEMES
from omega_scan.ports.settings_store import SettingsStore


def select_theme(*, settings_store: SettingsStore, theme_name: str) -> Result[None, ValidationError]:
    """Valide le nom contre le catalogue avant de le persister — un theme
    de couleur (choix manuel) reste independant du profil de rendu
    (decide automatiquement), jamais melanges dans le meme reglage."""
    if theme_name not in TUI_THEMES:
        return Err(
            ValidationError(
                f"Theme inconnu : {theme_name!r}. Choix : {sorted(TUI_THEMES.keys())}"
            )
        )
    settings_store.set("theme", theme_name)
    return Ok(None)
