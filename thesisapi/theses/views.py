from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from theses.models import *
from theses import serializers, paginators, perms


# Vai trò
class RoleViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [perms.IsAdmin]


# Người dùng
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user']:
            return [perms.IsAuthenticated()]

        return [perms.IsAdmin()]

    # Lấy thông tin User đang chứng thực, cập nhật thông tin User
    @action(methods=['get', 'patch'], url_path='current_user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)


# Giáo vụ
# Thông báo
# Vị trí
class PositionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = serializers.PositionSerializer


# Năm học
class SchoolYearViewSet(viewsets.ViewSet, generics.CreateAPIView,
                        generics.ListAPIView, generics.DestroyAPIView):
    queryset = SchoolYear.objects.all()
    serializer_class = serializers.SchoolYearSerializer
    parser_classes = [parsers.MultiPartParser]

    # permission_classes = [perms.IsAdmin]

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        return queryset

    # Sửa thông tin năm học
    def partial_update(self, request, pk=None):
        schy = self.get_object()
        serializer = self.serializer_class(schy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Khoa
class FacultyViewSet(viewsets.ViewSet, generics.CreateAPIView,
                     generics.ListAPIView, generics.DestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    pagination_class = paginators.BasePaginator
    parser_classes = [parsers.MultiPartParser]

    # permission_classes = [perms.IsAdmin, perms.IsMinistry]  # Xem lại quyền

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        return queryset

    # Sửa thông tin khoa
    def partial_update(self, request, pk=None):
        faculty = self.get_object()
        serializer = self.serializer_class(faculty, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Ngành học
class MajorViewSet(viewsets.ViewSet, generics.CreateAPIView,
                   generics.ListAPIView, generics.DestroyAPIView):
    queryset = Major.objects.all()
    serializer_class = serializers.MajorSerializer
    pagination_class = paginators.BasePaginator
    parser_classes = [parsers.MultiPartParser]

    # permission_classes = [perms.IsAdmin, perms.IsMinistry]  # Xem lại quyền

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        fac_id = self.request.query_params.get('faculty_id')
        if fac_id:
            queryset = queryset.filter(faculty_id=fac_id)

        return queryset

    # Sửa thông tin ngành
    def partial_update(self, request, pk=None):
        major = self.get_object()
        serializer = self.serializer_class(major, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Giảng viên
class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = serializers.LecturerSerializer
    pagination_class = paginators.BasePaginator
    parser_classes = [parsers.MultiPartParser]

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(full_name__icontains=q)

        fac_id = self.request.query_params.get('faculty_id')
        if fac_id:
            queryset = queryset.filter(faculty_id=fac_id)

        return queryset

    # Lấy hội đồng mà giảng viên tham gia


# Sinh Viên
class StudentViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    pagination_class = paginators.BasePaginator
    parser_classes = [parsers.MultiPartParser, ]

    # permission_classes = [perms.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(full_name__icontains=q)

        maj_id = self.request.query_params.get('major_id')
        if maj_id:
            queryset = queryset.filter(faculty_id=maj_id)

        return queryset

    # Lấy khóa luận mà sinh viên tham gia
    @action(methods=['get'], url_path='theses', detail=True)
    def get_theses(self, request, pk=None):
        try:
            student = self.queryset.get(pk=pk)
            theses = student.thesis_set.all()  # Lấy danh sách các khóa luận mà sinh viên tham gia
            serializer = serializers.ThesisSerializer(theses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"Lỗi": "Không tìm thấy sinh viên!"}, status=status.HTTP_404_NOT_FOUND)

    # Lấy điểm khóa luận của sinh viên


# Hội đồng
class CouncilViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.DestroyAPIView):
    queryset = Council.objects.all()
    serializer_class = serializers.CouncilSerializer
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [perms.IsMinistry]

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        status = self.request.query_params.get('is_lock')
        if status:
            queryset = queryset.filter(is_lock=status)

        return queryset

    # API để cập nhật trường is_lock của Council
    @action(methods=['post'], url_path='update_lock', detail=True)
    def update_lock(self, request, pk=None):
        council = self.get_object()
        council.is_lock = not council.is_lock
        council.save()
        return Response({'is_lock': council.is_lock}, status=status.HTTP_200_OK)


# Chi tiết hội đồng
class CouncilDetailViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.DestroyAPIView):
    queryset = CouncilDetail.objects.all()
    serializer_class = serializers.CouncilDetailSerializer
    parser_classes = [parsers.MultiPartParser]


# Khóa luận
class ThesisViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Thesis.objects.prefetch_related('students').all()
    serializer_class = serializers.ThesisSerializer
    parser_classes = [parsers.MultiPartParser, ]

    # permission_classes = [perms.IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()

        # Lọc theo các tham số truy vấn
        q = request.query_params.get('q')
        council_id = request.query_params.get('council_id')
        major_id = request.query_params.get('major_id')
        school_year_id = request.query_params.get('school_year_id')

        if q:
            queryset = queryset.filter(name__icontains=q)
        if council_id:
            queryset = queryset.filter(council_id=council_id)
        if major_id:
            queryset = queryset.filter(major_id=major_id)
        if school_year_id:
            queryset = queryset.filter(school_year_id=school_year_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

# Giảng viên hướng dẫn khóa luận
# Điểm
# Cột điểm
# Điểm thành phần
# Chi tiết điểm
