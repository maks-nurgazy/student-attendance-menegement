from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=30)
    credit = models.SmallIntegerField()
    co_class = models.ForeignKey('university_app.Class', on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField('users.Student', related_name='courses')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.SET_NULL, null=True, related_name='course_list')

    def __str__(self):
        return self.name


class Enrolled(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='enrolls')

    class Meta:
        unique_together = ('course_id', 'student_id')


class CourseApprove(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='course_approve')
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
