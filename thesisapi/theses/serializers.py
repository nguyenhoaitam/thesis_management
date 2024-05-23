from rest_framework import serializers
from theses.models import *


# Vai trò
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


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
        req = super().to_representation(instance)

        avatar = getattr(instance, 'avatar', None)
        if avatar:
            req['avatar'] = instance.avatar.url

        # Loại bỏ trường student, lecturer, ministry nếu không tồn tại
        if req.get('student') is None:
            req.pop('student')

        if req.get('lecturer') is None:
            req.pop('lecturer')

        if req.get('ministry') is None:
            req.pop('ministry')

        return req

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
        fields = ['code', 'name', 'faculty_name']


# Giảng viên
class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['code', 'full_name', 'birthday', 'address', 'user', 'faculty_name']


# Sinh viên
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['code', 'full_name', 'birthday', 'address', 'gpa', 'user', 'major']


# Hội đồng
class CouncilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Council
        fields = '__all__'


# Chi tiết hội đồng
class CouncilDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncilDetail
        fields = '__all__'


# Khóa luận
class ThesisSerializer(serializers.ModelSerializer):
    # major = MajorSerializer()
    class Meta:
        model = Thesis
        fields = ['code', 'name', 'start_date', 'end_date', 'report_file',
                  'total_score', 'result', 'council', 'major', 'school_year', 'students']


# Giảng viên hướng dẫn khóa luận
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'

# Điểm

# Cột điểm

# Điểm thành phần

# Chi tiết điểm
