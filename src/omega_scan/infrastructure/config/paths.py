# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Resolution des chemins runtime (var/), la seule source de verite pour ces chemins."""
from __future__ import annotations

import os
from pathlib import Path

DEFAULT_VAR_DIRNAME = "var"
ENV_VAR_DIR = "OMEGA_SCAN_VAR_DIR"


def resolve_var_dir() -> Path:
    """Racine des fichiers runtime : `$OMEGA_SCAN_VAR_DIR` si defini,
    sinon `./var` relatif au repertoire courant d'execution."""
    override = os.environ.get(ENV_VAR_DIR)
    if override:
        return Path(override)
    return Path.cwd() / DEFAULT_VAR_DIRNAME


def db_path(var_dir: Path | None = None) -> Path:
    base = var_dir if var_dir is not None else resolve_var_dir()
    return base / "db" / "app.db"


def settings_path(var_dir: Path | None = None) -> Path:
    base = var_dir if var_dir is not None else resolve_var_dir()
    return base / "settings.json"


def exports_dir(var_dir: Path | None = None) -> Path:
    base = var_dir if var_dir is not None else resolve_var_dir()
    return base / "exports"


def screenshots_dir(var_dir: Path | None = None) -> Path:
    """Dossier par defaut des captures d'ecran SVG (App.deliver_screenshot()
    sans `path=` explicite ecrirait sinon dans le dossier Telechargements
    de l'utilisateur, jamais var/ — meme piege deja documente et corrige
    cote omega-stress)."""
    base = var_dir if var_dir is not None else resolve_var_dir()
    return base / "screenshots"
