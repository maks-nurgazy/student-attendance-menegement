from django.contrib import admin

from course_app.models import Course, CourseApprove, Enrolled


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseApprove)
class CourseApproveAdmin(admin.ModelAdmin):
    pass


@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    pass
