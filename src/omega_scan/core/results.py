# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Result[T, E] generique : valeur de retour typee pour les echecs metier attendus."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T_co = TypeVar("T_co", covariant=True)
E_co = TypeVar("E_co", covariant=True)


@dataclass(frozen=True, slots=True)
class Ok(Generic[T_co]):
    """Issue reussie d'une operation, porte la valeur produite."""

    value: T_co

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class Err(Generic[E_co]):
    """Echec metier attendu, porte l'erreur (typiquement une DomainError)."""

    error: E_co

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True


Result = Ok[T_co] | Err[E_co]
"""Alias d'union utilise comme type de retour par tout command/query pouvant
echouer pour une raison metier prevue (voir ARCHITECTURE.md §5.1)."""
