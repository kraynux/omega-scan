# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Mise en forme des reponses HTTP brutes (ex normalizers/*.py de la v1).

Partagees par httpx_http_prober.py et httpx_path_prober.py, qui ont toutes
deux besoin de deduire un content_profile. Restent des fonctions pures
(aucune I/O) : placees en infrastructure/ plutot qu'en domain/ parce
qu'elles mettent en forme le resultat brut d'une collecte (etape avant
jugement), pas une regle de securite jugeant une preuve — cette derniere
responsabilite reste entierement dans domain/checks/*/service.py."""
from __future__ import annotations

from typing import Any

PROXY_HEADERS = {
    "x-forwarded-for",
    "x-forwarded-proto",
    "x-forwarded-host",
    "via",
    "forwarded",
}


def detect_proxy_suspected(headers: dict[str, str]) -> bool:
    """Detecte si un proxy/tunnel est suspecte a partir des headers."""
    headers_lower = {k.lower(): v for k, v in headers.items()}
    return any(h in headers_lower for h in PROXY_HEADERS)


def deduce_content_profile(content_type: str | None, body_preview: str | None) -> str:
    """Deduit html_page / json_api / plain_text / unknown depuis le
    Content-Type et un extrait du corps."""
    if not content_type:
        return "unknown"

    ct_lower = content_type.lower()

    if "application/json" in ct_lower:
        return "json_api"
    if "text/plain" in ct_lower:
        return "plain_text"
    if "text/html" in ct_lower:
        if body_preview:
            body_lower = body_preview.lower()
            if "<html" in body_lower or "<!doctype html" in body_lower or "<head" in body_lower:
                return "html_page"
        return "unknown"
    return "unknown"


def normalize_cookies(cookies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalise les cookies observes : name, value, domain, path, secure,
    httponly, samesite."""
    return [
        {
            "name": cookie.get("name", ""),
            "value": cookie.get("value", ""),
            "domain": cookie.get("domain", ""),
            "path": cookie.get("path", "/"),
            "secure": cookie.get("secure", False),
            "httponly": cookie.get("httponly", False),
            "samesite": cookie.get("samesite", None),
        }
        for cookie in cookies
    ]


def normalize_redirect_chain(redirect_history: list[Any]) -> list[dict[str, Any]]:
    """Normalise la chaine de redirections httpx : url, status."""
    return [{"url": str(response.url), "status": response.status_code} for response in redirect_history]
