# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_scan.application.pipeline.executor import execute
from omega_scan.domain.profiles.policies import get_profile
from omega_scan.domain.targets.validation import parse_target
from tests.unit.application.conftest import (
    FailingHttpProber,
    FakeConnectivityProber,
    FakeMethodsProber,
    FakePathProber,
    FakeTlsProber,
)


def test_execute_produces_completed_run_with_measured_duration(probers, audit_sink, now_factory):
    target = parse_target("example.org")
    profile = get_profile("standard")

    run = execute(
        target,
        profile,
        audit_sink=audit_sink,
        now_factory=now_factory,
        scan_id="scan-test0000",
        host_machine="test-host",
        **probers,
    )

    assert run.meta["scan_id"] == "scan-test0000"
    assert run.meta["host_machine"] == "test-host"
    assert run.summary.scan_status == "completed"
    assert run.meta["duration_ms"] > 0
    assert run.target is target
    assert any(e.action == "scan_finished" for e in audit_sink.events)


def test_execute_marks_completed_with_errors_on_partial_failure(audit_sink, now_factory):
    target = parse_target("example.org")
    profile = get_profile("standard")

    run = execute(
        target,
        profile,
        connectivity_prober=FakeConnectivityProber(),
        http_prober=FailingHttpProber(),
        tls_prober=FakeTlsProber(),
        path_prober=FakePathProber(),
        methods_prober=FakeMethodsProber(),
        audit_sink=audit_sink,
        now_factory=now_factory,
        scan_id="scan-test0001",
    )

    assert run.summary.scan_status == "completed_with_errors"
    assert len(run.errors) == 1
    assert run.errors[0]["failure_category"] == "connection_refused"
