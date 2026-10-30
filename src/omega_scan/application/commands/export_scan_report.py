# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : exporter un scan deja persiste vers un format concret."""
from __future__ import annotations

from pathlib import Path

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME

from omega_scan.core.enums import ExportFormat
from omega_scan.core.results import Err, Ok, Result
from omega_scan.domain.scans.exceptions import ScanNotFoundError
from omega_scan.ports.report_exporter import ReportExporter
from omega_scan.ports.scan_repository import ScanRepository
from omega_scan.shared.i18n import _


def export_scan_report(
    *,
    scan_repository: ScanRepository,
    report_exporter: ReportExporter,
    scan_id: str,
    output_path: Path,
    export_format: ExportFormat,
    export_theme: str = DEFAULT_EXPORT_THEME,
) -> Result[Path, ScanNotFoundError]:
    """Recupere le ScanRun complet (pas seulement son resume) et delegue le
    format concret au port report_exporter (ARCHITECTURE.md §4, Exports).
    `export_theme` n'a d'effet que sur le format HTML."""
    run = scan_repository.get(scan_id)
    if run is None:
        return Err(ScanNotFoundError(_("Aucun scan trouvé pour l'identifiant {scan_id!r}.").format(scan_id=scan_id)))

    output = report_exporter.export(
        run, output_path, export_format=export_format, export_theme=export_theme
    )
    return Ok(output)
