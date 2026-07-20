# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Collecte HTTP/HTTPS principale.
Section 9.5 de la spec.
Objectif : capturer les réponses principales avec tous les détails.
"""

import time
from typing import Dict, Any, List, Optional
import httpx

from models.target import Target
from config.profiles import ScanProfile
from core.errors import ScanError, build_error_from_exception
from core.logger import get_logger
from normalizers.headers import detect_proxy_suspected, deduce_content_profile
from normalizers.cookies import normalize_cookies
from normalizers.redirects import normalize_redirect_chain


# Limite de taille pour le body preview (en caractères)
BODY_PREVIEW_MAX_CHARS = 500


def _build_body_preview(response: httpx.Response) -> Dict[str, Any]:
    """
    Construit le body_preview à partir de la réponse.
    Section 9.5 de la spec.
    """
    try:
        # Essayer de décoder le texte
        text = response.text
        size_bytes = len(response.content)
        encoding = response.encoding or "utf-8"
        
        # Tronquer si nécessaire
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
    except Exception:
        # Si le décodage échoue, retourner un preview vide
        return {
            "text_preview": "",
            "size_bytes": len(response.content) if response.content else 0,
            "encoding": "unknown",
            "preview_truncated": False,
        }


def _extract_cookies(response: httpx.Response) -> List[Dict[str, Any]]:
    """
    Extrait les cookies de la réponse.
    """
    cookies = []
    for cookie in response.cookies.jar:
        cookies.append({
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain or "",
            "path": cookie.path or "/",
            "secure": cookie.secure,
            "httponly": False,  # httpx ne expose pas directement httponly
            "samesite": None,  # httpx ne expose pas directement samesite
        })
    return cookies


def _probe_scheme(
    url: str,
    scheme: str,
    profile: ScanProfile,
    errors: List[ScanError],
    target: Target,
) -> Dict[str, Any]:
    """
    Effectue une requête HTTP ou HTTPS et retourne le résultat brut.
    """
    logger = get_logger()
    
    result = {
        "attempted": True,
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
        "request": {
            "method": "GET",
            "headers_sent": {},
            "user_agent": profile.user_agent,
        },
        "body_preview": {
            "text_preview": "",
            "size_bytes": 0,
            "encoding": "unknown",
            "preview_truncated": False,
        },
        "error": None,
        "content_profile": "unknown",
    }
    
    # Configuration httpx
    timeout = httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )
    
    # Pour HTTPS, désactiver la vérification du certificat (on observe, on ne juge pas)
    verify = scheme != "https"
    
    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=profile.follow_redirects,
            max_redirects=profile.max_redirects,
            verify=verify,
        ) as client:
            start = time.time()
            response = client.get(
                url,
                headers={"User-Agent": profile.user_agent},
            )
            elapsed_ms = int((time.time() - start) * 1000)
            
            # Remplir le résultat
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
                scheme=scheme,
                url=url,
                success=True,
                status_code=response.status_code,
                elapsed_ms=elapsed_ms,
            )
    
    except Exception as e:
        result["ok"] = False
        result["error"] = str(e)
        logger.log_network_attempt(
            scheme=scheme,
            url=url,
            success=False,
            error=str(e),
        )
        errors.append(
            build_error_from_exception(
                e,
                module="http_probe",
                phase="http_probe",
                related_target=target.input_raw,
                related_scheme=scheme,
                fatal=False,
            )
        )
    
    return result


def probe_http(
    target: Target,
    profile: ScanProfile,
    errors: List[ScanError],
) -> Dict[str, Any]:
    """
    Collecte HTTP/HTTPS principale.
    Section 9.5 de la spec.
    Retourne le bloc http complet avec overview, http, https.
    """
    logger = get_logger()
    logger.info(f"[HTTP_PROBE] Début de la collecte HTTP pour {target.normalized_host}")
    
    http_result = None
    https_result = None
    
    # Tester HTTP si demandé
    if target.scan_modes in ("http", "both"):
        logger.info(f"[HTTP_PROBE] Test HTTP : {target.normalized_url_http}")
        http_result = _probe_scheme(
            target.normalized_url_http,
            "http",
            profile,
            errors,
            target,
        )
    
    # Tester HTTPS si demandé
    if target.scan_modes in ("https", "both"):
        logger.info(f"[HTTP_PROBE] Test HTTPS : {target.normalized_url_https}")
        https_result = _probe_scheme(
            target.normalized_url_https,
            "https",
            profile,
            errors,
            target,
        )
    
    # Construire http.overview
    overview = {
        "preferred_scheme": None,
        "catch_all_suspected": False,  # Sera rempli par path_probe (Lot 9)
        "proxy_suspected": False,
        "content_profile": "unknown",
        "path_probe_context": [],  # Sera rempli par path_probe (Lot 9)
    }
    
    # Déterminer le schéma préféré
    if https_result and https_result["ok"]:
        overview["preferred_scheme"] = "https"
    elif http_result and http_result["ok"]:
        overview["preferred_scheme"] = "http"
    
    # Détecter proxy_suspected (section 7)
    if https_result and https_result["headers"]:
        if detect_proxy_suspected(https_result["headers"]):
            overview["proxy_suspected"] = True
    elif http_result and http_result["headers"]:
        if detect_proxy_suspected(http_result["headers"]):
            overview["proxy_suspected"] = True
    
    # Déduire content_profile pour overview (basé sur le schéma préféré)
    if overview["preferred_scheme"] == "https" and https_result:
        overview["content_profile"] = deduce_content_profile(
            https_result["content_type"],
            https_result["body_preview"]["text_preview"],
        )
        https_result["content_profile"] = overview["content_profile"]
    elif overview["preferred_scheme"] == "http" and http_result:
        overview["content_profile"] = deduce_content_profile(
            http_result["content_type"],
            http_result["body_preview"]["text_preview"],
        )
        http_result["content_profile"] = overview["content_profile"]
    
    # Déduire content_profile pour chaque schéma individuellement
    if http_result and http_result["ok"]:
        http_result["content_profile"] = deduce_content_profile(
            http_result["content_type"],
            http_result["body_preview"]["text_preview"],
        )
    if https_result and https_result["ok"]:
        https_result["content_profile"] = deduce_content_profile(
            https_result["content_type"],
            https_result["body_preview"]["text_preview"],
        )
    
    logger.info(
        f"[HTTP_PROBE] Fin de la collecte : preferred={overview['preferred_scheme']}, "
        f"proxy={overview['proxy_suspected']}, content={overview['content_profile']}"
    )
    
    return {
        "overview": overview,
        "http": http_result if http_result else {
            "attempted": False,
            "requested_url": target.normalized_url_http,
            "final_url": target.normalized_url_http,
            "status_code": None,
            "reason": None,
            "ok": False,
            "elapsed_ms": None,
            "content_type": None,
            "content_length": None,
            "headers": {},
            "cookies": [],
            "redirect_chain": [],
            "request": {
                "method": "GET",
                "headers_sent": {},
                "user_agent": profile.user_agent,
            },
            "body_preview": {
                "text_preview": "",
                "size_bytes": 0,
                "encoding": "unknown",
                "preview_truncated": False,
            },
            "error": None,
            "content_profile": "unknown",
        },
        "https": https_result if https_result else {
            "attempted": False,
            "requested_url": target.normalized_url_https,
            "final_url": target.normalized_url_https,
            "status_code": None,
            "reason": None,
            "ok": False,
            "elapsed_ms": None,
            "content_type": None,
            "content_length": None,
            "headers": {},
            "cookies": [],
            "redirect_chain": [],
            "request": {
                "method": "GET",
                "headers_sent": {},
                "user_agent": profile.user_agent,
            },
            "body_preview": {
                "text_preview": "",
                "size_bytes": 0,
                "encoding": "unknown",
                "preview_truncated": False,
            },
            "error": None,
            "content_profile": "unknown",
        },
    }
