# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : forcer manuellement un profil de rendu, ou revenir a l'automatique."""
from __future__ import annotations

from omega_scan.core.enums import RenderProfile
from omega_scan.ports.settings_store import SettingsStore


def select_render_profile(
    *, settings_store: SettingsStore, render_profile: RenderProfile | None
) -> None:
    """Persiste une surcharge manuelle du profil de rendu. `None` revient
    au mode automatique (domain/terminal/service.py::resolve_render_profile),
    jamais un echec metier possible ici."""
    settings_store.set(
        "render_profile_override",
        render_profile.value if render_profile is not None else "",
    )
