# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation httpx du port HttpProber (collecte HTTP/HTTPS principale)."""
from __future__ import annotations

import time
from typing import Any

import httpx

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target
from omega_scan.infrastructure.exceptions import build_error_from_exception
from omega_scan.infrastructure.logging.app_logger import get_logger
from omega_scan.infrastructure.network._shaping import (
    deduce_content_profile,
    detect_proxy_suspected,
    normalize_cookies,
    normalize_redirect_chain,
)
from omega_scan.shared.i18n import N_, log_text

BODY_PREVIEW_MAX_CHARS = 500


def _build_body_preview(response: httpx.Response) -> dict[str, Any]:
    try:
        text = response.text
        size_bytes = len(response.content)
        encoding = response.encoding or "utf-8"

        truncated = False
        if len(text) > BODY_PREVIEW_MAX_CHARS:
            text = text[:BODY_PREVIEW_MAX_CHARS]
            truncated = True

        return {
            "text_preview": text,
            "size_bytes": size_bytes,
            "encoding": encoding,
            "preview_truncated": truncated,
        }
    except Exception:  # noqa: BLE001 - decodage best-effort
        return {
            "text_preview": "",
            "size_bytes": len(response.content) if response.content else 0,
            "encoding": "unknown",
            "preview_truncated": False,
        }


def _extract_cookies(response: httpx.Response) -> list[dict[str, Any]]:
    """HttpOnly/SameSite ne sont pas exposes par l'API publique de
    `http.cookiejar.Cookie` (utilise en interne par httpx), mais restent
    accessibles via l'attribut `_rest` (dict des attributs non standards du
    Set-Cookie, tel que parse) — technique standard, deja utilisee par de
    nombreux projets confrontes a la meme limitation d'httpx/cookiejar.
    Corrige un defaut reel : ces deux champs valaient auparavant toujours
    False/None, quelle que soit la reponse observee (Lot M5)."""
    cookies = []
    for cookie in response.cookies.jar:
        rest = {k.lower(): v for k, v in getattr(cookie, "_rest", {}).items()}
        cookies.append(
            {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain or "",
                "path": cookie.path or "/",
                "secure": cookie.secure,
                "httponly": "httponly" in rest,
                "samesite": rest.get("samesite"),
            }
        )
    return cookies


def _empty_scheme_result(url: str, profile: ScanProfile) -> dict[str, Any]:
    return {
        "attempted": False,
        "requested_url": url,
        "final_url": url,
        "status_code": None,
        "reason": None,
        "ok": False,
        "elapsed_ms": None,
        "content_type": None,
        "content_length": None,
        "headers": {},
        "cookies": [],
        "redirect_chain": [],
        "request": {"method": "GET", "headers_sent": {}, "user_agent": profile.user_agent},
        "body_preview": {
            "text_preview": "",
            "size_bytes": 0,
            "encoding": "unknown",
            "preview_truncated": False,
        },
        "error": None,
        "content_profile": "unknown",
    }


def _probe_scheme(
    url: str,
    scheme: str,
    profile: ScanProfile,
    errors: list[ScanError],
    target: Target,
) -> dict[str, Any]:
    logger = get_logger()
    result = _empty_scheme_result(url, profile)
    result["attempted"] = True

    timeout = httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )
    verify = scheme != "https"

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=profile.follow_redirects,
            max_redirects=profile.max_redirects,
            verify=verify,
        ) as client:
            start = time.time()
            response = client.get(url, headers={"User-Agent": profile.user_agent})
            elapsed_ms = int((time.time() - start) * 1000)

            result["final_url"] = str(response.url)
            result["status_code"] = response.status_code
            result["reason"] = response.reason_phrase
            result["ok"] = response.is_success
            result["elapsed_ms"] = elapsed_ms
            result["content_type"] = response.headers.get("content-type")
            result["content_length"] = int(response.headers.get("content-length", 0))
            result["headers"] = dict(response.headers)
            result["cookies"] = normalize_cookies(_extract_cookies(response))
            result["redirect_chain"] = normalize_redirect_chain(response.history)
            result["body_preview"] = _build_body_preview(response)

            logger.log_network_attempt(
                scheme=scheme, url=url, success=True,
                status_code=response.status_code, elapsed_ms=elapsed_ms,
            )
    except Exception as exc:  # noqa: BLE001 - traduit en ScanError, jamais leve
        result["ok"] = False
        result["error"] = str(exc)
        logger.log_network_attempt(scheme=scheme, url=url, success=False, error=str(exc))
        errors.append(
            build_error_from_exception(
                exc,
                module="http_probe",
                phase="http_probe",
                related_target=target.input_raw,
                related_scheme=scheme,
                fatal=False,
            )
        )

    return result


_CORS_PROBE_ORIGIN = "https://omega-scan-cors-probe.invalid"


def _empty_cors_result() -> dict[str, Any]:
    return {
        "attempted": False,
        "allow_origin": None,
        "allow_credentials": False,
        "reflects_arbitrary_origin": False,
    }


def _probe_cors(url: str | None, profile: ScanProfile) -> dict[str, Any]:
    """Sonde CORS optionnelle (Lot M5) : envoie une requete GET avec un
    header Origin arbitraire et observe si le serveur la reflete ou renvoie
    un wildcard. Best-effort : un echec n'est jamais ajoute a `errors` ni
    journalise comme un echec de scan (cette sonde est un approfondissement
    facultatif, pas une etape critique du pipeline)."""
    cors_data = _empty_cors_result()
    if not url:
        return cors_data

    timeout = httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )
    try:
        with httpx.Client(timeout=timeout, follow_redirects=profile.follow_redirects) as client:
            response = client.get(
                url,
                headers={"User-Agent": profile.user_agent, "Origin": _CORS_PROBE_ORIGIN},
            )
        cors_data["attempted"] = True
        allow_origin = response.headers.get("access-control-allow-origin")
        allow_credentials = (
            response.headers.get("access-control-allow-credentials", "").strip().lower() == "true"
        )
        cors_data["allow_origin"] = allow_origin
        cors_data["allow_credentials"] = allow_credentials
        cors_data["reflects_arbitrary_origin"] = allow_origin == _CORS_PROBE_ORIGIN
    except Exception:  # noqa: BLE001, S110 - sonde best-effort, ne doit jamais faire echouer le scan
        pass
    return cors_data


class HttpxHttpProber:
    """Implemente ports/http_prober.py::HttpProber."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        errors: list[ScanError],
    ) -> dict[str, Any]:
        logger = get_logger()
        logger.info(log_text(N_("[HTTP_PROBE] Début de la collecte HTTP pour {normalized_host}"), normalized_host=target.normalized_host))

        http_result = None
        https_result = None

        if target.scan_modes in ("http", "both"):
            http_result = _probe_scheme(target.normalized_url_http, "http", profile, errors, target)
        if target.scan_modes in ("https", "both"):
            https_result = _probe_scheme(
                target.normalized_url_https, "https", profile, errors, target
            )

        overview: dict[str, Any] = {
            "preferred_scheme": None,
            "catch_all_suspected": False,  # rempli par path_prober
            "proxy_suspected": False,
            "content_profile": "unknown",
            "path_probe_context": [],  # rempli par path_prober
        }

        if https_result and https_result["ok"]:
            overview["preferred_scheme"] = "https"
        elif http_result and http_result["ok"]:
            overview["preferred_scheme"] = "http"

        proxy_headers = (https_result or {}).get("headers") or (http_result or {}).get("headers")
        if proxy_headers and detect_proxy_suspected(proxy_headers):
            overview["proxy_suspected"] = True

        if overview["preferred_scheme"] == "https" and https_result:
            overview["content_profile"] = deduce_content_profile(
                https_result["content_type"], https_result["body_preview"]["text_preview"]
            )
            https_result["content_profile"] = overview["content_profile"]
        elif overview["preferred_scheme"] == "http" and http_result:
            overview["content_profile"] = deduce_content_profile(
                http_result["content_type"], http_result["body_preview"]["text_preview"]
            )
            http_result["content_profile"] = overview["content_profile"]

        if http_result and http_result["ok"]:
            http_result["content_profile"] = deduce_content_profile(
                http_result["content_type"], http_result["body_preview"]["text_preview"]
            )
        if https_result and https_result["ok"]:
            https_result["content_profile"] = deduce_content_profile(
                https_result["content_type"], https_result["body_preview"]["text_preview"]
            )

        logger.info(
            log_text(N_("[HTTP_PROBE] Fin de la collecte : preferred={preferred_scheme}, "
                        "proxy={proxy_suspected}, content={content_profile}"), preferred_scheme=overview['preferred_scheme'], proxy_suspected=overview['proxy_suspected'], content_profile=overview['content_profile'])
        )

        # Sonde CORS optionnelle (Lot M5), gatee comme le path probing (absente
        # du profil "quick", coherent avec l'esprit rapide/minimal de ce profil).
        cors_data = _empty_cors_result()
        if profile.path_checks_enabled:
            preferred_result = (
                https_result if overview["preferred_scheme"] == "https" else http_result
            )
            preferred_url = preferred_result.get("requested_url") if preferred_result else None
            cors_data = _probe_cors(preferred_url, profile)

        return {
            "overview": overview,
            "http": http_result if http_result else _empty_scheme_result(
                target.normalized_url_http, profile
            ),
            "https": https_result if https_result else _empty_scheme_result(
                target.normalized_url_https, profile
            ),
            "cors": cors_data,
        }
