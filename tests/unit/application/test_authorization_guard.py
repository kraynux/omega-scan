# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from datetime import datetime, timezone

from omega_scan.application.pipeline.guards.authorization_guard import check_authorization
from omega_scan.core.results import Err, Ok
from omega_scan.domain.targets.exceptions import UnauthorizedTargetError
from omega_scan.domain.targets.models import PinnedTarget, Target
from omega_scan.domain.targets.validation import parse_target


def _target(host: str = "example.org") -> Target:
    return parse_target(host)


def test_denied_without_pin_or_confirmation(target_repository):
    result = check_authorization(
        _target(), target_repository=target_repository, explicit_confirmation=False
    )
    assert isinstance(result, Err)
    assert isinstance(result.error, UnauthorizedTargetError)


def test_allowed_with_explicit_confirmation(target_repository):
    result = check_authorization(
        _target(), target_repository=target_repository, explicit_confirmation=True
    )
    assert isinstance(result, Ok)


def test_allowed_when_pinned_and_authorized(target_repository):
    target_repository.pin(
        PinnedTarget(
            normalized_host="example.org",
            authorized=True,
            pinned_at=datetime.now(timezone.utc).isoformat(),
        )
    )
    result = check_authorization(
        _target(), target_repository=target_repository, explicit_confirmation=False
    )
    assert isinstance(result, Ok)


def test_denied_when_pinned_but_not_authorized(target_repository):
    target_repository.pin(
        PinnedTarget(
            normalized_host="example.org",
            authorized=False,
            pinned_at=datetime.now(timezone.utc).isoformat(),
        )
    )
    result = check_authorization(
        _target(), target_repository=target_repository, explicit_confirmation=False
    )
    assert isinstance(result, Err)
