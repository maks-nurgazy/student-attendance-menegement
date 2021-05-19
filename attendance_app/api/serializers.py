import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from attendance_app.models import AttendanceReport, Attendance
from course_app.models import Course
from users.models import Student


class StudentRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        try:
            student = self.queryset.get(id=data)
        except Student.DoesNotExist:
            raise serializers.ValidationError(f'Student with this id={data} does not exist')
        return student

    def to_representation(self, instance):
        return "hello"


class AttendanceReportSerializer(serializers.ModelSerializer):
    student_number = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(AttendanceReportSerializer, self).__init__(*args, **kwargs)
        course_id = self.context['course_id']
        course = Course.objects.get(id=course_id)
        queryset = course.students.all()
        self.fields['student_id'] = StudentRelatedField(queryset=queryset, write_only=True)

    class Meta:
        model = AttendanceReport
        fields = ('student_id', 'student_number', 'student', 'status',)

    def get_student(self, obj):
        return obj.student.full_name

    def get_student_number(self, obj):
        return obj.student.id


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
    id = serializers.SerializerMethodField()
    date = serializers.DateField()

    def __init__(self, *args, **kwargs):
        super(AttendanceSerializer, self).__init__(*args, **kwargs)
        kwargs = self.context['kwargs']
        self.fields['reports'] = AttendanceReportSerializer(
            many=True, context={"course_id": kwargs['course_id']})

    def get_id(self, obj):
        return obj.id

    def validate_date(self, value):
        current_date = datetime.date.today()
        if current_date < value:
            raise ValidationError({"message": "Date cannot be future date"})
        if current_date - datetime.timedelta(days=3) > value:
            raise ValidationError({"message": "Date past. Ask from maksnurgazy to change"})
        return value

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        kwargs = self.context['kwargs']
        teacher = self.context['request'].user
        courses = teacher.course_list.all()
        course_id = kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)
        if course not in courses:
            raise ValidationError({"message": f"You don't have permission to - /courses/{course_id}/attendances"})
        date = validated_data['date']
        attendance, created = Attendance.objects.get_or_create(date=date, course=course)
        if created:
            for report in validated_data['reports']:
                AttendanceReport.objects.get_or_create(student=report['student_id'], status=report['status'],
                                                       attendance=attendance)

            data = {
                "date": attendance.date,
                "course": attendance.course.name,
                "created": created
            }
            return data
        else:
            message = {
                'message': f'{course.name} attendance for date: {date} already taken'
            }
            raise ValidationError(message)


class ArduinoSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
