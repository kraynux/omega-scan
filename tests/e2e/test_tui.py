# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests e2e du TUI Textual — seul niveau ou interfaces/tui/ est exerce de
bout en bout (ARCHITECTURE.md §9). Utilise un vrai DependencyContainer
(app.bootstrap.bootstrap sur un var_dir temporaire), pas un container fake :
c'est le cablage complet (SQLite reel, probers httpx reels) qui est verifie
ici, contrairement a tests/unit/application/ (fakes) ou tests/e2e/test_cli.py."""
from __future__ import annotations

import asyncio
from collections.abc import Iterator
from pathlib import Path

import pytest
from pytest_httpserver import HTTPServer

from omega_scan.app.bootstrap import Application, bootstrap
from omega_scan.interfaces.tui.app import OmegaScanApp
from omega_scan.interfaces.tui.screens.findings import FindingsScreen
from omega_scan.interfaces.tui.screens.history import HistoryScreen
from omega_scan.interfaces.tui.screens.scan_setup import ScanSetupScreen
from omega_scan.interfaces.tui.screens.targets import TargetsScreen


@pytest.fixture
def application(tmp_path: Path) -> Iterator[Application]:
    app = bootstrap(var_dir=tmp_path)
    yield app
    app.lifecycle.shutdown()


@pytest.mark.asyncio
async def test_startup_reaches_home_screen(application: Application) -> None:
    app = OmegaScanApp(application.container)
    async with app.run_test() as pilot:
        await pilot.press("space")  # ferme le splash (aucune temporisation, retour reel)
        await pilot.pause(0.2)
        assert type(app.screen).__name__ == "HomeScreen"


@pytest.mark.asyncio
async def test_navigate_to_scan_setup_and_back(application: Application) -> None:
    app = OmegaScanApp(application.container)
    async with app.run_test() as pilot:
        await pilot.press("space")  # ferme le splash (aucune temporisation, retour reel)
        await pilot.pause(0.2)
        await pilot.click("#scan")
        await pilot.pause(0.2)
        assert isinstance(app.screen, ScanSetupScreen)
        await pilot.press("escape")
        await pilot.pause(0.2)
        assert type(app.screen).__name__ == "HomeScreen"


@pytest.mark.asyncio
async def test_pin_target_then_visible_in_list(application: Application) -> None:
    app = OmegaScanApp(application.container)
    async with app.run_test() as pilot:
        from textual.widgets import Input

        await pilot.press("space")  # ferme le splash (aucune temporisation, retour reel)
        await pilot.pause(0.2)
        await pilot.click("#targets")
        await pilot.pause(0.2)
        assert isinstance(app.screen, TargetsScreen)
        app.screen.query_one("#host-input", Input).value = "example.org"
        await pilot.click("#pin")
        await pilot.pause(0.2)
        pinned = application.container.target_repository.list_pinned()
        assert any(p.normalized_host == "example.org" for p in pinned)


@pytest.mark.asyncio
async def test_full_scan_flow_reaches_findings_and_exports(
    application: Application, httpserver: HTTPServer, tmp_path: Path
) -> None:
    httpserver.expect_request("/").respond_with_data("hello", content_type="text/plain")
    app = OmegaScanApp(application.container)

    # Taille genereuse (pas la 80x24 par defaut de run_test()) : l'ecran de
    # saisie de scan s'est etoffe (selecteur de cibles epinglees/recentes,
    # retours utilisateur §10.5) et ne tient plus dans un tres petit terminal.
    async with app.run_test(size=(120, 50)) as pilot:
        from textual.widgets import Checkbox, Input, Select

        await pilot.press("space")  # ferme le splash (aucune temporisation, retour reel)
        await pilot.pause(0.2)
        await pilot.click("#scan")
        await pilot.pause(0.2)
        setup = app.screen
        assert isinstance(setup, ScanSetupScreen)
        setup.query_one("#target-input", Input).value = f"localhost:{httpserver.port}"
        setup.query_one("#profile-select", Select).value = "quick"
        setup.query_one("#authorization-checkbox", Checkbox).value = True
        await pilot.click("#launch")

        for _ in range(20):
            await asyncio.sleep(0.5)
            if isinstance(app.screen, FindingsScreen):
                break
        assert isinstance(app.screen, FindingsScreen)
        assert app.screen._scan.normalized_host == "localhost"

        await pilot.click("#export")
        await pilot.pause(0.3)
        output = tmp_path / "export-test.json"
        app.screen.query_one("#path-input", Input).value = str(output)
        await pilot.click("#confirm-export")
        await pilot.pause(0.3)
        assert output.exists()

        await pilot.press("escape")
        await pilot.press("escape")
        await pilot.pause(0.2)
        await pilot.click("#history")
        await pilot.pause(0.2)
        assert isinstance(app.screen, HistoryScreen)
