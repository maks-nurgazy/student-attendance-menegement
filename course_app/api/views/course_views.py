from rest_framework.viewsets import ModelViewSet

from course_app.api.serializers.course_serializers import CourseSerializer
from course_app.models import Course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
