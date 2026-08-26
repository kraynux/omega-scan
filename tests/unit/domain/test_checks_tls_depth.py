# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from omega_scan.domain.checks.tls_depth.service import run_tls_depth_checks

TARGET = {"normalized_host": "example.org", "requested_port": None, "requested_path": "/"}
PROFILE = {"profile_name": "standard"}


def _tls_data(**overrides):
    base = {"attempted": True, "handshake_success": True, "tls_version": "TLSv1.3", "cipher": "TLS_AES_256_GCM_SHA384"}
    base.update(overrides)
    return base


def test_modern_tls_produces_no_findings():
    assert run_tls_depth_checks(_tls_data(), TARGET, PROFILE) == []


def test_handshake_not_attempted_produces_no_findings():
    tls_data = _tls_data(attempted=False, handshake_success=False, tls_version=None, cipher=None)
    assert run_tls_depth_checks(tls_data, TARGET, PROFILE) == []


def test_obsolete_tls_version_fails():
    tls_data = _tls_data(tls_version="TLSv1.1")
    findings = run_tls_depth_checks(tls_data, TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["TLS-VERSION-001"].status == "FAIL"


def test_tls_1_2_is_not_flagged():
    tls_data = _tls_data(tls_version="TLSv1.2")
    findings = run_tls_depth_checks(tls_data, TARGET, PROFILE)
    assert "TLS-VERSION-001" not in {f.rule_id for f in findings}


def test_weak_cipher_warns():
    tls_data = _tls_data(cipher="ECDHE-RSA-RC4-SHA")
    findings = run_tls_depth_checks(tls_data, TARGET, PROFILE)
    rule_ids = {f.rule_id: f for f in findings}
    assert rule_ids["TLS-CIPHER-001"].status == "WARN"


def test_strong_cipher_is_clean():
    tls_data = _tls_data(cipher="TLS_AES_256_GCM_SHA384")
    findings = run_tls_depth_checks(tls_data, TARGET, PROFILE)
    assert "TLS-CIPHER-001" not in {f.rule_id for f in findings}
