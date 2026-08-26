# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat de persistance des cibles epinglees-autorisees."""
from __future__ import annotations

from typing import Protocol

from omega_scan.domain.targets.models import PinnedTarget


class TargetRepository(Protocol):
    """Port consomme par application/ (pin_target, unpin_target,
    authorization_guard, list_targets), implemente par
    infrastructure/storage/sqlite/target_repository.py."""

    def pin(self, pinned: PinnedTarget) -> None: ...

    def unpin(self, normalized_host: str) -> None: ...

    def get(self, normalized_host: str) -> PinnedTarget | None: ...

    def list_pinned(self) -> tuple[PinnedTarget, ...]: ...

    def clear(self) -> None:
        """Desepingle TOUTES les cibles (ecran Reglages, "Effacer toutes
        les cibles"). Purge complete et irreversible, confirmee cote
        interface avant appel."""
        ...
