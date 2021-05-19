from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from student_attendance_management.permissions import SuperUserOnly, AdminOnly
from university_app.api.serializers import DepartmentSerializer, FacultySerializer, UniversitySerializer, \
    ClassSerializer, DepartmentRelatedSerializer
from university_app.models import University, Department, Faculty, Class


class UniversityViewSet(ModelViewSet):
    permission_classes = (SuperUserOnly,)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


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
        return Class.objects.filter(department_id=department_id).order_by('num')

    def list(self, request, *args, **kwargs):
        response = super(ClassViewSet, self).list(request, *args, **kwargs)
        department_id = self.kwargs['department_id']
        department = Department.objects.get(id=department_id)
        data = {
            "department": department.name,
            "classes": response.data
        }
        return Response(data=data)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'department_id': self.kwargs['department_id'],
        }


class FacultyViewSet(ModelViewSet):
    permission_classes = (AdminOnly,)
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def list(self, request, *args, **kwargs):
        response = super(FacultyViewSet, self).list(request, *args, **kwargs)
        university = request.user.admin_profile.university
        data = {
            "university": university.name,
            "faculties": response.data
        }
        return Response(data=data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        faculty = Faculty.objects.get(pk=pk)
        departments = faculty.departments.all()
        print(departments)
        response = DepartmentSerializer(departments, many=True).data
        data = {
            "faculty": faculty.name,
            "departments": response
        }
        return Response(data=data)

    def get_serializer_context(self):
        context = super(FacultyViewSet, self).get_serializer_context()
        context['admin'] = self.request.user
        return context

    def get_queryset(self):
        admin = self.request.user
        university = admin.admin_profile.university
        queryset = Faculty.objects.filter(university=university)
        return queryset
