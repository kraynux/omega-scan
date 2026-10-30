# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Hierarchie d'exceptions d'infrastructure (ARCHITECTURE.md §5.2, §5.3)."""
from __future__ import annotations

from omega_scan.core.exceptions import OmegaScanError
from omega_scan.domain.scans.models import (
    FAILURE_CATEGORY_DNS,
    FAILURE_CATEGORY_REFUSED,
    FAILURE_CATEGORY_RESET,
    FAILURE_CATEGORY_TIMEOUT,
    FAILURE_CATEGORY_TLS_HANDSHAKE,
    FAILURE_CATEGORY_UNKNOWN,
    VALID_FAILURE_CATEGORIES,
    ScanError,
)
from omega_scan.shared.i18n import _


class InfrastructureError(OmegaScanError):
    """Racine des erreurs techniques d'infrastructure. Toute exception
    specifique a une technologie (sqlite3.Error, httpx.*, ssl.*...) est
    traduite vers un sous-type de celle-ci par l'adaptateur concerne,
    jamais laissee franchir la frontiere d'un port brute (ARCHITECTURE.md
    §5.3)."""


class StorageError(InfrastructureError):
    """Erreur de persistance, traduite depuis sqlite3.Error ou une erreur
    d'ecriture de fichier."""


class ParseError(InfrastructureError):
    """Erreur d'interpretation d'une donnee externe (reponse HTTP mal
    formee, fichier de configuration invalide...)."""


class AdapterConfigurationError(InfrastructureError):
    """Configuration d'un adaptateur invalide ou incomplete au demarrage."""


# ---------------------------------------------------------------------------
# Traduction des echecs reseau (ex core/errors.py de la v1, non touche au
# Lot M1). Ces types restent des InfrastructureError, jamais leves a travers
# les probers (ARCHITECTURE.md §0) : ils servent uniquement de vocabulaire
# pour classify_exception()/build_error_from_exception(), qui produisent un
# ScanError collecte, pas une exception propagee. Conserves ici pour
# compatibilite avec un futur usage direct (ex. app/bootstrap.py) et pour
# documenter la taxonomie technique correspondant a domain.scans.models.
# FAILURE_CATEGORY_*.
# ---------------------------------------------------------------------------


class ConnectivityError(InfrastructureError):
    """Erreur de connectivite reseau."""

    def __init__(self, message: str, failure_category: str) -> None:
        super().__init__(message)
        if failure_category not in VALID_FAILURE_CATEGORIES:
            raise ValueError(f"failure_category invalide : {failure_category}")
        self.failure_category = failure_category


class TimeoutError(ConnectivityError):
    def __init__(self, message: str = _("Timeout de connexion")) -> None:
        super().__init__(message, FAILURE_CATEGORY_TIMEOUT)


class ConnectionRefusedError(ConnectivityError):
    def __init__(self, message: str = _("Connexion refusée")) -> None:
        super().__init__(message, FAILURE_CATEGORY_REFUSED)


class DnsResolutionError(ConnectivityError):
    def __init__(self, message: str = _("Échec de résolution DNS")) -> None:
        super().__init__(message, FAILURE_CATEGORY_DNS)


class TlsHandshakeError(ConnectivityError):
    def __init__(self, message: str = _("Échec du handshake TLS")) -> None:
        super().__init__(message, FAILURE_CATEGORY_TLS_HANDSHAKE)


class ConnectionResetError(ConnectivityError):
    def __init__(self, message: str = _("Connexion réinitialisée par le pair")) -> None:
        super().__init__(message, FAILURE_CATEGORY_RESET)


def classify_exception(exc: Exception) -> str:
    """Classe une exception Python en failure_category, par inspection du
    nom de type et du message (fonctionne aussi bien pour httpx, socket,
    ssl que pour une exception generique — pas d'import direct de ces
    bibliotheques ici)."""
    exc_type = type(exc).__name__.lower()
    exc_msg = str(exc).lower()

    if "timeout" in exc_type or "timed out" in exc_msg:
        return FAILURE_CATEGORY_TIMEOUT
    if "refused" in exc_msg or "refused" in exc_type:
        return FAILURE_CATEGORY_REFUSED
    if "dns" in exc_msg or "dns" in exc_type or "name resolution" in exc_msg:
        return FAILURE_CATEGORY_DNS
    if "ssl" in exc_type or "tls" in exc_type or "certificate" in exc_msg:
        return FAILURE_CATEGORY_TLS_HANDSHAKE
    if "reset" in exc_msg or "broken pipe" in exc_msg:
        return FAILURE_CATEGORY_RESET
    return FAILURE_CATEGORY_UNKNOWN


def build_error_from_exception(
    exc: Exception,
    module: str,
    phase: str,
    related_target: str | None = None,
    related_scheme: str | None = None,
    fatal: bool = False,
) -> ScanError:
    """Construit un ScanError (domain) a partir d'une exception technique,
    categorisee automatiquement. Consomme par infrastructure/network/ :
    l'exception ne franchit jamais le port, seul ce ScanError le fait."""
    return ScanError(
        module=module,
        phase=phase,
        error_type=type(exc).__name__,
        message=str(exc),
        fatal=fatal,
        related_target=related_target,
        related_scheme=related_scheme,
        failure_category=classify_exception(exc),
    )
