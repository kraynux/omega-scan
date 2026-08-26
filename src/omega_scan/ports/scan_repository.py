# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat de persistance et d'historique des scans."""
from __future__ import annotations

from typing import Protocol

from omega_scan.domain.scans.models import ScanRun


class ScanRepository(Protocol):
    """Port consomme par application/ (run_scan, list_scan_history,
    get_scan_details, compare_scans), implemente par
    infrastructure/storage/sqlite/scan_repository.py.

    Filtre par `normalized_host` plutot que par un identifiant de profil :
    contrairement a omega-stress, les profils de scan sont des presets
    predefinis en lecture seule (domain/profiles/policies.py), pas des
    entites persistees pouvant servir de cle de filtrage."""

    def save(self, run: ScanRun) -> None: ...

    def get(self, scan_id: str) -> ScanRun | None: ...

    def list_history(
        self,
        *,
        normalized_host: str | None = None,
        limit: int = 50,
    ) -> tuple[ScanRun, ...]: ...

    def clear(self) -> None: ...
