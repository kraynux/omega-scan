# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_lib.terminal.models import TerminalSignals

from omega_scan.application.queries.detect_terminal import detect_terminal
from tests.unit.application.conftest import FakeTerminalDetector


def test_detect_terminal_resolves_render_profile():
    dto = detect_terminal(terminal_detector=FakeTerminalDetector())

    assert dto.family == "ghostty"
    assert dto.render_profile == "complete"


def test_detect_terminal_degrades_for_unknown_small_terminal():
    detector = FakeTerminalDetector(TerminalSignals(family="unknown-term", columns=40, rows=10))
    dto = detect_terminal(terminal_detector=detector)

    assert dto.render_profile == "mono"
