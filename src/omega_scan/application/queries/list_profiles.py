# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Query : lister les profils de scan predefinis (lecture seule, aucun port)."""
from __future__ import annotations

from omega_scan.application.dto.mappers import scan_profile_to_dto
from omega_scan.application.dto.profile_dto import ScanProfileDTO
from omega_scan.domain.profiles.policies import PROFILES


def list_profiles() -> tuple[ScanProfileDTO, ...]:
    """Pure : lit directement le catalogue domain/profiles/policies.py,
    aucun port necessaire (contrairement aux profils de charge d'omega-stress,
    ceux-ci ne sont ni persistes ni modifiables par l'utilisateur)."""
    return tuple(scan_profile_to_dto(p) for p in PROFILES.values())
