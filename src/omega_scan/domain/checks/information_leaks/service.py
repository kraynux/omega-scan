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
from omega_scan.shared.i18n import _


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
            title=_("Bannière Server exposée"),
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=_("Le header Server expose des informations : {server}").format(server=server),
            impact=_("Fuite d'information sur la technologie serveur."),
            remediation=_("Configurer le serveur pour masquer ou minimiser le header Server."),
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
            title=_("Bannière X-Powered-By exposée"),
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=_("Le header X-Powered-By expose des informations : {powered_by}").format(powered_by=powered_by),
            impact=_("Fuite d'information sur le framework/technologie."),
            remediation=_("Supprimer le header X-Powered-By de la configuration."),
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
            title=_("Messages d'erreur détaillés exposés"),
            status="WARN",
            severity="medium",
            confidence=confidence,
            applicability="applicable",
            description=_("Des messages d'erreur détaillés sont visibles dans la réponse : {join}").format(join=', '.join(found_patterns[:3])),
            impact=_("Fuite d'information sur l'implémentation, potentiellement exploitable."),
            remediation=_("Configurer le serveur pour afficher des pages d'erreur génériques "
                          "en production."),
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
            title=_("Stack trace exposé"),
            status="FAIL",
            severity="high",
            confidence=confidence,
            applicability="applicable",
            description=_("Un stack trace est visible dans la réponse : {join}").format(join=', '.join(found_patterns[:2])),
            impact=_("Fuite d'information critique sur l'implémentation, paths internes, "
                     "versions."),
            remediation=_("Désactiver l'affichage des stack traces en production. Utiliser des "
                          "pages d'erreur génériques."),
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
            title=_("Fichier robots.txt présent"),
            status="OK",
            severity="info",
            confidence="certain",
            applicability="applicable",
            description=_("Le fichier /robots.txt est présent et peut révéler des chemins "
                          "sensibles."),
            impact=_("Fuite d'information mineure sur la structure du site."),
            remediation=_("Vérifier que /robots.txt ne liste pas de chemins sensibles ou "
                          "administratifs."),
            evidence=Evidence(
                type="status_code",
                value=f"/robots.txt -> {robots_probe['status_code']}",
                source="path_probe",
            ),
            location={
                "url": _("{get}://{get2}/robots.txt").format(get=overview.get('preferred_scheme', 'https'), get2=target.get('normalized_host')),
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
            title=_("Fichier security.txt présent"),
            status="OK",
            severity="info",
            confidence="certain",
            applicability="applicable",
            description=_("Le fichier /.well-known/security.txt est présent (RFC 9116)."),
            impact=_("Bonne pratique : facilite le signalement responsable de vulnérabilités."),
            remediation=_("Aucune action requise."),
            evidence=Evidence(
                type="status_code",
                value=f"/.well-known/security.txt -> {probe['status_code']}",
                source="path_probe",
            ),
            location={
                "url": (
                    _("{get}://{get2}/.well-known/security.txt").format(get=overview.get('preferred_scheme', 'https'), get2=target.get('normalized_host'))
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
                title=_("Header technique exposé : {verbose_header}").format(verbose_header=verbose_header),
                status="WARN",
                severity="low",
                confidence=confidence,
                applicability="applicable",
                description=_("Le header {verbose_header} expose des informations techniques : "
                              "{value}").format(verbose_header=verbose_header, value=value),
                impact=_("Fuite d'information sur l'implémentation."),
                remediation=_("Supprimer le header {verbose_header} de la configuration.").format(verbose_header=verbose_header),
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
