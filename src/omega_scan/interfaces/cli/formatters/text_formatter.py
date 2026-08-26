# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Mise en forme texte/JSON des DTO pour la sortie CLI. Aucune decision metier."""
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any, cast

from omega_scan.application.dto.comparison_dto import ScanComparisonDTO
from omega_scan.application.dto.scan_dto import ScanRunDTO, ScanSummaryDTO
from omega_scan.application.dto.target_dto import PinnedTargetDTO


def to_json(value: Any) -> str:
    """Serialise un DTO (ou une sequence de DTO) en JSON indente, pour le
    mode scriptable (--json)."""
    if is_dataclass(value) and not isinstance(value, type):
        payload: Any = asdict(cast(Any, value))
    elif isinstance(value, (tuple, list)):
        payload = [asdict(cast(Any, item)) if is_dataclass(item) else item for item in value]
    else:
        payload = value
    return json.dumps(payload, indent=2, ensure_ascii=False)


def format_scan_summary(scan: ScanSummaryDTO) -> str:
    return (
        f"{scan.scan_id}  {scan.started_at}  {scan.normalized_host:<30}  "
        f"{scan.scan_status:<22}  note={scan.overall_rating}  "
        f"findings={scan.findings_total}"
    )


def format_scan_list(scans: tuple[ScanSummaryDTO, ...]) -> str:
    if not scans:
        return "Aucun scan."
    return "\n".join(format_scan_summary(s) for s in scans)


def format_scan_detail(run: ScanRunDTO) -> str:
    lines = [
        f"Scan {run.scan_id}",
        f"  Cible      : {run.normalized_host}",
        f"  Profil     : {run.profile_name}",
        f"  Demarre    : {run.started_at}",
        f"  Termine    : {run.finished_at}",
        f"  Duree      : {run.duration_ms} ms",
        f"  Statut     : {run.scan_status}",
        f"  Note       : {run.summary.overall_rating}",
        f"  Findings   : {run.summary.findings_total} / {len(run.findings)} regles evaluees",
    ]
    if run.errors:
        lines.append(f"  Erreurs    : {len(run.errors)}")
    if run.findings:
        lines.append("  Detail findings :")
        lines.extend(
            f"    [{f.status:<4}] {f.rule_id:<20} {f.title} (severite={f.severity})"
            for f in run.findings
            if f.status in ("WARN", "FAIL")
        )
    return "\n".join(lines)


def format_comparison(comparison: ScanComparisonDTO) -> str:
    lines = [
        f"Nouveaux    : {len(comparison.new_findings)}",
        f"Resolus     : {len(comparison.resolved_findings)}",
        f"Inchanges   : {len(comparison.unchanged_findings)}",
        f"Modifies    : {len(comparison.changed_findings)}",
    ]
    lines.extend(f"  + {f.rule_id} {f.title}" for f in comparison.new_findings)
    lines.extend(f"  - {f.rule_id} {f.title}" for f in comparison.resolved_findings)
    lines.extend(
        f"  ~ {c.previous.rule_id} {c.previous.status} -> {c.current.status}"
        for c in comparison.changed_findings
    )
    return "\n".join(lines)


def format_pinned_target(target: PinnedTargetDTO) -> str:
    note = f" — {target.note}" if target.note else ""
    return f"{target.normalized_host}  autorisee={target.authorized}  depuis {target.pinned_at}{note}"


def format_pinned_target_list(targets: tuple[PinnedTargetDTO, ...]) -> str:
    if not targets:
        return "Aucune cible epinglee."
    return "\n".join(format_pinned_target(t) for t in targets)


def format_error(message: str) -> str:
    return f"Erreur : {message}"
