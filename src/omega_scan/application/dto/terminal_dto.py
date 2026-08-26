# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""DTO expose a la presentation pour le profil de rendu detecte."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TerminalProfileDTO:
    """Vue plate d'un TerminalProfile (domain/terminal/models.py)."""

    family: str
    columns: int
    rows: int
    render_profile: str
