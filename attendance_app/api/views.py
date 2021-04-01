from datetime import datetime

from django.utils.dateparse import parse_date
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from attendance_app.api.serializers import AttendanceSerializer
from attendance_app.models import Attendance
from course_app.models import Course


class CourseAttendanceView(GenericAPIView):
    parser_classes = [JSONParser]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        # todo check course_id exists and belongs current user
        attendance = Attendance.objects.filter(course_id=course_id)
        date_str = self.request.GET.get('date')
        if date_str:
            date = date_str.split('-')
            num = len(date)
            if num == 3:
                attendance = attendance.filter(date__year=date[0], date__month=date[1], date__day=date[2])
            elif num == 2:
                attendance = attendance.filter(date__year=date[0], date__month=date[1])
            else:
                attendance = attendance.filter(date__year=date[0])
        return attendance

    def get(self, request, *args, **kwargs):
        data = self.serializer_class(self.get_queryset(), many=True).data
        return Response(data)

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
