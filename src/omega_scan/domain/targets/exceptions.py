# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Erreurs du sous-domaine targets (ARCHITECTURE.md §5.2, §7)."""
from __future__ import annotations

from omega_scan.domain.errors import DomainError


class TargetParseError(DomainError):
    """Entree cible invalide, non normalisable (hote absent, format illisible)."""


class UnauthorizedTargetError(DomainError):
    """Cible non confirmee et non deja epinglee-autorisee : le scan ne peut
    pas demarrer (ARCHITECTURE.md §7, verifie par
    application/pipeline/guards/authorization_guard.py)."""
