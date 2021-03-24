from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from attendance_app.api.serializers import AttendanceReportSerializer, DateSerializer


class SubjectAttendanceView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        reports = data['reports']
        date = data['date']
        date_serializer = DateSerializer(data={"date": date})
        date_serializer.is_valid(raise_exception=True)
        report_serializer = AttendanceReportSerializer(data=reports, many=True)
        report_serializer.is_valid(raise_exception=True)
        subject_id = kwargs['subject_id']

        return Response({"success": True})
