from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from theses import views

r = routers.DefaultRouter()
# Vai trò
r.register('roles', views.RoleViewSet, 'roles')

# Người dùng
r.register('users', views.UserViewSet, 'users')

# Giáo vụ

# Thông báo

# Vị trí
r.register('positions', views.PositionViewSet, 'positions')

# Năm học
r.register('school_years', views.SchoolYearViewSet, 'school_years')

# Khoa
r.register('faculties', views.FacultyViewSet, 'faculties')

# Ngành
r.register('majors', views.MajorViewSet, 'majors')

# Giảng viên
r.register('lecturers', views.LecturerViewSet, 'lecturers')

# Sinh viên
r.register('students', views.StudentViewSet, 'students')

# Hội đồng
r.register('councils', views.CouncilViewSet, 'councils')

# Chi tiết hội đồng
r.register('council_details', views.CouncilDetailViewSet, 'council_details')

# Khóa luận
r.register('theses', views.ThesisViewSet, 'theses')

# Giảng viên hướng dẫn khóa luận

# Điểm

# Cột điểm

# Điểm thành phần

# Chi tiết điểm

urlpatterns = [
    path('', include(r.urls)),
]
