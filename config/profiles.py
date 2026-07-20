# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Profils de scan.
Section 12 de la spec.
"""

from dataclasses import dataclass, asdict
from typing import List

@dataclass
class ScanProfile:
    profile_name: str
    timeout_connect: int
    timeout_read: int
    http_methods_tested: List[str]
    path_checks_enabled: bool
    path_probe_delay_ms: int
    path_probe_max_targets: int
    tls_checks_enabled: bool
    follow_redirects: bool
    max_redirects: int
    user_agent: str

    def to_dict(self) -> dict:
        return asdict(self)

# Profils prédéfinis (conformes au tableau de la spec)
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
    tls_checks_enabled=True, # Tolérant (auto-signé accepté sans FAIL)
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
        raise ValueError(f"Profil inconnu : {name}. Choix : {list(PROFILES.keys())}")
    return PROFILES[name]
