# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation concrete du port TerminalDetector."""
from __future__ import annotations

from omega_scan.domain.terminal.models import TerminalSignals
from omega_scan.infrastructure.terminal.fallback_resolver import resolve_family
from omega_scan.infrastructure.terminal.raw_capabilities import read_raw_signals


class SystemTerminalDetector:
    """Implemente ports/terminal_detector.py::TerminalDetector. Nommee
    SystemTerminalDetector (pas TerminalDetector) pour ne pas porter le
    meme nom que le Protocol qu'elle implemente."""

    def detect(self) -> TerminalSignals:
        raw = read_raw_signals()
        return TerminalSignals(
            family=resolve_family(raw),
            columns=raw.columns,
            rows=raw.rows,
            is_ssh=raw.is_ssh,
        )
