from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from student_attendance_management.permissions import SuperUserOnly, AdminOnly
from university_app.api.serializers import DepartmentSerializer, FacultySerializer, UniversitySerializer, \
    ClassSerializer, DepartmentRelatedSerializer
from university_app.models import University, Department, Faculty, Class


class UniversityView(APIView):
    permission_classes = (SuperUserOnly,)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    def get_object(self):
        obj = University.objects.first()
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        return Response({})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        obj = self.get_object()
        obj.name = serializer.validated_data['name']
        obj.save()
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        University.objects.first().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentViewSet(ModelViewSet):
    permission_classes = (AdminOnly,)
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        faculty_id = self.kwargs['faculty_id']
        return Department.objects.filter(faculty_id=faculty_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'faculty_id': self.kwargs['faculty_id'],
        }


class ClassViewSet(ModelViewSet):
    permission_classes = (AdminOnly,)
    serializer_class = ClassSerializer

    def get_queryset(self):
        department_id = self.kwargs['department_id']
        serializer = DepartmentRelatedSerializer(data={"department": department_id})
        serializer.is_valid(raise_exception=True)
        return Class.objects.filter(department_id=department_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'department_id': self.kwargs['department_id'],
        }


class FacultyViewSet(ModelViewSet):
    permission_classes = (AdminOnly,)
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
