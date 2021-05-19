from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from university_app.exceptions import NotFoundException
from university_app.models import University, Department, Faculty, Class
from users.api.serializers import DepartmentRelatedField


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


class DepartmentRelatedSerializer(serializers.Serializer):
    department = DepartmentRelatedField(queryset=Department.objects.all(), write_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'num')

    def create(self, validated_data):
        department_id = self.context['department_id']
        try:
            department = Department.objects.get(id=department_id)
        except ObjectDoesNotExist:
            raise ValidationError("This department does not exist")
        if department:
            try:
                obj = Class.objects.create(**validated_data, department=department)
            except IntegrityError:
                raise ValidationError("This class already exists")
            return obj
        else:
            raise NotFoundException()

    def update(self, instance, validated_data):
        instance.num = validated_data.get('num', instance.num)
        instance.save()
        return instance


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name')

    def create(self, validated_data):
        admin = self.context['admin']
        university = admin.admin_profile.university
        return Faculty.objects.create(**validated_data, university=university)
