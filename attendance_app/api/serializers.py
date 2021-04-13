from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from attendance_app.models import AttendanceReport, Attendance
from course_app.models import Course


class AttendanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceReport
        fields = ('student', 'status')


class CourseIdSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    def validate_id(self, value):
        course_teacher = Course.objects.get(value).teacher
        request_teacher = self.context['teacher']
        if not course_teacher.id == request_teacher.id:
            raise PermissionDenied(detail="You must be a teacher", code=400)
        return value

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AttendanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    reports = AttendanceReportSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        course = get_object_or_404(Course, id=self.context['course_id'])
        attendance = Attendance.objects.create(date=validated_data['date'], course=course)
        for report in validated_data['reports']:
            AttendanceReport.objects.create(**report, attendance=attendance)
        return attendance


class ArduinoSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
