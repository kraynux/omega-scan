# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Etape 5/6 du pipeline (ARCHITECTURE.md §4) : execution de bout en bout,
assemblage du ScanRun final."""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

from omega_scan.application.pipeline.hooks.audit_hook import AuditSink, emit_scan_finished
from omega_scan.application.pipeline.steps import run_probes_and_checks
from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.reports.service import calculate_summary
from omega_scan.domain.scans.models import ScanError, ScanRun
from omega_scan.domain.scans.service import compute_duration_ms, compute_scan_status
from omega_scan.domain.targets.models import Target
from omega_scan.ports.connectivity_prober import ConnectivityProber
from omega_scan.ports.http_prober import HttpProber
from omega_scan.ports.methods_prober import MethodsProber
from omega_scan.ports.path_prober import PathProber
from omega_scan.ports.tls_prober import TlsProber

NowFactory = Callable[[], datetime]
"""Horloge injectee, appelee deux fois par execute() (debut/fin) pour un
`duration_ms` reellement mesure — a la difference d'un `now: datetime`
unique fourni par l'appelant, qui figerait started_at et finished_at a la
meme valeur (voir INFO DEV en fin de fichier)."""


def execute(
    target: Target,
    profile: ScanProfile,
    *,
    connectivity_prober: ConnectivityProber,
    http_prober: HttpProber,
    tls_prober: TlsProber,
    path_prober: PathProber,
    methods_prober: MethodsProber,
    audit_sink: AuditSink,
    now_factory: NowFactory,
    scan_id: str,
    host_machine: str = "",
) -> ScanRun:
    """Execute la collecte et les checks, assemble et retourne le ScanRun
    final. N'appelle jamais la persistance (application/commands/run_scan.py
    reste responsable de scan_repository.save())."""
    started_at = now_factory()

    errors: list[ScanError] = []
    result: dict[str, Any] = run_probes_and_checks(
        target,
        profile,
        connectivity_prober=connectivity_prober,
        http_prober=http_prober,
        tls_prober=tls_prober,
        path_prober=path_prober,
        methods_prober=methods_prober,
        errors=errors,
    )

    finished_at = now_factory()
    scan_status = compute_scan_status(errors)
    summary = calculate_summary(result["findings"], scan_status, result["connectivity"])

    started_at_iso = started_at.isoformat().replace("+00:00", "Z")
    finished_at_iso = finished_at.isoformat().replace("+00:00", "Z")

    run = ScanRun(
        meta={
            "scan_id": scan_id,
            "scanner_name": "Omega-Scan",
            "scanner_version": "2.0.0",
            "started_at": started_at_iso,
            "finished_at": finished_at_iso,
            "duration_ms": compute_duration_ms(started_at_iso, finished_at_iso),
            "host_machine": host_machine,
            "operator_mode": "interactif",
            "export_targets": ["json"],
        },
        target=target,
        scan_profile=profile.to_dict(),
        connectivity=result["connectivity"],
        http=result["http"],
        tls=result["tls"],
        findings=result["findings"],
        summary=summary,
        errors=[e.to_dict() for e in errors],
    )

    emit_scan_finished(run, sink=audit_sink, occurred_at=finished_at)
    return run

# <-- INFO DEV ---------------------------------------------------------
# now_factory vs now : omega-stress injecte un `now: datetime` unique,
# reutilise tel quel pour started_at ET pour la cloture (abort/finish) de
# son pipeline.py::execute() — acceptable chez omega-stress car le detail
# temporel qui compte reellement pour un test de charge est l'INTERVALLE
# d'echantillonnage (IntervalSample.at_second, mesure differemment). Pour
# omega-scan, `duration_ms` est un champ affiche tel quel dans le resume
# (Summary/rapport), donc reellement mesure : figer started_at et
# finished_at a la meme valeur y produirait toujours 0ms. now_factory
# reste une fonction injectee (jamais un appel direct a datetime.now()
# dans ce fichier) : la discipline "horloge injectee" de domain/ est donc
# respectee, seule la forme de l'injection differe.
#---------------------------------------------------------------------->
