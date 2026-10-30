# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Calcul du resume d'un scan (ex `_calculate_summary` prive de core/pipeline.py)."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.findings.models import Finding
from omega_scan.domain.scans.models import Summary
from omega_scan.shared.i18n import _


def calculate_summary(
    findings: list[Finding], scan_status: str, connectivity: dict[str, Any] | None = None
) -> Summary:
    """Calcule le resume du scan : compteurs, ventilations, note A-F.

    `connectivity` optionnel (retro-compatible) : quand la cible n'est
    reellement joignable ni en HTTP ni en HTTPS, la note est forcee a
    "N/A" quel que soit le nombre de findings partiels deja produits (ex.
    un seul TRN-HTTPS-001 FAIL sur une cible injoignable donnait "B",
    posture jugee "correcte" — bug reel rapporte : une cible injoignable
    n'a AUCUNE posture evaluable, favorable ou non)."""
    checks_total = 0
    findings_total = 0
    status_breakdown = {"OK": 0, "WARN": 0, "FAIL": 0, "N/A": 0}
    severity_breakdown = {"info": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    category_breakdown: dict = {}
    top_issues: list[str] = []

    for f in findings:
        checks_total += 1
        status_breakdown[f.status] = status_breakdown.get(f.status, 0) + 1

        if f.status in ("WARN", "FAIL"):
            findings_total += 1
            severity_breakdown[f.severity] = severity_breakdown.get(f.severity, 0) + 1
            category_breakdown[f.category] = category_breakdown.get(f.category, 0) + 1

            if len(top_issues) < 5 and f.severity in ("high", "critical") or len(top_issues) < 5 and f.status == "FAIL":
                top_issues.append(f.title)

    unreachable = connectivity is not None and not (
        connectivity.get("http_reachable") or connectivity.get("https_reachable")
    )

    if checks_total == 0 or unreachable:
        # Aucune regle evaluee, OU cible confirmee injoignable en HTTP et en
        # HTTPS (meme si un ou deux findings partiels ont quand meme ete
        # produits, ex. TRN-HTTPS-001 FAIL) : distinct de "tout evalue est
        # bon" (findings_total == 0 AVEC une cible reellement joignable, cas
        # normal ci-dessous). Sans cette branche, un scan sur une cible
        # injoignable pouvait recevoir "A" (aucun check) ou "B" ("posture
        # correcte") selon l'endroit exact ou la connexion echouait — bug
        # reel rapporte dans les deux cas.
        overall_rating = "N/A"
        short_message = _("Scan incomplet : cible injoignable, aucune vérification possible.")
    elif findings_total == 0:
        overall_rating = "A"
        short_message = _("Posture de sécurité excellente.")
    elif findings_total <= 2:
        overall_rating = "B"
        short_message = _("Posture correcte, quelques améliorations recommandées.")
    elif findings_total <= 5:
        overall_rating = "C"
        short_message = _("Posture moyenne, plusieurs points à corriger.")
    elif findings_total <= 10:
        overall_rating = "D"
        short_message = _("Posture faible, corrections prioritaires nécessaires.")
    else:
        overall_rating = "F"
        short_message = _("Posture critique, action immédiate requise.")

    return Summary(
        scan_status=scan_status,
        checks_total=checks_total,
        findings_total=findings_total,
        status_breakdown=status_breakdown,
        severity_breakdown=severity_breakdown,
        category_breakdown=category_breakdown,
        top_issues=top_issues[:5],
        overall_rating=overall_rating,
        short_message=short_message,
    )
