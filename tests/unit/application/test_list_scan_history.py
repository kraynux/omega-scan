# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_scan.application.commands.run_scan import run_scan
from omega_scan.application.queries.list_scan_history import list_scan_history


def test_list_scan_history_filters_by_host(target_repository, scan_repository, probers, audit_sink, now_factory):
    run_scan(
        target_repository=target_repository, scan_repository=scan_repository,
        audit_sink=audit_sink, now_factory=now_factory,
        raw_target="example.org", profile_name="quick", authorization_confirmed=True, **probers,
    )
    run_scan(
        target_repository=target_repository, scan_repository=scan_repository,
        audit_sink=audit_sink, now_factory=now_factory,
        raw_target="other.example", profile_name="quick", authorization_confirmed=True, **probers,
    )

    all_history = list_scan_history(scan_repository=scan_repository)
    assert len(all_history) == 2

    filtered = list_scan_history(scan_repository=scan_repository, normalized_host="example.org")
    assert len(filtered) == 1
    assert filtered[0].normalized_host == "example.org"
