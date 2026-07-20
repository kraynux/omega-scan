# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Checks de fuites d'information (INF-*).
Section 13 de la spec.
Évalue : bannières, erreurs, stack traces, robots, headers bavards.
Toutes soumises à la logique proxy (section 7).
"""

from typing import List, Dict, Any, Optional
from models.finding import Finding
from models.evidence import Evidence
from checks.base import build_finding, degrade_confidence_for_proxy


# Patterns de détection d'erreurs et stack traces
ERROR_PATTERNS = [
    "exception",
    "stack trace",
    "error on line",
    "fatal error",
    "uncaught exception",
    "traceback (most recent call last)",
    "at java.",
    "at org.",
    "in /var/www/",
    "in /home/",
]

# Headers bavards
VERBOSE_HEADERS = [
    "x-aspnet-version",
    "x-aspnetmvc-version",
    "x-powered-by",
    "x-debug",
    "x-server",
    "x-backend-server",
]


def check_inf_banner_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    INF-BANNER-001 : Bannières serveur exposées.
    WARN si Server ou X-Powered-By présents (dégradé si proxy_suspected).
    """
    findings = []
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")
    
    if not preferred_scheme:
        return findings
    
    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return findings
    
    headers = http_result.get("headers", {})
    
    # Server
    server = headers.get("Server") or headers.get("server")
    if server:
        confidence = degrade_confidence_for_proxy("high", proxy_suspected)
        findings.append(build_finding(
            rule_id="INF-BANNER-001",
            category="information_leak",
            title="Bannière Server exposée",
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=f"Le header Server expose des informations : {server}",
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
                "component": "information_leak",
            },
            tags=["banner", "information_leak"],
        ))
    
    # X-Powered-By
    powered_by = headers.get("X-Powered-By") or headers.get("x-powered-by")
    if powered_by:
        confidence = degrade_confidence_for_proxy("high", proxy_suspected)
        findings.append(build_finding(
            rule_id="INF-BANNER-001",
            category="information_leak",
            title="Bannière X-Powered-By exposée",
            status="WARN",
            severity="low",
            confidence=confidence,
            applicability="applicable",
            description=f"Le header X-Powered-By expose des informations : {powered_by}",
            impact="Fuite d'information sur le framework/technologie.",
            remediation="Supprimer le header X-Powered-By de la configuration.",
            evidence=Evidence(
                type="header",
                value=powered_by,
                source="response.headers",
            ),
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
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    INF-ERROR-001 : Messages d'erreur détaillés exposés.
    WARN si patterns d'erreur détectés dans le body_preview.
    """
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")
    
    if not preferred_scheme:
        return None
    
    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None
    
    body_preview = http_result.get("body_preview", {}).get("text_preview", "").lower()
    
    # Chercher des patterns d'erreur
    found_patterns = [p for p in ERROR_PATTERNS if p in body_preview]
    
    if found_patterns:
        confidence = degrade_confidence_for_proxy("medium", proxy_suspected)
        return build_finding(
            rule_id="INF-ERROR-001",
            category="information_leak",
            title="Messages d'erreur détaillés exposés",
            status="WARN",
            severity="medium",
            confidence=confidence,
            applicability="applicable",
            description=f"Des messages d'erreur détaillés sont visibles dans la réponse : {', '.join(found_patterns[:3])}",
            impact="Fuite d'information sur l'implémentation, potentiellement exploitable.",
            remediation="Configurer le serveur pour afficher des pages d'erreur génériques en production.",
            evidence=Evidence(
                type="body_content",
                value=f"Patterns détectés : {', '.join(found_patterns[:3])}",
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
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    INF-STACK-001 : Stack traces exposés.
    FAIL si stack traces détectés (plus sévère que INF-ERROR-001).
    """
    overview = http_data.get("overview", {})
    proxy_suspected = overview.get("proxy_suspected", False)
    preferred_scheme = overview.get("preferred_scheme")
    
    if not preferred_scheme:
        return None
    
    http_result = http_data.get(preferred_scheme, {})
    if not http_result.get("ok"):
        return None
    
    body_preview = http_result.get("body_preview", {}).get("text_preview", "").lower()
    
    # Patterns spécifiques aux stack traces
    stack_patterns = [
        "traceback (most recent call last)",
        "at java.",
        "at org.",
        "stack trace",
        "exception in thread",
    ]
    
    found_patterns = [p for p in stack_patterns if p in body_preview]
    
    if found_patterns:
        confidence = degrade_confidence_for_proxy("high", proxy_suspected)
        return build_finding(
            rule_id="INF-STACK-001",
            category="information_leak",
            title="Stack trace exposé",
            status="FAIL",
            severity="high",
            confidence=confidence,
            applicability="applicable",
            description=f"Un stack trace est visible dans la réponse : {', '.join(found_patterns[:2])}",
            impact="Fuite d'information critique sur l'implémentation, paths internes, versions.",
            remediation="Désactiver l'affichage des stack traces en production. Utiliser des pages d'erreur génériques.",
            evidence=Evidence(
                type="body_content",
                value=f"Stack trace détecté : {', '.join(found_patterns[:2])}",
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
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    INF-ROBOTS-001 : Présence de /robots.txt.
    INFO (signal, pas fail).
    """
    path_context = http_data.get("overview", {}).get("path_probe_context", [])
    
    # Chercher /robots.txt dans le path_probe_context
    robots_probe = next((p for p in path_context if p["path"] == "/robots.txt"), None)
    
    if robots_probe and robots_probe["reason"] == "ok":
        return build_finding(
            rule_id="INF-ROBOTS-001",
            category="information_leak",
            title="Fichier robots.txt présent",
            status="OK",
            severity="info",
            confidence="certain",
            applicability="applicable",
            description="Le fichier /robots.txt est présent et peut révéler des chemins sensibles.",
            impact="Fuite d'information mineure sur la structure du site.",
            remediation="Vérifier que /robots.txt ne liste pas de chemins sensibles ou administratifs.",
            evidence=Evidence(
                type="status_code",
                value=f"/robots.txt → {robots_probe['status_code']}",
                source="path_probe",
            ),
            location={
                "url": f"{http_data.get('overview', {}).get('preferred_scheme', 'https')}://{target.get('normalized_host')}/robots.txt",
                "host": target.get("normalized_host"),
                "port": target.get("requested_port"),
                "scheme": http_data.get("overview", {}).get("preferred_scheme"),
                "path": "/robots.txt",
                "component": "information_leak",
            },
            tags=["robots", "information_leak"],
        )
    
    return None


def check_inf_header_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    INF-HEADER-001 : Headers bavards (X-AspNet-Version, X-Debug, etc.).
    WARN si headers techniques exposés.
    """
    findings = []
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
            # Ne pas dupliquer si déjà traité par INF-BANNER-001
            if verbose_header in ("x-powered-by",):
                continue
            
            value = headers_lower[verbose_header]
            confidence = degrade_confidence_for_proxy("medium", proxy_suspected)
            
            findings.append(build_finding(
                rule_id="INF-HEADER-001",
                category="information_leak",
                title=f"Header technique exposé : {verbose_header}",
                status="WARN",
                severity="low",
                confidence=confidence,
                applicability="applicable",
                description=f"Le header {verbose_header} expose des informations techniques : {value}",
                impact="Fuite d'information sur l'implémentation.",
                remediation=f"Supprimer le header {verbose_header} de la configuration.",
                evidence=Evidence(
                    type="header",
                    value=f"{verbose_header}: {value}",
                    source="response.headers",
                ),
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
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    Exécute tous les checks de fuites d'information.
    """
    findings = []
    
    # INF-BANNER-001
    findings.extend(check_inf_banner_001(http_data, target, profile))
    
    # INF-ERROR-001
    f = check_inf_error_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # INF-STACK-001
    f = check_inf_stack_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # INF-ROBOTS-001
    f = check_inf_robots_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # INF-HEADER-001
    findings.extend(check_inf_header_001(http_data, target, profile))
    
    return findings
