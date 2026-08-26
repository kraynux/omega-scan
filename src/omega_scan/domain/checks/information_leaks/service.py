# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks de fuites d'information (INF-*) : bannieres, erreurs, stack traces,
robots, headers bavards. Toutes soumises a la degradation proxy."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.checks.information_leaks.policies import (
    ERROR_PATTERNS,
    STACK_PATTERNS,
    VERBOSE_HEADERS,
)
from omega_scan.domain.findings.builders import build_finding, degrade_confidence_for_proxy
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding


def check_inf_banner_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """INF-BANNER-001 : bannieres serveur exposees (Server, X-Powered-By). WARN."""
    findings: list[Finding] = []
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")

    if not preferred_scheme:
        return findings

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return findings

    headers = http_result.get("headers", {})

    server = headers.get("Server") or headers.get("server")
    if server:
        confidence = degrade_confidence_for_proxy("high", proxy_suspected)
        findings.append(build_finding(
            rule_id="INF-BANNER-001",
            category="information_leak",
            title="Banniere Server exposee",
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=f"Le header Server expose des informations : {server}",
            impact="Fuite d'information sur la technologie serveur.",
            remediation="Configurer le serveur pour masquer ou minimiser le header Server.",
            evidence=Evidence(type="header", value=server, source="response.headers"),
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "information_leak",
            },
            tags=["banner", "information_leak"],
        ))

    powered_by = headers.get("X-Powered-By") or headers.get("x-powered-by")
    if powered_by:
        confidence = degrade_confidence_for_proxy("high", proxy_suspected)
        findings.append(build_finding(
            rule_id="INF-BANNER-001",
            category="information_leak",
            title="Banniere X-Powered-By exposee",
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=f"Le header X-Powered-By expose des informations : {powered_by}",
            impact="Fuite d'information sur le framework/technologie.",
            remediation="Supprimer le header X-Powered-By de la configuration.",
            evidence=Evidence(type="header", value=powered_by, source="response.headers"),
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "information_leak",
            },
            tags=["banner", "information_leak"],
        ))

    return findings


def check_inf_error_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """INF-ERROR-001 : messages d'erreur detailles exposes. WARN."""
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")

    if not preferred_scheme:
        return None

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None

    body_preview = http_result.get("body_preview", {}).get("text_preview", "").lower()
    found_patterns = [p for p in ERROR_PATTERNS if p in body_preview]

    if found_patterns:
        confidence = degrade_confidence_for_proxy("medium", proxy_suspected)
        return build_finding(
            rule_id="INF-ERROR-001",
            category="information_leak",
            title="Messages d'erreur detailles exposes",
            status="WARN",
            severity="medium",
            confidence=confidence,
            applicability="applicable",
            description=f"Des messages d'erreur detailles sont visibles dans la reponse : {', '.join(found_patterns[:3])}",
            impact="Fuite d'information sur l'implementation, potentiellement exploitable.",
            remediation="Configurer le serveur pour afficher des pages d'erreur generiques en production.",
            evidence=Evidence(
                type="body_content",
                value=f"Patterns detectes : {', '.join(found_patterns[:3])}",
                source="response.body_preview",
                excerpt=body_preview[:200],
            ),
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "information_leak",
            },
            tags=["error", "information_leak"],
        )

    return None


def check_inf_stack_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """INF-STACK-001 : stack trace expose. FAIL (plus severe que INF-ERROR-001)."""
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")

    if not preferred_scheme:
        return None

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None

    body_preview = http_result.get("body_preview", {}).get("text_preview", "").lower()
    found_patterns = [p for p in STACK_PATTERNS if p in body_preview]

    if found_patterns:
        confidence = degrade_confidence_for_proxy("high", proxy_suspected)
        return build_finding(
            rule_id="INF-STACK-001",
            category="information_leak",
            title="Stack trace expose",
            status="FAIL",
            severity="high",
            confidence=confidence,
            applicability="applicable",
            description=f"Un stack trace est visible dans la reponse : {', '.join(found_patterns[:2])}",
            impact="Fuite d'information critique sur l'implementation, paths internes, versions.",
            remediation="Desactiver l'affichage des stack traces en production. Utiliser des pages d'erreur generiques.",
            evidence=Evidence(
                type="body_content",
                value=f"Stack trace detecte : {', '.join(found_patterns[:2])}",
                source="response.body_preview",
                excerpt=body_preview[:300],
            ),
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "information_leak",
            },
            tags=["stack_trace", "information_leak"],
        )

    return None


def check_inf_robots_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """INF-ROBOTS-001 : presence de /robots.txt. Signal informatif, pas un echec."""
    overview = http_data.get("overview", {})
    path_context = overview.get("path_probe_context", [])
    robots_probe = next((p for p in path_context if p["path"] == "/robots.txt"), None)

    if robots_probe and robots_probe["reason"] == "ok":
        return build_finding(
            rule_id="INF-ROBOTS-001",
            category="information_leak",
            title="Fichier robots.txt present",
            status="OK",
            severity="info",
            confidence="certain",
            applicability="applicable",
            description="Le fichier /robots.txt est present et peut reveler des chemins sensibles.",
            impact="Fuite d'information mineure sur la structure du site.",
            remediation="Verifier que /robots.txt ne liste pas de chemins sensibles ou administratifs.",
            evidence=Evidence(
                type="status_code",
                value=f"/robots.txt -> {robots_probe['status_code']}",
                source="path_probe",
            ),
            location={
                "url": f"{overview.get('preferred_scheme', 'https')}://{target.get('normalized_host')}/robots.txt",
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": overview.get("preferred_scheme"),
                "path": "/robots.txt",
                "component": "information_leak",
            },
            tags=["robots", "information_leak"],
        )

    return None


def check_inf_securitytxt_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """INF-SECURITYTXT-001 : presence de /.well-known/security.txt (RFC 9116).
    Signal positif (bonne pratique), jamais un echec en son absence — meme
    patron que INF-ROBOTS-001 ci-dessus."""
    overview = http_data.get("overview", {})
    path_context = overview.get("path_probe_context", [])
    probe = next((p for p in path_context if p["path"] == "/.well-known/security.txt"), None)

    if probe and probe["reason"] == "ok":
        return build_finding(
            rule_id="INF-SECURITYTXT-001",
            category="information_leak",
            title="Fichier security.txt present",
            status="OK",
            severity="info",
            confidence="certain",
            applicability="applicable",
            description="Le fichier /.well-known/security.txt est present (RFC 9116).",
            impact="Bonne pratique : facilite le signalement responsable de vulnerabilites.",
            remediation="Aucune action requise.",
            evidence=Evidence(
                type="status_code",
                value=f"/.well-known/security.txt -> {probe['status_code']}",
                source="path_probe",
            ),
            location={
                "url": (
                    f"{overview.get('preferred_scheme', 'https')}://"
                    f"{target.get('normalized_host')}/.well-known/security.txt"
                ),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": overview.get("preferred_scheme"),
                "path": "/.well-known/security.txt",
                "component": "information_leak",
            },
            tags=["security-txt", "information_leak"],
        )

    return None


def check_inf_header_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """INF-HEADER-001 : headers bavards (X-AspNet-Version, X-Debug, etc.). WARN."""
    findings: list[Finding] = []
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")

    if not preferred_scheme:
        return findings

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return findings

    headers = http_result.get("headers", {})
    headers_lower = {k.lower(): v for k, v in headers.items()}

    for verbose_header in VERBOSE_HEADERS:
        if verbose_header in headers_lower:
            if verbose_header in ("x-powered-by",):
                continue  # deja traite par INF-BANNER-001

            value = headers_lower[verbose_header]
            confidence = degrade_confidence_for_proxy("medium", proxy_suspected)

            findings.append(build_finding(
                rule_id="INF-HEADER-001",
                category="information_leak",
                title=f"Header technique expose : {verbose_header}",
                status="WARN",
                severity="low",
                confidence=confidence,
                applicability="applicable",
                description=f"Le header {verbose_header} expose des informations techniques : {value}",
                impact="Fuite d'information sur l'implementation.",
                remediation=f"Supprimer le header {verbose_header} de la configuration.",
                evidence=Evidence(type="header", value=f"{verbose_header}: {value}", source="response.headers"),
                location={
                    "url": http_result.get("requested_url"),
                    "host": target.get("normalized_host"),
                    "port": target.get("requested_port"),
                    "scheme": preferred_scheme,
                    "path": target.get("requested_path"),
                    "component": "information_leak",
                },
                tags=["header", "information_leak"],
            ))

    return findings


def run_information_leaks_checks(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks de fuites d'information."""
    findings: list[Finding] = []
    findings.extend(check_inf_banner_001(http_data, target, profile))

    f = check_inf_error_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_inf_stack_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_inf_robots_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_inf_securitytxt_001(http_data, target, profile)
    if f:
        findings.append(f)

    findings.extend(check_inf_header_001(http_data, target, profile))

    return findings
