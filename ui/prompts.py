# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Saisies utilisateur et menus interactifs.
Section 16 de la spec.
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from typing import Optional, List


def prompt_target(console: Console) -> Optional[str]:
    """
    Demande la cible à scanner.
    Retourne None si l'utilisateur veut quitter.
    """
    console.print("\n[bold cyan]🎯 Saisie de la cible[/bold cyan]")
    console.print("Formats acceptés : IPv4, IPv6, hostname, URL complète")
    console.print("Exemples : 192.168.1.10, example.org, https://example.org/admin\n")
    
    target = Prompt.ask(
        "[bold]Cible[/bold] (ou [bold cyan]'q'[/bold cyan] pour quitter)",
        default="",
    )
    
    if target.lower() in ('q', 'quit', 'exit'):
        return None
    
    return target.strip()


def prompt_profile(console: Console) -> str:
    """
    Demande le profil de scan.
    """
    console.print("\n[bold cyan]⚙️  Choix du profil[/bold cyan]")
    console.print("  [bold cyan]\\[1][/]  quick      — Vérification rapide (transport/headers uniquement)")
    console.print("  [bold cyan]\\[2][/]  standard   — Scan complet (recommandé)")
    console.print("  [bold cyan]\\[3][/]  extended   — Scan approfondi (plus long)")
    console.print("  [bold cyan]\\[4][/]  local-lab  — Pour localhost/LAN (tolérant)")
    console.print()
    
    choice = Prompt.ask(
        "[bold]Profil[/bold]",
        choices=["1", "2", "3", "4"],
        default="2",
    )
    
    profiles = {
        "1": "quick",
        "2": "standard",
        "3": "extended",
        "4": "local-lab",
    }
    
    return profiles[choice]


def confirm_scan(console: Console, target: str, profile: str) -> bool:
    """
    Demande confirmation avant de lancer le scan.
    """
    console.print("\n[bold cyan]✅ Confirmation[/bold cyan]")
    console.print(f"  Cible  : [bold]{target}[/bold]")
    console.print(f"  Profil : [bold]{profile}[/bold]")
    console.print()
    
    return Confirm.ask("[bold]Lancer le scan ?[/bold]", default=True)


def prompt_action(console: Console) -> str:
    """
    Demande l'action après le scan.
    Retourne : 'detail', 'export', 'rescan', 'back', 'quit'
    """
    console.print("\n[bold cyan]📋 Actions disponibles[/bold cyan]\n")
    console.print("  [bold cyan]\\[d][/]  Détail par catégorie")
    console.print("  [bold cyan]\\[e][/]  Exporter les résultats")
    console.print("  [bold cyan]\\[r][/]  Relancer le scan")
    console.print("  [bold cyan]\\[b][/]  Retour au menu principal")
    console.print("  [bold cyan]\\[q][/]  Quitter")
    console.print()
    
    choice = Prompt.ask(
        "[bold]Action[/bold]",
        choices=["d", "e", "r", "b", "q"],
        default="d",
    )
    
    actions = {
        "d": "detail",
        "e": "export",
        "r": "rescan",
        "b": "back",
        "q": "quit",
    }
    
    return actions[choice]


def prompt_category(console: Console, categories: List[str]) -> Optional[str]:
    """
    Demande quelle catégorie de findings afficher.
    """
    console.print("\n[bold cyan]📂 Catégories disponibles[/bold cyan]\n")
    for i, cat in enumerate(categories, 1):
        console.print(f"  [bold cyan]\\[{i}][/]  {cat}")
    console.print("  [bold cyan]\\[b][/]  Retour")
    console.print()
    
    choice = Prompt.ask(
        "[bold]Catégorie[/bold]",
        choices=[str(i) for i in range(1, len(categories) + 1)] + ["b"],
    )
    
    if choice == "b":
        return None
    
    return categories[int(choice) - 1]


def prompt_export_format(console: Console) -> str:
    """
    Demande le format d'export.
    """
    console.print("\n[bold cyan]💾 Format d'export[/bold cyan]\n")
    console.print("  [bold cyan]\\[1][/]  JSON   — Source de vérité complète")
    console.print("  [bold cyan]\\[2][/]  Texte  — Rapport humain compact")
    console.print("  [bold cyan]\\[3][/]  HTML   — Rapport web lisible")
    console.print()
    
    choice = Prompt.ask(
        "[bold]Format[/bold]",
        choices=["1", "2", "3"],
        default="1",
    )
    
    formats = {
        "1": "json",
        "2": "text",
        "3": "html",
    }
    
    return formats[choice]
