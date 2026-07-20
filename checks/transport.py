# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Checks transport (TRN-*).
Section 13 de la spec.
Évalue : HTTPS, redirection HTTP→HTTPS, HSTS.
"""

from typing import List, Dict, Any, Optional
from models.finding import Finding
from models.evidence import Evidence
from checks.base import build_finding, degrade_confidence_for_proxy


def check_trn_http_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    TRN-HTTP-001 : HTTP accessible sans redirection vers HTTPS.
    WARN si HTTP répond sans rediriger vers HTTPS.
    """
    http_result = http_data.get("http", {})
    
    if not http_result.get("attempted") or not http_result.get("ok"):
        return None  # HTTP n'est pas accessible, pas de finding
    
    # Vérifier si HTTP redirige vers HTTPS
    redirect_chain = http_result.get("redirect_chain", [])
    final_url = http_result.get("final_url", "")
    
    if final_url.startswith("https://"):
        return None  # HTTP redirige vers HTTPS, OK
    
    # HTTP accessible sans redirection HTTPS
    return build_finding(
        rule_id="TRN-HTTP-001",
        category="transport",
        title="HTTP accessible sans redirection vers HTTPS",
        status="WARN",
        severity="medium",
        confidence="certain",
        applicability="applicable",
        description="Le service est accessible en HTTP sans redirection automatique vers HTTPS.",
        impact="Les données transitent en clair, exposées à l'interception.",
        remediation="Configurer une redirection permanente (301) de HTTP vers HTTPS.",
        evidence=Evidence(
            type="status_code",
            value=f"HTTP {http_result.get('status_code')} sur {http_result.get('requested_url')}",
            source="http_probe",
            excerpt=f"Final URL: {final_url}",
        ),
        location={
            "url": http_result.get("requested_url"),
            "host": target.get("normalized_host"),
            "port": target.get("requested_port") or 80,
            "scheme": "http",
            "path": target.get("requested_path"),
            "component": "transport",
        },
        references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections"],
        tags=["http", "redirect", "transport"],
    )


def check_trn_https_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    TRN-HTTPS-001 : HTTPS non accessible.
    FAIL si HTTPS n'est pas joignable.
    """
    https_result = http_data.get("https", {})
    
    if not https_result.get("attempted"):
        return None  # HTTPS n'a pas été testé (profil quick par exemple)
    
    if https_result.get("ok"):
        return None  # HTTPS fonctionne, OK
    
    # HTTPS non accessible
    return build_finding(
        rule_id="TRN-HTTPS-001",
        category="transport",
        title="HTTPS non accessible",
        status="FAIL",
        severity="high",
        confidence="certain",
        applicability="applicable",
        description="Le service n'est pas accessible en HTTPS.",
        impact="Aucune communication chiffrée possible, données exposées.",
        remediation="Configurer HTTPS avec un certificat valide.",
        evidence=Evidence(
            type="error",
            value=https_result.get("error", "HTTPS injoignable"),
            source="http_probe",
            excerpt=f"URL testée: {https_result.get('requested_url')}",
        ),
        location={
            "url": https_result.get("requested_url"),
            "host": target.get("normalized_host"),
            "port": target.get("requested_port") or 443,
            "scheme": "https",
            "path": target.get("requested_path"),
            "component": "transport",
        },
        references=["https://letsencrypt.org/"],
        tags=["https", "transport", "encryption"],
    )


def check_trn_hsts_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    TRN-HSTS-001 : HSTS absent.
    FAIL si HSTS absent (sauf local-lab sur loopback/LAN).
    """
    https_result = http_data.get("https", {})
    
    if not https_result.get("ok"):
        return None  # HTTPS ne fonctionne pas, HSTS non applicable
    
    headers = https_result.get("headers", {})
    hsts_header = headers.get("Strict-Transport-Security") or headers.get("strict-transport-security")
    
    # Vérifier si on est en local-lab sur loopback/LAN
    profile_name = profile.get("profile_name", "standard")
    scope_kind = target.get("scope_kind", "public")
    
    if profile_name == "local-lab" and scope_kind in ("loopback", "link_local", "private_lan"):
        # HSTS non applicable en local-lab sur LAN
        return build_finding(
            rule_id="TRN-HSTS-001",
            category="transport",
            title="HSTS non évalué (profil local-lab sur LAN)",
            status="N/A",
            severity="info",
            confidence="certain",
            applicability="not_applicable",
            description="HSTS n'est pas évalué en profil local-lab sur loopback/LAN.",
            impact="Aucun impact en environnement local contrôlé.",
            remediation="Aucune action requise.",
            location={
                "url": https_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port") or 443,
                "scheme": "https",
                "path": target.get("requested_path"),
                "component": "transport",
            },
            tags=["hsts", "transport", "local-lab"],
        )
    
    if not hsts_header:
        return build_finding(
            rule_id="TRN-HSTS-001",
            category="transport",
            title="Header HSTS absent",
            status="FAIL",
            severity="medium",
            confidence="certain",
            applicability="applicable",
            description="Le header Strict-Transport-Security est absent.",
            impact="Les navigateurs ne forcent pas HTTPS, vulnérable aux attaques downgrade.",
            remediation="Ajouter le header: Strict-Transport-Security: max-age=31536000; includeSubDomains",
            location={
                "url": https_result.get("requested_url"),
                "host": target.get("normalized_host"),
                "port": target.get("requested_port") or 443,
                "scheme": "https",
                "path": target.get("requested_path"),
                "component": "transport",
            },
            references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security"],
            tags=["hsts", "transport"],
        )
    
    return None  # HSTS présent, OK


def check_trn_hsts_002(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> Optional[Finding]:
    """
    TRN-HSTS-002 : HSTS max-age faible.
    WARN si max-age < 1 an (31536000 secondes).
    """
    https_result = http_data.get("https", {})
    
    if not https_result.get("ok"):
        return None
    
    headers = https_result.get("headers", {})
    hsts_header = headers.get("Strict-Transport-Security") or headers.get("strict-transport-security")
    
    if not hsts_header:
        return None  # Pas de HSTS, géré par TRN-HSTS-001
    
    # Parser max-age
    try:
        parts = hsts_header.split(";")
        max_age = None
        for part in parts:
            part = part.strip()
            if part.lower().startswith("max-age="):
                max_age = int(part.split("=")[1].strip())
                break
        
        if max_age is not None and max_age < 31536000:  # < 1 an
            return build_finding(
                rule_id="TRN-HSTS-002",
                category="transport",
                title="HSTS max-age faible",
                status="WARN",
                severity="low",
                confidence="certain",
                applicability="applicable",
                description=f"Le max-age HSTS est de {max_age} secondes (< 1 an).",
                impact="La protection HSTS est de courte durée.",
                remediation="Augmenter max-age à au moins 31536000 (1 an).",
                evidence=Evidence(
                    type="header",
                    value=hsts_header,
                    source="response.headers",
                    excerpt=f"max-age={max_age}",
                ),
                location={
                    "url": https_result.get("requested_url"),
                    "host": target.get("normalized_host"),
                    "port": target.get("requested_port") or 443,
                    "scheme": "https",
                    "path": target.get("requested_path"),
                    "component": "transport",
                },
                references=["https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security"],
                tags=["hsts", "transport"],
            )
    except (ValueError, IndexError):
        pass
    
    return None


def run_transport_checks(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    Exécute tous les checks transport.
    """
    findings = []
    
    # TRN-HTTP-001
    f = check_trn_http_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # TRN-HTTPS-001
    f = check_trn_https_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # TRN-HSTS-001
    f = check_trn_hsts_001(http_data, target, profile)
    if f:
        findings.append(f)
    
    # TRN-HSTS-002
    f = check_trn_hsts_002(http_data, target, profile)
    if f:
        findings.append(f)
    
    return findings
