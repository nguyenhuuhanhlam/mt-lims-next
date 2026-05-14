# Ghi nhận thay đổi: Upload File trên trang /tests

**Ngày thực hiện:** 2026-05-12  
**Phiên làm việc:** c0b94227-57b1-4558-8a88-16fc8942e18a

---

## Mục tiêu

Thêm chức năng upload 2 file (**Quy định Test** và **Kết quả Test**) vào trang danh sách `/tests`, tương tự như chức năng đã có trong phần **Bài Test** ở Detail Panel của từng phiếu yêu cầu.

Yêu cầu bổ sung: Upload chỉ hiển thị khi ở chế độ **Edit**, không hiện trên lưới bình thường.

---

## Các thay đổi đã thực hiện

### 1. `request_form/views.py` — Thêm view upload mới

Thêm view `test_row_upload_file` riêng biệt (khác với `test_upload_file` dùng cho Detail Panel):

```python
@login_required
def test_row_upload_file(request, test_id, file_type):
    """Upload file (method/result) từ trang danh sách /tests — render lại material_test_row."""
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "POST":
        file_obj = request.FILES.get("file")
        if file_obj:
            if file_type == "method":
                test.method_file = file_obj
                test.method_uploader = request.user
            elif file_type == "result":
                test.result_file = file_obj
                test.result_uploader = request.user
            test.save()
            return render(request, "request_form/partials/material_test_row.html", {"test": test})
    return JsonResponse({"error": "Upload failed"}, status=400)
```

> **Lý do tách view:** View upload cũ (`test_upload_file`) render lại `test_card.html` dùng cho Detail Panel. View mới render lại `material_test_row.html` phù hợp với trang danh sách.

---

### 2. `config/urls.py` — Đăng ký URL mới

```python
path("tests/<int:test_id>/row-upload/<str:file_type>/", test_row_upload_file, name="test_row_upload_file"),
```

---

### 3. `templates/request_form/partials/material_test_row.html` — Giữ lưới sạch

Cột "File" trong lưới bình thường **chỉ hiển thị icon download** (xuất hiện khi hover), không có form upload:

- Icon `file-down` (indigo) → File Quy định (nếu đã có)
- Icon `file-check` (emerald) → File Kết quả (nếu đã có)
- Nút Edit / Delete như cũ

---

### 4. `templates/request_form/partials/material_test_edit_row.html` — Upload trong Edit Row

Khi bấm Edit, row mở rộng gồm **3 phần**:

| Phần | Nội dung |
|---|---|
| Row 1 | Các trường: Mã số, Loại vật liệu, Số lượng, Đơn vị, Ngày TN |
| Row 2 | Trường Nội dung yêu cầu |
| Row 3 | **Upload Quy định** \| **Upload Kết quả** \| `ml-auto` → **Hủy** \| **Lưu** |

**Cấu trúc quan trọng:**
- Form chỉnh sửa text có `id="edit-form-{{ test.id }}"` để nút **Lưu** bên ngoài form có thể submit qua `form="edit-form-{{ test.id }}"`.
- Mỗi upload là một `<form>` riêng với `hx-encoding="multipart/form-data"`, swap lại toàn bộ `<tr>` sau khi upload.
- Nút **Hủy** dùng HTMX GET để lấy lại `material_test_row.html`.

---

## Trạng thái upload trong Edit Row

| Trạng thái file | Hiển thị |
|---|---|
| Chưa có file | Nút "Tải lên" (border dashed, màu nhạt) |
| Đã có file | Link "Đã tải" + nút "Tải lại" (icon refresh) |

- **Quy định:** Màu indigo
- **Kết quả:** Màu emerald

---

## Luồng hoạt động

```
Lưới /tests
  └─ Hover → hiện icon download (nếu có file)
  └─ Bấm nút Edit (icon edit-3)
       └─ HTMX GET → trả về material_test_edit_row.html
            ├─ Row 1-2: chỉnh sửa thông tin
            └─ Row 3: Upload Quy định | Upload Kết quả | Hủy | Lưu
                 ├─ Chọn file → HTMX POST multipart → swap lại <tr> (trạng thái bình thường)
                 └─ Bấm Lưu → HTMX POST form → swap lại <tr>
```

---

## Files thay đổi

| File | Loại thay đổi |
|---|---|
| `request_form/views.py` | Thêm view `test_row_upload_file` |
| `config/urls.py` | Thêm URL `tests/<id>/row-upload/<file_type>/` |
| `templates/request_form/partials/material_test_row.html` | Bỏ upload form, chỉ giữ download icon |
| `templates/request_form/partials/material_test_edit_row.html` | Thêm Row 3 upload + gộp nút Hủy/Lưu cùng hàng |
| `templates/request_form/material_test_list.html` | Cập nhật header bảng (7 cột) |
