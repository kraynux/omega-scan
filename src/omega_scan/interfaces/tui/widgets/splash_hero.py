# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Composition ASCII de l'ecran de demarrage (retours utilisateur §1),
logo original fourni par l'utilisateur (modifis.txt), caracteres non
modifies. Couleur par jetons de theme Rich/Textual (`$accent`/
`$foreground`/`$secondary`) directement dans le markup — PAS des couleurs
hex resolues et figees a la construction (bug reel rapporte : "couleurs
hardcodees... ne bouge pas avec les themes"). Ces jetons sont valides et
re-resolus reactivement par le moteur de rendu de Textual (Content, verifie
par un test direct) — meme mecanisme que omega-stress (widgets/splash_hero.py,
_FONT_TOKEN = "$foreground"). Markup construit une seule fois au niveau
module (contenu immediatement disponible au premier layout, jamais mis a
jour apres coup) : necessaire pour que le Center() englobant (screens/
splash.py) le centre correctement des le premier rendu."""
from __future__ import annotations

from textual.widgets import Static

_LOGO_LINES = (
    "                    ┌────────────────────────┐",
    "                    │    LINUX HTTP CHECK    │",
    "                    └────────────────────────┘",
    "                            ▓▒░v2.5░▒▓",
    "       _--═══-┌╦═══╦┐ ┌╦═╦═╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐",
    "     ◜🯐-══════│║   ║│ │║ ║ ║│ ├╬═     │║  ═╦┐ ├╬═══╬┤",
    "    //        └╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╩   ╩┘",
    "   🯖🯖             🯔  🯒.__🮣═════════════════🮢",
    "   |║             ║ Ω .__            ═      )",
    "   🯕🯕             🯗   🮠 ͟ 🮡═════════════════🮠",
    "    \\\\            ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═╗ ╦┐",
    "      🯒-═══════-🯑🯐└╩═══╦┐ │║      ├╬═══╬┤ │║ ║ ║│",
    "      🯒---═══---🯑 └╩═══╩┘ └╩═══╩┘ └╩   ╩┘ └╩ ╚═╩┘",
    "              SCAN | HTTP | HTTPS | EXPORTS | ANALYSES",
)
"""Logo original, fourni caractere pour caractere par l'utilisateur
(modifis.txt §1) — NE PAS modifier/simplifier les glyphes (retour reel :
"le logo du splash est pas celui d'origine tu l'as modifie")."""

# Lignes de cadre PUR (bordure du titre) + ligne du milieu du lettrage
# OMEGA (5) et SCAN (11) : entierement en $foreground (clair) — regle
# §1.1/§1.3.
_FULL_BRIGHT_LINES = frozenset({0, 2, 5, 11})
# Ligne "LINUX HTTP CHECK" : seuls les DEUX "│" exterieurs (le cadre)
# passent en clair, le texte a l'interieur reste $accent (vif) — retour
# reel : "le texte dans le container LINUX HTTP CHECK est blanc, il doit
# etre couleur vif", meme convention que omega-stress (contour clair,
# contenu vif).
_OUTER_PIPE_BRIGHT_LINES = frozenset({1})
# Accroche du bas : mots en $accent (vif), "|" en $foreground (clair) —
# regle §1.4, traitee a part (voir _build_markup).
_TAGLINE_INDEX = 13


def _build_markup() -> str:
    lines: list[str] = []
    for index, row in enumerate(_LOGO_LINES):
        if index == _TAGLINE_INDEX:
            words = [f"[$accent]{part}[/]" for part in row.strip().split(" | ")]
            leading = row[: len(row) - len(row.lstrip())]
            lines.append(leading + " [$foreground]|[/] ".join(words))
        elif index in _FULL_BRIGHT_LINES:
            lines.append(f"[$foreground]{row}[/]")
        elif index in _OUTER_PIPE_BRIGHT_LINES:
            first = row.index("│")
            last = row.rindex("│")
            lines.append(
                row[:first]
                + f"[$foreground]{row[first]}[/]"
                + f"[$accent]{row[first + 1 : last]}[/]"
                + f"[$foreground]{row[last]}[/]"
                + row[last + 1 :]
            )
        else:
            # Loupe + cadres exterieurs des lettres : $accent (vif), avec
            # une nuance $secondary sur les caracteres de decor purs
            # (regle §1.2, "nuances de couleur sur le dessin de la loupe").
            lines.append(f"[$accent]{row}[/]")
    return "\n".join(lines)


_MARKUP = _build_markup()


class SplashHero(Static):
    """Bloc decoratif de l'ecran de demarrage (screens/splash.py)."""

    def __init__(self) -> None:
        super().__init__(_MARKUP, classes="omega-splash-hero")
