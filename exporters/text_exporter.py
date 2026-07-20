# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Export texte du scan_result.
Section 17 de la spec.
Rendu humain compact, indépendant du terminal.
"""

from pathlib import Path
from typing import Union, List
from datetime import datetime

from models.scan_result import ScanResult
from core.logger import get_logger


def _format_duration(duration_ms: int) -> str:
    """Formate une durée en millisecondes en chaîne lisible."""
    if duration_ms < 1000:
        return f"{duration_ms}ms"
    elif duration_ms < 60000:
        return f"{duration_ms / 1000:.1f}s"
    else:
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        return f"{minutes}m {seconds}s"


def _format_status(status: str) -> str:
    """Formate un statut pour l'affichage texte."""
    symbols = {
        "OK": "[OK]",
        "WARN": "[WARN]",
        "FAIL": "[FAIL]",
        "N/A": "[N/A]",
    }
    return symbols.get(status, f"[{status}]")


def _format_severity(severity: str) -> str:
    """Formate une sévérité pour l'affichage texte."""
    return severity.upper()


def export_text(
    scan_result: ScanResult,
    output_path: Union[str, Path],
) -> Path:
    """
    Exporte le scan_result en fichier texte lisible.
    
    Args:
        scan_result: Résultat complet du scan
        output_path: Chemin du fichier de sortie
    
    Returns:
        Chemin du fichier créé
    """
    logger = get_logger()
    output_path = Path(output_path).resolve()
    
    logger.info(f"[TEXT_EXPORT] Export vers {output_path}")
    
    lines = []
    
    # En-tête
    lines.append("=" * 70)
    lines.append("OMEGA-SCAN ~ RAPPORT DE SCAN DE POSTURE DE SÉCURITÉ")
    lines.append("=" * 70)
    lines.append("")
    
    # Meta
    meta = scan_result.meta
    lines.append(f"Scan ID      : {meta['scan_id']}")
    lines.append(f"Cible        : {scan_result.target.normalized_host}")
    lines.append(f"Profil       : {scan_result.scan_profile['profile_name']}")
    lines.append(f"Démarré      : {meta['started_at']}")
    lines.append(f"Terminé      : {meta['finished_at']}")
    lines.append(f"Durée        : {_format_duration(meta['duration_ms'])}")
    lines.append(f"Machine      : {meta['host_machine']}")
    lines.append("")
    
    # Résumé
    summary = scan_result.summary
    lines.append("-" * 70)
    lines.append("RÉSUMÉ")
    lines.append("-" * 70)
    lines.append(f"Note globale : {summary.overall_rating}")
    lines.append(f"Statut       : {summary.scan_status}")
    lines.append(f"Message      : {summary.short_message}")
    lines.append("")
    lines.append(f"Checks totaux    : {summary.checks_total}")
    lines.append(f"Findings (W+F)   : {summary.findings_total}")
    lines.append("")
    
    # Ventilation par statut
    lines.append("Ventilation par statut :")
    for status, count in summary.status_breakdown.items():
        if count > 0:
            lines.append(f"  {_format_status(status):8s} : {count}")
    lines.append("")
    
    # Ventilation par sévérité
    if summary.findings_total > 0:
        lines.append("Ventilation par sévérité :")
        for severity, count in summary.severity_breakdown.items():
            if count > 0:
                lines.append(f"  {_format_severity(severity):8s} : {count}")
        lines.append("")
    
    # Top issues
    if summary.top_issues:
        lines.append("Principaux problèmes :")
        for i, issue in enumerate(summary.top_issues, 1):
            lines.append(f"  {i}. {issue}")
        lines.append("")
    
    # Findings détaillés
    if scan_result.findings:
        lines.append("-" * 70)
        lines.append("FINDINGS DÉTAILLÉS")
        lines.append("-" * 70)
        lines.append("")
        
        # Grouper par catégorie
        by_category = {}
        for finding in scan_result.findings:
            cat = finding.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(finding)
        
        # Afficher par catégorie
        for category, findings in sorted(by_category.items()):
            lines.append(f"[{category.upper()}]")
            lines.append("")
            
            for finding in findings:
                lines.append(f"  {_format_status(finding.status)} {finding.title}")
                lines.append(f"    Règle      : {finding.rule_id}")
                lines.append(f"    Sévérité   : {_format_severity(finding.severity)}")
                lines.append(f"    Confiance  : {finding.confidence}")
                lines.append(f"    Description: {finding.description}")
                
                if finding.impact:
                    lines.append(f"    Impact     : {finding.impact}")
                
                if finding.remediation:
                    lines.append(f"    Action     : {finding.remediation}")
                
                if finding.evidence:
                    lines.append(f"    Preuve     : {finding.evidence.value}")
                
                lines.append("")
    
    # Connectivité
    lines.append("-" * 70)
    lines.append("CONNECTIVITÉ")
    lines.append("-" * 70)
    conn = scan_result.connectivity
    lines.append(f"DNS résolu       : {'Oui' if conn['dns_resolution_attempted'] else 'Non'}")
    if conn['resolved_addresses']:
        lines.append(f"Adresses résolues: {', '.join(conn['resolved_addresses'])}")
    lines.append(f"HTTP accessible  : {'Oui' if conn['http_reachable'] else 'Non'}")
    lines.append(f"HTTPS accessible : {'Oui' if conn['https_reachable'] else 'Non'}")
    if conn['first_successful_scheme']:
        lines.append(f"Premier schéma   : {conn['first_successful_scheme']}")
    if conn['latency_overview_ms']:
        lines.append(f"Latence moyenne  : {_format_duration(conn['latency_overview_ms'])}")
    if conn['connection_notes']:
        lines.append(f"Notes            : {conn['connection_notes']}")
    lines.append("")
    
    # TLS
    tls = scan_result.tls
    if tls['attempted']:
        lines.append("-" * 70)
        lines.append("TLS")
        lines.append("-" * 70)
        lines.append(f"Handshake réussi : {'Oui' if tls['handshake_success'] else 'Non'}")
        if tls['tls_version']:
            lines.append(f"Version TLS      : {tls['tls_version']}")
        if tls['cipher']:
            lines.append(f"Cipher           : {tls['cipher']}")
        if tls['certificate_subject']:
            lines.append(f"Sujet certificat : {tls['certificate_subject']}")
        if tls['certificate_issuer']:
            lines.append(f"Émetteur         : {tls['certificate_issuer']}")
        if tls['certificate_san']:
            lines.append(f"SAN              : {', '.join(tls['certificate_san'][:5])}")
        if tls['not_before'] and tls['not_after']:
            lines.append(f"Validité         : {tls['not_before']} → {tls['not_after']}")
        lines.append(f"Hostname match   : {'Oui' if tls['hostname_match'] else 'Non'}")
        if tls['self_signed']:
            lines.append(f"Auto-signé       : Oui")
        if tls['validation_error']:
            lines.append(f"Erreur validation: {tls['validation_error']}")
        if tls['notes']:
            lines.append(f"Notes            : {tls['notes']}")
        lines.append("")
    
    # Erreurs
    if scan_result.errors:
        lines.append("-" * 70)
        lines.append("ERREURS")
        lines.append("-" * 70)
        for error in scan_result.errors:
            fatal_marker = " [FATAL]" if error['fatal'] else ""
            lines.append(f"  [{error['module']}] {error['error_type']}: {error['message']}{fatal_marker}")
            if error['failure_category']:
                lines.append(f"    Catégorie: {error['failure_category']}")
        lines.append("")
    
    # Pied de page
    lines.append("=" * 70)
    lines.append(f"Rapport généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} par Omega-scan v{meta['scanner_version']}")
    lines.append("=" * 70)
    
    # Écrire le fichier
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    logger.info(f"[TEXT_EXPORT] Export terminé : {output_path}")
    return output_path
