from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from users.models import User, Teacher, Student
from university_app.models import Department, Class
from rest_framework_simplejwt.tokens import RefreshToken


class DepartmentRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        department_id = data
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError('Department with this id does not exist')
        return department

    def to_representation(self, instance):
        return "hello"


class ClassRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        try:
            st_class = Class.objects.get(id=data)
        except Class.DoesNotExist:
            raise serializers.ValidationError('Class with this id does not exist')
        return st_class

    def to_representation(self, instance):
        return "hello"


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    department = DepartmentRelatedField(queryset=Department.objects.all(), write_only=True)
    st_class = ClassRelatedField(queryset=Class.objects.all(), write_only=True)

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'department', 'st_class')

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
        department = validated_data.pop('department')
        st_class = validated_data.pop('st_class')
        user = User.objects.create_student(**validated_data)
        st_class = Class.objects.get(num=st_class.id, department=department)
        profile = user.profile
        profile.st_class = st_class
        profile.save()
        return user


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
            refresh = RefreshToken.for_user(user=user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.roles.first(),
            }
            return validation
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
