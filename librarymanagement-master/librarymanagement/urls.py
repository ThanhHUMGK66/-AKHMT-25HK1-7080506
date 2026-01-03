"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),

    # path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.studentsignup_view),

    # --- ĐOẠN ĐÃ SỬA: THÊM name='...' (QUAN TRỌNG) ---
    # Phải có name='adminlogin' thì hệ thống mới biết đường chuyển hướng khi chưa đăng nhập
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html'), name='adminlogin'),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html'), name='studentlogin'),
    # --------------------------------------------------

    path('returnbook/<int:id>/', views.returnbook, name='returnbook'),

    # Đường dẫn đăng xuất (đã fix lỗi 405 ở bước trước)
    path('logout', views.logout_user, name='logout'),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),

    path('addbook', views.addbook_view),
    path('viewbook', views.viewbook_view),
    path('issuebook', views.issuebook_view),
    path('viewissuedbook', views.viewissuedbook_view, name='viewissuedbook'),
    path('viewstudent', views.viewstudent_view),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent, name='viewissuedbookbystudent'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
]