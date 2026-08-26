# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests d'integration de SqliteTargetRepository, sur une base SQLite reelle."""
from __future__ import annotations

from pathlib import Path

import pytest

from omega_scan.domain.targets.models import PinnedTarget
from omega_scan.infrastructure.storage.sqlite.connection import open_connection
from omega_scan.infrastructure.storage.sqlite.migrations import apply_schema
from omega_scan.infrastructure.storage.sqlite.target_repository import SqliteTargetRepository


@pytest.fixture
def repository(tmp_path: Path) -> SqliteTargetRepository:
    connection = open_connection(tmp_path / "app.db")
    apply_schema(connection)
    return SqliteTargetRepository(connection)


def test_pin_then_get_roundtrips(repository):
    pinned = PinnedTarget(
        normalized_host="example.org", authorized=True,
        pinned_at="2026-08-26T10:00:00Z", note="autorise par le client",
    )

    repository.pin(pinned)

    fetched = repository.get("example.org")
    assert fetched == pinned


def test_get_unknown_host_returns_none(repository):
    assert repository.get("unknown.example") is None


def test_pin_is_idempotent_on_normalized_host(repository):
    first = PinnedTarget(normalized_host="example.org", authorized=True, pinned_at="2026-08-26T10:00:00Z")
    second = PinnedTarget(
        normalized_host="example.org", authorized=True,
        pinned_at="2026-08-27T10:00:00Z", note="reconfirme",
    )

    repository.pin(first)
    repository.pin(second)

    fetched = repository.get("example.org")
    assert fetched.pinned_at == "2026-08-27T10:00:00Z"
    assert fetched.note == "reconfirme"
    assert len(repository.list_pinned()) == 1


def test_unpin_removes_the_target(repository):
    repository.pin(PinnedTarget(normalized_host="example.org", authorized=True, pinned_at="2026-08-26T10:00:00Z"))

    repository.unpin("example.org")

    assert repository.get("example.org") is None


def test_list_pinned_orders_most_recent_first(repository):
    repository.pin(PinnedTarget(normalized_host="a.example", authorized=True, pinned_at="2026-08-25T10:00:00Z"))
    repository.pin(PinnedTarget(normalized_host="b.example", authorized=True, pinned_at="2026-08-26T10:00:00Z"))

    hosts = [p.normalized_host for p in repository.list_pinned()]

    assert hosts == ["b.example", "a.example"]
