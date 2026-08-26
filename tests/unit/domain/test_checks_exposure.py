# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.exposure.service import run_exposure_checks

TARGET = {"normalized_host": "example.org", "requested_port": None}
PROFILE = {"profile_name": "standard"}


def _http_data(path_context):
    return {"overview": {"preferred_scheme": "https", "proxy_suspected": False, "catch_all_suspected": False, "path_probe_context": path_context}}


def test_admin_path_accessible_warns():
    http_data = _http_data([{"path": "/admin", "reason": "ok", "status_code": 200}])
    findings = run_exposure_checks(http_data, TARGET, PROFILE)
    assert findings[0].rule_id == "EXR-ADMIN-001"
    assert findings[0].status == "WARN"


def test_sensitive_file_accessible_fails():
    http_data = _http_data([{"path": "/.env", "reason": "ok", "status_code": 200}])
    findings = run_exposure_checks(http_data, TARGET, PROFILE)
    assert findings[0].rule_id == "EXR-SENSITIVE-001"
    assert findings[0].status == "FAIL"


def test_catchall_degrades_confidence_to_low():
    http_data = {
        "overview": {
            "preferred_scheme": "https",
            "proxy_suspected": False,
            "catch_all_suspected": True,
            "path_probe_context": [{"path": "/admin", "reason": "ok", "status_code": 200}],
        }
    }
    findings = run_exposure_checks(http_data, TARGET, PROFILE)
    assert findings[0].confidence == "low"


def test_previously_unjudged_path_now_produces_a_finding():
    """Lot M5 : reconciliation PROBE_*/JUDGED_* (voir policies.py) — /console
    est sonde (PROBE_ADMIN_PATHS) et desormais aussi juge (JUDGED_ADMIN_PATHS
    couvre integralement PROBE_ADMIN_PATHS), contrairement au comportement
    v1 herite documente jusqu'ici."""
    http_data = _http_data([{"path": "/console", "reason": "ok", "status_code": 200}])
    findings = run_exposure_checks(http_data, TARGET, PROFILE)
    assert findings[0].rule_id == "EXR-ADMIN-001"


def test_security_txt_never_judged_as_sensitive_exposure():
    """Exception explicite a la reconciliation (voir policies.py) :
    security.txt reste une convention publique, jamais un EXR-SENSITIVE-001,
    pour ne pas contredire INF-SECURITYTXT-001 (signal positif)."""
    http_data = _http_data(
        [{"path": "/.well-known/security.txt", "reason": "ok", "status_code": 200}]
    )
    findings = run_exposure_checks(http_data, TARGET, PROFILE)
    assert findings == []
