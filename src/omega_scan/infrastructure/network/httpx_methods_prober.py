# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation httpx du port MethodsProber (test des methodes HTTP)."""
from __future__ import annotations

from typing import Any

import httpx

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target
from omega_scan.infrastructure.exceptions import build_error_from_exception
from omega_scan.infrastructure.logging.app_logger import get_logger
from omega_scan.shared.i18n import N_, log_text


class HttpxMethodsProber:
    """Implemente ports/methods_prober.py::MethodsProber."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        http_data: dict[str, Any],
        errors: list[ScanError],
    ) -> dict[str, Any]:
        logger = get_logger()
        logger.info(log_text(N_("[METHODS_PROBE] Début du test des méthodes HTTP pour "
                                "{normalized_host}"), normalized_host=target.normalized_host))

        result: dict[str, Any] = {"methods_tested": []}

        preferred_scheme = http_data.get("overview", {}).get("preferred_scheme")
        if not preferred_scheme:
            logger.warning(N_("[METHODS_PROBE] Aucun schéma préféré, test des méthodes annulé"))
            return result

        base_url = http_data.get(preferred_scheme, {}).get("final_url")
        if not base_url:
            logger.warning(N_("[METHODS_PROBE] Pas d'URL finale, test des méthodes annulé"))
            return result

        methods_to_test = profile.http_methods_tested

        timeout = httpx.Timeout(
            connect=profile.timeout_connect,
            read=profile.timeout_read,
            write=profile.timeout_connect,
            pool=profile.timeout_connect,
        )

        for method in methods_to_test:
            logger.debug(log_text(N_("[METHODS_PROBE] Test de la méthode {method} sur {base_url}"), method=method, base_url=base_url))
            method_result: dict[str, Any] = {
                "method": method,
                "status_code": None,
                "reason": "not_tested",
                "allow_header": None,
            }

            try:
                with httpx.Client(timeout=timeout, follow_redirects=False, verify=False) as client:
                    response = client.request(method, base_url, headers={"User-Agent": profile.user_agent})
                    method_result["status_code"] = response.status_code

                    if response.status_code == 405:
                        method_result["reason"] = "disabled"
                    elif response.status_code == 501:
                        method_result["reason"] = "not_implemented"
                    elif response.status_code in (401, 403):
                        method_result["reason"] = "protected"
                    elif 200 <= response.status_code < 300:
                        method_result["reason"] = "enabled"
                    else:
                        method_result["reason"] = "unknown"

                    if method == "OPTIONS" and "allow" in response.headers:
                        method_result["allow_header"] = response.headers["allow"]

            except Exception as exc:  # noqa: BLE001 - traduit en ScanError, jamais leve
                method_result["reason"] = "error"
                errors.append(
                    build_error_from_exception(
                        exc, module="methods_probe", phase="methods_probe",
                        related_target=target.input_raw, fatal=False,
                    )
                )

            result["methods_tested"].append(method_result)

        logger.info(log_text(N_("[METHODS_PROBE] Fin du test des méthodes : {count} méthodes "
                                "testées"), count=len(result['methods_tested'])))
        return result
