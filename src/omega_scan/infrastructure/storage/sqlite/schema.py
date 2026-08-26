# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Definition DDL des tables SQLite du projet.

Choix de conception (different d'omega-stress) : `ScanRun` n'est PAS
aplati colonne par colonne dans `scans`. C'est un objet profondement
imbrique et heterogene (target/http/tls/findings/summary/errors, chacun
avec sa propre structure de dict), contrairement au `LoadRun` plat
d'omega-stress — un flattening complet exigerait des dizaines de colonnes
ou des tables filles pour un gain de requetage jamais demande par le plan
produit (pas de recherche par header ou par finding individuel prevue).
On stocke donc un hybride : quelques colonnes indexees pour le filtrage
reellement utile (`normalized_host`, `started_at`) + un blob JSON complet
via `ScanRun.to_dict()`, source de verite unique cote lecture."""
from __future__ import annotations

SCHEMA_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS scans (
        scan_id TEXT PRIMARY KEY,
        normalized_host TEXT NOT NULL,
        started_at TEXT NOT NULL,
        scan_status TEXT NOT NULL,
        overall_rating TEXT,
        run_json TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS pinned_targets (
        normalized_host TEXT PRIMARY KEY,
        authorized INTEGER NOT NULL,
        pinned_at TEXT NOT NULL,
        note TEXT
    )
    """,
)
