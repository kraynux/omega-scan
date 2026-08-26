# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command : rejouer un scan deja connu sans resaisie (ARCHITECTURE.md §4)."""
from __future__ import annotations

from omega_scan.application.commands.run_scan import run_scan
from omega_scan.application.dto.scan_dto import ScanRunDTO
from omega_scan.application.pipeline.executor import NowFactory
from omega_scan.application.pipeline.hooks.audit_hook import AuditSink
from omega_scan.core.results import Err, Result
from omega_scan.domain.profiles.exceptions import UnknownProfileError
from omega_scan.domain.scans.exceptions import ScanNotFoundError
from omega_scan.domain.targets.exceptions import TargetParseError, UnauthorizedTargetError
from omega_scan.ports.connectivity_prober import ConnectivityProber
from omega_scan.ports.http_prober import HttpProber
from omega_scan.ports.methods_prober import MethodsProber
from omega_scan.ports.path_prober import PathProber
from omega_scan.ports.scan_repository import ScanRepository
from omega_scan.ports.target_repository import TargetRepository
from omega_scan.ports.tls_prober import TlsProber


def replay_scan(
    *,
    scan_repository: ScanRepository,
    target_repository: TargetRepository,
    connectivity_prober: ConnectivityProber,
    http_prober: HttpProber,
    tls_prober: TlsProber,
    path_prober: PathProber,
    methods_prober: MethodsProber,
    audit_sink: AuditSink,
    now_factory: NowFactory,
    scan_id: str,
    authorization_confirmed: bool = False,
) -> Result[
    ScanRunDTO, ScanNotFoundError | TargetParseError | UnauthorizedTargetError | UnknownProfileError
]:
    """Recupere la cible et le profil d'un scan passe, puis relance
    run_scan() a l'identique — ne contourne jamais la garde d'autorisation :
    une cible epinglee depuis passe toujours par elle sans friction, une
    cible non epinglee exige `authorization_confirmed=True` a nouveau."""
    previous = scan_repository.get(scan_id)
    if previous is None:
        return Err(ScanNotFoundError(f"Aucun scan trouve pour l'identifiant {scan_id!r}."))

    return run_scan(
        target_repository=target_repository,
        scan_repository=scan_repository,
        connectivity_prober=connectivity_prober,
        http_prober=http_prober,
        tls_prober=tls_prober,
        path_prober=path_prober,
        methods_prober=methods_prober,
        audit_sink=audit_sink,
        now_factory=now_factory,
        raw_target=previous.target.input_raw,
        profile_name=previous.scan_profile.get("profile_name", "standard"),
        authorization_confirmed=authorization_confirmed,
        host_machine=previous.meta.get("host_machine", ""),
    )
