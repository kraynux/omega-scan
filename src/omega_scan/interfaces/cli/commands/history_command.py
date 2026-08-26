# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Sous-commande CLI `history` : lister, consulter, comparer, rejouer un scan."""
from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from omega_scan.application.commands.replay_scan import replay_scan
from omega_scan.application.queries.compare_scans import compare_scans
from omega_scan.application.queries.get_scan_details import get_scan_details
from omega_scan.application.queries.list_scan_history import list_scan_history
from omega_scan.core.results import Err, Ok, Result
from omega_scan.interfaces.cli.formatters.text_formatter import (
    format_comparison,
    format_scan_detail,
    format_scan_list,
    to_json,
)
from omega_scan.shared.clock import utc_now

if TYPE_CHECKING:
    # Import reserve au typage statique (voir interfaces/cli/main.py).
    from omega_scan.app.dependency_container import DependencyContainer


def _json_flag_parent() -> argparse.ArgumentParser:
    """Fragment `--json` partage entre les 4 actions (duplique
    volontairement plutot que factorise dans un fichier a part pour
    quatre lignes, meme choix qu'omega-stress)."""
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--json", action="store_true", help="Sortie machine (JSON)")
    return parent


def register(subparsers: argparse._SubParsersAction) -> None:
    """Enregistre `history list|show|compare|replay` sur le parser CLI."""
    parser = subparsers.add_parser("history", help="Consulter l'historique des scans")
    actions = parser.add_subparsers(dest="history_action", required=True)

    list_parser = actions.add_parser(
        "list", help="Lister l'historique, filtrable par cible", parents=[_json_flag_parent()]
    )
    list_parser.add_argument("--host", default=None, help="Filtre sur normalized_host")
    list_parser.add_argument("--limit", type=int, default=50)
    list_parser.set_defaults(handler=_handle_list)

    show_parser = actions.add_parser(
        "show", help="Afficher le detail complet d'un scan", parents=[_json_flag_parent()]
    )
    show_parser.add_argument("scan_id")
    show_parser.set_defaults(handler=_handle_show)

    compare_parser = actions.add_parser(
        "compare", help="Comparer deux scans d'une meme cible", parents=[_json_flag_parent()]
    )
    compare_parser.add_argument("previous_scan_id")
    compare_parser.add_argument("current_scan_id")
    compare_parser.set_defaults(handler=_handle_compare)

    replay_parser = actions.add_parser(
        "replay", help="Rejouer un scan deja connu, sans resaisie", parents=[_json_flag_parent()]
    )
    replay_parser.add_argument("scan_id")
    replay_parser.add_argument(
        "--authorize",
        action="store_true",
        help="Confirme l'autorisation si la cible n'est plus/pas epinglee",
    )
    replay_parser.set_defaults(handler=_handle_replay)


async def _handle_list(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    scans = list_scan_history(
        scan_repository=container.scan_repository,
        normalized_host=args.host,
        limit=args.limit,
    )
    return Ok(to_json(scans) if args.json else format_scan_list(scans))


async def _handle_show(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    run = get_scan_details(scan_repository=container.scan_repository, scan_id=args.scan_id)
    if run is None:
        return Err(f"Scan {args.scan_id!r} introuvable.")
    return Ok(to_json(run) if args.json else format_scan_detail(run))


async def _handle_compare(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    outcome = compare_scans(
        scan_repository=container.scan_repository,
        previous_scan_id=args.previous_scan_id,
        current_scan_id=args.current_scan_id,
    )
    if isinstance(outcome, Err):
        return Err(str(outcome.error))
    return Ok(to_json(outcome.value) if args.json else format_comparison(outcome.value))


async def _handle_replay(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    outcome = replay_scan(
        scan_repository=container.scan_repository,
        target_repository=container.target_repository,
        connectivity_prober=container.connectivity_prober,
        http_prober=container.http_prober,
        tls_prober=container.tls_prober,
        path_prober=container.path_prober,
        methods_prober=container.methods_prober,
        audit_sink=container.audit_sink,
        now_factory=utc_now,
        scan_id=args.scan_id,
        authorization_confirmed=args.authorize,
    )
    if isinstance(outcome, Err):
        return Err(str(outcome.error))
    run = outcome.value
    return Ok(to_json(run) if args.json else format_scan_detail(run))

# <-- INFO DEV ---------------------------------------------------------
# Role :
# - Traduit `omega-scan history list|show|compare|replay` en appels aux
#   queries/command deja construits au Lot M3.
# Pourquoi dans interfaces/cli/commands/ (charte) :
# - Adaptateur de presentation scriptable, aucune logique propre.
# Ce qu'il ne contient PAS :
# - Aucun filtre supplementaire (date, statut) : meme limitation deja
#   documentee cote ports/scan_repository.py et
#   application/queries/list_scan_history.py.
# Points cles :
# - `show`/`compare` retournent un Err (jamais une exception) pour un id
#   inconnu : ScanNotFoundError est deja un DomainError structure, ce
#   fichier se contente de le convertir en message CLI.
# - `replay` ne contourne jamais la garde d'autorisation : une cible
#   epinglee depuis passe sans friction, une cible qui ne l'est plus exige
#   `--authorize` a nouveau (voir application/commands/replay_scan.py).
# Comment il sera utilise (apercu) :
# - interfaces/cli/main.py::build_parser() appelle register() au demarrage.
#---------------------------------------------------------------------->
