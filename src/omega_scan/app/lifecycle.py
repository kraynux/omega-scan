# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Cycle de vie de l'application : fermeture propre des ressources partagees."""
from __future__ import annotations

from dataclasses import dataclass

from omega_scan.app.dependency_container import DependencyContainer


@dataclass(frozen=True, slots=True)
class AppLifecycle:
    """Enveloppe le DependencyContainer avec les operations de cycle de
    vie qui lui sont propres (fermeture)."""

    container: DependencyContainer

    def shutdown(self) -> None:
        """Ferme la connexion SQLite partagee. A appeler une seule fois,
        a la sortie normale du processus."""
        self.container.connection.close()
