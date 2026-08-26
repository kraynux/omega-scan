# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.findings.builders import build_finding
from omega_scan.domain.reports.comparison import compare_scans
from omega_scan.domain.reports.service import calculate_summary
from omega_scan.domain.scans.models import ScanRun, Summary
from omega_scan.domain.targets.validation import parse_target


def _finding(rule_id, status="WARN", severity="medium", path=None):
    return build_finding(
        rule_id=rule_id,
        category="headers",
        title=rule_id,
        status=status,
        severity=severity,
        confidence="certain",
        applicability="applicable",
        description="d",
        impact="i",
        remediation="r",
        location={"path": path} if path else None,
    )


def test_calculate_summary_no_findings_is_grade_a():
    findings = [_finding("HDR-NOSNIFF-001", status="OK", severity="info")]
    summary = calculate_summary(findings, "completed")
    assert summary.overall_rating == "A"
    assert summary.findings_total == 0


def test_calculate_summary_many_findings_is_grade_f():
    findings = [_finding(f"HDR-X-{i:03d}") for i in range(11)]
    summary = calculate_summary(findings, "completed")
    assert summary.overall_rating == "F"
    assert summary.findings_total == 11


def test_calculate_summary_top_issues_prioritizes_high_severity():
    findings = [_finding("HDR-CRIT-001", severity="critical"), _finding("HDR-LOW-001", severity="low")]
    summary = calculate_summary(findings, "completed")
    assert "HDR-CRIT-001" in summary.top_issues


def _make_run(findings):
    target = parse_target("example.org")
    return ScanRun(
        meta={"scan_id": "scan-x"},
        target=target,
        scan_profile={},
        connectivity={},
        http={},
        tls={},
        findings=findings,
        summary=Summary(
            scan_status="completed", checks_total=len(findings), findings_total=len(findings),
            status_breakdown={}, severity_breakdown={}, category_breakdown={}, top_issues=[],
            overall_rating="A", short_message="",
        ),
        errors=[],
    )


def test_compare_scans_detects_new_and_resolved_findings():
    previous = _make_run([_finding("HDR-SERVER-001")])
    current = _make_run([_finding("HDR-CSP-001")])
    comparison = compare_scans(previous, current)
    assert [f.rule_id for f in comparison.new_findings] == ["HDR-CSP-001"]
    assert [f.rule_id for f in comparison.resolved_findings] == ["HDR-SERVER-001"]
    assert comparison.unchanged_findings == []
    assert comparison.changed_findings == []


def test_compare_scans_detects_unchanged_and_changed_status():
    previous = _make_run([_finding("HDR-SERVER-001", status="WARN"), _finding("HDR-CSP-001", status="FAIL")])
    current = _make_run([_finding("HDR-SERVER-001", status="WARN"), _finding("HDR-CSP-001", status="OK")])
    comparison = compare_scans(previous, current)
    assert [f.rule_id for f in comparison.unchanged_findings] == ["HDR-SERVER-001"]
    assert len(comparison.changed_findings) == 1
    old, new = comparison.changed_findings[0]
    assert old.status == "FAIL" and new.status == "OK"


def test_compare_scans_groups_same_rule_by_distinct_path():
    previous = _make_run([_finding("EXR-SENSITIVE-001", path="/.env")])
    current = _make_run([_finding("EXR-SENSITIVE-001", path="/.env"), _finding("EXR-SENSITIVE-001", path="/config.php")])
    comparison = compare_scans(previous, current)
    assert len(comparison.new_findings) == 1
    assert comparison.new_findings[0].location["path"] == "/config.php"
    assert len(comparison.unchanged_findings) == 1
