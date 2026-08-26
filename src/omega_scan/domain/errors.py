# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Racine des erreurs metier attendues (ARCHITECTURE.md §5.2)."""
from __future__ import annotations

from omega_scan.core.exceptions import OmegaScanError


class DomainError(OmegaScanError):
    """Racine de toute erreur metier attendue. Les sous-types specifiques a
    un sous-domaine vivent dans le `exceptions.py` de ce sous-domaine
    (ex. `domain/targets/exceptions.py`), pas ici."""


class ValidationError(DomainError):
    """Valeur mal formee ne relevant d'aucun sous-domaine plus specifique."""
