# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Case de confirmation d'autorisation, obligatoire avant tout scan sur une
cible non deja epinglee (ARCHITECTURE.md §7).

Ne decide rien : coche non validee => le guard applicatif
(application/pipeline/guards/authorization_guard.py) refusera le scan de
toute facon. Pure ergonomie, pas un controle de securite."""
from __future__ import annotations

from typing import Any

from textual.widgets import Checkbox

_LABEL = "Je confirme etre autorise a scanner cette cible"


class AuthorizationCheckbox(Checkbox):
    """Wrapper autour de Checkbox portant le libelle d'autorisation fixe."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(_LABEL, **kwargs)
