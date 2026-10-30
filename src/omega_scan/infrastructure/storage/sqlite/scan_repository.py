# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation SQLite du port ScanRepository.

Voir schema.py pour la justification du stockage hybride (colonnes
indexees + blob JSON complet via ScanRun.to_dict())."""
from __future__ import annotations

import json
import sqlite3
from typing import Any

from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding
from omega_scan.domain.scans.models import ScanRun, Summary
from omega_scan.domain.targets.models import Target
from omega_scan.infrastructure.exceptions import StorageError
from omega_scan.shared.i18n import _


class SqliteScanRepository:
    """Implemente ports/scan_repository.py::ScanRepository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def save(self, run: ScanRun) -> None:
        try:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO scans (
                    scan_id, normalized_host, started_at, scan_status, overall_rating, run_json
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    run.meta["scan_id"],
                    run.target.normalized_host,
                    run.meta["started_at"],
                    run.summary.scan_status,
                    run.summary.overall_rating,
                    json.dumps(run.to_dict(), ensure_ascii=False),
                ),
            )
            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(
                _("Échec de sauvegarde du scan {get!r} : {exc}").format(get=run.meta.get('scan_id'), exc=exc)
            ) from exc

    def get(self, scan_id: str) -> ScanRun | None:
        try:
            row = self._connection.execute(
                "SELECT run_json FROM scans WHERE scan_id = ?", (scan_id,)
            ).fetchone()
        except sqlite3.Error as exc:
            raise StorageError(_("Échec de lecture du scan {scan_id!r} : {exc}").format(scan_id=scan_id, exc=exc)) from exc
        return _run_from_json(row["run_json"]) if row is not None else None

    def list_history(
        self,
        *,
        normalized_host: str | None = None,
        limit: int = 50,
    ) -> tuple[ScanRun, ...]:
        query = "SELECT run_json FROM scans WHERE 1 = 1"
        params: list[object] = []
        if normalized_host is not None:
            query += " AND normalized_host = ?"
            params.append(normalized_host)
        query += " ORDER BY started_at DESC LIMIT ?"
        params.append(limit)

        try:
            rows = self._connection.execute(query, params).fetchall()
        except sqlite3.Error as exc:
            raise StorageError(_("Échec de listage de l'historique des scans : {exc}").format(exc=exc)) from exc
        return tuple(_run_from_json(row["run_json"]) for row in rows)

    def clear(self) -> None:
        try:
            self._connection.execute("DELETE FROM scans")
            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(_("Échec de purge de l'historique des scans : {exc}").format(exc=exc)) from exc


def _run_from_json(raw: str) -> ScanRun:
    """Reconstruit un ScanRun a partir du JSON produit par
    ScanRun.to_dict() : les sous-objets (target/findings/summary) sont des
    dicts imbriques dans ce JSON, jamais des instances — il faut les
    reconstruire explicitement, `evidence` d'un finding en particulier
    (retiree du dict avant l'appel a Finding(**...) pour eviter un
    doublon d'argument avec le parametre `evidence=`)."""
    data: dict[str, Any] = json.loads(raw)

    findings = []
    for finding_data in data["findings"]:
        finding_fields = dict(finding_data)
        evidence_data = finding_fields.pop("evidence", None)
        findings.append(
            Finding(
                **finding_fields,
                evidence=Evidence(**evidence_data) if evidence_data else None,
            )
        )

    return ScanRun(
        meta=data["meta"],
        target=Target(**data["target"]),
        scan_profile=data["scan_profile"],
        connectivity=data["connectivity"],
        http=data["http"],
        tls=data["tls"],
        findings=findings,
        summary=Summary(**data["summary"]),
        errors=data["errors"],
    )
