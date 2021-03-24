from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

from users.managers import TeacherManager, StudentManager, AdminManager


class Role(models.Model):
    ADMIN = 1
    SUPERVISOR = 2
    TEACHER = 3
    STUDENT = 4

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (SUPERVISOR, 'Supervisor'),
        (STUDENT, 'Student'),
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


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True


def profile_img_dir(instance, filename):
    return f'profile/{filename}'


class StudentProfile(models.Model):
    class YearInUniversity(models.TextChoices):
        FRESHMAN = 1, _('Freshman')
        SOPHOMORE = 2, _('Sophomore')
        JUNIOR = 3, _('Junior')
        SENIOR = 4, _('Senior')
        GRADUATE = 5, _('Graduate')

    year_in_university = models.SmallIntegerField(
        choices=YearInUniversity.choices,
        default=YearInUniversity.FRESHMAN,
    )

    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), default='G')
    father = models.CharField(max_length=30, default='non')
    mother = models.CharField(max_length=30, default='non')
    image = models.ImageField(upload_to=profile_img_dir, default='profile/default.png')

    def save(self, *args, **kwargs):
        super(StudentProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            size = (300, 300)
            img.thumbnail(size)
            img.save(self.image.path)

    def is_upperclass(self):
        return self.year_in_university in {
            self.YearInUniversity.JUNIOR,
            self.YearInUniversity.SENIOR,
        }
