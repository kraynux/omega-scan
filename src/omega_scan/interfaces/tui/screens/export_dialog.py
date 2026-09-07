# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran d'export : choix du format et du chemin de destination."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME, EXPORT_PALETTES
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Select, Static

from omega_scan.application.commands.export_scan_report import export_scan_report
from omega_scan.core.enums import ExportFormat
from omega_scan.core.results import Err
from omega_scan.interfaces.tui.screens._base import OmegaScreen

if TYPE_CHECKING:
    from omega_scan.app.dependency_container import DependencyContainer


class ExportDialogScreen(OmegaScreen):
    """Exporte un scan deja termine vers JSON/texte/HTML."""

    def __init__(self, *, container: DependencyContainer, scan_id: str) -> None:
        super().__init__()
        self._container = container
        self._scan_id = scan_id

    def compose(self) -> ComposeResult:
        default_format = next(iter(ExportFormat))
        yield Header()
        with Vertical(classes="omega-form-panel"):
            yield Static("EXPORTER LE SCAN", classes="omega-title")
            yield Static("Format", classes="omega-subtitle")
            yield Select(
                [(f.value, f.value) for f in ExportFormat],
                value=default_format.value,
                id="format-select",
            )
            yield Static("Theme d'export (HTML uniquement)", classes="omega-subtitle")
            yield Select(
                [(name, name) for name in EXPORT_PALETTES],
                value=DEFAULT_EXPORT_THEME,
                id="theme-select",
            )
            exports_dir = self._container.settings_store.get(
                "exports_dir_override", str(self._container.default_exports_dir)
            ) or str(self._container.default_exports_dir)
            default_path = Path(exports_dir) / f"{self._scan_id}.{default_format.value}"
            yield Input(value=str(default_path), id="path-input")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button("Exporter", id="confirm-export", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button("Retour", id="back")
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id != "format-select":
            return
        path_input = self.query_one("#path-input", Input)
        current = Path(path_input.value)
        path_input.value = str(current.with_suffix(f".{event.value}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if event.button.id != "confirm-export":
            return
        format_select = self.query_one("#format-select", Select)
        theme_select = self.query_one("#theme-select", Select)
        output_path = Path(self.query_one("#path-input", Input).value)
        result = export_scan_report(
            scan_repository=self._container.scan_repository,
            report_exporter=self._container.report_exporter,
            scan_id=self._scan_id,
            output_path=output_path,
            export_format=ExportFormat(format_select.value),
            export_theme=str(theme_select.value),
        )
        if isinstance(result, Err):
            self.app.notify(str(result.error), title="Export impossible", severity="error")
            return
        self.app.notify(f"Ecrit vers {result.value}", title="Export reussi")
        self.dismiss()
