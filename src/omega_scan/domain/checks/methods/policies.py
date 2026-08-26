# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Table des regles par methode HTTP (MTH-*)."""
from __future__ import annotations

from typing import Any

METHOD_RULES: dict[str, dict[str, Any]] = {
    "OPTIONS": {
        "rule_id": "MTH-OPTIONS-001",
        "title": "Methode HTTP OPTIONS activee",
        "severity": "info",
        "default_confidence": "certain",
        "description": "La methode OPTIONS est activee et peut reveler les methodes autorisees.",
        "impact": "Fuite d'information mineure sur la configuration du serveur.",
        "remediation": "Desactiver la methode OPTIONS si elle n'est pas necessaire.",
    },
    "TRACE": {
        "rule_id": "MTH-TRACE-001",
        "title": "Methode HTTP TRACE activee",
        "severity": "medium",
        "default_confidence": "certain",
        "description": "La methode TRACE est activee, ce qui peut faciliter les attaques Cross-Site Tracing (XST).",
        "impact": "Risque de vol de cookies ou d'identifiants via XST.",
        "remediation": "Desactiver la methode TRACE dans la configuration du serveur web.",
    },
    "PUT": {
        "rule_id": "MTH-PUT-001",
        "title": "Methode HTTP PUT activee",
        "severity": "high",
        "default_confidence": "certain",
        "description": "La methode PUT est activee, permettant potentiellement l'upload de fichiers.",
        "impact": "Risque de depot de contenu malveillant ou de modification de ressources.",
        "remediation": "Desactiver la methode PUT sauf si explicitement requise et securisee.",
    },
    "DELETE": {
        "rule_id": "MTH-DELETE-001",
        "title": "Methode HTTP DELETE activee",
        "severity": "high",
        "default_confidence": "certain",
        "description": "La methode DELETE est activee, permettant potentiellement la suppression de ressources.",
        "impact": "Risque de suppression non autorisee de donnees.",
        "remediation": "Desactiver la methode DELETE sauf si explicitement requise et securisee.",
    },
    "PATCH": {
        "rule_id": "MTH-PATCH-001",
        "title": "Methode HTTP PATCH activee",
        "severity": "medium",
        "default_confidence": "certain",
        "description": "La methode PATCH est activee, permettant la modification partielle de ressources.",
        "impact": "Risque de modification non autorisee de donnees.",
        "remediation": "Desactiver la methode PATCH sauf si explicitement requise et securisee.",
    },
    "CONNECT": {
        "rule_id": "MTH-CONNECT-001",
        "title": "Methode HTTP CONNECT activee",
        "severity": "high",
        "default_confidence": "certain",
        "description": "La methode CONNECT est activee, permettant l'etablissement de tunnels TCP.",
        "impact": "Risque d'utilisation du serveur comme proxy ouvert pour des attaques.",
        "remediation": "Restreindre la methode CONNECT aux seuls ports necessaires (ex: 443) ou la desactiver.",
    },
}
