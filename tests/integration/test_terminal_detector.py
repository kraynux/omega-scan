# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests d'integration de la detection de terminal, sans terminal reel
(variables d'environnement manipulees via monkeypatch)."""
from __future__ import annotations

import pytest

from omega_scan.infrastructure.terminal.detector import SystemTerminalDetector
from omega_scan.infrastructure.terminal.fallback_resolver import resolve_family
from omega_scan.infrastructure.terminal.raw_capabilities import read_raw_signals


def _clear_terminal_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in (
        "TERM", "TERM_PROGRAM", "COLORTERM", "SSH_CLIENT", "SSH_CONNECTION",
        "TERMINATOR_UUID", "KONSOLE_VERSION", "GNOME_TERMINAL_SCREEN", "GNOME_TERMINAL_SERVICE",
    ):
        monkeypatch.delenv(var, raising=False)


def test_read_raw_signals_reflects_environment(monkeypatch: pytest.MonkeyPatch):
    _clear_terminal_env(monkeypatch)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setenv("TERM_PROGRAM", "ghostty")

    signals = read_raw_signals()

    assert signals.term == "xterm-256color"
    assert signals.term_program == "ghostty"
    assert signals.is_ssh is False


def test_resolve_family_recognizes_ghostty(monkeypatch: pytest.MonkeyPatch):
    _clear_terminal_env(monkeypatch)
    monkeypatch.setenv("TERM_PROGRAM", "ghostty")

    assert resolve_family(read_raw_signals()) == "ghostty"


def test_resolve_family_prioritizes_ssh(monkeypatch: pytest.MonkeyPatch):
    _clear_terminal_env(monkeypatch)
    monkeypatch.setenv("SSH_CLIENT", "1.2.3.4 22 22")
    monkeypatch.setenv("COLORTERM", "truecolor")

    assert resolve_family(read_raw_signals()) == "ssh-modern"


def test_resolve_family_detects_terminator_via_marker(monkeypatch: pytest.MonkeyPatch):
    _clear_terminal_env(monkeypatch)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setenv("TERMINATOR_UUID", "some-uuid")

    assert resolve_family(read_raw_signals()) == "terminator"


def test_system_terminal_detector_produces_terminal_signals(monkeypatch: pytest.MonkeyPatch):
    _clear_terminal_env(monkeypatch)
    monkeypatch.setenv("TERM_PROGRAM", "kitty")

    signals = SystemTerminalDetector().detect()

    assert signals.family == "kitty"
    assert signals.columns > 0
    assert signals.rows > 0
    assert signals.is_ssh is False
