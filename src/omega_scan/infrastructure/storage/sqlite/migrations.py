# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Application du schema SQLite sur une connexion ouverte."""
from __future__ import annotations

import sqlite3

from omega_scan.infrastructure.exceptions import StorageError
from omega_scan.infrastructure.storage.sqlite.schema import SCHEMA_STATEMENTS


def apply_schema(connection: sqlite3.Connection) -> None:
    """Cree les tables manquantes. Idempotent : peut etre appele a chaque
    demarrage sans effet sur une base deja a jour. Pas de mecanisme de
    colonnes additives (contrairement a omega-stress) : aucune evolution
    de schema anterieure a gerer, ce projet n'a encore rien publie."""
    try:
        for statement in SCHEMA_STATEMENTS:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as exc:
        raise StorageError(f"Echec de l'initialisation du schema SQLite : {exc}") from exc
