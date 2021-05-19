from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import TeacherManager, StudentManager, AdminManager, AdvisorManager


class Role(models.Model):
    ADMIN = 1
    SUPERVISOR = 2
    TEACHER = 3
    STUDENT = 4
    SUPERUSER = 5

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (SUPERVISOR, 'Supervisor'),
        (STUDENT, 'Student'),
        (SUPERUSER, 'Superuser'),
    )
    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    roles = models.ManyToManyField(Role)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    objects = AdminManager()

    def __str__(self):
        return self.email


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True


class Advisor(User):
    objects = AdvisorManager()

    class Meta:
        proxy = True


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True


def profile_img_dir(instance, filename):
    return f'profile/{filename}'


class StudentProfile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_profile')
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), default='G')
    father = models.CharField(max_length=30, default='non')
    mother = models.CharField(max_length=30, default='non')
    image = models.ImageField(upload_to=profile_img_dir, default='profile/default.png')
    st_class = models.ForeignKey('university_app.Class', on_delete=models.SET_NULL, null=True, related_name="students")

    def save(self, *args, **kwargs):
        super(StudentProfile, self).save(*args, **kwargs)
        save_image(self)

    def __str__(self):
        return f'{self.user.full_name}-profile'


class TeacherProfile(models.Model):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name='teacher_profile')
    image = models.ImageField(upload_to=profile_img_dir, default='profile/default.png')
    department = models.ForeignKey('university_app.Department', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super(TeacherProfile, self).save(*args, **kwargs)
        save_image(self)

    def __str__(self):
        return f'{self.user.full_name}-profile'


class AdvisorProfile(models.Model):
    user = models.OneToOneField(Advisor, on_delete=models.CASCADE, related_name='advisor_profile')
    image = models.ImageField(upload_to=profile_img_dir, default='profile/default.png')
    co_class = models.ForeignKey('university_app.Class', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super(AdvisorProfile, self).save(*args, **kwargs)
        save_image(self)

    def __str__(self):
        return f'{self.user.full_name}-profile'


class AdminProfile(models.Model):
    user = models.OneToOneField(Advisor, on_delete=models.CASCADE, related_name='admin_profile')
    university = models.ForeignKey('university_app.University', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.full_name}-profile'


def save_image(self):
    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
        size = (300, 300)
        img.thumbnail(size)
        img.save(self.image.path)
