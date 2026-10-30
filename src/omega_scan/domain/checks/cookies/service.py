# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks cookies (COO-*) : Secure, HttpOnly, SameSite.

Categorie prevue depuis la v1 (`Finding.category` documentait deja "cookies")
mais jamais implementee (paquet vide jusqu'au Lot M5, voir ARCHITECTURE.md
§0 et le rapport de migration du Lot M1)."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.findings.builders import build_finding, degrade_confidence_for_proxy
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding
from omega_scan.shared.i18n import _


def _location(target: dict[str, Any], scheme: str) -> dict[str, Any]:
    return {
        "url": None,
        "host": target.get("normalized_host"),
        "port": target.get("requested_port"),
        "scheme": scheme,
        "path": target.get("requested_path"),
        "component": "cookies",
    }


def check_coo_secure_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """COO-SECURE-001 : cookie observe sur HTTPS sans l'attribut Secure. WARN.
    Juge uniquement sur https : l'attribut Secure n'a pas de sens a evaluer
    sur une reponse HTTP simple."""
    findings: list[Finding] = []
    https_result = http_data.get("https", {})
    if not https_result.get("ok"):
        return findings

    proxy_suspected = http_data.get("overview", {}).get("proxy_suspected", False)

    for cookie in https_result.get("cookies", []):
        if not cookie.get("secure"):
            confidence = degrade_confidence_for_proxy("certain", proxy_suspected)
            findings.append(build_finding(
                rule_id="COO-SECURE-001",
                category="cookies",
                title=_("Cookie sans attribut Secure : {get}").format(get=cookie.get('name')),
                status="WARN",
                severity="medium",
                confidence=confidence,
                applicability="applicable",
                description=(
                    _("Le cookie '{get}' est posé sur une réponse HTTPS sans l'attribut Secure.").format(get=cookie.get('name'))
                ),
                impact=_("Le cookie peut être transmis en clair si le site est aussi "
                         "accessible en HTTP."),
                remediation=_("Ajouter l'attribut Secure à ce cookie."),
                evidence=Evidence(
                    type="cookie", value=cookie.get("name", ""), source="response.cookies"
                ),
                location=_location(target, "https"),
                tags=["cookies", "secure"],
            ))
    return findings


def check_coo_httponly_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """COO-HTTPONLY-001 : cookie sans l'attribut HttpOnly. WARN, severite low
    (impossible de distinguer ici un cookie de session sensible d'un cookie
    technique qui n'en a pas besoin, donc severite volontairement basse pour
    un signal generique). Juge les cookies observes sur https ET http."""
    findings: list[Finding] = []
    proxy_suspected = http_data.get("overview", {}).get("proxy_suspected", False)

    for scheme in ("https", "http"):
        result = http_data.get(scheme, {})
        if not result.get("ok"):
            continue
        for cookie in result.get("cookies", []):
            if not cookie.get("httponly"):
                confidence = degrade_confidence_for_proxy("certain", proxy_suspected)
                findings.append(build_finding(
                    rule_id="COO-HTTPONLY-001",
                    category="cookies",
                    title=_("Cookie sans attribut HttpOnly : {get}").format(get=cookie.get('name')),
                    status="WARN",
                    severity="low",
                    confidence=confidence,
                    applicability="applicable",
                    description=_("Le cookie '{get}' n'a pas l'attribut HttpOnly.").format(get=cookie.get('name')),
                    impact=_("Le cookie est accessible en JavaScript, ce qui aggrave l'impact "
                             "d'un XSS."),
                    remediation=_("Ajouter l'attribut HttpOnly si ce cookie n'est pas requis "
                                  "côté client."),
                    evidence=Evidence(
                        type="cookie", value=cookie.get("name", ""), source="response.cookies"
                    ),
                    location=_location(target, scheme),
                    tags=["cookies", "httponly"],
                ))
    return findings


def check_coo_samesite_001(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """COO-SAMESITE-001 : SameSite absent, ou 'None' sans Secure (risque
    CSRF). WARN. Juge les cookies observes sur https ET http."""
    findings: list[Finding] = []
    proxy_suspected = http_data.get("overview", {}).get("proxy_suspected", False)

    for scheme in ("https", "http"):
        result = http_data.get(scheme, {})
        if not result.get("ok"):
            continue
        for cookie in result.get("cookies", []):
            samesite = cookie.get("samesite")
            samesite_lower = (samesite or "").lower()
            at_risk = samesite is None or (samesite_lower == "none" and not cookie.get("secure"))
            if not at_risk:
                continue

            reason = (
                _("l'attribut SameSite est absent")
                if samesite is None
                else _("SameSite=None est déclaré sans l'attribut Secure")
            )
            confidence = degrade_confidence_for_proxy("certain", proxy_suspected)
            findings.append(build_finding(
                rule_id="COO-SAMESITE-001",
                category="cookies",
                title=_("Cookie à risque CSRF : {get}").format(get=cookie.get('name')),
                status="WARN",
                severity="medium",
                confidence=confidence,
                applicability="applicable",
                description=_("Le cookie '{get}' est à risque : {reason}.").format(get=cookie.get('name'), reason=reason),
                impact=_("Le cookie peut être envoyé lors de requêtes intersites, favorisant "
                         "les attaques CSRF."),
                remediation=_("Définir SameSite=Lax ou Strict, ou SameSite=None accompagné de "
                              "Secure."),
                evidence=Evidence(
                    type="cookie", value=cookie.get("name", ""), source="response.cookies"
                ),
                location=_location(target, scheme),
                tags=["cookies", "samesite", "csrf"],
            ))
    return findings


def run_cookies_checks(
    http_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks cookies."""
    findings: list[Finding] = []
    findings.extend(check_coo_secure_001(http_data, target, profile))
    findings.extend(check_coo_httponly_001(http_data, target, profile))
    findings.extend(check_coo_samesite_001(http_data, target, profile))
    return findings
