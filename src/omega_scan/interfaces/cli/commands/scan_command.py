# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Sous-commande CLI `scan` : lancer un scan complet, non interactif."""
from __future__ import annotations

import argparse
import socket
from typing import TYPE_CHECKING

from omega_scan.application.commands.run_scan import run_scan
from omega_scan.core.results import Err, Ok, Result
from omega_scan.interfaces.cli.formatters.text_formatter import format_scan_detail, to_json
from omega_scan.shared.clock import utc_now

if TYPE_CHECKING:
    # Import reserve au typage statique (voir interfaces/cli/main.py pour la
    # justification complete) : jamais execute a l'import reel.
    from omega_scan.app.dependency_container import DependencyContainer


def register(subparsers: argparse._SubParsersAction) -> None:
    """Enregistre `scan TARGET [--profile ...] [--authorize] [--json]`."""
    parser = subparsers.add_parser("scan", help="Lancer un scan de posture de securite")
    parser.add_argument("target", help="Cible brute : IPv4, IPv6, hostname ou URL")
    parser.add_argument(
        "--profile",
        choices=("quick", "standard", "extended", "local-lab"),
        default="standard",
    )
    parser.add_argument(
        "--authorize",
        action="store_true",
        help="Confirme explicitement l'autorisation de scanner cette cible pour ce scan "
        "(inutile si la cible est deja epinglee, voir la sous-commande `targets`)",
    )
    parser.add_argument("--json", action="store_true", help="Sortie machine (JSON)")
    parser.set_defaults(handler=_handle_scan)


async def _handle_scan(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    outcome = run_scan(
        target_repository=container.target_repository,
        scan_repository=container.scan_repository,
        connectivity_prober=container.connectivity_prober,
        http_prober=container.http_prober,
        tls_prober=container.tls_prober,
        path_prober=container.path_prober,
        methods_prober=container.methods_prober,
        audit_sink=container.audit_sink,
        now_factory=utc_now,
        raw_target=args.target,
        profile_name=args.profile,
        authorization_confirmed=args.authorize,
        host_machine=socket.gethostname(),
    )
    if isinstance(outcome, Err):
        return Err(str(outcome.error))

    run = outcome.value
    return Ok(to_json(run) if args.json else format_scan_detail(run))

# <-- INFO DEV ---------------------------------------------------------
# Role :
# - Traduit `omega-scan scan TARGET ...` en un appel a
#   application/commands/run_scan.py.
# Pourquoi dans interfaces/cli/commands/ (charte) :
# - Adaptateur de presentation scriptable, aucune logique propre : la garde
#   d'autorisation (ARCHITECTURE.md §7) reste entierement dans
#   application/pipeline/guards/authorization_guard.py, ce fichier se
#   contente de transmettre le booleen `--authorize`.
# Ce qu'il ne contient PAS :
# - Aucun import `infrastructure/` : les ports sont lus depuis `container`
#   (assemble par app/bootstrap.py au lot suivant), jamais construits ici.
# - `now_factory=utc_now` est passe directement depuis `shared/clock.py`,
#   pas via `container` : c'est une fonction pure sans etat, pas un port a
#   injecter (meme raisonnement que shared/ids.py cote application).
# Points cles :
# - `host_machine=socket.gethostname()` : appel stdlib direct, pas une
#   violation de la Dependency Rule (celle-ci porte sur les couches du
#   projet, pas sur l'usage de la bibliotheque standard — interfaces/cli/
#   main.py lui-meme importe deja `argparse`/`sys`/`asyncio` directement).
# Comment il sera utilise (apercu) :
# - interfaces/cli/main.py::build_parser() appelle register() au demarrage.
#---------------------------------------------------------------------->
