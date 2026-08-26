# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Construction de Finding et regles generiques de degradation de confiance,
communes a toutes les categories de domain/checks/ (ex checks/base.py)."""
from __future__ import annotations

import uuid
from typing import Any

from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding


def build_finding(
    rule_id: str,
    category: str,
    title: str,
    status: str,
    severity: str,
    confidence: str,
    applicability: str,
    description: str,
    impact: str,
    remediation: str,
    evidence: Evidence | None = None,
    location: dict[str, Any] | None = None,
    references: list[str] | None = None,
    tags: list[str] | None = None,
) -> Finding:
    """Construit un Finding avec un ID unique.

    Exception assumee a la regle "domaine sans horloge/alea" (voir
    domain/scans/service.py) : threader un generateur d'ID a travers chaque
    fonction de checks/*/service.py casserait leur signature identique a la
    v1 pour un gain de purete marginal (un finding_id n'a aucune portee
    metier, seulement une identite locale au sein d'un ScanRun)."""
    return Finding(
        finding_id=f"f-{uuid.uuid4().hex[:8]}",
        rule_id=rule_id,
        category=category,
        title=title,
        status=status,
        severity=severity,
        confidence=confidence,
        applicability=applicability,
        description=description,
        impact=impact,
        remediation=remediation,
        evidence=evidence,
        location=location,
        references=references or [],
        tags=tags or [],
    )


def degrade_confidence_for_proxy(confidence: str, proxy_suspected: bool) -> str:
    """Plafonne la confiance a 'medium' si un proxy est suspecte (ARCHITECTURE.md, §8 heritage v1)."""
    if proxy_suspected and confidence in ("certain", "high"):
        return "medium"
    return confidence


def degrade_confidence_for_catchall(confidence: str, catch_all_suspected: bool) -> str:
    """Plafonne la confiance a 'low' si un comportement catch-all est suspecte."""
    if catch_all_suspected and confidence in ("certain", "high", "medium"):
        return "low"
    return confidence
