# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Export JSON d'un ScanRun. Source de verite complete, strictement
JSON-serializable (ex exporters/json_exporter.py + core/serialization.py
de la v1, fusionnes ici : to_jsonable() n'a pas d'autre consommateur)."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from omega_scan.domain.scans.models import ScanRun
from omega_scan.infrastructure.logging.app_logger import get_logger


def _to_jsonable(obj: Any) -> Any:
    """Convertit recursivement un objet en structure JSON-serializable.
    Leve TypeError si un objet non convertible est rencontre."""
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, datetime):
        iso = obj.isoformat()
        if iso.endswith("+00:00"):
            iso = iso[:-6] + "Z"
        elif not iso.endswith("Z"):
            iso += "Z"
        return iso
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(item) for item in obj]
    if hasattr(obj, "to_dict"):
        return _to_jsonable(obj.to_dict())
    raise TypeError(f"Objet non serialisable : {type(obj).__name__} - {obj}")


def _dumps(obj: Any, indent: int = 2) -> str:
    return json.dumps(_to_jsonable(obj), indent=indent, ensure_ascii=False)


def export_json(run: ScanRun, output_path: str | Path, indent: int = 2) -> Path:
    """Exporte le ScanRun en fichier JSON."""
    logger = get_logger()

    abs_path = Path(output_path).absolute().resolve()
    logger.info(f"[JSON_EXPORT] Chemin absolu cible : {abs_path}")

    abs_path.parent.mkdir(parents=True, exist_ok=True)
    json_str = _dumps(run, indent=indent)

    with open(abs_path, "w", encoding="utf-8") as handle:
        handle.write(json_str)

    logger.info(f"[JSON_EXPORT] Export termine avec succes : {abs_path} ({len(json_str)} octets)")
    return abs_path


def export_json_string(run: ScanRun, indent: int = 2) -> str:
    """Exporte le ScanRun en chaine JSON (sans ecrire de fichier)."""
    return _dumps(run, indent=indent)
