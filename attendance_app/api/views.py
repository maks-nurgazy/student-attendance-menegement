from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from attendance_app.api.serializers import AttendanceSerializer, AttendanceReportSerializer
from attendance_app.models import Attendance
from course_app.models import Course
from student_attendance_management.permissions import IsAttendanceOwner


class CourseAttendanceView(GenericAPIView):
    parser_classes = [JSONParser]
    serializer_class = AttendanceSerializer
    permission_classes = (IsAttendanceOwner,)

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        attendance = Attendance.objects.filter(course_id=course_id)
        obj = get_object_or_404(Course.objects.all(), pk=self.kwargs["course_id"])
        self.check_object_permissions(self.request, obj)
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
        data = self.serializer_class(self.get_queryset(), context=self.get_serializer_context(), many=True).data
        return Response(data)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data=data)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'kwargs': self.kwargs
        }


class CourseAttendanceDetailView(GenericAPIView):
    parser_classes = [JSONParser]
    serializer_class = AttendanceSerializer
    permission_classes = (IsAttendanceOwner,)

    def get_object(self):
        attendance_id = self.kwargs['attendance_id']
        obj = get_object_or_404(Attendance.objects.all(), pk=attendance_id)
        self.check_object_permissions(self.request, obj.course)
        return obj

    def put(self, request, *args, **kwargs):
        data = self.request.data
        reports = data['reports']
        attendance = self.get_object()
        serializer = AttendanceReportSerializer(
            data=reports, many=True, context={"course_id": attendance.course.id})
        serializer.is_valid(raise_exception=True)
        self.update_attendance(attendance, serializer.validated_data)
        response = self.serializer_class(attendance, context={"kwargs": {"course_id": attendance.course.id}}).data
        return Response(data=response)

    def update_attendance(self, attendance, data):
        reports = attendance.reports
        for obj in data:
            report = reports.get(student=obj['student_id'])
            report.status = obj['status']
            report.save()
