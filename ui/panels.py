# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Panneaux d'information pour l'affichage console.
Section 16 de la spec.
"""

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from typing import Any


def display_scan_info(console: Console, scan_result: Any):
    """
    Affiche les informations principales du scan.
    """
    layout = Layout()
    layout.split_row(
        Layout(name="target", ratio=1),
        Layout(name="connectivity", ratio=1),
    )
    
    # Panneau cible
    target_info = []
    target_info.append(f"[bold]Host :[/bold] {scan_result.target.normalized_host}")
    target_info.append(f"[bold]Type :[/bold] {scan_result.target.target_kind}")
    target_info.append(f"[bold]Scope :[/bold] {scan_result.target.scope_kind}")
    target_info.append(f"[bold]Profil :[/bold] {scan_result.scan_profile['profile_name']}")
    
    layout["target"].update(Panel(
        "\n".join(target_info),
        title="🎯 Cible",
        border_style="cyan",
    ))
    
    # Panneau connectivité
    conn = scan_result.connectivity
    conn_info = []
    conn_info.append(f"[bold]DNS :[/bold] {'Résolu' if conn['dns_resolution_attempted'] else 'Non tenté'}")
    conn_info.append(f"[bold]HTTP :[/bold] {'✓' if conn['http_reachable'] else '✗'}")
    conn_info.append(f"[bold]HTTPS :[/bold] {'✓' if conn['https_reachable'] else '✗'}")
    
    if conn['latency_overview_ms']:
        conn_info.append(f"[bold]Latence :[/bold] {conn['latency_overview_ms']}ms")
    
    layout["connectivity"].update(Panel(
        "\n".join(conn_info),
        title="🌐 Connectivité",
        border_style="green",
    ))
    
    console.print(layout)


def display_tls_info(console: Console, tls_data: dict):
    """
    Affiche les informations TLS si disponibles.
    """
    if not tls_data.get('attempted'):
        return
    
    tls_info = []
    tls_info.append(f"[bold]Handshake :[/bold] {'✓ Réussi' if tls_data['handshake_success'] else '✗ Échoué'}")
    
    if tls_data.get('tls_version'):
        tls_info.append(f"[bold]Version :[/bold] {tls_data['tls_version']}")
    
    if tls_data.get('cipher'):
        tls_info.append(f"[bold]Cipher :[/bold] {tls_data['cipher']}")
    
    if tls_data.get('certificate_subject'):
        tls_info.append(f"[bold]Sujet :[/bold] {tls_data['certificate_subject']}")
    
    if tls_data.get('certificate_issuer'):
        tls_info.append(f"[bold]Émetteur :[/bold] {tls_data['certificate_issuer']}")
    
    tls_info.append(f"[bold]Hostname match :[/bold] {'✓' if tls_data.get('hostname_match') else '✗'}")
    
    if tls_data.get('self_signed'):
        tls_info.append(f"[bold yellow]⚠ Auto-signé[/bold yellow]")
    
    if tls_data.get('validation_error'):
        tls_info.append(f"[bold red]Erreur :[/bold red] {tls_data['validation_error']}")
    
    console.print(Panel(
        "\n".join(tls_info),
        title="🔐 TLS",
        border_style="blue",
    ))


def display_errors(console: Console, errors: list):
    """
    Affiche les erreurs du scan.
    """
    if not errors:
        return
    
    console.print("\n[bold red]⚠️  Erreurs rencontrées :[/bold red]")
    for error in errors:
        fatal_marker = " [bold red][FATAL][/bold red]" if error.get('fatal') else ""
        console.print(f"  • [{error['module']}] {error['error_type']}: {error['message']}{fatal_marker}")
    console.print()
