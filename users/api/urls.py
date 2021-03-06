from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from users.api.views import TeacherViewSet, AdvisorViewSet, StudentViewSet, UserLoginView, AdvisorStudentsView, \
    AdvisorStudentsDetailView, AdminsViewSet

router = DefaultRouter()
router.register('students', StudentViewSet)
router.register('teachers', TeacherViewSet)
router.register('advisors', AdvisorViewSet)
router.register('admins', AdminsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('advisor/students/', AdvisorStudentsView.as_view()),
    path('advisor/students/<int:id>/', AdvisorStudentsDetailView.as_view()),
    path('auth/login/', UserLoginView.as_view()),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
