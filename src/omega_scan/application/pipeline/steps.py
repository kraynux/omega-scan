# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Etapes 3-4/6 du pipeline (ARCHITECTURE.md §4) : collecte reseau puis checks.

Porte fidelement l'enchainement de l'ancien core/pipeline.py::run_scan (racine
du repot v1), moins le parsing de cible et la resolution de profil (deplaces
dans application/commands/run_scan.py, en amont du pipeline)."""
from __future__ import annotations

from typing import Any

from omega_scan.domain.checks.cookies.service import run_cookies_checks
from omega_scan.domain.checks.cors.service import run_cors_checks
from omega_scan.domain.checks.exposure.service import run_exposure_checks
from omega_scan.domain.checks.headers.service import run_headers_checks
from omega_scan.domain.checks.information_leaks.service import run_information_leaks_checks
from omega_scan.domain.checks.methods.service import run_methods_checks
from omega_scan.domain.checks.tls_depth.service import run_tls_depth_checks
from omega_scan.domain.checks.transport.service import run_transport_checks
from omega_scan.domain.findings.models import Finding
from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target
from omega_scan.ports.connectivity_prober import ConnectivityProber
from omega_scan.ports.http_prober import HttpProber
from omega_scan.ports.methods_prober import MethodsProber
from omega_scan.ports.path_prober import PathProber
from omega_scan.ports.tls_prober import TlsProber


def run_probes_and_checks(
    target: Target,
    profile: ScanProfile,
    *,
    connectivity_prober: ConnectivityProber,
    http_prober: HttpProber,
    tls_prober: TlsProber,
    path_prober: PathProber,
    methods_prober: MethodsProber,
    errors: list[ScanError],
) -> dict[str, Any]:
    """Collecte (connectivite -> http -> tls -> path -> methodes) puis juge
    (transport, headers, cache, cookies, CORS, exposition, methodes, fuites
    d'information, profondeur TLS — Lot M5 : cookies/CORS/TLS ajoutees,
    cookies etait vide et jamais appelee jusqu'ici).

    Toutes les probes partagent la meme liste `errors`, mutee par effet de
    bord (meme contrat que chaque port, voir ARCHITECTURE.md §5.3) :
    simplification assumee par rapport a la v1, qui accumulait une liste
    d'erreurs separee par phase avant de les fusionner dans le contexte —
    le resultat final (une seule liste de ScanError, dans le meme ordre
    relatif) est identique."""
    target_dict = target.to_dict()
    profile_dict = profile.to_dict()

    connectivity = connectivity_prober.probe(target, profile, errors)

    http_data = http_prober.probe(target, profile, errors)

    tls_data = tls_prober.probe(target, profile, errors)

    path_data = path_prober.probe(target, profile, http_data, errors)
    http_data["overview"]["catch_all_suspected"] = path_data["catch_all_suspected"]
    http_data["overview"]["path_probe_context"] = path_data["path_probe_context"]

    methods_data = methods_prober.probe(target, profile, http_data, errors)

    findings: list[Finding] = []
    findings.extend(run_transport_checks(http_data, target_dict, profile_dict))
    findings.extend(run_headers_checks(http_data, target_dict, profile_dict))
    findings.extend(run_cookies_checks(http_data, target_dict, profile_dict))
    findings.extend(run_cors_checks(http_data, target_dict, profile_dict))
    findings.extend(run_exposure_checks(http_data, target_dict, profile_dict))
    findings.extend(run_methods_checks(methods_data, target_dict, profile_dict, http_data))
    findings.extend(run_information_leaks_checks(http_data, target_dict, profile_dict))
    findings.extend(run_tls_depth_checks(tls_data, target_dict, profile_dict))

    return {
        "connectivity": connectivity,
        "http": http_data,
        "tls": tls_data,
        "findings": findings,
    }
