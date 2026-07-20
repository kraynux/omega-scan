# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Utilitaires de sérialisation JSON.
Garantit qu'aucun objet non sérialisable ne passe.
"""

import json
from datetime import datetime
from typing import Any

def to_jsonable(obj: Any) -> Any:
    """
    Convertit récursivement un objet en structure JSON-serializable.
    Lève TypeError si un objet non convertible est rencontré.
    """
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    elif isinstance(obj, datetime):
        # Normaliser le format ISO 8601 UTC
        iso = obj.isoformat()
        # Remplacer +00:00 par Z si présent
        if iso.endswith("+00:00"):
            iso = iso[:-6] + "Z"
        elif not iso.endswith("Z"):
            iso += "Z"
        return iso
    elif isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_jsonable(item) for item in obj]
    elif hasattr(obj, "to_dict"):
        return to_jsonable(obj.to_dict())
    else:
        raise TypeError(f"Objet non sérialisable : {type(obj).__name__} — {obj}")


def dumps(obj: Any, indent: int = 2) -> str:
    """Sérialise un objet en JSON avec conversion préalable."""
    return json.dumps(to_jsonable(obj), indent=indent, ensure_ascii=False)
