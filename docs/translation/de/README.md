<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT-Lizenz (siehe Datei LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Scanner für die Sicherheitslage von Webdiensten**

> Entwickelt von [kraynux](https://github.com/kraynux) für [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Offizielle Seite: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Vorschau: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Oberfläche und exportierte Berichte in **17 Sprachen** verfügbar — siehe [Sprachen der Oberfläche](#sprachen-der-oberfläche).  
**Sprachen:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** ist ein TUI- und CLI-Werkzeug, das die sichtbare Konfigurationshygiene Ihrer HTTP/HTTPS-Dienste analysiert. Es beobachtet, sammelt Fakten, wendet interpretierende Regeln an und erstellt umsetzbare Berichte, ohne jemals einen aktiven Angriff auszuführen. Werkzeug der Suite `omega-`, aufgebaut nach Clean Architecture — siehe `ARCHITECTURE.md` für alle technischen Details.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-scan/D.png" width="24%" />
</p>

## 1. Vision und Umfang

Omega-scan ist ein Scanner für die Sicherheitslage von Webdiensten, gedacht für die Systemadministration: schnell die sichtbare Konfigurationshygiene eines HTTP/HTTPS-Dienstes auf localhost, im LAN oder auf einem externen Ziel prüfen, auch hinter einem Tunnel wie Tailscale Funnel.

### Was Omega-scan tut

- Sammelt beobachtbare Fakten: Header, Cookies, HTTP-Methoden, TLS, sensible Pfade, CORS-Header.
- Wendet deklarative, interpretierende Regeln auf diese Fakten an.
- Erzeugt einheitliche, begründete und umsetzbare Befunde.
- Zeigt das Ergebnis in der TUI (Textual) oder in der skriptfähigen CLI und über drei Exporte: JSON, Text, HTML.
- Erkennt Fehlalarme, insbesondere Catch-all-Verhalten und durch Authentifizierung geschützte Pfade.
- Passt sich dem Kontext an: Proxy, Tunnel, Multi-Vhost, SNI.
- Verlangt eine ausdrückliche Autorisierungsbestätigung, bevor ein Ziel gescannt wird, das noch nicht als autorisiert angeheftet ist.
- Führt einen dauerhaften Scan-Verlauf pro Ziel, der wiederholt und über die Zeit verglichen werden kann.

### Was Omega-scan nicht tut

- Aktives Schwachstellen-Scannen: kein SQLi, XSS oder RCE.
- CVE-Scannen.
- Brute-Force- oder massives Fuzzing-Werkzeug.
- Tiefgehender Crawler.
- Aggressives paralleles Werkzeug für mehrere Ziele.
- Web-Dashboard.
- Authentifizierung auf Seiten des Scanners.

## 2. Installation

### Voraussetzungen

- Python 3.10+
- Internetverbindung, für die Abhängigkeiten und externe Scans

### Installation

Das offizielle Archiv wird im Format `.tar.gz` bereitgestellt. Prüfen Sie vor der Installation seine Integrität:

```bash
sha256sum omega-scan.tar.gz
```

### Methode 1 — Installationsskript

```bash
[ -d omega-scan ] && echo "ℹ️ Hier bereits entpackt, Schritt übersprungen." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan existiert bereits, Verschieben übersprungen." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Methode 2 — robuste Komplettinstallation



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Legt die virtuelle Umgebung `.venv` an, falls sie noch nicht existiert.
2. Installiert die Abhängigkeiten (`pip install -e .`; `pyproject.toml` bleibt die einzige maßgebliche Quelle).
3. Macht `omega-scan.sh` und `install.sh` ausführbar.
4. Fügt den Alias `scan` zu `~/.bashrc` und `~/.zshrc` hinzu (ohne Duplikat, falls schon vorhanden).

### Abhängigkeiten

Deklariert in `pyproject.toml` (kein `requirements.txt` mehr):
- `textual`: TUI-Oberfläche, Themes, automatische Anpassung an das Terminal
- `httpx`: moderner HTTP/HTTPS-Client
- `jinja2`: Templates für den HTML-Export
- Entwicklungsabhängigkeiten (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Verwendung

### Interaktiver Modus (TUI)

Empfohlen für den täglichen Gebrauch — ohne Argumente gestartet:

```bash
./omega-scan.sh
```

Ablauf: Startbildschirm (schließt sich per Tastendruck oder Klick) → Hauptmenü → Eingabe des Ziels und Wahl des Profils (mit Autorisierungsbestätigung, falls das Ziel noch nicht angeheftet ist) → Scan (Fortschrittsanzeige und Details der Netzwerkvorgänge live) → Ergebnisse (Gesamtnote, nach Kategorie filterbare Befunde, Details per Klick auf eine Zeile) → Export/Verlauf/Vergleich über das Hauptmenü. Die Anpassung an das Terminal (Farben, Größe, strukturelle Reduzierung) erfolgt automatisch; manuelle Anzeigeoptionen sind nicht mehr nötig.

#### Tastenkürzel

| Taste | Aktion |
|---|---|
| `↑` / `↓` | Zwischen den Elementen eines Bildschirms wechseln |
| `Tab` / `Umschalt+Tab` | Zwischen den Feldern eines Formulars wechseln |
| `Esc` | Zurück zum vorherigen Bildschirm (Bestätigung zum Beenden auf dem Startbildschirm) |
| `t` | Nächstes Theme (sofort angewendet, ohne Bestätigung) |
| `r` | Terminalerkennung aktualisieren |
| `a` | Hilfe anzeigen |
| `q` | Beenden (mit Bestätigung) |

### Sprachen der Oberfläche

Die Oberfläche ist in 17 Sprachen verfügbar: Französisch, Englisch, Spanisch, Portugiesisch (Brasilien), Italienisch, Deutsch, Niederländisch, Polnisch, Russisch, vereinfachtes Chinesisch, Vietnamesisch, Thailändisch, Indonesisch, Japanisch, Koreanisch, Hindi und Arabisch. Die Auswahl erfolgt in den Einstellungen („Langue / Language“) und gilt nach einem Neustart der Oberfläche; die Variable `OMEGA_SCAN_LANG` (zum Beispiel `OMEGA_SCAN_LANG=de ./omega-scan.sh`) erzwingt eine Sprache für eine Sitzung. Aus omega-suite gestartet, übernimmt omega-scan die Sprache der Suite. Auf einer Linux-Textkonsole (TTY) werden Sprachen mit nicht lateinischer Schrift für die Sitzung auf Englisch angezeigt. Die Kommandozeile bleibt auf Französisch.

### Kontakt und Support

Die Hilfe (Taste `a`) bietet einen Bildschirm **Kontakt und Support**: *Einen Kaffee spendieren* (PayPal-Seite des Entwicklers), *Support kontaktieren* (E-Mail-Adresse und Kontaktformular der Website, im Klartext angezeigt), *Mich als Nutzer melden (anonym)* und *Updates prüfen*. Die Meldung ist freiwillig, standardmäßig deaktiviert und wird nur ein einziges Mal gesendet: Sie dient nur dazu, die Nutzer zu zählen und, wenn gewünscht, ihren Kontinent oder ihr Land (geschlossene Listen, nie Freitext). Gesendet werden ein zufällig gezogener Schlüssel, der Name der Software (`omega-scan`) und ihre Version; nie ein Name, ein Rechnername, eine Einstellung, ein Ziel oder ein Ergebnis. Die IP-Adresse wird in den Meldungen nicht gespeichert, durchläuft aber wie jeder Besuch die Sicherheitsprüfungen und das Protokoll des Empfangsservers. Rückzug jederzeit über denselben Bildschirm (*Mich nicht mehr melden*). Die Update-Prüfung liest nur die Liste der auf der Website veröffentlichten Versionen, und nie ohne Klick.

### Skriptfähiger Modus (CLI)

Jeder Unterbefehl aktiviert den CLI-Modus (einfacher Text oder JSON mit `--json`):

```bash
# Ein Ziel scannen (--authorize erforderlich, wenn das Ziel nicht bereits angeheftet ist)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Verlauf
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Export
./omega-scan.sh export scan-30577411758e --format html --output bericht.html

# Als autorisiert angeheftete Ziele (kein --authorize bei späteren Scans nötig)
./omega-scan.sh targets pin example.org --note "Kundenvereinbarung 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Autorisierungsschutz für Ziele

Kein Scan startet ohne ausdrückliche Autorisierungsbestätigung für das Ziel (Kontrollkästchen in der TUI, `--authorize` in der CLI), außer das Ziel ist bereits angeheftet. Geprüft wird auf Anwendungsseite (`application/pipeline/guards/authorization_guard.py`), nicht nur in der Oberfläche.

### Akzeptierte Zielformate

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 mit Port
::1                         IPv6
[2001:db8::10]:8443         IPv6 mit eckigen Klammern und Port
example.org                 Hostname
intranet.lan:8080/admin     Hostname mit Port und Pfad
http://example.org          HTTP-URL
https://example.org/admin   HTTPS-URL
```

## 4. Scan-Profile

| Parameter | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Einsatz | Schnellprüfung | Vollständig (Standard) | Gründlich | localhost / LAN |
| Timeout Verbindung/Lesen | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| HTTP-Methoden | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Pfadprüfung | Nein | Ja (~20) | Ja (vollständig) | Ja (~20) |
| TLS | Nein | Ja | Ja (detailliert) | Ja (tolerant) |
| CORS-Sonde | Nein | Ja | Ja | Ja |
| Catch-all | - | Ja | Ja | Ja |
| HSTS-Richtlinie | Nicht bewertet | Standard | Streng | Tolerant |

### Wann welches Profil

- `quick`: Blitzprüfung vor der Inbetriebnahme
- `standard`: vollständiges Audit eines Produktivdienstes, empfohlen
- `extended`: gründliches Audit einschließlich riskanter HTTP-Methoden
- `local-lab`: Scan von localhost oder dem LAN, ohne die für öffentliche Dienste gedachten Regeln (insbesondere HSTS) als Mangel zu werten

## 5. Architektur

Omega-scan ist nach **Clean Architecture** aufgebaut (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), angelehnt an die Vorlage der Suite `omega-` (siehe `omega-stress`). Alle Details — Verzeichnisbaum, Abhängigkeitsregeln, Funktionsketten, Ausnahmehierarchie, Benennungssystematik — stehen in **`ARCHITECTURE.md`**, dem normativen Referenzdokument.

Sehr kurzer Überblick:

```text
src/omega_scan/
├── domain/          Reine Fachlogik (Ziele, Profile, Scans, Checks, Berichte, Themes...)
├── application/     Anwendungsfälle (commands/queries), Ausführungspipeline, Schutzprüfungen
├── ports/           Von der Anwendung erwartete Verträge (Sonden, Repositories, Exporter...)
├── infrastructure/  Konkrete Implementierungen (httpx, SQLite; Textual ist NICHT hier)
├── interfaces/      tui/ (Textual) und cli/ (skriptfähig), mit strikter Funktionsgleichheit
├── app/             Zusammenbau (DependencyContainer, Bootstrap, Lebenszyklus)
├── core/, shared/   Übergreifendes Vokabular, fachfremde Hilfsmittel
└── plugins/         Struktur angelegt, leer (keine bestätigte Erweiterungsachse)
```

Seit v1 unveränderte Entwurfsregeln:
- `domain/checks/`: urteilt anhand der Belege, greift nie aufs Netzwerk zu.
- `infrastructure/network/`: greift aufs Netzwerk zu, urteilt nie.
- `interfaces/`: zeigt an, enthält keine Fachlogik.
- `infrastructure/exporters/`: lesen das Scan-Ergebnis, berechnen nichts neu.

## 6. Systematik der Regeln

### Transport, `TRN-*`

- `TRN-HTTP-001`: HTTP erreichbar ohne Weiterleitung auf HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS nicht erreichbar, `FAIL`
- `TRN-HSTS-001`: HSTS-Header fehlt, `FAIL`
- `TRN-HSTS-002`: niedriges HSTS-`max-age`, unter 1 Jahr, `WARN`

### TLS-Tiefe, `TLS-*`

- `TLS-VERSION-001`: veraltetes TLS-Protokoll (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: offensichtlich schwache Cipher-Suite (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Header, `HDR-*`

- `HDR-CSP-001`: CSP fehlt auf einer HTML-Seite, `FAIL`
- `HDR-CSP-002`: zu großzügige CSP, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` fehlt, `WARN`
- `HDR-SERVER-001`: `Server`-Banner offengelegt, `WARN`
- `HDR-CACHE-001`: `Cache-Control` fehlt oder ist zu großzügig auf einer HTML-Seite, `WARN`

### Cookies, `COO-*`

- `COO-SECURE-001`: Cookie in einer HTTPS-Antwort ohne `Secure`-Attribut, `WARN`
- `COO-HTTPONLY-001`: Cookie ohne `HttpOnly`-Attribut, `WARN`
- `COO-SAMESITE-001`: `SameSite` fehlt, oder `None` ohne `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` kombiniert mit `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: beliebiger Origin unverändert in `Access-Control-Allow-Origin` zurückgespiegelt, `WARN`

### HTTP-Methoden, `MTH-*`

- `MTH-OPTIONS-001`: Methode OPTIONS aktiviert, `INFO`
- `MTH-TRACE-001`: Methode TRACE aktiviert, `WARN`
- `MTH-PUT-001`: Methode PUT aktiviert, `WARN`
- `MTH-DELETE-001`: Methode DELETE aktiviert, `WARN`
- `MTH-PATCH-001`: Methode PATCH aktiviert, `WARN`
- `MTH-CONNECT-001`: Methode CONNECT aktiviert, `WARN`

### Offenlegung, `EXR-*`

- `EXR-ADMIN-001`: Admin-Pfad ohne Authentifizierung erreichbar, `WARN`
- `EXR-SENSITIVE-001`: sensible Datei erreichbar, `.env`, `.git`, `FAIL`

### Informationslecks, `INF-*`

- `INF-BANNER-001`: Server-Banner offengelegt, `WARN`
- `INF-ERROR-001`: ausführliche Fehlermeldungen, `WARN`
- `INF-STACK-001`: Stacktrace offengelegt, `FAIL`
- `INF-ROBOTS-001`: Datei `robots.txt` vorhanden, `OK` zur Information
- `INF-HEADER-001`: gesprächige technische Header, `WARN`
- `INF-SECURITYTXT-001`: Datei `/.well-known/security.txt` vorhanden, `OK` zur Information

## 7. Vertrauensrichtlinie

| Stufe | Definition |
|---|---|
| `certain` | Direkter, eindeutiger Beleg, unverändert aus der Antwort gelesen: Header vorhanden oder nicht, roher HTTP-Code. |
| `high` | Klarer Beleg, aber indirekter Kontext: Methoden über OPTIONS, beobachtetes Cookie. |
| `medium` | Befund möglicherweise durch eine Zwischenstation beeinflusst: Proxy, WAF, Tunnel. |
| `low` | Indirekte Erkennung, mehrdeutiger Inhalt oder Situation `catch_all_suspected`. |

### Automatische Herabstufungen

- `catch_all_suspected = true`: Vertrauen auf `low` begrenzt
- `proxy_suspected = true`: Vertrauen auf `medium` begrenzt
- `observed_access_state = ambiguous`: Vertrauen auf `low` begrenzt

## 8. Erkennung von Fehlalarmen

### Catch-all-Verhalten

Bevor die sensiblen Pfade getestet werden, erzeugt Omega-scan einen unwahrscheinlichen Zufallspfad. Antwortet der Server darauf mit `200 OK`, wird das Ziel als `catch_all_suspected = true` markiert und alle Offenlegungsbefunde werden auf `confidence = low` herabgestuft.

### Authentifizierung oder Fehlen

Ein geschützter Pfad — `401`, `403` oder eine Weiterleitung zur Anmeldeseite — wird weder als fehlend noch als offengelegt markiert. Er wird als `N/A` markiert, mit dem Hinweis: „geschützter Pfad, Vorhandensein ohne Authentifizierung nicht bestätigbar“.

### Proxy / Tunnel

Werden die Header `X-Forwarded-*`, `Via` oder `Forwarded` erkannt, wechselt `proxy_suspected` auf `true`, und das Vertrauen der betroffenen Befunde — Banner, TLS — wird auf `medium` begrenzt.

## 9. Terminal-Kompatibilität

Die TUI (Textual) erkennt automatisch die Fähigkeiten des Terminals (Farbe, Größe) und passt ihr strukturelles Stylesheet entsprechend an (`complete`/`standard`/`reduced`/`mono`) — keine manuellen Optionen (`--no-emoji`, `--no-color`, `--plain`) mehr wie in v1. Der CLI-Modus bleibt immer einfacher Text (oder `--json`), unabhängig vom Terminal.

## 10. Exporte

Text- und HTML-Berichte werden in der in den Einstellungen gewählten Sprache geschrieben („Sprache der Exporte“, standardmäßig die der Oberfläche); JSON bleibt Daten und wird nicht übersetzt. Die Berichte werden standardmäßig in `var/exports/` erzeugt (Laufzeitpfad, siehe `ARCHITECTURE.md`) oder unter dem angegebenen Pfad (`--output` in der CLI, Dialog in der TUI).

### JSON, die maßgebliche Quelle

Vollständige Struktur des Scans (`ScanRun`), streng JSON-serialisierbar.

### Text, kompakter lesbarer Bericht

Außerhalb des Terminals lesbar, ohne ANSI-Codes, mit hierarchischer Gliederung.

### HTML, lesbarer Webbericht

Eigenständiger Bericht mit Inline-CSS, in jedem Browser lesbar, teil- und archivierbar.

## 11. Verlauf und Vergleich

Jeder Scan wird gespeichert (SQLite, `var/db/app.db`): Verlauf nach Ziel einsehbar, Details eines früheren Laufs, Vergleich zweier Scans (neu aufgetretene / behobene / unveränderte / geänderte Befunde) und Wiederholung eines Scans auf demselben Ziel ohne erneute Eingabe — in v1 nicht vorhanden, bei der Migration zu Clean Architecture hinzugekommen.

## 12. Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

Struktur: `tests/unit/` (Domain und Anwendung, ohne echte E/A), `tests/integration/` (echte SQLite-Datenbank/Dateien, simulierter HTTP-Server `pytest-httpserver`), `tests/e2e/` (CLI und TUI von Anfang bis Ende, `Textual.testing`).

## 13. Außerhalb des Umfangs

- CVE-Scannen
- Aktive Erkennung von SQLi, XSS, RCE
- Komplexe Authentifizierung auf Seiten des Scanners
- Tiefgehendes Crawling
- Fuzzing
- Massenhaftes Brute-Forcing von Pfaden
- Gleichzeitiges Scannen mehrerer Ziele
- Aggressive Parallelität
- Web-Dashboard

---

> Omega-scan — Beobachten, sammeln, interpretieren, berichten.  
> Ein Scanner für die Sicherheitslage, kein Angriffswerkzeug.
