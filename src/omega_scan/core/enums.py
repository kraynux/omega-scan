# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Enumerations transverses partagees par plusieurs couches."""
from __future__ import annotations

from enum import Enum

from omega_lib.terminal.models import RenderProfile

__all__ = ["CapabilityStatus", "ExportFormat", "RenderProfile", "ScanProfileName", "ScanStatus"]


class ScanProfileName(str, Enum):
    """Les 4 profils de scan predefinis (lecture seule, pas de CRUD
    utilisateur contrairement aux profils de charge d'omega-stress)."""

    QUICK = "quick"
    STANDARD = "standard"
    EXTENDED = "extended"
    LOCAL_LAB = "local-lab"


class ScanStatus(str, Enum):
    """Statut final d'un ScanRun (domain/scans/service.py::compute_scan_status)."""

    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    PARTIAL = "partial"
    FAILED = "failed"


class CapabilityStatus(str, Enum):
    """Statut d'une capacite consolidee (core/capability.py)."""

    AVAILABLE = "available"
    DEGRADED = "degraded"
    MISSING = "missing"
    DISQUALIFIED = "disqualified"


class ExportFormat(str, Enum):
    """Formats d'export d'un scan : HTML en premier (format par defaut
    propose a l'export, demande utilisateur), texte compact, JSON source
    de verite (pas de CSV, contrairement a omega-stress)."""

    HTML = "html"
    TEXT = "text"
    JSON = "json"
