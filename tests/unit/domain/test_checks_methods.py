# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.methods.service import run_methods_checks

TARGET = {"normalized_host": "example.org", "requested_port": None, "requested_path": "/"}
PROFILE = {"profile_name": "standard"}
HTTP_DATA = {"overview": {"preferred_scheme": "https", "proxy_suspected": False}}


def test_trace_enabled_warns():
    methods_data = {"methods_tested": [{"method": "TRACE", "reason": "enabled"}]}
    findings = run_methods_checks(methods_data, TARGET, PROFILE, HTTP_DATA)
    assert findings[0].rule_id == "MTH-TRACE-001"
    assert findings[0].status == "WARN"


def test_put_protected_is_not_applicable():
    methods_data = {"methods_tested": [{"method": "PUT", "reason": "protected"}]}
    findings = run_methods_checks(methods_data, TARGET, PROFILE, HTTP_DATA)
    assert findings[0].status == "N/A"


def test_disabled_method_produces_no_finding():
    methods_data = {"methods_tested": [{"method": "DELETE", "reason": "disabled"}]}
    findings = run_methods_checks(methods_data, TARGET, PROFILE, HTTP_DATA)
    assert findings == []


def test_unknown_status_warns_with_low_confidence():
    methods_data = {"methods_tested": [{"method": "PATCH", "reason": "unknown"}]}
    findings = run_methods_checks(methods_data, TARGET, PROFILE, HTTP_DATA)
    assert findings[0].confidence == "low"
    assert findings[0].applicability == "conditional"
