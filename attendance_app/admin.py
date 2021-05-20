from django.contrib import admin

from attendance_app.models import Attendance, AttendanceReport


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    pass
