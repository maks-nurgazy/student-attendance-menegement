from django.contrib import admin

from university_app.models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass
