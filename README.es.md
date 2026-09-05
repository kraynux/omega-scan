<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencia MIT (consulta el archivo LICENSE) -->
<div align="center">
  <img src="docs/assets/omega-scan.png" alt="Omega-Scan" width="256">
</div>

# 🔍 OMEGA-SCAN

**Escáner de postura de seguridad web**

> Desarrollado por **kraynux** para **Omega-server**  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Página oficial: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Vista previa: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

**Idiomas:**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-scan** es una herramienta TUI + CLI que analiza la higiene de configuración visible de servicios HTTP/HTTPS. Observa y recopila hechos, aplica reglas interpretativas declarativas y produce informes prácticos sin realizar nunca un ataque activo. Es la tercera herramienta de la suite `omega-` (después de `omega-fire` y `omega-stress`) y está estructurada según Clean Architecture; consulta `ARCHITECTURE.md` para ver todos los detalles técnicos.

## 1. Visión y alcance

Omega-scan es un escáner de postura de seguridad web destinado a la administración de sistemas: comprueba rápidamente la higiene de configuración visible de un servicio HTTP/HTTPS en localhost, una LAN o un objetivo externo, incluidos objetivos situados detrás de un túnel como Tailscale Funnel.

### Qué hace Omega-scan

- Recopila hechos observables: cabeceras, cookies, métodos HTTP, TLS, rutas sensibles y cabeceras CORS.
- Aplica reglas interpretativas declarativas a esos hechos.
- Produce findings homogéneos, justificados y accionables.
- Presenta el resultado en una TUI de Textual o en un CLI programable, con tres formatos de exportación: JSON, texto y HTML.
- Detecta falsos positivos, especialmente comportamientos catch-all y rutas protegidas por autenticación.
- Se adapta al contexto: proxy, túnel, multi-vhost y SNI.
- Exige confirmación explícita de autorización antes de escanear cualquier objetivo que no esté fijado y autorizado.
- Conserva un historial persistente de escaneos por objetivo, que se puede repetir y comparar con el tiempo.

### Qué no hace Omega-scan

- No realiza escaneo activo de vulnerabilidades, SQLi, XSS ni RCE.
- No escanea CVE.
- No es una herramienta de bruteforce ni fuzzing masivo.
- No realiza crawling profundo.
- No ejecuta escaneos paralelos agresivos de múltiples objetivos.
- No proporciona un dashboard web.
- No realiza autenticación desde el escáner.

## 2. Instalación

### Requisitos

- Python 3.10+
- Conexión a Internet para las dependencias y los escaneos externos

### Instalación

El archivo oficial se proporciona en formato `.tar.gz`. Verifica su integridad antes de instalarlo:

```bash
sha256sum omega-scan.tar.gz
```

### Método 1 — script de instalación

```bash
[ -d omega-scan ] && echo "ℹ️ Ya está extraído aquí; se omite el paso." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan ya existe; se omite el desplazamiento." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Método 2 — instalación completa resistente

```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Crea el entorno virtual `.venv` si todavía no existe.
2. Instala las dependencias (`pip install -e .`; `pyproject.toml` sigue siendo la única fuente de verdad).
3. Hace ejecutables `omega-scan.sh` e `install.sh`.
4. Añade el alias `scan` a `~/.bashrc` y `~/.zshrc` sin duplicarlo.

### Dependencias

Declaradas en `pyproject.toml` (ya no existe `requirements.txt`):
- `textual`: TUI, temas y adaptación automática al terminal.
- `httpx`: cliente HTTP/HTTPS moderno.
- `jinja2`: plantillas para la exportación HTML.
- Dependencias de desarrollo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`.

## 3. Uso

### Modo interactivo (TUI)

Recomendado para el uso diario; se inicia sin argumentos:

```bash
./omega-scan.sh
```

Flujo: pantalla de inicio (se cierra con una tecla o un clic) → menú principal → introducción del objetivo y selección del perfil (con confirmación de autorización si el objetivo no está fijado) → escaneo (barra de progreso y operaciones de red en directo) → resultados (puntuación global, findings filtrables por categoría y detalles al hacer clic en una fila) → exportación, historial y comparación desde el menú principal. La adaptación al terminal (colores, tamaño y degradación estructural) es automática; ya no se necesitan flags manuales de visualización.

#### Atajos de teclado

| Tecla | Acción |
|---|---|
| `↑` / `↓` | Navegar entre los elementos de una pantalla |
| `Tab` / `Mayús+Tab` | Navegar entre los campos de un formulario |
| `Esc` | Volver a la pantalla anterior (confirmación de salida en la pantalla de inicio) |
| `t` | Siguiente tema (se aplica inmediatamente, sin confirmación) |
| `r` | Actualizar la detección del terminal |
| `a` | Mostrar la ayuda |
| `q` | Salir con confirmación |

### Modo programable (CLI)

Cualquier subcomando inicia el modo CLI (texto simple o JSON con `--json`):

```bash
# Escanear un objetivo (--authorize es obligatorio si no está fijado)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Historial
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Exportación
./omega-scan.sh export scan-30577411758e --format html --output informe.html

# Objetivos fijados y autorizados (no se necesita --authorize en escaneos posteriores)
./omega-scan.sh targets pin example.org --note "autorización del cliente 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Protección de autorización del objetivo

Ningún escaneo comienza sin una confirmación explícita de autorización del objetivo (casilla en la TUI, `--authorize` en CLI), salvo que el objetivo ya esté fijado. La comprobación se aplica en la aplicación (`application/pipeline/guards/authorization_guard.py`), no solo en la interfaz.

### Formatos de objetivo aceptados

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 con puerto
::1                         IPv6
[2001:db8::10]:8443         IPv6 entre corchetes y con puerto
example.org                 Nombre de host
intranet.lan:8080/admin     Nombre de host con puerto y ruta
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Perfiles de escaneo

| Parámetro | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Uso | Comprobación rápida | Completo (predeterminado) | Profundo | localhost / LAN |
| Tiempo de espera conexión/lectura | 3 s / 6 s | 3 s / 6 s | 5 s / 10 s | 3 s / 6 s |
| Métodos HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Sondeo de rutas | No | Sí (aprox. 20) | Sí (completo) | Sí (aprox. 20) |
| TLS | No | Sí | Sí (detallado) | Sí (tolerante) |
| Sonda CORS | No | Sí | Sí | Sí |
| Catch-all | — | Sí | Sí | Sí |
| Política HSTS | No evaluada | Estándar | Estricta | Tolerante |

### Cuándo usar cada perfil

- `quick`: comprobación rápida antes de poner en producción.
- `standard`: auditoría completa de un servicio en producción; recomendada.
- `extended`: auditoría profunda que incluye métodos HTTP arriesgados.
- `local-lab`: escaneo de localhost o LAN sin aplicar de forma demasiado estricta las reglas destinadas a servicios públicos, especialmente HSTS.

## 5. Arquitectura

Omega-scan sigue **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alineada con la plantilla de la suite `omega-` (consulta `omega-stress`). Todos los detalles — árbol, reglas de dependencia, cadenas funcionales, jerarquía de excepciones y taxonomía de nombres — están en **`ARCHITECTURE.md`**, el documento normativo de referencia.

```text
src/omega_scan/
├── domain/          Lógica de negocio pura (objetivos, perfiles, escaneos, comprobaciones, informes, temas...)
├── application/     Casos de uso (commands/queries), pipeline de ejecución y guards
├── ports/           Contratos esperados por la aplicación (probers, repositories, exporters...)
├── infrastructure/  Implementaciones concretas (httpx, SQLite; Textual NO está aquí)
├── interfaces/      tui/ (Textual) y cli/ (programable), con estricta paridad funcional
├── app/             Ensamblaje (DependencyContainer, bootstrap y ciclo de vida)
├── core/, shared/   Vocabulario transversal y utilidades no pertenecientes al dominio
└── plugins/         Estructura preparada y vacía (sin eje de extensión confirmado)
```

Reglas de diseño sin cambios desde la v1:
- `domain/checks/`: juzga a partir de las pruebas y nunca hace operaciones de red.
- `infrastructure/network/`: realiza operaciones de red y nunca juzga.
- `interfaces/`: muestra datos y no contiene lógica de negocio.
- `infrastructure/exporters/`: lee los resultados del escaneo y nunca los recalcula.

## 6. Taxonomía de reglas

### Transporte, `TRN-*`

- `TRN-HTTP-001`: HTTP accesible sin redirección a HTTPS, `WARN`.
- `TRN-HTTPS-001`: HTTPS inaccesible, `FAIL`.
- `TRN-HSTS-001`: cabecera HSTS ausente, `FAIL`.
- `TRN-HSTS-002`: `max-age` de HSTS bajo, inferior a un año, `WARN`.

### Profundidad TLS, `TLS-*`

- `TLS-VERSION-001`: protocolo TLS obsoleto (< TLSv1.2), `FAIL`.
- `TLS-CIPHER-001`: conjunto criptográfico claramente débil (RC4, DES, NULL, EXPORT, MD5), `WARN`.

### Cabeceras, `HDR-*`

- `HDR-CSP-001`: CSP ausente en una página HTML, `FAIL`.
- `HDR-CSP-002`: CSP demasiado permisiva, `WARN`.
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` ausente, `WARN`.
- `HDR-SERVER-001`: banner `Server` expuesto, `WARN`.
- `HDR-CACHE-001`: `Cache-Control` ausente o permisiva en una página HTML, `WARN`.

### Cookies, `COO-*`

- `COO-SECURE-001`: cookie en una respuesta HTTPS sin atributo `Secure`, `WARN`.
- `COO-HTTPONLY-001`: cookie sin atributo `HttpOnly`, `WARN`.
- `COO-SAMESITE-001`: `SameSite` ausente o `None` sin `Secure`, `WARN`.

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` combinado con `Access-Control-Allow-Credentials: true`, `FAIL`.
- `COR-REFLECTED-ORIGIN-001`: un origen arbitrario se refleja tal cual en `Access-Control-Allow-Origin`, `WARN`.

### Métodos HTTP, `MTH-*`

- `MTH-OPTIONS-001`: método OPTIONS habilitado, `INFO`.
- `MTH-TRACE-001`: método TRACE habilitado, `WARN`.
- `MTH-PUT-001`: método PUT habilitado, `WARN`.
- `MTH-DELETE-001`: método DELETE habilitado, `WARN`.
- `MTH-PATCH-001`: método PATCH habilitado, `WARN`.
- `MTH-CONNECT-001`: método CONNECT habilitado, `WARN`.

### Exposición, `EXR-*`

- `EXR-ADMIN-001`: ruta administrativa accesible sin autenticación, `WARN`.
- `EXR-SENSITIVE-001`: archivo sensible accesible (`.env`, `.git`), `FAIL`.

### Fugas de información, `INF-*`

- `INF-BANNER-001`: banners del servidor expuestos, `WARN`.
- `INF-ERROR-001`: mensajes de error detallados, `WARN`.
- `INF-STACK-001`: stack trace expuesto, `FAIL`.
- `INF-ROBOTS-001`: `robots.txt` presente, `OK` informativo.
- `INF-HEADER-001`: cabeceras técnicas demasiado verbosas, `WARN`.
- `INF-SECURITYTXT-001`: `/.well-known/security.txt` presente, `OK` informativo.

## 7. Política de confianza

| Nivel | Definición |
|---|---|
| `certain` | Prueba directa e inequívoca leída tal cual en la respuesta: cabecera presente o ausente, código HTTP sin procesar. |
| `high` | Prueba clara con contexto indirecto: métodos obtenidos mediante OPTIONS o cookie observada. |
| `medium` | El resultado puede estar influido por un intermediario, proxy, WAF o túnel. |
| `low` | Detección indirecta, contenido ambiguo o estado `catch_all_suspected`. |

### Degradaciones automáticas

- `catch_all_suspected = true`: la confianza queda limitada a `low`.
- `proxy_suspected = true`: la confianza queda limitada a `medium`.
- `observed_access_state = ambiguous`: la confianza queda limitada a `low`.

## 8. Detección de falsos positivos

### Comportamiento catch-all

Antes de probar rutas sensibles, Omega-scan genera una ruta aleatoria improbable. Si el servidor responde `200 OK`, el objetivo se marca como `catch_all_suspected = true` y todos los findings de exposición se degradan a `confidence = low`.

### Autenticación frente a ausencia

Una ruta protegida, una respuesta `401`, `403` o una redirección al inicio de sesión no se marca ni como ausente ni como expuesta. Se marca `N/A` con la nota: «ruta protegida; no se puede confirmar su presencia sin autenticación».

### Proxy / túnel

Si se detectan cabeceras `X-Forwarded-*`, `Via` o `Forwarded`, `proxy_suspected` pasa a `true` y la confianza de los findings relacionados (banners, TLS) queda limitada a `medium`.

## 9. Compatibilidad con terminales

La TUI de Textual detecta automáticamente las capacidades del terminal (color y tamaño) y adapta su hoja de estilos estructural (`complete`/`standard`/`reduced`/`mono`); ya no se necesitan flags manuales (`--no-emoji`, `--no-color`, `--plain`) como en la v1. El modo CLI sigue usando texto simple (o `--json`) y es independiente del terminal.

## 10. Exportaciones

Los informes se generan por defecto en `var/exports/` (ruta de ejecución; consulta `ARCHITECTURE.md`) o en la ruta indicada (`--output` en CLI, diálogo en TUI).

### JSON, fuente de verdad

Estructura completa del escaneo (`ScanRun`), estrictamente serializable como JSON.

### Texto, informe humano compacto

Legible fuera del terminal, sin códigos ANSI y con estructura jerárquica.

### HTML, informe web legible

Informe autónomo con CSS integrado, visible en cualquier navegador, fácil de compartir y archivar.

## 11. Historial y comparación

Cada escaneo se persiste en SQLite (`var/db/app.db`): historial consultable por objetivo, detalle de ejecuciones anteriores, comparación entre dos escaneos (findings aparecidos, resueltos, sin cambios o modificados) y repetición de un escaneo sobre el mismo objetivo sin volver a introducirlo. Estas funciones no existían en la v1 y se añadieron durante la migración a Clean Architecture.

## 12. Pruebas

```bash
source .venv/bin/activate
pytest tests/ -v
```

Estructura: `tests/unit/` (dominio y aplicación, sin I/O real), `tests/integration/` (SQLite/archivos reales, servidor HTTP ficticio `pytest-httpserver`) y `tests/e2e/` (CLI y TUI de extremo a extremo, `Textual.testing`).

## 13. Fuera del alcance

- Escaneo de CVE.
- Detección activa de SQLi, XSS y RCE.
- Autenticación compleja desde el escáner.
- Crawling profundo.
- Fuzzing.
- Bruteforce masivo de rutas.
- Escaneo simultáneo de múltiples objetivos.
- Paralelismo agresivo.
- Dashboard web.

---

> Omega-scan — observar, recopilar, interpretar e informar.  
> Un escáner de postura, no una herramienta de ataque.
