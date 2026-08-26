# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_scan.application.commands.replay_scan import replay_scan
from omega_scan.application.commands.run_scan import run_scan
from omega_scan.core.results import Err, Ok
from omega_scan.domain.scans.exceptions import ScanNotFoundError
from omega_scan.domain.targets.exceptions import UnauthorizedTargetError


def test_replay_scan_reuses_target_and_profile(target_repository, scan_repository, probers, audit_sink, now_factory):
    first = run_scan(
        target_repository=target_repository,
        scan_repository=scan_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        raw_target="example.org",
        profile_name="quick",
        authorization_confirmed=True,
        **probers,
    )
    assert isinstance(first, Ok)
    original_scan_id = first.value.scan_id

    replayed = replay_scan(
        scan_repository=scan_repository,
        target_repository=target_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        scan_id=original_scan_id,
        authorization_confirmed=True,
        **probers,
    )

    assert isinstance(replayed, Ok)
    assert replayed.value.normalized_host == "example.org"
    assert replayed.value.profile_name == "quick"
    assert replayed.value.scan_id != original_scan_id


def test_replay_scan_unknown_id_is_not_found(target_repository, scan_repository, probers, audit_sink, now_factory):
    result = replay_scan(
        scan_repository=scan_repository,
        target_repository=target_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        scan_id="scan-does-not-exist",
        **probers,
    )

    assert isinstance(result, Err)
    assert isinstance(result.error, ScanNotFoundError)


def test_replay_scan_still_requires_authorization(target_repository, scan_repository, probers, audit_sink, now_factory):
    first = run_scan(
        target_repository=target_repository,
        scan_repository=scan_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        raw_target="example.org",
        profile_name="quick",
        authorization_confirmed=True,
        **probers,
    )
    scan_id = first.value.scan_id

    replayed = replay_scan(
        scan_repository=scan_repository,
        target_repository=target_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        scan_id=scan_id,
        authorization_confirmed=False,
        **probers,
    )

    assert isinstance(replayed, Err)
    assert isinstance(replayed.error, UnauthorizedTargetError)
