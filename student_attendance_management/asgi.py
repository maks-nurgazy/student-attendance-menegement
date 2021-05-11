import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import attendance_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_attendance_management.settings.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            attendance_app.routing.websocket_urlpatterns
        )
    ),
})
