# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Export HTML d'un ScanRun. Seul module du projet ou `jinja2` est importe.

Gabarit externe (templates/report.html.jinja, meme patron qu'omega-stress)
plutot qu'inline : permet la selection de theme d'export (§9.2 des retours
utilisateur) en injectant une Palette comme variables de contexte, sans
recharger un template different par theme."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import jinja2

from omega_scan.domain.scans.models import ScanRun
from omega_scan.domain.theme.policies import DEFAULT_EXPORT_THEME
from omega_scan.infrastructure.exporters.html_theme_resolver import resolve_export_palette
from omega_scan.infrastructure.logging.app_logger import get_logger

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_TEMPLATE_NAME = "report.html.jinja"

_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(_TEMPLATE_DIR),
    autoescape=jinja2.select_autoescape(["html", "jinja"]),
)


def export_html(
    run: ScanRun, output_path: str | Path, *, export_theme: str = DEFAULT_EXPORT_THEME
) -> Path:
    """Exporte le ScanRun en fichier HTML lisible, teinte selon `export_theme`
    (catalogue de 5 themes d'export, domain/theme/policies.py::EXPORT_PALETTES)."""
    logger = get_logger()
    output_path = Path(output_path).resolve()

    logger.info(f"[HTML_EXPORT] Export vers {output_path} (theme {export_theme})")

    palette = resolve_export_palette(export_theme)
    template = _environment.get_template(_TEMPLATE_NAME)

    html_content = template.render(
        meta=run.meta,
        target=run.target.to_dict(),
        scan_profile=run.scan_profile,
        connectivity=run.connectivity,
        tls=run.tls,
        findings=[f.to_dict() for f in run.findings],
        summary=run.summary.to_dict(),
        errors=run.errors,
        palette=palette,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")

    logger.info(f"[HTML_EXPORT] Export termine : {output_path}")
    return output_path
