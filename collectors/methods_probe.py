# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Test des méthodes HTTP.
Section 13 de la spec.
Règle d'or : fait du réseau, n'interprète jamais.
"""

import httpx
from typing import List, Dict, Any

from models.target import Target
from config.profiles import ScanProfile
from core.errors import ScanError, build_error_from_exception
from core.logger import get_logger


def probe_methods(
    target: Target,
    profile: ScanProfile,
    http_data: Dict[str, Any],
    errors: List[ScanError],
) -> Dict[str, Any]:
    """
    Teste les méthodes HTTP configurées dans le profil.
    """
    logger = get_logger()
    logger.info(f"[METHODS_PROBE] Début du test des méthodes HTTP pour {target.normalized_host}")
    
    result = {
        "methods_tested": [],
    }
    
    preferred_scheme = http_data.get("overview", {}).get("preferred_scheme")
    if not preferred_scheme:
        logger.warning("[METHODS_PROBE] Aucun schéma préféré, test des méthodes annulé")
        return result
        
    base_url = http_data.get(preferred_scheme, {}).get("final_url")
    if not base_url:
        logger.warning("[METHODS_PROBE] Pas d'URL finale, test des méthodes annulé")
        return result
        
    methods_to_test = profile.http_methods_tested
    
    # Correction : fournir les 4 paramètres du timeout httpx
    timeout = httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )
    
    for method in methods_to_test:
        logger.debug(f"[METHODS_PROBE] Test de la méthode {method} sur {base_url}")
        method_result = {
            "method": method,
            "status_code": None,
            "reason": "not_tested",
            "allow_header": None,
        }
        
        try:
            with httpx.Client(
                timeout=timeout,
                follow_redirects=False,
                verify=False,
            ) as client:
                response = client.request(
                    method,
                    base_url,
                    headers={"User-Agent": profile.user_agent},
                )
                
                method_result["status_code"] = response.status_code
                
                if response.status_code == 405:
                    method_result["reason"] = "disabled"
                elif response.status_code == 501:
                    method_result["reason"] = "not_implemented"
                elif response.status_code in (401, 403):
                    method_result["reason"] = "protected"
                elif 200 <= response.status_code < 300:
                    method_result["reason"] = "enabled"
                else:
                    method_result["reason"] = "unknown"
                    
                if method == "OPTIONS" and "allow" in response.headers:
                    method_result["allow_header"] = response.headers["allow"]
                    
        except Exception as e:
            method_result["reason"] = "error"
            errors.append(
                build_error_from_exception(
                    e,
                    module="methods_probe",
                    phase="methods_probe",
                    related_target=target.input_raw,
                    fatal=False,
                )
            )
            
        result["methods_tested"].append(method_result)
        
    logger.info(f"[METHODS_PROBE] Fin du test des méthodes : {len(result['methods_tested'])} méthodes testées")
    return result
