# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Guard 2/2 du pipeline : profil de rendu depuis la capacite terminal
(ARCHITECTURE.md §4, chaine Capacite terminal)."""
from __future__ import annotations

from omega_scan.core.enums import RenderProfile
from omega_scan.domain.terminal.service import resolve_render_profile
from omega_scan.ports.terminal_detector import TerminalDetector


def check_render_capability(*, terminal_detector: TerminalDetector) -> RenderProfile:
    """Determine le profil de rendu utilisable, jamais un refus : a la
    difference d'omega-stress (qui bloque un niveau d'intensite si le
    systeme local est insuffisant), omega-scan n'a pas de niveau a
    bloquer — seulement un profil de rendu a resoudre, avec MONO comme
    plancher garanti (domain/terminal/policies.py::DEFAULT_RENDER_PROFILE
    et la degradation par taille)."""
    signals = terminal_detector.detect()
    return resolve_render_profile(signals).render_profile
