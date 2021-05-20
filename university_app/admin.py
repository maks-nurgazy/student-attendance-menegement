from django.contrib import admin

from university_app.models import Faculty, University, Department, Class


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass
