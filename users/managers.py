from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Manager
from django.utils.translation import ugettext_lazy as _

import users.models


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
        super_user.roles.add(5)

        return super_user

    def create_student(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        student = self.create_user(email, password, **extra_fields)
        student.roles.add(4)
        users.models.StudentProfile.objects.create(user=student)
        return student

    def create_teacher(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        department = extra_fields.pop("department")
        teacher = self.create_user(email, password, **extra_fields)
        teacher.roles.add(3)
        users.models.TeacherProfile.objects.create(user=teacher, department=department)
        return teacher

    def create_advisor(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        co_class = extra_fields.pop("co_class")
        advisor, created = users.models.User.objects.get_or_create(email=email, **extra_fields)
        if created:
            advisor.set_password(password)
            advisor.save(using=self._db)
        advisor.roles.add(2)
        users.models.AdvisorProfile.objects.get_or_create(user=advisor, co_class=co_class)
        return advisor

    def create_admin(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        university = extra_fields.pop("university")
        admin, created = users.models.User.objects.get_or_create(email=email, **extra_fields)
        if created:
            admin.set_password(password)
            admin.save(using=self._db)
        admin.roles.add(1)
        users.models.AdminProfile.objects.get_or_create(user=admin, university=university)
        return admin


class TeacherManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(roles__in=[3])


class AdvisorManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(roles__in=[2])


class StudentManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(roles__in=[4])
