# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Affichage des findings en tableaux.
Section 16 de la spec.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict, Any


def display_findings_table(console: Console, findings: List[Any], title: str = "Findings"):
    """
    Affiche les findings dans un tableau compact.
    """
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Statut", style="cyan", width=8)
    table.add_column("Sévérité", style="yellow", width=10)
    table.add_column("Règle", style="green", width=20)
    table.add_column("Titre", style="white")
    
    for finding in findings:
        status = finding.status
        severity = finding.severity.upper()
        rule_id = finding.rule_id
        title_text = finding.title
        
        # Colorer les statuts
        if status == "FAIL":
            status_str = f"[bold red]{status}[/bold red]"
        elif status == "WARN":
            status_str = f"[bold yellow]{status}[/bold yellow]"
        elif status == "OK":
            status_str = f"[bold green]{status}[/bold green]"
        else:
            status_str = f"[dim]{status}[/dim]"
        
        table.add_row(status_str, severity, rule_id, title_text)
    
    console.print(table)


def display_findings_detail(console: Console, finding: Any):
    """
    Affiche le détail complet d'un finding.
    """
    # Couleur selon le statut
    if finding.status == "FAIL":
        border_style = "red"
    elif finding.status == "WARN":
        border_style = "yellow"
    elif finding.status == "OK":
        border_style = "green"
    else:
        border_style = "blue"
    
    content = []
    content.append(f"[bold]Règle :[/bold] {finding.rule_id}")
    content.append(f"[bold]Catégorie :[/bold] {finding.category}")
    content.append(f"[bold]Statut :[/bold] {finding.status}")
    content.append(f"[bold]Sévérité :[/bold] {finding.severity.upper()}")
    content.append(f"[bold]Confiance :[/bold] {finding.confidence}")
    content.append(f"[bold]Applicabilité :[/bold] {finding.applicability}")
    content.append("")
    content.append(f"[bold]Description :[/bold]")
    content.append(finding.description)
    content.append("")
    
    if finding.impact:
        content.append(f"[bold]Impact :[/bold]")
        content.append(finding.impact)
        content.append("")
    
    if finding.remediation:
        content.append(f"[bold]Action recommandée :[/bold]")
        content.append(finding.remediation)
        content.append("")
    
    if finding.evidence:
        content.append(f"[bold]Preuve :[/bold]")
        content.append(f"  Type : {finding.evidence.type}")
        content.append(f"  Valeur : {finding.evidence.value}")
        if finding.evidence.source:
            content.append(f"  Source : {finding.evidence.source}")
        if finding.evidence.excerpt:
            content.append(f"  Extrait : {finding.evidence.excerpt[:100]}...")
        content.append("")
    
    if finding.location:
        content.append(f"[bold]Localisation :[/bold]")
        content.append(f"  URL : {finding.location.get('url', 'N/A')}")
        content.append(f"  Composant : {finding.location.get('component', 'N/A')}")
    
    console.print(Panel(
        "\n".join(content),
        title=finding.title,
        border_style=border_style,
    ))


def display_summary_table(console: Console, summary: Any):
    """
    Affiche le résumé du scan.
    """
    table = Table(title="📊 Résumé du scan", show_header=False, box=None)
    table.add_column("Métrique", style="cyan", width=25)
    table.add_column("Valeur", style="white")
    
    table.add_row("Note globale", f"[bold]{summary.overall_rating}[/bold]")
    table.add_row("Statut", summary.scan_status)
    table.add_row("Checks totaux", str(summary.checks_total))
    table.add_row("Findings (WARN+FAIL)", str(summary.findings_total))
    table.add_row("", "")
    
    # Ventilation par statut
    table.add_row("[bold]Ventilation par statut[/bold]", "")
    for status, count in summary.status_breakdown.items():
        if count > 0:
            table.add_row(f"  {status}", str(count))
    
    table.add_row("", "")
    
    # Ventilation par sévérité
    if summary.findings_total > 0:
        table.add_row("[bold]Ventilation par sévérité[/bold]", "")
        for severity, count in summary.severity_breakdown.items():
            if count > 0:
                table.add_row(f"  {severity.upper()}", str(count))
    
    console.print(table)
    
    # Top issues
    if summary.top_issues:
        console.print("\n[bold cyan]🔥 Principaux problèmes :[/bold cyan]")
        for i, issue in enumerate(summary.top_issues, 1):
            console.print(f"  {i}. {issue}")
    
    console.print(f"\n[bold]{summary.short_message}[/bold]\n")
