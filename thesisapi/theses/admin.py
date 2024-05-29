from cloudinary.templatetags import cloudinary
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from theses.models import Role, User, Ministry, Position, SchoolYear, Faculty, Major, \
    Lecturer, Student, Council, CouncilDetail, Thesis, Score, ScoreComponent, ScoreColumn, ScoreDetail


class MyRoleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'gender', 'role']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['gender', 'role']
    readonly_fields = ['user_avatar']

    # Băm mật khẩu khi tạo bằng admin
    def save_model(self, request, obj, form, change):
        if not change:
            # Nếu đây là việc tạo mới người dùng
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

    def user_avatar(self, user):
        if user.avatar:
            if type(user.avatar) is cloudinary.CloudinaryResource:
                return mark_safe(f"<img width='100' src='{user.avatar.url}' />")
            return mark_safe(f"<img width='100' src='/static/{user.avatar.name}' />")
        else:
            return "No avatar"


class MyMinistryAdmin(admin.ModelAdmin):
    list_display = ['code', 'full_name', 'birthday', 'address', 'user']


class MyPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class MySchoolYearAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_year', 'end_year']
    search_fields = ['name']


class MyFacultyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']


class MyMajorAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'faculty']
    search_fields = ['code', 'name']
    list_filter = ['faculty']


class MyLecturerAdmin(admin.ModelAdmin):
    list_display = ['code', 'full_name', 'birthday', 'address', 'faculty', 'user_id']
    search_fields = ['code', 'full_name']
    list_filter = ['faculty']


class MyStudentAdmin(admin.ModelAdmin):
    list_display = ['code', 'full_name', 'birthday', 'address', 'gpa', 'user_id', 'major', 'thesis']
    search_fields = ['code', 'full_name']
    list_filter = ['major']


class MyCouncilAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_lock']
    search_fields = ['name']
    list_filter = ['is_lock']


class MyCouncilDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'lecturer', 'council', 'position']
    list_filter = ['council']


class MyThesisAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'start_date', 'end_date', 'total_score', 'result', 'major', 'council']
    search_fields = ['name', 'major']
    list_filter = ['major', 'school_year']


class MyScoreAdmin(admin.ModelAdmin):
    pass


class MyScoreComponentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'evaluation_method']
    search_fields = ['name']


class MyScoreColumnAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'weight', 'score_component_id']
    search_fields = ['name']
    list_filter = ['score_component_id']


class MyScoreDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'score_number', 'score_id', 'score_column_id']
    list_filter = ['score_id', 'score_column_id']


admin.site.register(Role, MyRoleAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(Ministry, MyMinistryAdmin)
admin.site.register(Position, MyPositionAdmin)
admin.site.register(SchoolYear, MySchoolYearAdmin)
admin.site.register(Faculty, MyFacultyAdmin)
admin.site.register(Major, MyMajorAdmin)
admin.site.register(Lecturer, MyLecturerAdmin)
admin.site.register(Student, MyStudentAdmin)
admin.site.register(Council, MyCouncilAdmin)
admin.site.register(CouncilDetail, MyCouncilDetailAdmin)
admin.site.register(Thesis, MyThesisAdmin)
admin.site.register(Score)
admin.site.register(ScoreComponent, MyScoreComponentAdmin)
admin.site.register(ScoreColumn, MyScoreColumnAdmin)
admin.site.register(ScoreDetail, MyScoreDetailAdmin)
