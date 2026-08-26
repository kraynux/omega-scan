# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
import pytest

from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.scans.service import (
    compute_duration_ms,
    compute_scan_status,
    has_fatal_error,
)


def test_compute_duration_ms():
    duration = compute_duration_ms("2026-08-26T10:00:00Z", "2026-08-26T10:00:01.500Z")
    assert duration == 1500


def test_compute_scan_status_no_errors_is_completed():
    assert compute_scan_status([]) == "completed"


def test_compute_scan_status_non_fatal_errors_is_completed_with_errors():
    errors = [ScanError(module="http_probe", phase="http_probe", error_type="Timeout", message="timeout")]
    assert compute_scan_status(errors) == "completed_with_errors"
    assert has_fatal_error(errors) is False


def test_compute_scan_status_fatal_error_is_failed():
    errors = [
        ScanError(module="target_parser", phase="validation", error_type="TargetParseError", message="x", fatal=True),
    ]
    assert compute_scan_status(errors) == "failed"
    assert has_fatal_error(errors) is True


def test_scan_error_rejects_invalid_failure_category():
    with pytest.raises(ValueError):
        ScanError(module="m", phase="p", error_type="e", message="msg", failure_category="not_a_real_category")
