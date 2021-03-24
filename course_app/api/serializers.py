from rest_framework import serializers

from course_app.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'credit', 'desc', 'teacher',)


class CourseRelatedSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class EnrollmentSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
