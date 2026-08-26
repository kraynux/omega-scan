# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.cors.service import run_cors_checks

TARGET = {"normalized_host": "example.org", "requested_port": None, "requested_path": "/"}
PROFILE = {"profile_name": "standard"}


def _http_data(cors):
    return {"overview": {"preferred_scheme": "https"}, "cors": cors}


def test_cors_not_attempted_produces_no_findings():
    http_data = _http_data({"attempted": False, "allow_origin": None, "allow_credentials": False, "reflects_arbitrary_origin": False})
    assert run_cors_checks(http_data, TARGET, PROFILE) == []


def test_no_cors_headers_produces_no_findings():
    http_data = _http_data({"attempted": True, "allow_origin": None, "allow_credentials": False, "reflects_arbitrary_origin": False})
    assert run_cors_checks(http_data, TARGET, PROFILE) == []


def test_wildcard_with_credentials_fails():
    http_data = _http_data({"attempted": True, "allow_origin": "*", "allow_credentials": True, "reflects_arbitrary_origin": False})
    findings = run_cors_checks(http_data, TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["COR-WILDCARD-CREDENTIALS-001"].status == "FAIL"


def test_wildcard_without_credentials_is_clean():
    http_data = _http_data({"attempted": True, "allow_origin": "*", "allow_credentials": False, "reflects_arbitrary_origin": False})
    findings = run_cors_checks(http_data, TARGET, PROFILE)
    assert "COR-WILDCARD-CREDENTIALS-001" not in {f.rule_id for f in findings}


def test_reflected_arbitrary_origin_warns():
    http_data = _http_data({
        "attempted": True,
        "allow_origin": "https://omega-scan-cors-probe.invalid",
        "allow_credentials": False,
        "reflects_arbitrary_origin": True,
    })
    findings = run_cors_checks(http_data, TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["COR-REFLECTED-ORIGIN-001"].status == "WARN"


def test_known_origin_not_reflecting_arbitrary_is_clean():
    http_data = _http_data({
        "attempted": True,
        "allow_origin": "https://trusted.example.org",
        "allow_credentials": True,
        "reflects_arbitrary_origin": False,
    })
    findings = run_cors_checks(http_data, TARGET, PROFILE)
    assert findings == []
