from rest_framework.viewsets import ModelViewSet

from users.api.serializers.student_serializers import TeacherSerializer
from users.models import Teacher


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
