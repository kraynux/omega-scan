# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Query : recuperer le detail complet d'un scan par id."""
from __future__ import annotations

from omega_scan.application.dto.mappers import scan_run_to_dto
from omega_scan.application.dto.scan_dto import ScanRunDTO
from omega_scan.ports.scan_repository import ScanRepository


def get_scan_details(*, scan_repository: ScanRepository, scan_id: str) -> ScanRunDTO | None:
    """Retourne None si le scan n'existe pas : l'absence d'un scan n'est
    pas un echec metier a traiter via Result, c'est un resultat de
    recherche normal (meme convention que ports/scan_repository.py::get())."""
    run = scan_repository.get(scan_id)
    if run is None:
        return None
    return scan_run_to_dto(run)
