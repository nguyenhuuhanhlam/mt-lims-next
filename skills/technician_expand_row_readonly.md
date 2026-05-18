# Ghi nhận thay đổi: Technician có thể mở rộng row xem chi tiết trên trang /tests

**Ngày thực hiện:** 2026-05-18
**Phiên làm việc:** 037aadd7-3d86-46ee-b0aa-cadcf8361060

---

## Vấn đề

Sau khi ẩn nút Edit/Delete khỏi display row của Technician, icon expand (edit-3) bị mất hoàn toàn. Technician không còn cách nào để xem chi tiết bài test hoặc upload file Method trên trang `/tests`.

---

## Giải pháp

Thay vì ẩn icon expand, **đổi icon** thành `eye` (xem) cho Technician. Khi click, vẫn gọi cùng URL `test_row_edit` nhưng template sẽ render chế độ **read-only** thay vì form chỉnh sửa. Upload Method vẫn có sẵn trong expanded row.

---

## Các thay đổi đã thực hiện

### 1. `material_tests/views.py` — Tách logic GET/POST trong `test_row_edit`

- **Bỏ** `@user_passes_test(not_technician)` khỏi decorator (để Technician có thể GET).
- **Thêm** kiểm tra thủ công trong POST: Technician cố lưu → trả về HTTP 403.

```python
@login_required
def test_row_edit(request, test_id):
    test = get_object_or_404(MaterialTest, pk=test_id)
    is_tech = not not_technician(request.user)
    if request.method == "POST":
        # Technician không được lưu (nút Lưu bị ẩn trong template, nhưng bảo vệ thêm ở backend)
        if is_tech:
            return HttpResponse(status=403)
        form = MaterialTestForm(request.POST, instance=test, user=request.user)
        if form.is_valid():
            form.save()
            return render(request, "material_tests/partials/material_test_row.html", {"test": test})
    else:
        form = MaterialTestForm(instance=test, user=request.user)
    return render(request, "material_tests/partials/material_test_edit_row.html", {"test": test, "form": form})
```

### 2. `material_test_row.html` — Đổi icon Technician từ upload sang eye

Technician thấy icon `eye` thay vì form upload inline. Click icon → mở expanded row:

```html
{% if is_technician %}
  <div class="w-px h-3 bg-gray-200 mx-0.5"></div>
  <button
    hx-get="{% url 'test_row_edit' test.id %}"
    hx-target="#test-row-{{ test.id }}"
    hx-swap="outerHTML"
    class="p-1 rounded-md hover:bg-indigo-100 text-gray-400 hover:text-indigo-600 transition-colors"
    title="Xem chi tiết / Upload file">
    <i data-lucide="eye" class="w-3.5 h-3.5"></i>
  </button>
{% else %}
  {# Manager/Admin: Edit + Delete đầy đủ #}
  ...
{% endif %}
```

### 3. `material_test_edit_row.html` — Hai chế độ hiển thị theo role

**Với Technician:** Read-only display + upload Method + nút Đóng.

```html
{% if is_technician %}
  {# Hiển thị text thuần — không có form input #}
  <div class="flex flex-wrap items-center gap-x-6 gap-y-2">
    <div>
      <span class="...">Mã số</span>
      <p>{{ test.test_code }}</p>
    </div>
    {# ... các trường: loại vật liệu, số lượng, ngày TN, người thực hiện, người kiểm tra, trạng thái #}
  </div>
  {% if test.content %}<p>{{ test.content }}</p>{% endif %}
{% else %}
  {# Manager/Admin: form chỉnh sửa đầy đủ #}
  <form id="edit-form-{{ test.id }}" hx-post="..."> ... </form>
{% endif %}
```

**Phần upload file (Row 3):**
- File Quy định (Method): hiển thị với mọi user (kể cả Technician)
- File Kết quả (Result): bọc trong `{% if not is_technician %}` — ẩn với Technician

**Nút hành động:**
- Nút "Đóng" (đổi tên từ "Hủy"): hiển thị với mọi user
- Nút "Lưu": bọc trong `{% if not is_technician %}` — ẩn với Technician

---

## So sánh trải nghiệm trong expanded row

| Phần | Technician | Manager |
|---|:---:|:---:|
| Dữ liệu bài test | 📖 Read-only text | ✏️ Form input |
| Upload Quy định (Method) | ✅ | ✅ |
| Upload Kết quả (Result) | ❌ Ẩn | ✅ |
| Nút Lưu | ❌ Ẩn | ✅ |
| Nút Đóng | ✅ | ✅ |

---

## Lưu ý thiết kế

> **Defense in depth:** Dù nút Lưu bị ẩn trong UI, backend `test_row_edit` vẫn kiểm tra `is_tech` trong POST handler và trả về HTTP 403 nếu Technician cố bypass. Đây là nguyên tắc bảo vệ hai lớp (UI + Backend).

> **Nút đổi tên Hủy → Đóng:** Với Technician không có gì để "hủy" (không có thay đổi nào), nên đổi tên nút thành "Đóng" giúp UX rõ ràng hơn.

---

## Trạng thái hiện tại

- ✅ Technician click icon `eye` → mở expanded row read-only.
- ✅ Technician có thể upload file Method trong expanded row.
- ✅ Technician không thể lưu thay đổi (cả UI lẫn backend đều bảo vệ).
- ✅ Manager/Admin không bị ảnh hưởng — trải nghiệm chỉnh sửa như cũ.
