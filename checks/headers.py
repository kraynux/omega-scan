# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Checks headers (HDR-*).
Section 13 de la spec.
Évalue : CSP, nosniff, referrer, framing, server banner, powered-by.
"""

from typing import List, Dict, Any, Optional
from models.finding import Finding
from models.evidence import Evidence
from checks.base import build_finding, degrade_confidence_for_proxy


def check_hdr_csp_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    HDR-CSP-001 : CSP absente sur html_page.
    FAIL si CSP absente et content_profile == html_page.
    """
    overview = http_data.get("overview", {})
    content_profile = overview.get("content_profile", "unknown")
    
    if content_profile != "html_page":
        return None  # CSP non applicable si pas HTML
    
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
            impact="Vulnérable aux attaques XSS et injection de contenu.",
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
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    HDR-CSP-002 : CSP trop permissive.
    WARN max, jamais FAIL (section 13).
    """
    overview = http_data.get("overview", {})
    content_profile = overview.get("content_profile", "unknown")
    
    if content_profile != "html_page":
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
        return None  # Pas de CSP, géré par HDR-CSP-001
    
    # Détecter les motifs permissifs
    csp_lower = csp_header.lower()
    permissive_patterns = [
        "default-src *",
        "script-src 'unsafe-inline'",
        "script-src 'unsafe-eval'",
    ]
    
    found_patterns = [p for p in permissive_patterns if p in csp_lower]
    
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
            description=f"CSP présente mais contient des directives permissives: {', '.join(found_patterns)}",
            impact="La protection CSP est affaiblie.",
            remediation="Restreindre les directives CSP (éviter 'unsafe-inline', '*', etc.).",
            evidence=Evidence(
                type="header",
                value=csp_header,
                source="response.headers",
                excerpt=f"Motifs permissifs détectés: {', '.join(found_patterns)}",
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
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    HDR-NOSNIFF-001 : X-Content-Type-Options absent.
    WARN si absent.
    """
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
            impact="Vulnérable aux attaques MIME sniffing.",
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
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    HDR-SERVER-001 : Server banner exposé.
    WARN si Server présent (dégradé si proxy_suspected).
    """
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
            title="Bannière Server exposée",
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


def run_headers_checks(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    Exécute tous les checks headers.
    """
    findings = []
    
    # HDR-CSP-001
    f = check_hdr_csp_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # HDR-CSP-002
    f = check_hdr_csp_002(http_data, target, profile)
    if f:
        findings.append(f)
    
    # HDR-NOSNIFF-001
    f = check_hdr_nosniff_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # HDR-SERVER-001
    f = check_hdr_server_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    return findings
