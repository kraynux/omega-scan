# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Horloge de production, utilisee a la frontiere presentation/application."""
from __future__ import annotations

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Heure courante en UTC. Implementation de production par defaut —
    domain/ et application/ ne l'appellent jamais elles-memes, elles
    recoivent toujours `now` explicitement en parametre."""
    return datetime.now(timezone.utc)
