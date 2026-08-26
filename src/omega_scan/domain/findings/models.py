# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Objet Finding : resultat d'une regle d'analyse appliquee aux preuves collectees."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from omega_scan.domain.findings.evidence import Evidence


@dataclass
class Finding:
    """Resultat d'une regle d'analyse."""

    finding_id: str
    rule_id: str  # ex. "TRN-HTTPS-001", "HDR-CSP-001"
    category: str  # "transport", "headers", "cookies", "cors", "methods", "exposure", "information_leak"
    title: str

    status: str  # "OK", "WARN", "FAIL", "N/A"
    severity: str  # "info", "low", "medium", "high", "critical"
    confidence: str  # "certain", "high", "medium", "low"
    applicability: str  # "applicable", "conditional", "not_applicable"

    description: str
    impact: str
    remediation: str

    evidence: Evidence | None = None
    location: dict[str, Any] | None = None  # {url, host, port, scheme, path, component}

    references: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = asdict(self)
        if self.evidence:
            result["evidence"] = self.evidence.to_dict()
        return result
