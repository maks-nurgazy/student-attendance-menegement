from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ajax_select import urls as ajax_select_urls

admin.autodiscover()
urlpatterns = [
    path('ajax_select/', include(ajax_select_urls)),
    path('attendance/', include('attendance_app.urls')),
    path('admin/', admin.site.urls),
    path('attendance-management/api/', include('users.api.urls')),
    path('attendance-management/api/', include('university_app.api.urls')),
    path('attendance-management/api/', include('attendance_app.api.urls')),
    path('attendance-management/api/', include('course_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
