# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Query : detecter le terminal courant et resoudre son profil de rendu."""
from __future__ import annotations

from omega_scan.application.dto.mappers import terminal_profile_to_dto
from omega_scan.application.dto.terminal_dto import TerminalProfileDTO
from omega_scan.domain.terminal.service import resolve_render_profile
from omega_scan.ports.terminal_detector import TerminalDetector


def detect_terminal(*, terminal_detector: TerminalDetector) -> TerminalProfileDTO:
    signals = terminal_detector.detect()
    profile = resolve_render_profile(signals)
    return terminal_profile_to_dto(profile)
