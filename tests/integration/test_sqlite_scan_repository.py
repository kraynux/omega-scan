# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests d'integration de SqliteScanRepository, sur une base SQLite reelle."""
from __future__ import annotations

from pathlib import Path

import pytest

from omega_scan.infrastructure.storage.sqlite.connection import open_connection
from omega_scan.infrastructure.storage.sqlite.migrations import apply_schema
from omega_scan.infrastructure.storage.sqlite.scan_repository import SqliteScanRepository


@pytest.fixture
def repository(tmp_path: Path) -> SqliteScanRepository:
    connection = open_connection(tmp_path / "app.db")
    apply_schema(connection)
    return SqliteScanRepository(connection)


def test_save_then_get_roundtrips_full_run(repository, sample_scan_run):
    repository.save(sample_scan_run)

    fetched = repository.get("scan-test0001")

    assert fetched is not None
    assert fetched.meta["scan_id"] == "scan-test0001"
    assert fetched.target.normalized_host == "example.org"
    assert fetched.summary.overall_rating == "B"
    assert len(fetched.findings) == 1
    assert fetched.findings[0].rule_id == "HDR-NOSNIFF-001"
    assert fetched.findings[0].evidence.value == "absent"


def test_get_unknown_scan_id_returns_none(repository):
    assert repository.get("scan-does-not-exist") is None


def test_list_history_filters_by_normalized_host(repository, sample_scan_run):
    repository.save(sample_scan_run)

    other = _with_scan_id_and_host(sample_scan_run, "scan-test0002", "other.example")
    repository.save(other)

    results = repository.list_history(normalized_host="example.org")

    assert len(results) == 1
    assert results[0].meta["scan_id"] == "scan-test0001"


def test_list_history_orders_most_recent_first(repository, sample_scan_run):
    older = _with_scan_id_and_started_at(sample_scan_run, "scan-test0001", "2026-08-25T10:00:00Z")
    newer = _with_scan_id_and_started_at(sample_scan_run, "scan-test0002", "2026-08-26T10:00:00Z")
    repository.save(older)
    repository.save(newer)

    results = repository.list_history()

    assert [r.meta["scan_id"] for r in results] == ["scan-test0002", "scan-test0001"]


def test_save_is_idempotent_on_scan_id(repository, sample_scan_run):
    repository.save(sample_scan_run)
    repository.save(sample_scan_run)

    assert len(repository.list_history()) == 1


def test_clear_removes_all_scans(repository, sample_scan_run):
    repository.save(sample_scan_run)

    repository.clear()

    assert repository.list_history() == ()


def _with_scan_id_and_host(run, scan_id, normalized_host):
    import dataclasses

    target = dataclasses.replace(run.target, normalized_host=normalized_host)
    meta = dict(run.meta, scan_id=scan_id)
    return dataclasses.replace(run, meta=meta, target=target)


def _with_scan_id_and_started_at(run, scan_id, started_at):
    import dataclasses

    meta = dict(run.meta, scan_id=scan_id, started_at=started_at)
    return dataclasses.replace(run, meta=meta)
