# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Écrans de l'application console.
Section 16 de la spec.
"""

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from typing import Optional, Any


def display_welcome(console: Console):
    """
    Écran d'accueil.
    """
    welcome_text = """
    
[bold cyan]🔒 Omega-scan — Scanner de Posture de Sécurité Web[/bold cyan]
____ _  _ ____ ____ ____    ____ ____ ____ _  _ 
|  | |\/| |___ | __ |__| __ [__  |    |__| |\ | 
|__| |  | |___ |__] |  |    ___] |___ |  | | \| 
                                                
[bold cyan]Analysez rapidement l'hygiène de configuration de vos services HTTP/HTTPS.[/bold cyan]

[bold]Fonctionnalités :[/bold]
  • Vérification transport (HTTPS, HSTS, redirections)
  • Analyse des headers de sécurité (CSP, nosniff, referrer)
  • Détection de chemins sensibles et admin
  • Inspection TLS et certificats
  • Test des méthodes HTTP
  • Détection de fuites d'information

[bold]Profils disponibles :[/bold]
  • quick      — Vérification rapide
  • standard   — Scan complet (recommandé)
  • extended   — Scan approfondi
  • local-lab  — Pour localhost/LAN

[dim]Navigation : chiffres pour les menus, q pour quitter[/dim]
"""
    
    console.print(Panel(
        Align.center(welcome_text),
        title="Bienvenue",
        border_style="cyan",
        padding=(1, 2),
    ))


def display_goodbye(console: Console):
    """
    Écran de sortie.
    """
    console.print("\n[bold cyan]👋 Au revoir ![/bold cyan]\n")


def display_scan_complete(console: Console, scan_result: Any):
    """
    Écran de fin de scan.
    """
    console.print("\n" + "=" * 70)
    console.print("[bold green]✅ Scan terminé[/bold green]")
    console.print("=" * 70 + "\n")
