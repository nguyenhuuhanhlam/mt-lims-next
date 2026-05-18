# Ghi nhận thay đổi: Ẩn mục Hệ thống trên Sidebar với non-Managers

**Ngày thực hiện:** 2026-05-18
**Phiên làm việc:** 037aadd7-3d86-46ee-b0aa-cadcf8361060

---

## Mục tiêu

Ẩn toàn bộ nhóm **Hệ thống** (bao gồm mục **Người dùng** và **Nhóm**) trên Sidebar đối với những user không thuộc nhóm `Managers`. Superuser luôn được coi là Manager và vẫn thấy mục này.

---

## Các thay đổi đã thực hiện

### 1. `core/context_processors.py` — Tạo mới Context Processor

Tạo file mới để inject biến phân quyền vào toàn bộ template context:

```python
def user_roles(request):
    """
    Inject biến phân quyền vào toàn bộ template context.
    - is_manager: True nếu user thuộc nhóm Managers hoặc là superuser.
    """
    is_manager = False
    if request.user.is_authenticated:
        is_manager = (
            request.user.is_superuser
            or request.user.groups.filter(name="Managers").exists()
        )
    return {
        "is_manager": is_manager,
    }
```

> **Lý do dùng context processor (không dùng trực tiếp trong template):**
> Django template không hỗ trợ gọi method có tham số như `groups.filter(name='Managers').exists`. Phải tính toán sẵn ở Python và truyền vào context.

### 2. `config/settings.py` — Đăng ký Context Processor

Thêm vào danh sách `context_processors` trong `TEMPLATES`:

```python
'context_processors': [
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'core.context_processors.user_roles',  # <-- thêm dòng này
],
```

### 3. `templates/partials/sidebar.html` — Bọc nhóm Hệ thống

Bọc toàn bộ phần label **Hệ thống**, link **Người dùng** và link **Nhóm** bằng `{% if is_manager %}`:

```html
{% if is_manager %}
<!-- Group: System -->
<div class="pt-5 pb-1 px-3" x-show="sidebarOpen" x-cloak>
    <span class="text-[10px] font-bold text-gray-400 uppercase tracking-[0.1em]">Hệ thống</span>
</div>
<div x-show="!sidebarOpen" class="border-t border-gray-100 my-4 mx-4"></div>

<a href="{% url 'user_list' %}" ...>Người dùng</a>
<a href="{% url 'group_list' %}" ...>Nhóm</a>
{% endif %}
```

---

## Logic phân quyền

| Loại user | Thấy mục Hệ thống? |
|---|---|
| Thuộc nhóm `Managers` | ✅ Có |
| Superuser (`is_superuser=True`) | ✅ Có |
| Technicians / Customers / User thường | ❌ Không |

---

## ⚠️ Lưu ý quan trọng (Việc cần làm tiếp theo)

Hiện tại, việc ẩn mục Hệ thống **chỉ là ẩn UI** trên sidebar. Người dùng vẫn có thể truy cập trực tiếp bằng URL nếu biết đường dẫn.

**Cần bổ sung bảo vệ ở tầng View** trong `system_admin/views.py` cho các hàm `user_list`, `group_list` (và các view CRUD liên quan) bằng decorator kiểm tra nhóm:

```python
from django.contrib.auth.decorators import user_passes_test

def is_manager(user):
    return user.is_superuser or user.groups.filter(name='Managers').exists()

@login_required
@user_passes_test(is_manager)
def user_list(request):
    ...
```

---

## Trạng thái hiện tại

- ✅ Sidebar đã ẩn mục Hệ thống với non-Managers.
- ✅ Context processor `is_manager` hoạt động toàn cục, dùng được ở mọi template.
- ⚠️ Các View của `system_admin` **chưa** được bảo vệ ở tầng backend — cần bổ sung trong bước tiếp theo.
