# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation par dispatch du port ReportExporter."""
from __future__ import annotations

from pathlib import Path

from omega_scan.core.enums import ExportFormat
from omega_scan.domain.scans.models import ScanRun
from omega_scan.domain.theme.policies import DEFAULT_EXPORT_THEME
from omega_scan.infrastructure.exporters.html_exporter import export_html
from omega_scan.infrastructure.exporters.json_exporter import export_json
from omega_scan.infrastructure.exporters.text_exporter import export_text


class DefaultReportExporter:
    """Implemente ports/report_exporter.py::ReportExporter en dispatchant
    vers json_exporter/text_exporter/html_exporter selon `export_format`.
    `export_theme` n'est consomme que par export_html (seul format teinte)."""

    def export(
        self,
        run: ScanRun,
        output_path: Path,
        *,
        export_format: ExportFormat,
        export_theme: str = DEFAULT_EXPORT_THEME,
    ) -> Path:
        if export_format is ExportFormat.HTML:
            return export_html(run, output_path, export_theme=export_theme)
        if export_format is ExportFormat.TEXT:
            return export_text(run, output_path)
        return export_json(run, output_path)
