<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT License (see LICENSE file) -->
<div align="center">
  <img src="docs/assets/omega-scan.png" alt="Omega-Scan" width="256">
</div>

# 🔍 OMEGA-SCAN

**Web security posture scanner**

> Developed by **kraynux** for **Omega-server**  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Official page: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Preview: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

**Languages:**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-scan** is a TUI + CLI tool that analyzes the visible configuration hygiene of HTTP/HTTPS services. It observes and collects facts, applies declarative interpretive rules, and produces actionable reports without ever performing an active attack. It is the third tool in the `omega-` suite (after `omega-fire` and `omega-stress`), structured according to Clean Architecture; see `ARCHITECTURE.md` for the complete technical details.

## 1. Vision and scope

Omega-scan is a web security posture scanner intended for system administration: quickly checking the visible configuration hygiene of an HTTP/HTTPS service on localhost, a LAN, or an external target, including targets behind a tunnel such as Tailscale Funnel.

### What Omega-scan does

- Collects observable facts: headers, cookies, HTTP methods, TLS, sensitive paths, and CORS headers.
- Applies declarative interpretive rules to those facts.
- Produces consistent, justified, actionable findings.
- Presents results in a Textual TUI or scriptable CLI, with three export formats: JSON, text, and HTML.
- Detects false positives, especially catch-all behavior and paths protected by authentication.
- Adapts to context: proxy, tunnel, multi-vhost, and SNI.
- Requires explicit authorization confirmation before scanning any target that is not already pinned and authorized.
- Keeps a persistent per-target scan history that can be replayed and compared over time.

### What Omega-scan does not do

- Active vulnerability scanning; no SQLi, XSS, or RCE testing.
- CVE scanning.
- Brute-force or large-scale fuzzing.
- Deep crawling.
- Aggressive parallel multi-target scanning.
- Web dashboard.
- Scanner-side authentication.

## 2. Installation

### Requirements

- Python 3.10+
- Internet connection for dependencies and external scans

### Installation

The official archive is supplied as `.tar.gz`. Verify its integrity before installation:

```bash
sha256sum omega-scan.tar.gz
```

### Method 1 — installation script

```bash
[ -d omega-scan ] && echo "ℹ️ Already extracted here; skipping step." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan already exists; skipping move." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Method 2 — resilient complete installation

```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Creates the `.venv` virtual environment if it does not already exist.
2. Installs dependencies (`pip install -e .`; `pyproject.toml` remains the single source of truth).
3. Makes `omega-scan.sh` and `install.sh` executable.
4. Adds the `scan` alias to `~/.bashrc` and `~/.zshrc` without duplicating it.

### Dependencies

Declared in `pyproject.toml` (there is no longer a `requirements.txt`):
- `textual`: TUI, themes, and automatic terminal adaptation.
- `httpx`: modern HTTP/HTTPS client.
- `jinja2`: templating for HTML export.
- Development dependencies (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`.

## 3. Usage

### Interactive mode (TUI)

Recommended for daily use; launch without arguments:

```bash
./omega-scan.sh
```

Workflow: start screen (closes on a key press or click) → main menu → enter the target and choose a profile (with authorization confirmation if the target is not already pinned) → scan (progress bar and network operations displayed live) → results (overall score, findings filterable by category, click a row for details) → export/history/comparison from the main menu. Terminal adaptation (colors, size, and structural degradation) is automatic; manual display flags are no longer needed.

#### Keyboard shortcuts

| Key | Action |
|---|---|
| `↑` / `↓` | Navigate between screen elements |
| `Tab` / `Shift+Tab` | Navigate between form fields |
| `Esc` | Return to the previous screen (exit confirmation on the home screen) |
| `t` | Next theme (applied immediately, without confirmation) |
| `r` | Refresh terminal detection |
| `a` | Show help |
| `q` | Quit with confirmation |

### Scriptable mode (CLI)

Any subcommand starts CLI mode (plain text, or JSON with `--json`):

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

# Pinned and authorized targets (no --authorize required for later scans)
./omega-scan.sh targets pin example.org --note "client approval 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Target authorization guard

No scan starts without explicit authorization confirmation for the target (checkbox in the TUI, `--authorize` in the CLI), unless the target is already pinned. The check is enforced in the application (`application/pipeline/guards/authorization_guard.py`), not only in the interface.

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
| Path probing | No | Yes (~20) | Yes (complete) | Yes (~20) |
| TLS | No | Yes | Yes (detailed) | Yes (tolerant) |
| CORS probe | No | Yes | Yes | Yes |
| Catch-all | — | Yes | Yes | Yes |
| HSTS policy | Not evaluated | Standard | Strict | Tolerant |

### Which profile to use

- `quick`: quick check before production deployment.
- `standard`: complete production-service audit; recommended.
- `extended`: in-depth audit including risky HTTP methods.
- `local-lab`: localhost or LAN scanning without applying public-facing rules too strictly, especially HSTS.

## 5. Architecture

Omega-scan follows **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), aligned with the `omega-` suite template (see `omega-stress`). The complete details — tree, dependency rules, functional chains, exception hierarchy, and naming taxonomy — are in **`ARCHITECTURE.md`**, the normative reference document.

```text
src/omega_scan/
├── domain/          Pure business logic (targets, profiles, scans, checks, reports, themes...)
├── application/     Use cases (commands/queries), execution pipeline, guards
├── ports/           Contracts expected by the application (probers, repositories, exporters...)
├── infrastructure/  Concrete implementations (httpx, SQLite; Textual is NOT here)
├── interfaces/      tui/ (Textual) and cli/ (scriptable), with strict functional parity
├── app/             Assembly (DependencyContainer, bootstrap, lifecycle)
├── core/, shared/   Cross-cutting vocabulary and non-business utilities
└── plugins/         Established, empty structure (no confirmed extension axis)
```

Design rules unchanged since v1:
- `domain/checks/`: judges from evidence and never performs network operations.
- `infrastructure/network/`: performs network operations and never judges.
- `interfaces/`: displays data and contains no business logic.
- `infrastructure/exporters/`: reads scan results and never recalculates them.

## 6. Rule taxonomy

### Transport, `TRN-*`

- `TRN-HTTP-001`: HTTP accessible without HTTPS redirection, `WARN`.
- `TRN-HTTPS-001`: HTTPS inaccessible, `FAIL`.
- `TRN-HSTS-001`: HSTS header absent, `FAIL`.
- `TRN-HSTS-002`: low HSTS `max-age`, less than one year, `WARN`.

### TLS depth, `TLS-*`

- `TLS-VERSION-001`: obsolete TLS protocol (< TLSv1.2), `FAIL`.
- `TLS-CIPHER-001`: clearly weak cipher suite (RC4, DES, NULL, EXPORT, MD5), `WARN`.

### Headers, `HDR-*`

- `HDR-CSP-001`: CSP absent on an HTML page, `FAIL`.
- `HDR-CSP-002`: overly permissive CSP, `WARN`.
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` absent, `WARN`.
- `HDR-SERVER-001`: `Server` banner exposed, `WARN`.
- `HDR-CACHE-001`: `Cache-Control` absent or permissive on an HTML page, `WARN`.

### Cookies, `COO-*`

- `COO-SECURE-001`: cookie on an HTTPS response without the `Secure` attribute, `WARN`.
- `COO-HTTPONLY-001`: cookie without the `HttpOnly` attribute, `WARN`.
- `COO-SAMESITE-001`: `SameSite` absent, or `None` without `Secure`, `WARN`.

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true`, `FAIL`.
- `COR-REFLECTED-ORIGIN-001`: arbitrary origin reflected as-is in `Access-Control-Allow-Origin`, `WARN`.

### HTTP methods, `MTH-*`

- `MTH-OPTIONS-001`: OPTIONS method enabled, `INFO`.
- `MTH-TRACE-001`: TRACE method enabled, `WARN`.
- `MTH-PUT-001`: PUT method enabled, `WARN`.
- `MTH-DELETE-001`: DELETE method enabled, `WARN`.
- `MTH-PATCH-001`: PATCH method enabled, `WARN`.
- `MTH-CONNECT-001`: CONNECT method enabled, `WARN`.

### Exposure, `EXR-*`

- `EXR-ADMIN-001`: admin path accessible without authentication, `WARN`.
- `EXR-SENSITIVE-001`: sensitive file accessible, `.env`, `.git`, `FAIL`.

### Information leaks, `INF-*`

- `INF-BANNER-001`: server banners exposed, `WARN`.
- `INF-ERROR-001`: detailed error messages, `WARN`.
- `INF-STACK-001`: exposed stack trace, `FAIL`.
- `INF-ROBOTS-001`: `robots.txt` present, informational `OK`.
- `INF-HEADER-001`: overly verbose technical headers, `WARN`.
- `INF-SECURITYTXT-001`: `/.well-known/security.txt` present, informational `OK`.

## 7. Confidence policy

| Level | Definition |
|---|---|
| `certain` | Direct, unambiguous evidence read directly from the response: header present or absent, raw HTTP status code. |
| `high` | Clear evidence with indirect context: methods discovered through OPTIONS, observed cookie. |
| `medium` | Finding possibly influenced by an intermediary, proxy, WAF, or tunnel. |
| `low` | Indirect detection, ambiguous content, or `catch_all_suspected` state. |

### Automatic downgrades

- `catch_all_suspected = true`: confidence capped at `low`.
- `proxy_suspected = true`: confidence capped at `medium`.
- `observed_access_state = ambiguous`: confidence capped at `low`.

## 8. False-positive detection

### Catch-all behavior

Before testing sensitive paths, Omega-scan generates an unlikely random path. If the server responds `200 OK`, the target is marked `catch_all_suspected = true`, and all exposure findings are downgraded to `confidence = low`.

### Authentication versus absence

A protected path, `401`, `403`, or redirect to login is marked neither absent nor exposed. It is marked `N/A` with the note: “protected path; presence cannot be confirmed without authentication”.

### Proxy / tunnel

If `X-Forwarded-*`, `Via`, or `Forwarded` headers are detected, `proxy_suspected` becomes `true`, and the confidence of related findings (banners, TLS) is capped at `medium`.

## 9. Terminal compatibility

The Textual TUI automatically detects terminal capabilities (color and size) and adapts its structural stylesheet (`complete`/`standard`/`reduced`/`mono`); manual flags (`--no-emoji`, `--no-color`, `--plain`) are no longer needed as in v1. CLI mode remains plain text (or `--json`) and independent of the terminal.

## 10. Exports

Reports are generated in `var/exports/` by default (runtime path; see `ARCHITECTURE.md`) or at the specified path (`--output` in CLI, dialog in TUI).

### JSON, source of truth

Complete scan structure (`ScanRun`), strictly JSON-serializable.

### Text, compact human report

Readable outside the terminal, without ANSI codes, with hierarchical structure.

### HTML, readable web report

Standalone report with inline CSS, viewable in any browser, shareable, and archivable.

## 11. History and comparison

Each scan is persisted (SQLite, `var/db/app.db`): history searchable by target, details of a previous run, comparison between two scans (findings appearing / resolved / unchanged / changed), and replay of a scan against the same target without re-entering it — features absent in v1 and added during the migration to Clean Architecture.

## 12. Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

Structure: `tests/unit/` (domain and application, no real I/O), `tests/integration/` (SQLite/real files, `pytest-httpserver` fake HTTP server), `tests/e2e/` (end-to-end CLI and TUI, `Textual.testing`).

## 13. Out of scope

- CVE scanning.
- Active SQLi, XSS, or RCE detection.
- Complex scanner-side authentication.
- Deep crawling.
- Fuzzing.
- Large-scale path brute-forcing.
- Simultaneous multi-target scanning.
- Aggressive parallelism.
- Web dashboard.

---

> Omega-scan — Observe, collect, interpret, report.  
> A posture scanner, not an attack tool.
