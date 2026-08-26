# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Point d'assemblage complet de l'application, appele une fois par processus."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from omega_scan.app.dependency_container import DependencyContainer, build_container
from omega_scan.app.lifecycle import AppLifecycle
from omega_scan.infrastructure.config import paths
from omega_scan.infrastructure.logging.app_logger import ScanLogger, set_logger
from omega_scan.infrastructure.logging.config import APP_LOG_FILENAME


@dataclass(frozen=True, slots=True)
class Application:
    """Resultat complet du demarrage : le conteneur cable et son cycle
    de vie, prets a etre distribues a interfaces/tui/ ou interfaces/cli/."""

    container: DependencyContainer
    lifecycle: AppLifecycle


def bootstrap(*, var_dir: Path | None = None, console_logging: bool = True) -> Application:
    """Sequence de demarrage complete : resout les chemins runtime,
    configure la journalisation technique, cable les adaptateurs
    concrets. Appeler une seule fois par processus.

    `console_logging=False` pour le TUI (voir __main__.py) : Textual
    prend le controle exclusif de l'ecran, une ecriture de log directe sur
    stderr pendant un scan corromprait son rendu. Le CLI garde
    `console_logging=True` par defaut (utile pour le scriptable/debug)."""
    base = var_dir if var_dir is not None else paths.resolve_var_dir()
    base.mkdir(parents=True, exist_ok=True)

    set_logger(
        ScanLogger(name="omega-scan", log_file=base / APP_LOG_FILENAME, console=console_logging)
    )
    container = build_container(var_dir=base)

    return Application(container=container, lifecycle=AppLifecycle(container=container))
