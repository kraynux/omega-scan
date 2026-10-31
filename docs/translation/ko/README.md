<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 라이선스 (LICENCE 파일 참조) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**웹 보안 상태 스캐너**

> [Omega-Server](https://kraynux.snake-mackarel.ts.net)를 위해 [kraynux](https://github.com/kraynux)가 개발   

공식 페이지: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; 미리보기: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 인터페이스와 내보낸 보고서는 **17개 언어**로 제공됩니다 — [인터페이스 언어](#인터페이스-언어) 참조.  
**언어:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan**은 HTTP/HTTPS 서비스의 겉으로 드러난 설정 위생 상태를 분석하는 TUI + CLI 도구입니다. 관찰하고, 사실을 수집하고, 해석 규칙을 적용해, 바로 조치할 수 있는 보고서를 만들며, 능동적인 공격은 절대 하지 않습니다. `omega-` 제품군의 도구이며 Clean Architecture로 구성되어 있습니다 — 기술적인 세부 사항은 모두 `ARCHITECTURE.md`를 참조하세요.

## 1. 비전과 범위

Omega-scan은 시스템 관리를 위한 웹 보안 상태 스캐너입니다: localhost, LAN, 외부 대상에 있는 HTTP/HTTPS 서비스의 겉으로 드러난 설정 위생 상태를 빠르게 확인하며, Tailscale Funnel 같은 터널 뒤에 있는 경우도 포함합니다.

### Omega-scan이 하는 일

- 관찰 가능한 사실을 수집합니다: 헤더, 쿠키, HTTP 메서드, TLS, 민감한 경로, CORS 헤더.
- 이 사실들에 선언적 해석 규칙을 적용합니다.
- 일관되고 근거가 있으며 조치 가능한 발견 사항을 만듭니다.
- 결과를 TUI(Textual) 또는 스크립트용 CLI로 보여 주며, 세 가지 내보내기(JSON, 텍스트, HTML)를 제공합니다.
- 오탐을 가려냅니다. 특히 catch-all 동작과 인증으로 보호되는 경로입니다.
- 상황에 맞춥니다: 프록시, 터널, 다중 vhost, SNI.
- 아직 허가된 대상으로 고정되지 않은 대상은 스캔 전에 반드시 명시적인 허가 확인을 요구합니다.
- 대상별 스캔 기록을 영구 보관하며, 다시 실행하고 시간에 따라 비교할 수 있습니다.

### Omega-scan이 하지 않는 일

- 능동적 취약점 스캔: SQLi, XSS, RCE 없음.
- CVE 스캔.
- 무차별 대입이나 대규모 퍼징 도구.
- 심층 크롤러.
- 공격적인 다중 대상 병렬 도구.
- 웹 대시보드.
- 스캐너 측 인증.

## 2. 설치

### 요구 사항

- Python 3.10+
- 의존성과 외부 스캔을 위한 인터넷 연결

### 설치

공식 아카이브는 `.tar.gz` 형식으로 제공됩니다. 설치 전에 무결성을 확인하세요:

```bash
sha256sum omega-scan.tar.gz
```

### 방법 1 — 설치 스크립트

```bash
[ -d omega-scan ] && echo "ℹ️ 이미 여기에 압축이 풀려 있어 이 단계를 건너뜁니다." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan이 이미 있어 이동을 건너뜁니다." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### 방법 2 — 견고한 전체 설치



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. 가상 환경 `.venv`가 아직 없으면 만듭니다.
2. 의존성을 설치합니다(`pip install -e .`; `pyproject.toml`이 유일한 기준 정보로 남습니다).
3. `omega-scan.sh`와 `install.sh`를 실행 가능하게 만듭니다.
4. 별칭 `scan`을 `~/.bashrc`와 `~/.zshrc`에 추가합니다(이미 있으면 중복하지 않습니다).

### 의존성

`pyproject.toml`에 선언(`requirements.txt`는 더 이상 없음):
- `textual`: TUI 인터페이스, 테마, 터미널 자동 적응
- `httpx`: 최신 HTTP/HTTPS 클라이언트
- `jinja2`: HTML 내보내기용 템플릿
- 개발 의존성(`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. 사용법

### 대화형 모드 (TUI)

일상적인 사용에 권장 — 인수 없이 실행합니다:

```bash
./omega-scan.sh
```

흐름: 시작 화면(키를 누르거나 클릭하면 닫힘) → 메인 메뉴 → 대상 입력과 프로필 선택(대상이 아직 고정되지 않았다면 허가 확인 포함) → 스캔(진행 표시와 네트워크 작업 세부 내용을 실시간 표시) → 결과(전체 등급, 범주별로 거를 수 있는 발견 사항, 줄을 클릭하면 상세) → 메인 메뉴에서 내보내기/기록/비교. 터미널에 대한 적응(색상, 크기, 구조 단순화)은 자동이며, 수동 표시 옵션은 더 이상 필요하지 않습니다.

#### 단축키

| 키 | 동작 |
|---|---|
| `↑` / `↓` | 화면의 항목 사이 이동 |
| `Tab` / `Shift+Tab` | 양식의 필드 사이 이동 |
| `Esc` | 이전 화면으로 돌아가기(홈 화면에서는 종료 확인) |
| `t` | 다음 테마(확인 없이 즉시 적용) |
| `r` | 터미널 감지 새로 고침 |
| `a` | 도움말 표시 |
| `q` | 종료(확인 후) |

### 인터페이스 언어

인터페이스는 17개 언어로 제공됩니다: 프랑스어, 영어, 스페인어, 포르투갈어(브라질), 이탈리아어, 독일어, 네덜란드어, 폴란드어, 러시아어, 중국어 간체, 베트남어, 태국어, 인도네시아어, 일본어, 한국어, 힌디어, 아랍어. 설정(“Langue / Language”)에서 선택하며 인터페이스를 다시 시작한 뒤 적용됩니다. 변수 `OMEGA_SCAN_LANG`(예: `OMEGA_SCAN_LANG=ko ./omega-scan.sh`)으로 한 세션 동안 언어를 강제할 수 있습니다. omega-suite에서 실행하면 omega-scan은 제품군의 언어를 사용합니다. Linux 텍스트 콘솔(TTY)에서는 라틴 문자가 아닌 언어가 해당 세션 동안 영어로 표시됩니다. 명령줄은 프랑스어로 유지됩니다.

### 스크립트 모드 (CLI)

하위 명령을 지정하면 CLI 모드가 됩니다(일반 텍스트, 또는 `--json`으로 JSON):

```bash
# 대상 스캔(대상이 아직 고정되지 않았다면 --authorize 필수)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# 기록
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# 내보내기
./omega-scan.sh export scan-30577411758e --format html --output report.html

# 허가된 대상으로 고정(이후 스캔에서는 --authorize 불필요)
./omega-scan.sh targets pin example.org --note "고객 합의 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### 대상 허가 보호 장치

대상이 이미 고정되어 있지 않은 한, 그 대상에 대한 명시적인 허가 확인(TUI에서는 체크박스, CLI에서는 `--authorize`) 없이는 어떤 스캔도 시작되지 않습니다. 이 확인은 인터페이스만이 아니라 애플리케이션 쪽(`application/pipeline/guards/authorization_guard.py`)에서 이루어집니다.

### 허용되는 대상 형식

```text
192.168.1.10                IPv4
192.168.1.10:8080           포트가 있는 IPv4
::1                         IPv6
[2001:db8::10]:8443         대괄호와 포트가 있는 IPv6
example.org                 호스트 이름
intranet.lan:8080/admin     포트와 경로가 있는 호스트 이름
http://example.org          HTTP URL
https://example.org/admin   HTTPS URL
```

## 4. 스캔 프로필

| 매개변수 | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| 용도 | 빠른 점검 | 전체(기본값) | 심층 | localhost / LAN |
| 연결/읽기 시간 제한 | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| HTTP 메서드 | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| 경로 탐색 | 아니요 | 예(약 20개) | 예(전체) | 예(약 20개) |
| TLS | 아니요 | 예 | 예(상세) | 예(관대) |
| CORS 프로브 | 아니요 | 예 | 예 | 예 |
| Catch-all | - | 예 | 예 | 예 |
| HSTS 정책 | 평가 안 함 | 표준 | 엄격 | 관대 |

### 언제 어떤 프로필을 쓸까

- `quick`: 운영 투입 전 번개 같은 점검
- `standard`: 운영 중인 서비스의 전체 감사, 권장
- `extended`: 위험한 HTTP 메서드까지 포함하는 심층 감사
- `local-lab`: localhost나 LAN 스캔. 공개 서비스용 규칙(특히 HSTS) 때문에 감점되지 않습니다

## 5. 아키텍처

Omega-scan은 **Clean Architecture**(domain / application / infrastructure / interfaces / ports / core / app / plugins / shared)로 구성되어 있으며, `omega-` 제품군의 템플릿(`omega-stress` 참조)에 맞춰져 있습니다. 전체 세부 사항 — 디렉터리 구조, 의존성 규칙, 기능 흐름, 예외 계층, 명명 체계 — 은 규범적 참조 문서인 **`ARCHITECTURE.md`**에 있습니다.

아주 짧은 개요:

```text
src/omega_scan/
├── domain/          순수 업무 로직(대상, 프로필, 스캔, 검사, 보고서, 테마...)
├── application/     사용 사례(commands/queries), 실행 파이프라인, 보호 장치
├── ports/           애플리케이션이 기대하는 계약(프로브, 저장소, 내보내기 도구...)
├── infrastructure/  구체 구현(httpx, SQLite; Textual은 여기에 없음)
├── interfaces/      tui/(Textual)와 cli/(스크립트용), 기능이 엄격히 동일
├── app/             조립(DependencyContainer, bootstrap, 수명 주기)
├── core/, shared/   공통 어휘, 업무 외 유틸리티
└── plugins/         구조만 마련됨, 비어 있음(확정된 확장 방향 없음)
```

v1 이후 바뀌지 않은 설계 규칙:
- `domain/checks/`: 증거를 바탕으로 판정하며, 네트워크에는 접근하지 않습니다.
- `infrastructure/network/`: 네트워크에 접근하며, 판정하지 않습니다.
- `interfaces/`: 표시만 하며 업무 로직을 담지 않습니다.
- `infrastructure/exporters/`: 스캔 결과를 읽기만 하며 아무것도 다시 계산하지 않습니다.

## 6. 규칙 체계

### 전송, `TRN-*`

- `TRN-HTTP-001`: HTTPS로 리디렉션되지 않고 HTTP로 접근 가능, `WARN`
- `TRN-HTTPS-001`: HTTPS로 접근 불가, `FAIL`
- `TRN-HSTS-001`: HSTS 헤더 없음, `FAIL`
- `TRN-HSTS-002`: HSTS `max-age`가 1년 미만으로 짧음, `WARN`

### TLS 깊이, `TLS-*`

- `TLS-VERSION-001`: 낡은 TLS 프로토콜(< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: 명백히 약한 암호 스위트(RC4, DES, NULL, EXPORT, MD5), `WARN`

### 헤더, `HDR-*`

- `HDR-CSP-001`: HTML 페이지에 CSP 없음, `FAIL`
- `HDR-CSP-002`: 지나치게 허용적인 CSP, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` 없음, `WARN`
- `HDR-SERVER-001`: `Server` 배너 노출, `WARN`
- `HDR-CACHE-001`: HTML 페이지에 `Cache-Control`이 없거나 지나치게 허용적, `WARN`

### 쿠키, `COO-*`

- `COO-SECURE-001`: HTTPS 응답의 쿠키에 `Secure` 속성 없음, `WARN`
- `COO-HTTPONLY-001`: 쿠키에 `HttpOnly` 속성 없음, `WARN`
- `COO-SAMESITE-001`: `SameSite` 없음, 또는 `Secure` 없이 `None`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *`와 `Access-Control-Allow-Credentials: true`의 조합, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: 임의의 출처가 `Access-Control-Allow-Origin`에 그대로 반사됨, `WARN`

### HTTP 메서드, `MTH-*`

- `MTH-OPTIONS-001`: OPTIONS 메서드 활성화, `INFO`
- `MTH-TRACE-001`: TRACE 메서드 활성화, `WARN`
- `MTH-PUT-001`: PUT 메서드 활성화, `WARN`
- `MTH-DELETE-001`: DELETE 메서드 활성화, `WARN`
- `MTH-PATCH-001`: PATCH 메서드 활성화, `WARN`
- `MTH-CONNECT-001`: CONNECT 메서드 활성화, `WARN`

### 노출, `EXR-*`

- `EXR-ADMIN-001`: 관리자 경로에 인증 없이 접근 가능, `WARN`
- `EXR-SENSITIVE-001`: 민감한 파일에 접근 가능, `.env`, `.git`, `FAIL`

### 정보 유출, `INF-*`

- `INF-BANNER-001`: 서버 배너 노출, `WARN`
- `INF-ERROR-001`: 상세한 오류 메시지, `WARN`
- `INF-STACK-001`: 스택 트레이스 노출, `FAIL`
- `INF-ROBOTS-001`: `robots.txt` 파일 있음, `OK` 참고용
- `INF-HEADER-001`: 정보를 과하게 드러내는 기술 헤더, `WARN`
- `INF-SECURITYTXT-001`: `/.well-known/security.txt` 파일 있음, `OK` 참고용

## 7. 신뢰 정책

| 수준 | 정의 |
|---|---|
| `certain` | 응답에서 그대로 읽은 직접적이고 모호하지 않은 증거: 헤더의 유무, 원시 HTTP 코드. |
| `high` | 증거는 명확하지만 맥락은 간접적: OPTIONS로 얻은 메서드, 관찰된 쿠키. |
| `medium` | 중간 장치의 영향을 받았을 수 있는 소견: 프록시, WAF, 터널. |
| `low` | 간접 탐지, 모호한 내용, 또는 `catch_all_suspected` 상황. |

### 자동 강등

- `catch_all_suspected = true`: 신뢰도 상한 `low`
- `proxy_suspected = true`: 신뢰도 상한 `medium`
- `observed_access_state = ambiguous`: 신뢰도 상한 `low`

## 8. 오탐 탐지

### catch-all 동작

민감한 경로를 시험하기 전에 Omega-scan은 존재할 리 없는 무작위 경로를 만듭니다. 서버가 여기에 `200 OK`로 응답하면 대상은 `catch_all_suspected = true`로 표시되고, 노출 관련 발견 사항은 모두 `confidence = low`로 강등됩니다.

### 인증인가, 없는 것인가

보호된 경로 — `401`, `403`, 또는 로그인 페이지로의 리디렉션 — 는 없다고도, 노출되었다고도 표시되지 않습니다. “보호된 경로, 인증 없이는 존재 여부를 확인할 수 없음”이라는 메모와 함께 `N/A`로 표시됩니다.

### 프록시 / 터널

`X-Forwarded-*`, `Via`, `Forwarded` 헤더가 감지되면 `proxy_suspected`가 `true`가 되고, 해당 발견 사항(배너, TLS)의 신뢰도 상한이 `medium`이 됩니다.

## 9. 터미널 호환성

TUI(Textual)는 터미널의 능력(색상, 크기)을 자동으로 감지하고 그에 맞게 구조 스타일시트(`complete`/`standard`/`reduced`/`mono`)를 조정합니다 — v1처럼 수동 옵션(`--no-emoji`, `--no-color`, `--plain`)이 더는 필요하지 않습니다. CLI 모드는 항상 일반 텍스트(또는 `--json`)이며 터미널과 무관합니다.

## 10. 내보내기

텍스트와 HTML 보고서는 설정에서 고른 언어로 작성됩니다(“내보내기 언어”, 기본값은 인터페이스와 같음). JSON은 데이터로 남으며 번역되지 않습니다. 보고서는 기본적으로 `var/exports/`에 생성되며(실행 경로, `ARCHITECTURE.md` 참조), 지정한 경로(CLI에서는 `--output`, TUI에서는 대화 상자)에 생성할 수도 있습니다.

### JSON, 기준 정보

스캔의 전체 구조(`ScanRun`), 엄격하게 JSON 직렬화 가능.

### 텍스트, 간결하고 읽기 쉬운 보고서

터미널 밖에서도 읽을 수 있으며, ANSI 코드가 없고 계층적으로 구성되어 있습니다.

### HTML, 읽기 쉬운 웹 보고서

인라인 CSS가 들어간 독립형 보고서로, 어떤 브라우저에서도 볼 수 있고 공유와 보관이 쉽습니다.

## 11. 기록과 비교

각 스캔은 저장됩니다(SQLite, `var/db/app.db`): 대상별 기록 조회, 지난 실행의 상세, 두 스캔의 비교(새로 나타남 / 해결됨 / 변화 없음 / 변경됨), 같은 대상에 대해 다시 입력하지 않고 스캔 다시 실행 — v1에는 없었고, Clean Architecture로 옮기면서 추가되었습니다.

## 12. 테스트

```bash
source .venv/bin/activate
pytest tests/ -v
```

구조: `tests/unit/`(실제 I/O 없는 도메인과 애플리케이션), `tests/integration/`(실제 SQLite/파일, 가짜 HTTP 서버 `pytest-httpserver`), `tests/e2e/`(처음부터 끝까지의 CLI와 TUI, `Textual.testing`).

## 13. 범위 밖

- CVE 스캔
- SQLi, XSS, RCE의 능동적 탐지
- 스캐너 측의 복잡한 인증
- 심층 크롤링
- 퍼징
- 대규모 경로 무차별 대입
- 여러 대상의 동시 스캔
- 공격적인 병렬 처리
- 웹 대시보드

---

> Omega-scan — 관찰하고, 수집하고, 해석하고, 보고한다.  
> 보안 상태 스캐너이지, 공격 도구가 아니다.
