<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT-licentie (zie het bestand LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Scanner van de webbeveiligingshouding**

> Gemaakt door [kraynux](https://github.com/kraynux) voor [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Officiële pagina: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Voorbeeld: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interface en geëxporteerde rapporten beschikbaar in **17 talen** — zie [Talen van de interface](#talen-van-de-interface).  
**Talen:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** is een TUI- en CLI-tool die de zichtbare configuratiehygiëne van uw HTTP/HTTPS-diensten analyseert. Hij observeert, verzamelt feiten, past interpretatieve regels toe en levert bruikbare rapporten, zonder ooit een actieve aanval uit te voeren. Tool van de suite `omega-`, opgebouwd volgens Clean Architecture — zie `ARCHITECTURE.md` voor alle technische details.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-scan/D.png" width="24%" />
</p>

## 1. Visie en reikwijdte

Omega-scan is een scanner van de webbeveiligingshouding, bedoeld voor systeembeheer: snel de zichtbare configuratiehygiëne van een HTTP/HTTPS-dienst controleren op localhost, in het LAN of op een extern doel, ook achter een tunnel zoals Tailscale Funnel.

### Wat Omega-scan doet

- Verzamelt waarneembare feiten: headers, cookies, HTTP-methoden, TLS, gevoelige paden, CORS-headers.
- Past declaratieve, interpretatieve regels toe op die feiten.
- Levert eenduidige, onderbouwde en bruikbare bevindingen.
- Toont het resultaat in de TUI (Textual) of in een scriptbare CLI, en via drie exports: JSON, tekst, HTML.
- Herkent valse positieven, met name catch-all-gedrag en paden die door authenticatie zijn beschermd.
- Past zich aan de context aan: proxy, tunnel, multi-vhost, SNI.
- Vraagt een uitdrukkelijke bevestiging van autorisatie voordat een doel wordt gescand dat nog niet als geautoriseerd is vastgepind.
- Bewaart per doel een blijvende geschiedenis van scans, opnieuw uit te voeren en in de tijd te vergelijken.

### Wat Omega-scan niet doet

- Actief scannen op kwetsbaarheden: geen SQLi, XSS of RCE.
- CVE-scans.
- Brute-force- of grootschalige fuzzingtool.
- Diepgaande crawler.
- Agressieve parallelle tool voor meerdere doelen.
- Webdashboard.
- Authenticatie aan de kant van de scanner.

## 2. Installatie

### Vereisten

- Python 3.10+
- Internetverbinding, voor de afhankelijkheden en externe scans

### Installatie

Het officiële archief wordt geleverd in `.tar.gz`-formaat. Controleer de integriteit vóór de installatie:

```bash
sha256sum omega-scan.tar.gz
```

### Methode 1 — installatiescript

```bash
[ -d omega-scan ] && echo "ℹ️ Hier al uitgepakt, stap overgeslagen." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan bestaat al, verplaatsen overgeslagen." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Methode 2 — robuuste volledige installatie



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Maakt de virtuele omgeving `.venv` aan als die nog niet bestaat.
2. Installeert de afhankelijkheden (`pip install -e .`; `pyproject.toml` blijft de enige bron van waarheid).
3. Maakt `omega-scan.sh` en `install.sh` uitvoerbaar.
4. Voegt de alias `scan` toe aan `~/.bashrc` en `~/.zshrc` (zonder dubbel als hij er al staat).

### Afhankelijkheden

Gedeclareerd in `pyproject.toml` (geen `requirements.txt` meer):
- `textual`: TUI-interface, thema's, automatische aanpassing aan de terminal
- `httpx`: moderne HTTP/HTTPS-client
- `jinja2`: templates voor de HTML-export
- Ontwikkelafhankelijkheden (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Gebruik

### Interactieve modus (TUI)

Aanbevolen voor dagelijks gebruik — gestart zonder argumenten:

```bash
./omega-scan.sh
```

Verloop: startscherm (sluit met een toets of een klik) → hoofdmenu → invoer van het doel en keuze van het profiel (met bevestiging van autorisatie als het doel nog niet is vastgepind) → scan (voortgangsbalk en details van de netwerkbewerkingen live) → resultaten (totaalscore, bevindingen te filteren per categorie, details door op een regel te klikken) → export/geschiedenis/vergelijking vanuit het hoofdmenu. De aanpassing aan de terminal (kleuren, grootte, structurele vereenvoudiging) gebeurt automatisch; handmatige weergaveopties zijn niet meer nodig.

#### Sneltoetsen

| Toets | Actie |
|---|---|
| `↑` / `↓` | Tussen de elementen van een scherm bewegen |
| `Tab` / `Shift+Tab` | Tussen de velden van een formulier bewegen |
| `Esc` | Terug naar het vorige scherm (bevestiging om af te sluiten op het startscherm) |
| `t` | Volgend thema (direct toegepast, zonder bevestiging) |
| `r` | Terminaldetectie vernieuwen |
| `a` | Help tonen |
| `q` | Afsluiten (met bevestiging) |

### Talen van de interface

De interface is beschikbaar in 17 talen: Frans, Engels, Spaans, Portugees (Brazilië), Italiaans, Duits, Nederlands, Pools, Russisch, vereenvoudigd Chinees, Vietnamees, Thai, Indonesisch, Japans, Koreaans, Hindi en Arabisch. De keuze gebeurt in de Instellingen („Langue / Language”) en geldt na een herstart van de interface; de variabele `OMEGA_SCAN_LANG` (bijvoorbeeld `OMEGA_SCAN_LANG=nl ./omega-scan.sh`) legt voor één sessie een taal op. Gestart vanuit omega-suite neemt omega-scan de taal van de suite over. Op een Linux-tekstconsole (TTY) worden talen met een niet-Latijns schrift voor die sessie in het Engels getoond. De opdrachtregel blijft in het Frans.

### Contact en ondersteuning

De hulp (toets `a`) biedt een scherm **Contact en ondersteuning**: *Trakteer op een koffie* (PayPal-pagina van de ontwikkelaar), *Contact opnemen met ondersteuning* (e-mailadres en contactformulier van de site, leesbaar weergegeven), *Mij aanmelden als gebruiker (anoniem)* en *Updates controleren*. De aanmelding is vrijwillig, standaard uitgeschakeld en wordt maar één keer verzonden: ze dient alleen om de gebruikers te tellen en, als u dat wilt, hun continent of land (gesloten lijsten, nooit vrije tekst). Ze verzendt een willekeurig gekozen sleutel, de naam van de software (`omega-scan`) en de versie; nooit een naam, een machinenaam, een instelling, een doel of een resultaat. Het IP-adres wordt niet opgeslagen in de aanmeldingen, maar gaat, zoals bij elk bezoek, door de beveiligingscontroles en het logboek van de ontvangende server. Intrekken kan op elk moment vanuit hetzelfde scherm (*Mij niet meer aanmelden*). De updatecontrole leest alleen de lijst van versies die op de site gepubliceerd zijn, en nooit zonder klik.

### Scriptbare modus (CLI)

Elke subopdracht activeert de CLI-modus (platte tekst, of JSON met `--json`):

```bash
# Een doel scannen (--authorize vereist als het doel nog niet is vastgepind)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Geschiedenis
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Export
./omega-scan.sh export scan-30577411758e --format html --output rapport.html

# Als geautoriseerd vastgepinde doelen (geen --authorize nodig bij latere scans)
./omega-scan.sh targets pin example.org --note "akkoord met klant 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Autorisatiecontrole van het doel

Geen enkele scan start zonder uitdrukkelijke bevestiging van autorisatie voor het doel (selectievakje in de TUI, `--authorize` in de CLI), behalve als het doel al is vastgepind. Gecontroleerd aan de kant van de applicatie (`application/pipeline/guards/authorization_guard.py`), niet alleen in de interface.

### Geaccepteerde doelformaten

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 met poort
::1                         IPv6
[2001:db8::10]:8443         IPv6 met vierkante haken en poort
example.org                 Hostnaam
intranet.lan:8080/admin     Hostnaam met poort en pad
http://example.org          HTTP-URL
https://example.org/admin   HTTPS-URL
```

## 4. Scanprofielen

| Parameter | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Gebruik | Snelle controle | Volledig (standaard) | Grondig | localhost / LAN |
| Time-out verbinden/lezen | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| HTTP-methoden | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Padonderzoek | Nee | Ja (~20) | Ja (volledig) | Ja (~20) |
| TLS | Nee | Ja | Ja (gedetailleerd) | Ja (tolerant) |
| CORS-sonde | Nee | Ja | Ja | Ja |
| Catch-all | - | Ja | Ja | Ja |
| HSTS-beleid | Niet beoordeeld | Standaard | Streng | Tolerant |

### Wanneer welk profiel

- `quick`: bliksemcontrole vóór de ingebruikname
- `standard`: volledige audit van een dienst in productie, aanbevolen
- `extended`: grondige audit inclusief riskante HTTP-methoden
- `local-lab`: scan van localhost of het LAN zonder de regels voor publieke diensten, met name HSTS, als tekortkoming mee te tellen

## 5. Architectuur

Omega-scan is opgebouwd volgens **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), afgestemd op het sjabloon van de suite `omega-` (zie `omega-stress`). Alle details — mappenstructuur, afhankelijkheidsregels, functionele ketens, uitzonderingshiërarchie, naamgevingsindeling — staan in **`ARCHITECTURE.md`**, het normatieve referentiedocument.

Zeer kort overzicht:

```text
src/omega_scan/
├── domain/          Pure bedrijfslogica (doelen, profielen, scans, checks, rapporten, thema's...)
├── application/     Use cases (commands/queries), uitvoeringspipeline, controles
├── ports/           Contracten die de applicatie verwacht (sondes, repositories, exporteurs...)
├── infrastructure/  Concrete implementaties (httpx, SQLite; Textual staat hier NIET)
├── interfaces/      tui/ (Textual) en cli/ (scriptbaar), met strikte functionele gelijkwaardigheid
├── app/             Samenstelling (DependencyContainer, bootstrap, levenscyclus)
├── core/, shared/   Gedeeld vocabulaire, niet-bedrijfsmatige hulpmiddelen
└── plugins/         Structuur aanwezig, leeg (geen bevestigde uitbreidingsas)
```

Ontwerpregels die sinds v1 ongewijzigd zijn:
- `domain/checks/`: oordeelt op basis van het bewijs, doet nooit netwerkverkeer.
- `infrastructure/network/`: doet het netwerkverkeer, oordeelt nooit.
- `interfaces/`: toont, bevat geen bedrijfslogica.
- `infrastructure/exporters/`: lezen het scanresultaat, herberekenen niets.

## 6. Indeling van de regels

### Transport, `TRN-*`

- `TRN-HTTP-001`: HTTP bereikbaar zonder omleiding naar HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS niet bereikbaar, `FAIL`
- `TRN-HSTS-001`: HSTS-header ontbreekt, `FAIL`
- `TRN-HSTS-002`: lage HSTS-`max-age`, korter dan 1 jaar, `WARN`

### TLS-diepte, `TLS-*`

- `TLS-VERSION-001`: verouderd TLS-protocol (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: duidelijk zwakke cipher suite (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Headers, `HDR-*`

- `HDR-CSP-001`: CSP ontbreekt op een HTML-pagina, `FAIL`
- `HDR-CSP-002`: te ruime CSP, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` ontbreekt, `WARN`
- `HDR-SERVER-001`: `Server`-banner zichtbaar, `WARN`
- `HDR-CACHE-001`: `Cache-Control` ontbreekt of is te ruim op een HTML-pagina, `WARN`

### Cookies, `COO-*`

- `COO-SECURE-001`: cookie in een HTTPS-antwoord zonder het attribuut `Secure`, `WARN`
- `COO-HTTPONLY-001`: cookie zonder het attribuut `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: `SameSite` ontbreekt, of `None` zonder `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` gecombineerd met `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: willekeurige origin ongewijzigd weerspiegeld in `Access-Control-Allow-Origin`, `WARN`

### HTTP-methoden, `MTH-*`

- `MTH-OPTIONS-001`: methode OPTIONS ingeschakeld, `INFO`
- `MTH-TRACE-001`: methode TRACE ingeschakeld, `WARN`
- `MTH-PUT-001`: methode PUT ingeschakeld, `WARN`
- `MTH-DELETE-001`: methode DELETE ingeschakeld, `WARN`
- `MTH-PATCH-001`: methode PATCH ingeschakeld, `WARN`
- `MTH-CONNECT-001`: methode CONNECT ingeschakeld, `WARN`

### Blootstelling, `EXR-*`

- `EXR-ADMIN-001`: beheerpad bereikbaar zonder authenticatie, `WARN`
- `EXR-SENSITIVE-001`: gevoelig bestand bereikbaar, `.env`, `.git`, `FAIL`

### Informatielekken, `INF-*`

- `INF-BANNER-001`: serverbanners zichtbaar, `WARN`
- `INF-ERROR-001`: gedetailleerde foutmeldingen, `WARN`
- `INF-STACK-001`: stacktrace zichtbaar, `FAIL`
- `INF-ROBOTS-001`: bestand `robots.txt` aanwezig, `OK` ter informatie
- `INF-HEADER-001`: te spraakzame technische headers, `WARN`
- `INF-SECURITYTXT-001`: bestand `/.well-known/security.txt` aanwezig, `OK` ter informatie

## 7. Vertrouwensbeleid

| Niveau | Definitie |
|---|---|
| `certain` | Direct, ondubbelzinnig bewijs, ongewijzigd uit het antwoord gelezen: header aanwezig of afwezig, ruwe HTTP-code. |
| `high` | Duidelijk bewijs maar indirecte context: methoden via OPTIONS, waargenomen cookie. |
| `medium` | Bevinding mogelijk beïnvloed door een tussenpartij: proxy, WAF, tunnel. |
| `low` | Indirecte detectie, dubbelzinnige inhoud of een situatie `catch_all_suspected`. |

### Automatische afwaarderingen

- `catch_all_suspected = true`: vertrouwen begrensd op `low`
- `proxy_suspected = true`: vertrouwen begrensd op `medium`
- `observed_access_state = ambiguous`: vertrouwen begrensd op `low`

## 8. Opsporing van valse positieven

### Catch-all-gedrag

Voordat de gevoelige paden worden getest, genereert Omega-scan een onwaarschijnlijk willekeurig pad. Antwoordt de server daarop met `200 OK`, dan wordt het doel gemarkeerd als `catch_all_suspected = true` en worden alle blootstellingsbevindingen afgewaardeerd naar `confidence = low`.

### Authenticatie of afwezigheid

Een beschermd pad — `401`, `403` of een omleiding naar een inlogpagina — wordt niet als afwezig en niet als blootgesteld gemarkeerd. Het wordt gemarkeerd als `N/A`, met de opmerking: „beschermd pad, aanwezigheid niet te bevestigen zonder authenticatie”.

### Proxy / tunnel

Worden de headers `X-Forwarded-*`, `Via` of `Forwarded` gedetecteerd, dan gaat `proxy_suspected` naar `true` en wordt het vertrouwen van de betrokken bevindingen — banners, TLS — begrensd op `medium`.

## 9. Compatibiliteit met terminals

De TUI (Textual) detecteert automatisch de mogelijkheden van de terminal (kleur, grootte) en past zijn structurele stijlblad daarop aan (`complete`/`standard`/`reduced`/`mono`) — geen handmatige opties (`--no-emoji`, `--no-color`, `--plain`) meer zoals in v1. De CLI-modus blijft altijd platte tekst (of `--json`), onafhankelijk van de terminal.

## 10. Exports

Tekst- en HTML-rapporten worden geschreven in de taal die in de Instellingen gekozen is („Taal van de exports”, standaard die van de interface); JSON blijft data en wordt niet vertaald. De rapporten worden standaard aangemaakt in `var/exports/` (runtimepad, zie `ARCHITECTURE.md`), of op het opgegeven pad (`--output` in de CLI, dialoogvenster in de TUI).

### JSON, de bron van waarheid

Volledige structuur van de scan (`ScanRun`), strikt JSON-serialiseerbaar.

### Tekst, compact leesbaar rapport

Leesbaar buiten de terminal, zonder ANSI-codes, met een hiërarchische opbouw.

### HTML, leesbaar webrapport

Zelfstandig rapport met inline CSS, te bekijken in elke browser, te delen en te archiveren.

## 11. Geschiedenis en vergelijking

Elke scan wordt opgeslagen (SQLite, `var/db/app.db`): geschiedenis raadpleegbaar per doel, details van een eerdere uitvoering, vergelijking tussen twee scans (bevindingen verschenen / opgelost / ongewijzigd / gewijzigd) en opnieuw uitvoeren van een scan op hetzelfde doel zonder het opnieuw in te voeren — ontbrak in v1, toegevoegd bij de migratie naar Clean Architecture.

## 12. Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

Structuur: `tests/unit/` (domein en applicatie, zonder echte I/O), `tests/integration/` (echte SQLite/bestanden, nagebootste HTTP-server `pytest-httpserver`), `tests/e2e/` (CLI en TUI van begin tot eind, `Textual.testing`).

## 13. Buiten de reikwijdte

- CVE-scans
- Actieve detectie van SQLi, XSS, RCE
- Complexe authenticatie aan de kant van de scanner
- Diepgaand crawlen
- Fuzzing
- Grootschalige brute force van paden
- Gelijktijdig scannen van meerdere doelen
- Agressief parallellisme
- Webdashboard

---

> Omega-scan — Observeren, verzamelen, interpreteren, rapporteren.  
> Een scanner van de beveiligingshouding, geen aanvalstool.
