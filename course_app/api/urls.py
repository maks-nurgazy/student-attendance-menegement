from django.urls import path, include
from rest_framework.routers import DefaultRouter

from course_app.api.views import CourseViewSet, EnrollmentView, StudentCourseView, TeacherCourseView, \
    CourseStudentsView, AdviserCourseApproveView

courses = DefaultRouter()
courses.register('courses', CourseViewSet)

urlpatterns = [
    path('', include(courses.urls)),
    path('student/enrollment/', EnrollmentView.as_view()),
    path('student/courses/', StudentCourseView.as_view()),
    path('teacher/courses/', TeacherCourseView.as_view()),
    path('adviser/approve/<int:id>/', AdviserCourseApproveView.as_view()),
    path('courses/<int:course_id>/students/', CourseStudentsView.as_view()),
]
