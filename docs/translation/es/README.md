<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencia MIT (ver el archivo LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Escáner de postura de seguridad web**

> Desarrollado por [kraynux](https://github.com/kraynux) para [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Página oficial: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Capturas: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interfaz e informes exportados disponibles en **17 idiomas** — ver [Idiomas de la interfaz](#idiomas-de-la-interfaz).  
**Idiomas:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** es una herramienta TUI + CLI que analiza la higiene de configuración visible de sus servicios HTTP/HTTPS. Observa, recoge hechos, aplica reglas interpretativas y genera informes accionables, sin realizar nunca un ataque activo. Herramienta de la suite `omega-`, estructurada en Clean Architecture — ver `ARCHITECTURE.md` para todos los detalles técnicos.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-scan/D.png" width="24%" />
</p>

## 1. Visión y alcance

Omega-scan es un escáner de postura de seguridad web, pensado para la administración de sistemas: comprobar rápidamente la higiene de configuración visible de un servicio HTTP/HTTPS en localhost, en la LAN o en un objetivo externo, incluso detrás de un túnel como Tailscale Funnel.

### Lo que hace Omega-scan

- Recoge hechos observables: cabeceras, cookies, métodos HTTP, TLS, rutas sensibles, cabeceras CORS.
- Aplica reglas interpretativas declarativas sobre esos hechos.
- Genera hallazgos homogéneos, justificados y accionables.
- Presenta el resultado en TUI (Textual) o en CLI scriptable, y mediante tres exportaciones: JSON, texto, HTML.
- Detecta falsos positivos, en particular los comportamientos catch-all y las rutas protegidas por autenticación.
- Se adapta al contexto: proxy, túnel, multi-vhost, SNI.
- Exige una confirmación explícita de autorización antes de escanear cualquier objetivo que no esté ya fijado como autorizado.
- Conserva un historial persistente de escaneos por objetivo, repetible y comparable en el tiempo.

### Lo que Omega-scan no hace

- Escaneo activo de vulnerabilidades: nada de SQLi, XSS ni RCE.
- Escaneo de CVE.
- Herramienta de fuerza bruta o de fuzzing masivo.
- Rastreador (crawler) profundo.
- Herramienta multiobjetivo paralela agresiva.
- Panel web.
- Autenticación del lado del escáner.

## 2. Instalación

### Requisitos

- Python 3.10+
- Conexión a Internet, para las dependencias y los escaneos externos

### Instalación

El archivo oficial se distribuye en formato `.tar.gz`. Compruebe su integridad antes de instalar:

```bash
sha256sum omega-scan.tar.gz
```

### Método 1 — script de instalación

```bash
[ -d omega-scan ] && echo "ℹ️ Ya extraído aquí, paso omitido." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan ya existe, traslado omitido." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Método 2 — instalación completa resiliente



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Crea el entorno virtual `.venv` si aún no existe.
2. Instala las dependencias (`pip install -e .`; `pyproject.toml` sigue siendo la única fuente de verdad).
3. Hace ejecutables `omega-scan.sh` e `install.sh`.
4. Añade el alias `scan` a `~/.bashrc` y `~/.zshrc` (sin duplicado si ya está presente).

### Dependencias

Declaradas en `pyproject.toml` (ya sin `requirements.txt`):
- `textual`: interfaz TUI, temas, adaptación automática al terminal
- `httpx`: cliente HTTP/HTTPS moderno
- `jinja2`: plantillas para la exportación HTML
- Dependencias de desarrollo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Uso

### Modo interactivo (TUI)

Recomendado para el uso diario — se lanza sin argumentos:

```bash
./omega-scan.sh
```

Recorrido: pantalla de inicio (se cierra con una tecla o un clic) → menú principal → introducción del objetivo y elección del perfil (con confirmación de autorización si el objetivo no está ya fijado) → escaneo (indicador de progreso y detalle de las operaciones de red en directo) → resultados (nota global, hallazgos filtrables por categoría, detalle al hacer clic en una línea) → exportación/historial/comparación desde el menú principal. La adaptación al terminal (colores, tamaño, degradación estructural) es automática; ya no hacen falta opciones de visualización manuales.

#### Atajos de teclado

| Tecla | Acción |
|---|---|
| `↑` / `↓` | Moverse entre los elementos de una pantalla |
| `Tab` / `Mayús+Tab` | Moverse entre los campos de un formulario |
| `Esc` | Volver a la pantalla anterior (confirmación de salida en la pantalla de inicio) |
| `t` | Tema siguiente (aplicado de inmediato, sin confirmación) |
| `r` | Actualizar la detección del terminal |
| `a` | Mostrar la ayuda |
| `q` | Salir (con confirmación) |

### Idiomas de la interfaz

La interfaz está disponible en 17 idiomas: francés, inglés, español, portugués (Brasil), italiano, alemán, neerlandés, polaco, ruso, chino simplificado, vietnamita, tailandés, indonesio, japonés, coreano, hindi y árabe. La elección se hace en Ajustes («Langue / Language») y se aplica tras reiniciar la interfaz; la variable `OMEGA_SCAN_LANG` (por ejemplo `OMEGA_SCAN_LANG=es ./omega-scan.sh`) fuerza un idioma durante una sesión. Lanzado desde omega-suite, omega-scan adopta el idioma de la suite. En una consola de texto Linux (TTY), los idiomas de escritura no latina se muestran en inglés durante la sesión. La línea de comandos sigue en francés.

### Contacto y soporte

La ayuda (tecla `a`) ofrece una pantalla **Contacto y soporte**: *Invitar a un café* (página PayPal del desarrollador), *Contactar con el soporte* (dirección de correo y formulario de contacto del sitio, mostrados en claro), *Declararme usuario (anónimo)* y *Buscar actualizaciones*. La declaración es voluntaria, está desactivada por defecto y se envía una sola vez: solo sirve para contar a los usuarios y, si se desea, su continente o su país (listas cerradas, nunca texto libre). Envía una clave elegida al azar, el nombre del programa (`omega-scan`) y su versión; nunca un nombre, un nombre de máquina, un ajuste, un objetivo ni un resultado. La dirección IP no se registra en las declaraciones, pero, como en cualquier visita, pasa por los controles de seguridad y el registro del servidor de recepción. Retirada en cualquier momento desde la misma pantalla (*Dejar de declararme*). La búsqueda de actualizaciones solo lee la lista de versiones publicadas en el sitio, y nunca sin un clic.

### Modo scriptable (CLI)

Cualquier subcomando activa el modo CLI (texto simple, o JSON con `--json`):

```bash
# Escanear un objetivo (--authorize obligatorio si el objetivo no está ya fijado)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Historial
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Exportación
./omega-scan.sh export scan-30577411758e --format html --output informe.html

# Objetivos fijados como autorizados (sin --authorize en los escaneos siguientes)
./omega-scan.sh targets pin example.org --note "acuerdo con el cliente 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Control de autorización del objetivo

Ningún escaneo empieza sin una confirmación explícita de autorización sobre el objetivo (casilla en la TUI, `--authorize` en CLI), salvo si el objetivo ya está fijado. Se verifica del lado de la aplicación (`application/pipeline/guards/authorization_guard.py`), no solo en la interfaz.

### Formatos de objetivo aceptados

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 con puerto
::1                         IPv6
[2001:db8::10]:8443         IPv6 con corchetes y puerto
example.org                 Nombre de host
intranet.lan:8080/admin     Nombre de host con puerto y ruta
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Perfiles de escaneo

| Parámetro | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Uso | Comprobación rápida | Completo (por defecto) | Exhaustivo | localhost / LAN |
| Timeout de conexión/lectura | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Métodos HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Sondeo de rutas | No | Sí (~20) | Sí (completo) | Sí (~20) |
| TLS | No | Sí | Sí (detallado) | Sí (tolerante) |
| Sonda CORS | No | Sí | Sí | Sí |
| Catch-all | - | Sí | Sí | Sí |
| Política HSTS | No evaluada | Estándar | Estricta | Tolerante |

### Cuándo usar cada perfil

- `quick`: comprobación relámpago antes de pasar a producción
- `standard`: auditoría completa de un servicio en producción, recomendado
- `extended`: auditoría exhaustiva que incluye los métodos HTTP de riesgo
- `local-lab`: escaneo de localhost o de la LAN sin penalizar las reglas pensadas para servicios públicos, en particular HSTS

## 5. Arquitectura

Omega-scan está estructurado en **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alineada con la plantilla de la suite `omega-` (ver `omega-stress`). Todos los detalles — árbol de carpetas, reglas de dependencia, cadenas funcionales, jerarquía de excepciones, taxonomía de nombres — están en **`ARCHITECTURE.md`**, el documento normativo de referencia.

Vista general muy breve:

```text
src/omega_scan/
├── domain/          Lógica de negocio pura (objetivos, perfiles, escaneos, checks, informes, temas...)
├── application/     Casos de uso (commands/queries), pipeline de ejecución, controles
├── ports/           Contratos que espera la aplicación (sondas, repositorios, exportadores...)
├── infrastructure/  Implementaciones concretas (httpx, SQLite; Textual NO está aquí)
├── interfaces/      tui/ (Textual) y cli/ (scriptable), con paridad funcional estricta
├── app/             Ensamblaje (DependencyContainer, bootstrap, ciclo de vida)
├── core/, shared/   Vocabulario transversal, utilidades no de negocio
└── plugins/         Estructura preparada, vacía (ningún eje de extensión confirmado)
```

Reglas de diseño sin cambios desde la v1:
- `domain/checks/`: juzga a partir de las pruebas, nunca hace red.
- `infrastructure/network/`: hace red, nunca juzga.
- `interfaces/`: muestra, no contiene ninguna lógica de negocio.
- `infrastructure/exporters/`: leen el resultado del escaneo, no recalculan nada.

## 6. Taxonomía de las reglas

### Transporte, `TRN-*`

- `TRN-HTTP-001`: HTTP accesible sin redirección a HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS no accesible, `FAIL`
- `TRN-HSTS-001`: cabecera HSTS ausente, `FAIL`
- `TRN-HSTS-002`: `max-age` de HSTS bajo, inferior a 1 año, `WARN`

### Profundidad TLS, `TLS-*`

- `TLS-VERSION-001`: protocolo TLS obsoleto (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: suite criptográfica claramente débil (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Cabeceras, `HDR-*`

- `HDR-CSP-001`: CSP ausente en una página HTML, `FAIL`
- `HDR-CSP-002`: CSP demasiado permisiva, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` ausente, `WARN`
- `HDR-SERVER-001`: banner `Server` expuesto, `WARN`
- `HDR-CACHE-001`: `Cache-Control` ausente o permisivo en una página HTML, `WARN`

### Cookies, `COO-*`

- `COO-SECURE-001`: cookie en una respuesta HTTPS sin el atributo `Secure`, `WARN`
- `COO-HTTPONLY-001`: cookie sin el atributo `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: `SameSite` ausente, o `None` sin `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` combinado con `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: origen arbitrario reflejado tal cual en `Access-Control-Allow-Origin`, `WARN`

### Métodos HTTP, `MTH-*`

- `MTH-OPTIONS-001`: método OPTIONS activado, `INFO`
- `MTH-TRACE-001`: método TRACE activado, `WARN`
- `MTH-PUT-001`: método PUT activado, `WARN`
- `MTH-DELETE-001`: método DELETE activado, `WARN`
- `MTH-PATCH-001`: método PATCH activado, `WARN`
- `MTH-CONNECT-001`: método CONNECT activado, `WARN`

### Exposición, `EXR-*`

- `EXR-ADMIN-001`: ruta de administración accesible sin autenticación, `WARN`
- `EXR-SENSITIVE-001`: archivo sensible accesible, `.env`, `.git`, `FAIL`

### Fugas de información, `INF-*`

- `INF-BANNER-001`: banners del servidor expuestos, `WARN`
- `INF-ERROR-001`: mensajes de error detallados, `WARN`
- `INF-STACK-001`: traza de pila (stack trace) expuesta, `FAIL`
- `INF-ROBOTS-001`: archivo `robots.txt` presente, `OK` informativo
- `INF-HEADER-001`: cabeceras técnicas demasiado locuaces, `WARN`
- `INF-SECURITYTXT-001`: archivo `/.well-known/security.txt` presente, `OK` informativo

## 7. Política de confianza

| Nivel | Definición |
|---|---|
| `certain` | Prueba directa, sin ambigüedad, leída tal cual en la respuesta: cabecera presente o ausente, código HTTP en bruto. |
| `high` | Prueba clara pero de contexto indirecto: métodos vía OPTIONS, cookie observada. |
| `medium` | Constatación posiblemente influida por un intermediario: proxy, WAF, túnel. |
| `low` | Detección indirecta, contenido ambiguo o situación `catch_all_suspected`. |

### Degradaciones automáticas

- `catch_all_suspected = true`: confianza limitada a `low`
- `proxy_suspected = true`: confianza limitada a `medium`
- `observed_access_state = ambiguous`: confianza limitada a `low`

## 8. Detección de falsos positivos

### Comportamiento catch-all

Antes de probar las rutas sensibles, Omega-scan genera una ruta aleatoria improbable. Si el servidor responde `200 OK` a ella, el objetivo se marca como `catch_all_suspected = true` y todos los hallazgos de exposición se degradan a `confidence = low`.

### Autenticación frente a ausencia

Una ruta protegida — `401`, `403` o redirección a una página de inicio de sesión — no se marca ni como ausente ni como expuesta. Se marca `N/A` con la nota: «ruta protegida, presencia no confirmable sin autenticación».

### Proxy / túnel

Si se detectan cabeceras `X-Forwarded-*`, `Via` o `Forwarded`, `proxy_suspected` pasa a `true` y los hallazgos afectados — banners, TLS — ven su confianza limitada a `medium`.

## 9. Compatibilidad con terminales

La TUI (Textual) detecta automáticamente las capacidades del terminal (color, tamaño) y adapta en consecuencia su hoja de estilo estructural (`complete`/`standard`/`reduced`/`mono`) — se acabaron las opciones manuales (`--no-emoji`, `--no-color`, `--plain`) de la v1. El modo CLI siempre sigue en texto simple (o `--json`), independiente del terminal.

## 10. Exportaciones

Los informes de texto y HTML se escriben en el idioma elegido en Ajustes («Idioma de las exportaciones», por defecto el de la interfaz); el JSON sigue siendo un dato, sin traducir. Los informes se generan por defecto en `var/exports/` (ruta de ejecución, ver `ARCHITECTURE.md`), o en la ruta indicada (`--output` en CLI, cuadro de diálogo en la TUI).

### JSON, fuente de verdad

Estructura completa del escaneo (`ScanRun`), estrictamente serializable en JSON.

### Texto, informe legible compacto

Legible fuera del terminal, sin códigos ANSI, con estructura jerarquizada.

### HTML, informe web legible

Informe autónomo con CSS en línea, consultable en cualquier navegador, compartible y archivable.

## 11. Historial y comparación

Cada escaneo se guarda (SQLite, `var/db/app.db`): historial consultable por objetivo, detalle de una ejecución anterior, comparación entre dos escaneos (hallazgos aparecidos / resueltos / sin cambios / modificados) y repetición de un escaneo sobre el mismo objetivo sin volver a introducirlo — ausentes en la v1, añadidos durante la migración a Clean Architecture.

## 12. Pruebas

```bash
source .venv/bin/activate
pytest tests/ -v
```

Estructura: `tests/unit/` (dominio y aplicación, sin E/S real), `tests/integration/` (SQLite/archivos reales, servidor HTTP ficticio `pytest-httpserver`), `tests/e2e/` (CLI y TUI de extremo a extremo, `Textual.testing`).

## 13. Fuera de alcance

- Escaneo de CVE
- Detección activa de SQLi, XSS, RCE
- Autenticación compleja del lado del escáner
- Rastreo profundo
- Fuzzing
- Fuerza bruta masiva de rutas
- Escaneo simultáneo de varios objetivos
- Paralelismo agresivo
- Panel web

---

> Omega-scan — Observar, recoger, interpretar, informar.  
> Un escáner de postura, no una herramienta de ataque.
