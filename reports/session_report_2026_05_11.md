# Báo cáo Phiên làm việc - 11/05/2026

## Mục tiêu chính
- Khắc phục lỗi Serialization JSON giữa Backend (Django) và Frontend (Alpine.js).
- Đảm bảo dữ liệu Người tham gia (Participants), Dự án (Project) và Đơn vị (Unit) được lưu trữ chính xác.
- Hiện đại hóa hệ thống tìm kiếm/lọc bằng công nghệ HTMX.

## Các công việc đã thực hiện

### 1. Khắc phục lỗi JSON & Đồng bộ dữ liệu
- **Vấn đề:** Lỗi `SyntaxError` khi parse JSON do Django/SQLite đôi khi lưu trữ dữ liệu dưới dạng chuỗi đã được encode (double-encoding).
- **Giải pháp:**
    - Triển khai cơ chế **Robust Parsing** trong JavaScript: Tự động phát hiện và parse lại nếu dữ liệu là chuỗi JSON lồng nhau.
    - Thêm các `@property` (`participants_json`, `project_json`, `unit_json`) vào model `Request` để đảm bảo dữ liệu gửi ra template luôn là JSON chuẩn.
    - Tích hợp Alpine.js trực tiếp vào `forms.py` thông qua thuộc tính `:value` và `x-model`, giúp đồng bộ hóa tức thì giữa UI và các hidden fields của Django Form.

### 2. Tích hợp HTMX (Hiện đại hóa UI)
- **Công nghệ:** Đưa HTMX vào hệ thống để thay thế logic lọc dữ liệu bằng JavaScript thuần.
- **Thay đổi chính:**
    - Thêm thư viện HTMX vào `base.html`.
    - Tách logic hiển thị danh sách yêu cầu ra thành partial template: `request_table_rows.html`.
    - Cập nhật View `request_list`: Sử dụng header `HX-Request` để trả về kết quả lọc dưới dạng HTML fragment thay vì tải lại toàn bộ trang.
    - Cập nhật `request_list.html`: Sử dụng `hx-get`, `hx-trigger`, `hx-target` để thực hiện tìm kiếm Real-time và lọc theo loại phiếu.
- **Kết quả:** Code JavaScript giảm đáng kể, logic lọc dữ liệu được đẩy về Server (Database) giúp hệ thống chịu tải tốt hơn khi dữ liệu lớn.

### 3. Cấu trúc lại Template
- Tối ưu hóa `request_create.html` bằng cách sử dụng một scope Alpine.js duy nhất cho toàn bộ form.
- Sử dụng `json_script` của Django để truyền dữ liệu khởi tạo an toàn, tránh lỗi XSS và lỗi ký tự đặc biệt.

## Trạng thái hiện tại
- **Giao diện:** Mượt mà, tìm kiếm và lọc không cần load trang.
- **Dữ liệu:** Lưu trữ ổn định cho các trường JSON phức tạp.
- **Công nghệ:** Stack hiện tại là **Django + Tailwind + Alpine.js + HTMX** (TALL stack cho Django).

---
*Người thực hiện: Antigravity AI*
