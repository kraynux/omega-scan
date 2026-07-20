# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Objet Evidence (section 10 de la spec).
Représente une preuve concrète associée à un finding.
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Evidence:
    """Preuve concrète associée à un finding."""
    
    type: str  # "header", "cookie", "status_code", "body_content", "tls_field", etc.
    value: str  # Valeur observée
    source: str  # Origine (ex: "response.headers", "tls.certificate")
    excerpt: Optional[str] = None  # Extrait contextuel (optionnel)
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire JSON-serializable."""
        return asdict(self)
