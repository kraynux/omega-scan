# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : purger tout l'historique des scans (ecran Reglages)."""
from __future__ import annotations

from omega_scan.ports.scan_repository import ScanRepository


def clear_scan_history(*, scan_repository: ScanRepository) -> None:
    scan_repository.clear()
