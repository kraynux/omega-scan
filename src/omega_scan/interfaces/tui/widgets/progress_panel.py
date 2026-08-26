# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Indicateur de progression indetermine, avec le detail des operations en
cours (retour reel : "pendant le scan on ne sait pas ce qui se passe... la
version de base affichait l'ecriture des operations") : le scan reste
atomique du point de vue du domaine (pas de flux d'evenements structures),
mais screens/scan_progress.py relaie les lignes du logger technique ici."""
from __future__ import annotations

from textual.containers import Middle
from textual.widgets import LoadingIndicator, RichLog, Static


class ProgressPanel(Middle):
    """Ecran d'attente pendant l'execution d'un scan."""

    def __init__(self, *, message: str) -> None:
        super().__init__(
            Static(message, classes="omega-subtitle"),
            LoadingIndicator(),
            RichLog(classes="omega-progress-log", max_lines=200, auto_scroll=True, markup=False),
            classes="omega-progress-panel",
        )

    def write_line(self, line: str) -> None:
        self.query_one(RichLog).write(line)
