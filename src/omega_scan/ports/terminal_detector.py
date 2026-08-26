# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat de detection des signaux bruts du terminal."""
from __future__ import annotations

from typing import Protocol

from omega_scan.domain.terminal.models import TerminalSignals


class TerminalDetector(Protocol):
    """Port consomme par application/queries/detect_terminal.py,
    implemente par infrastructure/terminal/detector.py."""

    def detect(self) -> TerminalSignals: ...
