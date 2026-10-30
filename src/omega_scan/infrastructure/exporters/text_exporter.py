# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Export texte d'un ScanRun. Rendu humain compact, independant du terminal."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from omega_scan.domain.scans.models import ScanRun
from omega_scan.infrastructure.logging.app_logger import get_logger
from omega_scan.shared.i18n import N_, _, log_text


def _tr(value: str | None) -> str | None:
    """R1 : texte enregistre en francais (titre, impact...) retraduit dans la langue de l'export."""
    return _(value) if value else value


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

    logger.info(log_text(N_("[TEXT_EXPORT] Export vers {output_path}"), output_path=output_path))

    lines: list[str] = []

    lines.append("=" * 70)
    lines.append(_("OMEGA-SCAN ~ RAPPORT DE SCAN DE POSTURE DE SÉCURITÉ"))
    lines.append("=" * 70)
    lines.append("")

    meta = run.meta
    lines.append(_("Scan ID      : {scan_id}").format(scan_id=meta['scan_id']))
    lines.append(_("Cible        : {normalized_host}").format(normalized_host=run.target.normalized_host))
    lines.append(_("Profil       : {profile_name}").format(profile_name=run.scan_profile['profile_name']))
    lines.append(_("Démarré      : {started_at}").format(started_at=meta['started_at']))
    lines.append(_("Terminé      : {finished_at}").format(finished_at=meta['finished_at']))
    lines.append(_("Durée        : {value}").format(value=_format_duration(meta['duration_ms'])))
    lines.append(_("Machine      : {host_machine}").format(host_machine=meta['host_machine']))
    lines.append("")

    summary = run.summary
    lines.append("-" * 70)
    lines.append("RESUME")
    lines.append("-" * 70)
    lines.append(_("Note globale : {overall_rating}").format(overall_rating=summary.overall_rating))
    lines.append(_("Statut       : {scan_status}").format(scan_status=summary.scan_status))
    lines.append(_("Message      : {short_message}").format(short_message=_tr(summary.short_message)))
    lines.append("")
    lines.append(_("Checks totaux    : {checks_total}").format(checks_total=summary.checks_total))
    lines.append(_("Findings (W+F)   : {findings_total}").format(findings_total=summary.findings_total))
    lines.append("")

    lines.append(_("Ventilation par statut :"))
    for status, count in summary.status_breakdown.items():
        if count > 0:
            lines.append(f"  {_format_status(status):8s} : {count}")
    lines.append("")

    if summary.findings_total > 0:
        lines.append(_("Ventilation par sévérité :"))
        for severity, count in summary.severity_breakdown.items():
            if count > 0:
                lines.append(f"  {_format_severity(severity):8s} : {count}")
        lines.append("")

    if summary.top_issues:
        lines.append(_("Principaux problèmes :"))
        for i, issue in enumerate(summary.top_issues, 1):
            lines.append(f"  {i}. {issue}")
        lines.append("")

    if run.findings:
        lines.append("-" * 70)
        lines.append(_("FINDINGS DÉTAILLÉS"))
        lines.append("-" * 70)
        lines.append("")

        by_category: dict[str, list] = {}
        for finding in run.findings:
            by_category.setdefault(finding.category, []).append(finding)

        for category, findings in sorted(by_category.items()):
            lines.append(f"[{category.upper()}]")
            lines.append("")

            for finding in findings:
                lines.append(f"  {_format_status(finding.status)} {_tr(finding.title)}")
                lines.append(_("    Règle      : {rule_id}").format(rule_id=finding.rule_id))
                lines.append(_("    Sévérité   : {value}").format(value=_format_severity(finding.severity)))
                lines.append(_("    Confiance  : {confidence}").format(confidence=finding.confidence))
                lines.append(_("    Description: {description}").format(description=_tr(finding.description)))

                if finding.impact:
                    lines.append(_("    Impact     : {impact}").format(impact=_tr(finding.impact)))
                if finding.remediation:
                    lines.append(_("    Action     : {remediation}").format(remediation=_tr(finding.remediation)))
                if finding.evidence:
                    lines.append(_("    Preuve     : {value}").format(value=finding.evidence.value))

                lines.append("")

    lines.append("-" * 70)
    lines.append("CONNECTIVITE")
    lines.append("-" * 70)
    conn = run.connectivity
    lines.append(_("DNS résolu       : {value}").format(value=_("Oui") if conn['dns_resolution_attempted'] else _("Non")))
    if conn["resolved_addresses"]:
        lines.append(_("Adresses résolues: {join}").format(join=', '.join(conn['resolved_addresses'])))
    lines.append(_("HTTP accessible  : {value}").format(value=_("Oui") if conn['http_reachable'] else _("Non")))
    lines.append(_("HTTPS accessible : {value}").format(value=_("Oui") if conn['https_reachable'] else _("Non")))
    if conn["first_successful_scheme"]:
        lines.append(_("Premier schéma   : {first_successful_scheme}").format(first_successful_scheme=conn['first_successful_scheme']))
    if conn["latency_overview_ms"]:
        lines.append(_("Latence moyenne  : {value}").format(value=_format_duration(conn['latency_overview_ms'])))
    if conn["connection_notes"]:
        lines.append(_("Notes            : {connection_notes}").format(connection_notes=conn['connection_notes']))
    lines.append("")

    tls = run.tls
    if tls["attempted"]:
        lines.append("-" * 70)
        lines.append("TLS")
        lines.append("-" * 70)
        lines.append(_("Handshake réussi : {value}").format(value=_("Oui") if tls['handshake_success'] else _("Non")))
        if tls["tls_version"]:
            lines.append(_("Version TLS      : {tls_version}").format(tls_version=tls['tls_version']))
        if tls["cipher"]:
            lines.append(_("Cipher           : {cipher}").format(cipher=tls['cipher']))
        if tls["certificate_subject"]:
            lines.append(_("Sujet certificat : {certificate_subject}").format(certificate_subject=tls['certificate_subject']))
        if tls["certificate_issuer"]:
            lines.append(_("Émetteur         : {certificate_issuer}").format(certificate_issuer=tls['certificate_issuer']))
        if tls["certificate_san"]:
            lines.append(_("SAN              : {join}").format(join=', '.join(tls['certificate_san'][:5])))
        if tls["not_before"] and tls["not_after"]:
            lines.append(_("Validité         : {not_before} -> {not_after}").format(not_before=tls['not_before'], not_after=tls['not_after']))
        lines.append(_("Hostname match   : {value}").format(value=_("Oui") if tls['hostname_match'] else _("Non")))
        if tls["self_signed"]:
            lines.append(_("Auto-signé       : Oui"))
        if tls["validation_error"]:
            lines.append(_("Erreur validation: {validation_error}").format(validation_error=tls['validation_error']))
        if tls["notes"]:
            lines.append(_("Notes            : {notes}").format(notes=tls['notes']))
        lines.append("")

    if run.errors:
        lines.append("-" * 70)
        lines.append(_("ERREURS"))
        lines.append("-" * 70)
        for error in run.errors:
            fatal_marker = " [FATAL]" if error["fatal"] else ""
            lines.append(f"  [{error['module']}] {error['error_type']}: {error['message']}{fatal_marker}")
            if error["failure_category"]:
                lines.append(_("    Catégorie: {failure_category}").format(failure_category=error['failure_category']))
        lines.append("")

    lines.append("=" * 70)
    lines.append(
        _("Rapport généré le {strftime} par Omega-scan v{scanner_version}").format(strftime=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'), scanner_version=meta['scanner_version'])
    )
    lines.append("=" * 70)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    logger.info(log_text(N_("[TEXT_EXPORT] Export terminé : {output_path}"), output_path=output_path))
    return output_path
