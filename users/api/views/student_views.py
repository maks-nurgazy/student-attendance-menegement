from rest_framework.viewsets import ModelViewSet

from users.api.serializers.student_serializers import StudentSerializer
from users.models import Student


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
