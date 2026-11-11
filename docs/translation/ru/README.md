<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Лицензия MIT (см. файл LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Сканер состояния веб-безопасности**

> Создано [kraynux](https://github.com/kraynux) для [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Официальная страница: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Скриншоты: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Интерфейс и экспортируемые отчёты доступны на **17 языках** — см. [Языки интерфейса](#языки-интерфейса).  
**Языки:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** — инструмент с TUI и CLI, который анализирует видимую гигиену настроек ваших служб HTTP/HTTPS. Он наблюдает, собирает факты, применяет правила интерпретации и выдаёт отчёты, по которым можно действовать, никогда не проводя активной атаки. Инструмент набора `omega-`, построенный по принципам Clean Architecture — все технические подробности см. в `ARCHITECTURE.md`.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ru/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ru/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ru/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ru/omega-scan/D.png" width="24%" />
</p>

## 1. Назначение и границы

Omega-scan — сканер состояния веб-безопасности для системного администрирования: быстро проверить видимую гигиену настроек службы HTTP/HTTPS на localhost, в локальной сети или на внешней цели, в том числе за туннелем вроде Tailscale Funnel.

### Что делает Omega-scan

- Собирает наблюдаемые факты: заголовки, cookie, методы HTTP, TLS, чувствительные пути, заголовки CORS.
- Применяет к этим фактам декларативные правила интерпретации.
- Выдаёт единообразные, обоснованные находки, по которым можно действовать.
- Показывает результат в TUI (Textual) или в CLI для сценариев и в трёх видах экспорта: JSON, текст, HTML.
- Распознаёт ложные срабатывания, особенно поведение catch-all и пути, защищённые аутентификацией.
- Подстраивается под контекст: прокси, туннель, несколько виртуальных хостов, SNI.
- Требует явного подтверждения права на сканирование любой цели, которая ещё не закреплена как разрешённая.
- Хранит постоянную историю сканирований по каждой цели, которые можно повторять и сравнивать во времени.

### Чего Omega-scan не делает

- Активное сканирование уязвимостей: никаких SQLi, XSS или RCE.
- Сканирование CVE.
- Перебор или массовый фаззинг.
- Глубокий обход сайтов (crawler).
- Агрессивное параллельное сканирование множества целей.
- Веб-панель.
- Аутентификацию на стороне сканера.

## 2. Установка

### Требования

- Python 3.10+
- Подключение к Интернету, для зависимостей и внешних сканирований

### Установка

Официальный архив поставляется в формате `.tar.gz`. Перед установкой проверьте его целостность:

```bash
sha256sum omega-scan.tar.gz
```

### Способ 1 — сценарий установки

```bash
[ -d omega-scan ] && echo "ℹ️ Уже распаковано здесь, шаг пропущен." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan уже существует, перемещение пропущено." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Способ 2 — полная устойчивая установка



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Создаёт виртуальное окружение `.venv`, если его ещё нет.
2. Устанавливает зависимости (`pip install -e .`; `pyproject.toml` остаётся единственным источником истины).
3. Делает `omega-scan.sh` и `install.sh` исполняемыми.
4. Добавляет псевдоним `scan` в `~/.bashrc` и `~/.zshrc` (без дублирования, если он уже есть).

### Зависимости

Объявлены в `pyproject.toml` (`requirements.txt` больше нет):
- `textual`: интерфейс TUI, темы, автоматическая подстройка под терминал
- `httpx`: современный клиент HTTP/HTTPS
- `jinja2`: шаблоны для экспорта в HTML
- Зависимости для разработки (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Использование

### Интерактивный режим (TUI)

Рекомендуется для повседневной работы — запускается без аргументов:

```bash
./omega-scan.sh
```

Порядок работы: заставка (закрывается нажатием клавиши или щелчком) → главное меню → ввод цели и выбор профиля (с подтверждением права на сканирование, если цель ещё не закреплена) → сканирование (индикатор хода и подробности сетевых операций в реальном времени) → результаты (общая оценка, находки с фильтром по категориям, подробности по щелчку на строке) → экспорт/история/сравнение из главного меню. Подстройка под терминал (цвета, размер, упрощение структуры) происходит автоматически; ручные параметры отображения больше не нужны.

#### Сочетания клавиш

| Клавиша | Действие |
|---|---|
| `↑` / `↓` | Переход между элементами экрана |
| `Tab` / `Shift+Tab` | Переход между полями формы |
| `Esc` | Возврат на предыдущий экран (подтверждение выхода на главном экране) |
| `t` | Следующая тема (применяется сразу, без подтверждения) |
| `r` | Обновить определение терминала |
| `a` | Показать справку |
| `q` | Выйти (с подтверждением) |

### Языки интерфейса

Интерфейс доступен на 17 языках: французском, английском, испанском, португальском (Бразилия), итальянском, немецком, нидерландском, польском, русском, упрощённом китайском, вьетнамском, тайском, индонезийском, японском, корейском, хинди и арабском. Язык выбирается в Настройках («Langue / Language») и применяется после перезапуска интерфейса; переменная `OMEGA_SCAN_LANG` (например, `OMEGA_SCAN_LANG=ru ./omega-scan.sh`) задаёт язык на один сеанс. При запуске из omega-suite omega-scan использует язык набора. В текстовой консоли Linux (TTY) языки с нелатинской письменностью на время сеанса показываются по-английски. Командная строка остаётся на французском.

### Контакты и поддержка

Справка (клавиша `a`) предлагает экран **Контакты и поддержка**: *Угостить кофе* (страница PayPal разработчика), *Связаться с поддержкой* (адрес электронной почты и контактная форма сайта, показанные открыто), *Зарегистрироваться как пользователь (анонимно)* и *Проверить обновления*. Регистрация добровольная, по умолчанию отключена и отправляется только один раз: она служит лишь для подсчёта пользователей и, по желанию, их континента или страны (закрытые списки, никогда не свободный текст). Отправляются случайно сгенерированный ключ, название программы (`omega-scan`) и её версия; никогда имя, имя машины, настройка, цель или результат. IP-адрес не сохраняется в регистрациях, но, как при любом посещении, проходит через проверки безопасности и журнал принимающего сервера. Отозвать регистрацию можно в любой момент на том же экране (*Больше не регистрировать меня*). Проверка обновлений лишь читает список версий, опубликованных на сайте, и никогда без щелчка.

### Режим для сценариев (CLI)

Любая подкоманда включает режим CLI (простой текст или JSON с `--json`):

```bash
# Сканировать цель (--authorize обязателен, если цель ещё не закреплена)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# История
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Экспорт
./omega-scan.sh export scan-30577411758e --format html --output otchet.html

# Цели, закреплённые как разрешённые (дальше --authorize не нужен)
./omega-scan.sh targets pin example.org --note "соглашение с клиентом 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Проверка права на сканирование цели

Ни одно сканирование не начинается без явного подтверждения права на цель (флажок в TUI, `--authorize` в CLI), если только цель уже не закреплена. Проверка выполняется на стороне приложения (`application/pipeline/guards/authorization_guard.py`), а не только в интерфейсе.

### Допустимые форматы цели

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 с портом
::1                         IPv6
[2001:db8::10]:8443         IPv6 в квадратных скобках с портом
example.org                 Имя хоста
intranet.lan:8080/admin     Имя хоста с портом и путём
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Профили сканирования

| Параметр | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Назначение | Быстрая проверка | Полное (по умолчанию) | Углублённое | localhost / локальная сеть |
| Тайм-аут соединения/чтения | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Методы HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Проверка путей | Нет | Да (~20) | Да (полная) | Да (~20) |
| TLS | Нет | Да | Да (подробно) | Да (мягко) |
| Зонд CORS | Нет | Да | Да | Да |
| Catch-all | - | Да | Да | Да |
| Политика HSTS | Не оценивается | Стандартная | Строгая | Мягкая |

### Когда какой профиль

- `quick`: молниеносная проверка перед вводом в эксплуатацию
- `standard`: полный аудит рабочей службы, рекомендуется
- `extended`: углублённый аудит, включая рискованные методы HTTP
- `local-lab`: сканирование localhost или локальной сети без штрафов по правилам для публичных служб, прежде всего HSTS

## 5. Архитектура

Omega-scan построен по принципам **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), согласованным с шаблоном набора `omega-` (см. `omega-stress`). Все подробности — дерево каталогов, правила зависимостей, функциональные цепочки, иерархия исключений, система именования — в **`ARCHITECTURE.md`**, нормативном справочном документе.

Очень краткий обзор:

```text
src/omega_scan/
├── domain/          Чистая предметная логика (цели, профили, сканирования, проверки, отчёты, темы...)
├── application/     Сценарии использования (commands/queries), конвейер выполнения, проверки допуска
├── ports/           Контракты, ожидаемые приложением (зонды, репозитории, экспортёры...)
├── infrastructure/  Конкретные реализации (httpx, SQLite; Textual здесь НЕТ)
├── interfaces/      tui/ (Textual) и cli/ (для сценариев), со строгим равенством возможностей
├── app/             Сборка (DependencyContainer, bootstrap, жизненный цикл)
├── core/, shared/   Общий словарь, вспомогательные средства вне предметной логики
└── plugins/         Структура заложена, пуста (ни одно направление расширения не подтверждено)
```

Правила проектирования, не менявшиеся с v1:
- `domain/checks/`: выносит оценку по доказательствам, никогда не обращается к сети.
- `infrastructure/network/`: работает с сетью, никогда не выносит оценок.
- `interfaces/`: отображает, не содержит предметной логики.
- `infrastructure/exporters/`: читают результат сканирования, ничего не пересчитывают.

## 6. Система правил

### Транспорт, `TRN-*`

- `TRN-HTTP-001`: HTTP доступен без перенаправления на HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS недоступен, `FAIL`
- `TRN-HSTS-001`: заголовок HSTS отсутствует, `FAIL`
- `TRN-HSTS-002`: малый `max-age` HSTS, меньше 1 года, `WARN`

### Глубина TLS, `TLS-*`

- `TLS-VERSION-001`: устаревший протокол TLS (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: явно слабый набор шифров (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Заголовки, `HDR-*`

- `HDR-CSP-001`: CSP отсутствует на HTML-странице, `FAIL`
- `HDR-CSP-002`: слишком либеральная CSP, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` отсутствует, `WARN`
- `HDR-SERVER-001`: раскрыт баннер `Server`, `WARN`
- `HDR-CACHE-001`: `Cache-Control` отсутствует или слишком либерален на HTML-странице, `WARN`

### Cookie, `COO-*`

- `COO-SECURE-001`: cookie в ответе HTTPS без атрибута `Secure`, `WARN`
- `COO-HTTPONLY-001`: cookie без атрибута `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: `SameSite` отсутствует или `None` без `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` вместе с `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: произвольный origin отражается как есть в `Access-Control-Allow-Origin`, `WARN`

### Методы HTTP, `MTH-*`

- `MTH-OPTIONS-001`: метод OPTIONS включён, `INFO`
- `MTH-TRACE-001`: метод TRACE включён, `WARN`
- `MTH-PUT-001`: метод PUT включён, `WARN`
- `MTH-DELETE-001`: метод DELETE включён, `WARN`
- `MTH-PATCH-001`: метод PATCH включён, `WARN`
- `MTH-CONNECT-001`: метод CONNECT включён, `WARN`

### Раскрытие, `EXR-*`

- `EXR-ADMIN-001`: административный путь доступен без аутентификации, `WARN`
- `EXR-SENSITIVE-001`: доступен чувствительный файл, `.env`, `.git`, `FAIL`

### Утечки сведений, `INF-*`

- `INF-BANNER-001`: раскрыты баннеры сервера, `WARN`
- `INF-ERROR-001`: подробные сообщения об ошибках, `WARN`
- `INF-STACK-001`: раскрыт стек вызовов (stack trace), `FAIL`
- `INF-ROBOTS-001`: присутствует файл `robots.txt`, `OK` для сведения
- `INF-HEADER-001`: слишком разговорчивые технические заголовки, `WARN`
- `INF-SECURITYTXT-001`: присутствует файл `/.well-known/security.txt`, `OK` для сведения

## 7. Политика доверия

| Уровень | Определение |
|---|---|
| `certain` | Прямое однозначное доказательство, прочитанное в ответе как есть: заголовок есть или нет, сырой код HTTP. |
| `high` | Ясное доказательство, но косвенный контекст: методы через OPTIONS, наблюдаемый cookie. |
| `medium` | Вывод, на который мог повлиять посредник: прокси, WAF, туннель. |
| `low` | Косвенное обнаружение, неоднозначное содержимое или ситуация `catch_all_suspected`. |

### Автоматическое понижение

- `catch_all_suspected = true`: доверие ограничено уровнем `low`
- `proxy_suspected = true`: доверие ограничено уровнем `medium`
- `observed_access_state = ambiguous`: доверие ограничено уровнем `low`

## 8. Обнаружение ложных срабатываний

### Поведение catch-all

Перед проверкой чувствительных путей Omega-scan генерирует маловероятный случайный путь. Если сервер отвечает на него `200 OK`, цель помечается `catch_all_suspected = true`, и все находки о раскрытии понижаются до `confidence = low`.

### Аутентификация или отсутствие

Защищённый путь — `401`, `403` или перенаправление на страницу входа — не помечается ни как отсутствующий, ни как раскрытый. Он помечается `N/A` с примечанием: «защищённый путь, наличие нельзя подтвердить без аутентификации».

### Прокси / туннель

Если обнаружены заголовки `X-Forwarded-*`, `Via` или `Forwarded`, `proxy_suspected` становится `true`, а доверие к соответствующим находкам — баннерам, TLS — ограничивается уровнем `medium`.

## 9. Совместимость с терминалами

TUI (Textual) автоматически определяет возможности терминала (цвет, размер) и соответственно подстраивает свою структурную таблицу стилей (`complete`/`standard`/`reduced`/`mono`) — никаких ручных параметров (`--no-emoji`, `--no-color`, `--plain`), как в v1. Режим CLI всегда остаётся простым текстом (или `--json`), независимо от терминала.

## 10. Экспорт

Текстовые и HTML-отчёты пишутся на языке, выбранном в Настройках («Язык экспорта», по умолчанию — язык интерфейса); JSON остаётся данными и не переводится. По умолчанию отчёты создаются в `var/exports/` (рабочий путь, см. `ARCHITECTURE.md`) или по указанному пути (`--output` в CLI, диалоговое окно в TUI).

### JSON — источник истины

Полная структура сканирования (`ScanRun`), строго сериализуемая в JSON.

### Текст — компактный отчёт для чтения

Читается вне терминала, без кодов ANSI, с иерархической структурой.

### HTML — удобочитаемый веб-отчёт

Самостоятельный отчёт со встроенным CSS: открывается в любом браузере, им можно делиться и хранить в архиве.

## 11. История и сравнение

Каждое сканирование сохраняется (SQLite, `var/db/app.db`): история по цели, подробности прошлого запуска, сравнение двух сканирований (находки появившиеся / устранённые / неизменные / изменённые) и повтор сканирования той же цели без повторного ввода — в v1 этого не было, добавлено при переходе на Clean Architecture.

## 12. Тесты

```bash
source .venv/bin/activate
pytest tests/ -v
```

Структура: `tests/unit/` (домен и приложение, без реального ввода-вывода), `tests/integration/` (настоящие SQLite/файлы, поддельный HTTP-сервер `pytest-httpserver`), `tests/e2e/` (CLI и TUI от начала до конца, `Textual.testing`).

## 13. Вне рамок

- Сканирование CVE
- Активное обнаружение SQLi, XSS, RCE
- Сложная аутентификация на стороне сканера
- Глубокий обход сайтов
- Фаззинг
- Массовый перебор путей
- Одновременное сканирование нескольких целей
- Агрессивный параллелизм
- Веб-панель

---

> Omega-scan — Наблюдать, собирать, интерпретировать, докладывать.  
> Сканер состояния безопасности, а не инструмент атаки.
