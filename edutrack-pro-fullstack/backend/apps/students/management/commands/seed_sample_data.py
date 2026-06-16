from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User
from apps.students.models import Attendance, Course, Department, Enrollment, Grade, Notice, StudentProfile, TeacherProfile


class Command(BaseCommand):
    help = "Create sample users and academic data for local testing."

    def handle(self, *args, **options):
        admin_user, _ = User.objects.get_or_create(
            email="admin@edutrack.com",
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("Admin@12345")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.role = User.Role.ADMIN
        admin_user.save()

        teacher_user, _ = User.objects.get_or_create(
            email="teacher@edutrack.com",
            defaults={
                "first_name": "Priya",
                "last_name": "Sharma",
                "role": User.Role.TEACHER,
                "phone": "9876543210",
            },
        )
        teacher_user.set_password("Teacher@12345")
        teacher_user.role = User.Role.TEACHER
        teacher_user.save()

        student_user, _ = User.objects.get_or_create(
            email="student@edutrack.com",
            defaults={
                "first_name": "Aarav",
                "last_name": "Mehta",
                "role": User.Role.STUDENT,
                "phone": "9876500001",
            },
        )
        student_user.set_password("Student@12345")
        student_user.role = User.Role.STUDENT
        student_user.save()

        department, _ = Department.objects.get_or_create(
            code="CSE",
            defaults={
                "name": "Computer Science Engineering",
                "description": "Department for software engineering and computer science students.",
            },
        )

        TeacherProfile.objects.get_or_create(
            user=teacher_user,
            defaults={
                "department": department,
                "designation": "Assistant Professor",
                "qualification": "M.Tech Computer Science",
            },
        )

        student_profile, _ = StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                "roll_number": "CSE2026001",
                "department": department,
                "guardian_name": "Rohit Mehta",
                "guardian_phone": "9876500002",
                "address": "Bengaluru, India",
            },
        )

        course, _ = Course.objects.get_or_create(
            code="PY101",
            defaults={
                "name": "Python Programming",
                "department": department,
                "teacher": teacher_user,
                "credits": 4,
            },
        )

        enrollment, _ = Enrollment.objects.get_or_create(student=student_profile, course=course)

        Attendance.objects.get_or_create(
            enrollment=enrollment,
            date=timezone.localdate(),
            defaults={"status": Attendance.Status.PRESENT, "marked_by": teacher_user},
        )

        Grade.objects.get_or_create(
            enrollment=enrollment,
            exam_type=Grade.ExamType.QUIZ,
            defaults={
                "marks_obtained": Decimal("86.00"),
                "max_marks": Decimal("100.00"),
                "remarks": "Good performance.",
                "created_by": teacher_user,
            },
        )

        Notice.objects.get_or_create(
            title="Welcome to EduTrack Pro",
            defaults={
                "message": "Your academic dashboard is ready.",
                "audience": Notice.Audience.ALL,
                "created_by": admin_user,
            },
        )

        self.stdout.write(self.style.SUCCESS("Sample data created successfully."))
        self.stdout.write("Admin: admin@edutrack.com / Admin@12345")
        self.stdout.write("Teacher: teacher@edutrack.com / Teacher@12345")
        self.stdout.write("Student: student@edutrack.com / Student@12345")
