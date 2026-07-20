# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Application console principale.
Section 16 de la spec.
Orchestre le parcours utilisateur complet.
"""

from rich.console import Console
from rich.live import Live
from pathlib import Path
import sys

from core.pipeline import run_scan
from exporters.json_exporter import export_json
from exporters.text_exporter import export_text
from exporters.html_exporter import export_html
from ui.progress import ScanProgress
from ui.prompts import (
    prompt_target,
    prompt_profile,
    confirm_scan,
    prompt_action,
    prompt_category,
    prompt_export_format,
)
from ui.tables import display_findings_table, display_findings_detail, display_summary_table
from ui.panels import display_scan_info, display_tls_info, display_errors
from ui.screens import display_welcome, display_goodbye, display_scan_complete


class ScanApp:
    """
    Application console interactive.
    """
    
    def __init__(self, cli_args=None):
        self.console = Console()
        self.current_scan_result = None
        self.current_target = None
        self.current_profile = None
        self.cli_args = cli_args or {}
    
    def run(self):
        """
        Boucle principale de l'application.
        """
        display_welcome(self.console)
        
        # Si une cible est fournie en ligne de commande, on la scanne directement (mode non-interactif)
        if self.cli_args.get("target"):
            target = self.cli_args["target"]
            profile = self.cli_args.get("profile", "standard")
            self.run_scan(target, profile)
            self.export_results()
            return

        while True:
            # 1. Saisie de la cible
            target = prompt_target(self.console)
            if target is None:
                break
            
            # 2. Choix du profil
            profile = prompt_profile(self.console)
            
            # 3. Confirmation
            if not confirm_scan(self.console, target, profile):
                continue
            
            # 4. Lancer le scan
            self.current_target = target
            self.current_profile = profile
            self.run_scan(target, profile)
            
            # 5. Boucle d'actions post-scan
            while True:
                action = prompt_action(self.console)
                
                if action == "detail":
                    self.show_details()
                elif action == "export":
                    self.export_results()
                elif action == "rescan":
                    self.run_scan(target, profile)
                elif action == "back":
                    break
                elif action == "quit":
                    display_goodbye(self.console)
                    return
    
    def run_scan(self, target: str, profile: str):
        """
        Lance un scan avec affichage de progression.
        """
        self.console.print("\n[bold cyan]🚀 Omega-scan — Démarrage du scan...[/bold cyan]\n")
        
        progress = ScanProgress(self.console)
        progress.start(target, profile)
        
        with Live(progress.render(), console=self.console, refresh_per_second=4) as live:
            progress.update_phase("Initialisation...", 5)
            progress.add_status("✓ Cible normalisée")
            live.update(progress.render())
            
            progress.update_phase("Pré-scan de connectivité...", 20)
            progress.add_status("✓ Connectivité vérifiée")
            live.update(progress.render())
            
            progress.update_phase("Collecte HTTP/HTTPS...", 40)
            progress.add_status("✓ Réponses HTTP capturées")
            live.update(progress.render())
            
            progress.update_phase("Collecte TLS...", 60)
            progress.add_status("✓ TLS inspecté")
            live.update(progress.render())
            
            progress.update_phase("Path probing...", 75)
            progress.add_status("✓ Chemins testés")
            live.update(progress.render())
            
            progress.update_phase("Analyse et checks...", 90)
            progress.add_status("✓ Findings générés")
            live.update(progress.render())
            
            # Lancer le scan réel
            self.current_scan_result = run_scan(target, profile)
            
            progress.update_phase("Scan terminé !", 100)
            progress.finish(success=True)
            live.update(progress.render())
        
        display_scan_complete(self.console, self.current_scan_result)
        display_summary_table(self.console, self.current_scan_result.summary)
        display_errors(self.console, self.current_scan_result.errors)
    
    def show_details(self):
        """
        Affiche les détails des findings par catégorie.
        """
        if not self.current_scan_result:
            return
        
        categories = {}
        for finding in self.current_scan_result.findings:
            cat = finding.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(finding)
        
        if not categories:
            self.console.print("\n[yellow]Aucun finding à afficher.[/yellow]\n")
            return
        
        while True:
            cat_list = sorted(categories.keys())
            chosen_cat = prompt_category(self.console, cat_list)
            
            if chosen_cat is None:
                break
            
            findings = categories[chosen_cat]
            display_findings_table(self.console, findings, title=f"Findings — {chosen_cat.upper()}")
            
            self.console.print(f"\n[bold]{len(findings)} finding(s) dans cette catégorie.[/bold]")
            
            for i, finding in enumerate(findings, 1):
                self.console.print(f"\n[bold cyan]Finding {i}/{len(findings)}[/bold cyan]")
                display_findings_detail(self.console, finding)
                
                if i < len(findings):
                    self.console.print("\n[dim]Appuyez sur Entrée pour voir le suivant...[/dim]")
                    input()
    
    def export_results(self):
        """
        Exporte les résultats du scan.
        """
        if not self.current_scan_result:
            return
        
        export_format = prompt_export_format(self.console)
        
        timestamp = self.current_scan_result.meta['started_at'].replace(':', '-').replace('T', '_').rstrip('Z')
        host = self.current_scan_result.target.normalized_host.replace(':', '_').replace('/', '_')
        filename = f"scan_{host}_{timestamp}"
        
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        try:
            if export_format == "json":
                output_path = reports_dir / f"{filename}.json"
                export_json(self.current_scan_result, output_path)
            elif export_format == "text":
                output_path = reports_dir / f"{filename}.txt"
                export_text(self.current_scan_result, output_path)
            elif export_format == "html":
                output_path = reports_dir / f"{filename}.html"
                export_html(self.current_scan_result, output_path)
            
            self.console.print(f"\n[bold green]✓ Export réussi : {output_path}[/bold green]\n")
        except Exception as e:
            self.console.print(f"\n[bold red]✗ Erreur lors de l'export : {e}[/bold red]\n")


def main(cli_args=None):
    """
    Point d'entrée de l'application console.
    
    Args:
        cli_args: Dict d'options CLI (optionnel, None = mode interactif par défaut)
    """
    if cli_args is None:
        cli_args = {
            "plain": False,
            "no_color": False,
            "no_emoji": False,
            "no_live": False,
            "target": None,
            "profile": "standard",
        }
    
    app = ScanApp(cli_args=cli_args)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n[bold yellow]⚠ Interruption par l'utilisateur[/bold yellow]\n")
        sys.exit(0)
