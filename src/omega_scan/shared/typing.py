# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Alias de type transverses reutilises dans les signatures de commands/queries."""
from __future__ import annotations

from collections.abc import Callable

IdFactory = Callable[[], str]
"""Signature d'un generateur d'identifiant injecte dans un command de
creation (voir shared/ids.py::new_id/new_scan_id, les implementations de
production)."""
