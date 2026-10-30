# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests e2e du dispatch CLI (interfaces/cli/main.py::run()) — seul niveau ou
interfaces/cli/ est exerce de bout en bout (ARCHITECTURE.md §9). Reutilise les
fakes de ports du Lot M3 (tests/unit/application/conftest.py) plutot que d'en
dupliquer une nouvelle serie."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from omega_scan.interfaces.cli.main import run
from tests.unit.application.conftest import (
    FakeAuditSink,
    FakeConnectivityProber,
    FakeHttpProber,
    FakeMethodsProber,
    FakePathProber,
    FakeReportExporter,
    FakeScanRepository,
    FakeTargetRepository,
    FakeTlsProber,
)


@dataclass
class FakeContainer:
    """Reprend uniquement les attributs consommes par interfaces/cli/ —
    memes noms que ceux qu'app/dependency_container.py exposera reellement
    au lot suivant (voir chaque commands/*.py::_handle_*)."""

    target_repository: FakeTargetRepository = field(default_factory=FakeTargetRepository)
    scan_repository: FakeScanRepository = field(default_factory=FakeScanRepository)
    connectivity_prober: FakeConnectivityProber = field(default_factory=FakeConnectivityProber)
    http_prober: FakeHttpProber = field(default_factory=FakeHttpProber)
    tls_prober: FakeTlsProber = field(default_factory=FakeTlsProber)
    path_prober: FakePathProber = field(default_factory=FakePathProber)
    methods_prober: FakeMethodsProber = field(default_factory=FakeMethodsProber)
    audit_sink: FakeAuditSink = field(default_factory=FakeAuditSink)
    report_exporter: FakeReportExporter = field(default_factory=FakeReportExporter)
    default_exports_dir: Path = field(default_factory=lambda: Path("/tmp/omega-scan-test-exports"))


@pytest.fixture
def container(tmp_path: Path) -> FakeContainer:
    return FakeContainer(default_exports_dir=tmp_path)


def test_scan_denied_without_authorize(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    code = run(container, ["scan", "example.org"])
    captured = capsys.readouterr()

    assert code == 1
    assert "non autorisée" in captured.err


def test_scan_succeeds_with_authorize(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    code = run(container, ["scan", "example.org", "--authorize"])
    captured = capsys.readouterr()

    assert code == 0
    assert "example.org" in captured.out
    assert container.scan_repository.list_history() != ()


def test_scan_json_output(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    code = run(container, ["scan", "example.org", "--authorize", "--json"])
    captured = capsys.readouterr()

    assert code == 0
    assert '"normalized_host": "example.org"' in captured.out


def test_scan_unknown_profile(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    code = run(container, ["scan", "example.org", "--authorize", "--profile", "quick"])
    assert code == 0
    captured = capsys.readouterr()
    assert "quick" in captured.out


def test_history_show_unknown_scan(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    code = run(container, ["history", "show", "scan-inconnu"])
    captured = capsys.readouterr()

    assert code == 1
    assert "introuvable" in captured.err


def test_history_list_then_show(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    run(container, ["scan", "example.org", "--authorize"])
    capsys.readouterr()

    list_code = run(container, ["history", "list", "--host", "example.org"])
    list_out = capsys.readouterr().out
    assert list_code == 0
    assert "example.org" in list_out

    scan_id = list_out.strip().split()[0]
    show_code = run(container, ["history", "show", scan_id])
    assert show_code == 0
    assert "example.org" in capsys.readouterr().out


def test_history_compare_two_scans(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    run(container, ["scan", "example.org", "--authorize"])
    first_id = next(iter(container.scan_repository._runs.keys()))
    run(container, ["scan", "example.org", "--authorize"])
    second_id = next(k for k in container.scan_repository._runs if k != first_id)
    capsys.readouterr()

    code = run(container, ["history", "compare", first_id, second_id])
    captured = capsys.readouterr()

    assert code == 0
    assert "Inchanges" in captured.out


def test_history_replay_pinned_target(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    run(container, ["targets", "pin", "example.org"])
    run(container, ["scan", "example.org", "--authorize"])
    scan_id = next(iter(container.scan_repository._runs.keys()))
    capsys.readouterr()

    code = run(container, ["history", "replay", scan_id])
    captured = capsys.readouterr()

    assert code == 0
    assert "example.org" in captured.out


def test_targets_pin_list_unpin(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    pin_code = run(container, ["targets", "pin", "example.org", "--note", "audit trimestriel"])
    assert pin_code == 0
    assert "audit trimestriel" in capsys.readouterr().out

    list_code = run(container, ["targets", "list"])
    assert list_code == 0
    assert "example.org" in capsys.readouterr().out

    unpin_code = run(container, ["targets", "unpin", "example.org"])
    assert unpin_code == 0
    capsys.readouterr()

    list_code_after = run(container, ["targets", "list"])
    assert list_code_after == 0
    assert "Aucune cible" in capsys.readouterr().out


def test_export_writes_report(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    run(container, ["scan", "example.org", "--authorize"])
    scan_id = next(iter(container.scan_repository._runs.keys()))
    capsys.readouterr()

    code = run(container, ["export", scan_id, "--format", "json"])
    captured = capsys.readouterr()

    assert code == 0
    assert "Export ecrit vers" in captured.out
    assert len(container.report_exporter.calls) == 1


def test_export_unknown_scan(container: FakeContainer, capsys: pytest.CaptureFixture) -> None:
    code = run(container, ["export", "scan-inconnu", "--format", "text"])
    captured = capsys.readouterr()

    assert code == 1
    assert "Aucun scan trouvé" in captured.err


def test_invalid_subcommand_exits_nonzero(container: FakeContainer) -> None:
    with pytest.raises(SystemExit) as excinfo:
        run(container, ["not-a-command"])
    assert excinfo.value.code != 0
