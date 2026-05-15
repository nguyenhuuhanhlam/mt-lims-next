# Ghi nhận thay đổi: UI Card Grouping & Bugfixes

**Ngày thực hiện:** 2026-05-13  
**Phiên làm việc:** 7bc910c1-00b6-44fa-871d-f5dbf55af9cd

---

## Mục tiêu

1. Thêm nền xám nhẹ vào các nhóm thông tin trong Detail Panel của trang `/requests` để dễ phân biệt vùng.
2. Áp dụng tương tự cho trang Create/Edit request (`/requests/{id}/edit`).
3. Kiểm tra và sửa lỗi xóa file khi xóa bài test.
4. Sửa lỗi 403 Forbidden khi HTMX DELETE request.

---

## Các thay đổi đã thực hiện

### 1. `templates/request_form/request_list.html` — Card grouping cho Detail Panel

Tab "Thông tin chung" trong Detail Panel được refactor: thay các divider `border-t` bằng card riêng biệt:

```html
<div class="bg-gray-50/70 rounded-xl p-3.5 border border-gray-100">
  <!-- nội dung nhóm -->
</div>
```

**6 card nhóm:**

| Card | Nội dung |
|---|---|
| Loại yêu cầu + Trạng thái | Badges pill |
| Người tạo + Ngày tạo | Key-value rows |
| Thông tin dự án | Tên dự án, Gói thầu, Địa điểm |
| Đơn vị yêu cầu | Địa chỉ, Số điện thoại |
| Người tham gia | Danh sách người tham gia |
| Nội dung | Textarea nội dung chi tiết |

Khoảng cách giữa card: `space-y-6` → `space-y-3`.

---

### 2. `templates/request_form/request_create.html` — Card grouping cho form Create/Edit

Áp dụng cùng style card cho form (dùng chung cho cả tạo mới và chỉnh sửa):

```html
<div class="bg-gray-50/70 rounded-xl p-4 border border-gray-100">
  <h3 class="text-[9px] font-bold text-indigo-500 uppercase tracking-[0.15em] mb-4">Tên nhóm</h3>
  <!-- các trường -->
</div>
```

**5 card nhóm:**

| Card | Trường |
|---|---|
| **Thông tin cơ bản** | Tiêu đề + Loại phiếu + Trạng thái + Người phụ trách |
| **Thông tin dự án** | Tên dự án + Gói thầu + Địa điểm |
| **Đơn vị yêu cầu** | Địa chỉ + Số điện thoại |
| **Người tham gia** | Dynamic list + nút Thêm người |
| **Nội dung** | Textarea nội dung chi tiết |

> **Lưu ý:** Tiêu đề nhóm label đổi từ `text-gray-400` → `text-indigo-500`. Row item người tham gia đổi nền từ `bg-gray-50/50` → `bg-white shadow-sm` để nổi bật trên card xám.

---

### 3. `request_form/models.py` — Sửa lỗi file leak khi xóa MaterialTest

**Vấn đề:** `test.delete()` Django chỉ xóa DB record, không xóa file vật lý khỏi disk → file rác tích tụ trong `media/tests/`.

**Giải pháp:** Override `delete()` trong model `MaterialTest`:

```python
import os

def delete(self, *args, **kwargs):
    # Xóa file vật lý khỏi disk trước khi xóa record
    if self.method_file:
        if os.path.isfile(self.method_file.path):
            os.remove(self.method_file.path)
    if self.result_file:
        if os.path.isfile(self.result_file.path):
            os.remove(self.result_file.path)
    super().delete(*args, **kwargs)
```

> **Lưu ý:** Kiểm tra `os.path.isfile()` trước khi xóa để tránh crash nếu file đã bị xóa ngoài hệ thống. Cũng áp dụng khi xóa Request (vì `CASCADE` gọi `delete()` trên từng MaterialTest).

---

### 4. `templates/base.html` — Sửa lỗi 403 Forbidden cho HTMX DELETE

**Vấn đề:** HTMX `hx-delete` không tự gửi CSRF token → Django trả về 403 Forbidden.

**Giải pháp:** Thêm global event listener vào `base.html` để inject header `X-CSRFToken` vào mọi HTMX request:

```javascript
document.body.addEventListener('htmx:configRequest', function(evt) {
  evt.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});
```

> Áp dụng toàn cục cho toàn bộ ứng dụng — fix cho DELETE, PUT, PATCH và mọi request HTMX không qua `<form>`.

---

## Files thay đổi

| File | Loại thay đổi |
|---|---|
| `templates/request_form/request_list.html` | Refactor Detail Panel: card grouping |
| `templates/request_form/request_create.html` | Refactor form: card grouping |
| `request_form/models.py` | Thêm `delete()` override để xóa file vật lý |
| `templates/base.html` | Thêm HTMX CSRF header config toàn cục |

---

## Trạng thái hiện tại

- ✅ Detail Panel và Form Create/Edit đều có card grouping nhất quán
- ✅ Xóa MaterialTest sẽ tự động xóa file khỏi disk
- ✅ HTMX DELETE request không còn bị 403 Forbidden
- ✅ Fix này áp dụng cho cả trang Detail Panel (`test_card.html`) lẫn trang danh sách (`material_test_row.html`)
