from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('chat/', include('attendance_app.urls')),
    path('admin/', admin.site.urls),
    path('attendance-management/api/', include('users.api.urls')),
    path('attendance-management/api/', include('university_app.api.urls')),
    path('attendance-management/api/', include('attendance_app.api.urls')),
    path('attendance-management/api/', include('course_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
