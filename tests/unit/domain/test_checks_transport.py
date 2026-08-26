# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.transport.service import run_transport_checks

TARGET = {"normalized_host": "example.org", "requested_port": None, "requested_path": "/", "scope_kind": "public"}
PROFILE_STANDARD = {"profile_name": "standard"}


def test_http_without_https_redirect_warns():
    http_data = {
        "http": {"attempted": True, "ok": True, "final_url": "http://example.org/", "status_code": 200, "requested_url": "http://example.org/"},
        "https": {"attempted": True, "ok": True, "headers": {"Strict-Transport-Security": "max-age=31536000"}, "requested_url": "https://example.org/"},
    }
    findings = run_transport_checks(http_data, TARGET, PROFILE_STANDARD)
    rule_ids = {f.rule_id for f in findings}
    assert "TRN-HTTP-001" in rule_ids


def test_http_redirecting_to_https_is_clean():
    http_data = {
        "http": {"attempted": True, "ok": True, "final_url": "https://example.org/", "status_code": 301, "requested_url": "http://example.org/"},
        "https": {"attempted": True, "ok": True, "headers": {"Strict-Transport-Security": "max-age=31536000"}, "requested_url": "https://example.org/"},
    }
    findings = run_transport_checks(http_data, TARGET, PROFILE_STANDARD)
    rule_ids = {f.rule_id for f in findings}
    assert "TRN-HTTP-001" not in rule_ids


def test_https_unreachable_fails():
    http_data = {
        "http": {"attempted": False},
        "https": {"attempted": True, "ok": False, "error": "connect timeout", "requested_url": "https://example.org/"},
    }
    findings = run_transport_checks(http_data, TARGET, PROFILE_STANDARD)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["TRN-HTTPS-001"].status == "FAIL"


def test_hsts_absent_fails():
    http_data = {
        "http": {"attempted": False},
        "https": {"attempted": True, "ok": True, "headers": {}, "requested_url": "https://example.org/"},
    }
    findings = run_transport_checks(http_data, TARGET, PROFILE_STANDARD)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["TRN-HSTS-001"].status == "FAIL"


def test_hsts_not_applicable_on_local_lab_lan():
    target = {**TARGET, "scope_kind": "private_lan"}
    profile = {"profile_name": "local-lab"}
    http_data = {
        "http": {"attempted": False},
        "https": {"attempted": True, "ok": True, "headers": {}, "requested_url": "https://192.168.1.10/"},
    }
    findings = run_transport_checks(http_data, target, profile)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["TRN-HSTS-001"].status == "N/A"


def test_hsts_short_max_age_warns():
    http_data = {
        "http": {"attempted": False},
        "https": {"attempted": True, "ok": True, "headers": {"Strict-Transport-Security": "max-age=3600"}, "requested_url": "https://example.org/"},
    }
    findings = run_transport_checks(http_data, TARGET, PROFILE_STANDARD)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["TRN-HSTS-002"].status == "WARN"
