# Ghi nhận thay đổi: Bổ sung Vai trò & Trạng thái cho Bài Thí Nghiệm (Material Test)

**Ngày thực hiện:** 2026-05-18
**Phiên làm việc:** f7eca154-0d4c-4fa5-b695-3e38ca0d6154

---

## Mục tiêu

Cải thiện hệ thống quản lý Bài Thí Nghiệm (Material Test) bằng cách:
1. Bổ sung **Người thực hiện** (thuộc nhóm `Technicians`) chịu trách nhiệm làm thí nghiệm.
2. Bổ sung **Người kiểm tra** (thuộc nhóm `Managers`) chịu trách nhiệm duyệt kết quả.
3. Bổ sung trường **Trạng thái** (Status) với hai giá trị: `Đang thực hiện` và `Hoàn tất`.
4. Áp dụng cơ chế kiểm soát: Chỉ có tài khoản được phân công làm **Người kiểm tra** mới có quyền chuyển trạng thái bài test sang `Hoàn tất`.

---

## Các thay đổi đã thực hiện

### 1. `material_tests/models.py` — Mở rộng Model
- Bổ sung trường `status` (CharField) với lựa chọn `in_progress` (Đang thực hiện) và `completed` (Hoàn tất).
- Bổ sung 2 trường `ForeignKey` liên kết với `User`:
  - `tester`: Giới hạn `limit_choices_to={'groups__name': 'Technicians'}`.
  - `reviewer`: Giới hạn `limit_choices_to={'groups__name': 'Managers'}`.
- Sửa lại thuộc tính `@property def is_completed` để trả về `self.status == 'completed'` (thay cho logic tự động dựa trên việc upload đủ 2 file).

### 2. `material_tests/forms.py` — Form và Phân quyền
- Bổ sung 3 trường mới vào `MaterialTestForm`.
- Cấu hình widget class Tailwind đồng bộ cho 3 trường này (`forms.Select`).
- **Logic kiểm tra quyền:** Trong hàm `__init__`, form giờ đây nhận thêm tham số `user` từ View. Trong hàm `clean()`, nếu `status` được chuyển sang `completed`, hệ thống sẽ kiểm tra xem `request.user` có trùng khớp với `reviewer` đã chọn hay không. Nếu không, trả về lỗi `ValidationError` ngay trên field `status`.

### 3. `material_tests/views.py` — Cập nhật View
- Sửa đổi toàn bộ các hàm gọi `MaterialTestForm` (như `test_create`, `test_edit`, `test_row_edit`...) để tự động truyền `user=request.user` vào Form.
- Tối ưu hóa việc lọc dữ liệu trên danh sách bằng QuerySet:
  - Cũ: `[t for t in tests if t.is_completed]`
  - Mới: `tests.filter(status='completed')`

### 4. Giao diện (Templates)
- **Danh sách test (`material_test_row.html`)**:
  - Đổi màu và text huy hiệu từ "Chờ file" sang "Đang thực hiện". Huy hiệu "Hoàn tất" dựa vào `test.status == 'completed'`.
  - Hiển thị tên Người thực hiện và Người kiểm tra ngay bên dưới Loại vật liệu.
- **Card chi tiết (`test_card.html`)**:
  - Tương tự như dòng lưới, bổ sung thông tin hiển thị người gán.
- **Form chỉnh sửa (`material_test_edit_row.html`, `test_edit_card.html`)**:
  - Bổ sung Row mới cho 3 trường: Người thực hiện, Người kiểm tra và Trạng thái.
  - Hiển thị thông báo lỗi text màu đỏ (red-500) ngay dưới trường Trạng thái nếu user cố tình vi phạm quyền duyệt.

---

## Trạng thái hiện tại
- ✅ Code đã cập nhật hoàn chỉnh.
- ⚠️ Cần chạy lệnh `python manage.py makemigrations` và `python manage.py migrate` từ bên trong Container Docker (do cấu trúc project chạy Docker nên AI không thể tự động chạy migrate bên ngoài host) để áp dụng cấu trúc Database mới.
