# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from datetime import datetime, timezone

from omega_scan.application.commands.pin_target import pin_target
from omega_scan.application.commands.unpin_target import unpin_target
from omega_scan.core.results import Err, Ok
from omega_scan.domain.targets.exceptions import TargetParseError


def test_pin_target_persists_and_authorizes(target_repository):
    result = pin_target(
        target_repository=target_repository,
        now=datetime.now(timezone.utc),
        raw_input="example.org",
        note="cible de test",
    )

    assert isinstance(result, Ok)
    dto = result.value
    assert dto.normalized_host == "example.org"
    assert dto.authorized is True
    assert dto.note == "cible de test"
    assert target_repository.get("example.org") is not None


def test_pin_target_rejects_invalid_input(target_repository):
    result = pin_target(
        target_repository=target_repository, now=datetime.now(timezone.utc), raw_input="   "
    )

    assert isinstance(result, Err)
    assert isinstance(result.error, TargetParseError)


def test_unpin_target_removes_pin(target_repository):
    pin_target(target_repository=target_repository, now=datetime.now(timezone.utc), raw_input="example.org")
    assert target_repository.get("example.org") is not None

    unpin_target(target_repository=target_repository, normalized_host="example.org")

    assert target_repository.get("example.org") is None


def test_unpin_unknown_target_is_a_noop(target_repository):
    unpin_target(target_repository=target_repository, normalized_host="never-pinned.org")
    assert target_repository.get("never-pinned.org") is None
