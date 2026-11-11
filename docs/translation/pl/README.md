<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencja MIT (zobacz plik LICENCE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan.png" alt="Omega-Scan" width="512">
</div>

# 🔍 OMEGA-SCAN

**Skaner stanu bezpieczeństwa usług WWW**

> Stworzone przez [kraynux](https://github.com/kraynux) dla [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Oficjalna strona: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Podgląd: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interfejs i eksportowane raporty dostępne w **17 językach** — zobacz [Języki interfejsu](#języki-interfejsu).  
**Języki:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** to narzędzie TUI + CLI, które analizuje widoczną higienę konfiguracji Twoich usług HTTP/HTTPS. Obserwuje, zbiera fakty, stosuje reguły interpretacyjne i tworzy raporty, na podstawie których można działać, nigdy nie przeprowadzając aktywnego ataku. Narzędzie pakietu `omega-`, zbudowane zgodnie z Clean Architecture — pełne szczegóły techniczne w `ARCHITECTURE.md`.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-scan/D.png" width="24%" />
</p>

## 1. Wizja i zakres

Omega-scan to skaner stanu bezpieczeństwa usług WWW przeznaczony do administracji systemami: szybko sprawdzić widoczną higienę konfiguracji usługi HTTP/HTTPS na localhost, w sieci LAN lub na celu zewnętrznym, także za tunelem takim jak Tailscale Funnel.

### Co robi Omega-scan

- Zbiera obserwowalne fakty: nagłówki, ciasteczka, metody HTTP, TLS, wrażliwe ścieżki, nagłówki CORS.
- Stosuje do tych faktów deklaratywne reguły interpretacyjne.
- Tworzy jednolite, uzasadnione ustalenia, na podstawie których można działać.
- Przedstawia wynik w TUI (Textual) lub w skryptowalnym CLI oraz w trzech eksportach: JSON, tekst, HTML.
- Wykrywa fałszywe alarmy, zwłaszcza zachowanie typu catch-all i ścieżki chronione uwierzytelnianiem.
- Dostosowuje się do kontekstu: proxy, tunel, multi-vhost, SNI.
- Wymaga wyraźnego potwierdzenia autoryzacji przed skanem każdego celu, który nie jest jeszcze przypięty jako autoryzowany.
- Prowadzi trwałą historię skanów dla każdego celu, którą można odtwarzać i porównywać w czasie.

### Czego Omega-scan nie robi

- Aktywnego skanowania podatności: bez SQLi, XSS czy RCE.
- Skanowania CVE.
- Narzędzia do brute force ani masowego fuzzingu.
- Głębokiego crawlera.
- Agresywnego narzędzia do równoległego skanowania wielu celów.
- Panelu WWW.
- Uwierzytelniania po stronie skanera.

## 2. Instalacja

### Wymagania

- Python 3.10+
- Połączenie z Internetem, dla zależności i skanów zewnętrznych

### Instalacja

Oficjalne archiwum jest dostarczane w formacie `.tar.gz`. Przed instalacją sprawdź jego integralność:

```bash
sha256sum omega-scan.tar.gz
```

### Metoda 1 — skrypt instalacyjny

```bash
[ -d omega-scan ] && echo "ℹ️ Już tu rozpakowano, krok pominięty." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan już istnieje, przenoszenie pominięte." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Metoda 2 — pełna, odporna instalacja



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Tworzy środowisko wirtualne `.venv`, jeśli jeszcze nie istnieje.
2. Instaluje zależności (`pip install -e .`; `pyproject.toml` pozostaje jedynym źródłem prawdy).
3. Nadaje plikom `omega-scan.sh` i `install.sh` prawo wykonywania.
4. Dodaje alias `scan` do `~/.bashrc` i `~/.zshrc` (bez duplikatu, jeśli już istnieje).

### Zależności

Zadeklarowane w `pyproject.toml` (już bez `requirements.txt`):
- `textual`: interfejs TUI, motywy, automatyczne dopasowanie do terminala
- `httpx`: nowoczesny klient HTTP/HTTPS
- `jinja2`: szablony dla eksportu HTML
- Zależności deweloperskie (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Użycie

### Tryb interaktywny (TUI)

Zalecany do codziennego użytku — uruchamiany bez argumentów:

```bash
./omega-scan.sh
```

Przebieg: ekran startowy (zamyka się klawiszem lub kliknięciem) → menu główne → wprowadzenie celu i wybór profilu (z potwierdzeniem autoryzacji, jeśli cel nie jest jeszcze przypięty) → skan (wskaźnik postępu i szczegóły operacji sieciowych na bieżąco) → wyniki (ocena ogólna, ustalenia filtrowane według kategorii, szczegóły po kliknięciu wiersza) → eksport/historia/porównanie z menu głównego. Dopasowanie do terminala (kolory, rozmiar, uproszczenie struktury) jest automatyczne; ręczne opcje wyświetlania nie są już potrzebne.

#### Skróty klawiszowe

| Klawisz | Działanie |
|---|---|
| `↑` / `↓` | Przechodzenie między elementami ekranu |
| `Tab` / `Shift+Tab` | Przechodzenie między polami formularza |
| `Esc` | Powrót do poprzedniego ekranu (potwierdzenie wyjścia na ekranie głównym) |
| `t` | Następny motyw (stosowany od razu, bez potwierdzenia) |
| `r` | Odświeżenie wykrywania terminala |
| `a` | Wyświetlenie pomocy |
| `q` | Wyjście (z potwierdzeniem) |

### Języki interfejsu

Interfejs jest dostępny w 17 językach: francuskim, angielskim, hiszpańskim, portugalskim (Brazylia), włoskim, niemieckim, niderlandzkim, polskim, rosyjskim, chińskim uproszczonym, wietnamskim, tajskim, indonezyjskim, japońskim, koreańskim, hindi i arabskim. Wyboru dokonuje się w Ustawieniach („Langue / Language”), a zmiana obowiązuje po ponownym uruchomieniu interfejsu; zmienna `OMEGA_SCAN_LANG` (na przykład `OMEGA_SCAN_LANG=pl ./omega-scan.sh`) wymusza język na czas jednej sesji. Uruchomiony z omega-suite, omega-scan przejmuje język pakietu. W tekstowej konsoli Linuksa (TTY) języki o piśmie innym niż łacińskie są na czas sesji wyświetlane po angielsku. Wiersz poleceń pozostaje po francusku.

### Kontakt i wsparcie

Pomoc (klawisz `a`) oferuje ekran **Kontakt i wsparcie**: *Postaw kawę* (strona PayPal dewelopera), *Skontaktuj się ze wsparciem* (adres e-mail i formularz kontaktowy strony, wyświetlane jawnie), *Zgłoś mnie jako użytkownika (anonimowo)* oraz *Sprawdź aktualizacje*. Zgłoszenie jest dobrowolne, domyślnie wyłączone i wysyłane tylko raz: służy wyłącznie do liczenia użytkowników oraz, jeśli tego chcesz, ich kontynentu lub kraju (zamknięte listy, nigdy dowolny tekst). Wysyła losowo wygenerowany klucz, nazwę programu (`omega-scan`) i jego wersję; nigdy imienia i nazwiska, nazwy maszyny, ustawienia, celu ani wyniku. Adres IP nie jest zapisywany w zgłoszeniach, ale — jak przy każdej wizycie — przechodzi przez kontrole bezpieczeństwa i dziennik serwera odbiorczego. Wycofanie w dowolnym momencie z tego samego ekranu (*Nie zgłaszaj mnie więcej*). Sprawdzanie aktualizacji odczytuje jedynie listę wersji opublikowanych na stronie, i nigdy bez kliknięcia.

### Tryb skryptowy (CLI)

Każde podpolecenie włącza tryb CLI (zwykły tekst lub JSON z `--json`):

```bash
# Skanowanie celu (--authorize wymagane, jeśli cel nie jest jeszcze przypięty)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Historia
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Eksport
./omega-scan.sh export scan-30577411758e --format html --output raport.html

# Cele przypięte jako autoryzowane (bez --authorize przy kolejnych skanach)
./omega-scan.sh targets pin example.org --note "zgoda klienta 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Kontrola autoryzacji celu

Żaden skan nie rozpocznie się bez wyraźnego potwierdzenia autoryzacji dla celu (pole wyboru w TUI, `--authorize` w CLI), chyba że cel jest już przypięty. Sprawdzane po stronie aplikacji (`application/pipeline/guards/authorization_guard.py`), a nie tylko w interfejsie.

### Akceptowane formaty celu

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 z portem
::1                         IPv6
[2001:db8::10]:8443         IPv6 w nawiasach kwadratowych z portem
example.org                 Nazwa hosta
intranet.lan:8080/admin     Nazwa hosta z portem i ścieżką
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Profile skanowania

| Parametr | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Zastosowanie | Szybkie sprawdzenie | Pełny (domyślny) | Dogłębny | localhost / LAN |
| Limit czasu połączenia/odczytu | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Metody HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Sondowanie ścieżek | Nie | Tak (~20) | Tak (pełne) | Tak (~20) |
| TLS | Nie | Tak | Tak (szczegółowo) | Tak (tolerancyjnie) |
| Sonda CORS | Nie | Tak | Tak | Tak |
| Catch-all | - | Tak | Tak | Tak |
| Polityka HSTS | Nieoceniana | Standardowa | Ścisła | Tolerancyjna |

### Kiedy który profil

- `quick`: błyskawiczne sprawdzenie przed wdrożeniem na produkcję
- `standard`: pełny audyt usługi produkcyjnej, zalecany
- `extended`: dogłębny audyt obejmujący ryzykowne metody HTTP
- `local-lab`: skan localhost lub sieci LAN bez karania za reguły przeznaczone dla usług publicznych, zwłaszcza HSTS

## 5. Architektura

Omega-scan jest zbudowany zgodnie z **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), wzorowaną na szablonie pakietu `omega-` (zobacz `omega-stress`). Wszystkie szczegóły — drzewo katalogów, reguły zależności, łańcuchy funkcjonalne, hierarchia wyjątków, systematyka nazewnictwa — znajdują się w **`ARCHITECTURE.md`**, normatywnym dokumencie referencyjnym.

Bardzo krótki przegląd:

```text
src/omega_scan/
├── domain/          Czysta logika biznesowa (cele, profile, skany, checki, raporty, motywy...)
├── application/     Przypadki użycia (commands/queries), potok wykonania, kontrole
├── ports/           Kontrakty oczekiwane przez aplikację (sondy, repozytoria, eksportery...)
├── infrastructure/  Konkretne implementacje (httpx, SQLite; Textual NIE jest tutaj)
├── interfaces/      tui/ (Textual) i cli/ (skryptowalne), ze ścisłą równością funkcji
├── app/             Składanie (DependencyContainer, bootstrap, cykl życia)
├── core/, shared/   Wspólne słownictwo, narzędzia niezwiązane z logiką biznesową
└── plugins/         Struktura przygotowana, pusta (brak potwierdzonej osi rozszerzeń)
```

Zasady projektowe niezmienione od v1:
- `domain/checks/`: ocenia na podstawie dowodów, nigdy nie korzysta z sieci.
- `infrastructure/network/`: korzysta z sieci, nigdy nie ocenia.
- `interfaces/`: wyświetla, nie zawiera żadnej logiki biznesowej.
- `infrastructure/exporters/`: czytają wynik skanu, niczego nie przeliczają.

## 6. Systematyka reguł

### Transport, `TRN-*`

- `TRN-HTTP-001`: HTTP dostępny bez przekierowania na HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS niedostępny, `FAIL`
- `TRN-HSTS-001`: brak nagłówka HSTS, `FAIL`
- `TRN-HSTS-002`: niski `max-age` HSTS, poniżej 1 roku, `WARN`

### Głębokość TLS, `TLS-*`

- `TLS-VERSION-001`: przestarzały protokół TLS (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: wyraźnie słaby zestaw szyfrów (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Nagłówki, `HDR-*`

- `HDR-CSP-001`: brak CSP na stronie HTML, `FAIL`
- `HDR-CSP-002`: zbyt liberalna CSP, `WARN`
- `HDR-NOSNIFF-001`: brak `X-Content-Type-Options`, `WARN`
- `HDR-SERVER-001`: ujawniony baner `Server`, `WARN`
- `HDR-CACHE-001`: brak lub zbyt liberalny `Cache-Control` na stronie HTML, `WARN`

### Ciasteczka, `COO-*`

- `COO-SECURE-001`: ciasteczko w odpowiedzi HTTPS bez atrybutu `Secure`, `WARN`
- `COO-HTTPONLY-001`: ciasteczko bez atrybutu `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: brak `SameSite` albo `None` bez `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` w połączeniu z `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: dowolne źródło odbite bez zmian w `Access-Control-Allow-Origin`, `WARN`

### Metody HTTP, `MTH-*`

- `MTH-OPTIONS-001`: włączona metoda OPTIONS, `INFO`
- `MTH-TRACE-001`: włączona metoda TRACE, `WARN`
- `MTH-PUT-001`: włączona metoda PUT, `WARN`
- `MTH-DELETE-001`: włączona metoda DELETE, `WARN`
- `MTH-PATCH-001`: włączona metoda PATCH, `WARN`
- `MTH-CONNECT-001`: włączona metoda CONNECT, `WARN`

### Ekspozycja, `EXR-*`

- `EXR-ADMIN-001`: ścieżka administracyjna dostępna bez uwierzytelnienia, `WARN`
- `EXR-SENSITIVE-001`: dostępny wrażliwy plik, `.env`, `.git`, `FAIL`

### Wycieki informacji, `INF-*`

- `INF-BANNER-001`: ujawnione banery serwera, `WARN`
- `INF-ERROR-001`: szczegółowe komunikaty o błędach, `WARN`
- `INF-STACK-001`: ujawniony stos wywołań (stack trace), `FAIL`
- `INF-ROBOTS-001`: obecny plik `robots.txt`, `OK` informacyjnie
- `INF-HEADER-001`: zbyt gadatliwe nagłówki techniczne, `WARN`
- `INF-SECURITYTXT-001`: obecny plik `/.well-known/security.txt`, `OK` informacyjnie

## 7. Zasady pewności

| Poziom | Definicja |
|---|---|
| `certain` | Bezpośredni, jednoznaczny dowód odczytany wprost z odpowiedzi: nagłówek obecny lub nieobecny, surowy kod HTTP. |
| `high` | Jasny dowód, ale pośredni kontekst: metody przez OPTIONS, zaobserwowane ciasteczko. |
| `medium` | Ustalenie, na które mógł wpłynąć pośrednik: proxy, WAF, tunel. |
| `low` | Wykrycie pośrednie, niejednoznaczna treść lub sytuacja `catch_all_suspected`. |

### Automatyczne obniżenia

- `catch_all_suspected = true`: pewność ograniczona do `low`
- `proxy_suspected = true`: pewność ograniczona do `medium`
- `observed_access_state = ambiguous`: pewność ograniczona do `low`

## 8. Wykrywanie fałszywych alarmów

### Zachowanie catch-all

Przed testem wrażliwych ścieżek Omega-scan generuje nieprawdopodobną losową ścieżkę. Jeśli serwer odpowie na nią `200 OK`, cel zostaje oznaczony jako `catch_all_suspected = true`, a wszystkie ustalenia dotyczące ekspozycji są obniżane do `confidence = low`.

### Uwierzytelnienie a brak

Ścieżka chroniona — `401`, `403` lub przekierowanie na stronę logowania — nie jest oznaczana ani jako nieobecna, ani jako ujawniona. Otrzymuje oznaczenie `N/A` z uwagą: „ścieżka chroniona, obecności nie da się potwierdzić bez uwierzytelnienia”.

### Proxy / tunel

Jeśli wykryto nagłówki `X-Forwarded-*`, `Via` lub `Forwarded`, `proxy_suspected` przyjmuje wartość `true`, a pewność odnośnych ustaleń — banerów, TLS — zostaje ograniczona do `medium`.

## 9. Zgodność z terminalami

TUI (Textual) automatycznie wykrywa możliwości terminala (kolor, rozmiar) i odpowiednio dostosowuje swój strukturalny arkusz stylów (`complete`/`standard`/`reduced`/`mono`) — koniec z ręcznymi opcjami (`--no-emoji`, `--no-color`, `--plain`) jak w v1. Tryb CLI zawsze pozostaje zwykłym tekstem (lub `--json`), niezależnie od terminala.

## 10. Eksporty

Raporty tekstowe i HTML są zapisywane w języku wybranym w Ustawieniach („Język eksportów”, domyślnie język interfejsu); JSON pozostaje danymi i nie jest tłumaczony. Raporty są domyślnie tworzone w `var/exports/` (ścieżka robocza, zobacz `ARCHITECTURE.md`) albo pod wskazaną ścieżką (`--output` w CLI, okno dialogowe w TUI).

### JSON, źródło prawdy

Pełna struktura skanu (`ScanRun`), ściśle serializowalna do JSON.

### Tekst, zwięzły raport do czytania

Czytelny poza terminalem, bez kodów ANSI, z hierarchiczną strukturą.

### HTML, czytelny raport WWW

Samodzielny raport z wbudowanym CSS, do obejrzenia w każdej przeglądarce, do udostępnienia i archiwizacji.

## 11. Historia i porównanie

Każdy skan jest zapisywany (SQLite, `var/db/app.db`): historia przeglądana według celu, szczegóły dawnego uruchomienia, porównanie dwóch skanów (ustalenia nowe / rozwiązane / niezmienione / zmienione) i ponowne uruchomienie skanu na tym samym celu bez ponownego wpisywania — brakowało tego w v1, dodano przy migracji do Clean Architecture.

## 12. Testy

```bash
source .venv/bin/activate
pytest tests/ -v
```

Struktura: `tests/unit/` (domena i aplikacja, bez prawdziwych operacji wejścia/wyjścia), `tests/integration/` (prawdziwe SQLite/pliki, pozorowany serwer HTTP `pytest-httpserver`), `tests/e2e/` (CLI i TUI od początku do końca, `Textual.testing`).

## 13. Poza zakresem

- Skanowanie CVE
- Aktywne wykrywanie SQLi, XSS, RCE
- Złożone uwierzytelnianie po stronie skanera
- Głębokie crawlowanie
- Fuzzing
- Masowy brute force ścieżek
- Jednoczesne skanowanie wielu celów
- Agresywna równoległość
- Panel WWW

---

> Omega-scan — Obserwować, zbierać, interpretować, raportować.  
> Skaner stanu bezpieczeństwa, a nie narzędzie ataku.
