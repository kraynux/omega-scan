# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Seuils des regles transport (TRN-*)."""
from __future__ import annotations

# TRN-HSTS-002 : en-dessous de ce max-age (secondes), le HSTS est juge trop court.
HSTS_MIN_MAX_AGE_SECONDS = 31536000  # 1 an
