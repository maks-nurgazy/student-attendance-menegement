from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api.views.student_views import StudentViewSet
from users.api.views.user_login_view import UserLoginView

router = DefaultRouter()
router.register('students', StudentViewSet)
router.register('teachers', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', UserLoginView.as_view()),
]
