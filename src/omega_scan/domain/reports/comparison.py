# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Comparaison entre deux scans d'une meme cible (upgrade fonctionnelle,
absente de la v1 mais deja anticipee dans les documents de conception
d'origine — voir document-unique-projet.md §20, "comparaison historique
entre scans, prevue comme evolution future")."""
from __future__ import annotations

from dataclasses import dataclass, field

from omega_scan.domain.findings.models import Finding
from omega_scan.domain.scans.models import ScanRun


def _finding_key(f: Finding) -> tuple[str, str]:
    """Cle de regroupement d'un finding : (rule_id, path) si location est
    renseignee (une meme regle peut viser plusieurs chemins, ex EXR-* sur
    plusieurs fichiers sensibles distincts), sinon rule_id seul."""
    path = (f.location or {}).get("path")
    return (f.rule_id, path) if path is not None else (f.rule_id, "")


@dataclass
class ScanComparison:
    """Resultat d'une comparaison entre deux ScanRun d'une meme cible."""

    new_findings: list[Finding] = field(default_factory=list)
    resolved_findings: list[Finding] = field(default_factory=list)
    unchanged_findings: list[Finding] = field(default_factory=list)
    changed_findings: list[tuple[Finding, Finding]] = field(default_factory=list)


def compare_scans(previous: ScanRun, current: ScanRun) -> ScanComparison:
    """Compare deux ScanRun sur leurs findings, regroupes par (rule_id, path).

    - new_findings : presents dans `current`, absents de `previous`.
    - resolved_findings : presents dans `previous`, absents de `current`.
    - unchanged_findings : presents des deux cotes avec le meme `status`.
    - changed_findings : presents des deux cotes avec un `status` different,
      tuple (finding_precedent, finding_courant).
    """
    previous_by_key: dict[tuple[str, str], Finding] = {
        _finding_key(f): f for f in previous.findings
    }
    current_by_key: dict[tuple[str, str], Finding] = {
        _finding_key(f): f for f in current.findings
    }

    comparison = ScanComparison()

    for key, current_finding in current_by_key.items():
        previous_finding = previous_by_key.get(key)
        if previous_finding is None:
            comparison.new_findings.append(current_finding)
        elif previous_finding.status != current_finding.status:
            comparison.changed_findings.append((previous_finding, current_finding))
        else:
            comparison.unchanged_findings.append(current_finding)

    for key, previous_finding in previous_by_key.items():
        if key not in current_by_key:
            comparison.resolved_findings.append(previous_finding)

    return comparison
