from django import forms
from django.contrib.auth.models import User
from . import models

# --- FORM LIÊN HỆ ---
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30, label='Họ Tên')
    Email = forms.EmailField(label='Email')
    Message = forms.CharField(max_length=500, label='Nội dung', widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

# --- FORM USER ---
class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        labels = {'first_name': 'Tên', 'last_name': 'Họ', 'username': 'Tên đăng nhập', 'password': 'Mật khẩu'}

# --- FORM SINH VIÊN ---
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra
        fields = ['enrollment', 'branch']
        labels = {'enrollment': 'Mã số sinh viên (MSSV)', 'branch': 'Ngành học'}

# --- FORM SÁCH/THIẾT BỊ ---
class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['name', 'isbn', 'author', 'category']
        labels = {
            'name': 'Tên Thiết Bị',
            'isbn': 'Mã Tài Sản (Asset ID)',
            'author': 'Hãng SX / Cấu Hình',
            'category': 'Loại Thiết Bị',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Dell Vostro 3500'}),
            'isbn': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: 111'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Core i5, RAM 8GB'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

# --- FORM CẤP PHÁT (ĐÃ FIX LỖI CRASH) ---
class IssuedBookForm(forms.Form):
    # 1. Chọn Thiết Bị (Bỏ to_field_name để dùng ID mặc định)
    isbn2 = forms.ModelChoiceField(
        queryset=models.Book.objects.all(),
        empty_label="-- Chọn thiết bị trong kho --",
        label='Chọn Thiết Bị',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # 2. Chọn Sinh Viên
    enrollment2 = forms.ModelChoiceField(
        queryset=models.StudentExtra.objects.all(),
        empty_label="-- Chọn sinh viên --",
        label='Sinh Viên Mượn',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Tùy chỉnh hiển thị trong danh sách chọn: "Tên [Mã]"
    def __init__(self, *args, **kwargs):
        super(IssuedBookForm, self).__init__(*args, **kwargs)
        self.fields['isbn2'].label_from_instance = lambda obj: f"{obj.name} [Mã: {obj.isbn}] - {obj.author}"
        self.fields['enrollment2'].label_from_instance = lambda obj: f"{obj.user.first_name} [MSSV: {obj.enrollment}]"