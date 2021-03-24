from abc import ABC, ABCMeta

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from attendance_app.models import AttendanceReport
from course_app.models import Course


class AttendanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceReport
        fields = ('id', 'student', 'status')


class DateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    date = serializers.DateField()


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
