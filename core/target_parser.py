# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Parser de cible.
Section 2 de la spec.
Normalise toute entrée avant le scan.
"""

import ipaddress
import urllib.parse
import re
from typing import Optional

from models.target import Target
from core.errors import TargetParseError


def _preprocess_ipv6(raw_input: str) -> str:
    """
    Détecte les IPv6 sans crochets et les entoure.
    Gère les formats : 
    - IPv6 pure : "2001:db8::10" → "[2001:db8::10]"
    - IPv6 avec port : "2001:db8::10:8080" → "[2001:db8::10]:8080"
    """
    if '//' in raw_input or raw_input.startswith('['):
        return raw_input
    
    # Compter les ':' pour détecter une possible IPv6
    if raw_input.count(':') < 2:
        return raw_input
    
    # Essayer de parser comme IPv6 pure
    try:
        ipaddress.ip_address(raw_input)
        return f"[{raw_input}]"
    except ValueError:
        pass
    
    # Essayer IPv6:port (dernier ':' sépare le port)
    last_colon = raw_input.rfind(':')
    if last_colon > 0:
        potential_host = raw_input[:last_colon]
        potential_port = raw_input[last_colon+1:]
        try:
            ipaddress.ip_address(potential_host)
            port_num = int(potential_port)
            if 1 <= port_num <= 65535:
                return f"[{potential_host}]:{port_num}"
        except (ValueError, TypeError):
            pass
    
    return raw_input


def _needs_scheme_prefix(raw_input: str) -> bool:
    """
    Détecte si l'entrée a besoin d'un préfixe '//' pour être correctement parsée.
    Cas : hostname:port/chemin sans schéma (ex: "intranet.lan:8080/admin")
    """
    # Si déjà un schéma ou un '//', pas besoin
    if '://' in raw_input or raw_input.startswith('//'):
        return False
    
    # Pattern : quelque_chose:chiffres/... (sans schéma)
    # Ex: "intranet.lan:8080/admin", "example.org:443/api"
    pattern = r'^[^:/]+:\d+(/|$)'
    if re.match(pattern, raw_input):
        return True
    
    return False


def parse_target(raw_input: str) -> Target:
    """
    Parse et normalise une cible brute en objet Target canonique.
    Lève TargetParseError si l'entrée est invalide.
    """
    raw_input = raw_input.strip()
    if not raw_input:
        raise TargetParseError("L'entrée cible est vide.")

    # Pré-traiter les IPv6 sans crochets
    raw_input = _preprocess_ipv6(raw_input)

    # Détecter si on doit ajouter '//' devant (cas hostname:port sans schéma)
    if _needs_scheme_prefix(raw_input):
        raw_input = f"//{raw_input}"

    # 1. Parsing URL
    parsed = urllib.parse.urlparse(raw_input)
    
    # Si toujours pas de netloc après le préfixe '//', essayer à nouveau
    if not parsed.scheme and not parsed.netloc:
        parsed = urllib.parse.urlparse(f"//{raw_input}")

    scheme = parsed.scheme.lower() if parsed.scheme else None
    netloc = parsed.netloc
    host = parsed.hostname
    port = parsed.port
    path = parsed.path if parsed.path else "/"

    if not host:
        raise TargetParseError(f"Impossible d'extraire un hôte valide de : {raw_input}")

    # 2. Classification target_kind et propriétés IP
    is_ip = False
    ip_version = None
    is_private = False
    is_loopback = False
    is_link_local = False
    is_global = False
    scope_kind = "hostname"
    target_kind = "hostname"

    try:
        clean_host = host.strip("[]")
        ip_obj = ipaddress.ip_address(clean_host)
        is_ip = True
        ip_version = ip_obj.version
        is_private = ip_obj.is_private
        is_loopback = ip_obj.is_loopback
        is_link_local = ip_obj.is_link_local
        is_global = ip_obj.is_global

        target_kind = "ipv4" if ip_version == 4 else "ipv6"

        # Classification scope_kind (taxonomie fermée de la spec)
        if is_loopback:
            scope_kind = "loopback"
        elif is_link_local:
            scope_kind = "link_local"
        elif is_private:
            # Distinction fine entre private_lan (RFC1918/ULA) et special_non_global (CGNAT, etc.)
            is_rfc1918 = (
                ip_obj in ipaddress.ip_network("10.0.0.0/8") or
                ip_obj in ipaddress.ip_network("172.16.0.0/12") or
                ip_obj in ipaddress.ip_network("192.168.0.0/16") or
                ip_obj in ipaddress.ip_network("fc00::/7")
            )
            scope_kind = "private_lan" if is_rfc1918 else "special_non_global"
        elif is_global:
            scope_kind = "public"
        else:
            # Cas CGNAT (100.64.0.0/10), multicast, réservé, benchmarking, etc.
            scope_kind = "special_non_global"

    except ValueError:
        # Ce n'est pas une IP, c'est un hostname
        target_kind = "hostname"
        scope_kind = "hostname"

    # 3. Normalisation des URLs
    def build_url(sch: str, nloc: str, pth: str) -> str:
        return f"{sch}://{nloc}{pth}"

    normalized_url_http = build_url("http", netloc, path)
    normalized_url_https = build_url("https", netloc, path)

    # 4. Détermination du mode de scan
    if scheme == "http":
        scan_modes = "http"
    elif scheme == "https":
        scan_modes = "https"
    else:
        scan_modes = "both"

    # 5. Construction de l'objet Target
    return Target(
        input_raw=raw_input,
        normalized_host=host,
        normalized_url_http=normalized_url_http,
        normalized_url_https=normalized_url_https,
        requested_scheme=scheme,
        requested_port=port,
        requested_path=path,
        target_kind=target_kind,
        scope_kind=scope_kind,
        scan_modes=scan_modes,
        is_ip=is_ip,
        ip_version=ip_version,
        is_private=is_private,
        is_loopback=is_loopback,
        is_link_local=is_link_local,
        is_global=is_global,
    )
