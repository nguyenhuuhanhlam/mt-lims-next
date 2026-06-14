# Cẩm nang Dự án MT-LIMS Next (Project Guide)

Tài liệu này là cẩm nang hướng dẫn toàn diện về kiến trúc hệ thống, chuẩn thiết kế, luồng nghiệp vụ và quy tắc phân quyền cho dự án **MT-LIMS Next**.

---

## 1. Kiến trúc Tổng quan & Tech Stack

### Tech Stack cốt lõi (TALL Stack)
* **Backend:** Django
* **Database:** MariaDB (Ban đầu dùng SQLite trong giai đoạn phát triển sơ khai)
* **Styling (CSS):** Tailwind CSS
* **State UI:** Alpine.js
* **Dynamic Interactions:** HTMX (Tải/lọc dữ liệu thời gian thực và tương tác inline)

### Cấu trúc Django Apps (Tái cấu trúc)
Dự án được phân tách từ app duy nhất `request_form` trước đây thành 4 app độc lập, chuyên biệt:
* **`core`:** Entry-point chính của ứng dụng, quản lý trang Dashboard, các trang dùng chung và context processors.
* **`lab_requests`:** Quản lý vòng đời Phiếu yêu cầu (Request), các views, forms và templates tương ứng.
* **`material_tests`:** Quản lý các bài thí nghiệm vật liệu (MaterialTest) liên kết với từng phiếu yêu cầu, bao gồm luồng thực hiện bài test và upload tài liệu liên quan.
* **`system_admin`:** Quản lý người dùng (User) và nhóm quyền (Group).

### Tương thích Cơ sở dữ liệu MariaDB
Hệ thống sử dụng thư viện `pymysql` và `python-dotenv` để kết nối MariaDB. Do server chạy phiên bản MariaDB cũ (10.3.32) không hỗ trợ cú pháp `RETURNING` (yêu cầu từ Django 5.2+), hệ thống áp dụng một monkey-patch trong file `config/settings.py` để bỏ qua kiểm tra phiên bản và tắt tính năng returning:

```python
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# Monkey-patch cho tương thích ngược MariaDB < 10.5
BaseDatabaseWrapper.check_database_version_supported = lambda self: None
DatabaseFeatures.can_return_columns_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False
```

---

## 2. Chuẩn Thiết kế & Giao diện (Twenty CRM Style)

### Nguyên tắc thiết kế chủ đạo
* **Compact & Dense:** Tối ưu không gian hiển thị, tăng mật độ thông tin nhưng vẫn rõ ràng.
* **Premium Aesthetics:** Sử dụng hiệu ứng kính mờ (glassmorphism/backdrop-blur), đổ bóng nhẹ (soft shadows), bo góc lớn (`rounded-xl` ~ 12px và `rounded-2xl` ~ 16px).
* **Typography Focus:** Cải thiện cấu trúc font chữ và kích thước chữ.

### Typography & Colors
* **Font:** `Inter` (Google Fonts).
* **Kích thước chữ:**
  * Tiêu đề: `text-lg font-bold`.
  * Nội dung bảng / lưới: `text-[13px]`.
  * Metadata / Label: `text-[9px]` đến `text-[11px]`, viết hoa (`uppercase`), giãn chữ (`tracking-widest` hoặc `tracking-[0.1em]`).
* **Màu sắc:**
  * Nền Sidebar & Border: Xám cực nhạt (`#fafafa`, Tailwind classes `bg-gray-50` / `border-gray-100`).
  * Màu nhấn chủ đạo (Primary): `indigo-500` / `indigo-600`.
  * Màu nhấn cho trạng thái hoàn tất: `emerald-500` / `emerald-600`.
  * Hover hàng dữ liệu: `bg-indigo-50/30`.

### Các Component Giao diện Đặc trưng
* **Sidebar (Rộng 220px khi mở, 64px khi co):** Bao gồm Workspace Switcher, menu phân nhóm (Nghiệp vụ, Hệ thống) và phần thông tin User + Logout dưới cùng.
* **Topbar (Cao 48px):** Cố định (sticky) với hiệu ứng `backdrop-blur`, chứa nút toggle Sidebar, Breadcrumbs và Actions nhanh.
* **Detail Panel (Rộng 380px):** Bảng trượt (slide-in) từ phải sang (`translate-x-full` sang `translate-x-0`) hiển thị thông tin chi tiết. Sử dụng Alpine.js để chuyển đổi các Tab (`x-show`) và hỗ trợ tính năng kéo thả thay đổi độ rộng (drag to resize).
* **Card Grouping:**
  * Thay vì sử dụng các đường kẻ phân tách `border-t` truyền thống, các thông tin trong Detail Panel và Form được gom nhóm vào các thẻ Card màu xám nhạt:
    ```html
    <div class="bg-gray-50/70 rounded-xl p-3.5 border border-gray-100">
        <!-- Nội dung nhóm -->
    </div>
    ```
  * Tiêu đề Card đổi sang màu xanh Indigo: `text-indigo-500` viết hoa, font chữ nhỏ, giãn dòng.
  * *Detail Panel:* Gồm 6 nhóm Card (Trạng thái/Loại phiếu, Người tạo/Ngày tạo, Thông tin dự án, Đơn vị yêu cầu, Người tham gia, Nội dung chi tiết).
  * *Form Tạo/Sửa:* Gồm 5 nhóm Card (Thông tin cơ bản, Thông tin dự án, Đơn vị yêu cầu, Người tham gia, Nội dung chi tiết).

---

## 3. Vai trò & Phân quyền (Role-Based Access Control)

Hệ thống phân quyền dựa trên 3 nhóm quyền chính: `Managers`, `Technicians`, và `Customers`. Superuser được coi là thuộc nhóm Managers.

### Bảng ma trận phân quyền chi tiết (RBAC Matrix)

| Module | Hành động | Technician | Customer | Manager / Superuser |
|---|---|:---:|:---:|:---:|
| **Phiếu Yêu cầu** | Xem danh sách / Chi tiết | ✅ | ✅ (Chỉ các phiếu do mình tạo/yêu cầu) | ✅ |
| | Tạo phiếu mới | ❌ | ❌ | ✅ |
| | Chỉnh sửa phiếu | ❌ | ❌ | ✅ |
| | Xóa phiếu | ❌ | ❌ | ✅ |
| **Bài Thí nghiệm** | Xem danh sách bài test | ✅ | ❌ | ✅ |
| | Tạo mới / Sửa / Xóa bài test | ❌ | ❌ | ✅ |
| | Tải lên file Quy quy định (Method) | ✅ | ❌ | ✅ |
| | Tải lên file Kết quả (Result) | ❌ | ❌ | ✅ |
| | Phê duyệt bài test (Hoàn tất) | ❌ | ❌ | ✅ (Chỉ Reviewer được chỉ định) |
| **Hệ thống** | Quản trị User & Group | ❌ | ❌ | ✅ |

### Phân quyền tại tầng UI (Templates)
Hệ thống sử dụng context processor `core/context_processors.py` để tiêm hai biến boolean `is_manager` và `is_technician` vào tất cả các template:
* `is_manager = True` nếu user là superuser hoặc nằm trong group `Managers`.
* `is_technician = True` nếu user nằm trong group `Technicians` và **không phải** manager.

#### Các quy tắc ẩn/hiện trên giao diện:
1. **Sidebar (Hệ thống):** Mục "Người dùng" và "Nhóm" được bọc trong `{% if is_manager %}`.
2. **Dashboard & Danh sách Phiếu:** Nút "Tạo yêu cầu" bị ẩn đối với Technician.
3. **Detail Panel (Phiếu yêu cầu):**
   * Footer chứa các nút chỉnh sửa/xóa phiếu bị ẩn đối với Technician.
   * Nút "+ Thêm test" và các nút sửa/xóa bài test trong tab Bài test bị ẩn đối với Technician.
   * Giao diện tải file Kết quả (Result) của bài test bị ẩn đối với Technician (chỉ hiển thị link tải nếu đã có file).
4. **Trang Danh sách bài test (`/tests`):**
   * Technician không có nút Edit/Delete trên mỗi dòng lưới.
   * Icon thao tác của Technician được đổi sang dạng `eye` (Xem chi tiết). Khi bấm vào sẽ mở rộng hàng dưới dạng **Đọc (Read-only)**.
   * Trong expanded row của Technician: các trường dữ liệu hiển thị dạng text thuần không có thẻ input, nút "Lưu" bị ẩn, nút "Hủy" đổi tên thành "Đóng".

### Phân quyền tại tầng Backend (Defense in depth)
Để ngăn chặn việc bypass UI bằng cách gọi trực tiếp URL, hệ thống định nghĩa helper kiểm tra quyền truy cập:

```python
def not_technician(user):
    """Cho phép truy cập nếu user là superuser, Manager, hoặc không phải Technician."""
    if user.is_superuser or user.groups.filter(name="Managers").exists():
        return True
    return not user.groups.filter(name="Technicians").exists()
```

> [!WARNING]
> Helper này được định nghĩa trực tiếp trong các file `views.py` tương ứng (ví dụ: `lab_requests/views.py`, `material_tests/views.py`) thay vì file dùng chung nhằm hạn chế tối đa các dependency vòng chéo giữa các app nhỏ.

* **View CRUD Phiếu & Test:** Các view tạo/sửa/xóa phiếu và bài test đều được bảo vệ bằng `@user_passes_test(not_technician)` hoặc `@user_passes_test(is_manager)`.
### Thông tin cá nhân mở rộng (UserProfile)
Để hỗ trợ lưu trữ các thông tin mở rộng của người dùng (số điện thoại, địa chỉ, ảnh đại diện, phòng ban, chức vụ) mà không làm vỡ các migration sẵn có của Django, hệ thống triển khai mô hình `UserProfile` liên kết 1-1 với model `User` mặc định:
* **Model definition:** Định nghĩa trong `system_admin/models.py`.
* **Signals:** Đăng ký các signals `post_save` để tự động tạo `UserProfile` tương ứng khi một `User` mới được khởi tạo và tự động lưu profile khi lưu User:
  ```python
  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          UserProfile.objects.create(user=instance)
  ```
* **Form & View integration:** Các view `user_create` và `user_edit` xử lý đồng thời hai ModelForm: `UserForm` và `UserProfileForm`, hỗ trợ cập nhật ảnh đại diện (`avatar`) thông qua request `enctype="multipart/form-data"`.

### Trang danh sách Người dùng (`/users/`)
Trang hiển thị danh sách toàn bộ người dùng trong hệ thống với các tùy chọn lọc và hiển thị tối ưu:
* **Hiển thị Nhóm (Groups):** Thay vì cột "Lần đăng nhập cuối", hệ thống hiển thị danh sách các nhóm mà người dùng thuộc về dưới dạng huy hiệu (badge) màu sắc khác nhau để dễ nhận biết (Managers: `rose`, Technicians: `amber`, Customers: `blue`, Khác: `gray`). Tên các nhóm được tự động định dạng Title case (viết hoa chữ cái đầu).
* **Bộ lọc nhanh (Quick Filters):** Thiết lập thanh công cụ dạng Segmented Control cho phép lọc nhanh danh sách người dùng theo các nhóm ("Tất cả", "Khách hàng", "Kỹ thuật viên", "Quản lý").
* **Đồng bộ hóa HTMX:** Bộ lọc nhóm được đồng bộ hoàn toàn với ô tìm kiếm văn bản qua thuộc tính `hx-include`, gửi đồng thời cả hai tham số `q` và `group` lên server để thực hiện lọc kết hợp.
* **Tối ưu hóa hiệu năng:** Queryset người dùng ở backend sử dụng `prefetch_related("groups")` để nạp trước quan hệ nhóm, loại bỏ nguy cơ xảy ra lỗi N+1 truy vấn khi render bảng.

---

## 4. Các Luồng Nghiệp vụ Chính

### Luồng Phiếu Yêu cầu (Request)
* **Cấu trúc Dữ liệu:** Gồm các trường cơ bản (Title, Type, Created_by) và các trường thông tin mở rộng được lưu trữ dưới dạng JSON (`status`, `participants`, `project_info`, `request_unit`).
* **Form & Model property:** Model `Request` cung cấp các `@property` để giải nén (unpack) dữ liệu JSON phục vụ render trên template. `RequestForm` tự động xử lý gộp (pack) dữ liệu nhập vào thành chuỗi JSON trước khi lưu. Form tích hợp trực tiếp `x-model` của Alpine.js để thực hiện liên kết hai chiều mượt mà.
* **Người quản lý & Khách hàng:**
  * Trường `customer`: Khóa ngoại liên kết `User`, lọc chỉ hiển thị nhóm `Customers`.
  * Trường `manager`: Khóa ngoại liên kết `User`, lọc hiển thị nhóm `Managers` và `Technicians`. Mặc định khi tạo mới phiếu, trường này lấy giá trị người tạo phiếu.

### Luồng Bài Thí nghiệm (Material Test)
* **Liên kết:** Mỗi bài thí nghiệm `MaterialTest` thuộc về một `Request` thông qua khóa ngoại.
* **Vai trò:**
  * `tester`: Người thực hiện (lọc thuộc nhóm `Technicians`).
  * `reviewer`: Người kiểm tra/duyệt (lọc thuộc nhóm `Managers`).
* **Trạng thái & Nghiệp vụ phê duyệt:**
  * Trạng thái bài test gồm `in_progress` (Đang thực hiện) và `completed` (Hoàn tất).
  * **Quy tắc duyệt:** Chỉ người dùng được phân công làm `reviewer` cho bài test đó mới có quyền chuyển trạng thái sang `completed`.
  * Ràng buộc này được thực thi tại hàm `clean()` của `MaterialTestForm`:
    ```python
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        reviewer = cleaned_data.get("reviewer")
        # Kiểm tra xem user hiện tại có phải reviewer được chọn hay không khi hoàn tất bài test
        if status == "completed" and self.user != reviewer:
            self.add_error("status", "Chỉ người kiểm tra (Reviewer) được phân công mới có quyền hoàn tất bài test này.")
        return cleaned_data
    ```
* **Tải lên tài liệu:**
  * Mỗi bài test cần 2 file: File Quy định (Method) và file Kết quả (Result).
  * Việc tải file được thực hiện qua HTMX (`hx-encoding="multipart/form-data"`), tự động hoán đổi giao diện thành "Đã tải lên" sau khi upload thành công.
  * Trên trang `/tests`, Technician được phép tải lên/cập nhật trực tiếp file Method từ dòng dữ liệu trên bảng bằng một form ẩn kích hoạt khi chọn file, không cần mở panel chỉnh sửa. Giao diện hiển thị icon thông minh: `upload` khi chưa có file và `refresh-cw` khi đã có file.

### Luồng Nhiệm vụ cá nhân (User Tasks)
* **Mục tiêu:** Cho phép người dùng đăng nhập xem và quản lý các bài thí nghiệm được giao riêng cho mình làm Tester (`tester = request.user`).
* **Định tuyến & Views:**
  * URL: `/tasks/` (tên URL: `user_tasks`).
  * View: `user_tasks` trong `material_tests/views.py` thực hiện lọc các bài test theo `tester=request.user`, đồng thời hỗ trợ tìm kiếm từ khóa `q` và lọc trạng thái thông qua HTMX tương tự như trang danh sách chung.
* **Giao diện:**
  * Được tích hợp vào một nhóm menu Sidebar riêng biệt có tên **Cá nhân** (Personal) dưới nhãn **Nhiệm vụ của bạn** (sử dụng icon Lucide `check-square`). Nhóm này đóng vai trò là nơi lưu trữ các chức năng cá nhân sau này như Profile, Đổi mật khẩu.
  * Sử dụng template `templates/material_tests/user_tasks.html`.
  * Tái sử dụng partial `material_tests/partials/material_test_table_rows.html` và `material_test_row.html` để đảm bảo giao diện hiển thị đồng bộ và tối ưu dung lượng code.

---

## 5. Kỹ thuật Lập trình & Các mẫu xử lý lỗi (Patterns & Gotchas)

### 1. Ngăn chặn rò rỉ File vật lý khi xóa bản ghi (File Leak Prevention)
Mặc định, Django sẽ không tự động xóa file trên đĩa cứng khi bản ghi chứa trường `FileField` hoặc `ImageField` bị xóa. Để tránh rác bộ nhớ tại thư mục `media/tests/`, model `MaterialTest` ghi đè hàm `delete()` để chủ động xóa file vật lý:

```python
import os

def delete(self, *args, **kwargs):
    # Xóa file Method khỏi disk
    if self.method_file and os.path.isfile(self.method_file.path):
        os.remove(self.method_file.path)
    # Xóa file Result khỏi disk
    if self.result_file and os.path.isfile(self.result_file.path):
        os.remove(self.result_file.path)
    super().delete(*args, **kwargs)
```

> [!TIP]
> Việc override này cũng bảo vệ hệ thống khi xóa một `Request` cha, vì Django sẽ gọi phương thức `delete()` của từng `MaterialTest` con theo liên kết cascade.

### 2. Sửa lỗi 403 Forbidden đối với HTMX DELETE Request
HTMX mặc định không tự động đính kèm CSRF token khi gửi các request không qua thẻ `<form>` (như `hx-delete` trên các button).
**Giải pháp:** Đăng ký một global event listener trong block JavaScript của trang layout chính (`templates/partials/scripts.html` hoặc `base.html`):

```javascript
document.body.addEventListener('htmx:configRequest', function(evt) {
    evt.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});
```

Đoạn code trên đảm bảo mọi request phát đi từ HTMX (DELETE, PUT, PATCH...) đều được đính kèm Header `X-CSRFToken` hợp lệ, giúp vượt qua lớp bảo vệ CSRF của Django.

### 3. Tránh xuống dòng cho các huy hiệu trạng thái (Status Badges)
Khi độ rộng của cột bảng bị thu nhỏ, chữ trong các huy hiệu (pill badges) có thể bị vỡ và tự động xuống dòng gây mất thẩm mỹ.
**Giải pháp:**
* Thêm class `max-w-full` và `flex-shrink-0` cho icon/chấm tròn trạng thái để tránh bị bóp méo.
* Bọc phần text trạng thái trong một thẻ `<span>` có class `truncate` để tự động thu gọn bằng dấu `...` thay vì xuống dòng.
* Thêm thuộc tính `title="[Trạng thái đầy đủ]"` để hiển thị tooltip khi người dùng hover qua.

```html
<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-100 max-w-full">
  <span class="w-1.5 h-1.5 rounded-full bg-amber-400 inline-block flex-shrink-0"></span>
  <span class="truncate" title="Đang thực hiện">Đang thực hiện</span>
</span>
```

---

## 6. Quy trình chạy Migrations & Quản trị Database (Docker environment)

Do dự án được cấu hình chạy khép kín bên trong các container Docker (sử dụng Docker Compose), các lệnh quản trị Django (như `makemigrations`, `migrate`, `createsuperuser`) phải được thực thi trực tiếp từ bên trong container `web`:

### 1. Tạo file migration cho một app cụ thể
Khi tạo mới hoặc chỉnh sửa model trong app (ví dụ `system_admin`), chạy lệnh sau để Django tạo file migration:
```bash
docker compose exec web python manage.py makemigrations [tên_app]
```

### 2. Áp dụng các thay đổi vào Database
Để chạy các migrations chưa được áp dụng vào MariaDB:
```bash
docker compose exec web python manage.py migrate
```

### 3. Tạo tài khoản quản trị (Superuser)
```bash
docker compose exec web python manage.py createsuperuser
```
