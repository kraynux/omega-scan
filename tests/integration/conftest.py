# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Fixtures partagees par les tests d'integration."""
from __future__ import annotations

import pytest

from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding
from omega_scan.domain.scans.models import ScanRun, Summary
from omega_scan.domain.targets.models import Target


@pytest.fixture
def sample_scan_run() -> ScanRun:
    """Un ScanRun minimal mais complet, utilisable par les tests de
    persistance et d'export sans lancer de scan reel."""
    target = Target(
        input_raw="example.org",
        normalized_host="example.org",
        normalized_url_http="http://example.org/",
        normalized_url_https="https://example.org/",
        requested_scheme=None,
        requested_port=None,
        requested_path="/",
        target_kind="hostname",
        scope_kind="hostname",
        scan_modes="both",
        is_ip=False,
        ip_version=None,
        is_private=False,
        is_loopback=False,
        is_link_local=False,
        is_global=False,
    )

    finding = Finding(
        finding_id="f-test0001",
        rule_id="HDR-NOSNIFF-001",
        category="headers",
        title="X-Content-Type-Options absent",
        status="WARN",
        severity="low",
        confidence="high",
        applicability="applicable",
        description="Le header X-Content-Type-Options est absent.",
        impact="Risque mineur de MIME-sniffing.",
        remediation="Ajouter X-Content-Type-Options: nosniff.",
        evidence=Evidence(type="header", value="absent", source="response.headers"),
        location={"path": "/"},
    )

    summary = Summary(
        scan_status="completed",
        checks_total=2,
        findings_total=1,
        status_breakdown={"OK": 1, "WARN": 1, "FAIL": 0, "N/A": 0},
        severity_breakdown={"info": 0, "low": 1, "medium": 0, "high": 0, "critical": 0},
        category_breakdown={"headers": 1},
        top_issues=["X-Content-Type-Options absent"],
        overall_rating="B",
        short_message="Posture correcte, quelques ameliorations recommandees.",
    )

    return ScanRun(
        meta={
            "scan_id": "scan-test0001",
            "scanner_name": "Omega-scan",
            "scanner_version": "0.1.0",
            "started_at": "2026-08-26T10:00:00Z",
            "finished_at": "2026-08-26T10:00:01Z",
            "duration_ms": 1000,
            "host_machine": "test-host",
            "operator_mode": "interactif",
            "export_targets": ["json"],
        },
        target=target,
        scan_profile={"profile_name": "quick"},
        connectivity={
            "dns_resolution_attempted": False,
            "resolved_addresses": [],
            "preferred_address": None,
            "http_reachable": True,
            "https_reachable": False,
            "ports_tested": [80],
            "reachable_ports": [80],
            "first_successful_scheme": "http",
            "latency_overview_ms": 10,
            "connection_notes": "",
            "failure_category": None,
        },
        http={},
        tls={"attempted": False},
        findings=[finding],
        summary=summary,
        errors=[],
    )
