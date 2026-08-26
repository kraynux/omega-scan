# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : desepingler toutes les cibles (ecran Reglages)."""
from __future__ import annotations

from omega_scan.ports.target_repository import TargetRepository


def clear_all_targets(*, target_repository: TargetRepository) -> None:
    target_repository.clear()
