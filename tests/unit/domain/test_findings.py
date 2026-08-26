# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.findings.builders import (
    build_finding,
    degrade_confidence_for_catchall,
    degrade_confidence_for_proxy,
)
from omega_scan.domain.findings.evidence import Evidence


def _make_finding(**overrides):
    defaults = {
        "rule_id": "TRN-HTTPS-001",
        "category": "transport",
        "title": "Titre",
        "status": "FAIL",
        "severity": "high",
        "confidence": "certain",
        "applicability": "applicable",
        "description": "desc",
        "impact": "impact",
        "remediation": "remediation",
    }
    defaults.update(overrides)
    return build_finding(**defaults)


def test_build_finding_generates_unique_ids():
    a = _make_finding()
    b = _make_finding()
    assert a.finding_id != b.finding_id
    assert a.finding_id.startswith("f-")


def test_finding_to_dict_serializes_evidence():
    finding = _make_finding(evidence=Evidence(type="header", value="nginx", source="response.headers"))
    data = finding.to_dict()
    assert data["evidence"]["value"] == "nginx"


def test_degrade_confidence_for_proxy_caps_at_medium():
    assert degrade_confidence_for_proxy("certain", True) == "medium"
    assert degrade_confidence_for_proxy("high", True) == "medium"
    assert degrade_confidence_for_proxy("medium", True) == "medium"
    assert degrade_confidence_for_proxy("certain", False) == "certain"


def test_degrade_confidence_for_catchall_caps_at_low():
    assert degrade_confidence_for_catchall("certain", True) == "low"
    assert degrade_confidence_for_catchall("medium", True) == "low"
    assert degrade_confidence_for_catchall("low", True) == "low"
    assert degrade_confidence_for_catchall("certain", False) == "certain"
