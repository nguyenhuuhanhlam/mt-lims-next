# Ghi nhận thay đổi: Bổ sung Role Khách hàng & Người quản lý cho Phiếu yêu cầu

**Ngày thực hiện:** 2026-05-16
**Phiên làm việc:** 2323fd44-c63f-4bff-b88a-6fdfcbf65284

---

## Mục tiêu

Cập nhật model `Request` để gán thêm 2 trường quan trọng:
1. **Khách hàng (Customer)**: Để khách hàng có thể theo dõi và xem phiếu của họ trên hệ thống. Field này được giới hạn (`limit_choices_to`) chỉ hiển thị các User thuộc nhóm `Customers`.
2. **Người quản lý (Manager)**: Để phân công người quản lý phiếu ra đề xuất trước khi tiến hành (thuộc nhóm `Managers` hoặc `Technicians`).

---

## Các thay đổi đã thực hiện

### 1. `lab_requests/models.py` — Bổ sung Database Relations

Thêm 2 Foreign Keys vào model `Request`:
- `customer`: Liên kết với `User`, `limit_choices_to={'groups__name': 'Customers'}`.
- `manager`: Liên kết với `User`, `limit_choices_to={'groups__name__in': ['Managers', 'Technicians']}`.

### 2. `lab_requests/forms.py` — Cập nhật Form

- Thêm `customer` và `manager` vào `fields` của `RequestForm`.
- Bổ sung UI widget (Select tag) đồng bộ với phong cách chung của hệ thống (Tailwind/Twenty CRM styling).
- Cải thiện UX dropdown: Thay thế lựa chọn rỗng mặc định (`---------`) bằng các nhãn text có ý nghĩa (`empty_label="Chọn người phụ trách..."`, v.v.).
- Khởi tạo mặc định: Khi tạo mới phiếu, trường **Người quản lý** tự động gán giá trị mặc định bằng với **Người phụ trách** (`initial['manager'] = initial.get('created_by')`).

### 3. Giao diện (Templates)

- **`templates/lab_requests/request_create.html`**:
  - Bổ sung 2 trường `Khách hàng` và `Người quản lý` dưới dạng Select box vào thẻ Card "Thông tin cơ bản".

- **`templates/lab_requests/partials/request_table_rows.html`**:
  - Truyền dữ liệu của Customer và Manager (`data-customer`, `data-manager`) vào thẻ `<tr>` của danh sách để HTMX/AlpineJS/VanillaJS có thể đọc.

- **`templates/lab_requests/request_list.html`**:
  - Cập nhật UI Detail Panel (Bảng chi tiết bên phải) bổ sung thêm 2 hàng thông tin "Khách hàng" và "Người quản lý" hiển thị bên dưới dòng "Người tạo".

---

## Trạng thái hiện tại

- ✅ Cấu trúc Database đã được cập nhật (Yêu cầu chạy `makemigrations` và `migrate`).
- ✅ Giao diện Form Tạo mới / Chỉnh sửa đã hỗ trợ chọn Khách hàng và Người quản lý.
- ✅ Bảng chi tiết (Detail panel) đã hiển thị thông tin này khi xem phiếu.
