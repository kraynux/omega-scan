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
from omega_scan.shared.i18n import _

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
            yield Static(_("COMPARAISON"), classes="omega-title")
            if isinstance(result, Err):
                yield Static(str(result.error), classes="omega-subtitle")
            else:
                comparison = result.value
                yield from self._section(_("Nouveaux findings"), comparison.new_findings)
                yield from self._section(_("Findings résolus"), comparison.resolved_findings)
                yield from self._section(_("Findings inchangés"), comparison.unchanged_findings)
                with Vertical():
                    yield Static(_("Findings changés"), classes="omega-subtitle")
                    if not comparison.changed_findings:
                        yield Static("(aucun)")
                    for changed in comparison.changed_findings:
                        yield Static(
                            _("{rule_id} : {status} -> {status2}").format(rule_id=changed.previous.rule_id, status=changed.previous.status, status2=changed.current.status)
                        )
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
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
                yield Static(_("{rule_id} — {title}").format(rule_id=finding.rule_id, title=finding.title))  # type: ignore[attr-defined]
