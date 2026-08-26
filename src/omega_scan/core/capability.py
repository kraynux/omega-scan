# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Modele generique de capacite (ARCHITECTURE.md §4, chaine Capacite terminal).

Contrairement a omega-stress, une seule source de sondage existe ici
(le terminal) : pas de core/capability_registry.py, domain/terminal/service.py
consomme directement l'instance produite par infrastructure/terminal/."""
from __future__ import annotations

from dataclasses import dataclass

from omega_scan.core.enums import CapabilityStatus


@dataclass(frozen=True, slots=True)
class Capability:
    """Etat consolide d'une capacite (ex. "terminal.color_depth")."""

    name: str
    status: CapabilityStatus
    detail: str = ""

    @property
    def is_usable(self) -> bool:
        """Une capacite MISSING ou DISQUALIFIED n'est jamais utilisable,
        DEGRADED reste utilisable avec restriction."""
        return self.status in (CapabilityStatus.AVAILABLE, CapabilityStatus.DEGRADED)
