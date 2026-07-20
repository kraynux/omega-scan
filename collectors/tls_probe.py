# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Collecte TLS, certificat, SNI, multi-vhost.
Section 9.6 et 7.3 de la spec.
Règle d'or : fait du réseau, n'interprète jamais.
"""

import socket
import ssl
from typing import Dict, Any, List, Optional
from datetime import datetime

from models.target import Target
from config.profiles import ScanProfile
from core.errors import ScanError, build_error_from_exception
from core.logger import get_logger


def _extract_san(cert_dict: Dict[str, Any]) -> List[str]:
    """Extrait les Subject Alternative Names du certificat décodé."""
    san = []
    for type_name, value in cert_dict.get("subjectAltName", []):
        san.append(f"{type_name}:{value}")
    return san


def _parse_cert_date(date_str: str) -> Optional[str]:
    """
    Parse une date de certificat au format 'Mon DD HH:MM:SS YYYY GMT'.
    Retourne ISO 8601 UTC ou None si parsing échoue.
    """
    try:
        date_str = " ".join(date_str.split())
        dt = datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z")
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return None


def _check_hostname_match(
    cert_dict: Dict[str, Any],
    expected_host: str,
) -> bool:
    """Vérifie si le certificat correspond au hostname attendu (CN ou SAN)."""
    if not cert_dict:
        return False
    
    subject = cert_dict.get("subject", ())
    cn = None
    for rdn in subject:
        for attr_type, attr_value in rdn:
            if attr_type == "commonName":
                cn = attr_value
                break
    
    san_list = _extract_san(cert_dict)
    hosts_to_check = [cn] if cn else []
    hosts_to_check.extend([s.split(":", 1)[1] for s in san_list if s.startswith("DNS:")])
    
    for host in hosts_to_check:
        if host == expected_host:
            return True
        if host.startswith("*.") and expected_host.endswith(host[2:]):
            return True
    
    return False


def probe_tls(
    target: Target,
    profile: ScanProfile,
    errors: List[ScanError],
) -> Dict[str, Any]:
    """
    Collecte TLS complète.
    Section 9.6 de la spec.
    """
    logger = get_logger()
    logger.info(f"[TLS_PROBE] Début de la collecte TLS pour {target.normalized_host}")
    
    tls_data = {
        "attempted": False,
        "handshake_success": False,
        "tls_version": None,
        "cipher": None,
        "certificate_present": False,
        "certificate_subject": None,
        "certificate_issuer": None,
        "certificate_san": [],
        "not_before": None,
        "not_after": None,
        "hostname_match": False,
        "validation_error": None,
        "self_signed": False,
        "sni_hostname_sent": None,
        "notes": "",
    }
    
    if not profile.tls_checks_enabled:
        logger.info("[TLS_PROBE] TLS désactivé par le profil")
        tls_data["notes"] = "TLS désactivé par le profil"
        return tls_data
    
    tls_host = target.normalized_host
    tls_port = target.requested_port if target.requested_port else 443
    sni_hostname = tls_host if target.target_kind == "hostname" else None
    tls_data["sni_hostname_sent"] = sni_hostname
    tls_data["attempted"] = True
    
    # IMPORTANT : CERT_REQUIRED force Python à parser le certificat.
    # check_hostname = False nous permet de détecter nous-mêmes les mismatchs
    # sans que la connexion ne soit immédiatement coupée par Python.
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED
    
    timeout = profile.timeout_connect
    
    try:
        logger.debug(f"[TLS_PROBE] Connexion à {tls_host}:{tls_port} (SNI: {sni_hostname})")
        sock = socket.create_connection((tls_host, tls_port), timeout=timeout)
        ssl_sock = context.wrap_socket(sock, server_hostname=sni_hostname)
        
        # Si on arrive ici, le handshake a réussi et le certificat est valide (chaîne de confiance OK)
        tls_data["handshake_success"] = True
        tls_data["tls_version"] = ssl_sock.version()
        
        cipher_info = ssl_sock.cipher()
        if cipher_info:
            tls_data["cipher"] = cipher_info[0]
        
        cert_dict = ssl_sock.getpeercert()
        if cert_dict:
            tls_data["certificate_present"] = True
            
            subject = cert_dict.get("subject", ())
            for rdn in subject:
                for attr_type, attr_value in rdn:
                    if attr_type == "commonName":
                        tls_data["certificate_subject"] = attr_value
                        break
            
            issuer = cert_dict.get("issuer", ())
            for rdn in issuer:
                for attr_type, attr_value in rdn:
                    if attr_type == "commonName":
                        tls_data["certificate_issuer"] = attr_value
                        break
            
            tls_data["certificate_san"] = _extract_san(cert_dict)
            tls_data["not_before"] = _parse_cert_date(cert_dict.get("notBefore"))
            tls_data["not_after"] = _parse_cert_date(cert_dict.get("notAfter"))
            tls_data["hostname_match"] = _check_hostname_match(cert_dict, tls_host)
            
            if tls_data["certificate_subject"] and tls_data["certificate_issuer"]:
                tls_data["self_signed"] = (tls_data["certificate_subject"] == tls_data["certificate_issuer"])
            
            if not tls_data["hostname_match"] and sni_hostname:
                tls_data["notes"] = f"Le certificat ne correspond pas à {sni_hostname}. Possible multi-vhost."
                logger.warning(f"[TLS_PROBE] {tls_data['notes']}")
        
        ssl_sock.close()
        logger.info(f"[TLS_PROBE] TLS OK : version={tls_data['tls_version']}, subject={tls_data['certificate_subject']}")

    except ssl.SSLCertVerificationError as e:
        # Le handshake TLS a fonctionné, mais le certificat est invalide (auto-signé, expiré, etc.)
        logger.warning(f"[TLS_PROBE] Certificat non validé : {e}")
        tls_data["handshake_success"] = True  # Le protocole TLS fonctionne quand même
        tls_data["validation_error"] = str(e)
        tls_data["self_signed"] = "self signed" in str(e).lower() or "self-signed" in str(e).lower()
        tls_data["notes"] = "Certificat présent mais non approuvé par la chaîne de confiance."

    except ssl.SSLError as e:
        # Échec réel du handshake (ex: port 80, protocole obsolète)
        logger.warning(f"[TLS_PROBE] Erreur SSL (handshake échoué) : {e}")
        errors.append(build_error_from_exception(e, module="tls_probe", phase="tls_probe", related_target=target.input_raw, fatal=False))
        tls_data["validation_error"] = str(e)

    except Exception as e:
        logger.warning(f"[TLS_PROBE] Erreur inattendue : {e}")
        errors.append(build_error_from_exception(e, module="tls_probe", phase="tls_probe", related_target=target.input_raw, fatal=False))
        tls_data["validation_error"] = str(e)
    
    return tls_data
