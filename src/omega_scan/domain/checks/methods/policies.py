# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Table des regles par methode HTTP (MTH-*)."""
from __future__ import annotations

from typing import Any

from omega_scan.shared.i18n import _

METHOD_RULES: dict[str, dict[str, Any]] = {
    "OPTIONS": {
        "rule_id": "MTH-OPTIONS-001",
        "title": _("Méthode HTTP OPTIONS activée"),
        "severity": "info",
        "default_confidence": "certain",
        "description": _("La méthode OPTIONS est activée et peut révéler les méthodes autorisées."),
        "impact": _("Fuite d'information mineure sur la configuration du serveur."),
        "remediation": _("Désactiver la méthode OPTIONS si elle n'est pas nécessaire."),
    },
    "TRACE": {
        "rule_id": "MTH-TRACE-001",
        "title": _("Méthode HTTP TRACE activée"),
        "severity": "medium",
        "default_confidence": "certain",
        "description": _("La méthode TRACE est activée, ce qui peut faciliter les attaques "
                         "Cross-Site Tracing (XST)."),
        "impact": _("Risque de vol de cookies ou d'identifiants via XST."),
        "remediation": _("Désactiver la méthode TRACE dans la configuration du serveur web."),
    },
    "PUT": {
        "rule_id": "MTH-PUT-001",
        "title": _("Méthode HTTP PUT activée"),
        "severity": "high",
        "default_confidence": "certain",
        "description": _("La méthode PUT est activée, permettant potentiellement l'upload de "
                         "fichiers."),
        "impact": _("Risque de dépôt de contenu malveillant ou de modification de ressources."),
        "remediation": _("Désactiver la méthode PUT sauf si explicitement requise et sécurisée."),
    },
    "DELETE": {
        "rule_id": "MTH-DELETE-001",
        "title": _("Méthode HTTP DELETE activée"),
        "severity": "high",
        "default_confidence": "certain",
        "description": _("La méthode DELETE est activée, permettant potentiellement la "
                         "suppression de ressources."),
        "impact": _("Risque de suppression non autorisée de données."),
        "remediation": _("Désactiver la méthode DELETE sauf si explicitement requise et "
                         "sécurisée."),
    },
    "PATCH": {
        "rule_id": "MTH-PATCH-001",
        "title": _("Méthode HTTP PATCH activée"),
        "severity": "medium",
        "default_confidence": "certain",
        "description": _("La méthode PATCH est activée, permettant la modification partielle "
                         "de ressources."),
        "impact": _("Risque de modification non autorisée de données."),
        "remediation": _("Désactiver la méthode PATCH sauf si explicitement requise et sécurisée."),
    },
    "CONNECT": {
        "rule_id": "MTH-CONNECT-001",
        "title": _("Méthode HTTP CONNECT activée"),
        "severity": "high",
        "default_confidence": "certain",
        "description": _("La méthode CONNECT est activée, permettant l'établissement de "
                         "tunnels TCP."),
        "impact": _("Risque d'utilisation du serveur comme proxy ouvert pour des attaques."),
        "remediation": _("Restreindre la méthode CONNECT aux seuls ports nécessaires (ex: 443) "
                         "ou la désactiver."),
    },
}
