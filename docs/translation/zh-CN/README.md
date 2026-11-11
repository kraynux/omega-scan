<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 许可证（见 LICENCE 文件） -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan.png" alt="Omega-Scan" width="512">
</div>

# 🔍 OMEGA-SCAN

**Web 安全态势扫描器**

> 由 [kraynux](https://github.com/kraynux) 为 [Omega-Server](https://kraynux.snake-mackarel.ts.net) 打造   

官方页面：[OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; 截图：[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 界面和导出的报告提供 **17 种语言** — 见[界面语言](#界面语言)。  
**语言：**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** 是一个 TUI + CLI 工具，用于分析你的 HTTP/HTTPS 服务在外部可见的配置规范程度。它观察、收集事实、应用解释性规则，并生成可据以行动的报告，绝不进行任何主动攻击。它是 `omega-` 套件中的一个工具，采用 Clean Architecture 构建 — 完整技术细节见 `ARCHITECTURE.md`。

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-scan/D.png" width="24%" />
</p>

## 1. 愿景与范围

Omega-scan 是面向系统管理的 Web 安全态势扫描器：快速检查 localhost、局域网或外部目标上 HTTP/HTTPS 服务的可见配置规范程度，包括位于 Tailscale Funnel 之类隧道之后的服务。

### Omega-scan 能做什么

- 收集可观察的事实：响应头、Cookie、HTTP 方法、TLS、敏感路径、CORS 响应头。
- 对这些事实应用声明式的解释性规则。
- 生成统一、有依据且可据以行动的发现项。
- 在 TUI（Textual）或可脚本化的 CLI 中呈现结果，并提供三种导出：JSON、文本、HTML。
- 识别误报，尤其是 catch-all 行为以及受认证保护的路径。
- 适应不同环境：代理、隧道、多虚拟主机、SNI。
- 对任何尚未固定为已授权的目标，扫描前都要求明确确认授权。
- 按目标保留持久的扫描历史，可重放，并可随时间对比。

### Omega-scan 不做什么

- 主动漏洞扫描：不做 SQLi、XSS 或 RCE。
- CVE 扫描。
- 暴力破解或大规模模糊测试工具。
- 深度爬虫。
- 激进的多目标并行工具。
- Web 仪表盘。
- 扫描器端认证。

## 2. 安装

### 前提条件

- Python 3.10+
- 互联网连接，用于安装依赖和扫描外部目标

### 安装

官方归档以 `.tar.gz` 格式提供。安装前请校验其完整性：

```bash
sha256sum omega-scan.tar.gz
```

### 方法 1 — 安装脚本

```bash
[ -d omega-scan ] && echo "ℹ️ 此处已解压，跳过此步骤。" || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan 已存在，跳过移动。" || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### 方法 2 — 稳健的完整安装



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`：

1. 如果虚拟环境 `.venv` 尚不存在，则创建它。
2. 安装依赖（`pip install -e .`；`pyproject.toml` 仍是唯一的权威来源）。
3. 使 `omega-scan.sh` 和 `install.sh` 可执行。
4. 将别名 `scan` 添加到 `~/.bashrc` 和 `~/.zshrc`（已存在时不会重复添加）。

### 依赖

在 `pyproject.toml` 中声明（不再有 `requirements.txt`）：
- `textual`：TUI 界面、主题、自动适配终端
- `httpx`：现代 HTTP/HTTPS 客户端
- `jinja2`：HTML 导出的模板
- 开发依赖（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-httpserver`、`trustme`、`ruff`、`mypy`、`import-linter`

## 3. 使用

### 交互模式（TUI）

推荐日常使用 — 不带参数启动：

```bash
./omega-scan.sh
```

流程：启动画面（按任意键或点击关闭）→ 主菜单 → 输入目标并选择配置（若目标尚未固定，需确认授权）→ 扫描（实时显示进度条和网络操作详情）→ 结果（总体评分、可按类别筛选的发现项、点击某行查看详情）→ 从主菜单进行导出/历史/对比。对终端的适配（颜色、尺寸、结构降级）是自动的，不再需要手动设置显示选项。

#### 键盘快捷键

| 按键 | 操作 |
|---|---|
| `↑` / `↓` | 在屏幕元素之间移动 |
| `Tab` / `Shift+Tab` | 在表单字段之间移动 |
| `Esc` | 返回上一屏（在主屏上会确认是否退出） |
| `t` | 下一个主题（立即应用，无需确认） |
| `r` | 刷新终端检测 |
| `a` | 显示帮助 |
| `q` | 退出（需确认） |

### 界面语言

界面提供 17 种语言：法语、英语、西班牙语、葡萄牙语（巴西）、意大利语、德语、荷兰语、波兰语、俄语、简体中文、越南语、泰语、印尼语、日语、韩语、印地语和阿拉伯语。在设置中选择（“Langue / Language”），重启界面后生效；变量 `OMEGA_SCAN_LANG`（例如 `OMEGA_SCAN_LANG=zh-CN ./omega-scan.sh`）可在一次会话中强制使用某种语言。从 omega-suite 启动时，omega-scan 使用套件的语言。在 Linux 文本控制台（TTY）上，非拉丁文字的语言在本次会话中以英语显示。命令行保持法语。

### 联系与支持

帮助（`a` 键）提供 **联系与支持** 界面：*请我喝杯咖啡*（开发者的 PayPal 页面）、*联系支持*（明文显示的电子邮件地址和网站联系表单）、*登记为用户（匿名）* 和 *检查更新*。 登记是自愿的，默认关闭，且只发送一次：仅用于统计用户数量，以及（如您愿意）其所在的大洲或国家（封闭列表，绝无自由文本）。它发送一个随机生成的密钥、软件名称（`omega-scan`）及其版本；绝不发送姓名、机器名称、设置、目标或结果。IP 地址不会记录在登记中，但与任何访问一样，会经过接收服务器的安全检查和日志。 可随时在同一界面撤回（*不再登记我*）。 检查更新仅读取网站上已发布版本的列表，且从不在未点击的情况下进行。

### 脚本模式（CLI）

任何子命令都会进入 CLI 模式（纯文本，或使用 `--json` 输出 JSON）：

```bash
# 扫描目标（若目标尚未固定，必须加 --authorize）
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# 历史
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# 导出
./omega-scan.sh export scan-30577411758e --format html --output report.html

# 固定为已授权的目标（之后的扫描无需 --authorize）
./omega-scan.sh targets pin example.org --note "客户协议 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### 目标授权保护

除非目标已固定，否则未经对该目标的明确授权确认（TUI 中的复选框，CLI 中的 `--authorize`），任何扫描都不会开始。该检查在应用层完成（`application/pipeline/guards/authorization_guard.py`），而不仅仅在界面层。

### 可接受的目标格式

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

## 4. 扫描配置

| 参数 | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| 用途 | 快速检查 | 完整（默认） | 深入 | localhost / 局域网 |
| 连接/读取超时 | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| HTTP 方法 | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| 路径探测 | 否 | 是（约 20 个） | 是（完整） | 是（约 20 个） |
| TLS | 否 | 是 | 是（详细） | 是（宽松） |
| CORS 探测 | 否 | 是 | 是 | 是 |
| Catch-all | - | 是 | 是 | 是 |
| HSTS 策略 | 不评估 | 标准 | 严格 | 宽松 |

### 何时使用哪种配置

- `quick`：上线前的闪电检查
- `standard`：对生产服务的完整审计，推荐
- `extended`：包含高风险 HTTP 方法的深入审计
- `local-lab`：扫描 localhost 或局域网，不会因面向公网服务的规则（尤其是 HSTS）而扣分

## 5. 架构

Omega-scan 采用 **Clean Architecture** 构建（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared），与 `omega-` 套件的模板保持一致（见 `omega-stress`）。完整细节——目录树、依赖规则、功能链、异常层级、命名体系——见 **`ARCHITECTURE.md`**，即规范性参考文档。

非常简短的概览：

```text
src/omega_scan/
├── domain/          纯业务逻辑（目标、配置、扫描、检查、报告、主题……）
├── application/     用例（commands/queries）、执行流水线、保护检查
├── ports/           应用所需的契约（探测器、仓储、导出器……）
├── infrastructure/  具体实现（httpx、SQLite；Textual 不在这里）
├── interfaces/      tui/（Textual）和 cli/（可脚本化），功能严格对等
├── app/             装配（DependencyContainer、bootstrap、生命周期）
├── core/, shared/   通用词汇、非业务工具
└── plugins/         结构已就位，为空（尚无确定的扩展方向）
```

自 v1 以来未变的设计规则：
- `domain/checks/`：根据证据进行判断，从不访问网络。
- `infrastructure/network/`：负责网络访问，从不做判断。
- `interfaces/`：只负责显示，不包含任何业务逻辑。
- `infrastructure/exporters/`：读取扫描结果，不重新计算任何东西。

## 6. 规则分类

### 传输，`TRN-*`

- `TRN-HTTP-001`：HTTP 可访问且未重定向到 HTTPS，`WARN`
- `TRN-HTTPS-001`：HTTPS 不可访问，`FAIL`
- `TRN-HSTS-001`：缺少 HSTS 响应头，`FAIL`
- `TRN-HSTS-002`：HSTS 的 `max-age` 过低，不足 1 年，`WARN`

### TLS 深度，`TLS-*`

- `TLS-VERSION-001`：过时的 TLS 协议（< TLSv1.2），`FAIL`
- `TLS-CIPHER-001`：明显较弱的加密套件（RC4、DES、NULL、EXPORT、MD5），`WARN`

### 响应头，`HDR-*`

- `HDR-CSP-001`：HTML 页面缺少 CSP，`FAIL`
- `HDR-CSP-002`：CSP 过于宽松，`WARN`
- `HDR-NOSNIFF-001`：缺少 `X-Content-Type-Options`，`WARN`
- `HDR-SERVER-001`：暴露了 `Server` 横幅，`WARN`
- `HDR-CACHE-001`：HTML 页面缺少 `Cache-Control` 或设置过于宽松，`WARN`

### Cookie，`COO-*`

- `COO-SECURE-001`：HTTPS 响应中的 Cookie 没有 `Secure` 属性，`WARN`
- `COO-HTTPONLY-001`：Cookie 没有 `HttpOnly` 属性，`WARN`
- `COO-SAMESITE-001`：缺少 `SameSite`，或为 `None` 但没有 `Secure`，`WARN`

### CORS，`COR-*`

- `COR-WILDCARD-CREDENTIALS-001`：`Access-Control-Allow-Origin: *` 与 `Access-Control-Allow-Credentials: true` 同时出现，`FAIL`
- `COR-REFLECTED-ORIGIN-001`：任意来源被原样回显到 `Access-Control-Allow-Origin` 中，`WARN`

### HTTP 方法，`MTH-*`

- `MTH-OPTIONS-001`：启用了 OPTIONS 方法，`INFO`
- `MTH-TRACE-001`：启用了 TRACE 方法，`WARN`
- `MTH-PUT-001`：启用了 PUT 方法，`WARN`
- `MTH-DELETE-001`：启用了 DELETE 方法，`WARN`
- `MTH-PATCH-001`：启用了 PATCH 方法，`WARN`
- `MTH-CONNECT-001`：启用了 CONNECT 方法，`WARN`

### 暴露，`EXR-*`

- `EXR-ADMIN-001`：管理路径无需认证即可访问，`WARN`
- `EXR-SENSITIVE-001`：敏感文件可被访问，`.env`、`.git`，`FAIL`

### 信息泄露，`INF-*`

- `INF-BANNER-001`：暴露了服务器横幅，`WARN`
- `INF-ERROR-001`：详细的错误信息，`WARN`
- `INF-STACK-001`：暴露了堆栈跟踪，`FAIL`
- `INF-ROBOTS-001`：存在 `robots.txt` 文件，`OK` 仅供参考
- `INF-HEADER-001`：技术性响应头泄露过多信息，`WARN`
- `INF-SECURITYTXT-001`：存在 `/.well-known/security.txt` 文件，`OK` 仅供参考

## 7. 可信度策略

| 级别 | 定义 |
|---|---|
| `certain` | 直接、无歧义的证据，从响应中原样读取：响应头存在或不存在、原始 HTTP 状态码。 |
| `high` | 证据清晰但上下文间接：通过 OPTIONS 得到的方法、观察到的 Cookie。 |
| `medium` | 结论可能受中间环节影响：代理、WAF、隧道。 |
| `low` | 间接检测、内容有歧义，或处于 `catch_all_suspected` 状态。 |

### 自动降级

- `catch_all_suspected = true`：可信度上限为 `low`
- `proxy_suspected = true`：可信度上限为 `medium`
- `observed_access_state = ambiguous`：可信度上限为 `low`

## 8. 误报检测

### Catch-all 行为

在测试敏感路径之前，Omega-scan 会生成一个几乎不可能存在的随机路径。如果服务器对它返回 `200 OK`，目标就会被标记为 `catch_all_suspected = true`，所有暴露类发现项都会降级为 `confidence = low`。

### 认证与不存在

受保护的路径——`401`、`403` 或重定向到登录页——既不会被标记为不存在，也不会被标记为已暴露。它会被标记为 `N/A`，并附注：“受保护路径，未经认证无法确认是否存在”。

### 代理 / 隧道

如果检测到 `X-Forwarded-*`、`Via` 或 `Forwarded` 响应头，`proxy_suspected` 就会变为 `true`，相关发现项（横幅、TLS）的可信度上限为 `medium`。

## 9. 终端兼容性

TUI（Textual）会自动检测终端的能力（颜色、尺寸），并据此调整其结构样式表（`complete`/`standard`/`reduced`/`mono`）——不再像 v1 那样需要手动选项（`--no-emoji`、`--no-color`、`--plain`）。CLI 模式始终是纯文本（或 `--json`），与终端无关。

## 10. 导出

文本和 HTML 报告使用设置中选择的语言编写（“导出语言”，默认与界面相同）；JSON 作为数据保持不翻译。报告默认生成在 `var/exports/`（运行时路径，见 `ARCHITECTURE.md`），或生成在指定路径（CLI 中用 `--output`，TUI 中用对话框）。

### JSON，权威来源

扫描的完整结构（`ScanRun`），严格可序列化为 JSON。

### 文本，紧凑的可读报告

在终端之外也可阅读，不含 ANSI 代码，结构分层清晰。

### HTML，易读的网页报告

内嵌 CSS 的独立报告，可在任何浏览器中查看，便于分享和归档。

## 11. 历史与对比

每次扫描都会保存（SQLite，`var/db/app.db`）：可按目标查看历史、查看过往运行的详情、对比两次扫描（新出现 / 已解决 / 未变化 / 已变化的发现项），以及对同一目标重放扫描而无需重新输入——这些在 v1 中没有，是迁移到 Clean Architecture 时加入的。

## 12. 测试

```bash
source .venv/bin/activate
pytest tests/ -v
```

结构：`tests/unit/`（领域和应用层，无真实 I/O），`tests/integration/`（真实 SQLite/文件、模拟 HTTP 服务器 `pytest-httpserver`），`tests/e2e/`（端到端 CLI 和 TUI，`Textual.testing`）。

## 13. 范围之外

- CVE 扫描
- 主动检测 SQLi、XSS、RCE
- 扫描器端的复杂认证
- 深度爬取
- 模糊测试
- 大规模路径暴力破解
- 多目标同时扫描
- 激进的并行处理
- Web 仪表盘

---

> Omega-scan — 观察、收集、解读、报告。  
> 一个态势扫描器，而不是攻击工具。
