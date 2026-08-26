# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""DTO exposes a la presentation pour un scan, en vue liste et en vue detail."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ScanSummaryDTO:
    """Vue liste d'un scan (historique), juste assez pour un tableau."""

    scan_id: str
    normalized_host: str
    started_at: str
    scan_status: str
    overall_rating: str
    short_message: str
    findings_total: int


@dataclass(frozen=True, slots=True)
class EvidenceDTO:
    """Vue plate d'une Evidence (domain/findings/evidence.py)."""

    type: str
    value: str
    source: str
    excerpt: str | None


@dataclass(frozen=True, slots=True)
class FindingDTO:
    """Vue plate d'un Finding (domain/findings/models.py)."""

    finding_id: str
    rule_id: str
    category: str
    title: str
    status: str
    severity: str
    confidence: str
    applicability: str
    description: str
    impact: str
    remediation: str
    evidence: EvidenceDTO | None
    location: dict[str, Any] | None
    references: tuple[str, ...]
    tags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ScanRunDTO:
    """Vue detail d'un ScanRun complet.

    connectivity/http/tls restent des dict bruts (deja JSON-serializables
    via ScanRun.to_dict(), structure profondement imbriquee et heterogene) :
    aucun consommateur de interfaces/ n'a encore besoin d'un typage plus
    fin de ces blocs — les findings, eux, sont types (FindingDTO) car ils
    seront affiches en tableau des le Lot M4."""

    scan_id: str
    normalized_host: str
    profile_name: str
    started_at: str
    finished_at: str
    duration_ms: int
    scan_status: str
    findings: tuple[FindingDTO, ...]
    summary: ScanSummaryDTO
    connectivity: dict[str, Any]
    http: dict[str, Any]
    tls: dict[str, Any]
    errors: tuple[dict[str, Any], ...]
