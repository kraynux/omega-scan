# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Command central : lancer un scan complet (ARCHITECTURE.md §4, §7)."""
from __future__ import annotations

from omega_scan.application.dto.mappers import scan_run_to_dto
from omega_scan.application.dto.scan_dto import ScanRunDTO
from omega_scan.application.pipeline.executor import NowFactory, execute
from omega_scan.application.pipeline.guards.authorization_guard import check_authorization
from omega_scan.application.pipeline.hooks.audit_hook import (
    AuditSink,
    emit_authorization_denied,
    emit_scan_started,
)
from omega_scan.core.results import Err, Ok, Result
from omega_scan.domain.profiles.exceptions import UnknownProfileError
from omega_scan.domain.profiles.policies import get_profile
from omega_scan.domain.targets.exceptions import TargetParseError, UnauthorizedTargetError
from omega_scan.domain.targets.validation import parse_target
from omega_scan.ports.connectivity_prober import ConnectivityProber
from omega_scan.ports.http_prober import HttpProber
from omega_scan.ports.methods_prober import MethodsProber
from omega_scan.ports.path_prober import PathProber
from omega_scan.ports.scan_repository import ScanRepository
from omega_scan.ports.target_repository import TargetRepository
from omega_scan.ports.tls_prober import TlsProber
from omega_scan.shared.ids import new_scan_id


def run_scan(
    *,
    target_repository: TargetRepository,
    scan_repository: ScanRepository,
    connectivity_prober: ConnectivityProber,
    http_prober: HttpProber,
    tls_prober: TlsProber,
    path_prober: PathProber,
    methods_prober: MethodsProber,
    audit_sink: AuditSink,
    now_factory: NowFactory,
    raw_target: str,
    profile_name: str,
    authorization_confirmed: bool = False,
    host_machine: str = "",
) -> Result[ScanRunDTO, TargetParseError | UnauthorizedTargetError | UnknownProfileError]:
    """Enchaine parsing de cible, garde d'autorisation, resolution de
    profil, execution du pipeline et persistance.

    Pas de `confirm_target_authorization` separe : la confirmation
    ponctuelle est un simple booleen local a ce scan (authorization_confirmed),
    exactement comme `explicit_confirmation` chez omega-stress — la rendre
    durable est le role de application/commands/pin_target.py, un chemin
    distinct et anterieur, pas une etape intermediaire de ce command."""
    try:
        target = parse_target(raw_target)
    except TargetParseError as exc:
        return Err(exc)

    authorization = check_authorization(
        target,
        target_repository=target_repository,
        explicit_confirmation=authorization_confirmed,
    )
    if isinstance(authorization, Err):
        emit_authorization_denied(target, sink=audit_sink, occurred_at=now_factory())
        return authorization

    try:
        profile = get_profile(profile_name)
    except UnknownProfileError as exc:
        return Err(exc)

    emit_scan_started(target, sink=audit_sink, occurred_at=now_factory())

    run = execute(
        target,
        profile,
        connectivity_prober=connectivity_prober,
        http_prober=http_prober,
        tls_prober=tls_prober,
        path_prober=path_prober,
        methods_prober=methods_prober,
        audit_sink=audit_sink,
        now_factory=now_factory,
        scan_id=new_scan_id(),
        host_machine=host_machine,
    )
    scan_repository.save(run)
    return Ok(scan_run_to_dto(run))
