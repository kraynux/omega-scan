<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - رخصة MIT (انظر ملف LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**ماسح الوضع الأمني لخدمات الويب**

> طوّره **kraynux** من أجل **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

الصفحة الرسمية: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; معاينة: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 الواجهة والتقارير المُصدَّرة متاحة بـ **17 لغة** — انظر [لغات الواجهة](#لغات-الواجهة).  
**اللغات:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](README.md)

---

**Omega-scan** أداة TUI + CLI تحلّل سلامة الإعدادات الظاهرة من الخارج لخدمات HTTP/HTTPS لديك. فهي تراقب، وتجمع الحقائق، وتطبّق قواعد تفسيرية، وتنتج تقارير قابلة للتنفيذ، دون أن تنفّذ أي هجوم نشط أبدًا. هي إحدى أدوات مجموعة `omega-`، مبنية وفق Clean Architecture — انظر `ARCHITECTURE.md` لكل التفاصيل التقنية.

## 1. الرؤية والنطاق

Omega-scan ماسح للوضع الأمني لخدمات الويب موجّه لإدارة الأنظمة: التحقق بسرعة من سلامة الإعدادات الظاهرة لخدمة HTTP/HTTPS على localhost أو الشبكة المحلية أو هدف خارجي، بما في ذلك ما يقع خلف نفق مثل Tailscale Funnel.

### ما يفعله Omega-scan

- يجمع حقائق يمكن ملاحظتها: الترويسات، وملفات تعريف الارتباط، وطرق HTTP، وTLS، والمسارات الحساسة، وترويسات CORS.
- يطبّق على هذه الحقائق قواعد تفسيرية تصريحية.
- ينتج نتائج موحّدة ومبرّرة وقابلة للتنفيذ.
- يعرض النتيجة في TUI (Textual) أو في CLI قابل للبرمجة النصية، ومن خلال ثلاثة أنواع من التصدير: JSON، ونص، وHTML.
- يكشف الإنذارات الكاذبة، ولا سيما سلوك catch-all والمسارات المحمية بالمصادقة.
- يتكيّف مع السياق: الوكيل، والنفق، والمضيفون الافتراضيون المتعددون، وSNI.
- يشترط تأكيدًا صريحًا للإذن قبل فحص أي هدف غير مثبّت مسبقًا بوصفه مأذونًا به.
- يحتفظ بسجل دائم للفحوص لكل هدف، قابل لإعادة التشغيل والمقارنة عبر الزمن.

### ما لا يفعله Omega-scan

- فحص الثغرات النشط: لا SQLi ولا XSS ولا RCE.
- فحص CVE.
- أداة للتخمين بالقوة الغاشمة أو للتشويش (fuzzing) على نطاق واسع.
- زاحف عميق.
- أداة عدوانية لفحص عدة أهداف بالتوازي.
- لوحة تحكم ويب.
- المصادقة من جهة الماسح.

## 2. التثبيت

### المتطلبات

- Python 3.10+
- اتصال بالإنترنت، من أجل الاعتماديات والفحوص الخارجية

### التثبيت

يُوزَّع الأرشيف الرسمي بصيغة `.tar.gz`. تحقّق من سلامته قبل التثبيت:

```bash
sha256sum omega-scan.tar.gz
```

### الطريقة 1 — نص التثبيت

```bash
[ -d omega-scan ] && echo "ℹ️ مُستخرَج هنا مسبقًا، تم تخطي الخطوة." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ‏~/omega-scan موجود مسبقًا، تم تخطي النقل." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### الطريقة 2 — تثبيت كامل متين



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. ينشئ البيئة الافتراضية `.venv` إن لم تكن موجودة.
2. يثبّت الاعتماديات (`pip install -e .`؛ ويبقى `pyproject.toml` المرجع الوحيد).
3. يجعل `omega-scan.sh` و`install.sh` قابلين للتنفيذ.
4. يضيف الاسم المستعار `scan` إلى `~/.bashrc` و`~/.zshrc` (من دون تكرار إن كان موجودًا).

### الاعتماديات

مُعرَّفة في `pyproject.toml` (لم يعد هناك `requirements.txt`):
- `textual`: واجهة TUI، والسمات، والتكيّف التلقائي مع الطرفية
- `httpx`: عميل HTTP/HTTPS حديث
- `jinja2`: قوالب تصدير HTML
- اعتماديات التطوير (`pip install -e ".[dev]"`): `pytest` و`pytest-asyncio` و`pytest-httpserver` و`trustme` و`ruff` و`mypy` و`import-linter`

## 3. الاستخدام

### الوضع التفاعلي (TUI)

يُنصح به للاستخدام اليومي — يُشغَّل من دون وسائط:

```bash
./omega-scan.sh
```

المسار: شاشة البداية (تُغلق بضغطة مفتاح أو نقرة) ← القائمة الرئيسية ← إدخال الهدف واختيار ملف التعريف (مع تأكيد الإذن إن لم يكن الهدف مثبّتًا مسبقًا) ← الفحص (مؤشر التقدّم وتفاصيل عمليات الشبكة معروضة مباشرة) ← النتائج (التقييم العام، والنتائج القابلة للتصفية حسب الفئة، والتفاصيل عند النقر على سطر) ← التصدير/السجل/المقارنة من القائمة الرئيسية. التكيّف مع الطرفية (الألوان، والحجم، وتبسيط البنية) تلقائي، ولم تعد هناك حاجة إلى خيارات عرض يدوية.

#### اختصارات لوحة المفاتيح

| المفتاح | الإجراء |
|---|---|
| `↑` / `↓` | التنقل بين عناصر الشاشة |
| `Tab` / `Shift+Tab` | التنقل بين حقول النموذج |
| `Esc` | العودة إلى الشاشة السابقة (تأكيد الخروج في الشاشة الرئيسية) |
| `t` | السمة التالية (تُطبَّق فورًا دون تأكيد) |
| `r` | تحديث اكتشاف الطرفية |
| `a` | عرض المساعدة |
| `q` | الخروج (مع تأكيد) |

### لغات الواجهة

الواجهة متاحة بـ 17 لغة: الفرنسية، والإنجليزية، والإسبانية، والبرتغالية (البرازيل)، والإيطالية، والألمانية، والهولندية، والبولندية، والروسية، والصينية المبسّطة، والفيتنامية، والتايلاندية، والإندونيسية، واليابانية، والكورية، والهندية، والعربية. يتم الاختيار من الإعدادات («Langue / Language») ويسري بعد إعادة تشغيل الواجهة؛ ويفرض المتغير `OMEGA_SCAN_LANG` (مثلًا `OMEGA_SCAN_LANG=ar ./omega-scan.sh`) لغة طوال جلسة واحدة. عند التشغيل من omega-suite، يأخذ omega-scan لغة المجموعة. على وحدة التحكم النصية في Linux ‏(TTY)، تُعرض اللغات ذات الكتابة غير اللاتينية بالإنجليزية طوال الجلسة. يبقى سطر الأوامر بالفرنسية.

### وضع البرمجة النصية (CLI)

أي أمر فرعي يفعّل وضع CLI (نص بسيط، أو JSON مع `--json`):

```bash
# فحص هدف (يلزم --authorize إن لم يكن الهدف مثبّتًا مسبقًا)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# السجل
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# التصدير
./omega-scan.sh export scan-30577411758e --format html --output report.html

# أهداف مثبّتة بوصفها مأذونًا بها (لا حاجة إلى --authorize في الفحوص اللاحقة)
./omega-scan.sh targets pin example.org --note "اتفاق مع العميل 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### حارس إذن الهدف

لا يبدأ أي فحص دون تأكيد صريح للإذن على الهدف (مربع اختيار في TUI، و`--authorize` في CLI)، ما لم يكن الهدف مثبّتًا مسبقًا. ويجري التحقق في جهة التطبيق (`application/pipeline/guards/authorization_guard.py`)، لا في الواجهة وحدها.

### صيغ الهدف المقبولة

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 مع منفذ
::1                         IPv6
[2001:db8::10]:8443         IPv6 بين معقوفين مع منفذ
example.org                 اسم المضيف
intranet.lan:8080/admin     اسم مضيف مع منفذ ومسار
http://example.org          عنوان HTTP
https://example.org/admin   عنوان HTTPS
```

## 4. ملفات تعريف الفحص

| المعامل | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| الاستخدام | تحقق سريع | كامل (افتراضي) | معمّق | localhost / الشبكة المحلية |
| مهلة الاتصال/القراءة | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| طرق HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| استقصاء المسارات | لا | نعم (~20) | نعم (كامل) | نعم (~20) |
| TLS | لا | نعم | نعم (مفصّل) | نعم (متساهل) |
| مسبار CORS | لا | نعم | نعم | نعم |
| Catch-all | - | نعم | نعم | نعم |
| سياسة HSTS | غير مُقيَّمة | قياسية | صارمة | متساهلة |

### متى تستخدم كل ملف تعريف

- `quick`: تحقق خاطف قبل الإطلاق في بيئة الإنتاج
- `standard`: تدقيق كامل لخدمة قيد الإنتاج، وهو المستحسن
- `extended`: تدقيق معمّق يشمل طرق HTTP الخطرة
- `local-lab`: فحص localhost أو الشبكة المحلية دون معاقبة القواعد المصممة للخدمات العامة، ولا سيما HSTS

## 5. البنية المعمارية

بُني Omega-scan وفق **Clean Architecture** ‏(domain / application / infrastructure / interfaces / ports / core / app / plugins / shared)، بما يتّسق مع قالب مجموعة `omega-` (انظر `omega-stress`). التفاصيل الكاملة — شجرة المجلدات، وقواعد الاعتماد، والسلاسل الوظيفية، وتسلسل الاستثناءات، ونظام التسمية — موجودة في **`ARCHITECTURE.md`**، الوثيقة المرجعية المعيارية.

نظرة عامة قصيرة جدًا:

```text
src/omega_scan/
├── domain/          منطق أعمال خالص (الأهداف، وملفات التعريف، والفحوص، والتحققات، والتقارير، والسمات...)
├── application/     حالات الاستخدام (commands/queries)، وخط التنفيذ، والحراس
├── ports/           العقود التي يتوقعها التطبيق (المسابير، والمستودعات، والمُصدِّرات...)
├── infrastructure/  تنفيذات فعلية (httpx، SQLite؛ Textual ليس هنا)
├── interfaces/      tui/ ‏(Textual) وcli/ (قابل للبرمجة النصية)، بتكافؤ وظيفي صارم
├── app/             التجميع (DependencyContainer، bootstrap، دورة الحياة)
├── core/, shared/   مفردات مشتركة، وأدوات مساعدة خارج منطق الأعمال
└── plugins/         البنية جاهزة، فارغة (لا يوجد محور توسعة مؤكد)
```

قواعد التصميم التي لم تتغير منذ v1:
- `domain/checks/`: يحكم استنادًا إلى الأدلة، ولا يتصل بالشبكة أبدًا.
- `infrastructure/network/`: يتصل بالشبكة، ولا يُصدر أحكامًا أبدًا.
- `interfaces/`: تعرض فقط، ولا تحتوي أي منطق أعمال.
- `infrastructure/exporters/`: تقرأ نتيجة الفحص، ولا تعيد حساب أي شيء.

## 6. تصنيف القواعد

### النقل، `TRN-*`

- `TRN-HTTP-001`: ‏HTTP متاح دون إعادة توجيه إلى HTTPS، `WARN`
- `TRN-HTTPS-001`: ‏HTTPS غير متاح، `FAIL`
- `TRN-HSTS-001`: ترويسة HSTS غائبة، `FAIL`
- `TRN-HSTS-002`: قيمة `max-age` في HSTS منخفضة، أقل من سنة، `WARN`

### عمق TLS، `TLS-*`

- `TLS-VERSION-001`: بروتوكول TLS قديم (< TLSv1.2)، `FAIL`
- `TLS-CIPHER-001`: مجموعة تشفير ضعيفة بوضوح (RC4، DES، NULL، EXPORT، MD5)، `WARN`

### الترويسات، `HDR-*`

- `HDR-CSP-001`: ‏CSP غائبة في صفحة HTML، `FAIL`
- `HDR-CSP-002`: ‏CSP متساهلة أكثر من اللازم، `WARN`
- `HDR-NOSNIFF-001`: ‏`X-Content-Type-Options` غائبة، `WARN`
- `HDR-SERVER-001`: لافتة `Server` مكشوفة، `WARN`
- `HDR-CACHE-001`: ‏`Cache-Control` غائبة أو متساهلة في صفحة HTML، `WARN`

### ملفات تعريف الارتباط، `COO-*`

- `COO-SECURE-001`: ملف تعريف ارتباط في استجابة HTTPS دون السمة `Secure`، `WARN`
- `COO-HTTPONLY-001`: ملف تعريف ارتباط دون السمة `HttpOnly`، `WARN`
- `COO-SAMESITE-001`: ‏`SameSite` غائبة، أو `None` دون `Secure`، `WARN`

### CORS، `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: ‏`Access-Control-Allow-Origin: *` مقترنة بـ `Access-Control-Allow-Credentials: true`، `FAIL`
- `COR-REFLECTED-ORIGIN-001`: مصدر عشوائي منعكس كما هو في `Access-Control-Allow-Origin`، `WARN`

### طرق HTTP، `MTH-*`

- `MTH-OPTIONS-001`: الطريقة OPTIONS مفعّلة، `INFO`
- `MTH-TRACE-001`: الطريقة TRACE مفعّلة، `WARN`
- `MTH-PUT-001`: الطريقة PUT مفعّلة، `WARN`
- `MTH-DELETE-001`: الطريقة DELETE مفعّلة، `WARN`
- `MTH-PATCH-001`: الطريقة PATCH مفعّلة، `WARN`
- `MTH-CONNECT-001`: الطريقة CONNECT مفعّلة، `WARN`

### الانكشاف، `EXR-*`

- `EXR-ADMIN-001`: مسار الإدارة متاح دون مصادقة، `WARN`
- `EXR-SENSITIVE-001`: ملف حساس متاح، `.env`، `.git`، `FAIL`

### تسرّب المعلومات، `INF-*`

- `INF-BANNER-001`: لافتات الخادم مكشوفة، `WARN`
- `INF-ERROR-001`: رسائل خطأ مفصّلة، `WARN`
- `INF-STACK-001`: تتبّع المكدس (stack trace) مكشوف، `FAIL`
- `INF-ROBOTS-001`: ملف `robots.txt` موجود، `OK` للعلم
- `INF-HEADER-001`: ترويسات تقنية تكشف أكثر من اللازم، `WARN`
- `INF-SECURITYTXT-001`: ملف `/.well-known/security.txt` موجود، `OK` للعلم

## 7. سياسة الثقة

| المستوى | التعريف |
|---|---|
| `certain` | دليل مباشر لا لبس فيه، يُقرأ كما هو في الاستجابة: وجود الترويسة أو غيابها، ورمز HTTP الخام. |
| `high` | دليل واضح لكن سياقه غير مباشر: الطرق عبر OPTIONS، وملف تعريف ارتباط مُلاحظ. |
| `medium` | استنتاج ربما تأثر بوسيط: وكيل، أو WAF، أو نفق. |
| `low` | اكتشاف غير مباشر، أو محتوى ملتبس، أو حالة `catch_all_suspected`. |

### الخفض التلقائي

- `catch_all_suspected = true`: أقصى ثقة هي `low`
- `proxy_suspected = true`: أقصى ثقة هي `medium`
- `observed_access_state = ambiguous`: أقصى ثقة هي `low`

## 8. كشف الإنذارات الكاذبة

### سلوك catch-all

قبل اختبار المسارات الحساسة، يولّد Omega-scan مسارًا عشوائيًا مستبعَد الوجود. فإذا ردّ الخادم عليه بـ `200 OK`، يُوسَم الهدف بـ `catch_all_suspected = true` وتُخفَّض كل نتائج الانكشاف إلى `confidence = low`.

### المصادقة أم الغياب

المسار المحمي — `401` أو `403` أو إعادة توجيه إلى صفحة تسجيل الدخول — لا يُوسَم غائبًا ولا مكشوفًا. بل يُوسَم `N/A` مع الملاحظة: «مسار محمي، لا يمكن تأكيد وجوده دون مصادقة».

### الوكيل / النفق

إذا اكتُشفت ترويسات `X-Forwarded-*` أو `Via` أو `Forwarded`، تصبح `proxy_suspected` بقيمة `true`، وتُحدّ ثقة النتائج المعنية — اللافتات وTLS — عند `medium`.

## 9. التوافق مع الطرفيات

تكتشف واجهة TUI ‏(Textual) قدرات الطرفية تلقائيًا (اللون، والحجم) وتكيّف ورقة أنماطها البنيوية وفقًا لذلك (`complete`/`standard`/`reduced`/`mono`) — دون الخيارات اليدوية (`--no-emoji` و`--no-color` و`--plain`) التي كانت في v1. يبقى وضع CLI نصًا بسيطًا دائمًا (أو `--json`)، مستقلًا عن الطرفية.

## 10. التصدير

تُكتب التقارير النصية وتقارير HTML باللغة المختارة في الإعدادات («لغة التصدير»، وهي افتراضيًا لغة الواجهة)؛ ويبقى JSON بيانات لا تُترجم. تُنشأ التقارير افتراضيًا في `var/exports/` (مسار التشغيل، انظر `ARCHITECTURE.md`)، أو في المسار المحدد (`--output` في CLI، ومربع حوار في TUI).

### JSON، المرجع

البنية الكاملة للفحص (`ScanRun`)، قابلة للتسلسل إلى JSON بصرامة.

### النص، تقرير مقروء موجز

مقروء خارج الطرفية، دون رموز ANSI، وببنية هرمية.

### HTML، تقرير ويب سهل القراءة

تقرير مستقل مع CSS مضمّن، يمكن عرضه في أي متصفح، ومشاركته وأرشفته.

## 11. السجل والمقارنة

يُحفظ كل فحص (SQLite، `var/db/app.db`): سجل قابل للتصفح حسب الهدف، وتفاصيل تشغيل سابق، ومقارنة بين فحصين (نتائج ظهرت / حُلّت / لم تتغير / تغيّرت)، وإعادة تشغيل فحص على الهدف نفسه دون إعادة إدخاله — لم تكن موجودة في v1، وأُضيفت عند الانتقال إلى Clean Architecture.

## 12. الاختبارات

```bash
source .venv/bin/activate
pytest tests/ -v
```

البنية: `tests/unit/` (النطاق والتطبيق، دون إدخال/إخراج حقيقي)، و`tests/integration/` (SQLite/ملفات حقيقية، وخادم HTTP وهمي `pytest-httpserver`)، و`tests/e2e/` (CLI وTUI من البداية إلى النهاية، `Textual.testing`).

## 13. خارج النطاق

- فحص CVE
- الكشف النشط عن SQLi وXSS وRCE
- المصادقة المعقدة من جهة الماسح
- الزحف العميق
- التشويش (fuzzing)
- تخمين المسارات بالقوة الغاشمة على نطاق واسع
- الفحص المتزامن لعدة أهداف
- التوازي العدواني
- لوحة تحكم ويب

---

> Omega-scan — راقب، واجمع، وفسّر، وأبلغ.  
> ماسح للوضع الأمني، لا أداة هجوم.
