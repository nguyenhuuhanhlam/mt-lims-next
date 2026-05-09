# Báo cáo Phân tích Dự án: MT-LIMS Next

## 1. Tổng quan dự án
Dự án **MT-LIMS Next** là một ứng dụng quản lý yêu cầu (Request Management System) được xây dựng trên nền tảng Django. Hệ thống cho phép người dùng tạo, quản lý và theo dõi các loại yêu cầu như "Hợp đồng" (Contract) và "Phiếu" (Slip).

## 2. Công nghệ sử dụng
- **Backend**: Python 3.x, Django Web Framework.
- **Database**: SQLite (db.sqlite3).
- **Frontend**: Django Templates, HTML/CSS.
- **Authentication**: Django Contrib Auth (tích hợp sẵn).

## 3. Cấu trúc thư mục chính
```text
mt-lims-next/
├── config/              # Cấu hình dự án Django (settings, urls, wsgi)
├── request_form/        # Ứng dụng chính xử lý logic yêu cầu
│   ├── migrations/      # Lịch sử thay đổi cơ sở dữ liệu
│   ├── admin.py         # Cấu hình trang quản trị
│   ├── forms.py         # Định nghĩa các biểu mẫu (RequestForm)
│   ├── models.py        # Định nghĩa cấu trúc dữ liệu (Request)
│   └── views.py         # Xử lý logic hiển thị và điều hướng
├── templates/           # Thư mục chứa các file HTML
│   ├── base.html        # Giao diện khung (Layout chính)
│   ├── dashboard.html   # Trang tổng quan
│   ├── registration/    # Các trang đăng nhập/đăng xuất
│   └── request_form/    # Các trang liên quan đến yêu cầu (list, create)
├── manage.py            # Công cụ quản lý dòng lệnh của Django
└── db.sqlite3           # Cơ sở dữ liệu SQLite
```

## 4. Các tính năng chính
- **Dashboard**: Hiển thị thống kê tổng số yêu cầu, số hợp đồng, số phiếu, yêu cầu mới trong ngày và danh sách các yêu cầu gần đây.
- **Quản lý yêu cầu**:
    - Danh sách yêu cầu: Hiển thị toàn bộ các yêu cầu đã tạo.
    - Tạo yêu cầu mới: Form nhập liệu bao gồm tiêu đề, loại yêu cầu (Contract/Slip) và nội dung.
- **Hệ thống API (Legacy)**: Cung cấp endpoint trả về dữ liệu JSON cho các yêu cầu.
- **Xác thực người dùng**: Yêu cầu đăng nhập (`@login_required`) để truy cập các tính năng.

## 5. Cấu trúc dữ liệu (Model: Request)
| Trường | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `title` | CharField | Tiêu đề của yêu cầu |
| `type` | CharField | Loại yêu cầu (contract hoặc slip) |
| `created_by` | ForeignKey | Người tạo (liên kết với bảng User của Django) |
| `content` | TextField | Nội dung chi tiết |
| `created_at` | DateTimeField | Thời gian tạo (tự động) |
| `updated_at` | DateTimeField | Thời gian cập nhật cuối cùng |

## 6. Luồng hoạt động (Workflow)
1. Người dùng truy cập vào hệ thống, nếu chưa đăng nhập sẽ được chuyển hướng đến trang `/accounts/login/`.
2. Sau khi đăng nhập, người dùng được đưa đến trang Dashboard (`/`) để xem tổng quan.
3. Người dùng có thể xem danh sách yêu cầu tại `/requests/` hoặc tạo yêu cầu mới tại `/requests/create/`.
4. Dữ liệu từ form được `RequestForm` kiểm tra tính hợp lệ trước khi lưu vào database.
5. Quản trị viên có thể quản lý dữ liệu thông qua trang `/admin/`.

## 7. Tài liệu bổ sung
- [Hệ thống thiết kế UI (UI Design System)](ui_design_system.md): Tài liệu chi tiết về các thành phần giao diện, màu sắc và typography theo phong cách Twenty CRM.
- [Kế hoạch triển khai (Implementation Plan)](implementation_plan.md): Lịch sử nâng cấp giao diện và các bước thực hiện.
