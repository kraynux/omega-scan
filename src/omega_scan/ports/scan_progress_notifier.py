# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Contrat de publication de la progression d'un scan vers la presentation."""
from __future__ import annotations

from typing import Protocol


class ScanProgressNotifier(Protocol):
    """Port consomme par application/pipeline/executor.py, implemente
    cote presentation (ex. interfaces/tui/widgets/progress_panel.py) —
    seul canal autorise entre l'execution d'un scan et son affichage en
    direct. Reprend les 3 valeurs deja utilisees par l'ecran de
    progression v1 (ui/progress.py : phase, pourcentage, message de
    statut) plutot que l'IntervalSample d'omega-stress, propre a un run
    de charge echantillonne dans le temps."""

    def notify(self, phase: str, percent: int, message: str) -> None:
        """Publie un point de progression. Ne bloque jamais sur le
        rendu : l'implementation est responsable de tout decouplage
        necessaire."""
        ...
