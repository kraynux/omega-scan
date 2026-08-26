# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Entites du sous-domaine terminal : signaux bruts et profil de rendu resolu
(porte depuis omega-stress)."""
from __future__ import annotations

from dataclasses import dataclass

from omega_scan.core.enums import RenderProfile


@dataclass(frozen=True, slots=True)
class TerminalSignals:
    """Signaux bruts remontes par infrastructure/terminal/raw_capabilities.py
    (Lot M2) — aucune decision ici, uniquement des faits observes."""

    family: str
    columns: int
    rows: int
    is_ssh: bool = False


@dataclass(frozen=True, slots=True)
class TerminalProfile:
    """Resultat de la decision prise par
    domain/terminal/service.py::resolve_render_profile a partir de TerminalSignals."""

    signals: TerminalSignals
    render_profile: RenderProfile
