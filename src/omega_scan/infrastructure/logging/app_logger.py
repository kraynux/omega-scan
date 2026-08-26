# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Journalisation technique du scanner (ex core/logger.py de la v1).

Separee du ScanRun : les logs tracent les tentatives reseau, le ScanRun ne
garde que les faits utiles a l'analyse. Distincte de audit_logger.py, qui
journalise les decisions d'autorisation, pas la mecanique reseau."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

LEVEL_DEBUG = logging.DEBUG
LEVEL_INFO = logging.INFO
LEVEL_WARNING = logging.WARNING
LEVEL_ERROR = logging.ERROR


class ScanLogger:
    """Logger technique du scanner, sur le module logging standard."""

    def __init__(
        self,
        name: str = "Omega-scan",
        level: int = logging.INFO,
        log_file: Path | None = None,
        console: bool = True,
    ) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers.clear()
        # Sans ca, un handler attache par une autre bibliotheque au logger
        # racine (ex. le serveur de test HTTP interne) rediffuse quand
        # meme nos messages vers la console reelle par propagation,
        # meme quand console=False ci-dessous n'attache aucun handler
        # ICI — bug reel observe en verifiant ce correctif.
        self.logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # `console=False` sous le TUI (app/bootstrap.py) : Textual controle
        # l'ecran en mode alternatif, une ecriture directe sur stderr
        # pendant un scan corrompt son rendu (defilement, curseur/spinner
        # desynchronise) — bug reel signale par l'utilisateur. Le fichier
        # de log reste toujours actif, seule la sortie console est
        # conditionnelle.
        if console:
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(LEVEL_DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def log_network_attempt(
        self,
        scheme: str,
        url: str,
        success: bool,
        status_code: int | None = None,
        elapsed_ms: int | None = None,
        error: str | None = None,
    ) -> None:
        if success:
            self.info(f"[NETWORK] {scheme.upper()} {url} -> {status_code} ({elapsed_ms}ms)")
        else:
            self.warning(f"[NETWORK] {scheme.upper()} {url} -> ECHEC : {error}")

    def log_phase_start(self, phase: str) -> None:
        self.info(f"[PHASE] Debut : {phase}")

    def log_phase_end(self, phase: str, duration_ms: int) -> None:
        self.info(f"[PHASE] Fin : {phase} ({duration_ms}ms)")

    def log_check(self, rule_id: str, status: str, confidence: str) -> None:
        self.debug(f"[CHECK] {rule_id} -> {status} (confidence: {confidence})")


_default_logger: ScanLogger | None = None


def get_logger() -> ScanLogger:
    """Retourne le logger global (cree a la demande)."""
    global _default_logger
    if _default_logger is None:
        _default_logger = ScanLogger(name="Omega-scan")
    return _default_logger


def set_logger(logger: ScanLogger) -> None:
    """Remplace le logger global (utile pour les tests)."""
    global _default_logger
    _default_logger = logger
