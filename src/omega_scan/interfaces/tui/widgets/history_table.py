# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tableau de l'historique des scans."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import DataTable

from omega_scan.shared.i18n import _

if TYPE_CHECKING:
    from omega_scan.application.dto.scan_dto import ScanSummaryDTO


class HistoryTable(DataTable[str]):
    """Une ligne par scan passe, la plus recente en premier."""

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns(_("Cible"), _("Date"), _("Statut"), _("Note"), _("Findings"))

    def set_scans(self, scans: tuple[ScanSummaryDTO, ...]) -> None:
        self.clear()
        for scan in scans:
            self.add_row(
                scan.normalized_host,
                scan.started_at,
                scan.scan_status,
                scan.overall_rating,
                str(scan.findings_total),
                key=scan.scan_id,
            )
