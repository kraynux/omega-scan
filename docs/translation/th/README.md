<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - สัญญาอนุญาต MIT (ดูไฟล์ LICENCE) -->
<div align="center">
  <img src="../../assets/omega-scan.png" alt="Omega-Scan" width="384">
</div>

# 🔍 OMEGA-SCAN

**เครื่องมือสแกนสถานะความปลอดภัยของเว็บ**

> พัฒนาโดย [kraynux](https://github.com/kraynux) สำหรับ [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

หน้าทางการ: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; ภาพหน้าจอ: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 อินเทอร์เฟซและรายงานที่ส่งออกมีให้ใช้ **17 ภาษา** — ดู [ภาษาของอินเทอร์เฟซ](#ภาษาของอินเทอร์เฟซ)  
**ภาษา:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** เป็นเครื่องมือแบบ TUI + CLI ที่วิเคราะห์ความเรียบร้อยของการตั้งค่าที่มองเห็นได้จากภายนอกของบริการ HTTP/HTTPS ของคุณ มันสังเกต เก็บข้อเท็จจริง ใช้กฎการตีความ และสร้างรายงานที่นำไปปฏิบัติได้ โดยไม่ทำการโจมตีเชิงรุกใด ๆ เลย เป็นเครื่องมือหนึ่งในชุด `omega-` จัดโครงสร้างตาม Clean Architecture — รายละเอียดทางเทคนิคทั้งหมดดูที่ `ARCHITECTURE.md`

## 1. วิสัยทัศน์และขอบเขต

Omega-scan เป็นเครื่องมือสแกนสถานะความปลอดภัยของเว็บสำหรับงานดูแลระบบ: ตรวจอย่างรวดเร็วว่าการตั้งค่าที่มองเห็นได้ของบริการ HTTP/HTTPS บน localhost ใน LAN หรือบนเป้าหมายภายนอก (รวมถึงที่อยู่หลังอุโมงค์อย่าง Tailscale Funnel) เรียบร้อยดีเพียงใด

### สิ่งที่ Omega-scan ทำ

- เก็บข้อเท็จจริงที่สังเกตได้: ส่วนหัว คุกกี้ เมธอด HTTP, TLS เส้นทางที่อ่อนไหว ส่วนหัว CORS
- ใช้กฎการตีความแบบประกาศกับข้อเท็จจริงเหล่านั้น
- สร้างข้อค้นพบที่เป็นรูปแบบเดียวกัน มีเหตุผลรองรับ และนำไปปฏิบัติได้
- แสดงผลใน TUI (Textual) หรือ CLI ที่เขียนสคริปต์ได้ และส่งออกได้สามแบบ: JSON ข้อความ HTML
- ตรวจจับผลบวกลวง โดยเฉพาะพฤติกรรม catch-all และเส้นทางที่ป้องกันด้วยการยืนยันตัวตน
- ปรับให้เข้ากับบริบท: พร็อกซี อุโมงค์ หลาย vhost, SNI
- ต้องยืนยันการได้รับอนุญาตอย่างชัดเจนก่อนสแกนเป้าหมายใดที่ยังไม่ได้ปักหมุดว่าได้รับอนุญาต
- เก็บประวัติการสแกนถาวรแยกตามเป้าหมาย เรียกซ้ำและเปรียบเทียบข้ามเวลาได้

### สิ่งที่ Omega-scan ไม่ทำ

- สแกนช่องโหว่เชิงรุก: ไม่มี SQLi, XSS หรือ RCE
- สแกน CVE
- เครื่องมือ brute force หรือฟัซซิงจำนวนมาก
- โปรแกรมไล่เก็บหน้าเว็บเชิงลึก
- เครื่องมือสแกนหลายเป้าหมายพร้อมกันแบบรุนแรง
- แดชบอร์ดเว็บ
- การยืนยันตัวตนฝั่งเครื่องมือสแกน

## 2. การติดตั้ง

### ข้อกำหนดเบื้องต้น

- Python 3.10+
- การเชื่อมต่ออินเทอร์เน็ต สำหรับส่วนที่ต้องพึ่งพาและการสแกนภายนอก

### การติดตั้ง

ไฟล์เก็บถาวรอย่างเป็นทางการมาในรูปแบบ `.tar.gz` ตรวจความถูกต้องก่อนติดตั้ง:

```bash
sha256sum omega-scan.tar.gz
```

### วิธีที่ 1 — สคริปต์ติดตั้ง

```bash
[ -d omega-scan ] && echo "ℹ️ แตกไฟล์ไว้ที่นี่แล้ว ข้ามขั้นตอนนี้" || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ มี ~/omega-scan อยู่แล้ว ข้ามการย้าย" || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### วิธีที่ 2 — ติดตั้งครบถ้วนแบบทนทาน



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. สร้างสภาพแวดล้อมเสมือน `.venv` หากยังไม่มี
2. ติดตั้งส่วนที่ต้องพึ่งพา (`pip install -e .`; `pyproject.toml` ยังคงเป็นแหล่งข้อมูลหลักเพียงแหล่งเดียว)
3. ทำให้ `omega-scan.sh` และ `install.sh` เรียกใช้งานได้
4. เพิ่มชื่อแทน `scan` ลงใน `~/.bashrc` และ `~/.zshrc` (ไม่เพิ่มซ้ำหากมีอยู่แล้ว)

### ส่วนที่ต้องพึ่งพา

ประกาศไว้ใน `pyproject.toml` (ไม่มี `requirements.txt` แล้ว):
- `textual`: อินเทอร์เฟซ TUI ธีม และการปรับให้เข้ากับเทอร์มินัลโดยอัตโนมัติ
- `httpx`: ไคลเอนต์ HTTP/HTTPS รุ่นใหม่
- `jinja2`: เทมเพลตสำหรับการส่งออก HTML
- ส่วนที่ต้องพึ่งพาสำหรับการพัฒนา (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. การใช้งาน

### โหมดโต้ตอบ (TUI)

แนะนำสำหรับการใช้งานประจำวัน — เรียกโดยไม่ใส่อาร์กิวเมนต์:

```bash
./omega-scan.sh
```

ลำดับการใช้งาน: หน้าจอเริ่มต้น (ปิดด้วยการกดปุ่มหรือคลิก) → เมนูหลัก → กรอกเป้าหมายและเลือกโปรไฟล์ (พร้อมยืนยันการได้รับอนุญาตหากเป้าหมายยังไม่ได้ปักหมุด) → การสแกน (แถบความคืบหน้าและรายละเอียดการทำงานเครือข่ายแสดงสด) → ผลลัพธ์ (คะแนนรวม ข้อค้นพบที่กรองตามหมวดหมู่ได้ รายละเอียดเมื่อคลิกที่บรรทัด) → การส่งออก/ประวัติ/การเปรียบเทียบจากเมนูหลัก การปรับให้เข้ากับเทอร์มินัล (สี ขนาด การลดทอนโครงสร้าง) เป็นไปโดยอัตโนมัติ ไม่ต้องใช้ตัวเลือกการแสดงผลด้วยตนเองอีกต่อไป

#### แป้นลัด

| แป้น | การทำงาน |
|---|---|
| `↑` / `↓` | เลื่อนไปมาระหว่างรายการบนหน้าจอ |
| `Tab` / `Shift+Tab` | เลื่อนไปมาระหว่างช่องของแบบฟอร์ม |
| `Esc` | กลับไปหน้าจอก่อนหน้า (ยืนยันการออกเมื่ออยู่ที่หน้าแรก) |
| `t` | ธีมถัดไป (ใช้ทันที ไม่ต้องยืนยัน) |
| `r` | รีเฟรชการตรวจจับเทอร์มินัล |
| `a` | แสดงความช่วยเหลือ |
| `q` | ออก (ต้องยืนยัน) |

### ภาษาของอินเทอร์เฟซ

อินเทอร์เฟซมีให้ใช้ 17 ภาษา: ฝรั่งเศส อังกฤษ สเปน โปรตุเกส (บราซิล) อิตาลี เยอรมัน ดัตช์ โปแลนด์ รัสเซีย จีนตัวย่อ เวียดนาม ไทย อินโดนีเซีย ญี่ปุ่น เกาหลี ฮินดี และอาหรับ เลือกได้ในการตั้งค่า (“Langue / Language”) และมีผลหลังจากรีสตาร์ตอินเทอร์เฟซ ตัวแปร `OMEGA_SCAN_LANG` (เช่น `OMEGA_SCAN_LANG=th ./omega-scan.sh`) ใช้บังคับภาษาสำหรับหนึ่งเซสชัน เมื่อเปิดจาก omega-suite แล้ว omega-scan จะใช้ภาษาของชุดเครื่องมือ บนคอนโซลข้อความของ Linux (TTY) ภาษาที่ไม่ได้ใช้อักษรละตินจะแสดงเป็นภาษาอังกฤษตลอดเซสชันนั้น บรรทัดคำสั่งยังคงเป็นภาษาฝรั่งเศส

### โหมดสคริปต์ (CLI)

คำสั่งย่อยใดก็ตามจะเปิดโหมด CLI (ข้อความธรรมดา หรือ JSON ด้วย `--json`):

```bash
# สแกนเป้าหมาย (ต้องใช้ --authorize หากเป้าหมายยังไม่ได้ปักหมุด)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# ประวัติ
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# การส่งออก
./omega-scan.sh export scan-30577411758e --format html --output report.html

# เป้าหมายที่ปักหมุดว่าได้รับอนุญาต (การสแกนครั้งถัดไปไม่ต้องใช้ --authorize)
./omega-scan.sh targets pin example.org --note "ข้อตกลงกับลูกค้า 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### ด่านตรวจการได้รับอนุญาตของเป้าหมาย

จะไม่มีการสแกนใดเริ่มต้นหากไม่มีการยืนยันการได้รับอนุญาตสำหรับเป้าหมายอย่างชัดเจน (ช่องทำเครื่องหมายใน TUI, `--authorize` ใน CLI) เว้นแต่เป้าหมายจะถูกปักหมุดไว้แล้ว การตรวจนี้ทำในฝั่งแอปพลิเคชัน (`application/pipeline/guards/authorization_guard.py`) ไม่ใช่แค่ในอินเทอร์เฟซ

### รูปแบบเป้าหมายที่รับได้

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 พร้อมพอร์ต
::1                         IPv6
[2001:db8::10]:8443         IPv6 ในวงเล็บเหลี่ยมพร้อมพอร์ต
example.org                 ชื่อโฮสต์
intranet.lan:8080/admin     ชื่อโฮสต์พร้อมพอร์ตและเส้นทาง
http://example.org          URL แบบ HTTP
https://example.org/admin   URL แบบ HTTPS
```

## 4. โปรไฟล์การสแกน

| พารามิเตอร์ | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| การใช้งาน | ตรวจเร็ว | ครบถ้วน (ค่าเริ่มต้น) | เชิงลึก | localhost / LAN |
| เวลารอเชื่อมต่อ/อ่าน | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| เมธอด HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| ตรวจเส้นทาง | ไม่ | ใช่ (~20) | ใช่ (ครบ) | ใช่ (~20) |
| TLS | ไม่ | ใช่ | ใช่ (ละเอียด) | ใช่ (ผ่อนปรน) |
| ตัวตรวจ CORS | ไม่ | ใช่ | ใช่ | ใช่ |
| Catch-all | - | ใช่ | ใช่ | ใช่ |
| นโยบาย HSTS | ไม่ประเมิน | มาตรฐาน | เข้มงวด | ผ่อนปรน |

### ควรใช้โปรไฟล์ใดเมื่อใด

- `quick`: ตรวจแบบสายฟ้าแลบก่อนนำขึ้นใช้งานจริง
- `standard`: ตรวจสอบบริการที่ใช้งานจริงอย่างครบถ้วน แนะนำ
- `extended`: ตรวจสอบเชิงลึกรวมถึงเมธอด HTTP ที่มีความเสี่ยง
- `local-lab`: สแกน localhost หรือ LAN โดยไม่ถูกหักคะแนนจากกฎที่ออกแบบมาสำหรับบริการสาธารณะ โดยเฉพาะ HSTS

## 5. สถาปัตยกรรม

Omega-scan จัดโครงสร้างตาม **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared) สอดคล้องกับแม่แบบของชุด `omega-` (ดู `omega-stress`) รายละเอียดทั้งหมด — โครงสร้างโฟลเดอร์ กฎการพึ่งพา สายงานเชิงหน้าที่ ลำดับชั้นของข้อยกเว้น ระบบการตั้งชื่อ — อยู่ใน **`ARCHITECTURE.md`** ซึ่งเป็นเอกสารอ้างอิงเชิงบรรทัดฐาน

ภาพรวมแบบสั้นมาก:

```text
src/omega_scan/
├── domain/          ตรรกะทางธุรกิจล้วน (เป้าหมาย โปรไฟล์ การสแกน การตรวจ รายงาน ธีม...)
├── application/     กรณีการใช้งาน (commands/queries) ไปป์ไลน์การทำงาน ด่านตรวจ
├── ports/           สัญญาที่แอปพลิเคชันคาดหวัง (ตัวตรวจ ที่เก็บข้อมูล ตัวส่งออก...)
├── infrastructure/  การทำงานจริง (httpx, SQLite; Textual ไม่ได้อยู่ที่นี่)
├── interfaces/      tui/ (Textual) และ cli/ (เขียนสคริปต์ได้) ความสามารถเท่ากันอย่างเคร่งครัด
├── app/             การประกอบ (DependencyContainer, bootstrap, วงจรชีวิต)
├── core/, shared/   คำศัพท์ร่วม เครื่องมือที่ไม่เกี่ยวกับธุรกิจ
└── plugins/         วางโครงสร้างไว้แล้ว ยังว่าง (ยังไม่มีแนวทางขยายที่ยืนยันแล้ว)
```

กฎการออกแบบที่ไม่เปลี่ยนตั้งแต่ v1:
- `domain/checks/`: ตัดสินจากหลักฐาน ไม่เข้าถึงเครือข่ายเลย
- `infrastructure/network/`: ทำงานกับเครือข่าย ไม่ตัดสินใด ๆ
- `interfaces/`: แสดงผล ไม่มีตรรกะทางธุรกิจ
- `infrastructure/exporters/`: อ่านผลการสแกน ไม่คำนวณสิ่งใดใหม่

## 6. ระบบกฎ

### การรับส่งข้อมูล, `TRN-*`

- `TRN-HTTP-001`: เข้าถึง HTTP ได้โดยไม่เปลี่ยนเส้นทางไป HTTPS, `WARN`
- `TRN-HTTPS-001`: เข้าถึง HTTPS ไม่ได้, `FAIL`
- `TRN-HSTS-001`: ไม่มีส่วนหัว HSTS, `FAIL`
- `TRN-HSTS-002`: `max-age` ของ HSTS ต่ำ น้อยกว่า 1 ปี, `WARN`

### ความลึกของ TLS, `TLS-*`

- `TLS-VERSION-001`: โปรโตคอล TLS ที่ล้าสมัย (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: ชุดการเข้ารหัสที่อ่อนอย่างชัดเจน (RC4, DES, NULL, EXPORT, MD5), `WARN`

### ส่วนหัว, `HDR-*`

- `HDR-CSP-001`: ไม่มี CSP บนหน้า HTML, `FAIL`
- `HDR-CSP-002`: CSP ผ่อนปรนเกินไป, `WARN`
- `HDR-NOSNIFF-001`: ไม่มี `X-Content-Type-Options`, `WARN`
- `HDR-SERVER-001`: เปิดเผยแบนเนอร์ `Server`, `WARN`
- `HDR-CACHE-001`: ไม่มี `Cache-Control` หรือผ่อนปรนเกินไปบนหน้า HTML, `WARN`

### คุกกี้, `COO-*`

- `COO-SECURE-001`: คุกกี้ในการตอบกลับ HTTPS ที่ไม่มีแอตทริบิวต์ `Secure`, `WARN`
- `COO-HTTPONLY-001`: คุกกี้ที่ไม่มีแอตทริบิวต์ `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: ไม่มี `SameSite` หรือเป็น `None` โดยไม่มี `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` ร่วมกับ `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: origin ใดก็ได้ถูกสะท้อนกลับตามเดิมใน `Access-Control-Allow-Origin`, `WARN`

### เมธอด HTTP, `MTH-*`

- `MTH-OPTIONS-001`: เปิดใช้เมธอด OPTIONS, `INFO`
- `MTH-TRACE-001`: เปิดใช้เมธอด TRACE, `WARN`
- `MTH-PUT-001`: เปิดใช้เมธอด PUT, `WARN`
- `MTH-DELETE-001`: เปิดใช้เมธอด DELETE, `WARN`
- `MTH-PATCH-001`: เปิดใช้เมธอด PATCH, `WARN`
- `MTH-CONNECT-001`: เปิดใช้เมธอด CONNECT, `WARN`

### การเปิดเผย, `EXR-*`

- `EXR-ADMIN-001`: เข้าถึงเส้นทางผู้ดูแลระบบได้โดยไม่ต้องยืนยันตัวตน, `WARN`
- `EXR-SENSITIVE-001`: เข้าถึงไฟล์ที่อ่อนไหวได้, `.env`, `.git`, `FAIL`

### ข้อมูลรั่วไหล, `INF-*`

- `INF-BANNER-001`: เปิดเผยแบนเนอร์ของเซิร์ฟเวอร์, `WARN`
- `INF-ERROR-001`: ข้อความแสดงข้อผิดพลาดแบบละเอียด, `WARN`
- `INF-STACK-001`: เปิดเผย stack trace, `FAIL`
- `INF-ROBOTS-001`: มีไฟล์ `robots.txt`, `OK` เพื่อเป็นข้อมูล
- `INF-HEADER-001`: ส่วนหัวทางเทคนิคเปิดเผยข้อมูลมากเกินไป, `WARN`
- `INF-SECURITYTXT-001`: มีไฟล์ `/.well-known/security.txt`, `OK` เพื่อเป็นข้อมูล

## 7. นโยบายความเชื่อมั่น

| ระดับ | นิยาม |
|---|---|
| `certain` | หลักฐานตรง ไม่กำกวม อ่านได้ตามเดิมจากการตอบกลับ: มีหรือไม่มีส่วนหัว รหัส HTTP ดิบ |
| `high` | หลักฐานชัดเจนแต่บริบทอ้อม: เมธอดผ่าน OPTIONS คุกกี้ที่สังเกตได้ |
| `medium` | ข้อสรุปที่อาจได้รับผลจากตัวกลาง: พร็อกซี, WAF อุโมงค์ |
| `low` | ตรวจพบทางอ้อม เนื้อหากำกวม หรืออยู่ในสถานการณ์ `catch_all_suspected` |

### การลดระดับอัตโนมัติ

- `catch_all_suspected = true`: ความเชื่อมั่นสูงสุดที่ `low`
- `proxy_suspected = true`: ความเชื่อมั่นสูงสุดที่ `medium`
- `observed_access_state = ambiguous`: ความเชื่อมั่นสูงสุดที่ `low`

## 8. การตรวจจับผลบวกลวง

### พฤติกรรม catch-all

ก่อนทดสอบเส้นทางที่อ่อนไหว Omega-scan จะสร้างเส้นทางสุ่มที่ไม่น่าจะมีอยู่จริง หากเซิร์ฟเวอร์ตอบ `200 OK` เป้าหมายจะถูกทำเครื่องหมาย `catch_all_suspected = true` และข้อค้นพบด้านการเปิดเผยทั้งหมดจะถูกลดระดับเป็น `confidence = low`

### การยืนยันตัวตนกับการไม่มีอยู่

เส้นทางที่ได้รับการป้องกัน — `401`, `403` หรือการเปลี่ยนเส้นทางไปหน้าเข้าสู่ระบบ — จะไม่ถูกทำเครื่องหมายว่าไม่มีอยู่ และไม่ถูกทำเครื่องหมายว่าถูกเปิดเผย แต่จะถูกทำเครื่องหมาย `N/A` พร้อมหมายเหตุ: “เส้นทางที่ได้รับการป้องกัน ยืนยันการมีอยู่ไม่ได้หากไม่ยืนยันตัวตน”

### พร็อกซี / อุโมงค์

หากตรวจพบส่วนหัว `X-Forwarded-*`, `Via` หรือ `Forwarded` ค่า `proxy_suspected` จะเปลี่ยนเป็น `true` และความเชื่อมั่นของข้อค้นพบที่เกี่ยวข้อง — แบนเนอร์, TLS — จะถูกจำกัดสูงสุดที่ `medium`

## 9. ความเข้ากันได้กับเทอร์มินัล

TUI (Textual) ตรวจจับความสามารถของเทอร์มินัล (สี ขนาด) โดยอัตโนมัติ และปรับสไตล์ชีตเชิงโครงสร้างให้เหมาะสม (`complete`/`standard`/`reduced`/`mono`) — ไม่ต้องใช้ตัวเลือกด้วยตนเอง (`--no-emoji`, `--no-color`, `--plain`) เหมือนใน v1 อีกแล้ว โหมด CLI เป็นข้อความธรรมดาเสมอ (หรือ `--json`) ไม่ขึ้นกับเทอร์มินัล

## 10. การส่งออก

รายงานข้อความและ HTML เขียนด้วยภาษาที่เลือกในการตั้งค่า (“ภาษาของการส่งออก” ค่าเริ่มต้นคือภาษาของอินเทอร์เฟซ) ส่วน JSON ยังคงเป็นข้อมูลและไม่ถูกแปล รายงานถูกสร้างใน `var/exports/` เป็นค่าเริ่มต้น (เส้นทางขณะทำงาน ดู `ARCHITECTURE.md`) หรือที่เส้นทางที่ระบุ (`--output` ใน CLI กล่องโต้ตอบใน TUI)

### JSON แหล่งข้อมูลหลัก

โครงสร้างทั้งหมดของการสแกน (`ScanRun`) แปลงเป็น JSON ได้อย่างเคร่งครัด

### ข้อความ รายงานกะทัดรัดสำหรับอ่าน

อ่านได้นอกเทอร์มินัล ไม่มีรหัส ANSI มีโครงสร้างเป็นลำดับชั้น

### HTML รายงานเว็บที่อ่านง่าย

รายงานแบบสมบูรณ์ในตัวพร้อม CSS ฝังในหน้า เปิดดูได้ในทุกเบราว์เซอร์ แชร์และเก็บถาวรได้

## 11. ประวัติและการเปรียบเทียบ

ทุกการสแกนถูกบันทึกไว้ (SQLite, `var/db/app.db`): เปิดดูประวัติตามเป้าหมายได้ ดูรายละเอียดการรันที่ผ่านมา เปรียบเทียบการสแกนสองครั้ง (ข้อค้นพบที่ปรากฏใหม่ / แก้ไขแล้ว / ไม่เปลี่ยน / เปลี่ยนไป) และเรียกสแกนซ้ำกับเป้าหมายเดิมโดยไม่ต้องกรอกใหม่ — สิ่งเหล่านี้ไม่มีใน v1 แต่เพิ่มเข้ามาเมื่อย้ายไปใช้ Clean Architecture

## 12. การทดสอบ

```bash
source .venv/bin/activate
pytest tests/ -v
```

โครงสร้าง: `tests/unit/` (โดเมนและแอปพลิเคชัน ไม่มี I/O จริง), `tests/integration/` (SQLite/ไฟล์จริง เซิร์ฟเวอร์ HTTP จำลอง `pytest-httpserver`), `tests/e2e/` (CLI และ TUI ตั้งแต่ต้นจนจบ, `Textual.testing`)

## 13. นอกขอบเขต

- การสแกน CVE
- การตรวจหา SQLi, XSS, RCE เชิงรุก
- การยืนยันตัวตนที่ซับซ้อนฝั่งเครื่องมือสแกน
- การไล่เก็บหน้าเว็บเชิงลึก
- ฟัซซิง
- brute force เส้นทางจำนวนมาก
- การสแกนหลายเป้าหมายพร้อมกัน
- การทำงานคู่ขนานแบบรุนแรง
- แดชบอร์ดเว็บ

---

> Omega-scan — สังเกต เก็บข้อมูล ตีความ รายงาน  
> เครื่องมือสแกนสถานะความปลอดภัย ไม่ใช่เครื่องมือโจมตี
