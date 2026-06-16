from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceViewSet,
    CourseViewSet,
    DepartmentViewSet,
    EnrollmentViewSet,
    GradeViewSet,
    NoticeViewSet,
    StudentProfileViewSet,
    TeacherProfileViewSet,
    dashboard_summary,
)

app_name = "students"

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="department")
router.register("teachers", TeacherProfileViewSet, basename="teacher")
router.register("profiles", StudentProfileViewSet, basename="student-profile")
router.register("courses", CourseViewSet, basename="course")
router.register("enrollments", EnrollmentViewSet, basename="enrollment")
router.register("attendance", AttendanceViewSet, basename="attendance")
router.register("grades", GradeViewSet, basename="grade")
router.register("notices", NoticeViewSet, basename="notice")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", dashboard_summary, name="dashboard-summary"),
]
