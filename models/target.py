# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Objet Target canonique (section 2.4 de la spec).
Produit une seule fois par target_parser.py, puis réutilisé par tous les modules.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List


@dataclass
class Target:
    """Représentation canonique d'une cible de scan."""
    
    # Entrée brute
    input_raw: str
    
    # Host normalisé (sans schéma, sans port, sans chemin)
    normalized_host: str
    
    # URLs normalisées
    normalized_url_http: str
    normalized_url_https: str
    
    # Intention utilisateur
    requested_scheme: Optional[str]  # "http", "https", ou None (auto)
    requested_port: Optional[int]
    requested_path: str  # "/" par défaut
    
    # Classification
    target_kind: str  # "hostname", "ipv4", "ipv6"
    scope_kind: str  # "loopback", "link_local", "private_lan", "special_non_global", "public", "hostname"
    
    # Modes de scan
    scan_modes: str  # "http", "https", "both"
    
    # Propriétés IP
    is_ip: bool
    ip_version: Optional[int]  # 4, 6, ou None si hostname
    is_private: bool
    is_loopback: bool
    is_link_local: bool
    is_global: bool
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire JSON-serializable."""
        return asdict(self)
