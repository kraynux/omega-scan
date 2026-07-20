# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Infrastructure de base pour les checks.
Section 10 et 11 de la spec.
"""

import uuid
from typing import Optional, Dict, Any, List
from models.finding import Finding
from models.evidence import Evidence


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
    evidence: Optional[Evidence] = None,
    location: Optional[Dict[str, Any]] = None,
    references: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> Finding:
    """
    Construit un Finding avec un ID unique.
    """
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
    """
    Dégrade la confiance si proxy_suspected est vrai (section 7.2 et 11).
    Plafonne à 'medium' si proxy suspecté.
    """
    if proxy_suspected and confidence in ("certain", "high"):
        return "medium"
    return confidence


def degrade_confidence_for_catchall(confidence: str, catch_all_suspected: bool) -> str:
    """
    Dégrade la confiance si catch_all_suspected est vrai (section 5.2 et 11).
    Plafonne à 'low' si catch-all suspecté.
    """
    if catch_all_suspected and confidence in ("certain", "high", "medium"):
        return "low"
    return confidence
