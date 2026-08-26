# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Preuve concrete associee a un finding."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Evidence:
    """Preuve concrete associee a un finding."""

    type: str  # "header", "cookie", "status_code", "body_content", "tls_field", etc.
    value: str
    source: str  # ex. "response.headers", "tls.certificate"
    excerpt: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)
