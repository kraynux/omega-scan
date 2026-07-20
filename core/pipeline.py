# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Pipeline de scan complet.
Section 3 de spec.
Orchestre : validation → normalisation → connectivité → collecte → checks → résultat.
"""

import time
from typing import Dict, Any, List, Optional
import socket

from models.target import Target
from models.scan_result import ScanResult
from models.summary import Summary
from config.profiles import ScanProfile, get_profile
from core.context import ScanContext
from core.errors import ScanError, TargetParseError
from core.target_parser import parse_target
from core.logger import get_logger
from collectors.connectivity import probe_connectivity
from collectors.http_probe import probe_http
from checks.transport import run_transport_checks
from checks.headers import run_headers_checks


def _calculate_summary(
    findings: List[Any],
    scan_status: str,
) -> Summary:
    """
    Calcule le résumé du scan (section 9.8).
    """
    # Compteurs
    checks_total = 0
    findings_total = 0
    status_breakdown = {"OK": 0, "WARN": 0, "FAIL": 0, "N/A": 0}
    severity_breakdown = {"info": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    category_breakdown = {}
    top_issues = []

    # Compter les checks (tous les findings, y compris OK et N/A)
    for f in findings:
        checks_total += 1
        status_breakdown[f.status] = status_breakdown.get(f.status, 0) + 1
        
        # findings_total = WARN + FAIL uniquement
        if f.status in ("WARN", "FAIL"):
            findings_total += 1
            severity_breakdown[f.severity] = severity_breakdown.get(f.severity, 0) + 1
            category_breakdown[f.category] = category_breakdown.get(f.category, 0) + 1
            
            # Top issues (3-5 max, les plus sévères)
            if len(top_issues) < 5 and f.severity in ("high", "critical"):
                top_issues.append(f.title)
            elif len(top_issues) < 5 and f.status == "FAIL":
                top_issues.append(f.title)

    # Note globale simplifiée
    if findings_total == 0:
        overall_rating = "A"
        short_message = "Posture de sécurité excellente."
    elif findings_total <= 2:
        overall_rating = "B"
        short_message = "Posture correcte, quelques améliorations recommandées."
    elif findings_total <= 5:
        overall_rating = "C"
        short_message = "Posture moyenne, plusieurs points à corriger."
    elif findings_total <= 10:
        overall_rating = "D"
        short_message = "Posture faible, corrections prioritaires nécessaires."
    else:
        overall_rating = "F"
        short_message = "Posture critique, action immédiate requise."

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


def run_scan(
    raw_target: str,
    profile_name: str = "standard",
) -> ScanResult:
    """
    Exécute un scan complet de bout en bout.
    Section 3 de la spec.
    
    Args:
        raw_target: Cible brute (IPv4, IPv6, hostname, URL)
        profile_name: Nom du profil (quick, standard, extended, local-lab)
    
    Returns:
        ScanResult complet
    """
    logger = get_logger()
    logger.info(f"[PIPELINE] Démarrage du scan pour : {raw_target}")

    # Initialiser le contexte
    ctx = ScanContext()
    ctx.profile_name = profile_name
    ctx.host_machine = socket.gethostname()
    ctx.start()

    # Récupérer le profil
    try:
        profile = get_profile(profile_name)
    except ValueError as e:
        logger.error(f"[PIPELINE] Profil invalide : {e}")
        ctx.add_error(ScanError(
            module="pipeline",
            phase="validation",
            error_type="InvalidProfile",
            message=str(e),
            fatal=True,
        ))
        ctx.finish()
        # Retourner un ScanResult minimal en cas d'erreur fatale
        return _build_minimal_result(ctx, raw_target, profile_name)

    # 1. Validation et normalisation de la cible
    logger.log_phase_start("validation")
    try:
        target = parse_target(raw_target)
        ctx.target = target
        logger.info(f"[PIPELINE] Cible normalisée : {target.normalized_host} ({target.target_kind}, {target.scope_kind})")
    except TargetParseError as e:
        logger.error(f"[PIPELINE] Erreur de parsing : {e}")
        ctx.add_error(ScanError(
            module="target_parser",
            phase="validation",
            error_type="TargetParseError",
            message=str(e),
            fatal=True,
            related_target=raw_target,
        ))
        ctx.finish()
        return _build_minimal_result(ctx, raw_target, profile_name)
    logger.log_phase_end("validation", 0)

    # 2. Pré-scan de connectivité
    logger.log_phase_start("connectivity")
    connectivity_errors: List[ScanError] = []
    connectivity = probe_connectivity(target, profile, connectivity_errors)
    for err in connectivity_errors:
        ctx.add_error(err)
    logger.log_phase_end("connectivity", connectivity.get("latency_overview_ms", 0) or 0)

    # Vérifier si au moins un schéma est accessible
    if not connectivity["http_reachable"] and not connectivity["https_reachable"]:
        logger.warning("[PIPELINE] Aucun schéma accessible, scan partiel")
        # Continuer quand même pour produire un résultat partiel

    # 3. Collecte HTTP/HTTPS (base)
    logger.log_phase_start("http_probe")
    http_errors: List[ScanError] = []
    http_data = probe_http(target, profile, http_errors)
    for err in http_errors:
        ctx.add_error(err)
    logger.log_phase_end("http_probe", 0)

    # 4. Collecte TLS
    logger.log_phase_start("tls_probe")
    from collectors.tls_probe import probe_tls
    tls_errors: List[ScanError] = []
    tls_data = probe_tls(target, profile, tls_errors)
    for err in tls_errors:
        ctx.add_error(err)
    logger.log_phase_end("tls_probe", 0)

    # 5. Path probing (dépend de http_data)
    logger.log_phase_start("path_probe")
    from collectors.path_probe import probe_paths
    path_errors: List[ScanError] = []
    path_data = probe_paths(target, profile, http_data, path_errors)
    for err in path_errors:
        ctx.add_error(err)
    http_data["overview"]["catch_all_suspected"] = path_data["catch_all_suspected"]
    http_data["overview"]["path_probe_context"] = path_data["path_probe_context"]
    logger.log_phase_end("path_probe", 0)

    # 6. Collecte des méthodes HTTP (dépend de http_data)
    logger.log_phase_start("methods_probe")
    from collectors.methods_probe import probe_methods
    methods_errors: List[ScanError] = []
    methods_data = probe_methods(target, profile, http_data, methods_errors)
    for err in methods_errors:
        ctx.add_error(err)
    logger.log_phase_end("methods_probe", 0)

    # 7. Checks transport
    logger.log_phase_start("checks_transport")
    transport_findings = run_transport_checks(
        http_data,
        target.to_dict(),
        profile.to_dict(),
    )
    logger.log_phase_end("checks_transport", 0)

    # 8. Checks headers
    logger.log_phase_start("checks_headers")
    headers_findings = run_headers_checks(
        http_data,
        target.to_dict(),
        profile.to_dict(),
    )
    logger.log_phase_end("checks_headers", 0)

    # 9. Checks exposure
    logger.log_phase_start("checks_exposure")
    from checks.exposure import run_exposure_checks
    exposure_findings = run_exposure_checks(
        http_data,
        target.to_dict(),
        profile.to_dict(),
    )
    logger.log_phase_end("checks_exposure", 0)

    # 10. Checks methods
    logger.log_phase_start("checks_methods")
    from checks.methods import run_methods_checks
    methods_findings = run_methods_checks(
        methods_data,
        target.to_dict(),
        profile.to_dict(),
        http_data,
    )
    logger.log_phase_end("checks_methods", 0)

    # 11. Checks information leaks
    logger.log_phase_start("checks_information_leaks")
    from checks.information_leaks import run_information_leaks_checks
    info_leaks_findings = run_information_leaks_checks(
        http_data,
        target.to_dict(),
        profile.to_dict(),
    )
    logger.log_phase_end("checks_information_leaks", 0)

    # 12. Combiner tous les findings
    all_findings = (
        transport_findings + 
        headers_findings + 
        exposure_findings + 
        methods_findings + 
        info_leaks_findings
    )

    # 13. Finaliser le contexte
    ctx.finish()

    # 14. Calculer le summary
    summary = _calculate_summary(all_findings, ctx.scan_status)

    # 15. Construire le ScanResult complet
    # NOTE : On utilise ici le tls_data collecté à l'étape 4, pas un dictionnaire en dur !
    result = ScanResult(
        meta=ctx.to_meta_dict(),
        target=target,
        scan_profile=profile.to_dict(),
        connectivity=connectivity,
        http=http_data,
        tls=tls_data,  # <-- Correction majeure : on utilise la vraie collecte TLS
        findings=all_findings,
        summary=summary,
        errors=[e.to_dict() for e in ctx.errors],
    )

    logger.info(
        f"[PIPELINE] Scan terminé : {summary.findings_total} findings "
        f"({summary.status_breakdown['FAIL']} FAIL, {summary.status_breakdown['WARN']} WARN)"
    )

    return result


def _build_minimal_result(
    ctx: ScanContext,
    raw_target: str,
    profile_name: str,
) -> ScanResult:
    """
    Construit un ScanResult minimal en cas d'erreur fatale précoce.
    """
    # Target minimal
    target = Target(
        input_raw=raw_target,
        normalized_host="",
        normalized_url_http="",
        normalized_url_https="",
        requested_scheme=None,
        requested_port=None,
        requested_path="/",
        target_kind="hostname",
        scope_kind="hostname",
        scan_modes="both",
        is_ip=False,
        ip_version=None,
        is_private=False,
        is_loopback=False,
        is_link_local=False,
        is_global=False,
    )

    # Profil minimal
    try:
        profile = get_profile(profile_name)
        profile_dict = profile.to_dict()
    except ValueError:
        profile_dict = {"profile_name": profile_name}

    # Connectivité vide
    connectivity = {
        "dns_resolution_attempted": False,
        "resolved_addresses": [],
        "preferred_address": None,
        "http_reachable": False,
        "https_reachable": False,
        "ports_tested": [],
        "reachable_ports": [],
        "first_successful_scheme": None,
        "latency_overview_ms": None,
        "connection_notes": "Scan interrompu avant connectivité",
        "failure_category": None,
    }

    # HTTP vide
    http_data = {
        "overview": {
            "preferred_scheme": None,
            "catch_all_suspected": False,
            "proxy_suspected": False,
            "content_profile": "unknown",
            "path_probe_context": [],
        },
        "http": {
            "attempted": False,
            "requested_url": "",
            "final_url": "",
            "status_code": None,
            "reason": None,
            "ok": False,
            "elapsed_ms": None,
            "content_type": None,
            "content_length": None,
            "headers": {},
            "cookies": [],
            "redirect_chain": [],
            "request": {"method": "GET", "headers_sent": {}, "user_agent": ""},
            "body_preview": {"text_preview": "", "size_bytes": 0, "encoding": "unknown", "preview_truncated": False},
            "error": None,
            "content_profile": "unknown",
        },
        "https": {
            "attempted": False,
            "requested_url": "",
            "final_url": "",
            "status_code": None,
            "reason": None,
            "ok": False,
            "elapsed_ms": None,
            "content_type": None,
            "content_length": None,
            "headers": {},
            "cookies": [],
            "redirect_chain": [],
            "request": {"method": "GET", "headers_sent": {}, "user_agent": ""},
            "body_preview": {"text_preview": "", "size_bytes": 0, "encoding": "unknown", "preview_truncated": False},
            "error": None,
            "content_profile": "unknown",
        },
    }

    # TLS vide
    tls_data = {
        "attempted": False,
        "handshake_success": False,
        "tls_version": None,
        "cipher": None,
        "certificate_present": False,
        "certificate_subject": None,
        "certificate_issuer": None,
        "certificate_san": [],
        "not_before": None,
        "not_after": None,
        "hostname_match": False,
        "validation_error": None,
        "self_signed": False,
        "sni_hostname_sent": None,
        "notes": "Scan interrompu avant TLS",
    }

    # Summary minimal
    summary = Summary(
        scan_status=ctx.scan_status,
        checks_total=0,
        findings_total=0,
        status_breakdown={"OK": 0, "WARN": 0, "FAIL": 0, "N/A": 0},
        severity_breakdown={"info": 0, "low": 0, "medium": 0, "high": 0, "critical": 0},
        category_breakdown={},
        top_issues=[],
        overall_rating="N/A",
        short_message="Scan interrompu par une erreur fatale.",
    )

    return ScanResult(
        meta=ctx.to_meta_dict(),
        target=target,
        scan_profile=profile_dict,
        connectivity=connectivity,
        http=http_data,
        tls=tls_data,
        findings=[],
        summary=summary,
        errors=[e.to_dict() for e in ctx.errors],
    )
