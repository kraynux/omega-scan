# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Classification des erreurs réseau et métier.
Section 3.1 et 9.9 de la spec.
"""

from dataclasses import dataclass, asdict
from typing import Optional


# ==============================================================================
# CONSTANTES DE CATÉGORISATION 
# ==============================================================================
FAILURE_CATEGORY_DNS = "dns_failure"
FAILURE_CATEGORY_REFUSED = "connection_refused"
FAILURE_CATEGORY_TIMEOUT = "timeout"
FAILURE_CATEGORY_TLS_HANDSHAKE = "tls_handshake_failure"
FAILURE_CATEGORY_RESET = "reset_by_peer"
FAILURE_CATEGORY_UNKNOWN = "unknown"

VALID_FAILURE_CATEGORIES = {
    FAILURE_CATEGORY_DNS,
    FAILURE_CATEGORY_REFUSED,
    FAILURE_CATEGORY_TIMEOUT,
    FAILURE_CATEGORY_TLS_HANDSHAKE,
    FAILURE_CATEGORY_RESET,
    FAILURE_CATEGORY_UNKNOWN,
}

# Phases du pipeline où une erreur peut survenir
PHASE_VALIDATION = "validation"
PHASE_NORMALIZATION = "normalization"
PHASE_CONNECTIVITY = "connectivity"
PHASE_HTTP_PROBE = "http_probe"
PHASE_TLS_PROBE = "tls_probe"
PHASE_PATH_PROBE = "path_probe"
PHASE_METHODS_PROBE = "methods_probe"
PHASE_NORMALIZERS = "normalizers"
PHASE_CHECKS = "checks"
PHASE_PIPELINE = "pipeline"
PHASE_EXPORT = "export"


# ==============================================================================
# MODÈLES D'ERREUR
# ==============================================================================
@dataclass
class ScanError:
    """
    Erreur survenue pendant le scan.
    Structure alignée sur la section 9.9 de la spec.
    """
    module: str
    phase: str
    error_type: str
    message: str
    fatal: bool = False
    related_target: Optional[str] = None
    related_scheme: Optional[str] = None
    failure_category: Optional[str] = None

    def __post_init__(self):
        if self.failure_category and self.failure_category not in VALID_FAILURE_CATEGORIES:
            raise ValueError(
                f"failure_category invalide : {self.failure_category}. "
                f"Valeurs autorisées : {VALID_FAILURE_CATEGORIES}"
            )

    def to_dict(self) -> dict:
        return asdict(self)


class ScanException(Exception):
    """Exception de base du scanner."""
    pass


class TargetParseError(ScanException):
    """Erreur de parsing de cible (section 2.2)."""
    pass


class ConnectivityError(ScanException):
    """Erreur de connectivité réseau."""
    def __init__(self, message: str, failure_category: str):
        super().__init__(message)
        if failure_category not in VALID_FAILURE_CATEGORIES:
            raise ValueError(f"failure_category invalide : {failure_category}")
        self.failure_category = failure_category


class TimeoutError(ConnectivityError):
    def __init__(self, message: str = "Timeout de connexion"):
        super().__init__(message, FAILURE_CATEGORY_TIMEOUT)


class ConnectionRefusedError(ConnectivityError):
    def __init__(self, message: str = "Connexion refusée"):
        super().__init__(message, FAILURE_CATEGORY_REFUSED)


class DnsResolutionError(ConnectivityError):
    def __init__(self, message: str = "Échec de résolution DNS"):
        super().__init__(message, FAILURE_CATEGORY_DNS)


class TlsHandshakeError(ConnectivityError):
    def __init__(self, message: str = "Échec du handshake TLS"):
        super().__init__(message, FAILURE_CATEGORY_TLS_HANDSHAKE)


class ConnectionResetError(ConnectivityError):
    def __init__(self, message: str = "Connexion réinitialisée par le pair"):
        super().__init__(message, FAILURE_CATEGORY_RESET)


# ==============================================================================
# UTILITAIRES DE CLASSIFICATION
# ==============================================================================
def classify_exception(exc: Exception) -> str:
    """
    Classe une exception Python en failure_category.
    Utilisé par les collectors pour remplir ScanError.failure_category.
    """
    exc_type = type(exc).__name__.lower()
    exc_msg = str(exc).lower()

    if "timeout" in exc_type or "timed out" in exc_msg:
        return FAILURE_CATEGORY_TIMEOUT
    elif "refused" in exc_msg or "refused" in exc_type:
        return FAILURE_CATEGORY_REFUSED
    elif "dns" in exc_msg or "dns" in exc_type or "name resolution" in exc_msg:
        return FAILURE_CATEGORY_DNS
    elif "ssl" in exc_type or "tls" in exc_type or "certificate" in exc_msg:
        return FAILURE_CATEGORY_TLS_HANDSHAKE
    elif "reset" in exc_msg or "broken pipe" in exc_msg:
        return FAILURE_CATEGORY_RESET
    else:
        return FAILURE_CATEGORY_UNKNOWN 


def build_error_from_exception(
    exc: Exception,
    module: str,
    phase: str,
    related_target: Optional[str] = None,
    related_scheme: Optional[str] = None,
    fatal: bool = False,
) -> ScanError:
    """
    Construit un ScanError à partir d'une exception.
    Catégorise automatiquement l'erreur réseau.
    """
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
