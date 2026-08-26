# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Generation d'identifiants opaques."""
from __future__ import annotations

import uuid


def new_id() -> str:
    """Identifiant opaque unique (hex UUID4), utilise pour toute entite
    creee cote application."""
    return uuid.uuid4().hex


def new_scan_id() -> str:
    """Identifiant d'un scan, meme format que l'ancien
    core/context.py::ScanContext.scan_id de la v1 ("scan-" + 12 hex) —
    conserve pour ne pas invalider le format deja utilise dans les
    rapports exportes."""
    return f"scan-{uuid.uuid4().hex[:12]}"
