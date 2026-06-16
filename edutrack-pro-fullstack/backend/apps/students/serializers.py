from django.utils import timezone
from rest_framework import serializers

from apps.accounts.models import User

from .models import Attendance, Course, Department, Enrollment, Grade, Notice, StudentProfile, TeacherProfile


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = TeacherProfile
        fields = "__all__"

    def validate_user(self, user):
        if user.role != User.Role.TEACHER:
            raise serializers.ValidationError("Selected user must have TEACHER role.")
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"

    def validate_user(self, user):
        if user.role != User.Role.STUDENT:
            raise serializers.ValidationError("Selected user must have STUDENT role.")
        return user


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.full_name", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def validate_teacher(self, teacher):
        if teacher and teacher.role != User.Role.TEACHER:
            raise serializers.ValidationError("Course teacher must have TEACHER role.")
        return teacher


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)
    roll_number = serializers.CharField(source="student.roll_number", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"

    def validate(self, attrs):
        student = attrs.get("student") or self.instance.student
        course = attrs.get("course") or self.instance.course
        duplicate = Enrollment.objects.filter(student=student, course=course)

        if self.instance:
            duplicate = duplicate.exclude(pk=self.instance.pk)

        if duplicate.exists():
            raise serializers.ValidationError("This student is already enrolled in this course.")

        if not course.is_active:
            raise serializers.ValidationError("Cannot enroll student in an inactive course.")

        return attrs


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="enrollment.student.user.full_name", read_only=True)
    roll_number = serializers.CharField(source="enrollment.student.roll_number", read_only=True)
    course_code = serializers.CharField(source="enrollment.course.code", read_only=True)

    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("marked_by",)

    def validate_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Attendance date cannot be in the future.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        enrollment = attrs.get("enrollment") or self.instance.enrollment

        if request and request.user.role == User.Role.TEACHER:
            if enrollment.course.teacher_id != request.user.id:
                raise serializers.ValidationError("Teachers can only mark attendance for their own courses.")

        return attrs


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="enrollment.student.user.full_name", read_only=True)
    roll_number = serializers.CharField(source="enrollment.student.roll_number", read_only=True)
    course_code = serializers.CharField(source="enrollment.course.code", read_only=True)
    percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Grade
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "percentage")

    def validate(self, attrs):
        request = self.context.get("request")
        enrollment = attrs.get("enrollment") or self.instance.enrollment
        marks_obtained = attrs.get("marks_obtained", self.instance.marks_obtained if self.instance else None)
        max_marks = attrs.get("max_marks", self.instance.max_marks if self.instance else None)

        if marks_obtained is not None and marks_obtained < 0:
            raise serializers.ValidationError("Marks cannot be negative.")

        if marks_obtained is not None and max_marks is not None and marks_obtained > max_marks:
            raise serializers.ValidationError("Marks obtained cannot be greater than maximum marks.")

        if request and request.user.role == User.Role.TEACHER:
            if enrollment.course.teacher_id != request.user.id:
                raise serializers.ValidationError("Teachers can only add grades for their own courses.")

        return attrs


class NoticeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = Notice
        fields = "__all__"
        read_only_fields = ("created_by", "created_at")
