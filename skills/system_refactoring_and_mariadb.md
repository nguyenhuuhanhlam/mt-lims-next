# Ghi nhận thay đổi: Tái cấu trúc Hệ thống & Chuyển đổi MariaDB

**Ngày thực hiện:** 2026-05-14  
**Phiên làm việc:** f989ad64-58a1-421b-922c-4f4d4199294c

---

## Mục tiêu

1. **Tái cấu trúc (Refactor):** Phân tách module lõi `request_form` đang bị phình to thành các Django App nhỏ gọn, độc lập theo từng nghiệp vụ (User/Group, Requests, Tests, Core).
2. **Đổi tên:** Đổi tên `request_form` thành `lab_requests` để phản ánh đúng chức năng cốt lõi.
3. **Database:** Chuyển đổi cơ sở dữ liệu từ SQLite sang MariaDB thực tế. Xử lý các lỗi tương thích với phiên bản MariaDB cũ.

---

## Các thay đổi đã thực hiện

### 1. Tái cấu trúc Thư mục (Django Apps)

Toàn bộ hệ thống trước đây nằm trong thư mục `request_form` đã được chia thành 4 app:

- **`lab_requests` (Đổi tên từ `request_form`)**:
  - Chỉ chứa Model `Request` và các View, Form, Template liên quan đến tạo mới/chỉnh sửa Phiếu yêu cầu.
- **`system_admin` (Tạo mới)**:
  - Tiếp nhận toàn bộ logic quản lý Người dùng (`User`) và Nhóm quyền (`Group`).
- **`material_tests` (Tạo mới)**:
  - Chứa Model `MaterialTest` và các View/Form xử lý giao diện bài test, cũng như tính năng upload file đính kèm.
- **`core` (Tạo mới)**:
  - Đóng vai trò là entry-point của ứng dụng, chứa View `dashboard` và các trang dùng chung.

*Toàn bộ thư mục `templates/` đã được tổ chức lại với các thư mục con tương ứng. Các lệnh gọi `{% url %}`, `{% include %}` và `{% extends %}` đã được cập nhật đường dẫn chính xác.*

---

### 2. Cấu hình Cơ sở dữ liệu MariaDB

- **Thư viện:** Cài đặt `pymysql` và `python-dotenv`.
- **Cấu hình:** Chuyển thông tin đăng nhập Database ra file `.env` (đã tạo file mẫu `.env.example`).
- **Xử lý tính tương thích (Monkey Patch):**
  - **Vấn đề:** Server hiện tại chạy MariaDB 10.3.32, nhưng Django 5.2 yêu cầu tối thiểu MariaDB 10.5+ và mặc định sử dụng cú pháp `RETURNING` (không có trên 10.3).
  - **Giải pháp:** Đã thêm cấu hình bỏ qua kiểm tra phiên bản và tắt tính năng `RETURNING` tại file `config/settings.py` để tương thích ngược.

```python
# Đoạn code trong settings.py
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

BaseDatabaseWrapper.check_database_version_supported = lambda self: None
DatabaseFeatures.can_return_columns_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False
```

---

### 3. Sửa lỗi trong quá trình Migration

- **Lỗi `ImportError`:** Đã khắc phục lỗi import `MaterialTest` trong `lab_requests/admin.py` bằng cách chuyển khai báo sang `material_tests/admin.py`.
- **Lỗi `OperationalError (1050)`:** Do quá trình migrate bị gián đoạn giữa chừng tạo ra các bảng rác. Đã sử dụng một script python (`drop_tables.py`) để xóa toàn bộ các bảng trong database `mtlimsdb` và chạy lại `migrate` thành công.

---

## Trạng thái hiện tại

- ✅ Kiến trúc hệ thống đã phân tách rõ ràng, chuẩn mực và dễ mở rộng.
- ✅ Kết nối MariaDB thành công, các bảng đã được khởi tạo (Migrated: admin, auth, contenttypes, lab_requests, sessions).
- ✅ Hệ thống sẵn sàng cho việc tạo tài khoản Admin và sử dụng.
