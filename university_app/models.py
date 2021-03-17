from django.db import models


class University(models.Model):
    name = models.CharField(max_length=50, verbose_name='university')


class Department(models.Model):
    name = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculties')


