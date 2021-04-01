from django.db import models
from django.utils import timezone


def current_time():
    return timezone.now()


def get_status_in_string(status):
    if status:
        return "Present"
    else:
        return "Absent"


class Attendance(models.Model):
    date = models.DateField(default=current_time)
    course = models.ForeignKey('course_app.Course', on_delete=models.CASCADE, related_name='attendances')

    def __str__(self):
        return f'{self.course.name} {self.date}'


class AttendanceReport(models.Model):
    attendance = models.ForeignKey('Attendance', on_delete=models.CASCADE, related_name='reports')
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} {get_status_in_string(self.status)}'
