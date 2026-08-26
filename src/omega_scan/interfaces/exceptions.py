# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Hierarchie d'exceptions de presentation, partagee par tui/ et cli/ (ARCHITECTURE.md §5.2)."""
from __future__ import annotations

from omega_scan.core.exceptions import OmegaScanError


class InterfaceError(OmegaScanError):
    """Racine des echecs propres a la couche de presentation (TUI et CLI),
    distincte des DomainError/ApplicationError qu'elle affiche."""


class UserInputError(InterfaceError):
    """Saisie utilisateur invalide avant meme d'atteindre un command/query
    (ex. argument CLI mal forme, valeur hors du vocabulaire attendu)."""


class RenderError(InterfaceError):
    """Echec de mise en forme d'un resultat deja obtenu (rare : les DTO
    sont deja des formes simples, ce type couvre surtout un gabarit ou un
    widget qui echoue a s'afficher)."""
