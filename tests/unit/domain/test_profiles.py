# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
import pytest

from omega_scan.domain.profiles.exceptions import UnknownProfileError
from omega_scan.domain.profiles.policies import get_profile


def test_get_profile_standard():
    profile = get_profile("standard")
    assert profile.profile_name == "standard"
    assert profile.tls_checks_enabled is True
    assert profile.path_checks_enabled is True


def test_get_profile_quick_disables_path_and_tls():
    profile = get_profile("quick")
    assert profile.path_checks_enabled is False
    assert profile.tls_checks_enabled is False


def test_get_profile_unknown_raises():
    with pytest.raises(UnknownProfileError):
        get_profile("does-not-exist")
