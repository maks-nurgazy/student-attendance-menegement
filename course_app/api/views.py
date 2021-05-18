import json

from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from course_app.api.serializers import CourseSerializer, EnrollmentSerializer, CourseRelatedField, \
    TeacherCourseValidSerializer
from course_app.models import Course, Enrolled, CourseApprove
from student_attendance_management.permissions import StudentsOnly, SupervisorsOnly, TeachersOnly
from users.api.serializers import StudentSerializer, ValidApproveStudentSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentCourseView(ListAPIView):
    permission_classes = (StudentsOnly,)
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        enrolls = user.enrolls
        courses = []
        for enroll in list(enrolls.all()):
            courses.append(enroll.course)
        return courses

    def get(self, request, *args, **kwargs):
        student = request.user
        try:
            course_approve = CourseApprove.objects.get(student=student)
            data = {
                "approved": course_approve.status,
                "courses": CourseSerializer(self.get_queryset(), many=True).data
            }
            return Response(data=data)
        except CourseApprove.DoesNotExist:
            data = {
                "approved": False,
                "message": "Courses not approved yet!"
            }
            return Response(data=data)


class TeacherCourseView(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher = self.request.user
        return teacher.course_list


class CourseStudentsView(ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = (TeachersOnly,)

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        serializer = TeacherCourseValidSerializer(data={"course": course_id}, context={"teacher": self.request.user})
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data['course']
        students = course.students
        return students


class EnrollmentView(APIView):
    permission_classes = (StudentsOnly,)

    def get(self, request, *args, **kwargs):
        student = request.user
        courses = Course.objects.filter(co_class=student.student_profile.st_class)
        response = CourseSerializer(courses, many=True).data
        return Response(response)

    def post(self, request, *args, **kwargs):
        courses = json.loads(request.body)['courses']
        student = request.user
        data = {
            "courses": courses
        }
        serializer = EnrollmentSerializer(data=data, context={"student": student})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data=data)

    def put(self, request, *args, **kwargs):
        response = self.delete(request, *args, **kwargs)
        data = response.data
        if "message" in data:
            return Response(data={"update": False, "message": data['message']})
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        student = request.user
        course_approve = CourseApprove.objects.get(student=student)
        if course_approve.status:
            return Response(data={"deleted": False, "message": "Enroll time finished"})
        else:
            Enrolled.objects.filter(student=student).delete()
            course_approve.delete()
            return Response(data={"deleted": True})


class AdviserCourseApproveView(APIView):
    permission_classes = (SupervisorsOnly,)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        advisor = request.user
        serializer = ValidApproveStudentSerializer(data={"student": id}, context={"advisor": advisor})

        serializer.is_valid(raise_exception=True)
        student = serializer.validated_data['student']
        course_approve, created = CourseApprove.objects.get_or_create(student=student)
        course_approve.status = True
        course_approve.save()
        enrolled = Enrolled.objects.filter(student=student)
        for enroll in enrolled:
            course = enroll.course
            if student not in course.students.all():
                course.students.add(student)
        data = {
            "status": True,
            "is_approved": course_approve.status
        }
        return Response(data=data)
