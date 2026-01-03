from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# =========================================================
# 1. MODEL SINH VIÊN MỞ RỘNG (Liên kết với User)
# =========================================================
class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40, verbose_name="Mã Số Sinh Viên (MSSV)")
    branch = models.CharField(max_length=40, verbose_name="Ngành Học")

    def __str__(self):
        return self.user.first_name + ' [' + str(self.enrollment) + ']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id

    class Meta:
        verbose_name = "Sinh Viên"
        verbose_name_plural = "Danh Sách Sinh Viên"


# =========================================================
# 2. MODEL THIẾT BỊ / SÁCH (Kho chứa)
# =========================================================
class Book(models.Model):
    # Danh mục thiết bị IT phòng Lab
    catchoice = [
        ('pc_laptop', 'Máy tính (PC/Laptop)'),
        ('network', 'Thiết bị mạng (Router/Switch)'),
        ('peripheral', 'Thiết bị ngoại vi (Phím/Chuột/Màn)'),
        ('component', 'Linh kiện điện tử'),
        ('furniture', 'Nội thất / Khác'),
    ]

    # Giữ nguyên tên biến (name, isbn, author) để code cũ không bị lỗi
    # Nhưng sửa 'verbose_name' để hiển thị Tiếng Việt trong Admin
    name = models.CharField(max_length=30, verbose_name="Tên Thiết Bị")
    isbn = models.PositiveIntegerField(verbose_name="Mã Tài Sản (Asset ID)")
    author = models.CharField(max_length=40, verbose_name="Hãng SX / Cấu Hình")
    category = models.CharField(max_length=30, choices=catchoice, default='pc_laptop', verbose_name="Loại Thiết Bị")

    def __str__(self):
        return str(self.name) + " [" + str(self.isbn) + ']'

    class Meta:
        verbose_name = "Thiết Bị"
        verbose_name_plural = "Kho Thiết Bị"


# =========================================================
# 3. MODEL PHIẾU MƯỢN (Quản lý cấp phát)
# =========================================================
def get_expiry():
    # Mặc định mượn 15 ngày
    return datetime.today() + timedelta(days=5)


class IssuedBook(models.Model):
    # Lưu MSSV và Mã thiết bị dưới dạng Text để tra cứu
    enrollment = models.CharField(max_length=30, verbose_name="MSSV Người Mượn")
    isbn = models.CharField(max_length=30, verbose_name="Mã Tài Sản")

    issuedate = models.DateField(auto_now=True, verbose_name="Ngày Cấp")
    expirydate = models.DateField(default=get_expiry, verbose_name="Hạn Trả")

    statuschoice = [
        ('Issued', 'Đang mượn'),
        ('Returned', 'Đã trả'),
    ]
    status = models.CharField(max_length=20, choices=statuschoice, default="Issued", verbose_name="Trạng Thái")

    def __str__(self):
        return f"Phiếu mượn: {self.enrollment} - {self.isbn}"

    class Meta:
        verbose_name = "Phiếu Mượn"
        verbose_name_plural = "Danh Sách Mượn Trả"