# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Point d'entree du package (`python -m omega_scan` et le script console
`omega-scan`).

Racine de composition finale : seul module a importer a la fois app/
(demarrage/arret) et interfaces/ (dispatch CLI/TUI). N'appartient a aucune
des 9 couches declarees, donc n'est contraint par aucun contrat de couches
import-linter — c'est pour cette raison que le cablage final vit ici plutot
que dans interfaces/cli/main.py ou interfaces/tui/app.py, qui ne doivent
jamais s'appeler l'un l'autre ni construire eux-memes le container."""
from __future__ import annotations

import sys

from omega_scan.app.bootstrap import bootstrap


def main(argv: list[str] | None = None) -> int:
    """Demarre l'application, dispatche vers le TUI (aucun argument) ou
    le CLI (au moins un argument), ferme proprement quelle que soit
    l'issue."""
    effective_argv = sys.argv[1:] if argv is None else argv
    # console_logging=False pour le TUI : Textual controle l'ecran en mode
    # alternatif, une ecriture de log directe sur stderr pendant un scan
    # corromprait son rendu (defilement observe, spinner desynchronise) —
    # bug reel signale par l'utilisateur (voir app/bootstrap.py).
    app = bootstrap(console_logging=bool(effective_argv))
    try:
        if not effective_argv:
            from omega_scan.interfaces.tui.app import OmegaScanApp

            OmegaScanApp(app.container).run()
            return 0

        from omega_scan.interfaces.cli.main import run as run_cli

        return run_cli(app.container, effective_argv)
    finally:
        app.lifecycle.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
