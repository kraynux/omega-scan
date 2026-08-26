# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat du test des methodes HTTP configurees par le profil."""
from __future__ import annotations

from typing import Any, Protocol

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target


class MethodsProber(Protocol):
    """Port consomme par application/pipeline/steps.py, implemente par
    infrastructure/network/httpx_methods_prober.py."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        http_data: dict[str, Any],
        errors: list[ScanError],
    ) -> dict[str, Any]:
        """Retourne `methods_tested`, un resultat par methode du profil."""
        ...
