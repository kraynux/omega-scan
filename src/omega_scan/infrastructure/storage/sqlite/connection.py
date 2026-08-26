# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ouverture d'une connexion SQLite configuree pour le projet."""
from __future__ import annotations

import sqlite3
from pathlib import Path


def open_connection(path: Path) -> sqlite3.Connection:
    """Ouvre (et cree si besoin) la base SQLite au chemin donne.

    `check_same_thread=False` : le TUI execute chaque scan dans un worker
    Textual (thread separe du thread principal, voir
    interfaces/tui/screens/scan_progress.py::asyncio.to_thread) tout en
    partageant la meme connexion, ouverte une seule fois au demarrage par
    app/dependency_container.py. Aucun acces concurrent reel n'a lieu
    (l'UI n'interroge pas la base pendant qu'un scan tourne), donc pas de
    verrou explicite necessaire ici — seule la restriction par defaut de
    sqlite3 (une connexion = un thread) est levee."""
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection
