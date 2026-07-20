# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Objet Summary (section 9.8 de la spec).
Résumé synthétique du scan pour affichage rapide.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict


@dataclass
class Summary:
    """Résumé synthétique du scan."""
    
    # Statut global
    scan_status: str  # "completed", "completed_with_errors", "partial", "failed"
    
    # Compteurs
    checks_total: int  # Toutes les règles évaluées (OK + WARN + FAIL + N/A)
    findings_total: int  # WARN + FAIL uniquement (pas OK, pas N/A)
    
    # Ventilation
    status_breakdown: Dict[str, int]  # {"OK": 15, "WARN": 3, "FAIL": 2, "N/A": 5}
    severity_breakdown: Dict[str, int]  # {"info": 1, "low": 2, "medium": 1, "high": 1}
    category_breakdown: Dict[str, int]  # {"transport": 2, "headers": 3, ...}
    
    # Top issues
    top_issues: List[str]  # 3-5 titres de findings les plus importants
    
    # Note globale
    overall_rating: str  # "A", "B", "C", "D", "F" ou "N/A"
    short_message: str  # Message court pour l'utilisateur
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire JSON-serializable."""
        return asdict(self)
