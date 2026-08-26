# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Listes de reference pour les checks de profondeur TLS (TLS-*)."""
from __future__ import annotations

OBSOLETE_TLS_VERSIONS = {"SSLv2", "SSLv3", "TLSv1", "TLSv1.1"}
"""Valeurs telles que retournees par ssl.SSLSocket.version(), jugees
obsoletes. TLSv1.2 est volontairement exclu (encore largement accepte en
pratique) ; TLSv1.3 n'apparait jamais dans cet ensemble."""

WEAK_CIPHER_PATTERNS = ["RC4", "DES", "NULL", "EXPORT", "MD5"]
"""Sous-chaines recherchees (apres mise en majuscules) dans le nom de la
suite cryptographique negociee. Heuristique par nom uniquement : la taille
de cle en bits n'est pas collectee par
infrastructure/network/httpx_tls_prober.py (seul le nom du cipher, premier
element du tuple retourne par ssl.SSLSocket.cipher(), est conserve)."""
