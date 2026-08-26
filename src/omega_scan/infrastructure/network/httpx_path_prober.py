# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation httpx du port PathProber (path probing + detection catch-all).

Les chemins sondes viennent de domain/checks/exposure/policies.py (deplaces
depuis config/paths.py au Lot M1), pas d'une ressource infrastructure/ :
decider quels chemins tester est deja une politique de securite/produit
(liste bornee, non-fuzzing), pas une donnee neutre."""
from __future__ import annotations

import time
import uuid
from typing import Any

import httpx

from omega_scan.domain.checks.exposure.policies import get_all_probe_paths
from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target
from omega_scan.infrastructure.exceptions import build_error_from_exception
from omega_scan.infrastructure.logging.app_logger import get_logger
from omega_scan.infrastructure.network._shaping import deduce_content_profile


def _generate_probe_token() -> str:
    return f"__Omega_scan_probe_{uuid.uuid4().hex[:16]}__"


def _timeout_for(profile: ScanProfile) -> httpx.Timeout:
    return httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )


def _detect_catch_all(
    base_url: str,
    base_content_profile: str,
    profile: ScanProfile,
    errors: list[ScanError],
    target: Target,
) -> bool:
    logger = get_logger()
    token = _generate_probe_token()
    probe_url = f"{base_url.rstrip('/')}/{token}"

    logger.debug(f"[PATH_PROBE] Test catch-all : {probe_url}")

    try:
        with httpx.Client(timeout=_timeout_for(profile), follow_redirects=False, verify=False) as client:
            response = client.get(probe_url, headers={"User-Agent": profile.user_agent})

            if response.status_code == 200:
                probe_profile = deduce_content_profile(
                    response.headers.get("content-type"), response.text[:500]
                )
                if probe_profile == base_content_profile and probe_profile != "unknown":
                    logger.warning(f"[PATH_PROBE] Catch-all detecte (meme profil : {probe_profile})")
                    return True
                logger.warning(f"[PATH_PROBE] Reponse 200 sur chemin improbable (profil: {probe_profile})")
                return True
            return False

    except Exception as exc:  # noqa: BLE001 - traduit en ScanError, jamais leve
        logger.debug(f"[PATH_PROBE] Test catch-all echoue : {exc}")
        errors.append(
            build_error_from_exception(
                exc,
                module="path_probe",
                phase="path_probe",
                related_target=target.input_raw,
                related_scheme="https" if "https://" in base_url else "http",
                fatal=False,
            )
        )
        return False


def _probe_single_path(
    url: str,
    path: str,
    profile: ScanProfile,
    errors: list[ScanError],
    target: Target,
) -> dict[str, Any]:
    full_url = f"{url.rstrip('/')}/{path.lstrip('/')}"

    result: dict[str, Any] = {
        "path": path,
        "status_code": None,
        "content_profile": "unknown",
        "reason": "not_tested",
    }

    try:
        with httpx.Client(timeout=_timeout_for(profile), follow_redirects=False, verify=False) as client:
            response = client.get(full_url, headers={"User-Agent": profile.user_agent})
            result["status_code"] = response.status_code

            if response.status_code == 200:
                result["reason"] = "ok"
                result["content_profile"] = deduce_content_profile(
                    response.headers.get("content-type"), response.text[:500]
                )
            elif 300 <= response.status_code < 400:
                result["reason"] = "redirect"
            elif response.status_code in (401, 403):
                result["reason"] = "protected"
            elif response.status_code == 404:
                result["reason"] = "not_found"
            else:
                result["reason"] = f"status_{response.status_code}"

    except Exception as exc:  # noqa: BLE001 - traduit en ScanError, jamais leve
        result["reason"] = "error"
        errors.append(
            build_error_from_exception(
                exc, module="path_probe", phase="path_probe",
                related_target=target.input_raw, fatal=False,
            )
        )

    return result


class HttpxPathProber:
    """Implemente ports/path_prober.py::PathProber."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        http_data: dict[str, Any],
        errors: list[ScanError],
    ) -> dict[str, Any]:
        logger = get_logger()
        logger.info(f"[PATH_PROBE] Debut du path probing pour {target.normalized_host}")

        result: dict[str, Any] = {"catch_all_suspected": False, "path_probe_context": []}

        if not profile.path_checks_enabled:
            logger.info("[PATH_PROBE] Path probing desactive par le profil")
            return result

        overview = http_data.get("overview", {})
        preferred_scheme = overview.get("preferred_scheme")
        if not preferred_scheme:
            logger.warning("[PATH_PROBE] Aucun schema prefere, path probing annule")
            return result

        base_url = http_data.get(preferred_scheme, {}).get("final_url")
        if not base_url:
            logger.warning("[PATH_PROBE] Pas d'URL finale, path probing annule")
            return result

        base_content_profile = overview.get("content_profile", "unknown")

        logger.info("[PATH_PROBE] Test catch-all...")
        result["catch_all_suspected"] = _detect_catch_all(
            base_url, base_content_profile, profile, errors, target
        )
        if result["catch_all_suspected"]:
            logger.warning(
                "[PATH_PROBE] Catch-all detecte, les findings de path probing auront une confiance degradee"
            )

        paths_to_test = get_all_probe_paths()
        if profile.path_probe_max_targets > 0:
            paths_to_test = paths_to_test[: profile.path_probe_max_targets]

        logger.info(f"[PATH_PROBE] Test de {len(paths_to_test)} chemins...")

        for i, path in enumerate(paths_to_test):
            if i > 0 and profile.path_probe_delay_ms > 0:
                time.sleep(profile.path_probe_delay_ms / 1000.0)

            probe_result = _probe_single_path(base_url, path, profile, errors, target)

            if result["catch_all_suspected"] and probe_result["reason"] == "ok":
                probe_result["reason"] = "catch_all_suspected"

            result["path_probe_context"].append(probe_result)

        interesting = [
            p for p in result["path_probe_context"]
            if p["reason"] in ("ok", "protected", "catch_all_suspected")
        ]
        logger.info(
            f"[PATH_PROBE] Fin : {len(result['path_probe_context'])} chemins testes, "
            f"{len(interesting)} interessants"
        )
        return result
