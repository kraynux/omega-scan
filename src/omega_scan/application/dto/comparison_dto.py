# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""DTO expose a la presentation pour une comparaison entre deux scans."""
from __future__ import annotations

from dataclasses import dataclass

from omega_scan.application.dto.scan_dto import FindingDTO


@dataclass(frozen=True, slots=True)
class ChangedFindingDTO:
    """Un finding present dans les deux scans mais dont le statut a change."""

    previous: FindingDTO
    current: FindingDTO


@dataclass(frozen=True, slots=True)
class ScanComparisonDTO:
    """Vue plate d'une ScanComparison (domain/reports/comparison.py)."""

    new_findings: tuple[FindingDTO, ...]
    resolved_findings: tuple[FindingDTO, ...]
    unchanged_findings: tuple[FindingDTO, ...]
    changed_findings: tuple[ChangedFindingDTO, ...]
