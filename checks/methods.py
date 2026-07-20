# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Checks des méthodes HTTP (MTH-*).
Section 13 de la spec.
Évalue : OPTIONS, TRACE, PUT, DELETE, PATCH, CONNECT.
"""

from typing import List, Dict, Any, Optional
from models.finding import Finding
from checks.base import build_finding, degrade_confidence_for_proxy


def _build_method_finding(
    method: str,
    reason: str,
    target: Dict[str, Any],
    profile: Dict[str, Any],
    http_data: Dict[str, Any],
) -> Optional[Finding]:
    # Pas de finding si la méthode est explicitement désactivée ou non implémentée
    if reason in ("disabled", "not_implemented"):
        return None
        
    proxy_suspected = http_data.get("overview", {}).get("proxy_suspected", False)
    preferred_scheme = http_data.get("overview", {}).get("preferred_scheme", "https")
    
    rules = {
        "OPTIONS": {
            "rule_id": "MTH-OPTIONS-001",
            "title": "Méthode HTTP OPTIONS activée",
            "severity": "info",
            "default_confidence": "certain",
            "description": "La méthode OPTIONS est activée et peut révéler les méthodes autorisées.",
            "impact": "Fuite d'information mineure sur la configuration du serveur.",
            "remediation": "Désactiver la méthode OPTIONS si elle n'est pas nécessaire.",
        },
        "TRACE": {
            "rule_id": "MTH-TRACE-001",
            "title": "Méthode HTTP TRACE activée",
            "severity": "medium",
            "default_confidence": "certain",
            "description": "La méthode TRACE est activée, ce qui peut faciliter les attaques Cross-Site Tracing (XST).",
            "impact": "Risque de vol de cookies ou d'identifiants via XST.",
            "remediation": "Désactiver la méthode TRACE dans la configuration du serveur web.",
        },
        "PUT": {
            "rule_id": "MTH-PUT-001",
            "title": "Méthode HTTP PUT activée",
            "severity": "high",
            "default_confidence": "certain",
            "description": "La méthode PUT est activée, permettant potentiellement l'upload de fichiers.",
            "impact": "Risque de dépôt de contenu malveillant ou de modification de ressources.",
            "remediation": "Désactiver la méthode PUT sauf si explicitement requise et sécurisée.",
        },
        "DELETE": {
            "rule_id": "MTH-DELETE-001",
            "title": "Méthode HTTP DELETE activée",
            "severity": "high",
            "default_confidence": "certain",
            "description": "La méthode DELETE est activée, permettant potentiellement la suppression de ressources.",
            "impact": "Risque de suppression non autorisée de données.",
            "remediation": "Désactiver la méthode DELETE sauf si explicitement requise et sécurisée.",
        },
        "PATCH": {
            "rule_id": "MTH-PATCH-001",
            "title": "Méthode HTTP PATCH activée",
            "severity": "medium",
            "default_confidence": "certain",
            "description": "La méthode PATCH est activée, permettant la modification partielle de ressources.",
            "impact": "Risque de modification non autorisée de données.",
            "remediation": "Désactiver la méthode PATCH sauf si explicitement requise et sécurisée.",
        },
        "CONNECT": {
            "rule_id": "MTH-CONNECT-001",
            "title": "Méthode HTTP CONNECT activée",
            "severity": "high",
            "default_confidence": "certain",
            "description": "La méthode CONNECT est activée, permettant l'établissement de tunnels TCP.",
            "impact": "Risque d'utilisation du serveur comme proxy ouvert pour des attaques.",
            "remediation": "Restreindre la méthode CONNECT aux seuls ports nécessaires (ex: 443) ou la désactiver.",
        }
    }
    
    if method not in rules:
        return None
        
    rule = rules[method]
    base_url = f"{preferred_scheme}://{target.get('normalized_host', '')}"
    
    location = {
        "url": base_url,
        "host": target.get("normalized_host"),
        "port": target.get("requested_port"),
        "scheme": preferred_scheme,
        "path": target.get("requested_path", "/"),
        "component": "methods",
    }
    
    if reason == "protected":
        return build_finding(
            rule_id=rule["rule_id"],
            category="methods",
            title=rule["title"] + " (protégée)",
            status="N/A",
            severity="info",
            confidence="high",
            applicability="not_applicable",
            description=rule["description"] + " Cependant, elle semble protégée par authentification.",
            impact="Risque mitigé par la présence d'une authentification.",
            remediation="Vérifier que l'authentification est robuste.",
            location=location,
            tags=["methods", method.lower()],
        )
        
    elif reason == "enabled":
        confidence = degrade_confidence_for_proxy(rule["default_confidence"], proxy_suspected)
        return build_finding(
            rule_id=rule["rule_id"],
            category="methods",
            title=rule["title"],
            status="WARN",
            severity=rule["severity"],
            confidence=confidence,
            applicability="applicable",
            description=rule["description"],
            impact=rule["impact"],
            remediation=rule["remediation"],
            location=location,
            tags=["methods", method.lower()],
        )
        
    elif reason in ("unknown", "error"):
        return build_finding(
            rule_id=rule["rule_id"],
            category="methods",
            title=rule["title"] + " (statut incertain)",
            status="WARN",
            severity="low",
            confidence="low",
            applicability="conditional",
            description=rule["description"] + " Le statut exact n'a pas pu être déterminé clairement.",
            impact=rule["impact"],
            remediation=rule["remediation"],
            location=location,
            tags=["methods", method.lower()],
        )
        
    return None


def run_methods_checks(
    methods_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
    http_data: Dict[str, Any],
) -> List[Finding]:
    """
    Exécute tous les checks de méthodes HTTP.
    """
    findings = []
    for method_test in methods_data.get("methods_tested", []):
        finding = _build_method_finding(
            method=method_test["method"],
            reason=method_test["reason"],
            target=target,
            profile=profile,
            http_data=http_data,
        )
        if finding:
            findings.append(finding)
            
    return findings
