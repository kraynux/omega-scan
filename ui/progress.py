# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Barre de progression et affichage du statut pendant le scan.
Section 16 de la spec.
"""

from rich.progress import Progress, TaskID, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from typing import Optional


class ScanProgress:
    """
    Affichage de la progression du scan.
    Une barre globale + 3-6 lignes de statut maximum.
    """
    
    def __init__(self, console: Console):
        self.console = console
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )
        self.task_id: Optional[TaskID] = None
        self.status_lines = []
    
    def start(self, target: str, profile: str):
        """Démarre l'affichage de progression."""
        self.task_id = self.progress.add_task(
            f"Scan de {target} (profil: {profile})",
            total=100,
        )
        self.status_lines = []
    
    def update_phase(self, phase: str, percentage: int):
        """Met à jour la phase en cours."""
        if self.task_id is not None:
            self.progress.update(self.task_id, completed=percentage, description=phase)
    
    def add_status(self, message: str):
        """Ajoute une ligne de statut (max 6 lignes)."""
        self.status_lines.append(message)
        if len(self.status_lines) > 6:
            self.status_lines = self.status_lines[-6:]
    
    def render(self) -> Layout:
        """Construit l'affichage complet."""
        layout = Layout()
        layout.split_column(
            Layout(name="progress", size=3),
            Layout(name="status", size=8),
        )
        
        layout["progress"].update(Panel(self.progress, title="Progression", border_style="blue"))
        
        if self.status_lines:
            status_text = "\n".join(self.status_lines)
            layout["status"].update(Panel(status_text, title="Statut", border_style="green"))
        else:
            layout["status"].update(Panel("En attente...", title="Statut", border_style="yellow"))
        
        return layout
    
    def finish(self, success: bool = True):
        """Termine la progression."""
        if self.task_id is not None:
            self.progress.update(self.task_id, completed=100)
