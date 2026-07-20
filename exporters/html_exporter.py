# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Export HTML du scan_result.
Section 17 de la spec.
Rapport lisible avec CSS inclus, template Jinja2.
"""

from pathlib import Path
from typing import Union
from datetime import datetime

from jinja2 import Template

from models.scan_result import ScanResult
from core.logger import get_logger


# Template HTML avec CSS inline
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omega-scan Rapport de scan - {{ target.normalized_host }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }
        .meta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .meta-item {
            background: #ecf0f1;
            padding: 10px;
            border-radius: 4px;
        }
        .meta-item strong {
            color: #2c3e50;
        }
        .summary-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .rating {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .stat {
            background: rgba(255,255,255,0.2);
            padding: 10px;
            border-radius: 4px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
        }
        .finding {
            background: #fff;
            border-left: 4px solid #95a5a6;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .finding.fail {
            border-left-color: #e74c3c;
        }
        .finding.warn {
            border-left-color: #f39c12;
        }
        .finding.ok {
            border-left-color: #27ae60;
        }
        .finding.na {
            border-left-color: #95a5a6;
        }
        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .finding-title {
            font-weight: bold;
            font-size: 16px;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .badge.fail {
            background: #e74c3c;
            color: white;
        }
        .badge.warn {
            background: #f39c12;
            color: white;
        }
        .badge.ok {
            background: #27ae60;
            color: white;
        }
        .badge.na {
            background: #95a5a6;
            color: white;
        }
        .finding-details {
            margin-top: 10px;
            font-size: 14px;
        }
        .finding-details dt {
            font-weight: bold;
            color: #7f8c8d;
            margin-top: 8px;
        }
        .finding-details dd {
            margin-left: 0;
            margin-bottom: 5px;
        }
        .category-section {
            margin-bottom: 30px;
        }
        .category-title {
            background: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .error {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .error.fatal {
            background: #f8d7da;
            border-left-color: #dc3545;
        }
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Omega-scan ~ Rapport de scan de posture de sécurité</h1>
        
        <div class="meta-grid">
            <div class="meta-item">
                <strong>Cible :</strong> {{ target.normalized_host }}
            </div>
            <div class="meta-item">
                <strong>Profil :</strong> {{ scan_profile.profile_name }}
            </div>
            <div class="meta-item">
                <strong>Scan ID :</strong> {{ meta.scan_id }}
            </div>
            <div class="meta-item">
                <strong>Durée :</strong> {{ meta.duration_ms }}ms
            </div>
            <div class="meta-item">
                <strong>Démarré :</strong> {{ meta.started_at }}
            </div>
            <div class="meta-item">
                <strong>Terminé :</strong> {{ meta.finished_at }}
            </div>
        </div>
        
        <div class="summary-box">
            <div class="rating">{{ summary.overall_rating }}</div>
            <div style="text-align: center; font-size: 18px;">{{ summary.short_message }}</div>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value">{{ summary.checks_total }}</div>
                    <div>Checks totaux</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ summary.findings_total }}</div>
                    <div>Findings (W+F)</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ summary.status_breakdown.FAIL | default(0) }}</div>
                    <div>FAIL</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ summary.status_breakdown.WARN | default(0) }}</div>
                    <div>WARN</div>
                </div>
            </div>
        </div>
        
        {% if findings %}
        <h2>📋 Findings détaillés</h2>
        
        {% set categories = {} %}
        {% for finding in findings %}
            {% if finding.category not in categories %}
                {% set _ = categories.update({finding.category: []}) %}
            {% endif %}
            {% set _ = categories[finding.category].append(finding) %}
        {% endfor %}
        
        {% for category, category_findings in categories.items() %}
        <div class="category-section">
            <div class="category-title">{{ category | upper }}</div>
            
            {% for finding in category_findings %}
            <div class="finding {{ finding.status | lower }}">
                <div class="finding-header">
                    <div class="finding-title">{{ finding.title }}</div>
                    <span class="badge {{ finding.status | lower }}">{{ finding.status }}</span>
                </div>
                <div class="finding-details">
                    <dl>
                        <dt>Règle</dt>
                        <dd>{{ finding.rule_id }}</dd>
                        
                        <dt>Sévérité</dt>
                        <dd>{{ finding.severity | upper }}</dd>
                        
                        <dt>Confiance</dt>
                        <dd>{{ finding.confidence }}</dd>
                        
                        <dt>Description</dt>
                        <dd>{{ finding.description }}</dd>
                        
                        {% if finding.impact %}
                        <dt>Impact</dt>
                        <dd>{{ finding.impact }}</dd>
                        {% endif %}
                        
                        {% if finding.remediation %}
                        <dt>Action recommandée</dt>
                        <dd>{{ finding.remediation }}</dd>
                        {% endif %}
                        
                        {% if finding.evidence %}
                        <dt>Preuve</dt>
                        <dd><code>{{ finding.evidence.value }}</code></dd>
                        {% endif %}
                    </dl>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
        {% endif %}
        
        <h2>🌐 Connectivité</h2>
        <div class="meta-grid">
            <div class="meta-item">
                <strong>DNS résolu :</strong> {{ 'Oui' if connectivity.dns_resolution_attempted else 'Non' }}
            </div>
            <div class="meta-item">
                <strong>HTTP accessible :</strong> {{ 'Oui' if connectivity.http_reachable else 'Non' }}
            </div>
            <div class="meta-item">
                <strong>HTTPS accessible :</strong> {{ 'Oui' if connectivity.https_reachable else 'Non' }}
            </div>
            {% if connectivity.first_successful_scheme %}
            <div class="meta-item">
                <strong>Premier schéma :</strong> {{ connectivity.first_successful_scheme }}
            </div>
            {% endif %}
            {% if connectivity.latency_overview_ms %}
            <div class="meta-item">
                <strong>Latence moyenne :</strong> {{ connectivity.latency_overview_ms }}ms
            </div>
            {% endif %}
        </div>
        
        {% if tls.attempted %}
        <h2>🔐 TLS</h2>
        <div class="meta-grid">
            <div class="meta-item">
                <strong>Handshake réussi :</strong> {{ 'Oui' if tls.handshake_success else 'Non' }}
            </div>
            {% if tls.tls_version %}
            <div class="meta-item">
                <strong>Version TLS :</strong> {{ tls.tls_version }}
            </div>
            {% endif %}
            {% if tls.cipher %}
            <div class="meta-item">
                <strong>Cipher :</strong> {{ tls.cipher }}
            </div>
            {% endif %}
            {% if tls.certificate_subject %}
            <div class="meta-item">
                <strong>Sujet certificat :</strong> {{ tls.certificate_subject }}
            </div>
            {% endif %}
            {% if tls.certificate_issuer %}
            <div class="meta-item">
                <strong>Émetteur :</strong> {{ tls.certificate_issuer }}
            </div>
            {% endif %}
            <div class="meta-item">
                <strong>Hostname match :</strong> {{ 'Oui' if tls.hostname_match else 'Non' }}
            </div>
            {% if tls.self_signed %}
            <div class="meta-item">
                <strong>Auto-signé :</strong> Oui
            </div>
            {% endif %}
        </div>
        {% endif %}
        
        {% if errors %}
        <h2>⚠️ Erreurs</h2>
        {% for error in errors %}
        <div class="error {{ 'fatal' if error.fatal else '' }}">
            <strong>[{{ error.module }}]</strong> {{ error.error_type }}: {{ error.message }}
            {% if error.fatal %}<span style="color: #dc3545; font-weight: bold;"> [FATAL]</span>{% endif %}
            {% if error.failure_category %}<br><small>Catégorie: {{ error.failure_category }}</small>{% endif %}
        </div>
        {% endfor %}
        {% endif %}
        
        <footer>
            Rapport généré le {{ generated_at }} par <strong>Omega-scan</strong> v{{ meta.scanner_version }}
        </footer>
    </div>
</body>
</html>
"""


def export_html(
    scan_result: ScanResult,
    output_path: Union[str, Path],
) -> Path:
    """
    Exporte le scan_result en fichier HTML lisible.
    
    Args:
        scan_result: Résultat complet du scan
        output_path: Chemin du fichier de sortie
    
    Returns:
        Chemin du fichier créé
    """
    logger = get_logger()
    output_path = Path(output_path).resolve()
    
    logger.info(f"[HTML_EXPORT] Export vers {output_path}")
    
    # Préparer les données pour le template
    template = Template(HTML_TEMPLATE)
    
    html_content = template.render(
        meta=scan_result.meta,
        target=scan_result.target.to_dict(),
        scan_profile=scan_result.scan_profile,
        connectivity=scan_result.connectivity,
        tls=scan_result.tls,
        findings=[f.to_dict() for f in scan_result.findings],
        summary=scan_result.summary.to_dict(),
        errors=scan_result.errors,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    
    # Écrire le fichier
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    logger.info(f"[HTML_EXPORT] Export terminé : {output_path}")
    return output_path
