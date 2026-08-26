# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecriture des evenements d'audit en JSON structure (une ligne par evenement)."""
from __future__ import annotations

import json
from pathlib import Path

from omega_scan.core.audit import AuditEvent


class AuditLogger:
    """Implemente la forme attendue par application/pipeline/hooks/
    audit_hook.py (Lot M3) : une methode `record`, appelable directement
    comme sink (`audit_logger.record`), sans wrapper supplementaire."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def record(self, event: AuditEvent) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(
            {
                "action": event.action,
                "outcome": event.outcome,
                "authorized": event.authorized,
                "detail": event.detail,
                "occurred_at": event.occurred_at.isoformat(),
            },
            ensure_ascii=False,
        )
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
