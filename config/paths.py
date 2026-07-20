# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Listes de chemins pour le path probing.
Section 14.2 de la spec : listes courtes, ciblées, non-fuzzing.
"""

# Chemins d'administration courants (~15 entrées)
ADMIN_PATHS = [
    "/admin", "/administrator", "/wp-admin", "/phpmyadmin", "/manager",
    "/console", "/dashboard", "/login", "/signin", "/auth",
    "/webadmin", "/sysadmin", "/controlpanel", "/backend", "/cms",
]

# Chemins sensibles courants (~15 entrées)
SENSITIVE_PATHS = [
    "/.env", "/config.php", "/debug", "/server-status", "/actuator",
    "/actuator/health", "/.git/config", "/.svn/entries", "/backup.sql",
    "/db.sql", "/wp-config.php", "/config.json", "/api/swagger.json",
    "/graphql", "/.well-known/security.txt",
]

# Suffixes de backup courants
BACKUP_SUFFIXES = [
    ".bak", ".old", ".orig", ".save", ".swp", "~", ".backup", ".copy",
]

def get_all_probe_paths() -> list:
    """Retourne la liste combinée des chemins de base à tester."""
    return ADMIN_PATHS + SENSITIVE_PATHS
