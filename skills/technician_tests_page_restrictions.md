# Ghi nhận thay đổi: Hạn chế quyền Technician trên trang /tests

**Ngày thực hiện:** 2026-05-18
**Phiên làm việc:** 037aadd7-3d86-46ee-b0aa-cadcf8361060

---

## Mục tiêu

Áp dụng hạn chế quyền cho user thuộc nhóm `Technicians` trên trang `/tests` (Thí nghiệm vật liệu):
- **Không** có nút Xóa bài thí nghiệm.
- **Không** có nút Chỉnh sửa (Edit) bài thí nghiệm.
- **Chỉ** được upload file **Quy định Test (Method)** trực tiếp từ display row.

> **Lưu ý thiết kế:** Thay vì ẩn nút Edit và buộc Technician phải không làm gì, ta đặt nút upload Method File trực tiếp ngay trên display row (hover hiện ra) — không cần mở edit mode. Điều này cải thiện UX đáng kể.

---

## Các thay đổi đã thực hiện

### `templates/material_tests/partials/material_test_row.html` — Phân nhánh action theo Role

Cột **File** (cột cuối cùng) được tái cấu trúc với 2 nhánh:

```html
{% if is_technician %}
  {# Technician: chỉ upload Method trực tiếp, không Edit/Delete #}
  <div class="w-px h-3 bg-gray-200 mx-0.5"></div>
  <form hx-post="{% url 'test_row_upload_file' test.id 'method' %}"
        hx-encoding="multipart/form-data"
        hx-target="#test-row-{{ test.id }}"
        hx-swap="outerHTML"
        class="inline">
    {% csrf_token %}
    <label class="cursor-pointer p-1 rounded-md hover:bg-indigo-100 text-gray-400 hover:text-indigo-600 transition-colors"
           title="{% if test.method_file %}Tải lại Quy định{% else %}Upload Quy định{% endif %}">
      <i data-lucide="{% if test.method_file %}refresh-cw{% else %}upload{% endif %}" class="w-3.5 h-3.5"></i>
      <input type="file" name="file" class="hidden" onchange="this.form.dispatchEvent(new Event('submit'))" accept=".pdf,.png,.jpg,.jpeg">
    </label>
  </form>
{% else %}
  {# Manager/Admin: Edit + Delete đầy đủ #}
  <div class="w-px h-3 bg-gray-200 mx-0.5"></div>
  <button hx-get="...">Edit</button>
  <button hx-delete="...">Delete</button>
{% endif %}
```

**Icon thông minh theo trạng thái file:**
- Chưa có file method → icon `upload` (tải lên lần đầu)
- Đã có file method → icon `refresh-cw` (tải lại / cập nhật)

---

## Bảng tổng hợp quyền trên trang /tests

| Hành động | Technician | Manager / Superuser |
|---|:---:|:---:|
| Xem danh sách bài TN | ✅ | ✅ |
| Tìm kiếm / lọc | ✅ | ✅ |
| Chỉnh sửa bài TN | ❌ | ✅ |
| Xóa bài TN | ❌ | ✅ |
| Upload file Quy định (Method) | ✅ (trực tiếp trên row) | ✅ |
| Upload file Kết quả (Result) | ❌ | ✅ |
| Tải xuống file đã có | ✅ | ✅ |

---

## Kết hợp với skill trước

Cùng với `technician_role_restrictions.md`, toàn bộ hệ thống phân quyền Technician được áp dụng nhất quán tại 2 điểm:

| Khu vực | File đã sửa |
|---|---|
| Detail Panel (trong /requests) | `test_card.html`, `test_list.html`, `request_list.html` |
| Trang /tests | `material_test_row.html` |

---

## ⚠️ Lưu ý (Việc cần làm tiếp theo)

Tương tự như các skill trước, cần bảo vệ tầng **View backend** cho `test_row_edit`, `test_delete` trong `material_tests/views.py`:

```python
from django.contrib.auth.decorators import user_passes_test

def not_technician_only(user):
    if user.is_superuser or user.groups.filter(name="Managers").exists():
        return True
    return not user.groups.filter(name="Technicians").exists()

@login_required
@user_passes_test(not_technician_only)
def test_row_edit(request, test_id):
    ...

@login_required
@user_passes_test(not_technician_only)
def test_delete(request, test_id):
    ...
```

---

## Trạng thái hiện tại

- ✅ Trang `/tests`: Technician chỉ thấy nút upload Method, không thấy Edit/Delete.
- ✅ Icon upload thông minh: `upload` khi chưa có file, `refresh-cw` khi đã có.
- ⚠️ Các View backend `test_row_edit` và `test_delete` **chưa** được bảo vệ.
