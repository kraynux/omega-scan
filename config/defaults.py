# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Paramètres par défaut du scanner.
Sections 4 et 12 de la spec.
"""

# Timeouts (en secondes)
DEFAULT_TIMEOUT_CONNECT = 3
DEFAULT_TIMEOUT_READ = 6

# User-Agent
DEFAULT_USER_AGENT = "Omega-scan/1.0 (Security Posture Scanner)"

# Throttling path probe (en millisecondes)
DEFAULT_PATH_PROBE_DELAY_MS = 200
DEFAULT_PATH_PROBE_MAX_TARGETS = 20

# Redirects
DEFAULT_MAX_REDIRECTS = 5
DEFAULT_FOLLOW_REDIRECTS = True

# Méthodes HTTP par défaut
DEFAULT_HTTP_METHODS = ["OPTIONS", "TRACE"]
