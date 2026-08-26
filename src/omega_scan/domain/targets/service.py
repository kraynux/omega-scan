# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Regles d'epinglage et d'autorisation de cible (ARCHITECTURE.md §7).

Fonctions pures : l'heure courante est fournie par l'appelant (`now_iso`),
jamais lue ici via `datetime.now()` — cette valeur sera injectee depuis
`shared/clock.py` par la couche application (Lot M3)."""
from __future__ import annotations

from omega_scan.domain.targets.models import PinnedTarget, Target


def pin_target(target: Target, now_iso: str, note: str | None = None) -> PinnedTarget:
    """Epingle une cible comme autorisee, avec la date de confirmation."""
    return PinnedTarget(
        normalized_host=target.normalized_host,
        authorized=True,
        pinned_at=now_iso,
        note=note,
    )


def is_authorized(pinned_targets: list[PinnedTarget], target: Target) -> bool:
    """Vrai si la cible est deja epinglee et autorisee."""
    return any(
        p.normalized_host == target.normalized_host and p.authorized
        for p in pinned_targets
    )
