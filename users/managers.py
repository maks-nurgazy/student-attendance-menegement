from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Manager
from django.utils.translation import ugettext_lazy as _


class AdminManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        super_user = self.create_user(email, password, **extra_fields)
        super_user.roles.add(1)

        return super_user

    def create_student(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        student = self.create_user(email, password, **extra_fields)
        student.roles.add(4)

        return student

    def create_teacher(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        teacher = self.create_user(email, password, **extra_fields)
        teacher.roles.add(3)

        return teacher


class TeacherManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(roles__in=[3])


class StudentManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(roles__in=[4])
