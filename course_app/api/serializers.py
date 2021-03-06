from django.db import IntegrityError
from rest_framework import serializers

from course_app.models import Course, Enrolled, CourseApprove
from users.models import Student, Teacher


class CourseRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        try:
            course = self.queryset.get(id=data)
        except Course.DoesNotExist:
            raise serializers.ValidationError(f'Course with id {data} not available for you')
        return course

    def to_representation(self, instance):
        return None


class CourseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'full_name')


class CourseDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'credit', 'co_class', 'teacher', 'students')

    def get_teacher(self, obj):
        return obj.teacher.full_name

    def get_students(self, obj):
        students = obj.students.all()
        return CourseStudentSerializer(students, many=True).data


class CourseSerializer(serializers.ModelSerializer):
    teacher_detail = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'credit', 'co_class', 'teacher', 'teacher_detail')
        extra_kwargs = {
            'teacher': {'write_only': True},
        }

    def get_teacher_detail(self, obj):
        try:
            return obj.teacher.full_name
        except AttributeError:
            return ""


class CourseRelatedSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class EnrollmentSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super(EnrollmentSerializer, self).__init__(*args, **kwargs)
        queryset = Course.objects.filter(co_class=self.context['student'].student_profile.st_class)
        self.fields['courses'] = CourseRelatedField(queryset=queryset, many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        courses = validated_data['courses']
        student = self.context['student']
        approve, created = CourseApprove.objects.get_or_create(student=student)
        res = {
            "status": "Verified" if approve.status else "Not approved",
            "courses": [],
        }
        for course in courses:
            enroll, created = Enrolled.objects.get_or_create(student=student, course=course)
            res['courses'].append(enroll.course.name)
        return res

    def get_co_class(self):
        return self.context['student'].student_profile.st_class


class TeacherCourseValidSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super(TeacherCourseValidSerializer, self).__init__(*args, **kwargs)
        queryset = Course.objects.filter(teacher=self.context['teacher'])
        self.fields['course'] = CourseRelatedField(queryset=queryset)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
