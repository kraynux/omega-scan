# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Forme generique d'un evenement d'audit, independante du support de journalisation.

Construit par application/pipeline/hooks/audit_hook.py a chaque decision
d'autorisation de cible (ARCHITECTURE.md §7), serialise par
infrastructure/logging/audit_logger.py."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Trace d'une action passee par le pipeline : quoi, quand, autorise ou
    non, avec quelle issue.

    occurred_at est fourni par l'appelant (pas de datetime.now() interne) :
    meme discipline d'horloge injectee que domain/scans/service.py, pour
    qu'application/pipeline/hooks/audit_hook.py (Lot M3) reste testable avec
    un temps fixe via shared/clock.py."""

    action: str
    outcome: str
    authorized: bool
    occurred_at: datetime
    detail: str = ""
