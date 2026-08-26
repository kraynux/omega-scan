# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Query : lister l'historique des scans, avec filtre optionnel par cible."""
from __future__ import annotations

from omega_scan.application.dto.mappers import scan_summary_to_dto
from omega_scan.application.dto.scan_dto import ScanSummaryDTO
from omega_scan.ports.scan_repository import ScanRepository


def list_scan_history(
    *,
    scan_repository: ScanRepository,
    normalized_host: str | None = None,
    limit: int = 50,
) -> tuple[ScanSummaryDTO, ...]:
    runs = scan_repository.list_history(normalized_host=normalized_host, limit=limit)
    return tuple(scan_summary_to_dto(run) for run in runs)
