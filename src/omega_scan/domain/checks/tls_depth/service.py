# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks de profondeur TLS (TLS-*) : version de protocole, suite cryptographique.

Categorie "transport" (pas une categorie dediee) : ces regles completent les
TRN-* deja existantes sur la meme posture de securite du transport. Ne juge
que si le handshake a reellement reussi (tls_data["handshake_success"]) : un
profil quick (tls_checks_enabled=False) ne tente jamais le handshake,
ces regles ne produisent alors naturellement aucun finding — le gating est
deja assure par infrastructure/network/httpx_tls_prober.py, jamais
reimplemente ici."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.checks.tls_depth.policies import OBSOLETE_TLS_VERSIONS, WEAK_CIPHER_PATTERNS
from omega_scan.domain.findings.builders import build_finding
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding
from omega_scan.shared.i18n import _


def _location(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "url": None,
        "host": target.get("normalized_host"),
        "port": target.get("requested_port"),
        "scheme": "https",
        "path": target.get("requested_path"),
        "component": "tls_depth",
    }


def check_tls_version_001(
    tls_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """TLS-VERSION-001 : protocole TLS obsolete (< TLSv1.2). FAIL."""
    if not tls_data.get("handshake_success"):
        return None

    version = tls_data.get("tls_version")
    if version not in OBSOLETE_TLS_VERSIONS:
        return None

    return build_finding(
        rule_id="TLS-VERSION-001",
        category="transport",
        title=_("Protocole TLS obsolète : {version}").format(version=version),
        status="FAIL",
        severity="high",
        confidence="certain",
        applicability="applicable",
        description=_("Le service négocie {version}, un protocole obsolète et vulnérable.").format(version=version),
        impact=_("Vulnérable aux attaques connues sur les protocoles TLS anciens (ex. POODLE, "
                 "BEAST)."),
        remediation=_("Désactiver les protocoles antérieurs à TLSv1.2 côté serveur."),
        evidence=Evidence(type="tls_field", value=str(version), source="tls.handshake"),
        location=_location(target),
        references=["https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security"],
        tags=["tls", "transport"],
    )


def check_tls_cipher_001(
    tls_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """TLS-CIPHER-001 : suite cryptographique manifestement faible. WARN."""
    if not tls_data.get("handshake_success"):
        return None

    cipher = tls_data.get("cipher")
    if not cipher:
        return None

    cipher_upper = cipher.upper()
    if not any(pattern in cipher_upper for pattern in WEAK_CIPHER_PATTERNS):
        return None

    return build_finding(
        rule_id="TLS-CIPHER-001",
        category="transport",
        title=_("Suite cryptographique faible : {cipher}").format(cipher=cipher),
        status="WARN",
        severity="medium",
        confidence="medium",
        applicability="applicable",
        description=_("La suite cryptographique négociée ({cipher}) est considérée faible.").format(cipher=cipher),
        impact=_("Le chiffrement peut être cassé ou affaibli face à un attaquant motivé."),
        remediation=_("Restreindre la configuration TLS du serveur aux suites modernes (ex. "
                      "AEAD/GCM)."),
        evidence=Evidence(type="tls_field", value=cipher, source="tls.handshake"),
        location=_location(target),
        tags=["tls", "cipher", "transport"],
    )


def run_tls_depth_checks(
    tls_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks de profondeur TLS."""
    findings: list[Finding] = []
    f = check_tls_version_001(tls_data, target, profile)
    if f:
        findings.append(f)
    f = check_tls_cipher_001(tls_data, target, profile)
    if f:
        findings.append(f)
    return findings
