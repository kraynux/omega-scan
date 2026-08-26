# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat de la collecte HTTP/HTTPS principale."""
from __future__ import annotations

from typing import Any, Protocol

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target


class HttpProber(Protocol):
    """Port consomme par application/pipeline/steps.py, implemente par
    infrastructure/network/httpx_http_prober.py."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        errors: list[ScanError],
    ) -> dict[str, Any]:
        """Remplit le bloc `http` de ScanRun (overview, http, https)."""
        ...
