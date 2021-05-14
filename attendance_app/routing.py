from django.urls import re_path
from .consumers import AttendanceConsumer

websocket_urlpatterns = [
    re_path(r'ws/attendance/(?P<room_name>\w+)/$', AttendanceConsumer.as_asgi()),
]
