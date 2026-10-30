# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran Aide : reference statique des raccourcis et fonctions de l'application."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, DataTable, Footer, Header, Static

from omega_scan.interfaces.tui.screens._base import OmegaScreen
from omega_scan.shared.i18n import _

_SHORTCUTS = (
    (_("Haut / Bas"), _("Naviguer entre les éléments d'un écran")),
    (_("Tab / Maj+Tab"), _("Naviguer entre les champs d'un formulaire")),
    (_("Échap"), _("Retour à l'écran précédent (confirmation de sortie sur l'accueil)")),
    ("t", _("Thème suivant (appliqué immédiatement, sans confirmation)")),
    ("r", _("Rafraîchir la détection du terminal")),
    ("a", _("Cette aide")),
    ("q", _("Quitter (avec confirmation)")),
)

_PROFILE_TABLE_COLUMNS = (_("Paramètre"), "quick", "standard", "extended", "local-lab")
_PROFILE_TABLE_ROWS = (
    (_("Usage"), _("Vérif. rapide"), _("Complet (défaut)"), _("Approfondi"), _("localhost / LAN")),
    (_("Timeout connect/read"), "3s / 6s", "3s / 6s", "5s / 10s", "3s / 6s"),
    (
        _("Méthodes HTTP"),
        "OPTIONS",
        "OPTIONS, TRACE",
        "OPTIONS, TRACE, PUT, DELETE, PATCH",
        "OPTIONS, TRACE",
    ),
    (_("Path probing"), _("Non"), _("Oui (~20)"), _("Oui (complet)"), _("Oui (~20)")),
    ("TLS", _("Non"), _("Oui"), _("Oui (détaillé)"), _("Oui (tolérant)")),
    (_("Catch-all"), "-", _("Oui"), _("Oui"), _("Oui")),
    (_("Politique HSTS"), _("Non évaluée"), _("Standard"), _("Strict"), _("Tolérante")),
)

_PROFILE_USAGE_NOTES = (
    ("quick", _("vérification éclair avant mise en production")),
    ("standard", _("audit complet d'un service en production, recommandé")),
    ("extended", _("audit approfondi incluant les méthodes HTTP risquées")),
    (
        "local-lab",
        (_("scan de localhost ou LAN sans pénaliser les règles pensées pour le public, HSTS "
           "notamment")),
    ),
)

_SECTIONS = (
    (
        _("Scanner"),
        (
            _("Saisir une cible (IPv4, IPv6, hostname ou URL), choisir un profil "
              "(quick/standard/extended/local-lab), confirmer l'autorisation si la cible n'est "
              "pas déjà épinglée, puis lancer le scan.")
        ),
    ),
    (
        _("Cibles"),
        (
            _("Épingler un hôte dispense de recocher la confirmation d'autorisation à chaque "
              "scan sur cette même cible.")
        ),
    ),
    (
        _("Historique"),
        (
            _("Liste tous les scans passés : détail complet, comparaison entre deux scans, ou "
              "rejouer un scan sur la même cible.")
        ),
    ),
    (
        _("Export"),
        (
            _("Depuis le détail d'un scan : JSON (source de vérité), texte (rapport compact) "
              "ou HTML (rapport lisible et partageable).")
        ),
    ),
)

_SCOPE_NOTICE = (
    _("Omega-scan observe la posture de sécurité visible d'un service HTTP/HTTPS : il ne "
      "réalise jamais de test actif (pas de SQLi, XSS, RCE, scan de CVE, fuzzing ou "
      "bruteforce).")
)


class HelpScreen(OmegaScreen):
    """Reference statique, accessible depuis n'importe quel ecran (touche `a`)."""

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("AIDE"), classes="omega-title")
            yield Static(_("Raccourcis clavier"), classes="omega-subtitle")
            for key, description in _SHORTCUTS:
                yield Static(_("{key:<14} {description}").format(key=key, description=description))
            yield Static("")
            yield Static(_("Fonctions"), classes="omega-subtitle")
            for title, description in _SECTIONS:
                yield Static(f"[b]{title}[/b]\n{description}\n")
            yield Static("")
            yield Static(_("Profils de scan"), classes="omega-subtitle")
            yield DataTable(id="profile-table")
            yield Static("")
            for name, note in _PROFILE_USAGE_NOTES:
                yield Static(f"[b]{name}[/b] : {note}")
            yield Static("")
            yield Static(_SCOPE_NOTICE, classes="omega-subtitle")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#profile-table", DataTable)
        table.add_columns(*_PROFILE_TABLE_COLUMNS)
        for row in _PROFILE_TABLE_ROWS:
            table.add_row(*row)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
