from django.urls import path

from attendance_app.api.views import SubjectAttendanceView

urlpatterns = [
    path('teacher/subjects/<int:subject_id>/attendances/', SubjectAttendanceView.as_view())
]
