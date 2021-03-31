import json

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from course_app.api.serializers import CourseSerializer
from course_app.models import Course, Enrolled
from users.models import Student


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentCourseView(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        enrolls = user.enrolls
        courses = []
        for enroll in list(enrolls.all()):
            courses.append(enroll.course)
        return courses


class EnrollmentView(APIView):

    def get(self, request, *args, **kwargs):
        student = request.user
        courses = Course.objects.filter(co_class=student.profile.st_class)
        response = CourseSerializer(courses, many=True).data
        return Response(response)

    def post(self, request, *args, **kwargs):
        courses = json.loads(request.body)['courses']
        student = request.user
        for course_id in courses:
            Enrolled.objects.create(student=student, course_id=course_id)
        return Response({"detail": "Enrolled"})

    def put(self, request, *args, **kwargs):
        pass
