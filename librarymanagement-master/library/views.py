from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date, timedelta, datetime
from django.core.mail import send_mail
from librarymanagement.settings import EMAIL_HOST_USER


# ==========================================
# CÁC VIEW CƠ BẢN (TRANG CHỦ, LOGIN, SIGNUP)
# ==========================================

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/index.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/studentclick.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/adminclick.html')


def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            # Tự động thêm user vào nhóm STUDENT
            my_student_group, created = Group.objects.get_or_create(name='STUDENT')
            my_student_group.user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request, 'library/studentsignup.html', context=mydict)


# ==========================================
# KIỂM TRA QUYỀN TRUY CẬP (DECORATORS)
# ==========================================

def is_admin(user):
    return user.is_superuser or user.is_staff


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')
    elif is_student(request.user):
        return render(request, 'library/studentafterlogin.html')
    else:
        return render(request, 'library/index.html')


# ==========================================
# CHỨC NĂNG ADMIN (QUẢN LÝ SÁCH, SINH VIÊN)
# ==========================================

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'library/bookadded.html')
    return render(request, 'library/addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books = models.Book.objects.all()
    return render(request, 'library/viewbook.html', {'books': books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            # Lấy đối tượng từ form đã cleaned (để tránh lỗi object ID)
            selected_book = form.cleaned_data['isbn2']
            selected_student = form.cleaned_data['enrollment2']

            obj = models.IssuedBook()
            obj.isbn = selected_book.isbn
            obj.enrollment = selected_student.enrollment
            obj.save()
            return render(request, 'library/bookissued.html')

    return render(request, 'library/issuebook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    issued_data = []

    for ib in issuedbooks:
        # Format ngày tháng
        issdate = str(ib.issuedate.day) + '-' + str(ib.issuedate.month) + '-' + str(ib.issuedate.year)
        expdate = str(ib.expirydate.day) + '-' + str(ib.expirydate.month) + '-' + str(ib.expirydate.year)

        # Tính phạt
        days = (date.today() - ib.issuedate)
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = day * 10

        # Lấy thông tin sách và sinh viên
        device = models.Book.objects.filter(isbn=ib.isbn).first()
        student = models.StudentExtra.objects.filter(enrollment=ib.enrollment).first()

        if device and student:
            item = {
                'student_name': student.get_name,
                'enrollment': student.enrollment,
                'book_name': device.name,
                'author': device.author,
                'issued_date': issdate,
                'expiry_date': expdate,
                'fine': fine,
                'status': ib.status,
                'id': ib.id # <--- QUAN TRỌNG: Cần ID để tạo nút bấm trả
            }
            issued_data.append(item)

    # Truyền sang HTML bằng biến 'issued_data' (dạng Dictionary dễ dùng)
    return render(request, 'library/viewissuedbook.html', {'issued_data': issued_data})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'library/viewstudent.html', {'students': students})


# ==========================================
# CHỨC NĂNG SINH VIÊN (QUAN TRỌNG: ĐÃ SỬA GỘP LIST)
# ==========================================

@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id).first()
    if not student:
        return render(request, 'library/index.html')

    issuedbook = models.IssuedBook.objects.filter(enrollment=student.enrollment)

    # Dùng 1 list chứa dictionary thay vì 2 list rời rạc
    issued_data = []

    for ib in issuedbook:
        device = models.Book.objects.filter(isbn=ib.isbn).first()

        if device:
            # Format ngày
            issdate = str(ib.issuedate.day) + '-' + str(ib.issuedate.month) + '-' + str(ib.issuedate.year)
            expdate = str(ib.expirydate.day) + '-' + str(ib.expirydate.month) + '-' + str(ib.expirydate.year)

            # Tính phạt
            days = (date.today() - ib.issuedate)
            d = days.days
            fine = 0
            if d > 15:
                day = d - 15
                fine = day * 10

            # Tạo dictionary chứa full thông tin
            item = {
                'book_name': device.name,
                'author': device.author,
                'issue_date': issdate,
                'expiry_date': expdate,
                'fine': fine,
                'status': ib.status,
                'branch': student.branch,
                'enrollment': student.enrollment,
                'id': ib.id  # Cần ID để làm nút Trả sách
            }
            issued_data.append(item)

    # Truyền sang HTML bằng biến 'issued_data'
    return render(request, 'library/viewissuedbookbystudent.html', {'issued_data': issued_data})


def returnbook(request, id):
    try:
        issued_book = models.IssuedBook.objects.get(pk=id)
        issued_book.status = "Returned"
        issued_book.save()
    except models.IssuedBook.DoesNotExist:
        pass

    # KIỂM TRA NGƯỜI DÙNG LÀ AI ĐỂ CHUYỂN HƯỚNG ĐÚNG
    if request.user.is_superuser or request.user.is_staff:
        # Nếu là Admin -> Quay về trang quản lý mượn trả của Admin
        return redirect('viewissuedbook')
    else:
        # Nếu là Sinh viên -> Quay về trang thiết bị cá nhân
        return redirect('viewissuedbookbystudent')


# ==========================================
# CÁC TRANG PHỤ
# ==========================================

def aboutus_view(request):
    return render(request, 'library/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']

            try:
                send_mail(str(name) + ' || ' + str(email), message, EMAIL_HOST_USER, ['wapka1503@gmail.com'],
                          fail_silently=False)
            except Exception as e:
                print(f"Lỗi gửi mail: {e}")

            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form': sub})


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect('/')