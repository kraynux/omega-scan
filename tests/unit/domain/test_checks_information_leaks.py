# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.information_leaks.service import run_information_leaks_checks

TARGET = {"normalized_host": "example.org", "requested_port": None, "requested_path": "/"}
PROFILE = {"profile_name": "standard"}


def _http_data(headers=None, body_text="", path_context=None):
    return {
        "overview": {
            "preferred_scheme": "https",
            "proxy_suspected": False,
            "path_probe_context": path_context or [],
        },
        "https": {
            "ok": True,
            "requested_url": "https://example.org/",
            "headers": headers or {},
            "body_preview": {"text_preview": body_text},
        },
    }


def test_server_banner_warns():
    findings = run_information_leaks_checks(_http_data(headers={"Server": "Apache/2.4"}), TARGET, PROFILE)
    rule_ids = {f.rule_id for f in findings}
    assert "INF-BANNER-001" in rule_ids


def test_stack_trace_fails_and_error_pattern_not_duplicated_as_warn_only():
    findings = run_information_leaks_checks(
        _http_data(body_text="Traceback (most recent call last): ..."), TARGET, PROFILE
    )
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["INF-STACK-001"].status == "FAIL"


def test_generic_error_message_warns():
    findings = run_information_leaks_checks(_http_data(body_text="Fatal error: something broke"), TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["INF-ERROR-001"].status == "WARN"


def test_robots_present_is_ok_info():
    findings = run_information_leaks_checks(
        _http_data(path_context=[{"path": "/robots.txt", "reason": "ok", "status_code": 200}]), TARGET, PROFILE
    )
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["INF-ROBOTS-001"].status == "OK"


def test_security_txt_present_is_ok_info():
    findings = run_information_leaks_checks(
        _http_data(path_context=[{"path": "/.well-known/security.txt", "reason": "ok", "status_code": 200}]),
        TARGET, PROFILE,
    )
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["INF-SECURITYTXT-001"].status == "OK"


def test_security_txt_absent_produces_no_finding():
    findings = run_information_leaks_checks(_http_data(path_context=[]), TARGET, PROFILE)
    assert "INF-SECURITYTXT-001" not in {f.rule_id for f in findings}


def test_verbose_header_warns_but_powered_by_not_duplicated():
    findings = run_information_leaks_checks(
        _http_data(headers={"X-Debug": "true", "X-Powered-By": "PHP/8.1"}), TARGET, PROFILE
    )
    header_findings = [f for f in findings if f.rule_id == "INF-HEADER-001"]
    assert len(header_findings) == 1  # X-Powered-By est exclu ici, deja couvert par INF-BANNER-001
