# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests d'integration des exporteurs JSON/texte/HTML, sur disque reel."""
from __future__ import annotations

import json
from pathlib import Path

from omega_scan.core.enums import ExportFormat
from omega_scan.infrastructure.exporters.exporter import DefaultReportExporter
from omega_scan.infrastructure.exporters.html_exporter import export_html
from omega_scan.infrastructure.exporters.json_exporter import export_json
from omega_scan.infrastructure.exporters.text_exporter import export_text


def test_export_json_writes_valid_serializable_json(tmp_path: Path, sample_scan_run):
    output_path = export_json(sample_scan_run, tmp_path / "scan.json")

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["meta"]["scan_id"] == "scan-test0001"
    assert data["target"]["normalized_host"] == "example.org"
    assert data["findings"][0]["rule_id"] == "HDR-NOSNIFF-001"


def test_export_text_writes_readable_report(tmp_path: Path, sample_scan_run):
    output_path = export_text(sample_scan_run, tmp_path / "scan.txt")

    content = output_path.read_text(encoding="utf-8")
    assert "OMEGA-SCAN" in content
    assert "example.org" in content
    assert "HDR-NOSNIFF-001" in content


def test_export_html_writes_valid_html_report(tmp_path: Path, sample_scan_run):
    output_path = export_html(sample_scan_run, tmp_path / "scan.html")

    content = output_path.read_text(encoding="utf-8")
    assert content.startswith("<!DOCTYPE html>")
    assert "example.org" in content
    assert "HDR-NOSNIFF-001" in content


def test_default_report_exporter_dispatches_on_format(tmp_path: Path, sample_scan_run):
    exporter = DefaultReportExporter()

    json_path = exporter.export(sample_scan_run, tmp_path / "scan.json", export_format=ExportFormat.JSON)
    html_path = exporter.export(sample_scan_run, tmp_path / "scan.html", export_format=ExportFormat.HTML)

    assert json_path.suffix == ".json"
    assert html_path.read_text(encoding="utf-8").startswith("<!DOCTYPE html>")
