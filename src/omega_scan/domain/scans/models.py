# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Objets Summary, ScanError et ScanRun : resultat complet d'un scan.

`ScanRun` remplace l'ancien `ScanResult` (renomme pour coherence avec
ARCHITECTURE.md, qui l'utilise partout — notamment pour l'historique et la
comparaison de scans, absents de la v1)."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from omega_scan.domain.findings.models import Finding
from omega_scan.domain.targets.models import Target

# Categories d'echec reseau (section 3.1 et 9.9 de la spec v1)
FAILURE_CATEGORY_DNS = "dns_failure"
FAILURE_CATEGORY_REFUSED = "connection_refused"
FAILURE_CATEGORY_TIMEOUT = "timeout"
FAILURE_CATEGORY_TLS_HANDSHAKE = "tls_handshake_failure"
FAILURE_CATEGORY_RESET = "reset_by_peer"
FAILURE_CATEGORY_UNKNOWN = "unknown"

VALID_FAILURE_CATEGORIES = {
    FAILURE_CATEGORY_DNS,
    FAILURE_CATEGORY_REFUSED,
    FAILURE_CATEGORY_TIMEOUT,
    FAILURE_CATEGORY_TLS_HANDSHAKE,
    FAILURE_CATEGORY_RESET,
    FAILURE_CATEGORY_UNKNOWN,
}

# Phases du pipeline ou une erreur peut survenir
PHASE_VALIDATION = "validation"
PHASE_NORMALIZATION = "normalization"
PHASE_CONNECTIVITY = "connectivity"
PHASE_HTTP_PROBE = "http_probe"
PHASE_TLS_PROBE = "tls_probe"
PHASE_PATH_PROBE = "path_probe"
PHASE_METHODS_PROBE = "methods_probe"
PHASE_NORMALIZERS = "normalizers"
PHASE_CHECKS = "checks"
PHASE_PIPELINE = "pipeline"
PHASE_EXPORT = "export"


@dataclass
class ScanError:
    """Erreur survenue pendant le scan (structure alignee sur la section
    9.9 de la spec v1). Une donnee collectee, jamais levee comme exception."""

    module: str
    phase: str
    error_type: str
    message: str
    fatal: bool = False
    related_target: str | None = None
    related_scheme: str | None = None
    failure_category: str | None = None

    def __post_init__(self) -> None:
        if self.failure_category and self.failure_category not in VALID_FAILURE_CATEGORIES:
            raise ValueError(
                f"failure_category invalide : {self.failure_category}. "
                f"Valeurs autorisees : {VALID_FAILURE_CATEGORIES}"
            )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Summary:
    """Resume synthetique du scan pour affichage rapide."""

    scan_status: str  # "completed", "completed_with_errors", "partial", "failed"
    checks_total: int  # Toutes les regles evaluees (OK + WARN + FAIL + N/A)
    findings_total: int  # WARN + FAIL uniquement

    status_breakdown: dict[str, int]
    severity_breakdown: dict[str, int]
    category_breakdown: dict[str, int]

    top_issues: list[str]

    overall_rating: str  # "A", "B", "C", "D", "F" ou "N/A"
    short_message: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScanRun:
    """Resultat complet d'un scan (ex `ScanResult`)."""

    meta: dict[str, Any]  # scan_id, scanner_name, scanner_version, started_at, finished_at, duration_ms, ...
    target: Target
    scan_profile: dict[str, Any]
    connectivity: dict[str, Any]
    http: dict[str, Any]
    tls: dict[str, Any]
    findings: list[Finding]
    summary: Summary
    errors: list[dict[str, Any]]

    def to_dict(self) -> dict:
        return {
            "meta": self.meta,
            "target": self.target.to_dict(),
            "scan_profile": self.scan_profile,
            "connectivity": self.connectivity,
            "http": self.http,
            "tls": self.tls,
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.summary.to_dict(),
            "errors": self.errors,
        }
