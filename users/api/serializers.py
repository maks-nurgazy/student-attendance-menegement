from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from course_app.models import Course, Enrolled
from users.models import User, Teacher, Student, Advisor, StudentProfile, Admin
from university_app.models import Department, Class, University
from rest_framework_simplejwt.tokens import RefreshToken


class DepartmentRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        department_id = data
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError('This Department does not exist')
        return department

    def to_representation(self, instance):
        return instance.id


class ClassRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        try:
            st_class = Class.objects.get(id=data)
        except Class.DoesNotExist:
            raise serializers.ValidationError('Class with this id does not exist')
        return st_class

    def to_representation(self, instance):
        return instance.id


class UniversityRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        try:
            university = University.objects.get(id=data)
        except University.DoesNotExist:
            raise serializers.ValidationError('University with this id does not exist')
        return university

    def to_representation(self, instance):
        return instance.id


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    department = DepartmentRelatedField(queryset=Department.objects.all(), write_only=True)
    st_class = ClassRelatedField(queryset=Class.objects.all(), write_only=True)
    info = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'department', 'st_class', 'info')

    def validate(self, attrs):
        st_class = attrs['st_class']
        department = attrs['department']
        try:
            Class.objects.get(num=st_class.id, department=department)
        except ObjectDoesNotExist:
            raise ValidationError(f'Class {st_class.num} does not exists in this department')
        return attrs

    def get_info(self, obj):
        profile = obj.student_profile
        data = {
            "class": profile.st_class.num,
            "department": profile.st_class.department.name
        }
        return data

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
        profile = user.student_profile
        profile.st_class = st_class
        profile.save()
        return user


class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    department = DepartmentRelatedField(queryset=Department.objects.all(), write_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'department')

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
        instance.teacher_profile.department = validated_data.get('department', instance.teacher_profile.department)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create_teacher(**validated_data)


class AdvisorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=128)
    co_class = ClassRelatedField(queryset=Class.objects.all(), write_only=True)
    meta = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Advisor
        fields = ('id', 'first_name', 'last_name', 'email', 'password', "co_class", "meta")

    def get_fields(self, *args, **kwargs):
        fields = super(AdvisorSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields.pop('password')
        return fields

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.advisor_profile.co_class = validated_data.get('co_class', instance.advisor_profile.co_class)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create_advisor(**validated_data)

    def get_meta(self, obj):
        co_class = obj.advisor_profile.co_class
        data = {
            "department": co_class.department.name,
            "class": co_class.num
        }
        return data


class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=128)
    university = UniversityRelatedField(queryset=University.objects.all(), write_only=True)
    university_detail = serializers.SerializerMethodField()

    class Meta:
        model = Admin
        fields = ('id', 'first_name', 'last_name', 'email', 'password', "university", 'university_detail')

    def get_fields(self, *args, **kwargs):
        fields = super(AdminSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields.pop('password')
        return fields

    def get_university_detail(self, obj):
        university = obj.admin_profile.university
        return university.name

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return User.objects.create_admin(**validated_data)


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


class AdvisorStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class StudentRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        try:
            student = self.queryset.get(id=data)
        except Student.DoesNotExist:
            raise serializers.ValidationError('Student with this id does not exist')
        return student

    def to_representation(self, instance):
        return "hello"


class ValidApproveStudentSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def __init__(self, *args, **kwargs):
        super(ValidApproveStudentSerializer, self).__init__(*args, **kwargs)
        user = self.context['advisor']
        profile = user.advisor_profile
        co_class = profile.co_class
        prof_students = co_class.students
        queryset = Student.objects.filter(student_profile__in=prof_students.all())
        self.fields['student'] = StudentRelatedField(queryset=queryset)


class StudentCourseSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    class_number = serializers.SerializerMethodField("get_class")

    class Meta:
        model = Course
        fields = ('name', 'teacher', 'credit', 'class_number',)

    def get_teacher(self, obj):
        teacher = obj.teacher
        return teacher.full_name

    def get_class(self, obj):
        return obj.co_class.num


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('gender', 'father', 'mother', 'image')


class AdvisorStudentDetailSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile', 'course')

    def get_course(self, obj):
        try:
            enrolled = Enrolled.objects.filter(student=obj)
            courses = []
            total_credit = 0
            for enroll in enrolled:
                course = enroll.course
                courses.append(course)
                total_credit += course.credit
            data = StudentCourseSerializer(courses, many=True).data
            data = {
                "total_credit": total_credit,
                "total_subject": len(courses),
                "course_data": data
            }
            return data
        except Exception as e:
            raise ValidationError({'message': e})

    def get_profile(self, obj):
        profile = obj.student_profile
        data = StudentProfileSerializer(profile).data
        return data
