# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Politiques de terminal : matrice famille -> profil de rendu, paliers de taille
(porte depuis omega-stress ; memes valeurs, la compatibilite terminal est un
constat transverse a la suite `omega-`, pas specifique au test de charge)."""
from __future__ import annotations

from omega_scan.core.enums import RenderProfile

TERMINAL_FAMILY_PROFILES: dict[str, RenderProfile] = {
    "ghostty": RenderProfile.COMPLETE,
    "alacritty": RenderProfile.COMPLETE,
    "wezterm": RenderProfile.COMPLETE,
    "kitty": RenderProfile.COMPLETE,
    "konsole": RenderProfile.STANDARD,
    "gnome-terminal": RenderProfile.STANDARD,
    "terminator": RenderProfile.STANDARD,
    "xfce4-terminal": RenderProfile.STANDARD,
    "urxvt": RenderProfile.REDUCED,
    "xterm": RenderProfile.REDUCED,
    "linux-tty": RenderProfile.MONO,
    "ssh-modern": RenderProfile.REDUCED,
    "ssh-legacy": RenderProfile.MONO,
}
"""Profil initial par famille de terminal detectee (noms normalises en
minuscules avec tirets, voir infrastructure/terminal/detector.py, Lot M2)."""

DEFAULT_RENDER_PROFILE: RenderProfile = RenderProfile.REDUCED
"""Profil applique quand la famille de terminal n'est pas reconnue."""

_SIZE_THRESHOLDS: tuple[tuple[int, int, RenderProfile], ...] = (
    (120, 32, RenderProfile.COMPLETE),
    (100, 28, RenderProfile.STANDARD),
    (80, 24, RenderProfile.REDUCED),
)
"""Paliers (colonnes minimales, lignes minimales, plafond de profil), du
plus exigeant au moins exigeant. En dessous du dernier palier : MONO."""

MINIMUM_USABLE_COLUMNS: int = 80
MINIMUM_USABLE_ROWS: int = 24

_PROFILE_ORDER: tuple[RenderProfile, ...] = (
    RenderProfile.MONO,
    RenderProfile.REDUCED,
    RenderProfile.STANDARD,
    RenderProfile.COMPLETE,
)
"""Ordre du moins au plus riche, utilise par most_restrictive()."""


def render_profile_ceiling_for_size(columns: int, rows: int) -> RenderProfile:
    """Plafond de profil de rendu autorise pour une taille de terminal
    donnee, independamment de la famille de terminal detectee."""
    for min_columns, min_rows, profile in _SIZE_THRESHOLDS:
        if columns >= min_columns and rows >= min_rows:
            return profile
    return RenderProfile.MONO


def most_restrictive(a: RenderProfile, b: RenderProfile) -> RenderProfile:
    """Retourne le profil le moins riche des deux."""
    return a if _PROFILE_ORDER.index(a) <= _PROFILE_ORDER.index(b) else b
