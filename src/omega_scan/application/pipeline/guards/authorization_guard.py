# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Guard 1/2 du pipeline : autorisation de la cible (ARCHITECTURE.md §4, §7)."""
from __future__ import annotations

from omega_scan.core.results import Err, Ok, Result
from omega_scan.domain.targets.exceptions import UnauthorizedTargetError
from omega_scan.domain.targets.models import Target
from omega_scan.ports.target_repository import TargetRepository


def check_authorization(
    target: Target,
    *,
    target_repository: TargetRepository,
    explicit_confirmation: bool,
) -> Result[None, UnauthorizedTargetError]:
    """Autorise si la cible est deja epinglee-autorisee, ou si une
    confirmation explicite est fournie pour ce scan precis.

    Utilise `target_repository.get(normalized_host)` plutot que
    `domain.targets.service.is_authorized(list_pinned(), target)` : le port
    expose deja un acces direct par cle (`get`), une recherche lineaire sur
    `list_pinned()` n'apporterait rien ici et couterait une lecture de
    l'historique complet des cibles epinglees a chaque scan."""
    pinned = target_repository.get(target.normalized_host)
    if pinned is not None and pinned.authorized:
        return Ok(None)
    if explicit_confirmation:
        return Ok(None)
    return Err(
        UnauthorizedTargetError(
            f"Cible {target.normalized_host!r} non autorisee : ni epinglee, "
            f"ni confirmation explicite fournie pour ce scan."
        )
    )
