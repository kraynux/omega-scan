# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Contexte d'exécution du scan.
Contient toutes les informations nécessaires au pipeline,
sans logique métier dispersée.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import uuid

from models.target import Target
from core.errors import ScanError


@dataclass
class ScanContext:
    """
    Contexte complet d'un scan.
    Passé à tous les modules du pipeline.
    """

    # Identification
    scan_id: str = field(default_factory=lambda: f"scan-{uuid.uuid4().hex[:12]}")
    scanner_name: str = "Omega-Scan"
    scanner_version: str = "1.0.0"

    # Timing
    started_at: Optional[str] = None  # ISO 8601 UTC
    finished_at: Optional[str] = None
    duration_ms: int = 0

    # Cible
    target: Optional[Target] = None

    # Profil
    profile_name: str = "standard"  # quick / standard / extended / local-lab

    # Hôte
    host_machine: str = ""

    # Mode opérateur
    operator_mode: str = "interactif"  # interactif / batch

    # Exports demandés
    export_targets: List[str] = field(default_factory=lambda: ["json"])

    # Erreurs accumulées
    errors: List[ScanError] = field(default_factory=list)

    # Statut final
    scan_status: str = "pending"  # pending / running / completed / completed_with_errors / partial / failed

    def start(self):
        """Marque le début du scan."""
        self.started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self.scan_status = "running"

    def finish(self):
        """Marque la fin du scan et calcule la durée."""
        self.finished_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        if self.started_at:
            start_dt = datetime.fromisoformat(self.started_at.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(self.finished_at.replace("Z", "+00:00"))
            self.duration_ms = int((end_dt - start_dt).total_seconds() * 1000)

        # Déterminer le statut final
        if not self.errors:
            self.scan_status = "completed"
        elif any(e.fatal for e in self.errors):
            self.scan_status = "failed"
        else:
            # Erreurs non fatales : le scan a produit des résultats partiels
            self.scan_status = "completed_with_errors"

    def add_error(self, error: ScanError):
        """Ajoute une erreur au contexte."""
        self.errors.append(error)
        if error.fatal:
            self.scan_status = "failed"

    def has_fatal_error(self) -> bool:
        """Vérifie si une erreur fatale est présente."""
        return any(e.fatal for e in self.errors)

    def to_meta_dict(self) -> Dict[str, Any]:
        """
        Extrait le bloc meta pour ScanResult (section 9.1).
        """
        return {
            "scan_id": self.scan_id,
            "scanner_name": self.scanner_name,
            "scanner_version": self.scanner_version,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": self.duration_ms,
            "host_machine": self.host_machine,
            "operator_mode": self.operator_mode,
            "export_targets": self.export_targets,
        }
