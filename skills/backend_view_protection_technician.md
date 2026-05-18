# Ghi nhận thay đổi: Bảo vệ tầng View Backend cho Technician

**Ngày thực hiện:** 2026-05-18
**Phiên làm việc:** 037aadd7-3d86-46ee-b0aa-cadcf8361060

---

## Mục tiêu

Hoàn thiện phân quyền cho nhóm `Technicians` ở **tầng View (Backend)** — không cho phép truy cập trực tiếp URL dù đã ẩn UI. Áp dụng `@user_passes_test` decorator lên các view có hành động tạo/sửa/xóa.

---

## Nguyên tắc thiết kế helper `not_technician`

```python
def not_technician(user):
    """Cho phép truy cập nếu user là superuser, Manager, hoặc không phải Technician."""
    if user.is_superuser or user.groups.filter(name="Managers").exists():
        return True
    return not user.groups.filter(name="Technicians").exists()
```

Logic ưu tiên:
1. Superuser → luôn được phép
2. Thuộc nhóm `Managers` → được phép
3. Thuộc nhóm `Technicians` → bị chặn
4. User thường (không thuộc nhóm nào) → được phép

> **Lưu ý:** Helper này được định nghĩa riêng trong **từng file views.py** (không tách ra file riêng) để đảm bảo tính đơn giản và không tạo dependency phức tạp giữa các app. Nếu sau này cần tái sử dụng nhiều, có thể chuyển sang `core/utils.py`.

---

## Các thay đổi đã thực hiện

### 1. `material_tests/views.py`

Thêm import và helper:

```python
from django.contrib.auth.decorators import login_required, user_passes_test

def not_technician(user): ...
```

Áp dụng `@user_passes_test(not_technician)` lên 4 view:

| View | Lý do bảo vệ |
|---|---|
| `test_create` | Technician không được tạo bài test mới |
| `test_edit` | Technician không được sửa bài test (từ Detail Panel) |
| `test_delete` | Technician không được xóa bài test |
| `test_row_edit` | Technician không được sửa bài test (từ trang /tests) |

*Không áp dụng cho:* `test_upload_file`, `test_row_upload_file` — Technician được phép upload file Method.

### 2. `lab_requests/views.py`

Tương tự, áp dụng lên 3 view:

| View | Lý do bảo vệ |
|---|---|
| `request_create` | Technician không được tạo phiếu mới |
| `request_edit` | Technician không được sửa phiếu |
| `request_delete` | Technician không được xóa phiếu |

*Không áp dụng cho:* `request_list` — Technician được xem danh sách.

---

## Hành vi khi Technician cố truy cập URL bị chặn

Django `@user_passes_test` mặc định redirect về `/accounts/login/?next=<url>` khi test fail. Vì project đã cấu hình `LOGIN_URL` và user đã đăng nhập, có thể cần chỉ định redirect rõ hơn:

```python
# Nếu muốn redirect về trang cụ thể thay vì login:
@user_passes_test(not_technician, login_url='/forbidden/')
```

Hiện tại để mặc định — khi Technician cố truy cập URL bị chặn, họ sẽ bị redirect về trang login.

---

## Tổng kết toàn bộ hệ thống phân quyền Technician

| Tầng | Trạng thái |
|---|---|
| UI — Sidebar (mục Hệ thống) | ✅ Ẩn hoàn toàn |
| UI — Detail Panel (sửa/xóa phiếu) | ✅ Ẩn footer Edit/Delete |
| UI — Detail Panel (thêm/sửa/xóa test) | ✅ Ẩn nút thêm, edit, delete |
| UI — Detail Panel (upload Result) | ✅ Ẩn form upload, chỉ xem |
| UI — Trang /tests (edit/delete row) | ✅ Ẩn, thay bằng nút upload Method |
| Backend — `request_create/edit/delete` | ✅ Bảo vệ bằng `@user_passes_test` |
| Backend — `test_create/edit/delete/row_edit` | ✅ Bảo vệ bằng `@user_passes_test` |
| Backend — `system_admin` views | ⚠️ Chưa bảo vệ (việc tiếp theo) |

---

## Trạng thái hiện tại

- ✅ Tầng UI và Backend đều đã bảo vệ nhất quán.
- ⚠️ Các view trong `system_admin` (user_list, group_list, user_create...) **chưa** được bảo vệ backend — cần bổ sung trong bước sau nếu cần.
