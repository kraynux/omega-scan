# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Export texte d'un ScanRun. Rendu humain compact, independant du terminal."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from omega_scan.domain.scans.models import ScanRun
from omega_scan.infrastructure.logging.app_logger import get_logger


def _format_duration(duration_ms: int) -> str:
    if duration_ms < 1000:
        return f"{duration_ms}ms"
    if duration_ms < 60000:
        return f"{duration_ms / 1000:.1f}s"
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}m {seconds}s"


def _format_status(status: str) -> str:
    symbols = {"OK": "[OK]", "WARN": "[WARN]", "FAIL": "[FAIL]", "N/A": "[N/A]"}
    return symbols.get(status, f"[{status}]")


def _format_severity(severity: str) -> str:
    return severity.upper()


def export_text(run: ScanRun, output_path: str | Path) -> Path:
    """Exporte le ScanRun en fichier texte lisible."""
    logger = get_logger()
    output_path = Path(output_path).resolve()

    logger.info(f"[TEXT_EXPORT] Export vers {output_path}")

    lines: list[str] = []

    lines.append("=" * 70)
    lines.append("OMEGA-SCAN ~ RAPPORT DE SCAN DE POSTURE DE SECURITE")
    lines.append("=" * 70)
    lines.append("")

    meta = run.meta
    lines.append(f"Scan ID      : {meta['scan_id']}")
    lines.append(f"Cible        : {run.target.normalized_host}")
    lines.append(f"Profil       : {run.scan_profile['profile_name']}")
    lines.append(f"Demarre      : {meta['started_at']}")
    lines.append(f"Termine      : {meta['finished_at']}")
    lines.append(f"Duree        : {_format_duration(meta['duration_ms'])}")
    lines.append(f"Machine      : {meta['host_machine']}")
    lines.append("")

    summary = run.summary
    lines.append("-" * 70)
    lines.append("RESUME")
    lines.append("-" * 70)
    lines.append(f"Note globale : {summary.overall_rating}")
    lines.append(f"Statut       : {summary.scan_status}")
    lines.append(f"Message      : {summary.short_message}")
    lines.append("")
    lines.append(f"Checks totaux    : {summary.checks_total}")
    lines.append(f"Findings (W+F)   : {summary.findings_total}")
    lines.append("")

    lines.append("Ventilation par statut :")
    for status, count in summary.status_breakdown.items():
        if count > 0:
            lines.append(f"  {_format_status(status):8s} : {count}")
    lines.append("")

    if summary.findings_total > 0:
        lines.append("Ventilation par severite :")
        for severity, count in summary.severity_breakdown.items():
            if count > 0:
                lines.append(f"  {_format_severity(severity):8s} : {count}")
        lines.append("")

    if summary.top_issues:
        lines.append("Principaux problemes :")
        for i, issue in enumerate(summary.top_issues, 1):
            lines.append(f"  {i}. {issue}")
        lines.append("")

    if run.findings:
        lines.append("-" * 70)
        lines.append("FINDINGS DETAILLES")
        lines.append("-" * 70)
        lines.append("")

        by_category: dict[str, list] = {}
        for finding in run.findings:
            by_category.setdefault(finding.category, []).append(finding)

        for category, findings in sorted(by_category.items()):
            lines.append(f"[{category.upper()}]")
            lines.append("")

            for finding in findings:
                lines.append(f"  {_format_status(finding.status)} {finding.title}")
                lines.append(f"    Regle      : {finding.rule_id}")
                lines.append(f"    Severite   : {_format_severity(finding.severity)}")
                lines.append(f"    Confiance  : {finding.confidence}")
                lines.append(f"    Description: {finding.description}")

                if finding.impact:
                    lines.append(f"    Impact     : {finding.impact}")
                if finding.remediation:
                    lines.append(f"    Action     : {finding.remediation}")
                if finding.evidence:
                    lines.append(f"    Preuve     : {finding.evidence.value}")

                lines.append("")

    lines.append("-" * 70)
    lines.append("CONNECTIVITE")
    lines.append("-" * 70)
    conn = run.connectivity
    lines.append(f"DNS resolu       : {'Oui' if conn['dns_resolution_attempted'] else 'Non'}")
    if conn["resolved_addresses"]:
        lines.append(f"Adresses resolues: {', '.join(conn['resolved_addresses'])}")
    lines.append(f"HTTP accessible  : {'Oui' if conn['http_reachable'] else 'Non'}")
    lines.append(f"HTTPS accessible : {'Oui' if conn['https_reachable'] else 'Non'}")
    if conn["first_successful_scheme"]:
        lines.append(f"Premier schema   : {conn['first_successful_scheme']}")
    if conn["latency_overview_ms"]:
        lines.append(f"Latence moyenne  : {_format_duration(conn['latency_overview_ms'])}")
    if conn["connection_notes"]:
        lines.append(f"Notes            : {conn['connection_notes']}")
    lines.append("")

    tls = run.tls
    if tls["attempted"]:
        lines.append("-" * 70)
        lines.append("TLS")
        lines.append("-" * 70)
        lines.append(f"Handshake reussi : {'Oui' if tls['handshake_success'] else 'Non'}")
        if tls["tls_version"]:
            lines.append(f"Version TLS      : {tls['tls_version']}")
        if tls["cipher"]:
            lines.append(f"Cipher           : {tls['cipher']}")
        if tls["certificate_subject"]:
            lines.append(f"Sujet certificat : {tls['certificate_subject']}")
        if tls["certificate_issuer"]:
            lines.append(f"Emetteur         : {tls['certificate_issuer']}")
        if tls["certificate_san"]:
            lines.append(f"SAN              : {', '.join(tls['certificate_san'][:5])}")
        if tls["not_before"] and tls["not_after"]:
            lines.append(f"Validite         : {tls['not_before']} -> {tls['not_after']}")
        lines.append(f"Hostname match   : {'Oui' if tls['hostname_match'] else 'Non'}")
        if tls["self_signed"]:
            lines.append("Auto-signe       : Oui")
        if tls["validation_error"]:
            lines.append(f"Erreur validation: {tls['validation_error']}")
        if tls["notes"]:
            lines.append(f"Notes            : {tls['notes']}")
        lines.append("")

    if run.errors:
        lines.append("-" * 70)
        lines.append("ERREURS")
        lines.append("-" * 70)
        for error in run.errors:
            fatal_marker = " [FATAL]" if error["fatal"] else ""
            lines.append(f"  [{error['module']}] {error['error_type']}: {error['message']}{fatal_marker}")
            if error["failure_category"]:
                lines.append(f"    Categorie: {error['failure_category']}")
        lines.append("")

    lines.append("=" * 70)
    lines.append(
        f"Rapport genere le {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} "
        f"par Omega-scan v{meta['scanner_version']}"
    )
    lines.append("=" * 70)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    logger.info(f"[TEXT_EXPORT] Export termine : {output_path}")
    return output_path
