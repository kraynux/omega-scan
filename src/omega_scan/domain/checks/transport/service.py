# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks transport (TRN-*) : HTTPS, redirection HTTP->HTTPS, HSTS."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.checks.transport.policies import HSTS_MIN_MAX_AGE_SECONDS
from omega_scan.domain.findings.builders import build_finding
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding
from omega_scan.shared.i18n import _


def check_trn_http_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """TRN-HTTP-001 : HTTP accessible sans redirection vers HTTPS. WARN."""
    http_result = http_data.get("http", {})

    if not http_result.get("attempted") or not http_result.get("ok"):
        return None

    final_url = http_result.get("final_url", "")
    if final_url.startswith("https://"):
        return None

    return build_finding(
        rule_id="TRN-HTTP-001",
        category="transport",
        title=_("HTTP accessible sans redirection vers HTTPS"),
        status="WARN",
        severity="medium",
        confidence="certain",
        applicability="applicable",
        description=_("Le service est accessible en HTTP sans redirection automatique vers HTTPS."),
        impact=_("Les données transitent en clair, exposées à l'interception."),
        remediation=_("Configurer une redirection permanente (301) de HTTP vers HTTPS."),
        evidence=Evidence(
            type="status_code",
            value=f"HTTP {http_result.get('status_code')} sur {http_result.get('requested_url')}",
            source="http_probe",
            excerpt=_("Final URL: {final_url}").format(final_url=final_url),
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
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """TRN-HTTPS-001 : HTTPS non accessible. FAIL."""
    https_result = http_data.get("https", {})

    if not https_result.get("attempted"):
        return None
    if https_result.get("ok"):
        return None

    return build_finding(
        rule_id="TRN-HTTPS-001",
        category="transport",
        title=_("HTTPS non accessible"),
        status="FAIL",
        severity="high",
        confidence="certain",
        applicability="applicable",
        description=_("Le service n'est pas accessible en HTTPS."),
        impact=_("Aucune communication chiffrée possible, données exposées."),
        remediation=_("Configurer HTTPS avec un certificat valide."),
        evidence=Evidence(
            type="error",
            value=https_result.get("error", "HTTPS injoignable"),
            source="http_probe",
            excerpt=_("URL testée: {get}").format(get=https_result.get('requested_url')),
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
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """TRN-HSTS-001 : HSTS absent. FAIL (N/A en local-lab sur loopback/LAN)."""
    https_result = http_data.get("https", {})

    if not https_result.get("ok"):
        return None

    headers = https_result.get("headers", {})
    hsts_header = headers.get("Strict-Transport-Security") or headers.get("strict-transport-security")

    profile_name = profile.get("profile_name", "standard")
    scope_kind = target.get("scope_kind", "public")

    if profile_name == "local-lab" and scope_kind in ("loopback", "link_local", "private_lan"):
        return build_finding(
            rule_id="TRN-HSTS-001",
            category="transport",
            title=_("HSTS non évalué (profil local-lab sur LAN)"),
            status="N/A",
            severity="info",
            confidence="certain",
            applicability="not_applicable",
            description=_("HSTS n'est pas évalué en profil local-lab sur loopback/LAN."),
            impact=_("Aucun impact en environnement local contrôlé."),
            remediation=_("Aucune action requise."),
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
            title=_("Header HSTS absent"),
            status="FAIL",
            severity="medium",
            confidence="certain",
            applicability="applicable",
            description=_("Le header Strict-Transport-Security est absent."),
            impact=_("Les navigateurs ne forcent pas HTTPS, vulnérable aux attaques downgrade."),
            remediation=_("Ajouter le header: Strict-Transport-Security: max-age=31536000; "
                          "includeSubDomains"),
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

    return None


def check_trn_hsts_002(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> Finding | None:
    """TRN-HSTS-002 : HSTS max-age faible (< 1 an). WARN."""
    https_result = http_data.get("https", {})

    if not https_result.get("ok"):
        return None

    headers = https_result.get("headers", {})
    hsts_header = headers.get("Strict-Transport-Security") or headers.get("strict-transport-security")

    if not hsts_header:
        return None

    try:
        parts = hsts_header.split(";")
        max_age = None
        for part in parts:
            part = part.strip()
            if part.lower().startswith("max-age="):
                max_age = int(part.split("=")[1].strip())
                break

        if max_age is not None and max_age < HSTS_MIN_MAX_AGE_SECONDS:
            return build_finding(
                rule_id="TRN-HSTS-002",
                category="transport",
                title=_("HSTS max-age faible"),
                status="WARN",
                severity="low",
                confidence="certain",
                applicability="applicable",
                description=_("Le max-age HSTS est de {max_age} secondes (< 1 an).").format(max_age=max_age),
                impact=_("La protection HSTS est de courte durée."),
                remediation=_("Augmenter max-age à au moins 31536000 (1 an)."),
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
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks transport."""
    findings = []

    f = check_trn_http_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_trn_https_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_trn_hsts_001(http_data, target, profile)
    if f:
        findings.append(f)

    f = check_trn_hsts_002(http_data, target, profile)
    if f:
        findings.append(f)

    return findings
