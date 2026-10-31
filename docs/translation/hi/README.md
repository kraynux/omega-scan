<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT लाइसेंस (LICENCE फ़ाइल देखें) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**वेब सुरक्षा स्थिति स्कैनर**

> [Omega-Server](https://kraynux.snake-mackarel.ts.net) के लिए [kraynux](https://github.com/kraynux) द्वारा निर्मित   

आधिकारिक पेज: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; झलक: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 इंटरफ़ेस और एक्सपोर्ट की गई रिपोर्टें **17 भाषाओं** में उपलब्ध हैं — देखें [इंटरफ़ेस की भाषाएँ](#इंटरफ़ेस-की-भाषाएँ)।  
**भाषाएँ:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** एक TUI + CLI टूल है जो आपकी HTTP/HTTPS सेवाओं की बाहर से दिखने वाली कॉन्फ़िगरेशन स्वच्छता का विश्लेषण करता है। यह देखता है, तथ्य जुटाता है, व्याख्या के नियम लागू करता है और ऐसी रिपोर्टें बनाता है जिन पर कार्रवाई की जा सके, बिना कभी कोई सक्रिय हमला किए। यह `omega-` सुइट का एक टूल है, Clean Architecture में बना — पूरी तकनीकी जानकारी के लिए `ARCHITECTURE.md` देखें।

## 1. दृष्टि और दायरा

Omega-scan सिस्टम प्रशासन के लिए बना वेब सुरक्षा स्थिति स्कैनर है: localhost, LAN या किसी बाहरी लक्ष्य पर किसी HTTP/HTTPS सेवा की दिखने वाली कॉन्फ़िगरेशन स्वच्छता को जल्दी जाँचना, Tailscale Funnel जैसी सुरंग के पीछे होने पर भी।

### Omega-scan क्या करता है

- देखे जा सकने वाले तथ्य जुटाता है: हेडर, कुकी, HTTP मेथड, TLS, संवेदनशील पथ, CORS हेडर।
- इन तथ्यों पर घोषणात्मक व्याख्या नियम लागू करता है।
- एकरूप, तर्कसंगत और कार्रवाई योग्य निष्कर्ष बनाता है।
- नतीजे TUI (Textual) या स्क्रिप्ट योग्य CLI में दिखाता है, और तीन एक्सपोर्ट देता है: JSON, टेक्स्ट, HTML।
- ग़लत चेतावनियों को पहचानता है, ख़ासकर catch-all व्यवहार और प्रमाणीकरण से सुरक्षित पथ।
- संदर्भ के अनुसार ढलता है: प्रॉक्सी, सुरंग, कई vhost, SNI।
- जो लक्ष्य पहले से अधिकृत के रूप में पिन नहीं है, उसे स्कैन करने से पहले स्पष्ट अनुमति की पुष्टि माँगता है।
- हर लक्ष्य के लिए स्कैन का स्थायी इतिहास रखता है, जिसे दोबारा चलाया और समय के साथ तुलना की जा सकती है।

### Omega-scan क्या नहीं करता

- सक्रिय कमज़ोरी स्कैन: कोई SQLi, XSS या RCE नहीं।
- CVE स्कैन।
- ब्रूट फ़ोर्स या बड़े पैमाने पर फ़ज़िंग का टूल।
- गहरा क्रॉलर।
- आक्रामक बहु-लक्ष्य समानांतर टूल।
- वेब डैशबोर्ड।
- स्कैनर की ओर से प्रमाणीकरण।

## 2. इंस्टॉलेशन

### आवश्यकताएँ

- Python 3.10+
- निर्भरताओं और बाहरी स्कैन के लिए इंटरनेट कनेक्शन

### इंस्टॉलेशन

आधिकारिक संग्रह `.tar.gz` प्रारूप में दिया जाता है। इंस्टॉल करने से पहले उसकी अखंडता जाँचें:

```bash
sha256sum omega-scan.tar.gz
```

### तरीका 1 — इंस्टॉलेशन स्क्रिप्ट

```bash
[ -d omega-scan ] && echo "ℹ️ यहाँ पहले से निकाला जा चुका है, यह चरण छोड़ा गया।" || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan पहले से मौजूद है, स्थानांतरण छोड़ा गया।" || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### तरीका 2 — मज़बूत पूर्ण इंस्टॉलेशन



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. वर्चुअल एनवायरनमेंट `.venv` बनाता है, अगर वह पहले से न हो।
2. निर्भरताएँ इंस्टॉल करता है (`pip install -e .`; `pyproject.toml` ही सत्य का एकमात्र स्रोत रहता है)।
3. `omega-scan.sh` और `install.sh` को चलाने योग्य बनाता है।
4. `~/.bashrc` और `~/.zshrc` में उपनाम `scan` जोड़ता है (पहले से हो तो दोहराता नहीं)।

### निर्भरताएँ

`pyproject.toml` में घोषित (अब कोई `requirements.txt` नहीं):
- `textual`: TUI इंटरफ़ेस, थीम, टर्मिनल के अनुसार अपने आप ढलना
- `httpx`: आधुनिक HTTP/HTTPS क्लाइंट
- `jinja2`: HTML एक्सपोर्ट के टेम्पलेट
- विकास निर्भरताएँ (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. उपयोग

### इंटरैक्टिव मोड (TUI)

रोज़मर्रा के उपयोग के लिए अनुशंसित — बिना आर्ग्युमेंट के चलाएँ:

```bash
./omega-scan.sh
```

क्रम: स्वागत स्क्रीन (कोई कुंजी दबाने या क्लिक करने पर बंद) → मुख्य मेनू → लक्ष्य भरना और प्रोफ़ाइल चुनना (अगर लक्ष्य पहले से पिन न हो तो अनुमति की पुष्टि के साथ) → स्कैन (प्रगति सूचक और नेटवर्क कार्यों का विवरण लाइव) → नतीजे (कुल अंक, श्रेणी के अनुसार छाँटे जा सकने वाले निष्कर्ष, किसी पंक्ति पर क्लिक करने पर विवरण) → मुख्य मेनू से एक्सपोर्ट/इतिहास/तुलना। टर्मिनल के अनुसार ढलना (रंग, आकार, संरचना का सरलीकरण) अपने आप होता है; अब प्रदर्शन के लिए मैनुअल विकल्पों की ज़रूरत नहीं।

#### कीबोर्ड शॉर्टकट

| कुंजी | क्रिया |
|---|---|
| `↑` / `↓` | स्क्रीन के तत्वों के बीच जाना |
| `Tab` / `Shift+Tab` | फ़ॉर्म के फ़ील्ड के बीच जाना |
| `Esc` | पिछली स्क्रीन पर लौटना (होम स्क्रीन पर बाहर निकलने की पुष्टि) |
| `t` | अगली थीम (तुरंत लागू, बिना पुष्टि) |
| `r` | टर्मिनल पहचान ताज़ा करना |
| `a` | सहायता दिखाना |
| `q` | बाहर निकलना (पुष्टि के साथ) |

### इंटरफ़ेस की भाषाएँ

इंटरफ़ेस 17 भाषाओं में उपलब्ध है: फ़्रेंच, अंग्रेज़ी, स्पेनिश, पुर्तगाली (ब्राज़ील), इतालवी, जर्मन, डच, पोलिश, रूसी, सरलीकृत चीनी, वियतनामी, थाई, इंडोनेशियाई, जापानी, कोरियाई, हिंदी और अरबी। चुनाव सेटिंग्स में होता है (“Langue / Language”) और इंटरफ़ेस दोबारा शुरू होने के बाद लागू होता है; चर `OMEGA_SCAN_LANG` (उदाहरण `OMEGA_SCAN_LANG=hi ./omega-scan.sh`) एक सत्र के लिए भाषा तय कर देता है। omega-suite से चलाने पर omega-scan सुइट की भाषा अपनाता है। Linux टेक्स्ट कंसोल (TTY) पर गैर-लैटिन लिपि वाली भाषाएँ उस सत्र में अंग्रेज़ी में दिखती हैं। कमांड लाइन फ़्रेंच में ही रहती है।

### स्क्रिप्ट मोड (CLI)

कोई भी उप-कमांड CLI मोड चालू कर देता है (सादा टेक्स्ट, या `--json` के साथ JSON):

```bash
# किसी लक्ष्य को स्कैन करें (लक्ष्य पहले से पिन न हो तो --authorize ज़रूरी)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# इतिहास
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# एक्सपोर्ट
./omega-scan.sh export scan-30577411758e --format html --output report.html

# अधिकृत के रूप में पिन किए गए लक्ष्य (आगे के स्कैन में --authorize की ज़रूरत नहीं)
./omega-scan.sh targets pin example.org --note "ग्राहक समझौता 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### लक्ष्य अनुमति सुरक्षा

जब तक लक्ष्य पहले से पिन न हो, लक्ष्य पर स्पष्ट अनुमति की पुष्टि (TUI में चेकबॉक्स, CLI में `--authorize`) के बिना कोई स्कैन शुरू नहीं होता। यह जाँच केवल इंटरफ़ेस में नहीं, बल्कि एप्लिकेशन की ओर (`application/pipeline/guards/authorization_guard.py`) होती है।

### स्वीकार्य लक्ष्य प्रारूप

```text
192.168.1.10                IPv4
192.168.1.10:8080           पोर्ट सहित IPv4
::1                         IPv6
[2001:db8::10]:8443         कोष्ठक और पोर्ट सहित IPv6
example.org                 होस्ट नाम
intranet.lan:8080/admin     पोर्ट और पथ सहित होस्ट नाम
http://example.org          HTTP URL
https://example.org/admin   HTTPS URL
```

## 4. स्कैन प्रोफ़ाइल

| मापदंड | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| उपयोग | त्वरित जाँच | पूर्ण (डिफ़ॉल्ट) | गहन | localhost / LAN |
| कनेक्शन/पढ़ने की समय-सीमा | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| HTTP मेथड | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| पथों की जाँच | नहीं | हाँ (~20) | हाँ (पूर्ण) | हाँ (~20) |
| TLS | नहीं | हाँ | हाँ (विस्तृत) | हाँ (उदार) |
| CORS जाँच | नहीं | हाँ | हाँ | हाँ |
| Catch-all | - | हाँ | हाँ | हाँ |
| HSTS नीति | मूल्यांकन नहीं | मानक | सख़्त | उदार |

### कौन-सी प्रोफ़ाइल कब

- `quick`: उत्पादन में डालने से पहले बिजली जैसी तेज़ जाँच
- `standard`: उत्पादन में चल रही सेवा का पूर्ण ऑडिट, अनुशंसित
- `extended`: जोखिम भरे HTTP मेथड सहित गहन ऑडिट
- `local-lab`: localhost या LAN का स्कैन, सार्वजनिक सेवाओं के लिए बने नियमों (ख़ासकर HSTS) के कारण अंक कटे बिना

## 5. आर्किटेक्चर

Omega-scan **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared) में बना है, `omega-` सुइट के ढाँचे के अनुरूप (देखें `omega-stress`)। पूरा विवरण — फ़ोल्डर संरचना, निर्भरता के नियम, कार्यात्मक शृंखलाएँ, अपवादों का पदानुक्रम, नामकरण पद्धति — **`ARCHITECTURE.md`** में है, जो मानक संदर्भ दस्तावेज़ है।

बहुत छोटा सार:

```text
src/omega_scan/
├── domain/          शुद्ध व्यावसायिक तर्क (लक्ष्य, प्रोफ़ाइल, स्कैन, जाँचें, रिपोर्ट, थीम...)
├── application/     उपयोग के मामले (commands/queries), निष्पादन पाइपलाइन, सुरक्षा जाँचें
├── ports/           एप्लिकेशन द्वारा अपेक्षित अनुबंध (जाँचकर्ता, रिपॉज़िटरी, एक्सपोर्टर...)
├── infrastructure/  ठोस कार्यान्वयन (httpx, SQLite; Textual यहाँ नहीं है)
├── interfaces/      tui/ (Textual) और cli/ (स्क्रिप्ट योग्य), सख़्त कार्यात्मक समानता के साथ
├── app/             जोड़ना (DependencyContainer, bootstrap, जीवन-चक्र)
├── core/, shared/   साझा शब्दावली, गैर-व्यावसायिक उपयोगिताएँ
└── plugins/         ढाँचा तैयार, खाली (कोई पुष्ट विस्तार दिशा नहीं)
```

v1 से अपरिवर्तित डिज़ाइन नियम:
- `domain/checks/`: प्रमाणों के आधार पर निर्णय देता है, कभी नेटवर्क का उपयोग नहीं करता।
- `infrastructure/network/`: नेटवर्क का उपयोग करता है, कभी निर्णय नहीं देता।
- `interfaces/`: केवल दिखाता है, कोई व्यावसायिक तर्क नहीं रखता।
- `infrastructure/exporters/`: स्कैन का नतीजा पढ़ते हैं, कुछ भी दोबारा नहीं निकालते।

## 6. नियमों का वर्गीकरण

### परिवहन, `TRN-*`

- `TRN-HTTP-001`: HTTPS पर रीडायरेक्ट के बिना HTTP उपलब्ध, `WARN`
- `TRN-HTTPS-001`: HTTPS उपलब्ध नहीं, `FAIL`
- `TRN-HSTS-001`: HSTS हेडर नहीं है, `FAIL`
- `TRN-HSTS-002`: HSTS का `max-age` कम, 1 वर्ष से कम, `WARN`

### TLS की गहराई, `TLS-*`

- `TLS-VERSION-001`: पुराना TLS प्रोटोकॉल (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: स्पष्ट रूप से कमज़ोर सिफ़र सूट (RC4, DES, NULL, EXPORT, MD5), `WARN`

### हेडर, `HDR-*`

- `HDR-CSP-001`: HTML पेज पर CSP नहीं है, `FAIL`
- `HDR-CSP-002`: बहुत ढीली CSP, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` नहीं है, `WARN`
- `HDR-SERVER-001`: `Server` बैनर उजागर, `WARN`
- `HDR-CACHE-001`: HTML पेज पर `Cache-Control` नहीं है या बहुत ढीला है, `WARN`

### कुकी, `COO-*`

- `COO-SECURE-001`: HTTPS उत्तर की कुकी में `Secure` विशेषता नहीं, `WARN`
- `COO-HTTPONLY-001`: कुकी में `HttpOnly` विशेषता नहीं, `WARN`
- `COO-SAMESITE-001`: `SameSite` नहीं है, या `Secure` के बिना `None`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` के साथ `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: कोई भी मूल `Access-Control-Allow-Origin` में ज्यों-का-त्यों लौटाया गया, `WARN`

### HTTP मेथड, `MTH-*`

- `MTH-OPTIONS-001`: OPTIONS मेथड सक्षम, `INFO`
- `MTH-TRACE-001`: TRACE मेथड सक्षम, `WARN`
- `MTH-PUT-001`: PUT मेथड सक्षम, `WARN`
- `MTH-DELETE-001`: DELETE मेथड सक्षम, `WARN`
- `MTH-PATCH-001`: PATCH मेथड सक्षम, `WARN`
- `MTH-CONNECT-001`: CONNECT मेथड सक्षम, `WARN`

### उजागर होना, `EXR-*`

- `EXR-ADMIN-001`: एडमिन पथ बिना प्रमाणीकरण के उपलब्ध, `WARN`
- `EXR-SENSITIVE-001`: संवेदनशील फ़ाइल उपलब्ध, `.env`, `.git`, `FAIL`

### जानकारी का रिसाव, `INF-*`

- `INF-BANNER-001`: सर्वर बैनर उजागर, `WARN`
- `INF-ERROR-001`: विस्तृत त्रुटि संदेश, `WARN`
- `INF-STACK-001`: स्टैक ट्रेस उजागर, `FAIL`
- `INF-ROBOTS-001`: `robots.txt` फ़ाइल मौजूद, `OK` जानकारी के लिए
- `INF-HEADER-001`: ज़रूरत से ज़्यादा बताने वाले तकनीकी हेडर, `WARN`
- `INF-SECURITYTXT-001`: `/.well-known/security.txt` फ़ाइल मौजूद, `OK` जानकारी के लिए

## 7. विश्वास नीति

| स्तर | परिभाषा |
|---|---|
| `certain` | उत्तर से ज्यों-का-त्यों पढ़ा गया सीधा, असंदिग्ध प्रमाण: हेडर है या नहीं, कच्चा HTTP कोड। |
| `high` | स्पष्ट प्रमाण पर संदर्भ अप्रत्यक्ष: OPTIONS से मिले मेथड, देखी गई कुकी। |
| `medium` | ऐसा निष्कर्ष जिस पर किसी मध्यस्थ का असर हो सकता है: प्रॉक्सी, WAF, सुरंग। |
| `low` | अप्रत्यक्ष पहचान, अस्पष्ट सामग्री, या `catch_all_suspected` स्थिति। |

### स्वचालित स्तर-घटाव

- `catch_all_suspected = true`: विश्वास की अधिकतम सीमा `low`
- `proxy_suspected = true`: विश्वास की अधिकतम सीमा `medium`
- `observed_access_state = ambiguous`: विश्वास की अधिकतम सीमा `low`

## 8. ग़लत चेतावनियों की पहचान

### catch-all व्यवहार

संवेदनशील पथों को जाँचने से पहले Omega-scan एक ऐसा यादृच्छिक पथ बनाता है जिसके होने की संभावना नहीं होती। अगर सर्वर उस पर `200 OK` लौटाए, तो लक्ष्य को `catch_all_suspected = true` चिह्नित किया जाता है और उजागर होने से जुड़े सभी निष्कर्ष `confidence = low` पर उतार दिए जाते हैं।

### प्रमाणीकरण या अनुपस्थिति

सुरक्षित पथ — `401`, `403` या लॉगिन पेज पर रीडायरेक्ट — को न अनुपस्थित माना जाता है, न उजागर। उसे इस टिप्पणी के साथ `N/A` चिह्नित किया जाता है: “सुरक्षित पथ, बिना प्रमाणीकरण के उपस्थिति की पुष्टि संभव नहीं”।

### प्रॉक्सी / सुरंग

अगर `X-Forwarded-*`, `Via` या `Forwarded` हेडर मिलते हैं, तो `proxy_suspected` `true` हो जाता है और संबंधित निष्कर्षों — बैनर, TLS — का विश्वास अधिकतम `medium` तक सीमित हो जाता है।

## 9. टर्मिनल संगतता

TUI (Textual) अपने आप टर्मिनल की क्षमताएँ (रंग, आकार) पहचानता है और उसके अनुसार अपनी संरचनात्मक स्टाइलशीट बदलता है (`complete`/`standard`/`reduced`/`mono`) — अब v1 की तरह मैनुअल विकल्पों (`--no-emoji`, `--no-color`, `--plain`) की ज़रूरत नहीं। CLI मोड हमेशा सादा टेक्स्ट (या `--json`) रहता है, टर्मिनल से स्वतंत्र।

## 10. एक्सपोर्ट

टेक्स्ट और HTML रिपोर्टें सेटिंग्स में चुनी गई भाषा में लिखी जाती हैं (“एक्सपोर्ट की भाषा”, डिफ़ॉल्ट रूप से इंटरफ़ेस वाली); JSON डेटा ही रहता है, उसका अनुवाद नहीं होता। रिपोर्टें डिफ़ॉल्ट रूप से `var/exports/` में बनती हैं (रनटाइम पथ, देखें `ARCHITECTURE.md`), या बताए गए पथ पर (CLI में `--output`, TUI में संवाद बॉक्स)।

### JSON, सत्य का स्रोत

स्कैन की पूरी संरचना (`ScanRun`), सख़्ती से JSON में बदलने योग्य।

### टेक्स्ट, संक्षिप्त पठनीय रिपोर्ट

टर्मिनल के बाहर भी पठनीय, बिना ANSI कोड के, श्रेणीबद्ध संरचना के साथ।

### HTML, पठनीय वेब रिपोर्ट

इनलाइन CSS वाली स्वतंत्र रिपोर्ट, किसी भी ब्राउज़र में देखी जा सकती है, साझा और संग्रहीत की जा सकती है।

## 11. इतिहास और तुलना

हर स्कैन सहेजा जाता है (SQLite, `var/db/app.db`): लक्ष्य के अनुसार इतिहास देखना, पिछले रन का विवरण, दो स्कैन की तुलना (नए दिखे / सुलझे / अपरिवर्तित / बदले हुए निष्कर्ष), और उसी लक्ष्य पर बिना दोबारा भरे स्कैन दोहराना — ये v1 में नहीं थे, Clean Architecture में बदलाव के दौरान जोड़े गए।

## 12. परीक्षण

```bash
source .venv/bin/activate
pytest tests/ -v
```

संरचना: `tests/unit/` (बिना असली I/O के डोमेन और एप्लिकेशन), `tests/integration/` (असली SQLite/फ़ाइलें, नकली HTTP सर्वर `pytest-httpserver`), `tests/e2e/` (शुरू से अंत तक CLI और TUI, `Textual.testing`)।

## 13. दायरे से बाहर

- CVE स्कैन
- SQLi, XSS, RCE की सक्रिय पहचान
- स्कैनर की ओर से जटिल प्रमाणीकरण
- गहरी क्रॉलिंग
- फ़ज़िंग
- पथों पर बड़े पैमाने पर ब्रूट फ़ोर्स
- कई लक्ष्यों का एक साथ स्कैन
- आक्रामक समानांतरता
- वेब डैशबोर्ड

---

> Omega-scan — देखो, जुटाओ, व्याख्या करो, रिपोर्ट करो।  
> सुरक्षा स्थिति का स्कैनर, हमले का औज़ार नहीं।
