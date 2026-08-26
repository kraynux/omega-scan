# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Dispatch CLI scriptable — mode non interactif (cron, CI).

Ne demarre PAS l'application lui-meme (voir run()).
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from typing import TYPE_CHECKING

from omega_scan.core.constants import APP_NAME
from omega_scan.core.results import Err
from omega_scan.interfaces.cli.commands import (
    export_command,
    history_command,
    scan_command,
    targets_command,
)
from omega_scan.interfaces.cli.formatters.text_formatter import format_error

if TYPE_CHECKING:
    # Import reserve au typage statique : jamais execute a l'import reel de
    # ce module, pour ne pas tirer transitivement infrastructure/
    # (sqlite3/httpx/jinja2) dans interfaces/, ce qu'import-linter interdit
    # explicitement (meme raisonnement qu'omega-stress).
    from omega_scan.app.dependency_container import DependencyContainer


def build_parser() -> argparse.ArgumentParser:
    """Construit le parser racine et y enregistre les quatre sous-commandes
    (scan/history/export/targets)."""
    parser = argparse.ArgumentParser(
        prog=APP_NAME, description="Scanner de posture de securite web (mode scriptable)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_command.register(subparsers)
    history_command.register(subparsers)
    export_command.register(subparsers)
    targets_command.register(subparsers)

    return parser


def run(container: DependencyContainer, argv: list[str] | None = None) -> int:
    """Parse argv et dispatche vers le handler de la sous-commande, avec un
    container DEJA construit (recu en parametre, jamais bati ici — voir
    src/omega_scan/__main__.py, la veritable racine de composition, a
    construire au lot suivant une fois le TUI egalement pret)."""
    args = build_parser().parse_args(argv)

    try:
        result = asyncio.run(args.handler(args, container))
    except Exception as exc:  # noqa: BLE001 — filet de securite deliberement generique (ARCHITECTURE.md §5.4)
        print(format_error(f"erreur inattendue : {exc}"), file=sys.stderr)
        return 1

    if isinstance(result, Err):
        print(format_error(result.error), file=sys.stderr)
        return 1

    print(result.value)
    return 0

# <-- INFO DEV ---------------------------------------------------------
# Role :
# - Construit le parser CLI et dispatche vers le handler choisi par
#   argparse (via `set_defaults(handler=...)` dans chaque module de
#   commands/), affiche le resultat — ne demarre ni n'arrete l'application.
# Pourquoi dans interfaces/cli/ (charte) :
# - Seul point d'arret ("filet de securite") cote CLI pour une exception
#   technique non prevue (ARCHITECTURE.md §5.4).
# Ce qu'il ne contient PAS :
# - Aucun appel a app/bootstrap.py (pas encore construit a ce stade de la
#   migration — voir docstring de run()) : le demarrage/arret de
#   l'application est du ressort exclusif de src/omega_scan/__main__.py,
#   la vraie racine de composition, au lot suivant (meme choix qu'omega-
#   stress, voir son propre INFO DEV pour la violation d'import-linter
#   evitee par cette separation).
# - Aucun import runtime de DependencyContainer : le type n'est importe
#   que sous TYPE_CHECKING.
# - Aucun import `textual`.
# Points cles :
# - Changement de syntaxe assume par rapport au CLI v1 (voir commit) :
#   `omega-scan --target X --profile Y` (flags a plat) devient
#   `omega-scan scan X --profile Y` (sous-commandes), alignement sur le
#   patron de toute la suite `omega-` (omega-stress).
# - `--plain`/`--no-color`/`--no-emoji`/`--no-live` de la v1 disparaissent
#   sans equivalent : ces flags degradaient le rendu Rich interactif, qui
#   n'existe plus cote CLI (toujours texte simple, ou --json) — l'ancien
#   role d'adaptation au terminal devient une preoccupation exclusive du
#   TUI Textual (domain/terminal/, infrastructure/terminal/, deja
#   construits, lot TUI a venir).
# Comment il sera utilise (apercu) :
# - src/omega_scan/__main__.py (a construire) appelle bootstrap() puis
#   run(container, argv), et ferme le cycle de vie dans un `finally`.
#---------------------------------------------------------------------->
