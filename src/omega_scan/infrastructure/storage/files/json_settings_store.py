# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation fichier JSON du port SettingsStore."""
from __future__ import annotations

import json
from pathlib import Path

from omega_scan.infrastructure.exceptions import StorageError
from omega_scan.shared.i18n import _


class JsonSettingsStore:
    """Implemente ports/settings_store.py::SettingsStore sur un fichier
    JSON plat. Recharge le fichier entier a chaque acces : le volume de
    preferences reste trivial (theme, profil de rendu), pas de cache
    necessaire."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def get(self, key: str, default: str | None = None) -> str | None:
        return self._read().get(key, default)

    def set(self, key: str, value: str) -> None:
        data = self._read()
        data[key] = value
        self._write(data)

    def all(self) -> dict[str, str]:
        return self._read()

    def _read(self) -> dict[str, str]:
        if not self._path.exists():
            return {}
        try:
            with self._path.open("r", encoding="utf-8") as handle:
                data: dict[str, str] = json.load(handle)
                return data
        except (OSError, json.JSONDecodeError) as exc:
            raise StorageError(_("Échec de lecture de {path} : {exc}").format(path=self._path, exc=exc)) from exc

    def _write(self, data: dict[str, str]) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, sort_keys=True)
        except OSError as exc:
            raise StorageError(_("Échec d'écriture de {path} : {exc}").format(path=self._path, exc=exc)) from exc
