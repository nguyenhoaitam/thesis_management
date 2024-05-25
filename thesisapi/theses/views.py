from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from theses.models import *
from theses import serializers, paginators, perms


# Vai trò (Quản lý trong Admin)
class RoleViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [perms.IsAdmin]


# Người dùng
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user']:
            return [perms.IsAuthenticated()]

        return [permissions.AllowAny()]

    # Lấy thông tin User đang chứng thực, cập nhật thông tin User, cập nhật mật khẩu thì băm
    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            data = request.data.copy()  # Tạo một bản sao của dữ liệu để tránh ảnh hưởng đến dữ liệu gốc
            if 'password' in data:
                data['password'] = make_password(data['password'])  # Băm mật khẩu mới

            serializer = serializers.UserSerializer(instance=user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.UserSerializer(user).data)


# Giáo vụ

# Vị trí
class PositionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = serializers.PositionSerializer


# Năm học (Quản lý trong Admin, Giáo vụ)
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


# Khoa (Quản lý trong Admin, Giáo vụ)
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


# Ngành học (Quản lý trong Admin, Giáo vụ)
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
    @action(detail=True, methods=['get'], url_path='councils')
    def get_councils(self, request, pk=None):
        try:
            lecturer = self.get_object()
            councils = Council.objects.filter(councildetail__lecturer=lecturer)
            serializer = serializers.CouncilSerializer(councils, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lecturer.DoesNotExist:
            return Response({"Lỗi": "Giảng viên không tồn tại!"}, status=status.HTTP_404_NOT_FOUND)


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
    # permission_classes = [perms.IsMinistry]

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

    # Lấy danh sách thành viên trong hội đồng
    @action(detail=True, methods=['get'], url_path='members')
    def get_members(self, request, pk=None):
        try:
            council = self.get_object()
            members = CouncilDetail.objects.filter(council=council).select_related('lecturer', 'position')
            members_data = [{
                "Tên": member.lecturer.full_name,
                "Vị trí": member.position.name
            } for member in members]
            return Response(members_data, status=status.HTTP_200_OK)
        except Council.DoesNotExist:
            return Response({"Lỗi": "Không tìm thấy hội đồng!"}, status=status.HTTP_404_NOT_FOUND)

    # Lấy danh sách khóa luận mà hội đồng chấm
    @action(methods=['get'], url_path='theses', detail=True)
    def get_theses(self, request, pk=None):
        try:
            council = self.queryset.get(pk=pk)
            theses = council.thesis_set.all()  # Lấy danh sách các khóa luận mà hội đồng chấm
            serializer = serializers.ThesisSerializer(theses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Council.DoesNotExist:
            return Response({"Lỗi": "Không tìm thấy hội đồng!"}, status=status.HTTP_404_NOT_FOUND)

    # Gán hội đồng vào khóa luận
    @action(detail=True, methods=['post'], url_path='assign-thesis')
    def assign_thesis(self, request, pk=None):
        try:
            council = self.get_object()
        except Council.DoesNotExist:
            return Response({'Lỗi': 'Hội đồng không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra tổng số lượng khóa luận mà hội đồng đã chấm
        if council.thesis_set.count() >= 5:
            return Response({'Lỗi': 'Một hội đồng chỉ chấm tối đa 5 khóa luận.'},
                            status=status.HTTP_400_BAD_REQUEST)

        thesis_code = request.data.get('thesis_code')
        try:
            thesis = Thesis.objects.get(code=thesis_code)
        except Thesis.DoesNotExist:
            return Response({'Lỗi': 'Khóa luận không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        if thesis.council:
            return Response({'Lỗi': f'Khóa luận {thesis_code} đã được gán hội đồng.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Gán hội đồng cho khóa luận
        thesis.council = council
        thesis.save()

        return Response(serializers.CouncilSerializer(council).data, status=status.HTTP_201_CREATED)

    # Xử lý gửi mail khi hội đồng khóa


# Chi tiết hội đồng
class CouncilDetailViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView):
    queryset = CouncilDetail.objects.all()
    serializer_class = serializers.CouncilDetailSerializer
    parser_classes = [parsers.MultiPartParser]

    # Thêm thành viên vào một hội đồng
    def create(self, request):
        council_id = request.data.get('council')
        lecturer_id = request.data.get('lecturer')
        position_id = request.data.get('position')

        try:
            council = Council.objects.prefetch_related('councildetail_set').get(id=council_id)
        except Council.DoesNotExist:
            return Response({'Lỗi': 'Hội đồng không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        council_details = council.councildetail_set.all()

        if council_details.count() >= 5:
            return Response({'Lỗi': 'Một hội đồng chỉ có tối đa năm thành viên.'}, status=status.HTTP_400_BAD_REQUEST)

        # Đếm số lượng từng vị trí bằng ID
        position_counts = {
            1: 0,  # ID của chủ tịch
            2: 0,  # ID của thư ký
            3: 0  # ID của phản biện
        }

        for detail in council_details:
            pos_id = detail.position.id
            if pos_id in position_counts:
                position_counts[pos_id] += 1

        try:
            position = Position.objects.get(id=position_id)
        except Position.DoesNotExist:
            return Response({'Lỗi': 'Vị trí không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra vị trí bằng ID
        if position.id == 1 and position_counts[1] >= 1:
            return Response({'Lỗi': 'Hội đồng chỉ có một chủ tịch.'}, status=status.HTTP_400_BAD_REQUEST)
        if position.id == 2 and position_counts[2] >= 1:
            return Response({'Lỗi': 'Hội đồng chỉ có một thư ký.'}, status=status.HTTP_400_BAD_REQUEST)
        if position.id == 3 and position_counts[3] >= 1:
            return Response({'Lỗi': 'Hội đồng chỉ có một phản biện.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lecturer = Lecturer.objects.get(user_id=lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({'Lỗi': 'Giảng viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra nếu giảng viên đã có một chức vụ trong hội đồng này
        if council_details.filter(lecturer_id=lecturer_id).exists():
            return Response({'Lỗi': 'Giảng viên này đã giữ một chức vụ khác trong hội đồng.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            council_detail = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xử lý gửi email/sms khi gán giảng viên phản biện


# Khóa luận
class ThesisViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Thesis.objects.prefetch_related('lecturers').all()
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

    # Thêm giảng viên hướng dẫn vào khóa luận
    @action(detail=True, methods=['post'], url_path='add_lecturer')
    def add_lecturer(self, request, pk=None):
        try:
            # Lấy đối tượng khóa luận
            thesis = self.get_object()

            # Kiểm tra xem đã đủ 2 giảng viên hướng dẫn chưa chưa
            if thesis.lecturers.count() >= 2:
                return Response({"Lỗi": "Đã đủ hai giảng viên hướng dẫn không thể thêm."}, status=status.HTTP_400_BAD_REQUEST)

            # Lấy mã giảng viên từ dữ liệu yêu cầu POST
            lecturer_code = request.data.get('lecturer_code')

            # Lấy đối tượng giảng viên từ mã
            lecturer = Lecturer.objects.get(user_id=lecturer_code)
        except (Thesis.DoesNotExist, Lecturer.DoesNotExist):
            return Response({"Lỗi": "Khóa luận hoặc Giảng viên không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        # Thêm giảng viên vào khóa luận
        thesis.lecturers.add(lecturer)
        thesis.save()

        # Trả về dữ liệu của khóa luận đã được cập nhật
        serializer = self.get_serializer(thesis)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Tính điểm tổng của KL

# Điểm
# Cột điểm
# Điểm thành phần
# Chi tiết điểm
