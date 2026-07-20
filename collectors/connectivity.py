# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Pré-scan de connectivité.
Section 3.1 et 4 de la spec.
Objectif : savoir ce qui répond avant d'évaluer quoi que ce soit.
"""

import socket
import time
from typing import List, Dict, Any, Optional
import httpx

from models.target import Target
from config.profiles import ScanProfile
from core.errors import (
    ScanError,
    classify_exception,
    build_error_from_exception,
    FAILURE_CATEGORY_DNS,
    FAILURE_CATEGORY_REFUSED,
    FAILURE_CATEGORY_TIMEOUT,
    FAILURE_CATEGORY_TLS_HANDSHAKE,
    FAILURE_CATEGORY_RESET,
    FAILURE_CATEGORY_UNKNOWN,
)
from core.logger import get_logger


def probe_connectivity(
    target: Target,
    profile: ScanProfile,
    errors: List[ScanError],
) -> Dict[str, Any]:
    """
    Pré-scan de connectivité.
    Teste DNS, HTTP, HTTPS, catégorise les échecs.
    Remplit le bloc connectivity du ScanResult.
    """
    logger = get_logger()
    logger.info(f"[CONNECTIVITY] Début du pré-scan pour {target.normalized_host}")

    # Initialisation du bloc connectivity
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
        "connection_notes": "",
        "failure_category": None,  # Sera rempli par schéma si échec
    }

    # 1. Résolution DNS (si hostname)
    if target.target_kind == "hostname":
        connectivity["dns_resolution_attempted"] = True
        try:
            logger.debug(f"[DNS] Résolution de {target.normalized_host}")
            addrinfo = socket.getaddrinfo(
                target.normalized_host,
                None,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM,
            )
            # Extraire les adresses IP uniques
            resolved = list(set(info[4][0] for info in addrinfo))
            connectivity["resolved_addresses"] = resolved
            if resolved:
                connectivity["preferred_address"] = resolved[0]
                logger.info(f"[DNS] Résolu : {resolved}")
            else:
                logger.warning(f"[DNS] Aucune adresse résolue pour {target.normalized_host}")
                errors.append(
                    ScanError(
                        module="connectivity",
                        phase="connectivity",
                        error_type="DnsResolutionError",
                        message=f"Aucune adresse IP résolue pour {target.normalized_host}",
                        fatal=False,
                        related_target=target.input_raw,
                        failure_category=FAILURE_CATEGORY_DNS,
                    )
                )
                connectivity["failure_category"] = FAILURE_CATEGORY_DNS
                return connectivity
        except socket.gaierror as e:
            logger.error(f"[DNS] Échec de résolution : {e}")
            errors.append(
                build_error_from_exception(
                    e,
                    module="connectivity",
                    phase="connectivity",
                    related_target=target.input_raw,
                    fatal=False,
                )
            )
            connectivity["failure_category"] = FAILURE_CATEGORY_DNS
            return connectivity
    else:
        # C'est une IP, pas de DNS à faire
        connectivity["preferred_address"] = target.normalized_host

    # 2. Déterminer les ports à tester
    ports_to_test = []
    if target.requested_port:
        ports_to_test.append(target.requested_port)
    else:
        # Ports par défaut selon le mode
        if target.scan_modes in ("http", "both"):
            ports_to_test.append(80)
        if target.scan_modes in ("https", "both"):
            ports_to_test.append(443)
    
    connectivity["ports_tested"] = ports_to_test

    # 3. Tester HTTP et HTTPS
    http_ok = False
    https_ok = False
    first_success = None
    latencies = []

    # Configuration httpx
    timeout = httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )

    # Tester HTTP
    if target.scan_modes in ("http", "both"):
        http_url = target.normalized_url_http
        logger.info(f"[HTTP] Test de {http_url}")
        try:
            with httpx.Client(timeout=timeout, follow_redirects=False) as client:
                start = time.time()
                response = client.head(http_url)
                elapsed_ms = int((time.time() - start) * 1000)
                latencies.append(elapsed_ms)
                
                if response.status_code < 500:
                    http_ok = True
                    connectivity["http_reachable"] = True
                    if target.requested_port:
                        connectivity["reachable_ports"].append(target.requested_port)
                    if first_success is None:
                        first_success = "http"
                    logger.info(f"[HTTP] {http_url} → {response.status_code} ({elapsed_ms}ms)")
                else:
                    logger.warning(f"[HTTP] {http_url} → {response.status_code} (5xx)")
        except Exception as e:
            logger.warning(f"[HTTP] {http_url} → ÉCHEC : {e}")
            errors.append(
                build_error_from_exception(
                    e,
                    module="connectivity",
                    phase="connectivity",
                    related_target=target.input_raw,
                    related_scheme="http",
                    fatal=False,
                )
            )

    # Tester HTTPS
    if target.scan_modes in ("https", "both"):
        https_url = target.normalized_url_https
        logger.info(f"[HTTPS] Test de {https_url}")
        try:
            with httpx.Client(timeout=timeout, follow_redirects=False, verify=False) as client:
                start = time.time()
                response = client.head(https_url)
                elapsed_ms = int((time.time() - start) * 1000)
                latencies.append(elapsed_ms)
                
                if response.status_code < 500:
                    https_ok = True
                    connectivity["https_reachable"] = True
                    if target.requested_port:
                        if target.requested_port not in connectivity["reachable_ports"]:
                            connectivity["reachable_ports"].append(target.requested_port)
                    if first_success is None:
                        first_success = "https"
                    logger.info(f"[HTTPS] {https_url} → {response.status_code} ({elapsed_ms}ms)")
                else:
                    logger.warning(f"[HTTPS] {https_url} → {response.status_code} (5xx)")
        except Exception as e:
            logger.warning(f"[HTTPS] {https_url} → ÉCHEC : {e}")
            errors.append(
                build_error_from_exception(
                    e,
                    module="connectivity",
                    phase="connectivity",
                    related_target=target.input_raw,
                    related_scheme="https",
                    fatal=False,
                )
            )

    # 4. Finaliser le bloc
    connectivity["first_successful_scheme"] = first_success
    if latencies:
        connectivity["latency_overview_ms"] = sum(latencies) // len(latencies)
    
    # Notes de connexion
    notes = []
    if not http_ok and not https_ok:
        notes.append("Aucun schéma accessible")
    elif http_ok and not https_ok:
        notes.append("HTTP accessible, HTTPS injoignable")
    elif https_ok and not http_ok:
        notes.append("HTTPS accessible, HTTP injoignable")
    
    connectivity["connection_notes"] = "; ".join(notes)

    logger.info(
        f"[CONNECTIVITY] Fin du pré-scan : HTTP={http_ok}, HTTPS={https_ok}, "
        f"first={first_success}, latency={connectivity['latency_overview_ms']}ms"
    )

    return connectivity
