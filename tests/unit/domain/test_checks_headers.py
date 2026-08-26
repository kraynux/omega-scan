# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.headers.service import run_headers_checks

TARGET = {"normalized_host": "example.org", "requested_port": None, "requested_path": "/"}
PROFILE = {"profile_name": "standard"}


def _http_data(headers, content_profile="html_page"):
    return {
        "overview": {"preferred_scheme": "https", "content_profile": content_profile, "proxy_suspected": False},
        "https": {"ok": True, "requested_url": "https://example.org/", "headers": headers},
    }


def test_csp_missing_on_html_page_fails():
    findings = run_headers_checks(_http_data({}), TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["HDR-CSP-001"].status == "FAIL"


def test_csp_not_applicable_when_not_html():
    findings = run_headers_checks(_http_data({}, content_profile="json_api"), TARGET, PROFILE)
    assert "HDR-CSP-001" not in {f.rule_id for f in findings}


def test_csp_permissive_warns_never_fails():
    findings = run_headers_checks(
        _http_data({"Content-Security-Policy": "default-src *"}), TARGET, PROFILE
    )
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["HDR-CSP-002"].status == "WARN"


def test_nosniff_absent_warns():
    findings = run_headers_checks(_http_data({}), TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["HDR-NOSNIFF-001"].status == "WARN"


def test_server_banner_exposed_warns():
    findings = run_headers_checks(_http_data({"Server": "nginx/1.18.0"}), TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["HDR-SERVER-001"].status == "WARN"
    assert "nginx" in rule_ids["HDR-SERVER-001"].description


def test_cache_control_absent_on_html_warns():
    findings = run_headers_checks(_http_data({}), TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["HDR-CACHE-001"].status == "WARN"


def test_cache_control_no_store_is_clean():
    findings = run_headers_checks(_http_data({"Cache-Control": "no-store"}), TARGET, PROFILE)
    assert "HDR-CACHE-001" not in {f.rule_id for f in findings}


def test_cache_control_public_still_warns():
    findings = run_headers_checks(_http_data({"Cache-Control": "public, max-age=3600"}), TARGET, PROFILE)
    assert "HDR-CACHE-001" in {f.rule_id for f in findings}


def test_cache_control_not_applicable_when_not_html():
    findings = run_headers_checks(_http_data({}, content_profile="json_api"), TARGET, PROFILE)
    assert "HDR-CACHE-001" not in {f.rule_id for f in findings}
