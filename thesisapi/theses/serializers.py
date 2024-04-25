from rest_framework import serializers
from theses.models import *


# Vai trò
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


# Người dùng
class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        req = super().to_representation(instance)
        avatar = getattr(instance, 'avatar', None)
        if avatar:
            req['avatar'] = instance.avatar.url
        return req  # Trả về đường dẫn ảnh đầy đủ

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'email', 'phone', 'gender', 'avatar', 'role']

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


# Giáo vụ

# Thông báo

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
        fields = ['fac_code', 'name']


# Ngành
class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['maj_code', 'name', 'faculty_name']


# Giảng viên
class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['lec_code', 'full_name', 'birthday', 'address', 'user', 'faculty_name']


# Sinh viên
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['stu_code', 'full_name', 'birthday', 'address', 'gpa', 'user', 'major']


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
        fields = ['the_code', 'name', 'start_date', 'end_date', 'report_file',
                  'total_score', 'result', 'council', 'major', 'school_year', 'students']


# Điểm

# Cột điểm

# Điểm thành phần

# Chi tiết điểm
