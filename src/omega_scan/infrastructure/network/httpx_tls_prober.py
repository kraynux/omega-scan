# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Implementation du port TlsProber (certificat, SNI, hostname match).

Nommee "httpx_" par coherence avec les autres probers de ce paquet, meme si
la collecte TLS elle-meme passe par `socket`/`ssl` standard (httpx ne
donne pas acces au certificat brut) : `httpx` reste le point d'entree
reseau principal du paquet, ce module en est un complement technique."""
from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone
from typing import Any, cast

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.scans.models import ScanError
from omega_scan.domain.targets.models import Target
from omega_scan.infrastructure.exceptions import build_error_from_exception
from omega_scan.infrastructure.logging.app_logger import get_logger
from omega_scan.shared.i18n import N_, _, log_text


def _extract_san(cert_dict: dict[str, Any]) -> list[str]:
    return [f"{type_name}:{value}" for type_name, value in cert_dict.get("subjectAltName", [])]


def _parse_cert_date(date_str: str | None) -> str | None:
    if date_str is None:
        return None
    try:
        date_str = " ".join(date_str.split())
        # Les certificats X.509 expriment toujours notBefore/notAfter en GMT
        # (RFC 5280) : %Z ne peuple pas tzinfo (naive), on l'attache nous-memes.
        dt = datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return None


def _check_hostname_match(cert_dict: dict[str, Any], expected_host: str) -> bool:
    if not cert_dict:
        return False

    subject = cert_dict.get("subject", ())
    cn = None
    for rdn in subject:
        for attr_type, attr_value in rdn:
            if attr_type == "commonName":
                cn = attr_value
                break

    hosts_to_check = [cn] if cn else []
    hosts_to_check.extend(s.split(":", 1)[1] for s in _extract_san(cert_dict) if s.startswith("DNS:"))

    for host in hosts_to_check:
        if host == expected_host:
            return True
        if host.startswith("*.") and expected_host.endswith(host[2:]):
            return True
    return False


class HttpxTlsProber:
    """Implemente ports/tls_prober.py::TlsProber."""

    def probe(
        self,
        target: Target,
        profile: ScanProfile,
        errors: list[ScanError],
    ) -> dict[str, Any]:
        logger = get_logger()
        logger.info(log_text(N_("[TLS_PROBE] Début de la collecte TLS pour {normalized_host}"), normalized_host=target.normalized_host))

        tls_data: dict[str, Any] = {
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
            logger.info(N_("[TLS_PROBE] TLS désactivé par le profil"))
            tls_data["notes"] = _("TLS désactivé par le profil")
            return tls_data

        tls_host = target.normalized_host
        tls_port = target.requested_port if target.requested_port else 443
        sni_hostname = tls_host if target.target_kind == "hostname" else None
        tls_data["sni_hostname_sent"] = sni_hostname
        tls_data["attempted"] = True

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED

        timeout = profile.timeout_connect

        try:
            logger.debug(log_text(N_("[TLS_PROBE] Connexion à {tls_host}:{tls_port} (SNI: "
                                     "{sni_hostname})"), tls_host=tls_host, tls_port=tls_port, sni_hostname=sni_hostname))
            sock = socket.create_connection((tls_host, tls_port), timeout=timeout)
            ssl_sock = context.wrap_socket(sock, server_hostname=sni_hostname)

            tls_data["handshake_success"] = True
            tls_data["tls_version"] = ssl_sock.version()

            cipher_info = ssl_sock.cipher()
            if cipher_info:
                tls_data["cipher"] = cipher_info[0]

            # getpeercert() : le typeshed de ssl ne distingue pas le type par cle
            # (subject/issuer sont des tuples imbriques, notBefore/notAfter des
            # str) et .get() en retourne l'union complete plutot que le type
            # exact de chaque cle — cast() vers dict[str, Any], deja traite
            # defensivement ci-dessous (.get(), isinstance implicite via les
            # helpers _extract_san/_parse_cert_date/_check_hostname_match).
            cert_dict = cast("dict[str, Any] | None", ssl_sock.getpeercert())
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
                    tls_data["self_signed"] = (
                        tls_data["certificate_subject"] == tls_data["certificate_issuer"]
                    )

                if not tls_data["hostname_match"] and sni_hostname:
                    tls_data["notes"] = (
                        _("Le certificat ne correspond pas à {sni_hostname}. Possible "
                          "multi-vhost.").format(sni_hostname=sni_hostname)
                    )
                    logger.warning(f"[TLS_PROBE] {tls_data['notes']}")

            ssl_sock.close()
            logger.info(
                log_text(N_("[TLS_PROBE] TLS OK : version={tls_version}, "
                            "subject={certificate_subject}"), tls_version=tls_data['tls_version'], certificate_subject=tls_data['certificate_subject'])
            )

        except ssl.SSLCertVerificationError as exc:
            logger.warning(log_text(N_("[TLS_PROBE] Certificat non valide : {exc}"), exc=exc))
            tls_data["handshake_success"] = True
            tls_data["validation_error"] = str(exc)
            tls_data["self_signed"] = (
                "self signed" in str(exc).lower() or "self-signed" in str(exc).lower()
            )
            tls_data["notes"] = _("Certificat présent mais non approuvé par la chaîne de "
                                  "confiance.")

        except ssl.SSLError as exc:
            logger.warning(log_text(N_("[TLS_PROBE] Erreur SSL (handshake échoué) : {exc}"), exc=exc))
            errors.append(
                build_error_from_exception(
                    exc, module="tls_probe", phase="tls_probe",
                    related_target=target.input_raw, fatal=False,
                )
            )
            tls_data["validation_error"] = str(exc)

        except Exception as exc:  # noqa: BLE001 - traduit en ScanError, jamais leve
            logger.warning(log_text(N_("[TLS_PROBE] Erreur inattendue : {exc}"), exc=exc))
            errors.append(
                build_error_from_exception(
                    exc, module="tls_probe", phase="tls_probe",
                    related_target=target.input_raw, fatal=False,
                )
            )
            tls_data["validation_error"] = str(exc)

        return tls_data
