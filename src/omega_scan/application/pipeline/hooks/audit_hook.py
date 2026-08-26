# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Hook : construit et emet les evenements d'audit d'un scan (ARCHITECTURE.md §7)."""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from omega_scan.core.audit import AuditEvent
from omega_scan.domain.scans.models import ScanRun
from omega_scan.domain.targets.models import Target

AuditSink = Callable[[AuditEvent], None]
"""Destination d'un evenement d'audit, fournie par l'appelant
(infrastructure/logging/audit_logger.py::record en production, un fake en
test) — local a ce module, pas promu en shared/typing.py tant qu'un seul
fichier le consomme."""


def emit_scan_started(target: Target, *, sink: AuditSink, occurred_at: datetime) -> None:
    sink(
        AuditEvent(
            action="scan_started",
            outcome="ok",
            authorized=True,
            occurred_at=occurred_at,
            detail=f"target={target.normalized_host}",
        )
    )


def emit_scan_finished(run: ScanRun, *, sink: AuditSink, occurred_at: datetime) -> None:
    sink(
        AuditEvent(
            action="scan_finished",
            outcome=run.summary.scan_status,
            authorized=True,
            occurred_at=occurred_at,
            detail=f"scan={run.meta['scan_id']} target={run.target.normalized_host}",
        )
    )


def emit_authorization_denied(target: Target, *, sink: AuditSink, occurred_at: datetime) -> None:
    sink(
        AuditEvent(
            action="scan_denied",
            outcome="unauthorized",
            authorized=False,
            occurred_at=occurred_at,
            detail=f"target={target.normalized_host}",
        )
    )
