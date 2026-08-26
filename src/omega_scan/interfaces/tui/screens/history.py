# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran Historique : liste des scans passes, detail, comparaison, relecture."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Input, Static

from omega_scan.application.queries.get_scan_details import get_scan_details
from omega_scan.application.queries.list_scan_history import list_scan_history
from omega_scan.interfaces.tui.screens._base import OmegaScreen
from omega_scan.interfaces.tui.screens.compare import CompareScreen
from omega_scan.interfaces.tui.screens.findings import FindingsScreen
from omega_scan.interfaces.tui.widgets.history_table import HistoryTable

if TYPE_CHECKING:
    from omega_scan.app.dependency_container import DependencyContainer


class HistoryScreen(OmegaScreen):
    """Liste filtrable par hote. Une comparaison se fait en deux temps :
    marquer une ligne comme reference, puis comparer une autre ligne avec
    elle — pas de selection multiple native au DataTable de Textual."""

    def __init__(self, *, container: DependencyContainer) -> None:
        super().__init__()
        self._container = container
        self._selected_scan_id: str | None = None
        self._reference_scan_id: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="omega-panel"):
            yield Static("HISTORIQUE", classes="omega-title")
            yield Input(placeholder="Filtrer par hote...", id="host-filter")
            yield HistoryTable(id="history-table")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button("Voir le detail", id="view")
                with Container(classes="omega-btn-frame"):
                    yield Button("Marquer comme reference", id="mark-reference")
                with Container(classes="omega-btn-frame"):
                    yield Button("Comparer avec la reference", id="compare")
                with Container(classes="omega-btn-frame"):
                    yield Button("Rejouer", id="replay")
                with Container(classes="omega-btn-frame"):
                    yield Button("Retour", id="back")
        yield Footer()

    def on_mount(self) -> None:
        self._refresh(None)

    def _refresh(self, host_filter: str | None) -> None:
        scans = list_scan_history(
            scan_repository=self._container.scan_repository,
            normalized_host=host_filter or None,
            limit=100,
        )
        self.query_one(HistoryTable).set_scans(scans)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "host-filter":
            self._refresh(event.value.strip())

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        # Entree/clic sur une ligne (DataTable.RowSelected) ouvre DIRECTEMENT
        # le detail (retours utilisateur §10.1 : "un clic sur l'historique
        # doit permettre de ressortir le diagnostic"), plutot que de se
        # contenter de memoriser la selection — le bouton "Voir le detail"
        # reste disponible pour qui prefere le clavier pur (Tab + Entree).
        self._selected_scan_id = str(event.row_key.value)
        self._push_details(self._selected_scan_id)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if self._selected_scan_id is None:
            self.app.notify("Selectionnez d'abord une ligne.", severity="warning")
            return

        if event.button.id == "view":
            self._push_details(self._selected_scan_id)
        elif event.button.id == "mark-reference":
            self._reference_scan_id = self._selected_scan_id
            self.app.notify(f"Reference : {self._reference_scan_id}")
        elif event.button.id == "compare":
            if self._reference_scan_id is None:
                self.app.notify("Marquez d'abord une reference.", severity="warning")
                return
            self.app.push_screen(
                CompareScreen(
                    container=self._container,
                    previous_scan_id=self._reference_scan_id,
                    current_scan_id=self._selected_scan_id,
                )
            )
        elif event.button.id == "replay":
            self._replay(self._selected_scan_id)

    def _push_details(self, scan_id: str) -> None:
        scan = get_scan_details(scan_repository=self._container.scan_repository, scan_id=scan_id)
        if scan is None:
            self.app.notify("Scan introuvable.", severity="error")
            return
        self.app.push_screen(FindingsScreen(container=self._container, scan=scan))

    def _replay(self, scan_id: str) -> None:
        from omega_scan.interfaces.tui.screens.scan_progress import ScanProgressScreen

        # Rejouer un scan deja connu vaut confirmation explicite (l'utilisateur
        # cible sciemment un hote deja scanne) : authorization_confirmed=True.
        # replay_scan() retrouve lui-meme la cible/le profil via scan_id.
        self.app.push_screen(
            ScanProgressScreen(
                container=self._container,
                replay_scan_id=scan_id,
                authorization_confirmed=True,
            )
        )
