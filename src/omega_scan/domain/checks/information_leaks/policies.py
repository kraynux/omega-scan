# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Motifs de detection pour les fuites d'information (INF-*)."""
from __future__ import annotations

ERROR_PATTERNS = [
    "exception",
    "stack trace",
    "error on line",
    "fatal error",
    "uncaught exception",
    "traceback (most recent call last)",
    "at java.",
    "at org.",
    "in /var/www/",
    "in /home/",
]

STACK_PATTERNS = [
    "traceback (most recent call last)",
    "at java.",
    "at org.",
    "stack trace",
    "exception in thread",
]

VERBOSE_HEADERS = [
    "x-aspnet-version",
    "x-aspnetmvc-version",
    "x-powered-by",
    "x-debug",
    "x-server",
    "x-backend-server",
]
