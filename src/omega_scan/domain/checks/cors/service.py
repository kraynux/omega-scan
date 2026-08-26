# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks CORS (COR-*) : configuration de partage de ressources cross-origin.

La collecte (infrastructure/network/httpx_http_prober.py::_probe_cors) envoie
une requete avec un header Origin arbitraire et observe la reponse — jamais
d'exploitation, uniquement l'observation d'un comportement de reflexion
d'origine ou de wildcard combine a des credentials, deux mauvaises pratiques
connues et documentees (MDN), jamais une preuve d'exploitation reelle."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.findings.builders import build_finding
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding


def _location(http_data: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    return {
        "url": None,
        "host": target.get("normalized_host"),
        "port": target.get("requested_port"),
        "scheme": http_data.get("overview", {}).get("preferred_scheme"),
        "path": target.get("requested_path"),
        "component": "cors",
    }


def check_cor_wildcard_credentials_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """COR-WILDCARD-CREDENTIALS-001 : ACAO=* combine a ACAC=true. FAIL (viole
    directement la specification CORS, dangereux)."""
    cors = http_data.get("cors", {})
    if not cors.get("attempted"):
        return None

    if cors.get("allow_origin") != "*" or not cors.get("allow_credentials"):
        return None

    return build_finding(
        rule_id="COR-WILDCARD-CREDENTIALS-001",
        category="cors",
        title="CORS wildcard combine a des credentials autorises",
        status="FAIL",
        severity="high",
        confidence="certain",
        applicability="applicable",
        description=(
            "Access-Control-Allow-Origin: * est combine a "
            "Access-Control-Allow-Credentials: true."
        ),
        impact="N'importe quel site tiers peut lire des reponses authentifiees de l'utilisateur.",
        remediation="Ne jamais combiner un wildcard avec Allow-Credentials ; whitelister les origines.",
        evidence=Evidence(
            type="header", value="Access-Control-Allow-Origin: *", source="response.headers"
        ),
        location=_location(http_data, target),
        references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS"],
        tags=["cors", "credentials"],
    )


def check_cor_reflected_origin_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """COR-REFLECTED-ORIGIN-001 : une origine arbitraire non reconnue est
    reflechie telle quelle. WARN (absence apparente de whitelist)."""
    cors = http_data.get("cors", {})
    if not cors.get("attempted") or not cors.get("reflects_arbitrary_origin"):
        return None

    return build_finding(
        rule_id="COR-REFLECTED-ORIGIN-001",
        category="cors",
        title="Origine arbitraire reflechie dans Access-Control-Allow-Origin",
        status="WARN",
        severity="medium",
        confidence="certain",
        applicability="applicable",
        description=(
            "Le service reflete telle quelle une origine arbitraire et non reconnue "
            "dans Access-Control-Allow-Origin."
        ),
        impact="Absence apparente de validation d'origine : un site tiers peut lire les reponses.",
        remediation="Valider l'origine recue contre une liste explicite avant de la reflechir.",
        evidence=Evidence(
            type="header", value=str(cors.get("allow_origin")), source="response.headers"
        ),
        location=_location(http_data, target),
        tags=["cors", "origin"],
    )


def run_cors_checks(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks CORS."""
    findings: list[Finding] = []
    f = check_cor_wildcard_credentials_001(http_data, target, profile)
    if f:
        findings.append(f)
    f = check_cor_reflected_origin_001(http_data, target, profile)
    if f:
        findings.append(f)
    return findings
