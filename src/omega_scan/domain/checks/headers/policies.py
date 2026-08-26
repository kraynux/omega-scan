# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Motifs et listes des regles headers (HDR-*)."""
from __future__ import annotations

# HDR-CSP-002 : directives CSP jugees trop permissives.
CSP_PERMISSIVE_PATTERNS = [
    "default-src *",
    "script-src 'unsafe-inline'",
    "script-src 'unsafe-eval'",
]

# HDR-CACHE-001 : directives Cache-Control considerees comme restreignant
# explicitement la mise en cache. Presence d'au moins une d'entre elles ->
# pas de finding.
CACHE_CONTROL_SAFE_DIRECTIVES = ["no-store", "private"]
