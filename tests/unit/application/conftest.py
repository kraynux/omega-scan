# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Fakes de ports partages par les tests unitaires de application/ — classes
Python simples implementant chaque Protocol, sans mock/patch, sans SQLite
reel, sans reseau, sans Textual (ARCHITECTURE.md §9)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest

from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import PinnedTarget
from omega_scan.domain.terminal.models import TerminalSignals


class FakeTargetRepository:
    def __init__(self) -> None:
        self._pinned: dict[str, PinnedTarget] = {}

    def pin(self, pinned: PinnedTarget) -> None:
        self._pinned[pinned.normalized_host] = pinned

    def unpin(self, normalized_host: str) -> None:
        self._pinned.pop(normalized_host, None)

    def get(self, normalized_host: str) -> PinnedTarget | None:
        return self._pinned.get(normalized_host)

    def list_pinned(self) -> tuple[PinnedTarget, ...]:
        return tuple(self._pinned.values())


class FakeScanRepository:
    def __init__(self) -> None:
        self._runs: dict[str, Any] = {}

    def save(self, run: Any) -> None:
        self._runs[run.meta["scan_id"]] = run

    def get(self, scan_id: str) -> Any | None:
        return self._runs.get(scan_id)

    def list_history(
        self, *, normalized_host: str | None = None, limit: int = 50
    ) -> tuple[Any, ...]:
        runs = list(self._runs.values())
        if normalized_host is not None:
            runs = [r for r in runs if r.target.normalized_host == normalized_host]
        runs.sort(key=lambda r: r.meta["started_at"], reverse=True)
        return tuple(runs[:limit])

    def clear(self) -> None:
        self._runs.clear()


class FakeConnectivityProber:
    def probe(self, target: Any, profile: Any, errors: list[ScanError]) -> dict[str, Any]:
        return {"http_reachable": True, "https_reachable": True}


class FakeHttpProber:
    def probe(self, target: Any, profile: Any, errors: list[ScanError]) -> dict[str, Any]:
        return {
            "overview": {
                "preferred_scheme": "https",
                "catch_all_suspected": False,
                "proxy_suspected": False,
                "content_profile": "unknown",
            },
            "http": {"attempted": True, "ok": True, "final_url": "https://example.org/"},
            "https": {"attempted": True, "ok": True, "headers": {}},
        }


class FakeTlsProber:
    def probe(self, target: Any, profile: Any, errors: list[ScanError]) -> dict[str, Any]:
        return {"attempted": True, "handshake_success": True}


class FakePathProber:
    def probe(
        self, target: Any, profile: Any, http_data: dict[str, Any], errors: list[ScanError]
    ) -> dict[str, Any]:
        return {"catch_all_suspected": False, "path_probe_context": []}


class FakeMethodsProber:
    def probe(
        self, target: Any, profile: Any, http_data: dict[str, Any], errors: list[ScanError]
    ) -> dict[str, Any]:
        return {"methods_tested": []}


class FailingHttpProber:
    """Ajoute une erreur non fatale a `errors`, comme un prober v1 reel
    face a un echec reseau previsible (ARCHITECTURE.md §5.3)."""

    def probe(self, target: Any, profile: Any, errors: list[ScanError]) -> dict[str, Any]:
        errors.append(
            ScanError(
                module="http_prober",
                phase="http_probe",
                error_type="ConnectError",
                message="Connexion refusee",
                fatal=False,
                failure_category="connection_refused",
            )
        )
        return {
            "overview": {
                "preferred_scheme": None,
                "catch_all_suspected": False,
                "proxy_suspected": False,
                "content_profile": "unknown",
            },
            "http": {"attempted": True, "ok": False},
            "https": {"attempted": True, "ok": False},
        }


class FakeReportExporter:
    def __init__(self) -> None:
        self.calls: list[tuple[Any, Path, Any]] = []

    def export(self, run: Any, output_path: Path, *, export_format: Any, export_theme: str = "omega-base") -> Path:
        self.calls.append((run, output_path, export_format))
        output_path.write_text("fake-report", encoding="utf-8")
        return output_path


class FakeSettingsStore:
    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    def get(self, key: str, default: str | None = None) -> str | None:
        return self._data.get(key, default)

    def set(self, key: str, value: str) -> None:
        self._data[key] = value

    def all(self) -> dict[str, str]:
        return dict(self._data)


class FakeTerminalDetector:
    def __init__(self, signals: TerminalSignals | None = None) -> None:
        self._signals = signals or TerminalSignals(
            family="ghostty", columns=140, rows=40, is_ssh=False
        )

    def detect(self) -> TerminalSignals:
        return self._signals


class FakeAuditSink:
    """Callable-like : accumule les evenements recus pour assertion."""

    def __init__(self) -> None:
        self.events: list[Any] = []

    def __call__(self, event: Any) -> None:
        self.events.append(event)


class SequentialClock:
    """now_factory deterministe : chaque appel avance de `step`, pour un
    duration_ms reellement non nul et reproductible en test."""

    def __init__(self, start: datetime | None = None, step: timedelta = timedelta(seconds=1)) -> None:
        self._current = start or datetime(2026, 1, 1, tzinfo=timezone.utc)
        self._step = step

    def __call__(self) -> datetime:
        value = self._current
        self._current = self._current + self._step
        return value


@pytest.fixture
def target_repository() -> FakeTargetRepository:
    return FakeTargetRepository()


@pytest.fixture
def scan_repository() -> FakeScanRepository:
    return FakeScanRepository()


@pytest.fixture
def probers() -> dict[str, Any]:
    return {
        "connectivity_prober": FakeConnectivityProber(),
        "http_prober": FakeHttpProber(),
        "tls_prober": FakeTlsProber(),
        "path_prober": FakePathProber(),
        "methods_prober": FakeMethodsProber(),
    }


@pytest.fixture
def audit_sink() -> FakeAuditSink:
    return FakeAuditSink()


@pytest.fixture
def now_factory() -> SequentialClock:
    return SequentialClock()
