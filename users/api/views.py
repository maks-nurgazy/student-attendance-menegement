from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from student_attendance_management.permissions import SupervisorsOnly
from users.api.serializers import StudentSerializer, TeacherSerializer, UserLoginSerializer, AdvisorSerializer, \
    AdvisorStudentSerializer, AdvisorStudentDetailSerializer, AdminSerializer
from users.models import Student, Teacher, Advisor, User, Admin


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class AdvisorViewSet(ModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer


class AdminsViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class UserLoginView(GenericAPIView):
    """ User login url """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }
            return Response(response, status=status_code)


class AdvisorStudentsView(ListAPIView):
    permission_classes = (SupervisorsOnly,)
    serializer_class = AdvisorStudentSerializer

    def get_queryset(self):
        user = self.request.user
        profile = user.advisor_profile
        co_class = profile.co_class
        prof_students = co_class.students
        queryset = []
        for prof in prof_students.all():
            queryset.append(prof.user)
        return queryset


class AdvisorStudentsDetailView(RetrieveAPIView):
    permission_classes = (SupervisorsOnly,)
    serializer_class = AdvisorStudentDetailSerializer

    def get_serializer_context(self):
        context = super(AdvisorStudentsDetailView, self).get_serializer_context()
        context['advisor'] = self.request.user
        return context

    def get_queryset(self):
        user = self.request.user
        profile = user.advisor_profile
        co_class = profile.co_class
        prof_students = co_class.students
        users = Student.objects.filter(student_profile__in=prof_students.all())
        return users

    def get_object(self):
        id = self.kwargs['id']
        try:
            obj = self.get_queryset().get(id=id)
            return obj
        except ObjectDoesNotExist:
            raise ValidationError("Does not exist")
