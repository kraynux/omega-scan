# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Chargement des feuilles de style selon le profil de rendu deja decide.

Fusionne ici ce qui serait, chez omega-stress, reparti entre
render_profile_resolver.py et stylesheet_loader.py : omega-scan n'a pas
besoin d'un fichier de decision separe (domain/terminal/service.py decide
deja seul le RenderProfile), seule la traduction profil -> chemins reste
une preoccupation de presentation."""
from __future__ import annotations

from pathlib import Path

from omega_scan.core.enums import RenderProfile

_STYLES_DIR = Path(__file__).parent.parent / "styles"

_PROFILE_STYLESHEETS: dict[RenderProfile, str] = {
    RenderProfile.COMPLETE: "complete.tcss",
    RenderProfile.STANDARD: "standard.tcss",
    RenderProfile.REDUCED: "reduced.tcss",
    RenderProfile.MONO: "mono.tcss",
}


def stylesheet_paths_for(profile: RenderProfile) -> tuple[Path, Path]:
    """Retourne (base.tcss, <profil>.tcss) — base toujours chargee en
    premier, le fichier du profil vient ensuite affiner/surcharger."""
    return (_STYLES_DIR / "base.tcss", _STYLES_DIR / _PROFILE_STYLESHEETS[profile])


def load_paths_for(profile: RenderProfile) -> list[str]:
    """Format attendu par `textual.app.App.CSS_PATH` (liste de chaines)."""
    return [str(path) for path in stylesheet_paths_for(profile)]
