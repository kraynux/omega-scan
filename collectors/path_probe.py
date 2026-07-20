# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Path probing et détection catch-all.
Section 5 et 6 de la spec.
Règle d'or : fait du réseau, n'interprète jamais.
"""

import time
import uuid
from typing import List, Dict, Any
import httpx

from models.target import Target
from config.profiles import ScanProfile
from config.paths import ADMIN_PATHS, SENSITIVE_PATHS, BACKUP_SUFFIXES
from core.errors import ScanError, build_error_from_exception
from core.logger import get_logger
from normalizers.headers import deduce_content_profile


def _generate_probe_token() -> str:
    """Génère un token aléatoire improbable pour le test catch-all."""
    return f"__Omega_scan_probe_{uuid.uuid4().hex[:16]}__"


def _detect_catch_all(
    base_url: str,
    base_content_profile: str,
    profile: ScanProfile,
    errors: List[ScanError],
    target: Target,
) -> bool:
    """
    Détecte le comportement catch-all.
    Section 5.1 de la spec.
    Retourne True si le serveur répond 200 avec le même profil de contenu
    sur un chemin aléatoire improbable.
    """
    logger = get_logger()
    token = _generate_probe_token()
    probe_url = f"{base_url.rstrip('/')}/{token}"
    
    logger.debug(f"[PATH_PROBE] Test catch-all : {probe_url}")
    
    # Correction : fournir les 4 paramètres du timeout httpx
    timeout = httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )
    
    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=False,
            verify=False,  # On observe, on ne juge pas
        ) as client:
            response = client.get(
                probe_url,
                headers={"User-Agent": profile.user_agent},
            )
            
            # Si 200 ET même content_profile que la racine → catch-all
            if response.status_code == 200:
                probe_profile = deduce_content_profile(
                    response.headers.get("content-type"),
                    response.text[:500],
                )
                
                # Catch-all si le profil est identique à celui de la racine
                if probe_profile == base_content_profile and probe_profile != "unknown":
                    logger.warning(f"[PATH_PROBE] Catch-all détecté (même profil : {probe_profile})")
                    return True
                
                # Même si le profil diffère, un 200 sur un token aléatoire est suspect
                logger.warning(f"[PATH_PROBE] Réponse 200 sur chemin improbable (profil: {probe_profile})")
                return True
            
            return False
    
    except Exception as e:
        logger.debug(f"[PATH_PROBE] Test catch-all échoué : {e}")
        errors.append(
            build_error_from_exception(
                e,
                module="path_probe",
                phase="path_probe",
                related_target=target.input_raw,
                related_scheme="https" if "https://" in base_url else "http",
                fatal=False,
            )
        )
        return False


def _probe_single_path(
    url: str,
    path: str,
    profile: ScanProfile,
    errors: List[ScanError],
    target: Target,
) -> Dict[str, Any]:
    """
    Teste un chemin unique et retourne le résultat.
    """
    logger = get_logger()
    full_url = f"{url.rstrip('/')}/{path.lstrip('/')}"
    
    result = {
        "path": path,
        "status_code": None,
        "content_profile": "unknown",
        "reason": "not_tested",
    }
    
    # Correction : fournir les 4 paramètres du timeout httpx
    timeout = httpx.Timeout(
        connect=profile.timeout_connect,
        read=profile.timeout_read,
        write=profile.timeout_connect,
        pool=profile.timeout_connect,
    )
    
    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=False,
            verify=False,
        ) as client:
            response = client.get(
                full_url,
                headers={"User-Agent": profile.user_agent},
            )
            
            result["status_code"] = response.status_code
            
            # Déterminer la raison
            if response.status_code == 200:
                result["reason"] = "ok"
                result["content_profile"] = deduce_content_profile(
                    response.headers.get("content-type"),
                    response.text[:500],
                )
            elif 300 <= response.status_code < 400:
                result["reason"] = "redirect"
            elif response.status_code == 401 or response.status_code == 403:
                result["reason"] = "protected"
            elif response.status_code == 404:
                result["reason"] = "not_found"
            else:
                result["reason"] = f"status_{response.status_code}"
    
    except Exception as e:
        result["reason"] = "error"
        errors.append(
            build_error_from_exception(
                e,
                module="path_probe",
                phase="path_probe",
                related_target=target.input_raw,
                fatal=False,
            )
        )
    
    return result


def probe_paths(
    target: Target,
    profile: ScanProfile,
    http_data: Dict[str, Any],
    errors: List[ScanError],
) -> Dict[str, Any]:
    """
    Exécute le path probing complet.
    Section 5 et 6 de la spec.
    
    Retourne un dict avec :
    - catch_all_suspected : bool
    - path_probe_context : list de {path, status_code, content_profile, reason}
    """
    logger = get_logger()
    logger.info(f"[PATH_PROBE] Début du path probing pour {target.normalized_host}")
    
    result = {
        "catch_all_suspected": False,
        "path_probe_context": [],
    }
    
    # Vérifier si le path probing est activé
    if not profile.path_checks_enabled:
        logger.info("[PATH_PROBE] Path probing désactivé par le profil")
        return result
    
    # Déterminer l'URL de base (schéma préféré)
    overview = http_data.get("overview", {})
    preferred_scheme = overview.get("preferred_scheme")
    
    if not preferred_scheme:
        logger.warning("[PATH_PROBE] Aucun schéma préféré, path probing annulé")
        return result
    
    base_url = http_data.get(preferred_scheme, {}).get("final_url")
    if not base_url:
        logger.warning("[PATH_PROBE] Pas d'URL finale, path probing annulé")
        return result
    
    base_content_profile = overview.get("content_profile", "unknown")
    
    # 1. Détection catch-all
    logger.info("[PATH_PROBE] Test catch-all...")
    result["catch_all_suspected"] = _detect_catch_all(
        base_url,
        base_content_profile,
        profile,
        errors,
        target,
    )
    
    if result["catch_all_suspected"]:
        logger.warning("[PATH_PROBE] Catch-all détecté, les findings de path probing auront une confiance dégradée")
    
    # 2. Tester les chemins sensibles et admin
    paths_to_test = ADMIN_PATHS + SENSITIVE_PATHS
    
    # Limiter au max_targets du profil
    if profile.path_probe_max_targets > 0:
        paths_to_test = paths_to_test[:profile.path_probe_max_targets]
    
    logger.info(f"[PATH_PROBE] Test de {len(paths_to_test)} chemins...")
    
    for i, path in enumerate(paths_to_test):
        # Throttling
        if i > 0 and profile.path_probe_delay_ms > 0:
            time.sleep(profile.path_probe_delay_ms / 1000.0)
        
        probe_result = _probe_single_path(
            base_url,
            path,
            profile,
            errors,
            target,
        )
        
        # Si catch-all détecté, marquer tous les "ok" comme suspects
        if result["catch_all_suspected"] and probe_result["reason"] == "ok":
            probe_result["reason"] = "catch_all_suspected"
        
        result["path_probe_context"].append(probe_result)
    
    # Compter les résultats intéressants
    interesting = [p for p in result["path_probe_context"] if p["reason"] in ("ok", "protected", "catch_all_suspected")]
    logger.info(f"[PATH_PROBE] Fin : {len(result['path_probe_context'])} chemins testés, {len(interesting)} intéressants")
    
    return result
