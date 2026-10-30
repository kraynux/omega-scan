# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Point d'entree Textual de l'application, cable par le composition root
(src/omega_scan/__main__.py)."""
from __future__ import annotations

import logging
from collections.abc import Iterable
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, ClassVar, cast

from omega_lib.terminal.policies import MINIMUM_USABLE_COLUMNS, MINIMUM_USABLE_ROWS
from omega_lib.theme.policies import TUI_THEMES
from textual.app import App, SystemCommand
from textual.binding import Binding, BindingType

from omega_scan.application.commands.select_theme import select_theme
from omega_scan.application.queries.detect_terminal import detect_terminal
from omega_scan.core.enums import RenderProfile
from omega_scan.core.results import Err
from omega_scan.interfaces.tui.controllers.startup_controller import (
    StartupState,
    resolve_startup_state,
)
from omega_scan.interfaces.tui.language_setting import notify_language_at_startup
from omega_scan.interfaces.tui.rendering.stylesheet_loader import load_paths_for
from omega_scan.interfaces.tui.rendering.textual_theme_builder import build_all_textual_themes
from omega_scan.interfaces.tui.screens.help_screen import HelpScreen
from omega_scan.interfaces.tui.screens.home import HomeScreen
from omega_scan.interfaces.tui.screens.quit_confirm import QuitConfirmScreen
from omega_scan.interfaces.tui.screens.splash import SplashScreen
from omega_scan.interfaces.tui.screens.terminal_warning import TerminalWarningScreen
from omega_scan.shared.i18n import N_, _

if TYPE_CHECKING:
    from textual.screen import Screen

    from omega_scan.app.dependency_container import DependencyContainer

TITLE = _("🔍 OMEGA-SCAN")
"""Icone loupe incluse DANS la chaine de titre (pas via Header(icon=...))
: HeaderIcon/HeaderTitle sont deux widgets Textual distincts, les fondre
dans une seule chaine les fait apparaitre comme une unite au lieu d'une
icone collee a gauche et un titre centre separement (meme convention que
omega-stress)."""


class OmegaScanApp(App[None]):
    """Application TUI d'omega-scan : resout theme/profil de rendu au
    demarrage, puis enchaine splash -> (avertissement terminal) -> accueil."""

    TITLE = TITLE
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("q", "quit", _("Quitter"), show=True),
        Binding("ctrl+q", "quit", _("Quitter"), show=False),
        Binding("t", "cycle_theme", _("Thème suivant"), show=True),
        Binding("r", "refresh_terminal", _("Rafraîchir"), show=True),
        Binding("a", "help", _("Aide"), show=True),
    ]

    def __init__(self, container: DependencyContainer) -> None:
        self._container = container
        self._startup_state = resolve_startup_state(
            terminal_detector=container.terminal_detector,
            settings_store=container.settings_store,
        )
        css_path = cast(
            "list[str | PurePath]", load_paths_for(self._startup_state.theme.render_profile)
        )
        self.pending_language: str | None = None
        """Langue choisie dans les Reglages : __main__.py relance l'interface apres la fermeture."""
        super().__init__(css_path=css_path)
        for theme in build_all_textual_themes():
            self.register_theme(theme)
        self.theme = self._startup_state.theme.theme_name

    def on_mount(self) -> None:
        notify_language_at_startup(self)
        self.push_screen(SplashScreen(), self._after_splash)

    def _after_splash(self, _result: None) -> None:
        terminal = self._startup_state.terminal
        too_small = terminal.columns < MINIMUM_USABLE_COLUMNS or terminal.rows < MINIMUM_USABLE_ROWS
        if terminal.render_profile == RenderProfile.MONO.value or too_small:
            message = (
                _("Terminal détecté : {family} ({columns}x{rows}). Rendu appliqué : "
                  "{render_profile}.").format(family=terminal.family, columns=terminal.columns, rows=terminal.rows, render_profile=terminal.render_profile)
            )
            self.push_screen(TerminalWarningScreen(message=message), self._show_home)
        else:
            self._show_home(None)

    def _show_home(self, _result: None) -> None:
        self.push_screen(HomeScreen(container=self._container))

    def watch_theme(self, _theme_name: str) -> None:
        terminal = self._startup_state.terminal
        self.sub_title = _("{theme} | {columns}x{rows}").format(theme=self.theme, columns=terminal.columns, rows=terminal.rows)

    async def action_quit(self) -> None:
        """Surcharge : demande confirmation avant de fermer."""
        self.push_screen(QuitConfirmScreen(), self._quit_if_confirmed)

    def _quit_if_confirmed(self, confirmed: bool | None) -> None:
        if confirmed:
            self.exit()

    def action_cycle_theme(self) -> None:
        """Touche `t` : bascule vers le theme SUIVANT du catalogue, sans
        confirmation (application immediate, meme commande que l'ecran
        Reglages)."""
        names = list(TUI_THEMES.keys())
        current_index = names.index(self.theme) if self.theme in names else 0
        next_name = names[(current_index + 1) % len(names)]
        try:
            result = select_theme(settings_store=self._container.settings_store, theme_name=next_name)
        except OSError as exc:
            # Retour utilisateur (GROS BUG omega-fire : "t" fermait
            # l'application) - meme correctif applique ici par coherence
            # (audit de la suite) : select_theme() ne rattrape que les
            # noms de theme invalides via Result/Err (validation), jamais
            # une erreur de persistance disque (permissions, disque
            # plein, systeme de fichiers en lecture seule) - celle-ci
            # remontait donc brute et faisait planter cette action sans
            # aucun rattrapage. Le theme change quand meme visuellement
            # (self.theme = next_name plus bas) : seule la PERSISTANCE
            # du choix echoue, pas la fonctionnalite immediate.
            self.notify(_("Thème appliqué mais non enregistré : {exc}").format(exc=exc), severity="warning")
            self.theme = next_name
            return
        if isinstance(result, Err):
            self.notify(str(result.error), severity="error")
            return
        self.theme = next_name

    def action_refresh_terminal(self) -> None:
        """Touche `r` : redetecte taille/famille du terminal et met a jour
        le sous-titre du Header — celui-ci ne se rafraichit sinon que sur
        un changement de theme (watch_theme), jamais sur un redimensionnement
        reel (Textual ne redeclenche pas ce watcher tout seul)."""
        terminal = detect_terminal(terminal_detector=self._container.terminal_detector)
        self._startup_state = StartupState(terminal=terminal, theme=self._startup_state.theme)
        self.sub_title = _("{theme} | {columns}x{rows}").format(theme=self.theme, columns=terminal.columns, rows=terminal.rows)
        self.notify(_("{family} ({columns}x{rows})").format(family=terminal.family, columns=terminal.columns, rows=terminal.rows), title=_("Terminal rafraîchi"))

    def action_help(self) -> None:
        self.push_screen(HelpScreen())

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        """Remplace la liste par defaut de Textual plutot que d'appeler
        `super()` : celle-ci inclut "Maximiser"/"Minimiser" un widget, une
        action generique de Textual jamais concue pour cette application
        (aucun widget ici ne beneficie d'un agrandissement plein ecran isole)
        et source de plantages reels signales par l'utilisateur."""
        yield SystemCommand(_("Thème"), _("Changer le thème actif"), self.action_change_theme)
        yield SystemCommand(
            _("Quitter"), _("Quitter l'application (avec confirmation)"), self.action_quit
        )
        yield SystemCommand(
            _("Capture d'écran"),
            _("Enregistrer une capture SVG de l'écran courant"),
            self._deliver_screenshot_to_configured_dir,
        )

    def _deliver_screenshot_to_configured_dir(self) -> None:
        """Livre la capture dans le dossier configure (Reglages ->
        Captures d'ecran), a defaut container.default_screenshots_dir —
        sans `path=` explicite, App.deliver_screenshot() ecrirait dans le
        dossier Telechargements de l'utilisateur, jamais var/."""
        configured = self._container.settings_store.get(
            "screenshots_dir_override", str(self._container.default_screenshots_dir)
        )
        directory = Path(configured or self._container.default_screenshots_dir)
        directory.mkdir(parents=True, exist_ok=True)
        self.deliver_screenshot(path=str(directory))

    def _handle_exception(self, error: Exception) -> None:
        """Filet de securite unique cote TUI (ARCHITECTURE.md §5.4) :
        toute exception technique non prevue est journalisee puis affichee
        comme notification, sans jamais fermer l'application."""
        logging.getLogger("omega_scan").error(N_("Exception non prévue"), exc_info=error)
        self.notify(
            str(error) or type(error).__name__,
            title=_("Erreur inattendue"),
            severity="error",
            timeout=10,
        )
