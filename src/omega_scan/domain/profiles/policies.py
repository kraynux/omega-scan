# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Catalogue des 4 profils de scan predefinis (quick/standard/extended/local-lab).

Profils en lecture seule (pas de CRUD utilisateur, a la difference des
profils de charge d'omega-stress) : voir ARCHITECTURE.md §2, domain/profiles/.
"""
from __future__ import annotations

from omega_scan.domain.profiles.exceptions import UnknownProfileError
from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.shared.i18n import _

PROFILE_QUICK = ScanProfile(
    profile_name="quick",
    timeout_connect=3,
    timeout_read=6,
    http_methods_tested=["OPTIONS"],
    path_checks_enabled=False,
    path_probe_delay_ms=0,
    path_probe_max_targets=0,
    tls_checks_enabled=False,
    follow_redirects=True,
    max_redirects=5,
    user_agent="Omega-scan/1.0 (quick)",
)

PROFILE_STANDARD = ScanProfile(
    profile_name="standard",
    timeout_connect=3,
    timeout_read=6,
    http_methods_tested=["OPTIONS", "TRACE"],
    path_checks_enabled=True,
    path_probe_delay_ms=200,
    path_probe_max_targets=20,
    tls_checks_enabled=True,
    follow_redirects=True,
    max_redirects=5,
    user_agent="Omega-scan/1.0 (standard)",
)

PROFILE_EXTENDED = ScanProfile(
    profile_name="extended",
    timeout_connect=5,
    timeout_read=10,
    http_methods_tested=["OPTIONS", "TRACE", "PUT", "DELETE", "PATCH"],
    path_checks_enabled=True,
    path_probe_delay_ms=300,
    path_probe_max_targets=100,
    tls_checks_enabled=True,
    follow_redirects=True,
    max_redirects=5,
    user_agent="Omega-scan/1.0 (extended)",
)

PROFILE_LOCAL_LAB = ScanProfile(
    profile_name="local-lab",
    timeout_connect=3,
    timeout_read=6,
    http_methods_tested=["OPTIONS", "TRACE"],
    path_checks_enabled=True,
    path_probe_delay_ms=100,
    path_probe_max_targets=20,
    tls_checks_enabled=True,  # Tolerant (auto-signe accepte sans FAIL)
    follow_redirects=True,
    max_redirects=5,
    user_agent="Omega-scan/1.0 (local-lab)",
)

PROFILES = {
    "quick": PROFILE_QUICK,
    "standard": PROFILE_STANDARD,
    "extended": PROFILE_EXTENDED,
    "local-lab": PROFILE_LOCAL_LAB,
}


def get_profile(name: str) -> ScanProfile:
    if name not in PROFILES:
        raise UnknownProfileError(_("Profil inconnu : {name}. Choix : {value}").format(name=name, value=list(PROFILES.keys())))
    return PROFILES[name]
