<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licenza MIT (vedi il file LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Scanner della postura di sicurezza web**

> Realizzato da [kraynux](https://github.com/kraynux) per [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Pagina ufficiale: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Anteprima: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interfaccia e report esportati disponibili in **17 lingue** — vedi [Lingue dell'interfaccia](#lingue-dellinterfaccia).  
**Lingue:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** è uno strumento TUI + CLI che analizza l'igiene di configurazione visibile dei tuoi servizi HTTP/HTTPS. Osserva, raccoglie fatti, applica regole interpretative e produce report utilizzabili, senza mai effettuare un attacco attivo. Strumento della suite `omega-`, strutturato in Clean Architecture — vedi `ARCHITECTURE.md` per tutti i dettagli tecnici.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-scan/D.png" width="24%" />
</p>

## 1. Visione e perimetro

Omega-scan è uno scanner della postura di sicurezza web pensato per l'amministrazione di sistema: verificare rapidamente l'igiene di configurazione visibile di un servizio HTTP/HTTPS su localhost, sulla LAN o su una destinazione esterna, anche dietro un tunnel come Tailscale Funnel.

### Cosa fa Omega-scan

- Raccoglie fatti osservabili: intestazioni, cookie, metodi HTTP, TLS, percorsi sensibili, intestazioni CORS.
- Applica regole interpretative dichiarative a questi fatti.
- Produce rilievi omogenei, motivati e utilizzabili.
- Presenta il risultato in TUI (Textual) o in CLI scriptabile, e tramite tre esportazioni: JSON, testo, HTML.
- Rileva i falsi positivi, in particolare i comportamenti catch-all e i percorsi protetti da autenticazione.
- Si adatta al contesto: proxy, tunnel, multi-vhost, SNI.
- Richiede una conferma esplicita di autorizzazione prima di analizzare qualsiasi destinazione non già fissata come autorizzata.
- Conserva una cronologia persistente delle scansioni per destinazione, ripetibile e confrontabile nel tempo.

### Cosa non fa Omega-scan

- Scansione attiva delle vulnerabilità: niente SQLi, XSS o RCE.
- Scansione di CVE.
- Strumento di forza bruta o di fuzzing massivo.
- Crawler profondo.
- Strumento aggressivo su più destinazioni in parallelo.
- Dashboard web.
- Autenticazione lato scanner.

## 2. Installazione

### Prerequisiti

- Python 3.10+
- Connessione a Internet, per le dipendenze e le scansioni esterne

### Installazione

L'archivio ufficiale è fornito in formato `.tar.gz`. Verificane l'integrità prima dell'installazione:

```bash
sha256sum omega-scan.tar.gz
```

### Metodo 1 — script di installazione

```bash
[ -d omega-scan ] && echo "ℹ️ Già estratto qui, passaggio saltato." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan esiste già, spostamento saltato." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Metodo 2 — installazione completa resiliente



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Crea l'ambiente virtuale `.venv` se non esiste già.
2. Installa le dipendenze (`pip install -e .`; `pyproject.toml` resta l'unica fonte di verità).
3. Rende eseguibili `omega-scan.sh` e `install.sh`.
4. Aggiunge l'alias `scan` a `~/.bashrc` e `~/.zshrc` (senza duplicati se già presente).

### Dipendenze

Dichiarate in `pyproject.toml` (niente più `requirements.txt`):
- `textual`: interfaccia TUI, temi, adattamento automatico al terminale
- `httpx`: client HTTP/HTTPS moderno
- `jinja2`: template per l'esportazione HTML
- Dipendenze di sviluppo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Utilizzo

### Modalità interattiva (TUI)

Consigliata per l'uso quotidiano — avviata senza argomenti:

```bash
./omega-scan.sh
```

Percorso: schermata iniziale (si chiude con un tasto o un clic) → menu principale → inserimento della destinazione e scelta del profilo (con conferma di autorizzazione se la destinazione non è già fissata) → scansione (indicatore di avanzamento e dettaglio delle operazioni di rete in tempo reale) → risultati (voto complessivo, rilievi filtrabili per categoria, dettaglio al clic su una riga) → esportazione/cronologia/confronto dal menu principale. L'adattamento al terminale (colori, dimensioni, degradazione strutturale) è automatico; non servono più opzioni di visualizzazione manuali.

#### Scorciatoie da tastiera

| Tasto | Azione |
|---|---|
| `↑` / `↓` | Spostarsi tra gli elementi di una schermata |
| `Tab` / `Maiusc+Tab` | Spostarsi tra i campi di un modulo |
| `Esc` | Tornare alla schermata precedente (conferma di uscita nella schermata iniziale) |
| `t` | Tema successivo (applicato subito, senza conferma) |
| `r` | Aggiornare il rilevamento del terminale |
| `a` | Mostrare l'aiuto |
| `q` | Uscire (con conferma) |

### Lingue dell'interfaccia

L'interfaccia è disponibile in 17 lingue: francese, inglese, spagnolo, portoghese (Brasile), italiano, tedesco, olandese, polacco, russo, cinese semplificato, vietnamita, thailandese, indonesiano, giapponese, coreano, hindi e arabo. La scelta si fa nelle Impostazioni («Langue / Language») e vale dopo il riavvio dell'interfaccia; la variabile `OMEGA_SCAN_LANG` (per esempio `OMEGA_SCAN_LANG=it ./omega-scan.sh`) impone una lingua per una sessione. Avviato da omega-suite, omega-scan usa la lingua della suite. In una console di testo Linux (TTY), le lingue con scrittura non latina vengono mostrate in inglese per la sessione. La riga di comando resta in francese.

### Contatti e supporto

L'aiuto (tasto `a`) propone una schermata **Contatti e supporto**: *Offrire un caffè* (pagina PayPal dello sviluppatore), *Contattare il supporto* (indirizzo e-mail e modulo di contatto del sito, mostrati in chiaro), *Dichiararmi utente (anonimo)* e *Verifica aggiornamenti*. La dichiarazione è volontaria, disattivata per impostazione predefinita e inviata una sola volta: serve solo a contare gli utenti e, se lo si desidera, il loro continente o paese (elenchi chiusi, mai testo libero). Invia una chiave estratta a caso, il nome del software (`omega-scan`) e la sua versione; mai un nome, un nome di macchina, un'impostazione, un obiettivo o un risultato. L'indirizzo IP non viene registrato nelle dichiarazioni, ma, come per ogni visita, passa per i controlli di sicurezza e il registro del server di ricezione. Ritiro in qualsiasi momento dalla stessa schermata (*Non dichiararmi più*). La verifica degli aggiornamenti legge solo l'elenco delle versioni pubblicate sul sito, e mai senza un clic.

### Modalità scriptabile (CLI)

Qualsiasi sottocomando attiva la modalità CLI (testo semplice, o JSON con `--json`):

```bash
# Analizzare una destinazione (--authorize obbligatorio se la destinazione non è già fissata)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Cronologia
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Esportazione
./omega-scan.sh export scan-30577411758e --format html --output report.html

# Destinazioni fissate come autorizzate (niente --authorize nelle scansioni successive)
./omega-scan.sh targets pin example.org --note "accordo con il cliente 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Controllo di autorizzazione della destinazione

Nessuna scansione parte senza una conferma esplicita di autorizzazione sulla destinazione (casella di spunta in TUI, `--authorize` in CLI), a meno che la destinazione non sia già fissata. Il controllo avviene lato applicazione (`application/pipeline/guards/authorization_guard.py`), non solo nell'interfaccia.

### Formati di destinazione accettati

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 con porta
::1                         IPv6
[2001:db8::10]:8443         IPv6 con parentesi quadre e porta
example.org                 Nome host
intranet.lan:8080/admin     Nome host con porta e percorso
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Profili di scansione

| Parametro | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Uso | Verifica rapida | Completo (predefinito) | Approfondito | localhost / LAN |
| Timeout connessione/lettura | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Metodi HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Sondaggio dei percorsi | No | Sì (~20) | Sì (completo) | Sì (~20) |
| TLS | No | Sì | Sì (dettagliato) | Sì (tollerante) |
| Sonda CORS | No | Sì | Sì | Sì |
| Catch-all | - | Sì | Sì | Sì |
| Politica HSTS | Non valutata | Standard | Rigorosa | Tollerante |

### Quando usare quale profilo

- `quick`: verifica lampo prima della messa in produzione
- `standard`: audit completo di un servizio in produzione, consigliato
- `extended`: audit approfondito che include i metodi HTTP rischiosi
- `local-lab`: scansione di localhost o della LAN senza penalizzare le regole pensate per i servizi pubblici, in particolare HSTS

## 5. Architettura

Omega-scan è strutturato in **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), allineata al modello della suite `omega-` (vedi `omega-stress`). Tutti i dettagli — albero delle cartelle, regole di dipendenza, catene funzionali, gerarchia delle eccezioni, tassonomia dei nomi — sono in **`ARCHITECTURE.md`**, il documento normativo di riferimento.

Panoramica molto breve:

```text
src/omega_scan/
├── domain/          Logica di business pura (destinazioni, profili, scansioni, check, report, temi...)
├── application/     Casi d'uso (commands/queries), pipeline di esecuzione, controlli
├── ports/           Contratti attesi dall'applicazione (sonde, repository, esportatori...)
├── infrastructure/  Implementazioni concrete (httpx, SQLite; Textual NON è qui)
├── interfaces/      tui/ (Textual) e cli/ (scriptabile), con parità funzionale rigorosa
├── app/             Assemblaggio (DependencyContainer, bootstrap, ciclo di vita)
├── core/, shared/   Vocabolario trasversale, utilità non di business
└── plugins/         Struttura predisposta, vuota (nessun asse di estensione confermato)
```

Regole di progettazione invariate dalla v1:
- `domain/checks/`: giudica a partire dalle prove, non fa mai rete.
- `infrastructure/network/`: fa rete, non giudica mai.
- `interfaces/`: mostra, non contiene alcuna logica di business.
- `infrastructure/exporters/`: leggono il risultato della scansione, non ricalcolano nulla.

## 6. Tassonomia delle regole

### Trasporto, `TRN-*`

- `TRN-HTTP-001`: HTTP accessibile senza reindirizzamento a HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS non accessibile, `FAIL`
- `TRN-HSTS-001`: intestazione HSTS assente, `FAIL`
- `TRN-HSTS-002`: `max-age` di HSTS basso, inferiore a 1 anno, `WARN`

### Profondità TLS, `TLS-*`

- `TLS-VERSION-001`: protocollo TLS obsoleto (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: suite crittografica palesemente debole (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Intestazioni, `HDR-*`

- `HDR-CSP-001`: CSP assente su una pagina HTML, `FAIL`
- `HDR-CSP-002`: CSP troppo permissiva, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` assente, `WARN`
- `HDR-SERVER-001`: banner `Server` esposto, `WARN`
- `HDR-CACHE-001`: `Cache-Control` assente o permissivo su una pagina HTML, `WARN`

### Cookie, `COO-*`

- `COO-SECURE-001`: cookie su una risposta HTTPS senza l'attributo `Secure`, `WARN`
- `COO-HTTPONLY-001`: cookie senza l'attributo `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: `SameSite` assente, oppure `None` senza `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` combinato con `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: origine arbitraria riflessa così com'è in `Access-Control-Allow-Origin`, `WARN`

### Metodi HTTP, `MTH-*`

- `MTH-OPTIONS-001`: metodo OPTIONS attivo, `INFO`
- `MTH-TRACE-001`: metodo TRACE attivo, `WARN`
- `MTH-PUT-001`: metodo PUT attivo, `WARN`
- `MTH-DELETE-001`: metodo DELETE attivo, `WARN`
- `MTH-PATCH-001`: metodo PATCH attivo, `WARN`
- `MTH-CONNECT-001`: metodo CONNECT attivo, `WARN`

### Esposizione, `EXR-*`

- `EXR-ADMIN-001`: percorso di amministrazione accessibile senza autenticazione, `WARN`
- `EXR-SENSITIVE-001`: file sensibile accessibile, `.env`, `.git`, `FAIL`

### Fughe di informazioni, `INF-*`

- `INF-BANNER-001`: banner del server esposti, `WARN`
- `INF-ERROR-001`: messaggi di errore dettagliati, `WARN`
- `INF-STACK-001`: stack trace esposta, `FAIL`
- `INF-ROBOTS-001`: file `robots.txt` presente, `OK` informativo
- `INF-HEADER-001`: intestazioni tecniche troppo loquaci, `WARN`
- `INF-SECURITYTXT-001`: file `/.well-known/security.txt` presente, `OK` informativo

## 7. Politica di fiducia

| Livello | Definizione |
|---|---|
| `certain` | Prova diretta, non ambigua, letta così com'è nella risposta: intestazione presente o assente, codice HTTP grezzo. |
| `high` | Prova chiara ma contesto indiretto: metodi tramite OPTIONS, cookie osservato. |
| `medium` | Rilievo forse influenzato da un intermediario: proxy, WAF, tunnel. |
| `low` | Rilevamento indiretto, contenuto ambiguo o situazione `catch_all_suspected`. |

### Declassamenti automatici

- `catch_all_suspected = true`: fiducia limitata a `low`
- `proxy_suspected = true`: fiducia limitata a `medium`
- `observed_access_state = ambiguous`: fiducia limitata a `low`

## 8. Rilevamento dei falsi positivi

### Comportamento catch-all

Prima di testare i percorsi sensibili, Omega-scan genera un percorso casuale improbabile. Se il server risponde `200 OK`, la destinazione viene contrassegnata `catch_all_suspected = true` e tutti i rilievi di esposizione vengono declassati a `confidence = low`.

### Autenticazione o assenza

Un percorso protetto — `401`, `403` o reindirizzamento verso una pagina di accesso — non viene contrassegnato né come assente né come esposto. Viene contrassegnato `N/A` con la nota: «percorso protetto, presenza non confermabile senza autenticazione».

### Proxy / tunnel

Se vengono rilevate intestazioni `X-Forwarded-*`, `Via` o `Forwarded`, `proxy_suspected` passa a `true` e i rilievi interessati — banner, TLS — hanno la fiducia limitata a `medium`.

## 9. Compatibilità con i terminali

La TUI (Textual) rileva automaticamente le capacità del terminale (colore, dimensioni) e adatta di conseguenza il suo foglio di stile strutturale (`complete`/`standard`/`reduced`/`mono`) — niente più opzioni manuali (`--no-emoji`, `--no-color`, `--plain`) come nella v1. La modalità CLI resta sempre in testo semplice (o `--json`), indipendente dal terminale.

## 10. Esportazioni

I report testo e HTML vengono scritti nella lingua scelta nelle Impostazioni («Lingua delle esportazioni», per impostazione predefinita quella dell'interfaccia); il JSON resta un dato, non tradotto. I report vengono generati in `var/exports/` per impostazione predefinita (percorso di esecuzione, vedi `ARCHITECTURE.md`), oppure nel percorso indicato (`--output` in CLI, finestra di dialogo in TUI).

### JSON, fonte di verità

Struttura completa della scansione (`ScanRun`), rigorosamente serializzabile in JSON.

### Testo, report leggibile compatto

Leggibile fuori dal terminale, senza codici ANSI, con struttura gerarchica.

### HTML, report web leggibile

Report autonomo con CSS inline, consultabile in qualsiasi browser, condivisibile e archiviabile.

## 11. Cronologia e confronto

Ogni scansione viene salvata (SQLite, `var/db/app.db`): cronologia consultabile per destinazione, dettaglio di un'esecuzione passata, confronto tra due scansioni (rilievi comparsi / risolti / invariati / modificati) e ripetizione di una scansione sulla stessa destinazione senza reinserirla — assenti nella v1, aggiunti durante la migrazione a Clean Architecture.

## 12. Test

```bash
source .venv/bin/activate
pytest tests/ -v
```

Struttura: `tests/unit/` (dominio e applicazione, senza I/O reale), `tests/integration/` (SQLite/file reali, server HTTP fittizio `pytest-httpserver`), `tests/e2e/` (CLI e TUI end-to-end, `Textual.testing`).

## 13. Fuori perimetro

- Scansione di CVE
- Rilevamento attivo di SQLi, XSS, RCE
- Autenticazione complessa lato scanner
- Crawling profondo
- Fuzzing
- Forza bruta massiva dei percorsi
- Scansione simultanea di più destinazioni
- Parallelismo aggressivo
- Dashboard web

---

> Omega-scan — Osservare, raccogliere, interpretare, riferire.  
> Uno scanner di postura, non uno strumento d'attacco.
