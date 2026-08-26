# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Hierarchie d'exceptions applicatives (ARCHITECTURE.md §5.2)."""
from __future__ import annotations

from omega_scan.core.exceptions import OmegaScanError


class ApplicationError(OmegaScanError):
    """Racine des echecs techniques inattendus survenant dans application/
    (bug, contrat viole) — jamais utilisee pour un echec metier attendu,
    qui reste porte par un Result[T, DomainError]."""


class UseCaseExecutionError(ApplicationError):
    """Un command ou query n'a pas pu aller a son terme pour une raison
    technique non anticipee par le metier."""


class CapabilityUnavailableError(ApplicationError):
    """Une capacite requise (application/pipeline/guards/capability_guard.py)
    est indisponible au moment de la verification."""


class PermissionDeniedError(ApplicationError):
    """Traduction applicative d'un refus d'autorisation, une fois
    l'UnauthorizedTargetError du domaine remonte et contextualise."""


class PartialExecutionError(ApplicationError):
    """Une action composee (ex. plusieurs etapes du pipeline de scan) a
    partiellement reussi avant d'echouer."""


class ProberFailureError(ApplicationError):
    """Echec technique d'un prober reseau, non categorisable en
    ScanError normal — traduit par l'adaptateur infrastructure depuis une
    exception httpx brute. Definie ici plutot que dans
    infrastructure/exceptions.py : c'est le seul type technique
    qu'application/pipeline/steps.py doit connaitre par son nom pour
    marquer un module en `partial`, et la Dependency Rule interdit a
    application/ d'importer infrastructure/ (ARCHITECTURE.md §5.2, meme
    raisonnement que RunnerFailureError chez omega-stress).

    Pas de RunnerFailureError ni AbortError ici : specifiques a
    omega-stress (generateur de charge, arret automatique sur seuil),
    sans equivalent chez omega-scan (voir ARCHITECTURE.md §0)."""
