from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from theses.models import Role, User, Ministry, Notify, Position, SchoolYear, Faculty, Major, \
    Lecturer, Student, Council, CouncilDetail, Thesis, Instructor, Score, ScoreComponent, ScoreColumn, ScoreDetail


class MyRoleAdmin(admin.ModelAdmin):
    list_display = ['role_code', 'name']


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email',
                    'avatar', 'phone', 'gender', 'role_name', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['gender', 'role_id']
    readonly_fields = ['my_avatar']

    def my_avatar(self, user):  # Xem lại đường dẫn
        if user.avatar:
            return mark_safe(f"<img src='/static/{user.avatar.name}' width='200' />")


class MyMinistryAdmin(admin.ModelAdmin):
    pass


class NotifyForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Notify
        fields = '__all__'


class MyNotifyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'title', 'content', 'created_date', 'active']
    search_fields = ['title', 'content']
    form = NotifyForm


class MyPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class MySchoolYearAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_year', 'end_year']
    search_fields = ['name']


class MyFacultyAdmin(admin.ModelAdmin):
    list_display = ['fac_code', 'name']
    search_fields = ['fac_code', 'name']


class MyMajorAdmin(admin.ModelAdmin):
    list_display = ['maj_code', 'name', 'faculty_name']
    search_fields = ['maj_code', 'name']
    list_filter = ['faculty']


class MyLecturerAdmin(admin.ModelAdmin):
    list_display = ['lec_code', 'full_name', 'birthday', 'address', 'faculty_name', 'user_id']
    search_fields = ['lec_code', 'full_name']
    list_filter = ['faculty']


class MyStudentAdmin(admin.ModelAdmin):
    list_display = ['stu_code', 'full_name', 'birthday', 'address', 'gpa', 'user_id', 'major_name']
    search_fields = ['stu_code', 'full_name']
    list_filter = ['major']


class MyCouncilAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_lock']
    search_fields = ['name']


class MyCouncilDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'lecturer_id', 'council_id', 'position_id']


class MyThesisAdmin(admin.ModelAdmin):
    list_display = ['the_code', 'name', 'start_date', 'end_date', 'total_score', 'result', 'major_name']
    search_fields = ['name', 'major_name']
    list_filter = ['major', 'school_year']


class MyInstructorAdmin():
    pass


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
admin.site.register(Ministry)
admin.site.register(Notify, MyNotifyAdmin)
admin.site.register(Position, MyPositionAdmin)
admin.site.register(SchoolYear, MySchoolYearAdmin)
admin.site.register(Faculty, MyFacultyAdmin)
admin.site.register(Major, MyMajorAdmin)
admin.site.register(Lecturer, MyLecturerAdmin)
admin.site.register(Student, MyStudentAdmin)
admin.site.register(Council, MyCouncilAdmin)
admin.site.register(CouncilDetail)
admin.site.register(Thesis, MyThesisAdmin)
admin.site.register(Instructor)
admin.site.register(Score)
admin.site.register(ScoreComponent, MyScoreComponentAdmin)
admin.site.register(ScoreColumn, MyScoreColumnAdmin)
admin.site.register(ScoreDetail, MyScoreDetailAdmin)