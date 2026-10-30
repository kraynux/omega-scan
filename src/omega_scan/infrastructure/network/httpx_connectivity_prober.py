# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation httpx du port ConnectivityProber (pre-scan DNS/HTTP/HTTPS)."""
from __future__ import annotations

import socket
import time
from typing import Any

import httpx

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import FAILURE_CATEGORY_DNS, ScanError
from omega_scan.domain.targets.models import Target
from omega_scan.infrastructure.exceptions import build_error_from_exception
from omega_scan.infrastructure.logging.app_logger import get_logger
from omega_scan.shared.i18n import N_, _, log_text


class HttpxConnectivityProber:
    """Implemente ports/connectivity_prober.py::ConnectivityProber. Seul
    endroit avec les autres modules de ce paquet ou `httpx` est importe."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        errors: list[ScanError],
    ) -> dict[str, Any]:
        logger = get_logger()
        logger.info(log_text(N_("[CONNECTIVITY] Début du pré-scan pour {normalized_host}"), normalized_host=target.normalized_host))

        connectivity: dict[str, Any] = {
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
            "failure_category": None,
        }

        if target.target_kind == "hostname":
            connectivity["dns_resolution_attempted"] = True
            try:
                logger.debug(log_text(N_("[DNS] Résolution de {normalized_host}"), normalized_host=target.normalized_host))
                addrinfo = socket.getaddrinfo(
                    target.normalized_host, None, socket.AF_UNSPEC, socket.SOCK_STREAM
                )
                resolved = list({info[4][0] for info in addrinfo})
                connectivity["resolved_addresses"] = resolved
                if resolved:
                    connectivity["preferred_address"] = resolved[0]
                    logger.info(log_text(N_("[DNS] Résolu : {resolved}"), resolved=resolved))
                else:
                    logger.warning(log_text(N_("[DNS] Aucune adresse résolue pour "
                                               "{normalized_host}"), normalized_host=target.normalized_host))
                    errors.append(
                        ScanError(
                            module="connectivity",
                            phase="connectivity",
                            error_type="DnsResolutionError",
                            message=_("Aucune adresse IP résolue pour {normalized_host}").format(normalized_host=target.normalized_host),
                            fatal=False,
                            related_target=target.input_raw,
                            failure_category=FAILURE_CATEGORY_DNS,
                        )
                    )
                    connectivity["failure_category"] = FAILURE_CATEGORY_DNS
                    return connectivity
            except socket.gaierror as exc:
                logger.error(log_text(N_("[DNS] Échec de résolution : {exc}"), exc=exc))
                errors.append(
                    build_error_from_exception(
                        exc,
                        module="connectivity",
                        phase="connectivity",
                        related_target=target.input_raw,
                        fatal=False,
                    )
                )
                connectivity["failure_category"] = FAILURE_CATEGORY_DNS
                return connectivity
        else:
            connectivity["preferred_address"] = target.normalized_host

        ports_to_test = []
        if target.requested_port:
            ports_to_test.append(target.requested_port)
        else:
            if target.scan_modes in ("http", "both"):
                ports_to_test.append(80)
            if target.scan_modes in ("https", "both"):
                ports_to_test.append(443)
        connectivity["ports_tested"] = ports_to_test

        http_ok = False
        https_ok = False
        first_success = None
        latencies: list[int] = []

        timeout = httpx.Timeout(
            connect=profile.timeout_connect,
            read=profile.timeout_read,
            write=profile.timeout_connect,
            pool=profile.timeout_connect,
        )

        if target.scan_modes in ("http", "both"):
            http_url = target.normalized_url_http
            logger.info(log_text(N_("[HTTP] Test de {http_url}"), http_url=http_url))
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
                        logger.info(f"[HTTP] {http_url} -> {response.status_code} ({elapsed_ms}ms)")
                    else:
                        logger.warning(f"[HTTP] {http_url} -> {response.status_code} (5xx)")
            except Exception as exc:  # noqa: BLE001 - traduit en ScanError, jamais leve
                logger.warning(log_text(N_("[HTTP] {http_url} -> ÉCHEC : {exc}"), http_url=http_url, exc=exc))
                errors.append(
                    build_error_from_exception(
                        exc,
                        module="connectivity",
                        phase="connectivity",
                        related_target=target.input_raw,
                        related_scheme="http",
                        fatal=False,
                    )
                )

        if target.scan_modes in ("https", "both"):
            https_url = target.normalized_url_https
            logger.info(log_text(N_("[HTTPS] Test de {https_url}"), https_url=https_url))
            try:
                with httpx.Client(timeout=timeout, follow_redirects=False, verify=False) as client:
                    start = time.time()
                    response = client.head(https_url)
                    elapsed_ms = int((time.time() - start) * 1000)
                    latencies.append(elapsed_ms)

                    if response.status_code < 500:
                        https_ok = True
                        connectivity["https_reachable"] = True
                        if (
                            target.requested_port
                            and target.requested_port not in connectivity["reachable_ports"]
                        ):
                            connectivity["reachable_ports"].append(target.requested_port)
                        if first_success is None:
                            first_success = "https"
                        logger.info(
                            f"[HTTPS] {https_url} -> {response.status_code} ({elapsed_ms}ms)"
                        )
                    else:
                        logger.warning(f"[HTTPS] {https_url} -> {response.status_code} (5xx)")
            except Exception as exc:  # noqa: BLE001
                logger.warning(log_text(N_("[HTTPS] {https_url} -> ÉCHEC : {exc}"), https_url=https_url, exc=exc))
                errors.append(
                    build_error_from_exception(
                        exc,
                        module="connectivity",
                        phase="connectivity",
                        related_target=target.input_raw,
                        related_scheme="https",
                        fatal=False,
                    )
                )

        connectivity["first_successful_scheme"] = first_success
        if latencies:
            connectivity["latency_overview_ms"] = sum(latencies) // len(latencies)

        notes = []
        if not http_ok and not https_ok:
            notes.append(_("Aucun schéma accessible"))
        elif http_ok and not https_ok:
            notes.append(_("HTTP accessible, HTTPS injoignable"))
        elif https_ok and not http_ok:
            notes.append(_("HTTPS accessible, HTTP injoignable"))
        connectivity["connection_notes"] = "; ".join(notes)

        logger.info(
            log_text(N_("[CONNECTIVITY] Fin du pré-scan : HTTP={http_ok}, HTTPS={https_ok}, "
                        "first={first_success}, latency={latency_overview_ms}ms"), http_ok=http_ok, https_ok=https_ok, first_success=first_success, latency_overview_ms=connectivity['latency_overview_ms'])
        )
        return connectivity
