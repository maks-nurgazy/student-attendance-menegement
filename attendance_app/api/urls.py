from django.urls import path

from attendance_app.api.views import CourseAttendanceView

urlpatterns = [
    path('teacher/courses/<int:course_id>/attendances/', CourseAttendanceView.as_view())
]
