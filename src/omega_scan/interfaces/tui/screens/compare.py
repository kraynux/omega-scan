# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran de comparaison entre deux scans d'une meme cible."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Static

from omega_scan.application.queries.compare_scans import compare_scans
from omega_scan.core.results import Err
from omega_scan.interfaces.tui.screens._base import OmegaScreen

if TYPE_CHECKING:
    from omega_scan.app.dependency_container import DependencyContainer


class CompareScreen(OmegaScreen):
    """Affiche le resultat de compare_scans() : nouveaux / resolus /
    inchanges / changes, en listes categorisees simples."""

    def __init__(
        self, *, container: DependencyContainer, previous_scan_id: str, current_scan_id: str
    ) -> None:
        super().__init__()
        self._container = container
        self._previous_scan_id = previous_scan_id
        self._current_scan_id = current_scan_id

    def compose(self) -> ComposeResult:
        yield Header()
        result = compare_scans(
            scan_repository=self._container.scan_repository,
            previous_scan_id=self._previous_scan_id,
            current_scan_id=self._current_scan_id,
        )
        with VerticalScroll(classes="omega-panel"):
            yield Static("COMPARAISON", classes="omega-title")
            if isinstance(result, Err):
                yield Static(str(result.error), classes="omega-subtitle")
            else:
                comparison = result.value
                yield from self._section("Nouveaux findings", comparison.new_findings)
                yield from self._section("Findings resolus", comparison.resolved_findings)
                yield from self._section("Findings inchanges", comparison.unchanged_findings)
                with Vertical():
                    yield Static("Findings changes", classes="omega-subtitle")
                    if not comparison.changed_findings:
                        yield Static("(aucun)")
                    for changed in comparison.changed_findings:
                        yield Static(
                            f"{changed.previous.rule_id} : "
                            f"{changed.previous.status} -> {changed.current.status}"
                        )
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button("Retour", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()

    def _section(self, title: str, findings: tuple[object, ...]) -> ComposeResult:
        with Vertical():
            yield Static(title, classes="omega-subtitle")
            if not findings:
                yield Static("(aucun)")
            for finding in findings:
                yield Static(f"{finding.rule_id} — {finding.title}")  # type: ignore[attr-defined]
