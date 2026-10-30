# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Query : comparer deux scans d'une meme cible (ARCHITECTURE.md §4, Historique
et comparaison).

Pas de application/services/scan_comparison_service.py separe : la logique
tient dans les 2 lectures + l'appel a domain/reports/comparison.py + le
mapping DTO, sans orchestration transversale a plusieurs commands/queries
qui justifierait un fichier de service dedie (meme constat qu'omega-stress
pour history_query_service.py, laisse vide faute de besoin reel)."""
from __future__ import annotations

from omega_scan.application.dto.comparison_dto import ScanComparisonDTO
from omega_scan.application.dto.mappers import scan_comparison_to_dto
from omega_scan.core.results import Err, Ok, Result
from omega_scan.domain.reports.comparison import compare_scans as compute_comparison
from omega_scan.domain.scans.exceptions import ScanNotFoundError
from omega_scan.ports.scan_repository import ScanRepository
from omega_scan.shared.i18n import _


def compare_scans(
    *,
    scan_repository: ScanRepository,
    previous_scan_id: str,
    current_scan_id: str,
) -> Result[ScanComparisonDTO, ScanNotFoundError]:
    previous = scan_repository.get(previous_scan_id)
    if previous is None:
        return Err(ScanNotFoundError(_("Aucun scan trouvé pour l'identifiant "
                                       "{previous_scan_id!r}.").format(previous_scan_id=previous_scan_id)))

    current = scan_repository.get(current_scan_id)
    if current is None:
        return Err(ScanNotFoundError(_("Aucun scan trouvé pour l'identifiant {current_scan_id!r}.").format(current_scan_id=current_scan_id)))

    comparison = compute_comparison(previous, current)
    return Ok(scan_comparison_to_dto(comparison))
