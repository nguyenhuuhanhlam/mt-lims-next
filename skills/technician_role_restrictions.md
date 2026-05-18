# Ghi nhận thay đổi: Hạn chế quyền Technician trên Detail Panel

**Ngày thực hiện:** 2026-05-18
**Phiên làm việc:** 037aadd7-3d86-46ee-b0aa-cadcf8361060

---

## Mục tiêu

User thuộc nhóm `Technicians` khi vào trang **Phiếu yêu cầu** và xem chi tiết (Detail Panel) sẽ bị hạn chế:
- **Không** được chỉnh sửa hoặc xóa Phiếu yêu cầu.
- **Không** được tạo mới, chỉnh sửa, hoặc xóa Bài Test.
- **Chỉ** được upload file **Quy định Test (Method)**. File **Kết quả Test (Result)** chỉ hiển thị để xem/tải, không có form upload.

---

## Các thay đổi đã thực hiện

### 1. `core/context_processors.py` — Bổ sung biến `is_technician`

```python
def user_roles(request):
    is_manager = False
    is_technician = False
    if request.user.is_authenticated:
        is_manager = (
            request.user.is_superuser
            or request.user.groups.filter(name="Managers").exists()
        )
        if not is_manager:
            is_technician = request.user.groups.filter(name="Technicians").exists()
    return {
        "is_manager": is_manager,
        "is_technician": is_technician,
    }
```

> **Lưu ý thiết kế:** `is_technician` chỉ `True` khi user **không phải** Manager/superuser. Nếu một user vừa thuộc `Managers` vừa thuộc `Technicians`, quyền Manager sẽ được ưu tiên.

---

### 2. `templates/lab_requests/request_list.html` — Ẩn footer Edit/Delete

**Panel Footer** (nút Chỉnh sửa + Xóa phiếu) được bọc trong `{% if not is_technician %}`:

```html
{% if not is_technician %}
<div class="border-t border-gray-100 p-5 bg-gray-50/30 flex gap-2.5">
  <a id="detail-edit-link" href="#">Chỉnh sửa</a>
  <a id="detail-delete-link" href="#">🗑</a>
</div>
{% endif %}
```

Đồng thời, inject biến JS để ngăn gán href khi không có quyền:

```html
<script>
  const IS_TECHNICIAN = {{ is_technician|yesno:'true,false' }};
  // ...
  if (!IS_TECHNICIAN) {
    document.getElementById('detail-edit-link').href = '/requests/' + row.dataset.id + '/edit/';
    document.getElementById('detail-delete-link').href = '/requests/' + row.dataset.id + '/delete/';
  }
</script>
```

---

### 3. `templates/core/dashboard.html` & `templates/lab_requests/request_list.html` — Ẩn nút "Tạo yêu cầu"

Nút **Tạo yêu cầu** ở thanh công cụ phía trên cùng của trang Dashboard và trang danh sách Phiếu yêu cầu được bọc trong `{% if not is_technician %}`:

```html
{% if not is_technician %}
<a href="{% url 'request_create' %}" class="...">
  <i data-lucide="plus" class="w-3.5 h-3.5"></i>
  Tạo yêu cầu
</a>
{% endif %}
```

---

### 3. `templates/material_tests/partials/test_list.html` — Ẩn nút "Thêm test"

```html
{% if not is_technician %}
<button @click="showModal = true">+ Thêm test</button>
{% endif %}
```

---

### 4. `templates/material_tests/partials/test_card.html` — Ẩn Edit/Delete bài test & upload Result

**Nút Edit/Delete bài test:**
```html
{% if not is_technician %}
<div class="flex items-center gap-1 border-l border-gray-100 pl-2">
  <button hx-get="...">Edit</button>
  <button hx-delete="...">Delete</button>
</div>
{% endif %}
```

**Kết quả Test (Result File)** — phân nhánh theo role:
```html
{% if is_technician %}
  {# Technician: chỉ xem, không upload #}
  {% if test.result_file %}
    <a href="{{ test.result_file.url }}">Đã tải</a>
  {% else %}
    <span>Chưa có file</span>
  {% endif %}
{% else %}
  {# Manager/Admin: xem + upload đầy đủ #}
  ...
{% endif %}
```

---

## Bảng tổng hợp quyền theo Role

| Hành động | Technician | Manager / Superuser |
|---|:---:|:---:|
| Xem thông tin phiếu | ✅ | ✅ |
| Tạo phiếu mới | ❌ | ✅ |
| Chỉnh sửa phiếu | ❌ | ✅ |
| Xóa phiếu | ❌ | ✅ |
| Xem danh sách bài test | ✅ | ✅ |
| Thêm bài test | ❌ | ✅ |
| Sửa bài test | ❌ | ✅ |
| Xóa bài test | ❌ | ✅ |
| Upload file Method | ✅ | ✅ |
| Upload file Result | ❌ | ✅ |

---

## ⚠️ Lưu ý (Việc cần làm tiếp theo)

Hiện tại các hạn chế trên chỉ ở **tầng UI (Template)**. Cần bổ sung bảo vệ ở **tầng View (Backend)** trong `lab_requests/views.py` và `material_tests/views.py`:

```python
from django.contrib.auth.decorators import user_passes_test

def not_technician_only(user):
    """Chặn user chỉ thuộc Technicians (không phải Manager/superuser)."""
    if user.is_superuser or user.groups.filter(name="Managers").exists():
        return True
    return not user.groups.filter(name="Technicians").exists()

# Áp dụng lên các view edit/delete:
@login_required
@user_passes_test(not_technician_only)
def request_edit(request, pk):
    ...
```

---

## Trạng thái hiện tại

- ✅ UI đã ẩn đúng các nút theo role Technician.
- ✅ Nút "Tạo yêu cầu" trên Dashboard và danh sách yêu cầu đã bị ẩn.
- ⚠️ Các View backend **chưa** được bảo vệ — cần bổ sung `@user_passes_test` trong bước tiếp theo.
