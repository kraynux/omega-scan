# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks d'exposition (EXR-*) : chemins admin, fichiers sensibles."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.checks.exposure.policies import JUDGED_ADMIN_PATHS, JUDGED_SENSITIVE_PATHS
from omega_scan.domain.findings.builders import (
    build_finding,
    degrade_confidence_for_catchall,
    degrade_confidence_for_proxy,
)
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding


def check_exr_admin_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """EXR-ADMIN-001 : chemin admin accessible sans authentification. WARN."""
    findings = []
    overview = http_data.get("overview", {})
    path_context = overview.get("path_probe_context", [])
    proxy_suspected = overview.get("proxy_suspected", False)
    catch_all_suspected = overview.get("catch_all_suspected", False)

    for probe in path_context:
        if probe["path"] in JUDGED_ADMIN_PATHS and probe["reason"] == "ok":
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
                impact="Interface d'administration potentiellement exposee.",
                remediation="Restreindre l'acces par IP ou exiger une authentification forte.",
                evidence=Evidence(
                    type="status_code",
                    value=f"{probe['path']} -> {probe['status_code']}",
                    source="path_probe",
                ),
                location={
                    "url": f"{overview.get('preferred_scheme', 'https')}://{target.get('normalized_host')}{probe['path']}",
                    "host": target.get("normalized_host"),
                    "port": target.get("requested_port"),
                    "scheme": overview.get("preferred_scheme"),
                    "path": probe["path"],
                    "component": "exposure",
                },
                tags=["admin", "exposure"],
            ))

    return findings


def check_exr_sensitive_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """EXR-SENSITIVE-001 : fichier sensible accessible. FAIL."""
    findings = []
    overview = http_data.get("overview", {})
    path_context = overview.get("path_probe_context", [])
    proxy_suspected = overview.get("proxy_suspected", False)
    catch_all_suspected = overview.get("catch_all_suspected", False)

    for probe in path_context:
        if probe["path"] in JUDGED_SENSITIVE_PATHS and probe["reason"] == "ok":
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
                impact="Fuite de donnees sensibles (credentials, configuration).",
                remediation="Bloquer l'acces a ces fichiers via la configuration du serveur web.",
                evidence=Evidence(
                    type="status_code",
                    value=f"{probe['path']} -> {probe['status_code']}",
                    source="path_probe",
                ),
                location={
                    "url": f"{overview.get('preferred_scheme', 'https')}://{target.get('normalized_host')}{probe['path']}",
                    "host": target.get("normalized_host"),
                    "port": target.get("requested_port"),
                    "scheme": overview.get("preferred_scheme"),
                    "path": probe["path"],
                    "component": "exposure",
                },
                tags=["sensitive", "exposure", "information_leak"],
            ))

    return findings


def run_exposure_checks(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks d'exposition."""
    findings = []
    findings.extend(check_exr_admin_001(http_data, target, profile))
    findings.extend(check_exr_sensitive_001(http_data, target, profile))
    return findings
