# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Normalisation des headers HTTP.
Section 7, 8 et 9.5 de la spec.
Déduit content_profile et proxy_suspected.
"""

from typing import Dict, Any, Optional


# Headers indicateurs de proxy/tunnel (section 7.1)
PROXY_HEADERS = {
    "x-forwarded-for",
    "x-forwarded-proto",
    "x-forwarded-host",
    "via",
    "forwarded",
}


def detect_proxy_suspected(headers: Dict[str, str]) -> bool:
    """
    Détecte si un proxy/tunnel est suspecté basé sur les headers.
    Section 7.1 de la spec.
    """
    headers_lower = {k.lower(): v for k, v in headers.items()}
    return any(h in headers_lower for h in PROXY_HEADERS)


def deduce_content_profile(
    content_type: Optional[str],
    body_preview: Optional[str],
) -> str:
    """
    Déduit le profil de contenu à partir du Content-Type et du corps.
    Section 9.5 de la spec.
    Retourne : html_page, json_api, plain_text, ou unknown.
    """
    if not content_type:
        return "unknown"
    
    ct_lower = content_type.lower()
    
    # JSON API
    if "application/json" in ct_lower:
        return "json_api"
    
    # Plain text
    if "text/plain" in ct_lower:
        return "plain_text"
    
    # HTML page : doit avoir text/html ET des balises HTML dans le corps
    if "text/html" in ct_lower:
        if body_preview:
            body_lower = body_preview.lower()
            if "<html" in body_lower or "<!doctype html" in body_lower or "<head" in body_lower:
                return "html_page"
        # Si pas de corps ou pas de balises, rester prudent
        return "unknown"
    
    # Autres types (XML, CSS, JS, images, etc.)
    return "unknown"


def normalize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Normalise les headers pour stockage dans scan_result.
    Conserve les clés telles quelles (case-sensitive pour l'affichage).
    """
    return dict(headers)
