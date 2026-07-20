# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Export JSON du scan_result.
Section 17 de la spec.
Source de vérité complète, strictement JSON-serializable.
"""

import json
from pathlib import Path
from typing import Union

from models.scan_result import ScanResult
from core.serialization import dumps
from core.logger import get_logger


def export_json(
    scan_result: ScanResult,
    output_path: Union[str, Path],
    indent: int = 2,
) -> Path:
    """
    Exporte le scan_result en fichier JSON.
    """
    logger = get_logger()
    
    # 1. Forcer le chemin absolu pour éviter toute ambiguïté de répertoire courant
    abs_path = Path(output_path).absolute().resolve()
    logger.info(f"[JSON_EXPORT] Chemin absolu ciblé : {abs_path}")
    
    # 2. Créer le répertoire parent de force
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 3. Sérialiser
    json_str = dumps(scan_result, indent=indent)
    
    # 4. Écrire
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(json_str)
    
    logger.info(f"[JSON_EXPORT] Export terminé avec succès : {abs_path} ({len(json_str)} octets)")
    return abs_path


def export_json_string(
    scan_result: ScanResult,
    indent: int = 2,
) -> str:
    """
    Exporte le scan_result en chaîne JSON (sans écrire de fichier).
    """
    return dumps(scan_result, indent=indent)
