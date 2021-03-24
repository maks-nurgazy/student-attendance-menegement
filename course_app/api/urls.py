from django.urls import path, include
from rest_framework.routers import DefaultRouter

from course_app.api.views import CourseViewSet, EnrollmentView, StudentCourseView

courses = DefaultRouter()
courses.register('courses', CourseViewSet)

urlpatterns = [
    path('', include(courses.urls)),
    path('student/enrollment/', EnrollmentView.as_view()),

    path('student/courses/', StudentCourseView.as_view()),
]
