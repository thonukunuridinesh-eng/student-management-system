from django.contrib import admin

from .models import Attendance, Course, Department, Enrollment, Grade, Notice, StudentProfile, TeacherProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "designation", "joining_date")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("department", "designation")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "user", "department", "status", "admission_date")
    search_fields = ("roll_number", "user__email", "user__first_name", "user__last_name")
    list_filter = ("department", "status", "admission_date")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "teacher", "credits", "is_active")
    search_fields = ("code", "name", "department__name")
    list_filter = ("department", "is_active")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "enrolled_on")
    search_fields = ("student__roll_number", "student__user__email", "course__code")
    list_filter = ("status", "course", "enrolled_on")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "date", "status", "marked_by")
    search_fields = ("enrollment__student__roll_number", "enrollment__course__code")
    list_filter = ("status", "date")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "exam_type", "marks_obtained", "max_marks", "percentage", "created_by")
    search_fields = ("enrollment__student__roll_number", "enrollment__course__code")
    list_filter = ("exam_type", "created_at")


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "is_active", "created_by", "created_at")
    search_fields = ("title", "message")
    list_filter = ("audience", "is_active", "created_at")
