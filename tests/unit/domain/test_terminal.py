# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.core.enums import RenderProfile
from omega_scan.domain.terminal.models import TerminalSignals
from omega_scan.domain.terminal.service import resolve_render_profile


def test_ghostty_large_terminal_is_complete():
    profile = resolve_render_profile(TerminalSignals(family="ghostty", columns=140, rows=40))
    assert profile.render_profile == RenderProfile.COMPLETE


def test_ghostty_small_terminal_degrades_below_family_ceiling():
    profile = resolve_render_profile(TerminalSignals(family="ghostty", columns=70, rows=20))
    assert profile.render_profile == RenderProfile.MONO


def test_unknown_family_defaults_to_reduced():
    profile = resolve_render_profile(TerminalSignals(family="some-unknown-terminal", columns=140, rows=40))
    assert profile.render_profile == RenderProfile.REDUCED


def test_linux_tty_is_always_mono():
    profile = resolve_render_profile(TerminalSignals(family="linux-tty", columns=200, rows=60))
    assert profile.render_profile == RenderProfile.MONO
