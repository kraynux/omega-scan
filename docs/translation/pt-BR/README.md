<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licença MIT (ver o arquivo LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Scanner de postura de segurança web**

> Desenvolvido por **kraynux** para **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Página oficial: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Capturas de tela: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interface e relatórios exportados disponíveis em **17 idiomas** — veja [Idiomas da interface](#idiomas-da-interface).  
**Idiomas:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** é uma ferramenta TUI + CLI que analisa a higiene de configuração visível dos seus serviços HTTP/HTTPS. Ela observa, coleta fatos, aplica regras interpretativas e produz relatórios acionáveis, sem jamais realizar um ataque ativo. Ferramenta da suíte `omega-`, estruturada em Clean Architecture — veja `ARCHITECTURE.md` para todos os detalhes técnicos.

## 1. Visão e escopo

O Omega-scan é um scanner de postura de segurança web, voltado à administração de sistemas: verificar rapidamente a higiene de configuração visível de um serviço HTTP/HTTPS em localhost, na LAN ou em um alvo externo, inclusive por trás de um túnel como o Tailscale Funnel.

### O que o Omega-scan faz

- Coleta fatos observáveis: cabeçalhos, cookies, métodos HTTP, TLS, caminhos sensíveis, cabeçalhos CORS.
- Aplica regras interpretativas declarativas sobre esses fatos.
- Produz achados homogêneos, justificados e acionáveis.
- Apresenta o resultado em TUI (Textual) ou em CLI scriptável, e por meio de três exportações: JSON, texto, HTML.
- Detecta falsos positivos, em especial comportamentos catch-all e caminhos protegidos por autenticação.
- Adapta-se ao contexto: proxy, túnel, multi-vhost, SNI.
- Exige uma confirmação explícita de autorização antes de escanear qualquer alvo que ainda não esteja fixado como autorizado.
- Mantém um histórico persistente de escaneamentos por alvo, repetível e comparável ao longo do tempo.

### O que o Omega-scan não faz

- Varredura ativa de vulnerabilidades: nada de SQLi, XSS ou RCE.
- Varredura de CVE.
- Ferramenta de força bruta ou de fuzzing em massa.
- Rastreador (crawler) profundo.
- Ferramenta agressiva de vários alvos em paralelo.
- Painel web.
- Autenticação do lado do scanner.

## 2. Instalação

### Pré-requisitos

- Python 3.10+
- Conexão com a Internet, para as dependências e os escaneamentos externos

### Instalação

O arquivo oficial é distribuído no formato `.tar.gz`. Verifique sua integridade antes de instalar:

```bash
sha256sum omega-scan.tar.gz
```

### Método 1 — script de instalação

```bash
[ -d omega-scan ] && echo "ℹ️ Já extraído aqui, etapa ignorada." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan já existe, movimentação ignorada." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Método 2 — instalação completa resiliente



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Cria o ambiente virtual `.venv` se ele ainda não existir.
2. Instala as dependências (`pip install -e .`; `pyproject.toml` continua sendo a única fonte de verdade).
3. Torna `omega-scan.sh` e `install.sh` executáveis.
4. Adiciona o alias `scan` a `~/.bashrc` e `~/.zshrc` (sem duplicar se já existir).

### Dependências

Declaradas em `pyproject.toml` (sem mais `requirements.txt`):
- `textual`: interface TUI, temas, adaptação automática ao terminal
- `httpx`: cliente HTTP/HTTPS moderno
- `jinja2`: templates para a exportação HTML
- Dependências de desenvolvimento (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Uso

### Modo interativo (TUI)

Recomendado para o uso diário — iniciado sem argumentos:

```bash
./omega-scan.sh
```

Percurso: tela de abertura (fecha com uma tecla ou um clique) → menu principal → informar o alvo e escolher o perfil (com confirmação de autorização se o alvo ainda não estiver fixado) → escaneamento (indicador de progresso e detalhe das operações de rede ao vivo) → resultados (nota geral, achados filtráveis por categoria, detalhe ao clicar em uma linha) → exportação/histórico/comparação a partir do menu principal. A adaptação ao terminal (cores, tamanho, degradação estrutural) é automática; não são mais necessárias opções manuais de exibição.

#### Atalhos de teclado

| Tecla | Ação |
|---|---|
| `↑` / `↓` | Navegar entre os itens de uma tela |
| `Tab` / `Shift+Tab` | Navegar entre os campos de um formulário |
| `Esc` | Voltar à tela anterior (confirmação de saída na tela inicial) |
| `t` | Próximo tema (aplicado na hora, sem confirmação) |
| `r` | Atualizar a detecção do terminal |
| `a` | Mostrar a ajuda |
| `q` | Sair (com confirmação) |

### Idiomas da interface

A interface está disponível em 17 idiomas: francês, inglês, espanhol, português (Brasil), italiano, alemão, holandês, polonês, russo, chinês simplificado, vietnamita, tailandês, indonésio, japonês, coreano, hindi e árabe. A escolha é feita em Configurações («Langue / Language») e vale após reiniciar a interface; a variável `OMEGA_SCAN_LANG` (por exemplo `OMEGA_SCAN_LANG=pt-BR ./omega-scan.sh`) força um idioma durante uma sessão. Iniciado pelo omega-suite, o omega-scan usa o idioma da suíte. Em um console de texto Linux (TTY), os idiomas de escrita não latina aparecem em inglês durante a sessão. A linha de comando continua em francês.

### Modo scriptável (CLI)

Qualquer subcomando ativa o modo CLI (texto simples, ou JSON com `--json`):

```bash
# Escanear um alvo (--authorize obrigatório se o alvo ainda não estiver fixado)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Histórico
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Exportação
./omega-scan.sh export scan-30577411758e --format html --output relatorio.html

# Alvos fixados como autorizados (dispensam --authorize nos escaneamentos seguintes)
./omega-scan.sh targets pin example.org --note "acordo com o cliente 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Controle de autorização do alvo

Nenhum escaneamento começa sem uma confirmação explícita de autorização sobre o alvo (caixa de seleção na TUI, `--authorize` na CLI), a menos que o alvo já esteja fixado. A verificação é feita do lado da aplicação (`application/pipeline/guards/authorization_guard.py`), não apenas na interface.

### Formatos de alvo aceitos

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 com porta
::1                         IPv6
[2001:db8::10]:8443         IPv6 com colchetes e porta
example.org                 Nome de host
intranet.lan:8080/admin     Nome de host com porta e caminho
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Perfis de escaneamento

| Parâmetro | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Uso | Verificação rápida | Completo (padrão) | Aprofundado | localhost / LAN |
| Timeout de conexão/leitura | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Métodos HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Sondagem de caminhos | Não | Sim (~20) | Sim (completa) | Sim (~20) |
| TLS | Não | Sim | Sim (detalhado) | Sim (tolerante) |
| Sonda CORS | Não | Sim | Sim | Sim |
| Catch-all | - | Sim | Sim | Sim |
| Política HSTS | Não avaliada | Padrão | Rígida | Tolerante |

### Quando usar cada perfil

- `quick`: verificação relâmpago antes de ir para produção
- `standard`: auditoria completa de um serviço em produção, recomendado
- `extended`: auditoria aprofundada incluindo os métodos HTTP de risco
- `local-lab`: escaneamento de localhost ou da LAN sem penalizar regras pensadas para serviços públicos, em especial HSTS

## 5. Arquitetura

O Omega-scan é estruturado em **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alinhada ao modelo da suíte `omega-` (veja `omega-stress`). Todos os detalhes — árvore de pastas, regras de dependência, cadeias funcionais, hierarquia de exceções, taxonomia de nomes — estão em **`ARCHITECTURE.md`**, o documento normativo de referência.

Visão geral bem curta:

```text
src/omega_scan/
├── domain/          Lógica de negócio pura (alvos, perfis, escaneamentos, checks, relatórios, temas...)
├── application/     Casos de uso (commands/queries), pipeline de execução, controles
├── ports/           Contratos esperados pela aplicação (sondas, repositórios, exportadores...)
├── infrastructure/  Implementações concretas (httpx, SQLite; o Textual NÃO está aqui)
├── interfaces/      tui/ (Textual) e cli/ (scriptável), com paridade funcional estrita
├── app/             Montagem (DependencyContainer, bootstrap, ciclo de vida)
├── core/, shared/   Vocabulário transversal, utilitários fora do negócio
└── plugins/         Estrutura pronta, vazia (nenhum eixo de extensão confirmado)
```

Regras de design inalteradas desde a v1:
- `domain/checks/`: julga a partir das provas, nunca faz rede.
- `infrastructure/network/`: faz rede, nunca julga.
- `interfaces/`: exibe, não contém nenhuma lógica de negócio.
- `infrastructure/exporters/`: leem o resultado do escaneamento, não recalculam nada.

## 6. Taxonomia das regras

### Transporte, `TRN-*`

- `TRN-HTTP-001`: HTTP acessível sem redirecionamento para HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS não acessível, `FAIL`
- `TRN-HSTS-001`: cabeçalho HSTS ausente, `FAIL`
- `TRN-HSTS-002`: `max-age` de HSTS baixo, inferior a 1 ano, `WARN`

### Profundidade TLS, `TLS-*`

- `TLS-VERSION-001`: protocolo TLS obsoleto (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: suíte criptográfica claramente fraca (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Cabeçalhos, `HDR-*`

- `HDR-CSP-001`: CSP ausente em uma página HTML, `FAIL`
- `HDR-CSP-002`: CSP permissiva demais, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` ausente, `WARN`
- `HDR-SERVER-001`: banner `Server` exposto, `WARN`
- `HDR-CACHE-001`: `Cache-Control` ausente ou permissivo em uma página HTML, `WARN`

### Cookies, `COO-*`

- `COO-SECURE-001`: cookie em resposta HTTPS sem o atributo `Secure`, `WARN`
- `COO-HTTPONLY-001`: cookie sem o atributo `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: `SameSite` ausente, ou `None` sem `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` combinado com `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: origem arbitrária refletida tal qual em `Access-Control-Allow-Origin`, `WARN`

### Métodos HTTP, `MTH-*`

- `MTH-OPTIONS-001`: método OPTIONS ativado, `INFO`
- `MTH-TRACE-001`: método TRACE ativado, `WARN`
- `MTH-PUT-001`: método PUT ativado, `WARN`
- `MTH-DELETE-001`: método DELETE ativado, `WARN`
- `MTH-PATCH-001`: método PATCH ativado, `WARN`
- `MTH-CONNECT-001`: método CONNECT ativado, `WARN`

### Exposição, `EXR-*`

- `EXR-ADMIN-001`: caminho de administração acessível sem autenticação, `WARN`
- `EXR-SENSITIVE-001`: arquivo sensível acessível, `.env`, `.git`, `FAIL`

### Vazamentos de informação, `INF-*`

- `INF-BANNER-001`: banners do servidor expostos, `WARN`
- `INF-ERROR-001`: mensagens de erro detalhadas, `WARN`
- `INF-STACK-001`: stack trace exposto, `FAIL`
- `INF-ROBOTS-001`: arquivo `robots.txt` presente, `OK` informativo
- `INF-HEADER-001`: cabeçalhos técnicos reveladores demais, `WARN`
- `INF-SECURITYTXT-001`: arquivo `/.well-known/security.txt` presente, `OK` informativo

## 7. Política de confiança

| Nível | Definição |
|---|---|
| `certain` | Prova direta, sem ambiguidade, lida tal qual na resposta: cabeçalho presente ou ausente, código HTTP bruto. |
| `high` | Prova clara, mas com contexto indireto: métodos via OPTIONS, cookie observado. |
| `medium` | Constatação possivelmente influenciada por um intermediário: proxy, WAF, túnel. |
| `low` | Detecção indireta, conteúdo ambíguo ou situação `catch_all_suspected`. |

### Rebaixamentos automáticos

- `catch_all_suspected = true`: confiança limitada a `low`
- `proxy_suspected = true`: confiança limitada a `medium`
- `observed_access_state = ambiguous`: confiança limitada a `low`

## 8. Detecção de falsos positivos

### Comportamento catch-all

Antes de testar os caminhos sensíveis, o Omega-scan gera um caminho aleatório improvável. Se o servidor responder `200 OK` a ele, o alvo é marcado como `catch_all_suspected = true` e todos os achados de exposição são rebaixados para `confidence = low`.

### Autenticação versus ausência

Um caminho protegido — `401`, `403` ou redirecionamento para uma página de login — não é marcado nem como ausente nem como exposto. Ele é marcado `N/A` com a observação: «caminho protegido, presença não confirmável sem autenticação».

### Proxy / túnel

Se forem detectados cabeçalhos `X-Forwarded-*`, `Via` ou `Forwarded`, `proxy_suspected` passa a `true` e os achados afetados — banners, TLS — têm sua confiança limitada a `medium`.

## 9. Compatibilidade com terminais

A TUI (Textual) detecta automaticamente as capacidades do terminal (cor, tamanho) e adapta sua folha de estilo estrutural de acordo (`complete`/`standard`/`reduced`/`mono`) — acabaram-se as opções manuais (`--no-emoji`, `--no-color`, `--plain`) da v1. O modo CLI continua sempre em texto simples (ou `--json`), independente do terminal.

## 10. Exportações

Os relatórios de texto e HTML são escritos no idioma escolhido em Configurações («Idioma das exportações», por padrão o da interface); o JSON continua sendo um dado, não traduzido. Os relatórios são gerados em `var/exports/` por padrão (caminho de execução, veja `ARCHITECTURE.md`), ou no caminho indicado (`--output` na CLI, caixa de diálogo na TUI).

### JSON, fonte de verdade

Estrutura completa do escaneamento (`ScanRun`), estritamente serializável em JSON.

### Texto, relatório legível compacto

Legível fora do terminal, sem códigos ANSI, com estrutura hierarquizada.

### HTML, relatório web legível

Relatório autônomo com CSS embutido, consultável em qualquer navegador, compartilhável e arquivável.

## 11. Histórico e comparação

Cada escaneamento é salvo (SQLite, `var/db/app.db`): histórico consultável por alvo, detalhe de uma execução anterior, comparação entre dois escaneamentos (achados surgidos / resolvidos / inalterados / alterados) e repetição de um escaneamento no mesmo alvo sem redigitá-lo — ausentes na v1, acrescentados durante a migração para Clean Architecture.

## 12. Testes

```bash
source .venv/bin/activate
pytest tests/ -v
```

Estrutura: `tests/unit/` (domínio e aplicação, sem E/S real), `tests/integration/` (SQLite/arquivos reais, servidor HTTP falso `pytest-httpserver`), `tests/e2e/` (CLI e TUI de ponta a ponta, `Textual.testing`).

## 13. Fora do escopo

- Varredura de CVE
- Detecção ativa de SQLi, XSS, RCE
- Autenticação complexa do lado do scanner
- Rastreamento profundo
- Fuzzing
- Força bruta massiva de caminhos
- Escaneamento simultâneo de vários alvos
- Paralelismo agressivo
- Painel web

---

> Omega-scan — Observar, coletar, interpretar, relatar.  
> Um scanner de postura, não uma ferramenta de ataque.
