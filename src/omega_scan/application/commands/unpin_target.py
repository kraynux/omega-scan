# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : retirer l'epinglage d'une cible."""
from __future__ import annotations

from omega_scan.ports.target_repository import TargetRepository


def unpin_target(*, target_repository: TargetRepository, normalized_host: str) -> None:
    """Retire l'epinglage. Un futur scan sur cette cible redemandera une
    confirmation explicite (ARCHITECTURE.md §7) — aucun echec metier
    possible ici, retirer un epinglage deja absent est un no-op."""
    target_repository.unpin(normalized_host)
