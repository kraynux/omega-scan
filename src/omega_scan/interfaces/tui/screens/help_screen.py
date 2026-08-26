# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran Aide : reference statique des raccourcis et fonctions de l'application."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, DataTable, Footer, Header, Static

from omega_scan.interfaces.tui.screens._base import OmegaScreen

_SHORTCUTS = (
    ("Haut / Bas", "Naviguer entre les elements d'un ecran"),
    ("Tab / Maj+Tab", "Naviguer entre les champs d'un formulaire"),
    ("Echap", "Retour a l'ecran precedent (confirmation de sortie sur l'accueil)"),
    ("t", "Theme suivant (applique immediatement, sans confirmation)"),
    ("r", "Rafraichir la detection du terminal"),
    ("a", "Cette aide"),
    ("q", "Quitter (avec confirmation)"),
)

_PROFILE_TABLE_COLUMNS = ("Parametre", "quick", "standard", "extended", "local-lab")
_PROFILE_TABLE_ROWS = (
    ("Usage", "Verif. rapide", "Complet (defaut)", "Approfondi", "localhost / LAN"),
    ("Timeout connect/read", "3s / 6s", "3s / 6s", "5s / 10s", "3s / 6s"),
    (
        "Methodes HTTP",
        "OPTIONS",
        "OPTIONS, TRACE",
        "OPTIONS, TRACE, PUT, DELETE, PATCH",
        "OPTIONS, TRACE",
    ),
    ("Path probing", "Non", "Oui (~20)", "Oui (complet)", "Oui (~20)"),
    ("TLS", "Non", "Oui", "Oui (detaille)", "Oui (tolerant)"),
    ("Catch-all", "-", "Oui", "Oui", "Oui"),
    ("Politique HSTS", "Non evaluee", "Standard", "Strict", "Tolerante"),
)

_PROFILE_USAGE_NOTES = (
    ("quick", "verification eclair avant mise en production"),
    ("standard", "audit complet d'un service en production, recommande"),
    ("extended", "audit approfondi incluant les methodes HTTP risquees"),
    (
        "local-lab",
        ("scan de localhost ou LAN sans penaliser les regles pensees pour le "
         "public, HSTS notamment"),
    ),
)

_SECTIONS = (
    (
        "Scanner",
        (
            "Saisir une cible (IPv4, IPv6, hostname ou URL), choisir un profil "
            "(quick/standard/extended/local-lab), confirmer l'autorisation si la "
            "cible n'est pas deja epinglee, puis lancer le scan."
        ),
    ),
    (
        "Cibles",
        (
            "Epingler un hote dispense de recocher la confirmation d'autorisation "
            "a chaque scan sur cette meme cible."
        ),
    ),
    (
        "Historique",
        (
            "Liste tous les scans passes : detail complet, comparaison entre deux "
            "scans, ou rejouer un scan sur la meme cible."
        ),
    ),
    (
        "Export",
        (
            "Depuis le detail d'un scan : JSON (source de verite), texte "
            "(rapport compact) ou HTML (rapport lisible et partageable)."
        ),
    ),
)

_SCOPE_NOTICE = (
    "Omega-scan observe la posture de securite visible d'un service "
    "HTTP/HTTPS : il ne realise jamais de test actif (pas de SQLi, XSS, "
    "RCE, scan de CVE, fuzzing ou bruteforce)."
)


class HelpScreen(OmegaScreen):
    """Reference statique, accessible depuis n'importe quel ecran (touche `a`)."""

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static("AIDE", classes="omega-title")
            yield Static("Raccourcis clavier", classes="omega-subtitle")
            for key, description in _SHORTCUTS:
                yield Static(f"{key:<14} {description}")
            yield Static("")
            yield Static("Fonctions", classes="omega-subtitle")
            for title, description in _SECTIONS:
                yield Static(f"[b]{title}[/b]\n{description}\n")
            yield Static("")
            yield Static("Profils de scan", classes="omega-subtitle")
            yield DataTable(id="profile-table")
            yield Static("")
            for name, note in _PROFILE_USAGE_NOTES:
                yield Static(f"[b]{name}[/b] : {note}")
            yield Static("")
            yield Static(_SCOPE_NOTICE, classes="omega-subtitle")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button("Retour", id="back")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#profile-table", DataTable)
        table.add_columns(*_PROFILE_TABLE_COLUMNS)
        for row in _PROFILE_TABLE_ROWS:
            table.add_row(*row)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
