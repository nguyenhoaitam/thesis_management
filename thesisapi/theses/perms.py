from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    message = "Bạn không có quyền truy cập tài nguyên này!"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_authenticated


class IsAdmin(BasePermission):
    message = "Bạn không có quyền truy cập tài nguyên này!"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_authenticated and request.user.role.role_code == 'admin'


class IsMinistry(BasePermission):
    message = "Bạn không có quyền truy cập tài nguyên này!"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_authenticated and request.user.role.role_code == 'ministry'


class IsLecturer(BasePermission):
    message = "Bạn không có quyền truy cập tài nguyên này!"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_authenticated and request.user.role.role_code == 'lecturer'


class IsStudent(BasePermission):
    message = "Bạn không có quyền truy cập tài nguyên này!"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_authenticated and request.user.role.role_code == 'student'


class CommentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return super().has_permission(request, view) and request.user == comment.user


class PostOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, post):
        return super().has_permission(request, view) and request.user == post.user
