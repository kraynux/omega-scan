# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat du path probing et de la detection catch-all."""
from __future__ import annotations

from typing import Any, Protocol

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target


class PathProber(Protocol):
    """Port consomme par application/pipeline/steps.py, implemente par
    infrastructure/network/httpx_path_prober.py. Depend du bloc `http`
    deja collecte (schema prefere, URL finale)."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        http_data: dict[str, Any],
        errors: list[ScanError],
    ) -> dict[str, Any]:
        """Retourne `catch_all_suspected` et `path_probe_context`."""
        ...
