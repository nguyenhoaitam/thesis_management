from rest_framework import serializers
from theses.models import *


# Vai trò (Quản lý trong Admin)


# Người dùng
class UserSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    lecturer = serializers.SerializerMethodField()
    ministry = serializers.SerializerMethodField()

    # Lấy thông tin của sinh viên, giảng viên, giáo vụ nếu có liên kết với user thì hiện ra
    def get_student(self, obj):
        try:
            student = Student.objects.get(user=obj)
            return StudentSerializer(student).data
        except Student.DoesNotExist:
            return None

    def get_lecturer(self, obj):
        try:
            lecturer = Lecturer.objects.get(user=obj)
            return LecturerSerializer(lecturer).data
        except Lecturer.DoesNotExist:
            return None

    def get_ministry(self, obj):
        try:
            ministry = Ministry.objects.get(user=obj)
            return MinistrySerializer(ministry).data
        except Ministry.DoesNotExist:
            return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['role'] = instance.role.name if instance.role else None

        avatar = getattr(instance, 'avatar', None)
        if avatar:
            rep['avatar'] = instance.avatar.url

        # Loại bỏ trường student, lecturer, ministry nếu không tồn tại
        if rep.get('student') is None:
            rep.pop('student')

        if rep.get('lecturer') is None:
            rep.pop('lecturer')

        if rep.get('ministry') is None:
            rep.pop('ministry')

        return rep

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'email', 'phone', 'gender', 'avatar', 'role', 'student', 'lecturer', 'ministry']

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


# Giáo vụ
class MinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministry
        fields = ['code', 'full_name', 'birthday', 'address', 'user']


# Vị trí
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


# Năm học
class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = '__all__'


# Khoa
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['code', 'name']


# Ngành
class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['code', 'name', 'faculty']

    # Trả về tên khoa khi GET
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['faculty'] = instance.faculty.name if instance.faculty else None
        return rep


# Giảng viên
class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['code', 'full_name', 'birthday', 'address', 'faculty']

    # Trả về tên khoa khi GET
    def to_representation(self, instance): # to_representation được ghi đè để thay đổi cách hiển thị
        rep = super().to_representation(instance)
        rep['faculty'] = instance.faculty.name if instance.faculty else None
        return rep


# Sinh viên
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['code', 'full_name', 'birthday', 'address', 'gpa', 'user', 'major']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['major'] = instance.major.name if instance.major else None
        return rep


# Hội đồng
class CouncilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Council
        fields = ['id', 'name', 'description', 'is_lock']


# Chi tiết hội đồng
class CouncilDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncilDetail
        fields = ['id', 'lecturer', 'council', 'position']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['lecturer'] = instance.lecturer.full_name if instance.lecturer else None
        rep['council'] = instance.council.name if instance.council else None
        rep['position'] = instance.position.name if instance.position else None
        return rep


# Khóa luận
class ThesisSerializer(serializers.ModelSerializer):
    lecturers = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()

    def get_lecturers(self, obj):
        lecturers_queryset = obj.lecturers.all()
        return LecturerSerializer(lecturers_queryset, many=True).data

    def get_reviewer(self, obj):
        if obj.council:
            reviewer_detail = obj.council.councildetail_set.filter(position__name='Phản biện').first()
            if reviewer_detail:
                return LecturerSerializer(reviewer_detail.lecturer).data
        return None

    class Meta:
        model = Thesis
        fields = ['code', 'name', 'start_date', 'end_date', 'report_file',
                  'total_score', 'result', 'council', 'major',
                  'school_year', 'student', 'lecturers', 'reviewer']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['council'] = instance.council.name if instance.council else None
        rep['major'] = instance.major.name if instance.major else None
        rep['school_year'] = instance.school_year.name if instance.school_year else None
        rep['student'] = instance.student.full_name if instance.student else None
        return rep


# Điểm
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'


# Cột điểm
class ScoreColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreColumn
        fields = '__all__'


# Điểm thành phần
class ScoreComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreComponent
        fields = '__all__'


# Chi tiết điểm
class ScoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreDetail
        fields = '__all__'
