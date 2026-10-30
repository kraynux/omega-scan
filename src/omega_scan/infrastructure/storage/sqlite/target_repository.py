# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation SQLite du port TargetRepository."""
from __future__ import annotations

import sqlite3

from omega_scan.domain.targets.models import PinnedTarget
from omega_scan.infrastructure.exceptions import StorageError
from omega_scan.shared.i18n import _


class SqliteTargetRepository:
    """Implemente ports/target_repository.py::TargetRepository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def pin(self, pinned: PinnedTarget) -> None:
        try:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO pinned_targets (
                    normalized_host, authorized, pinned_at, note
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    pinned.normalized_host,
                    int(pinned.authorized),
                    pinned.pinned_at,
                    pinned.note,
                ),
            )
            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(
                _("Échec d'épinglage de la cible {normalized_host!r} : {exc}").format(normalized_host=pinned.normalized_host, exc=exc)
            ) from exc

    def unpin(self, normalized_host: str) -> None:
        try:
            self._connection.execute(
                "DELETE FROM pinned_targets WHERE normalized_host = ?", (normalized_host,)
            )
            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(
                _("Échec de désépinglage de la cible {normalized_host!r} : {exc}").format(normalized_host=normalized_host, exc=exc)
            ) from exc

    def get(self, normalized_host: str) -> PinnedTarget | None:
        try:
            row = self._connection.execute(
                "SELECT * FROM pinned_targets WHERE normalized_host = ?", (normalized_host,)
            ).fetchone()
        except sqlite3.Error as exc:
            raise StorageError(
                _("Échec de lecture de la cible épinglée {normalized_host!r} : {exc}").format(normalized_host=normalized_host, exc=exc)
            ) from exc
        return _row_to_pinned_target(row) if row is not None else None

    def list_pinned(self) -> tuple[PinnedTarget, ...]:
        try:
            rows = self._connection.execute(
                "SELECT * FROM pinned_targets ORDER BY pinned_at DESC"
            ).fetchall()
        except sqlite3.Error as exc:
            raise StorageError(_("Échec de listage des cibles épinglées : {exc}").format(exc=exc)) from exc
        return tuple(_row_to_pinned_target(row) for row in rows)

    def clear(self) -> None:
        try:
            self._connection.execute("DELETE FROM pinned_targets")
            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(_("Échec de purge des cibles épinglées : {exc}").format(exc=exc)) from exc


def _row_to_pinned_target(row: sqlite3.Row) -> PinnedTarget:
    return PinnedTarget(
        normalized_host=row["normalized_host"],
        authorized=bool(row["authorized"]),
        pinned_at=row["pinned_at"],
        note=row["note"],
    )
