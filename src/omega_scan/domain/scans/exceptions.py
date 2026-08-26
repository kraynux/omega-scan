# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Erreurs du sous-domaine scans.

Les echecs reseau previsibles restent portes par ScanError en tant que
donnee, pas par une exception (voir domain/scans/models.py). ScanNotFoundError
est le premier besoin reel, ajoute au Lot M3 pour les commands/queries qui
recuperent un scan par id (replay_scan, get_scan_details, compare_scans)."""
from __future__ import annotations

from omega_scan.domain.errors import DomainError


class ScanNotFoundError(DomainError):
    """Aucun ScanRun trouve pour l'identifiant de scan demande."""
