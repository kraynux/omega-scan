# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Entite representant l'etat d'un theme applique (porte depuis omega-stress,
catalogue partage de la suite, ARCHITECTURE.md §8)."""
from __future__ import annotations

from dataclasses import dataclass

from omega_scan.core.enums import RenderProfile


@dataclass(frozen=True, slots=True)
class AppliedTheme:
    """Theme effectivement applique a l'interface : nom retenu, profil de
    rendu courant, et repli eventuel si le theme demande etait inconnu."""

    theme_name: str
    render_profile: RenderProfile
    fell_back_from: str | None = None
