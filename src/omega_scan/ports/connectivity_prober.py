# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat du pre-scan de connectivite (DNS, HTTP, HTTPS)."""
from __future__ import annotations

from typing import Any, Protocol

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target


class ConnectivityProber(Protocol):
    """Port consomme par application/pipeline/steps.py, implemente par
    infrastructure/network/httpx_connectivity_prober.py."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        errors: list[ScanError],
    ) -> dict[str, Any]:
        """Remplit le bloc `connectivity` de ScanRun. Les echecs reseau
        previsibles sont ajoutes a `errors` (effet de bord), jamais leves —
        meme contrat que la v1 (ARCHITECTURE.md §5.3)."""
        ...
