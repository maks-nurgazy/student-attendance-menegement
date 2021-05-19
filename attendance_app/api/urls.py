from django.urls import path

from attendance_app.api.views import CourseAttendanceView, CourseAttendanceDetailView

urlpatterns = [
    path('teacher/courses/<int:course_id>/attendances/', CourseAttendanceView.as_view()),
    path('teacher/attendances/<int:attendance_id>/', CourseAttendanceDetailView.as_view()),
]
