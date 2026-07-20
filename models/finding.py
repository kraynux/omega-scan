# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Objet Finding (section 10 de la spec).
Résultat d'une règle d'analyse appliquée aux preuves collectées.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from models.evidence import Evidence


@dataclass
class Finding:
    """Résultat d'une règle d'analyse."""
    
    # Identification
    finding_id: str  # UUID ou identifiant unique
    rule_id: str  # Ex: "TRN-HTTPS-001", "HDR-CSP-001"
    category: str  # "transport", "headers", "cookies", "methods", "exposure", "information_leak"
    title: str
    
    # Verdict
    status: str  # "OK", "WARN", "FAIL", "N/A"
    severity: str  # "info", "low", "medium", "high", "critical"
    confidence: str  # "certain", "high", "medium", "low"
    applicability: str  # "applicable", "conditional", "not_applicable"
    
    # Explication
    description: str
    impact: str
    remediation: str
    
    # Preuve
    evidence: Optional[Evidence] = None
    
    # Localisation
    location: Optional[Dict[str, Any]] = None  # {url, host, port, scheme, path, component}
    
    # Métadonnées
    references: List[str] = field(default_factory=list)  # Liens externes
    tags: List[str] = field(default_factory=list)  # Tags pour filtrage
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire JSON-serializable."""
        result = asdict(self)
        if self.evidence:
            result["evidence"] = self.evidence.to_dict()
        return result
