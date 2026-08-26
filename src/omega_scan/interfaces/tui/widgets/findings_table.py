# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tableau des findings d'un scan, filtrable par categorie."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import DataTable

if TYPE_CHECKING:
    from omega_scan.application.dto.scan_dto import FindingDTO

_STATUS_ORDER = {"FAIL": 0, "WARN": 1, "N/A": 2, "OK": 3}


class FindingsTable(DataTable[str]):
    """Une ligne par finding, triee FAIL/WARN d'abord (les plus actionnables)."""

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("Categorie", "Regle", "Titre", "Statut", "Severite")

    def set_findings(self, findings: tuple[FindingDTO, ...]) -> None:
        self.clear()
        ordered = sorted(findings, key=lambda f: _STATUS_ORDER.get(f.status, 9))
        for finding in ordered:
            self.add_row(
                finding.category,
                finding.rule_id,
                finding.title,
                finding.status,
                finding.severity,
                key=finding.finding_id,
            )
