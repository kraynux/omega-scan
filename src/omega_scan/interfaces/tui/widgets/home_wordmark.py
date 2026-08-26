# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Bandeau texte OMEGA-SCAN (3 lignes, sans cadre) affiche en haut de
screens/home.py (retours utilisateur §2). Couleur par jetons de theme
Rich/Textual (`$accent`/`$foreground`) directement dans le markup — pas
des couleurs hex figees a la construction (meme correctif que
widgets/splash_hero.py, voir sa docstring pour le detail complet : les
jetons sont reactifs au changement de theme, une couleur hex resolue une
fois ne l'est pas)."""
from __future__ import annotations

from textual.widgets import Static

_WORDMARK_LINES = (
    "┌╦═══╦┐ ┌╦═╦═╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐   ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═╗ ╦┐",
    "│║   ║│ │║ ║ ║│ ├╬══    │║  ═╦┐ ├╬═══╬┤ ═ └╩═══╦┐ │║      ├╬═══╬┤ │║ ║ ║│",
    "└╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╩   ╩┘   └╩═══╩┘ └╩═══╩┘ └╩   ╩┘ └╩ ╚═╩┘",
)
"""OMEGA-SCAN en un seul bandeau de lettres, fourni par l'utilisateur
(modifis.txt §2), caracteres non modifies."""

_MARKUP = "\n".join((
    f"[$accent]{_WORDMARK_LINES[0]}[/]",
    f"[$foreground]{_WORDMARK_LINES[1]}[/]",
    f"[$accent]{_WORDMARK_LINES[2]}[/]",
))


class HomeWordmark(Static):
    """Bandeau decoratif centre en haut de screens/home.py."""

    def __init__(self) -> None:
        super().__init__(_MARKUP, classes="omega-home-wordmark")
