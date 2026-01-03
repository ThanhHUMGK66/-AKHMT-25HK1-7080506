from django.contrib import admin
from .models import Book, StudentExtra, IssuedBook

# ==============================================================================
# 1. TÙY CHỈNH THƯƠNG HIỆU (BRANDING)
# ==============================================================================
admin.site.site_header = "Hệ Thống Quản Trị LabTrack"  # Tiêu đề lớn ở trang đăng nhập
admin.site.site_title = "LabTrack Admin"  # Tiêu đề tab trình duyệt
admin.site.index_title = "Trung Tâm Điều Khiển"  # Dòng chào mừng trang chủ


# ==============================================================================
# 2. CẤU HÌNH HIỂN THỊ CHO TỪNG BẢNG DỮ LIỆU
# ==============================================================================

class BookAdmin(admin.ModelAdmin):
    # Hiển thị các cột này ra ngoài bảng thay vì "Book object"
    list_display = ('name', 'isbn', 'author', 'category')

    # Thanh tìm kiếm (Tìm theo Tên, Mã, Hãng SX)
    search_fields = ('name', 'isbn', 'author')

    # Bộ lọc bên tay phải (Lọc theo loại thiết bị)
    list_filter = ('category',)

    # Số dòng mỗi trang
    list_per_page = 20


class StudentExtraAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'enrollment', 'branch')
    search_fields = ('enrollment', 'user__first_name', 'user__last_name')
    list_filter = ('branch',)

    # Hàm lấy họ tên từ bảng User liên kết
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_full_name.short_description = 'Họ và Tên'


class IssuedBookAdmin(admin.ModelAdmin):
    # Hiển thị chi tiết phiếu mượn
    list_display = ('isbn', 'enrollment', 'issuedate', 'expirydate', 'status')

    # Tìm kiếm theo Mã sách hoặc MSSV
    search_fields = ('isbn', 'enrollment')

    # CỰC QUAN TRỌNG: Lọc theo Trạng thái (để tìm ai chưa trả sách) và Ngày mượn
    list_filter = ('status', 'issuedate', 'expirydate')

    # Cho phép sửa trạng thái (Returned/Issued) ngay ở danh sách bên ngoài
    list_editable = ('status',)


# ==============================================================================
# 3. ĐĂNG KÝ MODEL
# ==============================================================================
admin.site.register(Book, BookAdmin)
admin.site.register(StudentExtra, StudentExtraAdmin)
admin.site.register(IssuedBook, IssuedBookAdmin)