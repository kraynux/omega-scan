# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Normalisation des cookies HTTP.
Section 9.5 de la spec.
"""

from typing import List, Dict, Any


def normalize_cookies(cookies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalise les cookies pour stockage dans scan_result.
    Chaque cookie doit avoir : name, value, domain, path, secure, httponly, samesite.
    """
    normalized = []
    for cookie in cookies:
        normalized.append({
            "name": cookie.get("name", ""),
            "value": cookie.get("value", ""),
            "domain": cookie.get("domain", ""),
            "path": cookie.get("path", "/"),
            "secure": cookie.get("secure", False),
            "httponly": cookie.get("httponly", False),
            "samesite": cookie.get("samesite", None),
        })
    return normalized
