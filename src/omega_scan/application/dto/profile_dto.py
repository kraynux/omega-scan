# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""DTO expose a la presentation pour un profil de scan predefini."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScanProfileDTO:
    """Vue plate d'un ScanProfile (domain/profiles/models.py)."""

    profile_name: str
    timeout_connect: int
    timeout_read: int
    http_methods_tested: tuple[str, ...]
    path_checks_enabled: bool
    tls_checks_enabled: bool
