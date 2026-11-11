# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Assemblage manuel des adaptateurs concrets derriere les ports (pas de framework DI)."""
from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from omega_lib.infrastructure.declaration import build_contact_support
from omega_lib.infrastructure.declaration.app_version import project_version
from omega_lib.infrastructure.terminal.detector import SystemTerminalDetector
from omega_lib.ports.declaration import ContactSupportServices

from omega_scan.application.pipeline.hooks.audit_hook import AuditSink
from omega_scan.infrastructure.config import paths
from omega_scan.infrastructure.exporters.exporter import DefaultReportExporter
from omega_scan.infrastructure.logging.app_logger import get_logger
from omega_scan.infrastructure.logging.audit_logger import AuditLogger
from omega_scan.infrastructure.network.httpx_connectivity_prober import HttpxConnectivityProber
from omega_scan.infrastructure.network.httpx_http_prober import HttpxHttpProber
from omega_scan.infrastructure.network.httpx_methods_prober import HttpxMethodsProber
from omega_scan.infrastructure.network.httpx_path_prober import HttpxPathProber
from omega_scan.infrastructure.network.httpx_tls_prober import HttpxTlsProber
from omega_scan.infrastructure.storage.files.json_settings_store import JsonSettingsStore
from omega_scan.infrastructure.storage.sqlite.connection import open_connection
from omega_scan.infrastructure.storage.sqlite.migrations import apply_schema
from omega_scan.infrastructure.storage.sqlite.scan_repository import SqliteScanRepository
from omega_scan.infrastructure.storage.sqlite.target_repository import SqliteTargetRepository

SOFTWARE = "omega-scan"
"""Nom du logiciel pour la reception des declarations et le site (download/)."""
PROJECT_ROOT = Path(__file__).resolve().parents[3]
"""Racine du projet : pyproject.toml, seule source de la version."""


@dataclass(frozen=True, slots=True)
class DependencyContainer:
    """Regroupe toutes les instances d'adaptateurs concretes, construites
    une fois au demarrage et partagees pour toute la duree du processus.
    Noms de champs fixes par le Lot M4a (interfaces/cli/) : ce container
    doit les honorer a l'identique, le CLI et le TUI consomment le meme
    objet sans variante."""

    connection: sqlite3.Connection
    target_repository: SqliteTargetRepository
    scan_repository: SqliteScanRepository
    connectivity_prober: HttpxConnectivityProber
    http_prober: HttpxHttpProber
    tls_prober: HttpxTlsProber
    path_prober: HttpxPathProber
    methods_prober: HttpxMethodsProber
    audit_sink: AuditSink
    report_exporter: DefaultReportExporter
    terminal_detector: SystemTerminalDetector
    settings_store: JsonSettingsStore
    technical_logger: logging.Logger
    default_exports_dir: Path = field(default_factory=paths.exports_dir)
    default_screenshots_dir: Path = field(default_factory=paths.screenshots_dir)
    contact_support: ContactSupportServices | None = None
    """Aide -> Contact et support (omega-lib, D-016, 2026-11-09) : declaration anonyme une seule
    fois, mises a jour, navigateur. None : bouton masque (conteneur partiel des tests)."""


def build_container(*, var_dir: Path | None = None) -> DependencyContainer:
    """Construit et cable l'integralite des adaptateurs concrets. Ouvre
    la connexion SQLite et applique le schema : appeler une seule fois
    par processus."""
    base = var_dir if var_dir is not None else paths.resolve_var_dir()

    connection = open_connection(paths.db_path(base))
    apply_schema(connection)
    audit_logger = AuditLogger(base / "audit.jsonl")

    return DependencyContainer(
        contact_support=build_contact_support(SOFTWARE, project_version(PROJECT_ROOT, SOFTWARE), base),
        connection=connection,
        target_repository=SqliteTargetRepository(connection),
        scan_repository=SqliteScanRepository(connection),
        connectivity_prober=HttpxConnectivityProber(),
        http_prober=HttpxHttpProber(),
        tls_prober=HttpxTlsProber(),
        path_prober=HttpxPathProber(),
        methods_prober=HttpxMethodsProber(),
        audit_sink=audit_logger.record,
        report_exporter=DefaultReportExporter(),
        terminal_detector=SystemTerminalDetector(),
        settings_store=JsonSettingsStore(paths.settings_path(base)),
        technical_logger=get_logger().logger,
        default_exports_dir=paths.exports_dir(base),
        default_screenshots_dir=paths.screenshots_dir(base),
    )
