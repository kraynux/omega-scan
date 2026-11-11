<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Lisensi MIT (lihat berkas LICENCE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan.png" alt="Omega-Scan" width="512">
</div>

# 🔍 OMEGA-SCAN

**Pemindai postur keamanan web**

> Dibuat oleh [kraynux](https://github.com/kraynux) untuk [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Halaman resmi: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Pratinjau: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Antarmuka dan laporan ekspor tersedia dalam **17 bahasa** — lihat [Bahasa antarmuka](#bahasa-antarmuka).  
**Bahasa:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** adalah alat TUI + CLI yang menganalisis kerapian konfigurasi yang terlihat dari luar pada layanan HTTP/HTTPS Anda. Alat ini mengamati, mengumpulkan fakta, menerapkan aturan interpretasi, dan menghasilkan laporan yang dapat ditindaklanjuti, tanpa pernah melakukan serangan aktif. Alat dari rangkaian `omega-`, disusun dengan Clean Architecture — lihat `ARCHITECTURE.md` untuk detail teknis lengkap.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-scan/D.png" width="24%" />
</p>

## 1. Visi dan cakupan

Omega-scan adalah pemindai postur keamanan web untuk administrasi sistem: memeriksa dengan cepat kerapian konfigurasi yang terlihat dari sebuah layanan HTTP/HTTPS di localhost, LAN, atau target eksternal, termasuk di balik terowongan seperti Tailscale Funnel.

### Yang dilakukan Omega-scan

- Mengumpulkan fakta yang dapat diamati: header, cookie, metode HTTP, TLS, jalur sensitif, header CORS.
- Menerapkan aturan interpretasi deklaratif pada fakta-fakta tersebut.
- Menghasilkan temuan yang seragam, beralasan, dan dapat ditindaklanjuti.
- Menampilkan hasil di TUI (Textual) atau CLI untuk skrip, serta melalui tiga ekspor: JSON, teks, HTML.
- Mendeteksi positif palsu, terutama perilaku catch-all dan jalur yang dilindungi autentikasi.
- Menyesuaikan diri dengan konteks: proxy, terowongan, multi-vhost, SNI.
- Mewajibkan konfirmasi otorisasi yang eksplisit sebelum memindai target mana pun yang belum disematkan sebagai terotorisasi.
- Menyimpan riwayat pemindaian permanen per target yang dapat diulang dan dibandingkan dari waktu ke waktu.

### Yang tidak dilakukan Omega-scan

- Pemindaian kerentanan aktif: tanpa SQLi, XSS, atau RCE.
- Pemindaian CVE.
- Alat brute force atau fuzzing massal.
- Crawler mendalam.
- Alat multi-target paralel yang agresif.
- Dasbor web.
- Autentikasi di sisi pemindai.

## 2. Instalasi

### Prasyarat

- Python 3.10+
- Koneksi Internet, untuk dependensi dan pemindaian eksternal

### Instalasi

Arsip resmi disediakan dalam format `.tar.gz`. Periksa integritasnya sebelum memasang:

```bash
sha256sum omega-scan.tar.gz
```

### Metode 1 — skrip instalasi

```bash
[ -d omega-scan ] && echo "ℹ️ Sudah diekstrak di sini, langkah dilewati." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan sudah ada, pemindahan dilewati." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Metode 2 — instalasi lengkap yang tangguh



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Membuat lingkungan virtual `.venv` jika belum ada.
2. Memasang dependensi (`pip install -e .`; `pyproject.toml` tetap menjadi satu-satunya sumber kebenaran).
3. Menjadikan `omega-scan.sh` dan `install.sh` dapat dieksekusi.
4. Menambahkan alias `scan` ke `~/.bashrc` dan `~/.zshrc` (tanpa duplikat jika sudah ada).

### Dependensi

Dideklarasikan di `pyproject.toml` (tidak ada lagi `requirements.txt`):
- `textual`: antarmuka TUI, tema, penyesuaian otomatis dengan terminal
- `httpx`: klien HTTP/HTTPS modern
- `jinja2`: templat untuk ekspor HTML
- Dependensi pengembangan (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Penggunaan

### Mode interaktif (TUI)

Disarankan untuk pemakaian sehari-hari — dijalankan tanpa argumen:

```bash
./omega-scan.sh
```

Alur: layar pembuka (tertutup dengan satu tombol atau klik) → menu utama → isian target dan pilihan profil (dengan konfirmasi otorisasi jika target belum disematkan) → pemindaian (indikator kemajuan dan detail operasi jaringan ditampilkan langsung) → hasil (nilai keseluruhan, temuan yang dapat difilter per kategori, detail saat mengeklik sebuah baris) → ekspor/riwayat/perbandingan dari menu utama. Penyesuaian dengan terminal (warna, ukuran, penyederhanaan struktur) berlangsung otomatis; opsi tampilan manual tidak diperlukan lagi.

#### Pintasan keyboard

| Tombol | Aksi |
|---|---|
| `↑` / `↓` | Berpindah antarelemen layar |
| `Tab` / `Shift+Tab` | Berpindah antarkolom formulir |
| `Esc` | Kembali ke layar sebelumnya (konfirmasi keluar di layar awal) |
| `t` | Tema berikutnya (langsung diterapkan, tanpa konfirmasi) |
| `r` | Menyegarkan deteksi terminal |
| `a` | Menampilkan bantuan |
| `q` | Keluar (dengan konfirmasi) |

### Bahasa antarmuka

Antarmuka tersedia dalam 17 bahasa: Prancis, Inggris, Spanyol, Portugis (Brasil), Italia, Jerman, Belanda, Polandia, Rusia, Tionghoa Sederhana, Vietnam, Thai, Indonesia, Jepang, Korea, Hindi, dan Arab. Pilihan dibuat di Pengaturan (“Langue / Language”) dan berlaku setelah antarmuka dimulai ulang; variabel `OMEGA_SCAN_LANG` (misalnya `OMEGA_SCAN_LANG=id ./omega-scan.sh`) memaksakan bahasa untuk satu sesi. Jika dijalankan dari omega-suite, omega-scan memakai bahasa rangkaian. Di konsol teks Linux (TTY), bahasa beraksara non-Latin ditampilkan dalam bahasa Inggris selama sesi itu. Baris perintah tetap berbahasa Prancis.

### Kontak dan dukungan

Bantuan (tombol `a`) menyediakan layar **Kontak dan dukungan**: *Traktir kopi* (halaman PayPal pengembang), *Hubungi dukungan* (alamat email dan formulir kontak situs, ditampilkan apa adanya), *Daftarkan saya sebagai pengguna (anonim)*, dan *Periksa pembaruan*. Pendaftaran bersifat sukarela, nonaktif secara bawaan, dan dikirim hanya sekali: hanya digunakan untuk menghitung pengguna dan, jika Anda mau, benua atau negara mereka (daftar tertutup, tidak pernah teks bebas). Yang dikirim adalah kunci yang diambil secara acak, nama perangkat lunak (`omega-scan`), dan versinya; tidak pernah nama, nama mesin, pengaturan, target, maupun hasil. Alamat IP tidak disimpan dalam pendaftaran, tetapi, seperti setiap kunjungan, melewati pemeriksaan keamanan dan log server penerima. Penarikan kapan saja dari layar yang sama (*Jangan daftarkan saya lagi*). Pemeriksaan pembaruan hanya membaca daftar versi yang dipublikasikan di situs, dan tidak pernah tanpa klik.

### Mode skrip (CLI)

Setiap subperintah mengaktifkan mode CLI (teks biasa, atau JSON dengan `--json`):

```bash
# Memindai target (--authorize wajib jika target belum disematkan)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Riwayat
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Ekspor
./omega-scan.sh export scan-30577411758e --format html --output laporan.html

# Target yang disematkan sebagai terotorisasi (pemindaian berikutnya tanpa --authorize)
./omega-scan.sh targets pin example.org --note "kesepakatan klien 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Penjaga otorisasi target

Tidak ada pemindaian yang dimulai tanpa konfirmasi otorisasi yang eksplisit untuk target (kotak centang di TUI, `--authorize` di CLI), kecuali target sudah disematkan. Pemeriksaan ini dilakukan di sisi aplikasi (`application/pipeline/guards/authorization_guard.py`), tidak hanya di antarmuka.

### Format target yang diterima

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 dengan port
::1                         IPv6
[2001:db8::10]:8443         IPv6 dalam kurung siku dengan port
example.org                 Nama host
intranet.lan:8080/admin     Nama host dengan port dan jalur
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Profil pemindaian

| Parameter | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Kegunaan | Pemeriksaan cepat | Lengkap (bawaan) | Mendalam | localhost / LAN |
| Batas waktu koneksi/baca | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Metode HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Penyelidikan jalur | Tidak | Ya (~20) | Ya (lengkap) | Ya (~20) |
| TLS | Tidak | Ya | Ya (terperinci) | Ya (toleran) |
| Probe CORS | Tidak | Ya | Ya | Ya |
| Catch-all | - | Ya | Ya | Ya |
| Kebijakan HSTS | Tidak dinilai | Standar | Ketat | Toleran |

### Kapan memakai profil yang mana

- `quick`: pemeriksaan kilat sebelum masuk produksi
- `standard`: audit lengkap layanan produksi, disarankan
- `extended`: audit mendalam termasuk metode HTTP berisiko
- `local-lab`: pemindaian localhost atau LAN tanpa terkena penalti dari aturan yang dirancang untuk layanan publik, terutama HSTS

## 5. Arsitektur

Omega-scan disusun dengan **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), selaras dengan templat rangkaian `omega-` (lihat `omega-stress`). Detail lengkap — pohon folder, aturan dependensi, rantai fungsional, hierarki pengecualian, taksonomi penamaan — ada di **`ARCHITECTURE.md`**, dokumen acuan normatif.

Gambaran singkat:

```text
src/omega_scan/
├── domain/          Logika bisnis murni (target, profil, pemindaian, pemeriksaan, laporan, tema...)
├── application/     Kasus penggunaan (commands/queries), pipeline eksekusi, penjaga
├── ports/           Kontrak yang diharapkan aplikasi (probe, repositori, pengekspor...)
├── infrastructure/  Implementasi konkret (httpx, SQLite; Textual TIDAK ada di sini)
├── interfaces/      tui/ (Textual) dan cli/ (untuk skrip), dengan kesetaraan fungsi yang ketat
├── app/             Perakitan (DependencyContainer, bootstrap, siklus hidup)
├── core/, shared/   Kosakata lintas bagian, utilitas nonbisnis
└── plugins/         Struktur sudah disiapkan, kosong (belum ada arah perluasan yang dipastikan)
```

Aturan desain yang tidak berubah sejak v1:
- `domain/checks/`: menilai berdasarkan bukti, tidak pernah mengakses jaringan.
- `infrastructure/network/`: mengakses jaringan, tidak pernah menilai.
- `interfaces/`: menampilkan, tidak berisi logika bisnis apa pun.
- `infrastructure/exporters/`: membaca hasil pemindaian, tidak menghitung ulang apa pun.

## 6. Taksonomi aturan

### Transportasi, `TRN-*`

- `TRN-HTTP-001`: HTTP dapat diakses tanpa pengalihan ke HTTPS, `WARN`
- `TRN-HTTPS-001`: HTTPS tidak dapat diakses, `FAIL`
- `TRN-HSTS-001`: header HSTS tidak ada, `FAIL`
- `TRN-HSTS-002`: `max-age` HSTS rendah, kurang dari 1 tahun, `WARN`

### Kedalaman TLS, `TLS-*`

- `TLS-VERSION-001`: protokol TLS usang (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: rangkaian sandi yang jelas lemah (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Header, `HDR-*`

- `HDR-CSP-001`: CSP tidak ada di halaman HTML, `FAIL`
- `HDR-CSP-002`: CSP terlalu longgar, `WARN`
- `HDR-NOSNIFF-001`: `X-Content-Type-Options` tidak ada, `WARN`
- `HDR-SERVER-001`: banner `Server` terekspos, `WARN`
- `HDR-CACHE-001`: `Cache-Control` tidak ada atau terlalu longgar di halaman HTML, `WARN`

### Cookie, `COO-*`

- `COO-SECURE-001`: cookie pada respons HTTPS tanpa atribut `Secure`, `WARN`
- `COO-HTTPONLY-001`: cookie tanpa atribut `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: `SameSite` tidak ada, atau `None` tanpa `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` dikombinasikan dengan `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: origin sembarang dipantulkan apa adanya di `Access-Control-Allow-Origin`, `WARN`

### Metode HTTP, `MTH-*`

- `MTH-OPTIONS-001`: metode OPTIONS aktif, `INFO`
- `MTH-TRACE-001`: metode TRACE aktif, `WARN`
- `MTH-PUT-001`: metode PUT aktif, `WARN`
- `MTH-DELETE-001`: metode DELETE aktif, `WARN`
- `MTH-PATCH-001`: metode PATCH aktif, `WARN`
- `MTH-CONNECT-001`: metode CONNECT aktif, `WARN`

### Paparan, `EXR-*`

- `EXR-ADMIN-001`: jalur admin dapat diakses tanpa autentikasi, `WARN`
- `EXR-SENSITIVE-001`: berkas sensitif dapat diakses, `.env`, `.git`, `FAIL`

### Kebocoran informasi, `INF-*`

- `INF-BANNER-001`: banner server terekspos, `WARN`
- `INF-ERROR-001`: pesan galat terperinci, `WARN`
- `INF-STACK-001`: stack trace terekspos, `FAIL`
- `INF-ROBOTS-001`: berkas `robots.txt` ada, `OK` sebagai informasi
- `INF-HEADER-001`: header teknis yang terlalu banyak membocorkan informasi, `WARN`
- `INF-SECURITYTXT-001`: berkas `/.well-known/security.txt` ada, `OK` sebagai informasi

## 7. Kebijakan keyakinan

| Tingkat | Definisi |
|---|---|
| `certain` | Bukti langsung yang tidak ambigu, dibaca apa adanya dari respons: header ada atau tidak, kode HTTP mentah. |
| `high` | Bukti jelas tetapi konteksnya tidak langsung: metode melalui OPTIONS, cookie yang teramati. |
| `medium` | Temuan yang mungkin dipengaruhi perantara: proxy, WAF, terowongan. |
| `low` | Deteksi tidak langsung, konten ambigu, atau situasi `catch_all_suspected`. |

### Penurunan otomatis

- `catch_all_suspected = true`: keyakinan dibatasi pada `low`
- `proxy_suspected = true`: keyakinan dibatasi pada `medium`
- `observed_access_state = ambiguous`: keyakinan dibatasi pada `low`

## 8. Deteksi positif palsu

### Perilaku catch-all

Sebelum menguji jalur sensitif, Omega-scan membuat jalur acak yang tidak mungkin ada. Jika server menjawab `200 OK` untuk jalur itu, target ditandai `catch_all_suspected = true` dan semua temuan paparan diturunkan ke `confidence = low`.

### Autentikasi atau ketiadaan

Jalur yang dilindungi — `401`, `403`, atau pengalihan ke halaman masuk — tidak ditandai tidak ada maupun terekspos. Jalur itu ditandai `N/A` dengan catatan: “jalur dilindungi, keberadaannya tidak dapat dipastikan tanpa autentikasi”.

### Proxy / terowongan

Jika header `X-Forwarded-*`, `Via`, atau `Forwarded` terdeteksi, `proxy_suspected` menjadi `true` dan keyakinan temuan terkait — banner, TLS — dibatasi pada `medium`.

## 9. Kompatibilitas terminal

TUI (Textual) otomatis mendeteksi kemampuan terminal (warna, ukuran) dan menyesuaikan lembar gaya strukturalnya (`complete`/`standard`/`reduced`/`mono`) — tidak ada lagi opsi manual (`--no-emoji`, `--no-color`, `--plain`) seperti di v1. Mode CLI selalu berupa teks biasa (atau `--json`), tidak bergantung pada terminal.

## 10. Ekspor

Laporan teks dan HTML ditulis dalam bahasa yang dipilih di Pengaturan (“Bahasa ekspor”, bawaannya sama dengan antarmuka); JSON tetap berupa data dan tidak diterjemahkan. Laporan dibuat di `var/exports/` secara bawaan (jalur runtime, lihat `ARCHITECTURE.md`), atau di jalur yang ditentukan (`--output` di CLI, kotak dialog di TUI).

### JSON, sumber kebenaran

Struktur lengkap pemindaian (`ScanRun`), sepenuhnya dapat diserialisasi ke JSON.

### Teks, laporan ringkas yang mudah dibaca

Dapat dibaca di luar terminal, tanpa kode ANSI, dengan struktur bertingkat.

### HTML, laporan web yang mudah dibaca

Laporan mandiri dengan CSS sebaris, dapat dibuka di peramban mana pun, mudah dibagikan dan diarsipkan.

## 11. Riwayat dan perbandingan

Setiap pemindaian disimpan (SQLite, `var/db/app.db`): riwayat dapat dilihat per target, detail eksekusi sebelumnya, perbandingan dua pemindaian (temuan muncul / teratasi / tidak berubah / berubah), dan pengulangan pemindaian pada target yang sama tanpa mengetik ulang — tidak ada di v1, ditambahkan saat migrasi ke Clean Architecture.

## 12. Pengujian

```bash
source .venv/bin/activate
pytest tests/ -v
```

Struktur: `tests/unit/` (domain dan aplikasi, tanpa I/O sungguhan), `tests/integration/` (SQLite/berkas sungguhan, server HTTP tiruan `pytest-httpserver`), `tests/e2e/` (CLI dan TUI dari awal sampai akhir, `Textual.testing`).

## 13. Di luar cakupan

- Pemindaian CVE
- Deteksi aktif SQLi, XSS, RCE
- Autentikasi kompleks di sisi pemindai
- Crawling mendalam
- Fuzzing
- Brute force jalur secara massal
- Pemindaian banyak target secara bersamaan
- Paralelisme agresif
- Dasbor web

---

> Omega-scan — Mengamati, mengumpulkan, menafsirkan, melaporkan.  
> Pemindai postur, bukan alat serang.
