# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Query : cibles recemment scannees mais jamais epinglees, les plus
recentes en tete, limitees a 10 (retours utilisateur §8.5/§10.5).

Derivee de l'historique des scans plutot que portee par un nouveau
port/repository dedie : aucune persistance propre a ce concept, seulement
une lecture filtree de donnees deja stockees."""
from __future__ import annotations

from omega_scan.application.queries.list_scan_history import list_scan_history
from omega_scan.ports.scan_repository import ScanRepository
from omega_scan.ports.target_repository import TargetRepository

_MAX_RECENT = 10


def list_recent_targets(
    *, scan_repository: ScanRepository, target_repository: TargetRepository
) -> tuple[str, ...]:
    """Hotes distincts, tries du plus recent au plus ancien, en excluant
    ceux deja epingles (deja proposes separement, voir list_targets)."""
    pinned_hosts = {p.normalized_host for p in target_repository.list_pinned()}
    scans = list_scan_history(scan_repository=scan_repository, limit=200)
    seen: list[str] = []
    for scan in scans:
        if scan.normalized_host in pinned_hosts or scan.normalized_host in seen:
            continue
        seen.append(scan.normalized_host)
        if len(seen) >= _MAX_RECENT:
            break
    return tuple(seen)
