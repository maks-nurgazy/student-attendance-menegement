from rest_framework import serializers

from university_app.exceptions import NotFoundException
from university_app.models import University, Department, Faculty, Class


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id', 'name')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')

    def create(self, validated_data):
        faculty_id = self.context['faculty_id']
        faculty = Faculty.objects.get(id=faculty_id)
        if faculty:
            return Department.objects.create(**validated_data, faculty=faculty)
        else:
            raise NotFoundException()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'num')

    def create(self, validated_data):
        department_id = self.context['department_id']
        department = Department.objects.get(id=department_id)
        if department:
            return Class.objects.create(**validated_data, department=department)
        else:
            raise NotFoundException()

    def update(self, instance, validated_data):
        instance.num = validated_data.get('num', instance.num)
        instance.save()
        return instance


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'university')
