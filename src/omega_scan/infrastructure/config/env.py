# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Reserve pour la lecture de variables d'environnement propres a omega-scan.

Vide pour l'instant : la seule variable d'environnement du projet
(`OMEGA_SCAN_VAR_DIR`) est deja lue directement par
infrastructure/config/paths.py::resolve_var_dir(), qui est son unique
consommateur. Ce module existe pour coherence de gabarit avec omega-stress
et accueillera une lecture reelle si un second besoin apparait."""
from __future__ import annotations
