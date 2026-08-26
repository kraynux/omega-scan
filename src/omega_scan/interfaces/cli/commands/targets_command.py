# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Sous-commande CLI `targets` : gerer les cibles epinglees-autorisees.

Extension au perimetre indicatif d'ARCHITECTURE.md §2 (non listee
explicitement dans l'arborescence, qui ne mentionne que
`run_command`/`profile_command`/`history_command`/`export_command` par
analogie avec omega-stress) : necessaire pour epingler une cible en mode
non interactif/scriptable (cron, CI) sans passer par `--authorize` a
chaque scan — meme besoin reel que `pin_target`/`unpin_target`/
`list_targets`, deja construits cote application/ au Lot M3."""
from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from omega_scan.application.commands.pin_target import pin_target
from omega_scan.application.commands.unpin_target import unpin_target
from omega_scan.application.queries.list_targets import list_targets
from omega_scan.core.results import Err, Ok, Result
from omega_scan.interfaces.cli.formatters.text_formatter import (
    format_pinned_target,
    format_pinned_target_list,
    to_json,
)
from omega_scan.shared.clock import utc_now

if TYPE_CHECKING:
    # Import reserve au typage statique (voir interfaces/cli/main.py).
    from omega_scan.app.dependency_container import DependencyContainer


def _json_flag_parent() -> argparse.ArgumentParser:
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--json", action="store_true", help="Sortie machine (JSON)")
    return parent


def register(subparsers: argparse._SubParsersAction) -> None:
    """Enregistre `targets pin|unpin|list` sur le parser CLI."""
    parser = subparsers.add_parser("targets", help="Gerer les cibles epinglees-autorisees")
    actions = parser.add_subparsers(dest="targets_action", required=True)

    pin_parser = actions.add_parser(
        "pin", help="Epingler une cible comme autorisee de facon durable"
    )
    pin_parser.add_argument("host", help="Cible brute a epingler")
    pin_parser.add_argument("--note", default=None)
    pin_parser.set_defaults(handler=_handle_pin)

    unpin_parser = actions.add_parser("unpin", help="Retirer l'epinglage d'une cible")
    unpin_parser.add_argument("normalized_host")
    unpin_parser.set_defaults(handler=_handle_unpin)

    list_parser = actions.add_parser(
        "list", help="Lister les cibles epinglees", parents=[_json_flag_parent()]
    )
    list_parser.set_defaults(handler=_handle_list)


async def _handle_pin(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    outcome = pin_target(
        target_repository=container.target_repository,
        now=utc_now(),
        raw_input=args.host,
        note=args.note,
    )
    if isinstance(outcome, Err):
        return Err(str(outcome.error))
    return Ok(format_pinned_target(outcome.value))


async def _handle_unpin(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    unpin_target(target_repository=container.target_repository, normalized_host=args.normalized_host)
    return Ok(f"Cible {args.normalized_host!r} retiree des cibles epinglees.")


async def _handle_list(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    targets = list_targets(target_repository=container.target_repository)
    return Ok(to_json(targets) if args.json else format_pinned_target_list(targets))

# <-- INFO DEV ---------------------------------------------------------
# Role :
# - Traduit `omega-scan targets pin|unpin|list` en appels aux
#   commands/query deja construits au Lot M3.
# Pourquoi dans interfaces/cli/commands/ (charte) :
# - Adaptateur de presentation, aucune logique propre : l'epinglage EST la
#   confirmation d'autorisation (domain/targets/service.py::pin_target),
#   ce fichier ne fait que collecter l'entree utilisateur.
# Ce qu'il ne contient PAS :
# - Aucun garde-fou supplementaire : `unpin_target` est un no-op silencieux
#   sur une cible deja absente (voir son docstring), ce fichier ne le
#   contredit pas en verifiant l'existence avant appel.
# Comment il sera utilise (apercu) :
# - interfaces/cli/main.py::build_parser() appelle register() au demarrage.
#---------------------------------------------------------------------->
