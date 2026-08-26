# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Checks des methodes HTTP (MTH-*) : OPTIONS, TRACE, PUT, DELETE, PATCH, CONNECT."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.checks.methods.policies import METHOD_RULES
from omega_scan.domain.findings.builders import build_finding, degrade_confidence_for_proxy
from omega_scan.domain.findings.models import Finding


def _build_method_finding(
    method: str,
    reason: str,
    target: dict[str, Any],
    profile: dict[str, Any],
    http_data: dict[str, Any],
) -> Finding | None:
    if reason in ("disabled", "not_implemented"):
        return None

    if method not in METHOD_RULES:
        return None

    proxy_suspected = http_data.get("overview", {}).get("proxy_suspected", False)
    preferred_scheme = http_data.get("overview", {}).get("preferred_scheme", "https")
    rule = METHOD_RULES[method]

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
            title=rule["title"] + " (protegee)",
            status="N/A",
            severity="info",
            confidence="high",
            applicability="not_applicable",
            description=rule["description"] + " Cependant, elle semble protegee par authentification.",
            impact="Risque mitige par la presence d'une authentification.",
            remediation="Verifier que l'authentification est robuste.",
            location=location,
            tags=["methods", method.lower()],
        )

    if reason == "enabled":
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

    if reason in ("unknown", "error"):
        return build_finding(
            rule_id=rule["rule_id"],
            category="methods",
            title=rule["title"] + " (statut incertain)",
            status="WARN",
            severity="low",
            confidence="low",
            applicability="conditional",
            description=rule["description"] + " Le statut exact n'a pas pu etre determine clairement.",
            impact=rule["impact"],
            remediation=rule["remediation"],
            location=location,
            tags=["methods", method.lower()],
        )

    return None


def run_methods_checks(
    methods_data: dict[str, Any],
    target: dict[str, Any],
    profile: dict[str, Any],
    http_data: dict[str, Any],
) -> list[Finding]:
    """Execute tous les checks de methodes HTTP."""
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
