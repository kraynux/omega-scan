# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from omega_scan.application.queries.list_profiles import list_profiles


def test_list_profiles_returns_the_four_predefined_profiles():
    profiles = list_profiles()

    assert {p.profile_name for p in profiles} == {"quick", "standard", "extended", "local-lab"}
