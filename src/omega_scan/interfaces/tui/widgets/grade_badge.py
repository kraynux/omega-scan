# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Badge affichant la note globale d'un scan (A-F, ou N/A)."""
from __future__ import annotations

from textual.widgets import Static


class GradeBadge(Static):
    """Affiche `overall_rating` avec une classe CSS par lettre, pour une
    coloration coherente avec le theme actif (voir styles/base.tcss)."""

    def __init__(self, *, overall_rating: str, short_message: str) -> None:
        letter_class = overall_rating.lower().replace("/", "").replace(" ", "")
        super().__init__(
            f" {overall_rating} — {short_message}",
            classes=f"omega-grade-badge omega-grade-{letter_class}",
        )
