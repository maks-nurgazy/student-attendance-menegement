from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from attendance_app.api.serializers import AttendanceSerializer


class CourseAttendanceView(GenericAPIView):
    parser_classes = [JSONParser]
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True})

    def get_serializer_context(self):
        return {
            'course_id': self.kwargs['course_id']
        }
