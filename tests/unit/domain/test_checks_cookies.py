# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.cookies.service import run_cookies_checks

TARGET = {"normalized_host": "example.org", "requested_port": None, "requested_path": "/"}
PROFILE = {"profile_name": "standard"}


def _http_data(https_cookies=None, http_cookies=None, https_ok=True, http_ok=False):
    return {
        "overview": {"preferred_scheme": "https", "proxy_suspected": False},
        "https": {"ok": https_ok, "cookies": https_cookies or []},
        "http": {"ok": http_ok, "cookies": http_cookies or []},
    }


def _cookie(**overrides):
    base = {
        "name": "session",
        "value": "abc",
        "domain": "example.org",
        "path": "/",
        "secure": True,
        "httponly": True,
        "samesite": "Lax",
    }
    base.update(overrides)
    return base


def test_no_cookies_produces_no_findings():
    assert run_cookies_checks(_http_data(), TARGET, PROFILE) == []


def test_fully_compliant_cookie_produces_no_findings():
    http_data = _http_data(https_cookies=[_cookie()])
    assert run_cookies_checks(http_data, TARGET, PROFILE) == []


def test_https_cookie_without_secure_warns():
    http_data = _http_data(https_cookies=[_cookie(secure=False)])
    findings = run_cookies_checks(http_data, TARGET, PROFILE)
    rule_ids = {f.rule_id for f in findings}
    assert "COO-SECURE-001" in rule_ids


def test_cookie_without_httponly_warns():
    http_data = _http_data(https_cookies=[_cookie(httponly=False)])
    findings = run_cookies_checks(http_data, TARGET, PROFILE)
    rule_ids = {f.rule_id for f in findings}
    assert "COO-HTTPONLY-001" in rule_ids


def test_cookie_without_samesite_warns():
    http_data = _http_data(https_cookies=[_cookie(samesite=None)])
    findings = run_cookies_checks(http_data, TARGET, PROFILE)
    rule_ids = {f.rule_id for f in findings}
    assert "COO-SAMESITE-001" in rule_ids


def test_samesite_none_with_secure_is_clean():
    http_data = _http_data(https_cookies=[_cookie(samesite="None", secure=True)])
    findings = run_cookies_checks(http_data, TARGET, PROFILE)
    assert "COO-SAMESITE-001" not in {f.rule_id for f in findings}


def test_samesite_none_without_secure_warns():
    http_data = _http_data(https_cookies=[_cookie(samesite="None", secure=False)])
    findings = run_cookies_checks(http_data, TARGET, PROFILE)
    assert "COO-SAMESITE-001" in {f.rule_id for f in findings}
