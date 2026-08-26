# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Erreurs du sous-domaine profiles."""
from __future__ import annotations

from omega_scan.domain.errors import DomainError


class UnknownProfileError(DomainError):
    """Nom de profil de scan non reconnu parmi quick/standard/extended/local-lab."""
