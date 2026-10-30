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


def install_language() -> None:
    """Langue de l'interface installee AVANT d'importer la TUI (plan i18n de la suite §5) :
    les textes traduits au chargement d'un module (raccourcis, titres) sont deja dans la
    bonne langue. Jamais pour la ligne de commande (R3 : elle reste en francais)."""
    import os

    from omega_lib.infrastructure.terminal.detector import SystemTerminalDetector

    from omega_scan.infrastructure.config import paths
    from omega_scan.infrastructure.storage.files.json_settings_store import JsonSettingsStore
    from omega_scan.shared.i18n import LANGUAGE

    LANGUAGE.install(
        settings_store=JsonSettingsStore(paths.settings_path(paths.resolve_var_dir())),
        environ=os.environ,
        terminal_family=SystemTerminalDetector().detect().family,
    )


def restart_for_language(code: str) -> None:  # pragma: no cover - remplace le processus
    """Meme Python, meme module : seule l'interface redemarre, dans la langue choisie."""
    import os

    from omega_scan.shared.i18n import LANGUAGE

    LANGUAGE.prepare_restart_environment(os.environ, code)
    os.execv(sys.executable, [sys.executable, "-m", "omega_scan"])


def main(argv: list[str] | None = None) -> int:
    """Demarre l'application, dispatche vers le TUI (aucun argument) ou
    le CLI (au moins un argument), ferme proprement quelle que soit
    l'issue."""
    effective_argv = sys.argv[1:] if argv is None else argv
    if not effective_argv:
        install_language()

    from omega_scan.app.bootstrap import bootstrap

    # console_logging=False pour le TUI : Textual controle l'ecran en mode
    # alternatif, une ecriture de log directe sur stderr pendant un scan
    # corromprait son rendu (defilement observe, spinner desynchronise) —
    # bug reel signale par l'utilisateur (voir app/bootstrap.py).
    app = bootstrap(console_logging=bool(effective_argv))
    pending_language: str | None = None
    try:
        if not effective_argv:
            from omega_scan.interfaces.tui.app import OmegaScanApp

            tui = OmegaScanApp(app.container)
            tui.run()
            pending_language = tui.pending_language
        else:
            from omega_scan.interfaces.cli.main import run as run_cli

            return run_cli(app.container, effective_argv)
    finally:
        app.lifecycle.shutdown()
    if pending_language is not None:
        restart_for_language(pending_language)  # apres l'arret propre de l'application
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
