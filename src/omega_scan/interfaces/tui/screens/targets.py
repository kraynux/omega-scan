# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran Cibles : cibles epinglees-autorisees, epingler/desepingler."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Input, Static

from omega_scan.application.commands.pin_target import pin_target
from omega_scan.application.commands.unpin_target import unpin_target
from omega_scan.application.queries.list_targets import list_targets
from omega_scan.core.results import Err
from omega_scan.interfaces.tui.screens._base import OmegaScreen
from omega_scan.shared.clock import utc_now
from omega_scan.shared.i18n import _

if TYPE_CHECKING:
    from omega_scan.app.dependency_container import DependencyContainer


class TargetsScreen(OmegaScreen):
    """Epingler une cible dispense de recocher la confirmation
    d'autorisation a chaque scan sur cette meme cible (ARCHITECTURE.md §7)."""

    def __init__(self, *, container: DependencyContainer) -> None:
        super().__init__()
        self._container = container
        self._selected_host: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="omega-panel"):
            yield Static(_("CIBLES ÉPINGLÉES"), classes="omega-title")
            table: DataTable[str] = DataTable(id="targets-table")
            table.cursor_type = "row"
            yield table
            yield Input(placeholder=_("Hôte à épingler..."), id="host-input")
            yield Input(placeholder=_("Note (optionnel)"), id="note-input")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Épingler"), id="pin", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Désépingler la sélection"), id="unpin")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#targets-table", DataTable).add_columns(_("Hôte"), _("Épinglé le"), _("Note"))
        self._refresh()

    def _refresh(self) -> None:
        table = self.query_one("#targets-table", DataTable)
        table.clear()
        for target in list_targets(target_repository=self._container.target_repository):
            table.add_row(
                target.normalized_host,
                target.pinned_at,
                target.note or "",
                key=target.normalized_host,
            )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self._selected_host = str(event.row_key.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "pin":
            self._pin()
        elif event.button.id == "unpin":
            self._unpin()
        elif event.button.id == "back":
            self.dismiss()

    def _pin(self) -> None:
        host_input = self.query_one("#host-input", Input)
        note_input = self.query_one("#note-input", Input)
        raw_input = host_input.value.strip()
        if not raw_input:
            self.app.notify(_("Saisissez un hôte."), severity="warning")
            return
        result = pin_target(
            target_repository=self._container.target_repository,
            now=utc_now(),
            raw_input=raw_input,
            note=note_input.value.strip() or None,
        )
        if isinstance(result, Err):
            self.app.notify(str(result.error), title=_("Cible invalide"), severity="error")
            return
        host_input.value = ""
        note_input.value = ""
        self._refresh()

    def _unpin(self) -> None:
        if self._selected_host is None:
            self.app.notify(_("Sélectionnez d'abord une ligne."), severity="warning")
            return
        unpin_target(target_repository=self._container.target_repository, normalized_host=self._selected_host)
        self._selected_host = None
        self._refresh()
