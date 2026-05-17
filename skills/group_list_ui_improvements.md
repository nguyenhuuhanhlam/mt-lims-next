# Ghi nhận thay đổi: Cải tiến giao diện Danh sách Nhóm (Group List)

**Ngày thực hiện:** 2026-05-17
**Phiên làm việc:** 8de843a2-2b68-4ce0-9db9-99e5e993590f

---

## Mục tiêu

Cải thiện giao diện quản lý danh sách Nhóm (Groups) theo sát chuẩn thiết kế "Twenty CRM" của dự án:
1. Loại bỏ các nút thao tác (Xóa/Sửa) khỏi lưới dữ liệu để giao diện gọn gàng hơn.
2. Thêm bảng trượt chi tiết (Detail Panel) ở bên phải.
3. Tích hợp HTMX để gọi danh sách người dùng (User) thuộc nhóm hiển thị ngay trên Detail Panel.
4. Đưa các tính năng Xóa và Sửa xuống phần Footer của bảng trượt để tránh thao tác nhầm.

---

## Các thay đổi đã thực hiện

### 1. Backend & Định tuyến
- **`system_admin/urls.py`**: Đăng ký thêm URL mới `path("groups/<int:pk>/members/", group_members, name="group_members")` để phục vụ HTMX.
- **`system_admin/views.py`**: Bổ sung hàm `group_members` để truy xuất và trả về giao diện HTML (danh sách thành viên của một nhóm thông qua quan hệ `user_set`).

### 2. Giao diện (Templates)
- **`templates/system_admin/partials/group_table_rows.html`**:
  - Loại bỏ cột "Thao tác" cùng với các nút Sửa/Xóa.
  - Thêm class `cursor-pointer`, `request-row` và sự kiện `onclick="openDetail(this)"` vào mỗi thẻ `<tr>`.
  - Gán dữ liệu cho hàng bằng `data-id` và `data-name`.
  
- **`templates/system_admin/group_list.html`**:
  - Bổ sung cấu trúc HTML của **Detail Panel** (ẩn mặc định) bao gồm Header (tên nhóm), Body (khu vực trống tải dữ liệu thành viên) và Footer (các nút Sửa/Xóa).
  - Cập nhật Javascript với các hàm `openDetail(row)` và `closeDetail()` để điều khiển hiệu ứng trượt (`translate-x-full`) và kích hoạt `htmx.ajax` nạp danh sách thành viên.

- **`templates/system_admin/partials/group_members.html`**:
  - File mới được tạo để render (trả về qua HTMX) danh sách người dùng trong nhóm. Giao diện thiết kế theo hướng thẻ gọn gàng: Avatar chữ cái đầu, Tên đầy đủ và Email.

---

## Trạng thái hiện tại
- ✅ Giao diện lưới gọn gàng hơn, tính tương tác cao.
- ✅ Bảng trượt Detail Panel hiển thị mượt mà.
- ✅ HTMX hoạt động trơn tru trong việc tải danh sách thành viên.
- ✅ An toàn thao tác được cải thiện nhờ việc dời các nút xóa/sửa xuống dưới cùng của bảng trượt.
