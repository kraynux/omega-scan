# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Decision du profil de rendu a partir des signaux bruts du terminal
(porte depuis omega-stress)."""
from __future__ import annotations

from omega_scan.domain.terminal.models import TerminalProfile, TerminalSignals
from omega_scan.domain.terminal.policies import (
    DEFAULT_RENDER_PROFILE,
    TERMINAL_FAMILY_PROFILES,
    most_restrictive,
    render_profile_ceiling_for_size,
)


def resolve_render_profile(signals: TerminalSignals) -> TerminalProfile:
    """Combine la famille de terminal et sa taille : le profil retenu est
    le plus restrictif des deux (une taille insuffisante degrade meme un
    terminal par ailleurs complet, jamais l'inverse)."""
    family_profile = TERMINAL_FAMILY_PROFILES.get(signals.family, DEFAULT_RENDER_PROFILE)
    size_ceiling = render_profile_ceiling_for_size(signals.columns, signals.rows)
    resolved = most_restrictive(family_profile, size_ceiling)
    return TerminalProfile(signals=signals, render_profile=resolved)
