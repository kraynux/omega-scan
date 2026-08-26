# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Sous-commande CLI `export` : ecrire un scan deja persiste dans un format concret."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from omega_scan.application.commands.export_scan_report import export_scan_report
from omega_scan.core.enums import ExportFormat
from omega_scan.core.results import Err, Ok, Result
from omega_scan.domain.theme.policies import DEFAULT_EXPORT_THEME

if TYPE_CHECKING:
    # Import reserve au typage statique (voir interfaces/cli/main.py).
    from omega_scan.app.dependency_container import DependencyContainer


def register(subparsers: argparse._SubParsersAction) -> None:
    """Enregistre `export SCAN_ID --format {json,text,html} [--output PATH]`."""
    parser = subparsers.add_parser("export", help="Exporter un scan deja persiste")
    parser.add_argument("scan_id")
    parser.add_argument("--format", choices=("html", "text", "json"), default="html")
    parser.add_argument("--theme", default=DEFAULT_EXPORT_THEME, help="Theme d'export (HTML uniquement)")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Chemin de sortie ; par defaut var/exports/<scan_id>.<format>",
    )
    parser.set_defaults(handler=_handle_export)


async def _handle_export(
    args: argparse.Namespace, container: DependencyContainer
) -> Result[str, str]:
    export_format = ExportFormat(args.format)
    output_path = args.output or (container.default_exports_dir / f"{args.scan_id}.{args.format}")

    outcome = export_scan_report(
        scan_repository=container.scan_repository,
        report_exporter=container.report_exporter,
        scan_id=args.scan_id,
        output_path=output_path,
        export_format=export_format,
        export_theme=args.theme,
    )
    if isinstance(outcome, Err):
        return Err(str(outcome.error))
    return Ok(f"Export ecrit vers {outcome.value}")

# <-- INFO DEV ---------------------------------------------------------
# Role :
# - Traduit `omega-scan export SCAN_ID --format ...` en un appel a
#   application/commands/export_scan_report.py.
# Pourquoi dans interfaces/cli/commands/ (charte) :
# - Adaptateur de presentation, aucune logique propre.
# Ce qu'il ne contient PAS :
# - Aucun import `infrastructure.config.paths` : la Dependency Rule
#   (ARCHITECTURE.md §3) interdit a `interfaces/` d'importer
#   `infrastructure/` directement. Le chemin par defaut vient de
#   `container.default_exports_dir` (un `Path` deja resolu, expose comme
#   simple donnee par app/dependency_container.py au lot suivant — pas un
#   import de module d'infrastructure), pas d'un calcul refait ici.
# Points cles :
# - `--output` explicite prime toujours sur le chemin par defaut.
# Comment il sera utilise (apercu) :
# - interfaces/cli/main.py::build_parser() appelle register() au demarrage.
#---------------------------------------------------------------------->
