# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Modèles de données du scanner.
Tous les objets sont strictement JSON-serialisables.
"""

from models.target import Target
from models.evidence import Evidence
from models.finding import Finding
from models.summary import Summary
from models.scan_result import ScanResult

__all__ = ["Target", "Evidence", "Finding", "Summary", "ScanResult"]
