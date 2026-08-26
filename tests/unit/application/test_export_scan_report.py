# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_scan.application.commands.export_scan_report import export_scan_report
from omega_scan.application.commands.run_scan import run_scan
from omega_scan.core.enums import ExportFormat
from omega_scan.core.results import Err, Ok
from omega_scan.domain.scans.exceptions import ScanNotFoundError
from tests.unit.application.conftest import FakeReportExporter


def test_export_scan_report_writes_via_port(target_repository, scan_repository, probers, audit_sink, now_factory, tmp_path):
    scanned = run_scan(
        target_repository=target_repository,
        scan_repository=scan_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        raw_target="example.org",
        profile_name="quick",
        authorization_confirmed=True,
        **probers,
    )
    scan_id = scanned.value.scan_id
    exporter = FakeReportExporter()
    output_path = tmp_path / "report.json"

    result = export_scan_report(
        scan_repository=scan_repository,
        report_exporter=exporter,
        scan_id=scan_id,
        output_path=output_path,
        export_format=ExportFormat.JSON,
    )

    assert isinstance(result, Ok)
    assert result.value == output_path
    assert output_path.exists()
    assert len(exporter.calls) == 1


def test_export_scan_report_unknown_scan(scan_repository, tmp_path):
    result = export_scan_report(
        scan_repository=scan_repository,
        report_exporter=FakeReportExporter(),
        scan_id="scan-does-not-exist",
        output_path=tmp_path / "report.json",
        export_format=ExportFormat.JSON,
    )

    assert isinstance(result, Err)
    assert isinstance(result.error, ScanNotFoundError)
