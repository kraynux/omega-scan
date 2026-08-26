# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat d'export d'un ScanRun vers un format concret."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol

from omega_scan.core.enums import ExportFormat
from omega_scan.domain.scans.models import ScanRun


class ReportExporter(Protocol):
    """Port consomme par application/commands/export_scan_report.py,
    implemente par infrastructure/exporters/exporter.py — un seul port
    pour les 3 formats (JSON/texte/HTML), pas un port par format : le
    choix de format est un parametre d'appel, pas une variation de
    contrat (contrairement aux 5 probers reseau, qui sont 5 collectes
    independantes, voir ARCHITECTURE.md §0)."""

    def export(
        self,
        run: ScanRun,
        output_path: Path,
        *,
        export_format: ExportFormat,
        export_theme: str = "omega-base",
    ) -> Path: ...
