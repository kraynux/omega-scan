# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Query : lister les cibles epinglees-autorisees."""
from __future__ import annotations

from omega_scan.application.dto.mappers import pinned_target_to_dto
from omega_scan.application.dto.target_dto import PinnedTargetDTO
from omega_scan.ports.target_repository import TargetRepository


def list_targets(*, target_repository: TargetRepository) -> tuple[PinnedTargetDTO, ...]:
    return tuple(pinned_target_to_dto(p) for p in target_repository.list_pinned())
