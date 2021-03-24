from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Teacher, Student


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)


    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    def get_fields(self, *args, **kwargs):
        fields = super(StudentSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields.pop('password')
        return fields

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create_student(**validated_data)


class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    def get_fields(self, *args, **kwargs):
        fields = super(TeacherSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields.pop('password')
        return fields

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create_teacher(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.roles.first(),
            }
            return validation
        except settings.AUTH_USER_MODEL.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
