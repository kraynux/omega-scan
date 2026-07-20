# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Checks d'exposition (EXR-*).
Section 13 de la spec.
Évalue : chemins admin, fichiers sensibles, backups.
"""

from typing import List, Dict, Any, Optional
from models.finding import Finding
from models.evidence import Evidence
from checks.base import build_finding, degrade_confidence_for_proxy, degrade_confidence_for_catchall


def check_exr_admin_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    EXR-ADMIN-001 : Chemin admin accessible sans authentification.
    WARN si un chemin admin répond 200 sans protection.
    """
    findings = []
    path_context = http_data.get("overview", {}).get("path_probe_context", [])
    proxy_suspected = http_data.get("overview", {}).get("proxy_suspected", False)
    catch_all_suspected = http_data.get("overview", {}).get("catch_all_suspected", False)
    
    admin_paths = ["/admin", "/administrator", "/wp-admin", "/phpmyadmin", "/manager"]
    
    for probe in path_context:
        if probe["path"] in admin_paths and probe["reason"] == "ok":
            confidence = "high"
            confidence = degrade_confidence_for_proxy(confidence, proxy_suspected)
            confidence = degrade_confidence_for_catchall(confidence, catch_all_suspected)
            
            findings.append(build_finding(
                rule_id="EXR-ADMIN-001",
                category="exposure",
                title=f"Chemin admin accessible : {probe['path']}",
                status="WARN",
                severity="medium",
                confidence=confidence,
                applicability="applicable",
                description=f"Le chemin {probe['path']} est accessible sans authentification.",
                impact="Interface d'administration potentiellement exposée.",
                remediation="Restreindre l'accès par IP ou exiger une authentification forte.",
                evidence=Evidence(
                    type="status_code",
                    value=f"{probe['path']} → {probe['status_code']}",
                    source="path_probe",
                ),
                location={
                    "url": f"{http_data.get('overview', {}).get('preferred_scheme', 'https')}://{target.get('normalized_host')}{probe['path']}",
                    "host": target.get("normalized_host"),
                    "port": target.get("requested_port"),
                    "scheme": http_data.get("overview", {}).get("preferred_scheme"),
                    "path": probe["path"],
                    "component": "exposure",
                },
                tags=["admin", "exposure"],
            ))
    
    return findings


def check_exr_sensitive_001(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    EXR-SENSITIVE-001 : Fichier sensible accessible.
    FAIL si .env, config.php, .git/config, etc. répondent 200.
    """
    findings = []
    path_context = http_data.get("overview", {}).get("path_probe_context", [])
    proxy_suspected = http_data.get("overview", {}).get("proxy_suspected", False)
    catch_all_suspected = http_data.get("overview", {}).get("catch_all_suspected", False)
    
    sensitive_paths = ["/.env", "/.git/config", "/.svn/entries", "/wp-config.php", "/config.php"]
    
    for probe in path_context:
        if probe["path"] in sensitive_paths and probe["reason"] == "ok":
            confidence = "certain"
            confidence = degrade_confidence_for_proxy(confidence, proxy_suspected)
            confidence = degrade_confidence_for_catchall(confidence, catch_all_suspected)
            
            findings.append(build_finding(
                rule_id="EXR-SENSITIVE-001",
                category="exposure",
                title=f"Fichier sensible accessible : {probe['path']}",
                status="FAIL",
                severity="high",
                confidence=confidence,
                applicability="applicable",
                description=f"Le fichier {probe['path']} est accessible publiquement.",
                impact="Fuite de données sensibles (credentials, configuration).",
                remediation="Bloquer l'accès à ces fichiers via la configuration du serveur web.",
                evidence=Evidence(
                    type="status_code",
                    value=f"{probe['path']} → {probe['status_code']}",
                    source="path_probe",
                ),
                location={
                    "url": f"{http_data.get('overview', {}).get('preferred_scheme', 'https')}://{target.get('normalized_host')}{probe['path']}",
                    "host": target.get("normalized_host"),
                    "port": target.get("requested_port"),
                    "scheme": http_data.get("overview", {}).get("preferred_scheme"),
                    "path": probe["path"],
                    "component": "exposure",
                },
                tags=["sensitive", "exposure", "information_leak"],
            ))
    
    return findings


def run_exposure_checks(
    http_data: Dict[str, Any],
    target: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Finding]:
    """
    Exécute tous les checks d'exposition.
    """
    findings = []
    findings.extend(check_exr_admin_001(http_data, target, profile))
    findings.extend(check_exr_sensitive_001(http_data, target, profile))
    return findings
