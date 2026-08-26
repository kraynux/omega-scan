# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Listes de chemins pour le path probing et le jugement d'exposition (EXR-*).

RECONCILIATION PROBE_*/JUDGED_* (Lot M5) : la v1 sondait 15+15 chemins
(PROBE_*) mais n'en jugeait que 5+5 (JUDGED_*), une incoherence heritee et
documentee au Lot M1 (des chemins comme /console, /dashboard ou /backup.sql
repondaient 200 sans jamais produire de finding). Decision produit assumee
pour ce lot : JUDGED_* couvre desormais integralement PROBE_*, a UNE
exception explicite — "/.well-known/security.txt" est retire de
JUDGED_SENSITIVE_PATHS. Ce chemin est une convention intentionnellement
publique (RFC 9116) : le juger comme "fichier sensible expose" (EXR-SENSITIVE-001,
FAIL) contredirait directement INF-SECURITYTXT-001 (Lot M5), qui traite sa
presence comme un signal positif. Un seul chemin ne peut pas etre a la fois
une fuite et une bonne pratique."""
from __future__ import annotations

# Chemins effectivement sondes par le path prober (~15 + ~15 entrees, non-fuzzing).
PROBE_ADMIN_PATHS = [
    "/admin", "/administrator", "/wp-admin", "/phpmyadmin", "/manager",
    "/console", "/dashboard", "/login", "/signin", "/auth",
    "/webadmin", "/sysadmin", "/controlpanel", "/backend", "/cms",
]

PROBE_SENSITIVE_PATHS = [
    "/.env", "/config.php", "/debug", "/server-status", "/actuator",
    "/actuator/health", "/.git/config", "/.svn/entries", "/backup.sql",
    "/db.sql", "/wp-config.php", "/config.json", "/api/swagger.json",
    "/graphql", "/.well-known/security.txt",
]

PROBE_BACKUP_SUFFIXES = [".bak", ".old", ".orig", ".save", ".swp", "~", ".backup", ".copy"]


def get_all_probe_paths() -> list:
    """Liste combinee des chemins de base a sonder."""
    return PROBE_ADMIN_PATHS + PROBE_SENSITIVE_PATHS


# Sous-ensemble juge par run_exposure_checks() — desormais identique a
# PROBE_ADMIN_PATHS (aucune exception necessaire cote chemins admin).
JUDGED_ADMIN_PATHS = list(PROBE_ADMIN_PATHS)

# Identique a PROBE_SENSITIVE_PATHS, moins security.txt (voir docstring ci-dessus,
# juge separement et positivement par INF-SECURITYTXT-001).
JUDGED_SENSITIVE_PATHS = [
    p for p in PROBE_SENSITIVE_PATHS if p != "/.well-known/security.txt"
]
