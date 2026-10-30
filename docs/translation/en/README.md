<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT License (see LICENCE file) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Web security posture scanner**

> Built by **kraynux** for **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Official page: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Preview: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interface and exported reports available in **17 languages** — see [Interface languages](#interface-languages).  
**Languages:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** is a TUI + CLI tool that analyzes the visible configuration hygiene of your HTTP/HTTPS services. It observes, collects facts, applies interpretive rules and produces actionable reports, without ever performing an active attack. A tool of the `omega-` suite, structured in Clean Architecture — see `ARCHITECTURE.md` for the full technical details.

## 1. Vision and scope

Omega-scan is a web security posture scanner meant for system administration: quickly checking the visible configuration hygiene of an HTTP/HTTPS service on localhost, the LAN or an external target, including behind a tunnel such as Tailscale Funnel.

### What Omega-scan does

- Collects observable facts: headers, cookies, HTTP methods, TLS, sensitive paths, CORS headers.
- Applies declarative interpretive rules to these facts.
- Produces consistent, justified and actionable findings.
- Presents the result in a TUI (Textual) or a scriptable CLI, and through three exports: JSON, text, HTML.
- Detects false positives, especially catch-all behavior and paths protected by authentication.
- Adapts to the context: proxy, tunnel, multi-vhost, SNI.
- Requires explicit authorization confirmation before scanning any target that is not already pinned-authorized.
- Keeps a persistent per-target scan history that can be replayed and compared over time.

### What Omega-scan does not do

- Active vulnerability scanning: no SQLi, XSS or RCE.
- CVE scanning.
- Brute force or massive fuzzing tool.
- Deep crawler.
- Aggressive parallel multi-target tool.
- Web dashboard.
- Scanner-side authentication.

## 2. Installation

### Requirements

- Python 3.10+
- Internet connection, for the dependencies and external scans

### Installation

The official archive is provided in `.tar.gz` format. Check its integrity before installing:

```bash
sha256sum omega-scan.tar.gz
```

### Method 1 — installation script

```bash
[ -d omega-scan ] && echo "ℹ️ Already extracted here, step skipped." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan already exists, move skipped." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Method 2 — resilient full installation



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Creates the `.venv` virtual environment if it does not already exist.
2. Installs the dependencies (`pip install -e .`; `pyproject.toml` remains the single source of truth).
3. Makes `omega-scan.sh` and `install.sh` executable.
4. Adds the `scan` alias to `~/.bashrc` and `~/.zshrc` (no duplicate if already present).

### Dependencies

Declared in `pyproject.toml` (no more `requirements.txt`):
- `textual`: TUI interface, themes, automatic adaptation to the terminal
- `httpx`: modern HTTP/HTTPS client
- `jinja2`: templating for the HTML export
- Development dependencies (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Usage

### Interactive mode (TUI)

Recommended for everyday use — launched without arguments:

```bash
./omega-scan.sh
```

Flow: splash screen (closes on a key press or a click) → main menu → input of the target and choice of profile (with authorization confirmation if the target is not already pinned) → scan (progress gauge and details of network operations shown live) → results (overall grade, findings filterable by category, details on clicking a row) → export/history/comparison from the main menu. Adaptation to the terminal (colors, size, structural degradation) is automatic; manual display flags are no longer needed.

#### Keyboard shortcuts

| Key | Action |
|---|---|
| `↑` / `↓` | Move between the items of a screen |
| `Tab` / `Shift+Tab` | Move between the fields of a form |
| `Esc` | Back to the previous screen (exit confirmation on the home screen) |
| `t` | Next theme (applied immediately, no confirmation) |
| `r` | Refresh terminal detection |
| `a` | Show help |
| `q` | Quit (with confirmation) |

### Interface languages

The interface is available in 17 languages: French, English, Spanish, Portuguese (Brazil), Italian, German, Dutch, Polish, Russian, Simplified Chinese, Vietnamese, Thai, Indonesian, Japanese, Korean, Hindi and Arabic. The choice is made in Settings ("Langue / Language") and takes effect after the interface restarts; the `OMEGA_SCAN_LANG` variable (for example `OMEGA_SCAN_LANG=en ./omega-scan.sh`) forces a language for one session. When launched from omega-suite, omega-scan uses the suite's language. On a Linux text console (TTY), languages with a non-Latin script are shown in English for the session. The command line stays in French.

### Scriptable mode (CLI)

Any subcommand triggers CLI mode (plain text, or JSON with `--json`):

```bash
# Scan a target (--authorize required if the target is not already pinned)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# History
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Export
./omega-scan.sh export scan-30577411758e --format html --output report.html

# Pinned-authorized targets (no --authorize needed on later scans)
./omega-scan.sh targets pin example.org --note "client agreement 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Target authorization guard

No scan starts without explicit authorization confirmation for the target (a checkbox in the TUI, `--authorize` in the CLI), unless the target is already pinned. Enforced on the application side (`application/pipeline/guards/authorization_guard.py`), not only in the interface.

### Accepted target formats

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 with port
::1                         IPv6
[2001:db8::10]:8443         IPv6 with brackets and port
example.org                 Hostname
intranet.lan:8080/admin     Hostname with port and path
http://example.org          HTTP URL
https://example.org/admin   HTTPS URL
```

## 4. Scan profiles

| Parameter | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Use | Quick check | Full (default) | In-depth | localhost / LAN |
| Connect/read timeout | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| HTTP methods | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Path probing | No | Yes (~20) | Yes (full) | Yes (~20) |
| TLS | No | Yes | Yes (detailed) | Yes (tolerant) |
| CORS probe | No | Yes | Yes | Yes |
| Catch-all | - | Yes | Yes | Yes |
| HSTS policy | Not evaluated | Standard | Strict | Tolerant |

### When to use which profile

- `quick`: lightning check before going to production
- `standard`: full audit of a production service, recommended
- `extended`: in-depth audit including risky HTTP methods
- `local-lab`: scan of localhost or the LAN without penalizing rules designed for public services, HSTS in particular

## 5. Architecture

Omega-scan is structured in **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), aligned with the `omega-` suite template (see `omega-stress`). The full details — tree, dependency rules, functional chains, exception hierarchy, naming taxonomy — live in **`ARCHITECTURE.md`**, the normative reference document.

Very short overview:

```text
src/omega_scan/
├── domain/          Pure business logic (targets, profiles, scans, checks, reports, themes...)
├── application/     Use cases (commands/queries), execution pipeline, guards
├── ports/           Contracts expected by the application (probers, repositories, exporters...)
├── infrastructure/  Concrete implementations (httpx, SQLite; Textual is NOT here)
├── interfaces/      tui/ (Textual) and cli/ (scriptable), with strict feature parity
├── app/             Assembly (DependencyContainer, bootstrap, lifecycle)
├── core/, shared/   Cross-cutting vocabulary, non-business utilities
└── plugins/         Structure in place, empty (no confirmed extension axis)
```

Design rules unchanged since v1:
- `domain/checks/`: judges from the evidence, never does networking.
- `infrastructure/network/`: does networking, never judges.
- `interfaces/`: displays, contains no business logic.
- `infrastructure/exporters/`: read the scan result, recompute nothing.

## 6. Rule taxonomy

### Transport, `TRN-*`

- `TRN-HTTP-001`: HTTP reachable without redirect to HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS not reachable, `FAIL`
- `TRN-HSTS-001`: HSTS header missing, `FAIL`
- `TRN-HSTS-002`: weak HSTS `max-age`, under 1 year, `WARN`

### TLS depth, `TLS-*`

- `TLS-VERSION-001`: obsolete TLS protocol (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: clearly weak cipher suite (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Headers, `HDR-*`

- `HDR-CSP-001`: CSP missing on an HTML page, `FAIL`
- `HDR-CSP-002`: overly permissive CSP, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` missing, `WARN`
- `HDR-SERVER-001`: `Server` banner exposed, `WARN`
- `HDR-CACHE-001`: `Cache-Control` missing or permissive on an HTML page, `WARN`

### Cookies, `COO-*`

- `COO-SECURE-001`: cookie on an HTTPS response without the `Secure` attribute, `WARN`
- `COO-HTTPONLY-001`: cookie without the `HttpOnly` attribute, `WARN`
- `COO-SAMESITE-001`: `SameSite` missing, or `None` without `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: arbitrary origin reflected as-is in `Access-Control-Allow-Origin`, `WARN`

### HTTP methods, `MTH-*`

- `MTH-OPTIONS-001`: OPTIONS method enabled, `INFO`
- `MTH-TRACE-001`: TRACE method enabled, `WARN`
- `MTH-PUT-001`: PUT method enabled, `WARN`
- `MTH-DELETE-001`: DELETE method enabled, `WARN`
- `MTH-PATCH-001`: PATCH method enabled, `WARN`
- `MTH-CONNECT-001`: CONNECT method enabled, `WARN`

### Exposure, `EXR-*`

- `EXR-ADMIN-001`: admin path reachable without authentication, `WARN`
- `EXR-SENSITIVE-001`: sensitive file reachable, `.env`, `.git`, `FAIL`

### Information leaks, `INF-*`

- `INF-BANNER-001`: server banners exposed, `WARN`
- `INF-ERROR-001`: detailed error messages, `WARN`
- `INF-STACK-001`: stack trace exposed, `FAIL`
- `INF-ROBOTS-001`: `robots.txt` file present, `OK` info
- `INF-HEADER-001`: talkative technical headers, `WARN`
- `INF-SECURITYTXT-001`: `/.well-known/security.txt` file present, `OK` info

## 7. Confidence policy

| Level | Definition |
|---|---|
| `certain` | Direct, unambiguous evidence read as-is in the response: header present or absent, raw HTTP code. |
| `high` | Clear evidence but indirect context: methods through OPTIONS, observed cookie. |
| `medium` | Finding possibly influenced by an intermediary: proxy, WAF, tunnel. |
| `low` | Indirect detection, ambiguous content, or a `catch_all_suspected` situation. |

### Automatic downgrades

- `catch_all_suspected = true`: confidence capped at `low`
- `proxy_suspected = true`: confidence capped at `medium`
- `observed_access_state = ambiguous`: confidence capped at `low`

## 8. False positive detection

### Catch-all behavior

Before testing sensitive paths, Omega-scan generates an improbable random path. If the server answers `200 OK` to it, the target is marked `catch_all_suspected = true` and every exposure finding is downgraded to `confidence = low`.

### Authentication vs. absence

A protected path — `401`, `403` or a redirect to a login page — is marked neither absent nor exposed. It is marked `N/A` with the note "protected path, presence cannot be confirmed without authentication".

### Proxy / tunnel

If `X-Forwarded-*`, `Via` or `Forwarded` headers are detected, `proxy_suspected` becomes `true` and the affected findings — banners, TLS — have their confidence capped at `medium`.

## 9. Terminal compatibility

The TUI (Textual) automatically detects the terminal's capabilities (color, size) and adapts its structural stylesheet accordingly (`complete`/`standard`/`reduced`/`mono`) — no more manual flags (`--no-emoji`, `--no-color`, `--plain`) as in v1. CLI mode always stays plain text (or `--json`), independent of the terminal.

## 10. Exports

Text and HTML reports are written in the language chosen in Settings ("Export language", by default the interface language); JSON stays data and is not translated. Reports are generated in `var/exports/` by default (runtime path, see `ARCHITECTURE.md`), or at the given path (`--output` in the CLI, a dialog in the TUI).

### JSON, the source of truth

Full structure of the scan (`ScanRun`), strictly JSON-serializable.

### Text, compact human-readable report

Readable outside a terminal, without ANSI codes, with a hierarchical structure.

### HTML, readable web report

Self-contained report with inline CSS, viewable in any browser, shareable and archivable.

## 11. History and comparison

Each scan is persisted (SQLite, `var/db/app.db`): history can be browsed by target, details of a past run, comparison between two scans (findings appeared / resolved / unchanged / changed), and replay of a scan on the same target without re-entering it — missing from v1, added during the migration to Clean Architecture.

## 12. Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

Structure: `tests/unit/` (domain and application, without real I/O), `tests/integration/` (real SQLite/files, fake HTTP server `pytest-httpserver`), `tests/e2e/` (end-to-end CLI and TUI, `Textual.testing`).

## 13. Out of scope

- CVE scanning
- Active detection of SQLi, XSS, RCE
- Complex scanner-side authentication
- Deep crawling
- Fuzzing
- Massive path brute forcing
- Simultaneous multi-target scanning
- Aggressive parallelism
- Web dashboard

---

> Omega-scan — Observe, collect, interpret, report.  
> A posture scanner, not an attack tool.
