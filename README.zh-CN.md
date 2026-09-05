<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 许可证（见 LICENSE 文件） -->
<div align="center">
  <img src="docs/assets/omega-scan.png" alt="Omega-Scan" width="256">
</div>

# 🔍 OMEGA-SCAN

**Web 安全态势扫描器**

> 由 **kraynux** 为 **Omega-server** 开发  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

官方页面：[OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; 预览：[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

**语言：**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-scan** 是一个 TUI + CLI 工具，用于分析 HTTP/HTTPS 服务可见的配置安全性。它观察并收集事实，应用声明式解释规则，生成可执行的报告，但绝不执行主动攻击。它是 `omega-` 套件中的第三个工具（继 `omega-fire` 和 `omega-stress` 之后），采用 Clean Architecture 组织；完整技术说明请参阅 `ARCHITECTURE.md`。

## 1. 愿景与范围

Omega-scan 是面向系统管理的 Web 安全态势扫描器：用于快速检查 localhost、LAN 或外部目标上的 HTTP/HTTPS 服务的可见配置安全性，也支持位于 Tailscale Funnel 等隧道后的目标。

### Omega-scan 的功能

- 收集可观察事实：请求头、Cookie、HTTP 方法、TLS、敏感路径和 CORS 请求头。
- 对这些事实应用声明式解释规则。
- 生成统一、有依据且可执行的 findings。
- 通过 Textual TUI 或可脚本化 CLI 输出结果，并支持 JSON、文本和 HTML 三种导出格式。
- 检测误报，尤其是 catch-all 行为和受身份验证保护的路径。
- 适配不同上下文：代理、隧道、多虚拟主机和 SNI。
- 在扫描尚未固定并授权的目标前，要求明确的授权确认。
- 持久化保存每个目标的扫描历史，支持重放和随时间比较。

### Omega-scan 不做什么

- 不执行主动漏洞扫描，不检测 SQLi、XSS 或 RCE。
- 不扫描 CVE。
- 不是暴力破解或大规模模糊测试工具。
- 不进行深度爬取。
- 不进行激进的并行多目标扫描。
- 不提供 Web 控制面板。
- 不在扫描器端执行身份验证。

## 2. 安装

### 前置要求

- Python 3.10+
- 用于安装依赖和执行外部扫描的 Internet 连接

### 安装

官方归档以 `.tar.gz` 格式提供。安装前请验证完整性：

```bash
sha256sum omega-scan.tar.gz
```

### 方法 1 — 安装脚本

```bash
[ -d omega-scan ] && echo "ℹ️ 已在此处解压，跳过该步骤。" || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan 已存在，跳过移动。" || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### 方法 2 — 可重复执行的完整安装

```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh` 会：

1. 在不存在时创建 `.venv` 虚拟环境。
2. 安装依赖（`pip install -e .`；`pyproject.toml` 仍是唯一可信来源）。
3. 为 `omega-scan.sh` 和 `install.sh` 添加执行权限。
4. 将 `scan` 别名添加到 `~/.bashrc` 和 `~/.zshrc`，如果已存在则不会重复添加。

### 依赖

依赖声明位于 `pyproject.toml` 中（不再使用 `requirements.txt`）：
- `textual`：TUI、主题和终端自动适配。
- `httpx`：现代 HTTP/HTTPS 客户端。
- `jinja2`：HTML 导出模板。
- 开发依赖（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-httpserver`、`trustme`、`ruff`、`mypy`、`import-linter`。

## 3. 使用方法

### 交互模式（TUI）

推荐日常使用，直接无参数启动：

```bash
./omega-scan.sh
```

操作流程：启动画面（按键或单击关闭）→ 主菜单 → 输入目标并选择配置文件（如果目标尚未固定，则确认授权）→ 扫描（实时显示进度和网络操作）→ 结果（总评分、可按类别筛选的 findings，单击行查看详情）→ 从主菜单进行导出、查看历史和比较。终端适配（颜色、尺寸和结构降级）会自动完成，不再需要手动显示参数。

#### 键盘快捷键

| 按键 | 操作 |
|---|---|
| `↑` / `↓` | 在屏幕元素之间移动 |
| `Tab` / `Shift+Tab` | 在表单字段之间移动 |
| `Esc` | 返回上一屏幕（在首页确认退出） |
| `t` | 切换到下一个主题（立即应用，无需确认） |
| `r` | 刷新终端检测 |
| `a` | 显示帮助 |
| `q` | 退出（需要确认） |

### 可脚本化模式（CLI）

任何子命令都会启动 CLI（纯文本，或通过 `--json` 输出 JSON）：

```bash
# 扫描目标（如果目标尚未固定，则必须使用 --authorize）
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# 历史
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# 导出
./omega-scan.sh export scan-30577411758e --format html --output report.html

# 固定并授权的目标（后续扫描无需 --authorize）
./omega-scan.sh targets pin example.org --note "客户批准 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### 目标授权护栏

除非目标已经固定，否则没有明确的目标授权确认，扫描不会开始（TUI 复选框，CLI 使用 `--authorize`）。该检查在应用层执行（`application/pipeline/guards/authorization_guard.py`），而不是只在界面层执行。

### 支持的目标格式

```text
192.168.1.10                IPv4
192.168.1.10:8080           带端口的 IPv4
::1                         IPv6
[2001:db8::10]:8443         带方括号和端口的 IPv6
example.org                 主机名
intranet.lan:8080/admin     带端口和路径的主机名
http://example.org          HTTP URL
https://example.org/admin   HTTPS URL
```

## 4. 扫描配置文件

| 参数 | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| 用途 | 快速检查 | 完整（默认） | 深入检查 | localhost / LAN |
| 连接/读取超时 | 3 秒 / 6 秒 | 3 秒 / 6 秒 | 5 秒 / 10 秒 | 3 秒 / 6 秒 |
| HTTP 方法 | OPTIONS | OPTIONS、TRACE | OPTIONS、TRACE、PUT、DELETE、PATCH | OPTIONS、TRACE |
| 路径探测 | 否 | 是（约 20 个） | 是（完整） | 是（约 20 个） |
| TLS | 否 | 是 | 是（详细） | 是（宽容） |
| CORS 探测 | 否 | 是 | 是 | 是 |
| Catch-all | — | 是 | 是 | 是 |
| HSTS 策略 | 不评估 | 标准 | 严格 | 宽容 |

### 如何选择配置文件

- `quick`：上线前的快速检查。
- `standard`：生产服务的完整审计，推荐使用。
- `extended`：包含高风险 HTTP 方法的深入审计。
- `local-lab`：扫描 localhost 或 LAN，不严格套用面向公网服务的规则，尤其是 HSTS 规则。

## 5. 架构

Omega-scan 遵循 **Clean Architecture**（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared），并与 `omega-` 套件模板保持一致（参阅 `omega-stress`）。完整说明——目录树、依赖规则、功能链、异常层级和命名分类——位于规范参考文档 **`ARCHITECTURE.md`**。

```text
src/omega_scan/
├── domain/          纯业务逻辑（目标、配置文件、扫描、检查、报告、主题……）
├── application/     用例（commands/queries）、执行管线和护栏
├── ports/           应用所需契约（probers、repositories、exporters……）
├── infrastructure/  具体实现（httpx、SQLite；Textual 不在此处）
├── interfaces/      tui/（Textual）和 cli/（可脚本化），功能严格对等
├── app/             组装（DependencyContainer、bootstrap、生命周期）
├── core/, shared/   跨领域词汇和非业务工具
└── plugins/         已建立但为空的结构（尚无确认的扩展方向）
```

自 v1 起保持不变的设计规则：
- `domain/checks/`：根据证据做判断，从不执行网络操作。
- `infrastructure/network/`：执行网络操作，从不做判断。
- `interfaces/`：显示数据，不包含业务逻辑。
- `infrastructure/exporters/`：读取扫描结果，不重新计算结果。

## 6. 规则分类

### 传输层，`TRN-*`

- `TRN-HTTP-001`：HTTP 可访问且未重定向到 HTTPS，`WARN`。
- `TRN-HTTPS-001`：HTTPS 不可访问，`FAIL`。
- `TRN-HSTS-001`：缺少 HSTS 请求头，`FAIL`。
- `TRN-HSTS-002`：HSTS 的 `max-age` 较低，少于一年，`WARN`。

### TLS 深度，`TLS-*`

- `TLS-VERSION-001`：TLS 协议过时（< TLSv1.2），`FAIL`。
- `TLS-CIPHER-001`：明显较弱的密码套件（RC4、DES、NULL、EXPORT、MD5），`WARN`。

### 请求头，`HDR-*`

- `HDR-CSP-001`：HTML 页面缺少 CSP，`FAIL`。
- `HDR-CSP-002`：CSP 过于宽松，`WARN`。
- `HDR-NOSNIFF-001`：缺少 `X-Content-Type-Options`，`WARN`。
- `HDR-SERVER-001`：暴露 `Server` 横幅，`WARN`。
- `HDR-CACHE-001`：HTML 页面缺少 `Cache-Control` 或配置过于宽松，`WARN`。

### Cookie，`COO-*`

- `COO-SECURE-001`：HTTPS 响应中的 Cookie 缺少 `Secure` 属性，`WARN`。
- `COO-HTTPONLY-001`：Cookie 缺少 `HttpOnly` 属性，`WARN`。
- `COO-SAMESITE-001`：缺少 `SameSite`，或设置为 `None` 但没有 `Secure`，`WARN`。

### CORS，`COR-*`

- `COR-WILDCARD-CREDENTIALS-001`：`Access-Control-Allow-Origin: *` 与 `Access-Control-Allow-Credentials: true` 同时出现，`FAIL`。
- `COR-REFLECTED-ORIGIN-001`：任意 origin 原样反射到 `Access-Control-Allow-Origin`，`WARN`。

### HTTP 方法，`MTH-*`

- `MTH-OPTIONS-001`：OPTIONS 方法已启用，`INFO`。
- `MTH-TRACE-001`：TRACE 方法已启用，`WARN`。
- `MTH-PUT-001`：PUT 方法已启用，`WARN`。
- `MTH-DELETE-001`：DELETE 方法已启用，`WARN`。
- `MTH-PATCH-001`：PATCH 方法已启用，`WARN`。
- `MTH-CONNECT-001`：CONNECT 方法已启用，`WARN`。

### 暴露，`EXR-*`

- `EXR-ADMIN-001`：管理路径无需身份验证即可访问，`WARN`。
- `EXR-SENSITIVE-001`：敏感文件可访问（`.env`、`.git`），`FAIL`。

### 信息泄露，`INF-*`

- `INF-BANNER-001`：暴露服务器横幅，`WARN`。
- `INF-ERROR-001`：错误消息过于详细，`WARN`。
- `INF-STACK-001`：暴露堆栈跟踪，`FAIL`。
- `INF-ROBOTS-001`：存在 `robots.txt`，信息提示 `OK`。
- `INF-HEADER-001`：技术请求头过于详细，`WARN`。
- `INF-SECURITYTXT-001`：存在 `/.well-known/security.txt`，信息提示 `OK`。

## 7. 可信度策略

| 等级 | 定义 |
|---|---|
| `certain` | 直接且无歧义的证据，原样读取自响应：请求头存在或缺失，原始 HTTP 状态码。 |
| `high` | 证据清晰但上下文间接：通过 OPTIONS 发现的方法、观察到的 Cookie。 |
| `medium` | 结果可能受到中间设备、代理、WAF 或隧道影响。 |
| `low` | 间接检测、内容含糊或处于 `catch_all_suspected` 状态。 |

### 自动降级

- `catch_all_suspected = true`：可信度最高为 `low`。
- `proxy_suspected = true`：可信度最高为 `medium`。
- `observed_access_state = ambiguous`：可信度最高为 `low`。

## 8. 误报检测

### Catch-all 行为

在测试敏感路径之前，Omega-scan 会生成一个不太可能存在的随机路径。如果服务器对其返回 `200 OK`，则将目标标记为 `catch_all_suspected = true`，所有暴露类 findings 的可信度都会降级为 `confidence = low`。

### 身份验证与缺失的区别

受保护路径、`401`、`403` 或重定向到登录页面的情况，既不会标记为不存在，也不会标记为暴露，而是标记为 `N/A`，并附注：“路径受到保护；没有身份验证时无法确认其存在”。

### 代理 / 隧道

如果检测到 `X-Forwarded-*`、`Via` 或 `Forwarded` 请求头，则将 `proxy_suspected` 设置为 `true`，相关 findings（横幅、TLS）的可信度最高为 `medium`。

## 9. 终端兼容性

Textual TUI 会自动检测终端能力（颜色和尺寸），并相应调整结构化样式（`complete`/`standard`/`reduced`/`mono`）；不再需要 v1 中的手动参数（`--no-emoji`、`--no-color`、`--plain`）。CLI 模式始终使用纯文本（或 `--json`），与终端无关。

## 10. 导出

报告默认生成在 `var/exports/`（运行时路径，参阅 `ARCHITECTURE.md`），也可以写入指定路径（CLI 使用 `--output`，TUI 使用对话框）。

### JSON，事实来源

完整扫描结构（`ScanRun`），严格可序列化为 JSON。

### 文本，紧凑的人类可读报告

无需 ANSI 控制码，在终端之外也能阅读，并保持层级结构。

### HTML，可读的 Web 报告

带内嵌 CSS 的独立报告，可在任何浏览器中查看，便于分享和归档。

## 11. 历史与比较

每次扫描都会持久化保存到 SQLite（`var/db/app.db`）：可以按目标查询历史、查看过去运行的详情、比较两次扫描（新出现、已解决、未变化或已变化的 findings），并在无需重新输入目标的情况下重放同一目标的扫描。这些功能在 v1 中尚不存在，是迁移到 Clean Architecture 时新增的。

## 12. 测试

```bash
source .venv/bin/activate
pytest tests/ -v
```

目录结构：`tests/unit/`（领域和应用，无真实 I/O）、`tests/integration/`（SQLite/真实文件、`pytest-httpserver` 虚拟 HTTP 服务器）、`tests/e2e/`（CLI 和 TUI 端到端测试，`Textual.testing`）。

## 13. 不在范围内

- CVE 扫描。
- 主动检测 SQLi、XSS 和 RCE。
- 扫描器端的复杂身份验证。
- 深度爬取。
- 模糊测试。
- 大规模路径暴力破解。
- 同时扫描多个目标。
- 激进的并行处理。
- Web 控制面板。

---

> Omega-scan —— 观察、收集、解释、报告。  
> 它是态势扫描器，不是攻击工具。
