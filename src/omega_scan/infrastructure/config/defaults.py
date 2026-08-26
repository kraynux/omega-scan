# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Parametres par defaut du scanner (valeurs techniques, pas des politiques
de securite/produit — celles-ci vivent dans domain/*/policies.py)."""
from __future__ import annotations

DEFAULT_TIMEOUT_CONNECT = 3
DEFAULT_TIMEOUT_READ = 6

DEFAULT_USER_AGENT = "Omega-scan/1.0 (Security Posture Scanner)"

DEFAULT_PATH_PROBE_DELAY_MS = 200
DEFAULT_PATH_PROBE_MAX_TARGETS = 20

DEFAULT_MAX_REDIRECTS = 5
DEFAULT_FOLLOW_REDIRECTS = True

DEFAULT_HTTP_METHODS = ["OPTIONS", "TRACE"]
