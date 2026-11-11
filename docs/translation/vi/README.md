<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Giấy phép MIT (xem tệp LICENCE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan.png" alt="Omega-Scan" width="512">
</div>

# 🔍 OMEGA-SCAN

**Công cụ quét tình trạng bảo mật web**

> Được [kraynux](https://github.com/kraynux) xây dựng cho [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Trang chính thức: [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Ảnh chụp màn hình: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Giao diện và báo cáo xuất có sẵn bằng **17 ngôn ngữ** — xem [Ngôn ngữ giao diện](#ngôn-ngữ-giao-diện).  
**Ngôn ngữ:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-scan** là công cụ TUI + CLI phân tích mức độ chuẩn mực trong cấu hình hiển thị ra bên ngoài của các dịch vụ HTTP/HTTPS của bạn. Nó quan sát, thu thập dữ kiện, áp dụng các quy tắc diễn giải và tạo ra báo cáo có thể dùng để hành động, không bao giờ thực hiện tấn công chủ động. Đây là một công cụ của bộ `omega-`, được tổ chức theo Clean Architecture — xem `ARCHITECTURE.md` để biết đầy đủ chi tiết kỹ thuật.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-scan/D.png" width="24%" />
</p>

## 1. Tầm nhìn và phạm vi

Omega-scan là công cụ quét tình trạng bảo mật web dành cho quản trị hệ thống: kiểm tra nhanh mức độ chuẩn mực trong cấu hình hiển thị của một dịch vụ HTTP/HTTPS trên localhost, mạng LAN hoặc một mục tiêu bên ngoài, kể cả khi nằm sau đường hầm như Tailscale Funnel.

### Omega-scan làm gì

- Thu thập các dữ kiện quan sát được: tiêu đề, cookie, phương thức HTTP, TLS, đường dẫn nhạy cảm, tiêu đề CORS.
- Áp dụng các quy tắc diễn giải dạng khai báo lên những dữ kiện đó.
- Tạo ra các phát hiện thống nhất, có căn cứ và có thể dùng để hành động.
- Hiển thị kết quả trong TUI (Textual) hoặc CLI có thể viết script, và qua ba kiểu xuất: JSON, văn bản, HTML.
- Phát hiện cảnh báo nhầm, đặc biệt là hành vi catch-all và các đường dẫn được bảo vệ bằng xác thực.
- Thích ứng với ngữ cảnh: proxy, đường hầm, nhiều vhost, SNI.
- Yêu cầu xác nhận cấp phép rõ ràng trước khi quét bất kỳ mục tiêu nào chưa được ghim là đã cấp phép.
- Lưu lịch sử quét lâu dài theo từng mục tiêu, có thể chạy lại và so sánh theo thời gian.

### Omega-scan không làm gì

- Quét lỗ hổng chủ động: không SQLi, XSS hay RCE.
- Quét CVE.
- Công cụ dò mật khẩu hay fuzzing quy mô lớn.
- Trình thu thập (crawler) chuyên sâu.
- Công cụ quét song song nhiều mục tiêu một cách hung hãn.
- Bảng điều khiển web.
- Xác thực phía công cụ quét.

## 2. Cài đặt

### Yêu cầu

- Python 3.10+
- Kết nối Internet, để cài các phụ thuộc và quét các mục tiêu bên ngoài

### Cài đặt

Bản lưu trữ chính thức được cung cấp ở định dạng `.tar.gz`. Hãy kiểm tra tính toàn vẹn trước khi cài đặt:

```bash
sha256sum omega-scan.tar.gz
```

### Cách 1 — script cài đặt

```bash
[ -d omega-scan ] && echo "ℹ️ Đã giải nén ở đây, bỏ qua bước này." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan đã tồn tại, bỏ qua việc di chuyển." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Cách 2 — cài đặt đầy đủ, bền vững



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh`:

1. Tạo môi trường ảo `.venv` nếu chưa có.
2. Cài các phụ thuộc (`pip install -e .`; `pyproject.toml` vẫn là nguồn chuẩn duy nhất).
3. Cấp quyền thực thi cho `omega-scan.sh` và `install.sh`.
4. Thêm bí danh `scan` vào `~/.bashrc` và `~/.zshrc` (không trùng lặp nếu đã có).

### Phụ thuộc

Khai báo trong `pyproject.toml` (không còn `requirements.txt`):
- `textual`: giao diện TUI, giao diện màu, tự động thích ứng với terminal
- `httpx`: trình khách HTTP/HTTPS hiện đại
- `jinja2`: mẫu cho bản xuất HTML
- Phụ thuộc phát triển (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Sử dụng

### Chế độ tương tác (TUI)

Khuyên dùng hằng ngày — chạy không có đối số:

```bash
./omega-scan.sh
```

Trình tự: màn hình khởi động (đóng bằng một phím hoặc một cú nhấp) → menu chính → nhập mục tiêu và chọn cấu hình (có xác nhận cấp phép nếu mục tiêu chưa được ghim) → quét (thanh tiến trình và chi tiết thao tác mạng hiển thị trực tiếp) → kết quả (điểm tổng thể, các phát hiện lọc được theo nhóm, chi tiết khi nhấp vào một dòng) → xuất/lịch sử/so sánh từ menu chính. Việc thích ứng với terminal (màu, kích thước, giản lược cấu trúc) là tự động; không cần tùy chọn hiển thị thủ công nữa.

#### Phím tắt

| Phím | Thao tác |
|---|---|
| `↑` / `↓` | Di chuyển giữa các mục trên màn hình |
| `Tab` / `Shift+Tab` | Di chuyển giữa các trường của biểu mẫu |
| `Esc` | Quay lại màn hình trước (xác nhận thoát ở màn hình chính) |
| `t` | Giao diện màu tiếp theo (áp dụng ngay, không cần xác nhận) |
| `r` | Làm mới việc nhận diện terminal |
| `a` | Hiện trợ giúp |
| `q` | Thoát (có xác nhận) |

### Ngôn ngữ giao diện

Giao diện có sẵn bằng 17 ngôn ngữ: tiếng Pháp, tiếng Anh, tiếng Tây Ban Nha, tiếng Bồ Đào Nha (Brasil), tiếng Ý, tiếng Đức, tiếng Hà Lan, tiếng Ba Lan, tiếng Nga, tiếng Trung giản thể, tiếng Việt, tiếng Thái, tiếng Indonesia, tiếng Nhật, tiếng Hàn, tiếng Hindi và tiếng Ả Rập. Ngôn ngữ được chọn trong Thiết lập (“Langue / Language”) và có hiệu lực sau khi khởi động lại giao diện; biến `OMEGA_SCAN_LANG` (ví dụ `OMEGA_SCAN_LANG=vi ./omega-scan.sh`) buộc dùng một ngôn ngữ trong một phiên. Khi được chạy từ omega-suite, omega-scan dùng ngôn ngữ của bộ công cụ. Trên console văn bản Linux (TTY), giao diện hiển thị bằng tiếng Anh trong phiên đó đối với tiếng Việt và các ngôn ngữ không dùng chữ Latinh. Dòng lệnh vẫn bằng tiếng Pháp.

### Liên hệ và hỗ trợ

Phần trợ giúp (phím `a`) có màn hình **Liên hệ và hỗ trợ**: *Mời một ly cà phê* (trang PayPal của nhà phát triển), *Liên hệ hỗ trợ* (địa chỉ email và biểu mẫu liên hệ của trang web, hiển thị rõ ràng), *Khai báo là người dùng (ẩn danh)* và *Kiểm tra cập nhật*. Việc khai báo là tự nguyện, tắt theo mặc định và chỉ gửi một lần: nó chỉ dùng để đếm số người dùng và, nếu bạn muốn, châu lục hoặc quốc gia của họ (danh sách đóng, không bao giờ là văn bản tự do). Nó gửi một khóa được tạo ngẫu nhiên, tên phần mềm (`omega-scan`) và phiên bản của nó; không bao giờ gửi tên, tên máy, thiết lập, mục tiêu hay kết quả. Địa chỉ IP không được lưu trong các khai báo, nhưng, như mọi lượt truy cập, nó đi qua các kiểm tra bảo mật và nhật ký của máy chủ nhận. Có thể rút lại bất cứ lúc nào từ cùng màn hình (*Không khai báo tôi nữa*). Việc kiểm tra cập nhật chỉ đọc danh sách các phiên bản đã phát hành trên trang web, và không bao giờ khi chưa nhấp.

### Chế độ script (CLI)

Bất kỳ lệnh con nào cũng kích hoạt chế độ CLI (văn bản thuần, hoặc JSON với `--json`):

```bash
# Quét một mục tiêu (bắt buộc --authorize nếu mục tiêu chưa được ghim)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Lịch sử
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Xuất
./omega-scan.sh export scan-30577411758e --format html --output baocao.html

# Mục tiêu đã ghim là được cấp phép (các lần quét sau không cần --authorize)
./omega-scan.sh targets pin example.org --note "thỏa thuận với khách hàng 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Chốt kiểm tra cấp phép mục tiêu

Không lần quét nào bắt đầu nếu chưa có xác nhận cấp phép rõ ràng cho mục tiêu (ô đánh dấu trong TUI, `--authorize` trong CLI), trừ khi mục tiêu đã được ghim. Việc kiểm tra diễn ra ở phía ứng dụng (`application/pipeline/guards/authorization_guard.py`), không chỉ ở giao diện.

### Định dạng mục tiêu được chấp nhận

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 có cổng
::1                         IPv6
[2001:db8::10]:8443         IPv6 trong ngoặc vuông, có cổng
example.org                 Tên máy chủ
intranet.lan:8080/admin     Tên máy chủ có cổng và đường dẫn
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Cấu hình quét

| Tham số | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Mục đích | Kiểm tra nhanh | Đầy đủ (mặc định) | Chuyên sâu | localhost / LAN |
| Thời gian chờ kết nối/đọc | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Phương thức HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Dò đường dẫn | Không | Có (~20) | Có (đầy đủ) | Có (~20) |
| TLS | Không | Có | Có (chi tiết) | Có (nới lỏng) |
| Thăm dò CORS | Không | Có | Có | Có |
| Catch-all | - | Có | Có | Có |
| Chính sách HSTS | Không đánh giá | Tiêu chuẩn | Nghiêm ngặt | Nới lỏng |

### Khi nào dùng cấu hình nào

- `quick`: kiểm tra chớp nhoáng trước khi đưa vào vận hành
- `standard`: kiểm định đầy đủ một dịch vụ đang vận hành, khuyên dùng
- `extended`: kiểm định chuyên sâu, bao gồm các phương thức HTTP rủi ro
- `local-lab`: quét localhost hoặc mạng LAN mà không bị trừ điểm vì các quy tắc dành cho dịch vụ công khai, nhất là HSTS

## 5. Kiến trúc

Omega-scan được tổ chức theo **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), thống nhất với mẫu của bộ `omega-` (xem `omega-stress`). Chi tiết đầy đủ — cây thư mục, quy tắc phụ thuộc, chuỗi chức năng, phân cấp ngoại lệ, quy ước đặt tên — nằm trong **`ARCHITECTURE.md`**, tài liệu tham chiếu mang tính quy chuẩn.

Tổng quan rất ngắn:

```text
src/omega_scan/
├── domain/          Logic nghiệp vụ thuần (mục tiêu, cấu hình, lần quét, kiểm tra, báo cáo, giao diện màu...)
├── application/     Ca sử dụng (commands/queries), pipeline thực thi, các chốt kiểm tra
├── ports/           Hợp đồng mà ứng dụng cần (bộ thăm dò, kho lưu trữ, bộ xuất...)
├── infrastructure/  Triển khai cụ thể (httpx, SQLite; Textual KHÔNG nằm ở đây)
├── interfaces/      tui/ (Textual) và cli/ (viết script được), tương đương chức năng nghiêm ngặt
├── app/             Lắp ráp (DependencyContainer, bootstrap, vòng đời)
├── core/, shared/   Từ vựng dùng chung, tiện ích không thuộc nghiệp vụ
└── plugins/         Đã có cấu trúc, đang trống (chưa có hướng mở rộng nào được xác nhận)
```

Các quy tắc thiết kế không đổi kể từ v1:
- `domain/checks/`: đánh giá dựa trên bằng chứng, không bao giờ truy cập mạng.
- `infrastructure/network/`: truy cập mạng, không bao giờ đánh giá.
- `interfaces/`: hiển thị, không chứa logic nghiệp vụ nào.
- `infrastructure/exporters/`: đọc kết quả quét, không tính lại gì cả.

## 6. Hệ thống quy tắc

### Truyền tải, `TRN-*`

- `TRN-HTTP-001`: HTTP truy cập được mà không chuyển hướng sang HTTPS, `WARN`
- `TRN-HTTPS-001`: không truy cập được HTTPS, `FAIL`
- `TRN-HSTS-001`: thiếu tiêu đề HSTS, `FAIL`
- `TRN-HSTS-002`: `max-age` của HSTS thấp, dưới 1 năm, `WARN`

### Chiều sâu TLS, `TLS-*`

- `TLS-VERSION-001`: giao thức TLS lỗi thời (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001`: bộ mã hóa rõ ràng là yếu (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Tiêu đề, `HDR-*`

- `HDR-CSP-001`: thiếu CSP trên trang HTML, `FAIL`
- `HDR-CSP-002`: CSP quá lỏng lẻo, `WARN`
- `HDR-NOSNIFF-001`: thiếu `X-Content-Type-Options`, `WARN`
- `HDR-SERVER-001`: lộ banner `Server`, `WARN`
- `HDR-CACHE-001`: thiếu `Cache-Control` hoặc quá lỏng lẻo trên trang HTML, `WARN`

### Cookie, `COO-*`

- `COO-SECURE-001`: cookie trong phản hồi HTTPS không có thuộc tính `Secure`, `WARN`
- `COO-HTTPONLY-001`: cookie không có thuộc tính `HttpOnly`, `WARN`
- `COO-SAMESITE-001`: thiếu `SameSite`, hoặc `None` mà không có `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001`: `Access-Control-Allow-Origin: *` đi cùng `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001`: origin tùy ý bị phản chiếu nguyên vẹn trong `Access-Control-Allow-Origin`, `WARN`

### Phương thức HTTP, `MTH-*`

- `MTH-OPTIONS-001`: phương thức OPTIONS được bật, `INFO`
- `MTH-TRACE-001`: phương thức TRACE được bật, `WARN`
- `MTH-PUT-001`: phương thức PUT được bật, `WARN`
- `MTH-DELETE-001`: phương thức DELETE được bật, `WARN`
- `MTH-PATCH-001`: phương thức PATCH được bật, `WARN`
- `MTH-CONNECT-001`: phương thức CONNECT được bật, `WARN`

### Phơi lộ, `EXR-*`

- `EXR-ADMIN-001`: đường dẫn quản trị truy cập được mà không cần xác thực, `WARN`
- `EXR-SENSITIVE-001`: tệp nhạy cảm truy cập được, `.env`, `.git`, `FAIL`

### Rò rỉ thông tin, `INF-*`

- `INF-BANNER-001`: lộ banner máy chủ, `WARN`
- `INF-ERROR-001`: thông báo lỗi chi tiết, `WARN`
- `INF-STACK-001`: lộ stack trace, `FAIL`
- `INF-ROBOTS-001`: có tệp `robots.txt`, `OK` để tham khảo
- `INF-HEADER-001`: tiêu đề kỹ thuật tiết lộ quá nhiều, `WARN`
- `INF-SECURITYTXT-001`: có tệp `/.well-known/security.txt`, `OK` để tham khảo

## 7. Chính sách tin cậy

| Mức | Định nghĩa |
|---|---|
| `certain` | Bằng chứng trực tiếp, không mơ hồ, đọc nguyên văn từ phản hồi: tiêu đề có hay không, mã HTTP thô. |
| `high` | Bằng chứng rõ ràng nhưng ngữ cảnh gián tiếp: phương thức qua OPTIONS, cookie quan sát được. |
| `medium` | Kết luận có thể bị một bên trung gian ảnh hưởng: proxy, WAF, đường hầm. |
| `low` | Phát hiện gián tiếp, nội dung mơ hồ, hoặc tình huống `catch_all_suspected`. |

### Tự động hạ mức

- `catch_all_suspected = true`: độ tin cậy tối đa là `low`
- `proxy_suspected = true`: độ tin cậy tối đa là `medium`
- `observed_access_state = ambiguous`: độ tin cậy tối đa là `low`

## 8. Phát hiện cảnh báo nhầm

### Hành vi catch-all

Trước khi thử các đường dẫn nhạy cảm, Omega-scan tạo một đường dẫn ngẫu nhiên khó có thật. Nếu máy chủ trả về `200 OK` cho đường dẫn đó, mục tiêu được đánh dấu `catch_all_suspected = true` và mọi phát hiện về phơi lộ đều bị hạ xuống `confidence = low`.

### Xác thực hay không tồn tại

Một đường dẫn được bảo vệ — `401`, `403` hoặc chuyển hướng tới trang đăng nhập — không bị đánh dấu là không tồn tại, cũng không bị đánh dấu là bị phơi lộ. Nó được đánh dấu `N/A` kèm ghi chú: “đường dẫn được bảo vệ, không thể xác nhận sự tồn tại khi chưa xác thực”.

### Proxy / đường hầm

Nếu phát hiện các tiêu đề `X-Forwarded-*`, `Via` hoặc `Forwarded`, `proxy_suspected` chuyển thành `true` và độ tin cậy của các phát hiện liên quan — banner, TLS — bị giới hạn ở `medium`.

## 9. Tương thích terminal

TUI (Textual) tự động nhận diện khả năng của terminal (màu, kích thước) và điều chỉnh bảng kiểu cấu trúc tương ứng (`complete`/`standard`/`reduced`/`mono`) — không còn tùy chọn thủ công (`--no-emoji`, `--no-color`, `--plain`) như ở v1. Chế độ CLI luôn là văn bản thuần (hoặc `--json`), không phụ thuộc terminal.

## 10. Xuất

Báo cáo văn bản và HTML được viết bằng ngôn ngữ chọn trong Thiết lập (“Ngôn ngữ bản xuất”, mặc định là ngôn ngữ giao diện); JSON vẫn là dữ liệu, không được dịch. Báo cáo được tạo mặc định trong `var/exports/` (đường dẫn khi chạy, xem `ARCHITECTURE.md`), hoặc tại đường dẫn được chỉ định (`--output` trong CLI, hộp thoại trong TUI).

### JSON, nguồn chuẩn

Toàn bộ cấu trúc của lần quét (`ScanRun`), tuần tự hóa JSON nghiêm ngặt.

### Văn bản, báo cáo dễ đọc gọn nhẹ

Đọc được ngoài terminal, không có mã ANSI, có cấu trúc phân cấp.

### HTML, báo cáo web dễ đọc

Báo cáo độc lập với CSS nhúng sẵn, xem được trên mọi trình duyệt, dễ chia sẻ và lưu trữ.

## 11. Lịch sử và so sánh

Mỗi lần quét đều được lưu (SQLite, `var/db/app.db`): xem lịch sử theo mục tiêu, chi tiết một lần chạy trước, so sánh hai lần quét (phát hiện mới xuất hiện / đã khắc phục / không đổi / đã thay đổi), và chạy lại một lần quét trên cùng mục tiêu mà không cần nhập lại — v1 không có, được bổ sung khi chuyển sang Clean Architecture.

## 12. Kiểm thử

```bash
source .venv/bin/activate
pytest tests/ -v
```

Cấu trúc: `tests/unit/` (domain và ứng dụng, không có I/O thật), `tests/integration/` (SQLite/tệp thật, máy chủ HTTP giả `pytest-httpserver`), `tests/e2e/` (CLI và TUI từ đầu đến cuối, `Textual.testing`).

## 13. Ngoài phạm vi

- Quét CVE
- Phát hiện chủ động SQLi, XSS, RCE
- Xác thực phức tạp phía công cụ quét
- Thu thập trang chuyên sâu
- Fuzzing
- Dò đường dẫn hàng loạt
- Quét đồng thời nhiều mục tiêu
- Song song hóa hung hãn
- Bảng điều khiển web

---

> Omega-scan — Quan sát, thu thập, diễn giải, báo cáo.  
> Một công cụ quét tình trạng bảo mật, không phải công cụ tấn công.
