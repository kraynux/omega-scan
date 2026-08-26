# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Transitions de statut d'un scan : fonctions pures, remplacant les methodes
start()/finish()/add_error() de l'ancien ScanContext (qui appelait
datetime.now() directement). L'heure courante est fournie par l'appelant
(shared/clock.py, cable par application/, Lot M3)."""
from __future__ import annotations

from datetime import datetime

from omega_scan.domain.scans.models import ScanError


def compute_duration_ms(started_at_iso: str, finished_at_iso: str) -> int:
    """Duree entre deux horodatages ISO 8601 UTC, en millisecondes."""
    start_dt = datetime.fromisoformat(started_at_iso.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(finished_at_iso.replace("Z", "+00:00"))
    return int((end_dt - start_dt).total_seconds() * 1000)


def has_fatal_error(errors: list[ScanError]) -> bool:
    return any(e.fatal for e in errors)


def compute_scan_status(errors: list[ScanError]) -> str:
    """"completed" si aucune erreur, "failed" si au moins une erreur fatale,
    sinon "completed_with_errors" (memes regles que l'ancien ScanContext.finish())."""
    if not errors:
        return "completed"
    if has_fatal_error(errors):
        return "failed"
    return "completed_with_errors"
