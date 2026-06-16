from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="teachers")
    designation = models.CharField(max_length=100, default="Faculty")
    qualification = models.CharField(max_length=150, blank=True)
    joining_date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def clean(self):
        if self.user_id and self.user.role != "TEACHER":
            raise ValidationError("Teacher profile can only be created for users with TEACHER role.")

    def __str__(self):
        return self.user.full_name


class StudentProfile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        GRADUATED = "GRADUATED", "Graduated"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    roll_number = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="students")
    admission_date = models.DateField(default=timezone.localdate)
    date_of_birth = models.DateField(null=True, blank=True)
    guardian_name = models.CharField(max_length=120, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ["roll_number"]

    def clean(self):
        if self.user_id and self.user.role != "STUDENT":
            raise ValidationError("Student profile can only be created for users with STUDENT role.")

    def __str__(self):
        return f"{self.roll_number} - {self.user.full_name}"


class Course(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="courses")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="courses")
    credits = models.PositiveSmallIntegerField(default=3)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def clean(self):
        if self.teacher_id and self.teacher.role != "TEACHER":
            raise ValidationError("Course teacher must be a user with TEACHER role.")

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = "ENROLLED", "Enrolled"
        COMPLETED = "COMPLETED", "Completed"
        DROPPED = "DROPPED", "Dropped"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_on = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ENROLLED)

    class Meta:
        ordering = ["-enrolled_on"]
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_student_course_enrollment")
        ]

    def __str__(self):
        return f"{self.student.roll_number} -> {self.course.code}"


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=20, choices=Status.choices)
    remarks = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="marked_attendance")

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(fields=["enrollment", "date"], name="unique_attendance_per_day")
        ]

    def clean(self):
        if self.date and self.date > timezone.localdate():
            raise ValidationError("Attendance date cannot be in the future.")

    def __str__(self):
        return f"{self.enrollment} - {self.date} - {self.status}"


class Grade(models.Model):
    class ExamType(models.TextChoices):
        ASSIGNMENT = "ASSIGNMENT", "Assignment"
        QUIZ = "QUIZ", "Quiz"
        MIDTERM = "MIDTERM", "Midterm"
        FINAL = "FINAL", "Final"

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="grades")
    exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("100.00"))
    remarks = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_grades")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["enrollment", "exam_type"], name="unique_grade_per_exam")
        ]

    def clean(self):
        if self.marks_obtained < 0:
            raise ValidationError("Marks cannot be negative.")
        if self.marks_obtained > self.max_marks:
            raise ValidationError("Marks obtained cannot be greater than maximum marks.")

    @property
    def percentage(self):
        if not self.max_marks:
            return 0
        return round(float((self.marks_obtained / self.max_marks) * 100), 2)

    def __str__(self):
        return f"{self.enrollment} - {self.exam_type}"


class Notice(models.Model):
    class Audience(models.TextChoices):
        ALL = "ALL", "All"
        TEACHERS = "TEACHERS", "Teachers"
        STUDENTS = "STUDENTS", "Students"

    title = models.CharField(max_length=160)
    message = models.TextField()
    audience = models.CharField(max_length=20, choices=Audience.choices, default=Audience.ALL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="notices")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
