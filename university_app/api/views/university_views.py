from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from university_app.api.serializers.university_serializers import UniversitySerializer, DepartmentSerializer, \
    FacultySerializer
from university_app.models import University, Department, Faculty


class UniversityView(APIView):
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
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        faculty_id = self.kwargs['faculty_id']
        return Department.objects.filter(faculty_id=faculty_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'faculty_id': self.kwargs['faculty_id'],
        }


class FacultyViewSet(ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
