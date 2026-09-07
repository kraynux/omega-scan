# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Conversion entites de domaine -> DTO. Seul endroit du projet ou une
entite/VO de domain/ est lue pour produire un objet de application/dto/."""
from __future__ import annotations

from omega_lib.terminal.models import TerminalProfile

from omega_scan.application.dto.comparison_dto import ChangedFindingDTO, ScanComparisonDTO
from omega_scan.application.dto.profile_dto import ScanProfileDTO
from omega_scan.application.dto.scan_dto import EvidenceDTO, FindingDTO, ScanRunDTO, ScanSummaryDTO
from omega_scan.application.dto.target_dto import PinnedTargetDTO
from omega_scan.application.dto.terminal_dto import TerminalProfileDTO
from omega_scan.domain.findings.evidence import Evidence
from omega_scan.domain.findings.models import Finding
from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.reports.comparison import ScanComparison
from omega_scan.domain.scans.models import ScanRun
from omega_scan.domain.targets.models import PinnedTarget


def pinned_target_to_dto(pinned: PinnedTarget) -> PinnedTargetDTO:
    return PinnedTargetDTO(
        normalized_host=pinned.normalized_host,
        authorized=pinned.authorized,
        pinned_at=pinned.pinned_at,
        note=pinned.note,
    )


def evidence_to_dto(evidence: Evidence) -> EvidenceDTO:
    return EvidenceDTO(
        type=evidence.type,
        value=evidence.value,
        source=evidence.source,
        excerpt=evidence.excerpt,
    )


def finding_to_dto(finding: Finding) -> FindingDTO:
    return FindingDTO(
        finding_id=finding.finding_id,
        rule_id=finding.rule_id,
        category=finding.category,
        title=finding.title,
        status=finding.status,
        severity=finding.severity,
        confidence=finding.confidence,
        applicability=finding.applicability,
        description=finding.description,
        impact=finding.impact,
        remediation=finding.remediation,
        evidence=evidence_to_dto(finding.evidence) if finding.evidence is not None else None,
        location=finding.location,
        references=tuple(finding.references),
        tags=tuple(finding.tags),
    )


def scan_summary_to_dto(run: ScanRun) -> ScanSummaryDTO:
    return ScanSummaryDTO(
        scan_id=run.meta["scan_id"],
        normalized_host=run.target.normalized_host,
        started_at=run.meta["started_at"],
        scan_status=run.summary.scan_status,
        overall_rating=run.summary.overall_rating,
        short_message=run.summary.short_message,
        findings_total=run.summary.findings_total,
    )


def scan_run_to_dto(run: ScanRun) -> ScanRunDTO:
    return ScanRunDTO(
        scan_id=run.meta["scan_id"],
        normalized_host=run.target.normalized_host,
        profile_name=run.scan_profile.get("profile_name", ""),
        started_at=run.meta["started_at"],
        finished_at=run.meta["finished_at"],
        duration_ms=run.meta["duration_ms"],
        scan_status=run.summary.scan_status,
        findings=tuple(finding_to_dto(f) for f in run.findings),
        summary=scan_summary_to_dto(run),
        connectivity=run.connectivity,
        http=run.http,
        tls=run.tls,
        errors=tuple(run.errors),
    )


def scan_comparison_to_dto(comparison: ScanComparison) -> ScanComparisonDTO:
    return ScanComparisonDTO(
        new_findings=tuple(finding_to_dto(f) for f in comparison.new_findings),
        resolved_findings=tuple(finding_to_dto(f) for f in comparison.resolved_findings),
        unchanged_findings=tuple(finding_to_dto(f) for f in comparison.unchanged_findings),
        changed_findings=tuple(
            ChangedFindingDTO(previous=finding_to_dto(prev), current=finding_to_dto(curr))
            for prev, curr in comparison.changed_findings
        ),
    )


def scan_profile_to_dto(profile: ScanProfile) -> ScanProfileDTO:
    return ScanProfileDTO(
        profile_name=profile.profile_name,
        timeout_connect=profile.timeout_connect,
        timeout_read=profile.timeout_read,
        http_methods_tested=tuple(profile.http_methods_tested),
        path_checks_enabled=profile.path_checks_enabled,
        tls_checks_enabled=profile.tls_checks_enabled,
    )


def terminal_profile_to_dto(profile: TerminalProfile) -> TerminalProfileDTO:
    return TerminalProfileDTO(
        family=profile.signals.family,
        columns=profile.signals.columns,
        rows=profile.signals.rows,
        render_profile=profile.render_profile.value,
    )
