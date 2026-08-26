# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran de resultats : resume, tableau des findings filtrable, detail, export.

Un seul ecran pour un scan qui vient de tourner ou un scan charge depuis
l'historique (application/queries/get_scan_details.py) : les deux
fournissent le meme ScanRunDTO, pas de duplication d'ecran."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Footer, Header, Select, Static

from omega_scan.interfaces.tui.screens._base import OmegaScreen
from omega_scan.interfaces.tui.screens.export_dialog import ExportDialogScreen
from omega_scan.interfaces.tui.widgets.findings_table import FindingsTable
from omega_scan.interfaces.tui.widgets.grade_badge import GradeBadge

if TYPE_CHECKING:
    from omega_scan.app.dependency_container import DependencyContainer
    from omega_scan.application.dto.scan_dto import FindingDTO, ScanRunDTO

_ALL_CATEGORIES = "*"


class FindingDetailScreen(ModalScreen[None]):
    """Detail d'un finding, en modal par-dessus FindingsScreen."""

    def __init__(self, *, finding: FindingDTO) -> None:
        super().__init__()
        self._finding = finding

    def compose(self) -> ComposeResult:
        finding = self._finding
        with Vertical(classes="omega-panel omega-modal"):
            yield Static(f"{finding.rule_id} — {finding.title}", classes="omega-title")
            yield Static(f"Statut: {finding.status}  Severite: {finding.severity}  Confiance: {finding.confidence}")
            yield Static(finding.description)
            yield Static(f"[b]Impact[/b]\n{finding.impact}")
            yield Static(f"[b]Remediation[/b]\n{finding.remediation}")
            if finding.evidence is not None:
                yield Static(f"[b]Preuve[/b] ({finding.evidence.source})\n{finding.evidence.value}")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button("Fermer", id="close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.dismiss()


class FindingsScreen(OmegaScreen):
    """Resume + tableau des findings d'un ScanRunDTO donne."""

    def __init__(self, *, container: DependencyContainer, scan: ScanRunDTO) -> None:
        super().__init__()
        self._container = container
        self._scan = scan

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="omega-panel"):
            yield Static(f"RESULTATS — {self._scan.normalized_host}", classes="omega-title")
            yield GradeBadge(
                overall_rating=self._scan.summary.overall_rating,
                short_message=self._scan.summary.short_message,
            )
            yield Static(
                "Cliquez sur une ligne (ou Entree) pour le diagnostic detaille de ce finding.",
                classes="omega-hint",
            )
            yield Select(
                [("Toutes categories", _ALL_CATEGORIES)]
                + [(c, c) for c in sorted({f.category for f in self._scan.findings})],
                value=_ALL_CATEGORIES,
                id="category-filter",
            )
            yield FindingsTable(id="findings-table")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button("Exporter", id="export", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button("Retour", id="back")
        yield Footer()

    def on_mount(self) -> None:
        self._refresh_table(_ALL_CATEGORIES)

    def _refresh_table(self, category: str) -> None:
        findings = self._scan.findings
        if category != _ALL_CATEGORIES:
            findings = tuple(f for f in findings if f.category == category)
        self.query_one(FindingsTable).set_findings(findings)

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "category-filter":
            self._refresh_table(str(event.value))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        finding_id = event.row_key.value
        finding = next((f for f in self._scan.findings if f.finding_id == finding_id), None)
        if finding is not None:
            self.app.push_screen(FindingDetailScreen(finding=finding))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "export":
            self.app.push_screen(
                ExportDialogScreen(container=self._container, scan_id=self._scan.scan_id)
            )
        elif event.button.id == "back":
            self.dismiss()
