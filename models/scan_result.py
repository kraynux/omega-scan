# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Objet ScanResult (section 9 de la spec).
Structure complète du résultat de scan, strictement JSON-serializable.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime

from models.target import Target
from models.finding import Finding
from models.summary import Summary


@dataclass
class ScanResult:
    """Résultat complet d'un scan."""
    
    # 9.1 meta
    meta: Dict[str, Any]  # scan_id, scanner_name, scanner_version, started_at, finished_at, duration_ms, host_machine, operator_mode, export_targets
    
    # 9.2 target
    target: Target
    
    # 9.3 scan_profile
    scan_profile: Dict[str, Any]  # profile_name, follow_redirects, timeout_connect, timeout_read, http_methods_tested, path_checks_enabled, tls_checks_enabled, max_redirects, user_agent, path_probe_delay_ms, path_probe_max_targets, external_tools_used
    
    # 9.4 connectivity
    connectivity: Dict[str, Any]  # dns_resolution_attempted, resolved_addresses, preferred_address, http_reachable, https_reachable, ports_tested, reachable_ports, first_successful_scheme, latency_overview_ms, connection_notes, failure_category
    
    # 9.5 http
    http: Dict[str, Any]  # overview, http, https (chacun avec attempted, requested_url, final_url, status_code, reason, ok, elapsed_ms, content_type, content_length, headers, cookies, redirect_chain, request, body_preview, error, catch_all_suspected, proxy_suspected, content_profile, path_probe_context)
    
    # 9.6 tls
    tls: Dict[str, Any]  # attempted, handshake_success, tls_version, cipher, certificate_present, certificate_subject, certificate_issuer, certificate_san, not_before, not_after, hostname_match, validation_error, self_signed, sni_hostname_sent, notes
    
    # 9.7 findings
    findings: List[Finding]
    
    # 9.8 summary
    summary: Summary
    
    # 9.9 errors
    errors: List[Dict[str, Any]]  # module, phase, error_type, message, fatal, related_target, related_scheme, failure_category
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire JSON-serializable."""
        result = {
            "meta": self.meta,
            "target": self.target.to_dict(),
            "scan_profile": self.scan_profile,
            "connectivity": self.connectivity,
            "http": self.http,
            "tls": self.tls,
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.summary.to_dict(),
            "errors": self.errors,
        }
        return result
