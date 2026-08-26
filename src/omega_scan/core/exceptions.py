# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Racine absolue des exceptions du projet (ARCHITECTURE.md §5.2)."""
from __future__ import annotations


class OmegaScanError(Exception):
    """Racine absolue : un `except OmegaScanError` generique attrape toute
    erreur du projet, quelle que soit sa couche d'origine."""


class ConfigurationError(OmegaScanError):
    """Configuration invalide ou incomplete (chemins, variables d'environnement)."""
