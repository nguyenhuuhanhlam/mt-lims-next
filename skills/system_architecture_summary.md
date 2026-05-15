# Tóm tắt Tổng quan Kiến trúc và Giao diện (MT-LIMS Next)

Tài liệu này tóm tắt ngắn gọn các tiêu chuẩn kiến trúc, thiết kế và nghiệp vụ cốt lõi của hệ thống, được tổng hợp từ các báo cáo trước đó.

## 1. Tổng quan Hệ thống (MT-LIMS Next)
* **Mục tiêu:** Hệ thống quản lý yêu cầu (Hợp đồng, Phiếu) dựa trên Django.
* **Stack Công nghệ (TALL Stack):** Django (Backend) + SQLite (Database) + Tailwind CSS (Styling) + Alpine.js (State UI) + HTMX (Tương tác động).
* **Luồng hoạt động:** Yêu cầu đăng nhập -> Dashboard (thống kê) -> Quản lý danh sách / Tạo mới yêu cầu.

## 2. Cấu trúc Dữ liệu & Nghiệp vụ (Models & Forms)
* **Model `Request`:** Gồm các trường cơ bản (Title, Type, Created_by, Content, Timestamps) và các trường mở rộng dạng JSON:
  * **Trạng thái (status):** Đang xem xét, Đang thực hiện, Hoàn tất, Hủy bỏ.
  * **Người tham gia:** Danh sách (Họ tên, Chức vụ).
  * **Thông tin dự án:** Tên dự án, Gói thầu, Địa điểm.
  * **Đơn vị yêu cầu:** Địa chỉ, Số điện thoại.
  * *Lưu ý:* Các trường JSON có `@property` bổ trợ để đảm bảo xuất chuẩn định dạng sang Template.
* **Form (`RequestForm`):**
  * Tự động tách (unpack) / gộp (pack) các trường JSON thành ô nhập liệu riêng.
  * Tích hợp trực tiếp Alpine.js (`x-model`) vào Form của Django để đồng bộ hai chiều.

## 3. Tiêu chuẩn Thiết kế (Twenty CRM Style)
* **Nguyên tắc cốt lõi:** Compact & Dense (Tối ưu không gian), Premium Aesthetics (Hiệu ứng kính mờ, đổ bóng nhẹ, bo góc lớn), Typography Focus.
* **Font & Kích thước (Typography):**
  * Font chính: Inter.
  * Tiêu đề: `text-lg` in đậm.
  * Nội dung bảng: `text-[13px]`.
  * Metadata / Label: `text-[9px]` đến `text-[11px]`, in hoa (uppercase), giãn chữ (tracking-widest).
* **Màu sắc & Giao diện:**
  * Màu nền Sidebar/Border: Xám cực nhạt (`#fafafa`, `gray-50`/`100`).
  * Màu nhấn chủ đạo (Primary): `indigo-500` / `indigo-600`.
  * Bo góc: `rounded-xl` (12px) cho thẻ/nút, `rounded-2xl` (16px) cho Form/Card lớn.
* **Thành phần Component chính:**
  * **Sidebar (220px/64px) & Topbar (48px):** Có Workspace switcher, Icon Lucide (size 3.5), Topbar dính (sticky) kèm hiệu ứng `backdrop-blur`.
  * **Bảng dữ liệu:** Badges dạng viên thuốc (Pill) bo tròn 100%, hàng hover nhạt (`indigo-50/30`).
  * **Detail Panel (380px):** Bảng chi tiết dạng trượt (slide-in) từ phải sang với shadow lớn.

## 4. Logic Giao diện (HTMX & Alpine.js)
* **HTMX:** Xử lý tìm kiếm và lọc danh sách thời gian thực (Real-time). Server trả về đoạn HTML nhỏ (fragment) thay vì load lại toàn bộ trang, giúp giảm Javascript thuần.
* **Alpine.js:** Quản lý đóng/mở Sidebar, Topbar, Detail panel và form nhập liệu động (ví dụ: thêm/xóa hàng danh sách người tham gia trực tiếp).
* **Truyền dữ liệu:** Sử dụng `json_script` của Django để truyền dữ liệu tĩnh an toàn sang cho Javascript/Alpine.js.

## 5. Module Thí nghiệm Vật liệu (Material Tests)
* **Cấu trúc Dữ liệu:** Bổ sung Model `MaterialTest` liên kết với `Request` qua khóa ngoại. Quản lý trạng thái hoàn tất (`is_completed`) dựa trên việc tải lên đủ 2 file: File Quy định test (Method) và File Kết quả (Result).
* **Lưu trữ File:** Thiết lập hệ thống lưu file local (`MEDIA_ROOT` và `MEDIA_URL` trong settings) để dễ dàng triển khai ở giai đoạn phát triển.
* **Giao diện & HTMX:**
  * **Detail Panel Tabs:** Nâng cấp Detail Panel với cấu trúc Thẻ (Tabs) dùng Alpine.js (`x-show`) và bổ sung tính năng Kéo thả để thay đổi độ rộng (Drag to resize).
  * **Tương tác ngầm:** Danh sách bài test được tải (Load), Tạo mới (Create Modal), Chỉnh sửa trực tiếp (Inline Edit), Xóa (Inline Delete) hoàn toàn thông qua HTMX.
  * **Tải file:** Form tải file được thực thi bằng HTMX (`hx-encoding="multipart/form-data"`), tự động hoán đổi giao diện thành "Đã tải lên" sau khi file được upload. Khắc phục lỗi hiển thị icon bằng sự kiện `htmx:afterSwap` toàn cục.
