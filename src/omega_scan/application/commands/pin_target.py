# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : epingler une cible comme autorisee de facon durable."""
from __future__ import annotations

from datetime import datetime

from omega_scan.application.dto.mappers import pinned_target_to_dto
from omega_scan.application.dto.target_dto import PinnedTargetDTO
from omega_scan.core.results import Err, Ok, Result
from omega_scan.domain.targets import service as targets_service
from omega_scan.domain.targets.exceptions import TargetParseError
from omega_scan.domain.targets.validation import parse_target
from omega_scan.ports.target_repository import TargetRepository


def pin_target(
    *,
    target_repository: TargetRepository,
    now: datetime,
    raw_input: str,
    note: str | None = None,
) -> Result[PinnedTargetDTO, TargetParseError]:
    """Parse l'entree saisie, epingle la cible comme autorisee (confirmation
    implicite : epingler EST l'acte de confirmation, ARCHITECTURE.md §7) et
    persiste."""
    try:
        target = parse_target(raw_input)
    except TargetParseError as exc:
        return Err(exc)

    now_iso = now.isoformat().replace("+00:00", "Z")
    pinned = targets_service.pin_target(target, now_iso, note)
    target_repository.pin(pinned)
    return Ok(pinned_target_to_dto(pinned))
