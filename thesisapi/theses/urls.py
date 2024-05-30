from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from theses import views

r = routers.DefaultRouter()

# Vai trò (Quản lý trong Admin)
r.register('users', views.UserViewSet, 'users')  # Người dùng
# Giáo vụ
r.register('positions', views.PositionViewSet, 'positions')  # Vị trí
r.register('school_years', views.SchoolYearViewSet, 'school_years')  # Năm học
r.register('faculties', views.FacultyViewSet, 'faculties')  # Khoa
r.register('majors', views.MajorViewSet, 'majors')  # Ngành
r.register('lecturers', views.LecturerViewSet, 'lecturers')  # Giảng viên
r.register('students', views.StudentViewSet, 'students')  # Sinh viên
r.register('councils', views.CouncilViewSet, 'councils')  # Hội đồng
r.register('council_details', views.CouncilDetailViewSet, 'council_details')  # Chi tiết hội đồng
r.register('theses', views.ThesisViewSet, 'theses')  # Khóa luận
r.register('score', views.ScoreViewSet, 'scores')  # Điểm
r.register('criterias', views.CriteriaViewSet, 'criterias')  # Tiêu chí
r.register('thesiscriterias', views.ThesisCriteriaViewSet, 'thesiscriterias')  # Tiêu chí của khóa luận
r.register('posts', views.PostViewSet, 'posts')  # Bài đăng
r.register('comments', views.CommentViewSet, 'comments')  # Bình luận

urlpatterns = [
    path('', include(r.urls)),
]
