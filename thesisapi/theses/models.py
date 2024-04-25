from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Role(models.Model):  # Vai trò (Quản trị viên, Giáo vụ, Giảng viên, Sinh viên)
    role_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.name


class User(AbstractUser):  # Người dùng
    Gender_choice = [
        ('male', 'Nam'),
        ('female', 'Nữ')
    ]
    avatar = CloudinaryField(default='https://res.cloudinary.com/dkmurrwq5/image/upload/v1713421473/user.png')
    phone = models.CharField(max_length=10, null=False)
    gender = models.CharField(max_length=10, null=False, choices=Gender_choice)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def has_role(self, required_role):  # Hàm kiểm tra quyền của User
        return self.role == required_role

    def role_name(self):
        return self.role.name if self.role else None

    def save(self, *args, **kwargs):  # Hàm này có thể dùng để viết thay đổi mật khẩu
        if not self.pk and self.is_superuser:  # Kiểm tra nếu là superuser thì gán role admin
            self.role = Role.objects.get(role_code='admin')  # Gán role là admin cho superuser mới
        super().save(*args, **kwargs)


class Ministry(models.Model):  # Giáo vụ
    mi_code = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=50,unique=True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Notify(BaseModel):  # Thông báo
    title = models.CharField(max_length=50, null=False)
    content = RichTextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Position(models.Model):  # Vị trí
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name


class SchoolYear(models.Model):  # Năm học
    name = models.CharField(max_length=15, null=False)
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return self.name


class Faculty(models.Model):  # Khoa
    fac_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Major(models.Model):  # Ngành
    maj_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def faculty_name(self):
        return self.faculty.name if self.faculty else None


class Lecturer(models.Model):  # Giảng viên
    lec_code = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    def faculty_name(self):
        return self.faculty.name if self.faculty else None


class Student(models.Model):  # Sinh viên
    stu_code = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    gpa = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name

    def major_name(self):
        return self.major.name if self.major else None


class Council(models.Model):  # Hội đồng
    name = models.CharField(max_length=50, null=False)
    description = RichTextField()
    is_lock = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CouncilDetail(models.Model):  # Chi tiết hội đồng
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)


class Thesis(models.Model):  # Khóa luận
    the_code = models.CharField(max_length=10, null=False, primary_key=True)
    name = models.CharField(max_length=200, null=False)
    start_date = models.DateField()
    end_date = models.DateField()
    report_file = RichTextField(null=True)  # File báo cáo
    total_score = models.FloatField(null=True, default=0)
    result = models.BooleanField(default=False)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT)
    council = models.ForeignKey(Council, on_delete=models.PROTECT)
    students = models.ManyToManyField(Student, null=True, blank=False)  # Nhiều sinh viên ()

    # Hàm tính điểm TB

    def __str__(self):
        return self.name

    def major_name(self):
        return self.major.name if self.major else None


class Instructor(models.Model):  # Giảng viên hướng dẫn khóa luận (Tối đa 2)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT)


class Score(models.Model):  # Điểm
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE)
    council_detail = models.ForeignKey(CouncilDetail, on_delete=models.PROTECT)


class ScoreComponent(models.Model):  # Điểm thành phần = Tiêu chí (Ví dụ: Kiến thức chuyên môn, phương pháp nghiên cứu, kỹ năng trình bày)
    name = models.CharField(max_length=20, null=False)
    evaluation_method = models.CharField(max_length=150, null=True)  # Phương pháp đánh giá

    def __str__(self):
        return self.name


class ScoreColumn(models.Model):  # Cột điểm
    name = models.CharField(max_length=20, null=False)
    weight = models.FloatField(null=False)  # Trọng số (%)
    score_component = models.ForeignKey(ScoreComponent, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ScoreDetail(models.Model):  # Chi tiết điểm
    score_number = models.FloatField()
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    score_column = models.ForeignKey(ScoreColumn, on_delete=models.CASCADE)
