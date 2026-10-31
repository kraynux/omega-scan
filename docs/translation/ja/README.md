<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT ライセンス（LICENCE ファイルを参照） -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**Web セキュリティ態勢スキャナー**

> [Omega-Server](https://kraynux.snake-mackarel.ts.net) のために [kraynux](https://github.com/kraynux) が開発   

公式ページ：[OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; スクリーンショット：[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 インターフェースとエクスポートされるレポートは **17 言語** に対応 — [インターフェースの言語](#インターフェースの言語)を参照。  
**言語：**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** は、HTTP/HTTPS サービスの外から見える設定の健全性を解析する TUI + CLI ツールです。観察し、事実を集め、解釈ルールを適用し、対処につながるレポートを作成します。能動的な攻撃は一切行いません。`omega-` スイートのツールで、Clean Architecture で構成されています — 技術的な詳細はすべて `ARCHITECTURE.md` を参照してください。

## 1. ビジョンと範囲

Omega-scan はシステム管理向けの Web セキュリティ態勢スキャナーです：localhost、LAN、外部ターゲット上の HTTP/HTTPS サービスについて、Tailscale Funnel のようなトンネルの背後にある場合も含め、外から見える設定の健全性を素早く確認します。

### Omega-scan ができること

- 観測できる事実を収集します：ヘッダー、Cookie、HTTP メソッド、TLS、機密性の高いパス、CORS ヘッダー。
- それらの事実に、宣言的な解釈ルールを適用します。
- 一貫性があり、根拠を示した、対処につながる検出結果を作成します。
- 結果を TUI（Textual）またはスクリプト可能な CLI で表示し、3 種類のエクスポート（JSON、テキスト、HTML）を備えます。
- 誤検知を見抜きます。特に catch-all の挙動や、認証で保護されたパスです。
- 状況に適応します：プロキシ、トンネル、マルチ vhost、SNI。
- まだ許可済みとしてピン留めされていないターゲットは、スキャンの前に必ず明示的な許可の確認を求めます。
- ターゲットごとのスキャン履歴を永続的に保存し、再実行や経時的な比較ができます。

### Omega-scan がしないこと

- 能動的な脆弱性スキャン：SQLi、XSS、RCE は行いません。
- CVE スキャン。
- 総当たりや大規模なファジングのツール。
- 深いクローラー。
- 攻撃的な複数ターゲットの並列ツール。
- Web ダッシュボード。
- スキャナー側の認証。

## 2. インストール

### 前提条件

- Python 3.10+
- 依存関係と外部スキャンのためのインターネット接続

### インストール

公式アーカイブは `.tar.gz` 形式で提供されます。インストールの前に整合性を確認してください：

```bash
sha256sum omega-scan.tar.gz
```

### 方法 1 — インストールスクリプト

```bash
[ -d omega-scan ] && echo "ℹ️ ここに展開済みのため、この手順をスキップします。" || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan はすでに存在するため、移動をスキップします。" || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### 方法 2 — 堅牢なフルインストール



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`：

1. 仮想環境 `.venv` がまだなければ作成します。
2. 依存関係をインストールします（`pip install -e .`。`pyproject.toml` が唯一の正となる情報源です）。
3. `omega-scan.sh` と `install.sh` を実行可能にします。
4. エイリアス `scan` を `~/.bashrc` と `~/.zshrc` に追加します（既にあれば重複させません）。

### 依存関係

`pyproject.toml` で宣言（`requirements.txt` は廃止）：
- `textual`：TUI インターフェース、テーマ、端末への自動適応
- `httpx`：最新の HTTP/HTTPS クライアント
- `jinja2`：HTML エクスポートのテンプレート
- 開発用の依存関係（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-httpserver`、`trustme`、`ruff`、`mypy`、`import-linter`

## 3. 使い方

### 対話モード（TUI）

日常の利用におすすめ — 引数なしで起動します：

```bash
./omega-scan.sh
```

流れ：スプラッシュ画面（キーまたはクリックで閉じる）→ メインメニュー → ターゲットの入力とプロファイルの選択（ターゲットがまだピン留めされていなければ許可の確認あり）→ スキャン（進捗表示とネットワーク操作の詳細をリアルタイム表示）→ 結果（総合評価、カテゴリで絞り込める検出結果、行をクリックすると詳細）→ メインメニューからエクスポート／履歴／比較。端末への適応（色、サイズ、構造の簡略化）は自動で、手動の表示オプションはもう不要です。

#### キーボードショートカット

| キー | 操作 |
|---|---|
| `↑` / `↓` | 画面の項目間を移動 |
| `Tab` / `Shift+Tab` | フォームの入力欄間を移動 |
| `Esc` | 前の画面に戻る（ホーム画面では終了を確認） |
| `t` | 次のテーマ（確認なしですぐに適用） |
| `r` | 端末の検出を更新 |
| `a` | ヘルプを表示 |
| `q` | 終了（確認あり） |

### インターフェースの言語

インターフェースは 17 言語に対応しています：フランス語、英語、スペイン語、ポルトガル語（ブラジル）、イタリア語、ドイツ語、オランダ語、ポーランド語、ロシア語、簡体字中国語、ベトナム語、タイ語、インドネシア語、日本語、韓国語、ヒンディー語、アラビア語。設定（「Langue / Language」）で選択し、インターフェースの再起動後に反映されます。変数 `OMEGA_SCAN_LANG`（例：`OMEGA_SCAN_LANG=ja ./omega-scan.sh`）で、1 セッションの間だけ言語を固定できます。omega-suite から起動した場合、omega-scan はスイートの言語を使います。Linux のテキストコンソール（TTY）では、ラテン文字以外の言語はそのセッション中は英語で表示されます。コマンドラインはフランス語のままです。

### スクリプトモード（CLI）

サブコマンドを指定すると CLI モードになります（プレーンテキスト、または `--json` で JSON）：

```bash
# ターゲットをスキャン（ピン留めされていなければ --authorize が必須）
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# 履歴
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# エクスポート
./omega-scan.sh export scan-30577411758e --format html --output report.html

# 許可済みとしてピン留めしたターゲット（以降のスキャンでは --authorize 不要）
./omega-scan.sh targets pin example.org --note "顧客との合意 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### ターゲットの許可ガード

ターゲットがすでにピン留めされていない限り、そのターゲットに対する明示的な許可の確認（TUI ではチェックボックス、CLI では `--authorize`）なしにスキャンが始まることはありません。この確認はインターフェースだけでなく、アプリケーション側（`application/pipeline/guards/authorization_guard.py`）で行われます。

### 受け付けるターゲットの形式

```text
192.168.1.10                IPv4
192.168.1.10:8080           ポート付き IPv4
::1                         IPv6
[2001:db8::10]:8443         角かっことポート付き IPv6
example.org                 ホスト名
intranet.lan:8080/admin     ポートとパス付きホスト名
http://example.org          HTTP の URL
https://example.org/admin   HTTPS の URL
```

## 4. スキャンプロファイル

| パラメーター | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| 用途 | 簡易チェック | 完全（既定） | 詳細 | localhost / LAN |
| 接続／読み取りのタイムアウト | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| HTTP メソッド | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| パスの探査 | なし | あり（約 20） | あり（完全） | あり（約 20） |
| TLS | なし | あり | あり（詳細） | あり（寛容） |
| CORS プローブ | なし | あり | あり | あり |
| Catch-all | - | あり | あり | あり |
| HSTS ポリシー | 評価しない | 標準 | 厳格 | 寛容 |

### どのプロファイルをいつ使うか

- `quick`：本番投入前の瞬時チェック
- `standard`：本番サービスの完全な監査。推奨
- `extended`：危険な HTTP メソッドを含む詳細な監査
- `local-lab`：localhost や LAN のスキャン。公開サービス向けのルール（特に HSTS）で減点されません

## 5. アーキテクチャ

Omega-scan は **Clean Architecture**（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared）で構成され、`omega-` スイートのテンプレート（`omega-stress` を参照）に揃えてあります。完全な詳細 — ディレクトリ構成、依存関係のルール、機能の連鎖、例外の階層、命名体系 — は、規範的な参照文書である **`ARCHITECTURE.md`** にあります。

ごく短い概要：

```text
src/omega_scan/
├── domain/          純粋な業務ロジック（ターゲット、プロファイル、スキャン、チェック、レポート、テーマ...）
├── application/     ユースケース（commands/queries）、実行パイプライン、ガード
├── ports/           アプリケーションが期待する契約（プローブ、リポジトリ、エクスポーター...）
├── infrastructure/  具体的な実装（httpx、SQLite。Textual はここにはありません）
├── interfaces/      tui/（Textual）と cli/（スクリプト可能）、機能は厳密に同等
├── app/             組み立て（DependencyContainer、bootstrap、ライフサイクル）
├── core/, shared/   横断的な語彙、業務外のユーティリティ
└── plugins/         構造のみ用意、空（確定した拡張の方向性なし）
```

v1 から変わらない設計ルール：
- `domain/checks/`：証拠をもとに判定し、ネットワークには一切アクセスしません。
- `infrastructure/network/`：ネットワークにアクセスし、判定はしません。
- `interfaces/`：表示するだけで、業務ロジックは含みません。
- `infrastructure/exporters/`：スキャン結果を読むだけで、何も再計算しません。

## 6. ルールの体系

### トランスポート、`TRN-*`

- `TRN-HTTP-001`：HTTPS へのリダイレクトなしに HTTP に到達できる、`WARN`
- `TRN-HTTPS-001`：HTTPS に到達できない、`FAIL`
- `TRN-HSTS-001`：HSTS ヘッダーがない、`FAIL`
- `TRN-HSTS-002`：HSTS の `max-age` が短く 1 年未満、`WARN`

### TLS の深さ、`TLS-*`

- `TLS-VERSION-001`：古い TLS プロトコル（< TLSv1.2）、`FAIL`
- `TLS-CIPHER-001`：明らかに弱い暗号スイート（RC4、DES、NULL、EXPORT、MD5）、`WARN`

### ヘッダー、`HDR-*`

- `HDR-CSP-001`：HTML ページに CSP がない、`FAIL`
- `HDR-CSP-002`：CSP が緩すぎる、`WARN`
- `HDR-NOSNIFF-001`：`X-Content-Type-Options` がない、`WARN`
- `HDR-SERVER-001`：`Server` バナーが露出している、`WARN`
- `HDR-CACHE-001`：HTML ページに `Cache-Control` がない、または緩すぎる、`WARN`

### Cookie、`COO-*`

- `COO-SECURE-001`：HTTPS のレスポンスの Cookie に `Secure` 属性がない、`WARN`
- `COO-HTTPONLY-001`：Cookie に `HttpOnly` 属性がない、`WARN`
- `COO-SAMESITE-001`：`SameSite` がない、または `Secure` なしの `None`、`WARN`

### CORS、`COR-*`

- `COR-WILDCARD-CREDENTIALS-001`：`Access-Control-Allow-Origin: *` と `Access-Control-Allow-Credentials: true` の組み合わせ、`FAIL`
- `COR-REFLECTED-ORIGIN-001`：任意のオリジンが `Access-Control-Allow-Origin` にそのまま反映される、`WARN`

### HTTP メソッド、`MTH-*`

- `MTH-OPTIONS-001`：OPTIONS メソッドが有効、`INFO`
- `MTH-TRACE-001`：TRACE メソッドが有効、`WARN`
- `MTH-PUT-001`：PUT メソッドが有効、`WARN`
- `MTH-DELETE-001`：DELETE メソッドが有効、`WARN`
- `MTH-PATCH-001`：PATCH メソッドが有効、`WARN`
- `MTH-CONNECT-001`：CONNECT メソッドが有効、`WARN`

### 露出、`EXR-*`

- `EXR-ADMIN-001`：管理用パスに認証なしでアクセスできる、`WARN`
- `EXR-SENSITIVE-001`：機密ファイルにアクセスできる、`.env`、`.git`、`FAIL`

### 情報漏えい、`INF-*`

- `INF-BANNER-001`：サーバーのバナーが露出している、`WARN`
- `INF-ERROR-001`：詳細なエラーメッセージ、`WARN`
- `INF-STACK-001`：スタックトレースが露出している、`FAIL`
- `INF-ROBOTS-001`：`robots.txt` ファイルがある、`OK` 参考情報
- `INF-HEADER-001`：情報を出しすぎる技術的なヘッダー、`WARN`
- `INF-SECURITYTXT-001`：`/.well-known/security.txt` ファイルがある、`OK` 参考情報

## 7. 信頼度ポリシー

| レベル | 定義 |
|---|---|
| `certain` | レスポンスからそのまま読み取った、直接的で曖昧さのない証拠：ヘッダーの有無、生の HTTP コード。 |
| `high` | 証拠は明確だが文脈が間接的：OPTIONS で得たメソッド、観測した Cookie。 |
| `medium` | 中継機器の影響を受けている可能性がある所見：プロキシ、WAF、トンネル。 |
| `low` | 間接的な検出、曖昧な内容、または `catch_all_suspected` の状況。 |

### 自動的な格下げ

- `catch_all_suspected = true`：信頼度の上限は `low`
- `proxy_suspected = true`：信頼度の上限は `medium`
- `observed_access_state = ambiguous`：信頼度の上限は `low`

## 8. 誤検知の検出

### catch-all の挙動

機密性の高いパスを試す前に、Omega-scan はありえないランダムなパスを生成します。サーバーがそれに `200 OK` を返した場合、ターゲットは `catch_all_suspected = true` とされ、露出に関するすべての検出結果が `confidence = low` に格下げされます。

### 認証か、存在しないのか

保護されたパス — `401`、`403`、またはログインページへのリダイレクト — は、存在しないとも露出しているともされません。「保護されたパス。認証なしでは存在を確認できません」という注記付きで `N/A` とされます。

### プロキシ／トンネル

`X-Forwarded-*`、`Via`、`Forwarded` ヘッダーが検出されると、`proxy_suspected` が `true` になり、関係する検出結果（バナー、TLS）の信頼度の上限が `medium` になります。

## 9. 端末との互換性

TUI（Textual）は端末の能力（色、サイズ）を自動的に検出し、それに合わせて構造スタイルシート（`complete`/`standard`/`reduced`/`mono`）を調整します — v1 のような手動オプション（`--no-emoji`、`--no-color`、`--plain`）はもう不要です。CLI モードは常にプレーンテキスト（または `--json`）で、端末に依存しません。

## 10. エクスポート

テキストと HTML のレポートは、設定で選んだ言語で書かれます（「エクスポートの言語」、既定はインターフェースと同じ）。JSON はデータのままで翻訳されません。レポートは既定で `var/exports/` に生成されます（実行時のパス、`ARCHITECTURE.md` を参照）。または指定したパス（CLI では `--output`、TUI ではダイアログ）に生成されます。

### JSON、正となる情報源

スキャンの完全な構造（`ScanRun`）、厳密に JSON シリアライズ可能。

### テキスト、コンパクトで読みやすいレポート

端末の外でも読めて、ANSI コードを含まず、階層的に構成されています。

### HTML、読みやすい Web レポート

インライン CSS を含む単体で完結したレポートで、どのブラウザーでも閲覧でき、共有や保管が容易です。

## 11. 履歴と比較

各スキャンは保存されます（SQLite、`var/db/app.db`）：ターゲットごとの履歴の閲覧、過去の実行の詳細、2 つのスキャンの比較（出現／解消／変化なし／変化した検出結果）、同じターゲットに対する再入力なしの再実行ができます — v1 にはなく、Clean Architecture への移行時に追加されました。

## 12. テスト

```bash
source .venv/bin/activate
pytest tests/ -v
```

構成：`tests/unit/`（実際の I/O を伴わないドメインとアプリケーション）、`tests/integration/`（実際の SQLite／ファイル、模擬 HTTP サーバー `pytest-httpserver`）、`tests/e2e/`（エンドツーエンドの CLI と TUI、`Textual.testing`）。

## 13. 範囲外

- CVE スキャン
- SQLi、XSS、RCE の能動的な検出
- スキャナー側の複雑な認証
- 深いクロール
- ファジング
- パスの大規模な総当たり
- 複数ターゲットの同時スキャン
- 攻撃的な並列処理
- Web ダッシュボード

---

> Omega-scan — 観察し、集め、解釈し、報告する。  
> 態勢を確かめるスキャナーであって、攻撃ツールではありません。
