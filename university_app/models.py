from django.db import models


class University(models.Model):
    name = models.CharField(max_length=50, verbose_name='university', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"


class Faculty(models.Model):
    name = models.CharField(max_length=50, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Faculties"


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name


class Class(models.Model):
    num = models.PositiveSmallIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classes')

    class Meta:
        unique_together = [['num', 'department']]

    def __str__(self):
        return f'{self.num} course'
