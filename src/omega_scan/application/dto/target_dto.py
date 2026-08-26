# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""DTO expose a la presentation pour une cible epinglee-autorisee."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PinnedTargetDTO:
    """Vue plate d'une PinnedTarget (domain/targets/models.py)."""

    normalized_host: str
    authorized: bool
    pinned_at: str
    note: str | None
