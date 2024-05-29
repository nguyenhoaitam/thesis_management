import cloudinary
from django.contrib.auth.hashers import make_password
from django.http import Http404
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from theses.models import *
from theses import serializers, paginators, perms
from django.core.mail import EmailMessage
from django.conf import settings


# Vai trò (Quản lý trong Admin)

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
    pagination_class = paginators.BasePaginator


# Năm học (Quản lý trong Admin, Giáo vụ)
class SchoolYearViewSet(viewsets.ViewSet, generics.CreateAPIView,
                        generics.ListAPIView, generics.DestroyAPIView):
    queryset = SchoolYear.objects.all()
    serializer_class = serializers.SchoolYearSerializer
    parser_classes = [parsers.MultiPartParser]
    pagination_class = paginators.BasePaginator

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
        lecturer = self.get_object()
        council_details = CouncilDetail.objects.filter(lecturer=lecturer).select_related('council', 'position')
        serializer = serializers.CouncilDetailWithIDSerializer(council_details, many=True)
        return Response(serializer.data)

    # Lấy khóa luận mà giảng viên hướng dẫn
    @action(detail=True, methods=['get'])
    def theses(self, request, pk=None):
        lecturer = self.get_object()
        theses = Thesis.objects.filter(lecturers=lecturer)
        serializer = serializers.ThesisSerializer(theses, many=True)
        return Response(serializer.data)

    # Lấy khóa luận giảng viên phản biện
    @action(detail=True, methods=['get'])
    def theses_review(self, request, pk=None):
        lecturer = self.get_object()
        review_positions = Position.objects.filter(name__icontains='Phản biện')
        council_details = CouncilDetail.objects.filter(lecturer=lecturer, position__in=review_positions).select_related(
            'council')
        council_ids = council_details.values_list('council_id', flat=True)
        theses = Thesis.objects.filter(council_id__in=council_ids).select_related('major', 'school_year',   'council').prefetch_related('lecturers')
        serializer = serializers.ThesisSerializer(theses, many=True)
        return Response(serializer.data)


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

    # Gán khóa luận vào sinh viên
    @action(detail=True, methods=['post'], url_path='assign_thesis')
    def assign_thesis(self, request, pk=None):
        student = self.get_object()
        thesis_code = request.data.get('thesis_code')

        # Kiểm tra nếu sinh viên đã có khóa luận
        if student.thesis:
            return Response({'Lỗi': 'Sinh viên đã có khóa luận'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            thesis = Thesis.objects.get(pk=thesis_code)
        except Thesis.DoesNotExist:
            return Response({'Lỗi': 'Không tìm thấy khóa luận'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra ngành của sinh viên phải cùng với ngành của khóa luận
        if student.major != thesis.major:
            return Response({'Lỗi': 'Không thể thêm do sinh viên và khóa luận không cùng ngành'}, status=status.HTTP_400_BAD_REQUEST)

        student.thesis = thesis
        student.save()

        serializer = self.get_serializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Lấy điểm khóa luận của sinh viên


# Hội đồng
class CouncilViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.DestroyAPIView):
    queryset = Council.objects.all()
    serializer_class = serializers.CouncilSerializer
    parser_classes = [parsers.MultiPartParser]
    pagination_class = paginators.BasePaginator
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

    # Sửa thông tin hội đồng
    def partial_update(self, request, pk=None):
        council = self.get_object()
        serializer = self.serializer_class(council, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                "full_name": member.lecturer.full_name,
                "position": member.position.name
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

        # Kiểm tra nếu hội đồng có giảng viên là giảng viên hướng dẫn khóa luận đó
        thesis_lecturers = thesis.lecturers.all()
        council_lecturers = council.councildetail_set.values_list('lecturer', flat=True)
        if any(lecturer.user_id in council_lecturers for lecturer in thesis_lecturers):
            return Response({'Lỗi': 'Hội đồng có giảng viên là giảng viên hướng dẫn khóa luận này.'},
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

            # Sau khi lưu chi tiết của hội đồng thành công
            if position.id == 3:  # Nếu giảng viên được gán là phản biện
                lecturer_email = lecturer.user.email
                council_name = council.name
                subject = f'Bạn đã được giao làm phản biện cho hội đồng "{council_name}"'
                message = (
                    f'Chào mừng bạn đã được giao vai trò phản biện cho hội đồng "{council_name}".\n'
                    'Vui lòng chuẩn bị và liên hệ với các thành viên khác trong hội đồng để hoàn thành nhiệm vụ của mình.\n'
                    '__Giáo vụ__'
                )

                from_email = 'Thesis Management <{}>'.format(settings.DEFAULT_FROM_EMAIL)

                # Gửi email thông báo cho giảng viên
                email = EmailMessage(subject, message, from_email, to=[lecturer_email])
                email.send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Http404:
            return Response({'Lỗi': 'Thành viên hội đồng không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Lỗi': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Khóa luận
class ThesisViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Thesis.objects.prefetch_related('lecturers').all()
    serializer_class = serializers.ThesisSerializer
    parser_classes = [parsers.MultiPartParser, ]
    pagination_class = paginators.ThesisPaginator

    # permission_classes = [perms.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        # Lọc theo các tham số truy vấn
        q = self.request.query_params.get('q')
        council_id = self.request.query_params.get('council_id')
        major_id = self.request.query_params.get('major_id')
        school_year_id = self.request.query_params.get('school_year_id')

        if q:
            queryset = queryset.filter(name__icontains=q)
        if council_id:
            queryset = queryset.filter(council_id=council_id)
        if major_id:
            queryset = queryset.filter(major_id=major_id)
        if school_year_id:
            queryset = queryset.filter(school_year_id=school_year_id)

        return queryset

    @action(detail=True, methods=['get'], url_path='students')
    def students(self, request, pk=None):
        thesis = self.get_object()
        students = thesis.student_set.all()
        serializer = serializers.StudentSerializer(students, many=True)
        return Response(serializer.data)

    # Sửa thông tin
    def partial_update(self, request, pk=None):
        thesis = self.get_object()
        serializer = self.serializer_class(thesis, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            lecturer = Lecturer.objects.get(code=lecturer_code)
        except (Thesis.DoesNotExist, Lecturer.DoesNotExist):
            return Response({"Lỗi": "Khóa luận hoặc giảng viên không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem giảng viên đã có trong danh sách hướng dẫn chưa
        if lecturer in thesis.lecturers.all():
            return Response({"Lỗi": "Giảng viên đã có trong danh sách hướng dẫn."}, status=status.HTTP_400_BAD_REQUEST)

        # Thêm giảng viên vào khóa luận
        thesis.lecturers.add(lecturer)
        thesis.save()

        # Trả về dữ liệu của khóa luận đã được cập nhật
        serializer = self.get_serializer(thesis)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Tính điểm tổng của KL

    # Thêm file báo cáo


# Điểm
# Cột điểm
# Điểm thành phần
# Chi tiết điểm
