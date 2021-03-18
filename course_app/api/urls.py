from django.urls import path, include
from rest_framework.routers import DefaultRouter

from course_app.api.views.course_views import CourseViewSet

courses = DefaultRouter()
courses.register('courses', CourseViewSet)

urlpatterns = [
    path('', include(courses.urls)),
]
