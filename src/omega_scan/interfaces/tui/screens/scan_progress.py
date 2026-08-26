# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ecran de progression : lance run_scan()/replay_scan() dans un worker, sans
bloquer l'UI. Un seul ecran pour les deux flux (nouveau scan ou relecture
d'un scan connu) plutot que d'en dupliquer un second identique."""
from __future__ import annotations

import asyncio
import logging
import socket
from collections.abc import Callable
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.screen import Screen

from omega_scan.application.commands.replay_scan import replay_scan
from omega_scan.application.commands.run_scan import run_scan
from omega_scan.application.dto.scan_dto import ScanRunDTO
from omega_scan.core.results import Err, Result
from omega_scan.domain.errors import DomainError
from omega_scan.interfaces.tui.screens.findings import FindingsScreen
from omega_scan.interfaces.tui.widgets.progress_panel import ProgressPanel
from omega_scan.shared.clock import utc_now

if TYPE_CHECKING:
    from omega_scan.app.dependency_container import DependencyContainer

_ScanResult = Result[ScanRunDTO, DomainError]


class _RelayHandler(logging.Handler):
    """Relaie chaque enregistrement du logger technique vers un callback,
    le temps d'un scan (voir ScanProgressScreen._run_scan)."""

    def __init__(self, callback: Callable[[str], None]) -> None:
        super().__init__(level=logging.INFO)
        self._callback = callback

    def emit(self, record: logging.LogRecord) -> None:
        self._callback(record.getMessage())


class ScanProgressScreen(Screen[None]):
    """Ecran transitoire : disparait des que le scan se termine (succes ->
    FindingsScreen remplace cet ecran, echec -> notification puis retour).

    Soit `raw_target`+`profile_name` (nouveau scan), soit `replay_scan_id`
    (relecture) doivent etre fournis, jamais les deux."""

    def __init__(
        self,
        *,
        container: DependencyContainer,
        authorization_confirmed: bool,
        raw_target: str | None = None,
        profile_name: str | None = None,
        replay_scan_id: str | None = None,
    ) -> None:
        super().__init__()
        self._container = container
        self._authorization_confirmed = authorization_confirmed
        self._raw_target = raw_target
        self._profile_name = profile_name
        self._replay_scan_id = replay_scan_id

    def compose(self) -> ComposeResult:
        label = self._raw_target or f"relecture de {self._replay_scan_id}"
        yield ProgressPanel(message=f"Scan de {label} en cours...")

    def on_mount(self) -> None:
        self.run_worker(self._run_scan(), exclusive=True)

    def _on_log_record(self, message: str) -> None:
        # Emis depuis le thread du worker (les probers tournent via
        # asyncio.to_thread) : call_from_thread est obligatoire, la
        # manipulation directe d'un widget Textual hors thread principal
        # n'est pas sure.
        self.app.call_from_thread(self._write_log_line, message)

    def _write_log_line(self, message: str) -> None:
        if self.is_mounted:
            self.query_one(ProgressPanel).write_line(message)

    async def _run_scan(self) -> None:
        container = self._container

        handler = _RelayHandler(self._on_log_record)
        technical_logger = container.technical_logger
        technical_logger.addHandler(handler)

        def _call_replay_scan() -> _ScanResult:
            assert self._replay_scan_id is not None
            return replay_scan(
                target_repository=container.target_repository,
                scan_repository=container.scan_repository,
                connectivity_prober=container.connectivity_prober,
                http_prober=container.http_prober,
                tls_prober=container.tls_prober,
                path_prober=container.path_prober,
                methods_prober=container.methods_prober,
                audit_sink=container.audit_sink,
                now_factory=utc_now,
                scan_id=self._replay_scan_id,
                authorization_confirmed=self._authorization_confirmed,
            )

        def _call_run_scan() -> _ScanResult:
            assert self._raw_target is not None and self._profile_name is not None
            return run_scan(
                target_repository=container.target_repository,
                scan_repository=container.scan_repository,
                connectivity_prober=container.connectivity_prober,
                http_prober=container.http_prober,
                tls_prober=container.tls_prober,
                path_prober=container.path_prober,
                methods_prober=container.methods_prober,
                audit_sink=container.audit_sink,
                now_factory=utc_now,
                raw_target=self._raw_target,
                profile_name=self._profile_name,
                authorization_confirmed=self._authorization_confirmed,
                host_machine=socket.gethostname(),
            )

        try:
            if self._replay_scan_id is not None:
                result = await asyncio.to_thread(_call_replay_scan)
            else:
                result = await asyncio.to_thread(_call_run_scan)
        finally:
            technical_logger.removeHandler(handler)
        if isinstance(result, Err):
            self.app.notify(str(result.error), title="Scan refuse", severity="error")
            self.dismiss()
            return
        self.app.switch_screen(FindingsScreen(container=self._container, scan=result.value))
