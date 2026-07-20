# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Journalisation technique du scanner.
Séparée du scan_result : les logs tracent les tentatives réseau,
le scan_result ne garde que les faits utiles à l'analyse (section 4.4).
"""

import logging
import sys
from typing import Optional
from pathlib import Path


# Niveaux de log
LEVEL_DEBUG = logging.DEBUG
LEVEL_INFO = logging.INFO
LEVEL_WARNING = logging.WARNING
LEVEL_ERROR = logging.ERROR


class ScanLogger:
    """
    Logger technique du scanner.
    Utilise le module logging standard de Python.
    """

    def __init__(
        self,
        name: str = "Omega-scan",
        level: int = logging.INFO,
        log_file: Optional[Path] = None,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers.clear()  # Éviter les doublons

        # Format commun
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler console
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Handler fichier (optionnel)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(LEVEL_DEBUG)  # Toujours tout logger dans le fichier
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def log_network_attempt(
        self,
        scheme: str,
        url: str,
        success: bool,
        status_code: Optional[int] = None,
        elapsed_ms: Optional[int] = None,
        error: Optional[str] = None,
    ):
        """
        Trace une tentative réseau (section 4.4).
        Séparé du scan_result pour garder les logs détaillés.
        """
        if success:
            self.info(
                f"[NETWORK] {scheme.upper()} {url} → {status_code} "
                f"({elapsed_ms}ms)"
            )
        else:
            self.warning(
                f"[NETWORK] {scheme.upper()} {url} → ÉCHEC : {error}"
            )

    def log_phase_start(self, phase: str):
        """Log le début d'une phase du pipeline."""
        self.info(f"[PHASE] Début : {phase}")

    def log_phase_end(self, phase: str, duration_ms: int):
        """Log la fin d'une phase du pipeline."""
        self.info(f"[PHASE] Fin : {phase} ({duration_ms}ms)")

    def log_check(self, rule_id: str, status: str, confidence: str):
        """Log l'exécution d'un check."""
        self.debug(f"[CHECK] {rule_id} → {status} (confidence: {confidence})")


# Logger global par défaut
_default_logger: Optional[ScanLogger] = None


def get_logger() -> ScanLogger:
    """Retourne le logger global (créé à la demande)."""
    global _default_logger
    if _default_logger is None:
        _default_logger = ScanLogger(name="Omega-scan")
    return _default_logger


def set_logger(logger: ScanLogger):
    """Remplace le logger global (utile pour les tests)."""
    global _default_logger
    _default_logger = logger
