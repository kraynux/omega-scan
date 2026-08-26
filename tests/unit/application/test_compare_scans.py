# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_scan.application.commands.run_scan import run_scan
from omega_scan.application.queries.compare_scans import compare_scans
from omega_scan.core.results import Err, Ok
from omega_scan.domain.scans.exceptions import ScanNotFoundError


def _scan(target_repository, scan_repository, probers, audit_sink, now_factory):
    result = run_scan(
        target_repository=target_repository,
        scan_repository=scan_repository,
        audit_sink=audit_sink,
        now_factory=now_factory,
        raw_target="example.org",
        profile_name="quick",
        authorization_confirmed=True,
        **probers,
    )
    assert isinstance(result, Ok)
    return result.value.scan_id


def test_compare_scans_identical_runs_have_no_diff(target_repository, scan_repository, probers, audit_sink, now_factory):
    first_id = _scan(target_repository, scan_repository, probers, audit_sink, now_factory)
    second_id = _scan(target_repository, scan_repository, probers, audit_sink, now_factory)

    result = compare_scans(
        scan_repository=scan_repository, previous_scan_id=first_id, current_scan_id=second_id
    )

    assert isinstance(result, Ok)
    comparison = result.value
    assert comparison.new_findings == ()
    assert comparison.resolved_findings == ()
    assert comparison.changed_findings == ()


def test_compare_scans_missing_id(target_repository, scan_repository, probers, audit_sink, now_factory):
    existing_id = _scan(target_repository, scan_repository, probers, audit_sink, now_factory)

    result = compare_scans(
        scan_repository=scan_repository,
        previous_scan_id="scan-missing",
        current_scan_id=existing_id,
    )

    assert isinstance(result, Err)
    assert isinstance(result.error, ScanNotFoundError)
