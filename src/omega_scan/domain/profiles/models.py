# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Objet ScanProfile : parametrage d'un profil de scan."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class ScanProfile:
    profile_name: str
    timeout_connect: int
    timeout_read: int
    http_methods_tested: list[str]
    path_checks_enabled: bool
    path_probe_delay_ms: int
    path_probe_max_targets: int
    tls_checks_enabled: bool
    follow_redirects: bool
    max_redirects: int
    user_agent: str

    def to_dict(self) -> dict:
        return asdict(self)
