# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Objets Target et PinnedTarget : cible canonique et autorisation memorisee."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Target:
    """Representation canonique d'une cible de scan, produite une seule
    fois par domain/targets/validation.py::parse_target."""

    input_raw: str
    normalized_host: str
    normalized_url_http: str
    normalized_url_https: str
    requested_scheme: str | None
    requested_port: int | None
    requested_path: str
    target_kind: str  # "hostname", "ipv4", "ipv6"
    scope_kind: str  # "loopback", "link_local", "private_lan", "special_non_global", "public", "hostname"
    scan_modes: str  # "http", "https", "both"
    is_ip: bool
    ip_version: int | None
    is_private: bool
    is_loopback: bool
    is_link_local: bool
    is_global: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PinnedTarget:
    """Cible epinglee avec une decision d'autorisation memorisee, evitant
    de reconfirmer a chaque scan (ARCHITECTURE.md §7). Produite par
    domain/targets/service.py::pin_target, persistee par
    infrastructure/storage/sqlite/target_repository.py (Lot M2)."""

    normalized_host: str
    authorized: bool
    pinned_at: str  # ISO 8601 UTC, fourni par l'appelant (voir service.py)
    note: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)
