# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran de saisie : cible, profil, confirmation d'autorisation."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Select, Static

from omega_scan.application.queries.list_profiles import list_profiles
from omega_scan.application.queries.list_recent_targets import list_recent_targets
from omega_scan.application.queries.list_targets import list_targets
from omega_scan.interfaces.tui.screens._base import OmegaScreen
from omega_scan.interfaces.tui.screens.scan_progress import ScanProgressScreen
from omega_scan.interfaces.tui.widgets.authorization_checkbox import AuthorizationCheckbox
from omega_scan.shared.i18n import _

if TYPE_CHECKING:
    from omega_scan.app.dependency_container import DependencyContainer

_NONE = "__none__"


class ScanSetupScreen(OmegaScreen):
    """Formulaire de lancement d'un scan. La case d'autorisation reste une
    simple commodite : le guard applicatif est la seule verification qui
    compte, une cible deja epinglee n'en a de toute facon pas besoin."""

    def __init__(self, *, container: DependencyContainer) -> None:
        super().__init__()
        self._container = container
        self._pinned_hosts: set[str] = set()

    def compose(self) -> ComposeResult:
        pinned = list_targets(target_repository=self._container.target_repository)
        recent = list_recent_targets(
            scan_repository=self._container.scan_repository,
            target_repository=self._container.target_repository,
        )
        self._pinned_hosts = {p.normalized_host for p in pinned}

        picker_options: list[tuple[str, str]] = [(_("(saisie libre ci-dessous)"), _NONE)]
        if pinned:
            picker_options += [(_("★ {normalized_host}").format(normalized_host=p.normalized_host), p.normalized_host) for p in pinned]
        if recent:
            picker_options += [(host, host) for host in recent]

        yield Header()
        with Vertical(classes="omega-form-panel"):
            yield Static(_("SCANNER UNE CIBLE"), classes="omega-title")
            yield Static(_("Cibles épinglées (★) et récentes"), classes="omega-subtitle")
            yield Select(picker_options, value=_NONE, id="target-picker")
            yield Static(_("Cible"), classes="omega-subtitle")
            yield Input(placeholder=_("ex. example.org, 192.168.1.10, https://intranet.lan:8443"), id="target-input")
            yield Static(_("Profil"), classes="omega-subtitle")
            yield Select(
                [(profile.profile_name, profile.profile_name) for profile in list_profiles()],
                value="standard",
                id="profile-select",
            )
            yield AuthorizationCheckbox(id="authorization-checkbox")
            yield Static(
                _("Non requis si la cible est déjà épinglée (écran Cibles)."),
                classes="omega-hint",
            )
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Lancer"), id="launch", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id != "target-picker" or event.value == _NONE:
            return
        host = str(event.value)
        target_input = self.query_one("#target-input", Input)
        target_input.value = host
        checkbox = self.query_one("#authorization-checkbox", AuthorizationCheckbox)
        if host in self._pinned_hosts:
            checkbox.value = True
            checkbox.disabled = True
        else:
            checkbox.disabled = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if event.button.id != "launch":
            return
        raw_target = self.query_one("#target-input", Input).value.strip()
        if not raw_target:
            self.app.notify(_("Saisissez une cible."), severity="warning")
            return
        profile_name = self.query_one("#profile-select", Select).value
        authorization_confirmed = self.query_one(
            "#authorization-checkbox", AuthorizationCheckbox
        ).value
        self.app.push_screen(
            ScanProgressScreen(
                container=self._container,
                raw_target=raw_target,
                profile_name=str(profile_name),
                authorization_confirmed=authorization_confirmed,
            )
        )
