# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Normalisation de la chaîne de redirections.
Section 9.5 de la spec.
"""

from typing import List, Dict, Any


def normalize_redirect_chain(redirect_history: List[Any]) -> List[Dict[str, Any]]:
    """
    Normalise la chaîne de redirections pour stockage dans scan_result.
    Chaque entrée doit avoir : url, status.
    """
    normalized = []
    for response in redirect_history:
        normalized.append({
            "url": str(response.url),
            "status": response.status_code,
        })
    return normalized
