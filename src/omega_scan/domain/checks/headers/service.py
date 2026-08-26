# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks headers (HDR-*) : CSP, nosniff, referrer, framing, bannieres, cache."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.checks.headers.policies import (
    CACHE_CONTROL_SAFE_DIRECTIVES,
    CSP_PERMISSIVE_PATTERNS,
)
from omega_scan.domain.findings.builders import build_finding, degrade_confidence_for_proxy
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding


def check_hdr_csp_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """HDR-CSP-001 : CSP absente sur page HTML. FAIL."""
    overview = http_data.get("overview", {})
    if overview.get("content_profile", "unknown") != "html_page":
        return None

    preferred_scheme = overview.get("preferred_scheme")
    if not preferred_scheme:
        return None

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None

    headers = http_result.get("headers", {})
    csp_header = headers.get("Content-Security-Policy") or headers.get("content-security-policy")

    if not csp_header:
        return build_finding(
            rule_id="HDR-CSP-001",
            category="headers",
            title="Content-Security-Policy absente",
            status="FAIL",
            severity="medium",
            confidence="certain",
            applicability="applicable",
            description="Le header Content-Security-Policy est absent sur une page HTML.",
            impact="Vulnerable aux attaques XSS et injection de contenu.",
            remediation="Ajouter un header Content-Security-Policy restrictif.",
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "headers",
            },
            references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"],
            tags=["csp", "headers", "xss"],
        )

    return None


def check_hdr_csp_002(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """HDR-CSP-002 : CSP trop permissive. WARN au maximum, jamais FAIL."""
    overview = http_data.get("overview", {})
    if overview.get("content_profile", "unknown") != "html_page":
        return None

    preferred_scheme = overview.get("preferred_scheme")
    if not preferred_scheme:
        return None

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None

    headers = http_result.get("headers", {})
    csp_header = headers.get("Content-Security-Policy") or headers.get("content-security-policy")

    if not csp_header:
        return None

    csp_lower = csp_header.lower()
    found_patterns = [p for p in CSP_PERMISSIVE_PATTERNS if p in csp_lower]

    if found_patterns:
        proxy_suspected = overview.get("proxy_suspected", False)
        confidence = degrade_confidence_for_proxy("medium", proxy_suspected)

        return build_finding(
            rule_id="HDR-CSP-002",
            category="headers",
            title="Content-Security-Policy trop permissive",
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=f"CSP presente mais contient des directives permissives: {', '.join(found_patterns)}",
            impact="La protection CSP est affaiblie.",
            remediation="Restreindre les directives CSP (eviter 'unsafe-inline', '*', etc.).",
            evidence=Evidence(
                type="header",
                value=csp_header,
                source="response.headers",
                excerpt=f"Motifs permissifs detectes: {', '.join(found_patterns)}",
            ),
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "headers",
            },
            references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"],
            tags=["csp", "headers"],
        )

    return None


def check_hdr_nosniff_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """HDR-NOSNIFF-001 : X-Content-Type-Options absent ou invalide. WARN."""
    overview = http_data.get("overview", {})
    preferred_scheme = overview.get("preferred_scheme")
    if not preferred_scheme:
        return None

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None

    headers = http_result.get("headers", {})
    nosniff = headers.get("X-Content-Type-Options") or headers.get("x-content-type-options")

    if not nosniff or nosniff.lower() != "nosniff":
        return build_finding(
            rule_id="HDR-NOSNIFF-001",
            category="headers",
            title="X-Content-Type-Options absent ou invalide",
            status="WARN",
            severity="low",
            confidence="certain",
            applicability="applicable",
            description="Le header X-Content-Type-Options: nosniff est absent.",
            impact="Vulnerable aux attaques MIME sniffing.",
            remediation="Ajouter le header: X-Content-Type-Options: nosniff",
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "headers",
            },
            references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options"],
            tags=["nosniff", "headers"],
        )

    return None


def check_hdr_server_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """HDR-SERVER-001 : bannière Server exposee. WARN (degradee si proxy suspecte)."""
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")
    if not preferred_scheme:
        return None

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None

    headers = http_result.get("headers", {})
    server = headers.get("Server") or headers.get("server")

    if server:
        confidence = degrade_confidence_for_proxy("high", proxy_suspected)

        return build_finding(
            rule_id="HDR-SERVER-001",
            category="headers",
            title="Banniere Server exposee",
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=f"Le header Server expose des informations: {server}",
            impact="Fuite d'information sur la technologie serveur.",
            remediation="Configurer le serveur pour masquer ou minimiser le header Server.",
            evidence=Evidence(
                type="header",
                value=server,
                source="response.headers",
            ),
            location={
                "url": http_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": preferred_scheme,
                "path": target.get("requested_path"),
                "component": "headers",
            },
            tags=["server", "headers", "information_leak"],
        )

    return None


def check_hdr_cache_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """HDR-CACHE-001 : Cache-Control absent ou permissif sur une page HTML
    potentiellement porteuse de contenu utilisateur. WARN, confiance
    heuristique (impossible de savoir avec certitude si la page contient
    des donnees sensibles sans connaitre le contexte metier)."""
    overview = http_data.get("overview", {})
    if overview.get("content_profile", "unknown") != "html_page":
        return None

    preferred_scheme = overview.get("preferred_scheme")
    if not preferred_scheme:
        return None

    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None

    headers = http_result.get("headers", {})
    cache_control = headers.get("Cache-Control") or headers.get("cache-control")
    cache_control_lower = (cache_control or "").lower()

    has_safe_directive = any(d in cache_control_lower for d in CACHE_CONTROL_SAFE_DIRECTIVES)
    if cache_control is not None and has_safe_directive:
        return None

    return build_finding(
        rule_id="HDR-CACHE-001",
        category="headers",
        title="Cache-Control absent ou permissif",
        status="WARN",
        severity="low",
        confidence="medium",
        applicability="applicable",
        description=(
            "Le header Cache-Control est absent ou ne restreint pas explicitement la "
            f"mise en cache (valeur observee : {cache_control!r})."
        ),
        impact="Du contenu potentiellement sensible pourrait etre conserve par des caches partages.",
        remediation="Definir Cache-Control: no-store (ou private) sur les reponses porteuses de donnees utilisateur.",
        evidence=Evidence(type="header", value=cache_control or "(absent)", source="response.headers"),
        location={
            "url": http_result.get("requested_url"),
            "host": target.get("normalized_host"),
            "port": target.get("requested_port"),
            "scheme": preferred_scheme,
            "path": target.get("requested_path"),
            "component": "headers",
        },
        references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control"],
        tags=["cache", "headers"],
    )


def run_headers_checks(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks headers."""
    findings = []

    f = check_hdr_csp_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_hdr_csp_002(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_hdr_nosniff_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_hdr_server_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_hdr_cache_001(http_data, target, profile)
    if f:
        findings.append(f)

    return findings
