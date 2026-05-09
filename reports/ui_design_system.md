# MT-LIMS Design System & UI Documentation

Báo cáo này ghi nhận các thông số kỹ thuật và phong cách thiết kế đã được áp dụng sau khi hiện đại hóa giao diện theo phong cách **Twenty CRM**.

## 1. Nguyên tắc cốt lõi (Design Principles)
- **Compact & Dense**: Tối ưu hóa không gian hiển thị, giảm khoảng trắng thừa để tập trung vào dữ liệu.
- **Premium Aesthetics**: Sử dụng các hiệu ứng hiện đại như `backdrop-blur` (glassmorphism), `shadow-sm`, và border mượt mà (`rounded-xl` / `rounded-2xl`).
- **Typography Focus**: Sử dụng font chữ Inter với các kích thước nhỏ nhưng đậm nét (bold) để tạo sự chuyên nghiệp.

## 2. Thông số kỹ thuật UI (UI Tokens)

### Màu sắc (Colors)
- **Sidebar Background**: `#fafafa` (Xám cực nhạt)
- **Primary Indigo**: `indigo-500` / `indigo-600` (Màu nhấn chủ đạo)
- **Text Primary**: `gray-900` (Đen xám đậm)
- **Text Secondary**: `gray-400` / `gray-500` (Xám nhạt cho metadata)
- **Borders**: `gray-50` / `gray-100` (Đường kẻ cực mảnh)

### Kích thước (Dimensions)
- **Sidebar Width**: 220px (Expanded) / 64px (Collapsed)
- **Topbar Height**: 48px (h-12)
- **Border Radius**: 
  - Thẻ thống kê: `rounded-xl` (12px)
  - Card lớn/Form: `rounded-2xl` (16px)
  - Nút bấm/Input: `rounded-lg` / `rounded-xl`

### Font Size (Typography)
- **Tiêu đề chính**: `text-lg` (18px), font-bold.
- **Nội dung bảng**: `text-[13px]`, font-bold (Tiêu đề) và font-medium (Nội dung).
- **Labels / Metadata**: `text-[9px]` - `text-[11px]`, font-bold, uppercase, tracking-widest.

## 3. Thành phần chính (Core Components)

### Sidebar
- **Workspace Switcher**: Thiết kế dạng nút bấm nổi bật trên cùng.
- **Nav Items**: Icon Lucide (size 3.5), font-medium, padding gọn gàng.
- **Group Labels**: Phân nhóm bằng đường kẻ mảnh hoặc text nhỏ.

### Topbar
- **Hiệu ứng**: `sticky`, `backdrop-blur-md`, `bg-white/80`.
- **Breadcrumbs**: Sử dụng font `[11px]` font-semibold, phân tách bằng icon chevron nhỏ.

### Data Table (Request List)
- **Badges**: Dạng Pill (bo tròn hoàn toàn), background nhạt, text đậm, có chấm màu biểu thị trạng thái.
- **Rows**: Hover highlight màu `indigo-50/30`, khoảng cách dòng hẹp.

### Detail Panel
- Chiều rộng: 380px.
- Hiệu ứng: Trượt từ phải sang (slide-in) với shadow lớn.
- Bố cục: Thông tin tóm tắt phía trên, nội dung chi tiết phía dưới trong box màu nhạt.

## 4. Công nghệ sử dụng
- **Tailwind CSS**: Utility-first styling.
- **Lucide Icons**: Bộ icon nhất quán.
- **Alpine.js**: Xử lý logic đóng/mở Sidebar, Topbar, Detail Panel và Filter.
- **Inter Font**: Font chữ hiện đại qua Google Fonts.
