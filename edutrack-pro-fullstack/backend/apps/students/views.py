from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import User
from apps.common.permissions import IsAdminOrTeacherRole, IsAdminRole, IsAdminWriteOrAuthenticatedRead

from .models import Attendance, Course, Department, Enrollment, Grade, Notice, StudentProfile, TeacherProfile
from .serializers import (
    AttendanceSerializer,
    CourseSerializer,
    DepartmentSerializer,
    EnrollmentSerializer,
    GradeSerializer,
    NoticeSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
)


def is_admin(user):
    return user.is_staff or user.role == User.Role.ADMIN


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "code"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return [IsAuthenticated()]


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.select_related("user", "department")
    serializer_class = TeacherProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["user__first_name", "user__last_name", "user__email", "department__name"]
    ordering_fields = ["joining_date", "user__first_name"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return [IsAuthenticated()]


class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["roll_number", "user__first_name", "user__last_name", "user__email", "department__name"]
    ordering_fields = ["roll_number", "admission_date"]

    def get_queryset(self):
        user = self.request.user
        queryset = StudentProfile.objects.select_related("user", "department")

        if is_admin(user):
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(enrollments__course__teacher=user).distinct()

        return queryset.filter(user=user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return [IsAuthenticated()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("department", "teacher")
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "code", "department__name", "teacher__first_name", "teacher__last_name"]
    ordering_fields = ["code", "name", "credits"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return [IsAuthenticated()]


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["student__roll_number", "student__user__first_name", "course__name", "course__code"]
    ordering_fields = ["enrolled_on", "status"]

    def get_queryset(self):
        user = self.request.user
        queryset = Enrollment.objects.select_related("student__user", "course", "course__teacher")

        if is_admin(user):
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(course__teacher=user)

        return queryset.filter(student__user=user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return [IsAuthenticated()]


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["enrollment__student__roll_number", "enrollment__course__code"]
    ordering_fields = ["date", "status"]

    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.select_related("enrollment__student__user", "enrollment__course", "marked_by")

        if is_admin(user):
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(enrollment__course__teacher=user)

        return queryset.filter(enrollment__student__user=user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrTeacherRole()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["enrollment__student__roll_number", "enrollment__course__code", "exam_type"]
    ordering_fields = ["created_at", "marks_obtained", "exam_type"]

    def get_queryset(self):
        user = self.request.user
        queryset = Grade.objects.select_related("enrollment__student__user", "enrollment__course", "created_by")

        if is_admin(user):
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(enrollment__course__teacher=user)

        return queryset.filter(enrollment__student__user=user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrTeacherRole()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer
    permission_classes = [IsAdminWriteOrAuthenticatedRead]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "message", "audience"]
    ordering_fields = ["created_at", "audience"]

    def get_queryset(self):
        user = self.request.user
        queryset = Notice.objects.select_related("created_by")

        if is_admin(user):
            return queryset

        queryset = queryset.filter(is_active=True)

        if user.role == User.Role.TEACHER:
            return queryset.filter(audience__in=[Notice.Audience.ALL, Notice.Audience.TEACHERS])

        return queryset.filter(audience__in=[Notice.Audience.ALL, Notice.Audience.STUDENTS])

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    user = request.user

    if is_admin(user):
        return Response(
            {
                "role": user.role,
                "departments": Department.objects.count(),
                "teachers": TeacherProfile.objects.count(),
                "students": StudentProfile.objects.count(),
                "courses": Course.objects.count(),
                "enrollments": Enrollment.objects.count(),
                "attendance_records": Attendance.objects.count(),
                "grades": Grade.objects.count(),
            }
        )

    if user.role == User.Role.TEACHER:
        return Response(
            {
                "role": user.role,
                "courses": Course.objects.filter(teacher=user).count(),
                "students": Enrollment.objects.filter(course__teacher=user).values("student").distinct().count(),
                "attendance_records": Attendance.objects.filter(enrollment__course__teacher=user).count(),
                "grades_created": Grade.objects.filter(enrollment__course__teacher=user).count(),
            }
        )

    grades = Grade.objects.filter(enrollment__student__user=user)
    attendance = Attendance.objects.filter(enrollment__student__user=user)

    return Response(
        {
            "role": user.role,
            "enrolled_courses": Enrollment.objects.filter(student__user=user).count(),
            "present_days": attendance.filter(status=Attendance.Status.PRESENT).count(),
            "absent_days": attendance.filter(status=Attendance.Status.ABSENT).count(),
            "average_marks": grades.aggregate(avg=Avg("marks_obtained"))["avg"] or 0,
            "grades": grades.count(),
        }
    )
