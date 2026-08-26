# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from datetime import datetime, timezone

from omega_scan.application.commands.run_scan import run_scan
from omega_scan.core.results import Err, Ok
from omega_scan.domain.profiles.exceptions import UnknownProfileError
from omega_scan.domain.targets.exceptions import TargetParseError, UnauthorizedTargetError
from omega_scan.domain.targets.models import PinnedTarget


def _run_scan(target_repository, scan_repository, probers, audit_sink, now_factory, **kwargs):
    return run_scan(
        target_repository=target_repository,
        scan_repository=scan_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        raw_target=kwargs.pop("raw_target", "example.org"),
        profile_name=kwargs.pop("profile_name", "standard"),
        **probers,
        **kwargs,
    )


def test_run_scan_denied_without_authorization(target_repository, scan_repository, probers, audit_sink, now_factory):
    result = _run_scan(target_repository, scan_repository, probers, audit_sink, now_factory)

    assert isinstance(result, Err)
    assert isinstance(result.error, UnauthorizedTargetError)
    assert scan_repository.list_history() == ()
    assert any(e.action == "scan_denied" for e in audit_sink.events)


def test_run_scan_authorized_via_explicit_confirmation(
    target_repository, scan_repository, probers, audit_sink, now_factory
):
    result = _run_scan(
        target_repository, scan_repository, probers, audit_sink, now_factory,
        authorization_confirmed=True,
    )

    assert isinstance(result, Ok)
    dto = result.value
    assert dto.normalized_host == "example.org"
    assert dto.scan_status == "completed"
    assert dto.duration_ms > 0
    assert scan_repository.get(dto.scan_id) is not None
    assert any(e.action == "scan_started" for e in audit_sink.events)
    assert any(e.action == "scan_finished" for e in audit_sink.events)


def test_run_scan_authorized_via_pinned_target(
    target_repository, scan_repository, probers, audit_sink, now_factory
):
    target_repository.pin(
        PinnedTarget(
            normalized_host="example.org",
            authorized=True,
            pinned_at=datetime.now(timezone.utc).isoformat(),
        )
    )

    result = _run_scan(target_repository, scan_repository, probers, audit_sink, now_factory)

    assert isinstance(result, Ok)


def test_run_scan_rejects_invalid_target(target_repository, scan_repository, probers, audit_sink, now_factory):
    result = _run_scan(
        target_repository, scan_repository, probers, audit_sink, now_factory,
        raw_target="   ", authorization_confirmed=True,
    )

    assert isinstance(result, Err)
    assert isinstance(result.error, TargetParseError)


def test_run_scan_rejects_unknown_profile(target_repository, scan_repository, probers, audit_sink, now_factory):
    result = _run_scan(
        target_repository, scan_repository, probers, audit_sink, now_factory,
        authorization_confirmed=True, profile_name="does-not-exist",
    )

    assert isinstance(result, Err)
    assert isinstance(result.error, UnknownProfileError)
